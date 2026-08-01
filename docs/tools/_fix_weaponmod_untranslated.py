# -*- coding: utf-8 -*-
from pathlib import Path

path = Path("items.lua")
text = path.read_text(encoding="utf-8")
needle = 'Untranslated("<bullet_point> " .. _InternalTranslate(mod.display, mod))'
print("occurrences", text.count(needle))

old = """\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tfor key, mod in sorted_pairs(allData) do
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tif table.find(changes, key) then
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tlines[#lines + 1] = Untranslated(\"<bullet_point> \" .. _InternalTranslate(mod.display, mod))
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tindices[lines[#lines]] = 999
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\telse
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tlines[#lines + 1] = Untranslated(\"<style WeaponModExtraModificationsTransparent>\" .. _InternalTranslate(mod.display, mod) .. \"</style>\")
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tend"""

new = """\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tfor key, mod in sorted_pairs(allData) do
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tlocal body = _InternalTranslate(mod.display, mod)
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tif type(body) ~= \"string\" or not body:find(\"%w\") then
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tgoto jazz_skip_mod_line
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tif table.find(changes, key) then
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tlines[#lines + 1] = T{990002014, \"<bullet_point> <text>\", text = Untranslated(body)}
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tindices[lines[#lines]] = 999
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\telse
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tlines[#lines + 1] = T{990002015, \"<style WeaponModExtraModificationsTransparent><text></style>\", text = Untranslated(body)}
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t::jazz_skip_mod_line::
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tend"""

count = text.count(old)
print("block count", count)
if count == 0:
    raise SystemExit("block not found")
path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")
print("applied")
