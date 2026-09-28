"""Read ModItem scalar properties without depending on serializer whitespace.

Lexical scan only: never evaluates Lua. JSON stdout for check-generated-sync.ps1.
"""
import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(r'''--\[(=*)\[.*?\]\1\]|--[^\n]*|\[(=*)\[.*?\]\2\]|"(?:\\.|[^\\"])*"|'(?:\\.|[^\\'])*'|[A-Za-z_][A-Za-z_0-9]*|[^\s]''', re.S)


def records(text):
    tokens = [(m.group(), m.start()) for m in TOKEN.finditer(text)
              if not m.group().startswith('--')]
    stack = []
    result = []
    fields = {'Id': 'Id', 'id': 'Id', 'name': 'Name',
              'entity_name': 'EntityName', 'CodeFileName': 'CodeFileName'}
    for i, (token, offset) in enumerate(tokens):
        if token == '{':
            record = None
            if i >= 4 and [t[0] for t in tokens[i-4:i-2]] == ['PlaceObj', '('] and tokens[i-1][0] == ',':
                cls = tokens[i-2][0][1:-1]
                if cls.startswith('ModItem'):
                    record = dict(Class=cls, Id=None, Name=None, EntityName=None, CodeFileName=None, Offset=tokens[i-4][1])
                    result.append(record)
            stack.append(record)
        elif token == '}':
            if not stack:
                raise ValueError('Unmatched closing brace at ' + str(offset))
            stack.pop()
        elif stack and stack[-1] is not None and i + 2 < len(tokens):
            # Properties start immediately after the table opening or a separator.
            if tokens[i-1][0] not in ('{', ',', ';'):
                continue
            key = token[1:-1] if token.startswith(('"', "'")) else token
            separator, value = tokens[i+1][0], tokens[i+2][0]
            if key in fields and separator in (',', '=') and value.startswith(('"', "'")):
                stack[-1][fields[key]] = value[1:-1]
    if stack:
        raise ValueError('Unclosed table in items.lua')
    return result


if __name__ == '__main__':
    print(json.dumps(records(Path(sys.argv[1]).read_text(encoding='utf-8-sig')), ensure_ascii=True))
