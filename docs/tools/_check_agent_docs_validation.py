"""Exercise the real documentation validator against an isolated temporary suite."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    validator = Path(__file__).resolve().parents[2] / '.agents/skills/document-jazz-systems/scripts/check-system-docs.ps1'
    shell = shutil.which('pwsh') or shutil.which('powershell')
    if not shell:
        raise SystemExit('PowerShell is required')
    with tempfile.TemporaryDirectory(prefix='jazz-doc-validator-') as temp:
        root = Path(temp) / 'jazz'

        def write(name, content='fixture\n'):
            file = root / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(content, encoding='utf-8')

        for name in ['docs/specs/README.md', 'docs/specs/_template/change.md',
                     'docs/decisions/README.md', 'docs/ownership/README.md',
                     'docs/ownership/exclusive-resources.yaml', 'docs/technical/README.md',
                     'docs/technical/systems/README.md', 'docs/technical/systems/file-coverage.md',
                     'docs/wiki/README.md', 'docs/showcase/README.md',
                     'docs/showcase/ru/sample.md', 'docs/showcase/en/sample.md',
                     'scripts/docs/publish-github-wiki.ps1']:
            write(name)
        write('docs/README.md', '\n'.join(f'{name}/README.md' for name in
              ['specs', 'decisions', 'ownership', 'technical', 'wiki', 'showcase']) + '\n')
        write('docs/showcase/pages.json', json.dumps({'order': ['sample'], 'pages': {
            'sample': {'wikiBase': 'sample', 'ru': 'sample', 'en': 'sample'}}}))
        skill = '.agents/skills/sample/SKILL.md'
        yaml = '.agents/skills/sample/agents/openai.yaml'
        write(skill, '---\nname: sample\ndescription: A sample fixture skill.\n---\n\nBody.\n')
        write('docs/clean.md')

        def run(label, paths=None, ok=True, needle=None):
            # PowerShell single-quoted literals, including apostrophes in temp paths.
            quote = lambda value: "'" + str(value).replace("'", "''") + "'"
            command = f'& {quote(validator)} -SuiteRoot {quote(root)}'
            if paths is not None:
                command += ' -Paths @(' + ','.join(map(quote, paths)) + ')'
            result = subprocess.run([shell, '-NoProfile', '-NonInteractive', '-Command', command],
                                    capture_output=True, encoding='utf-8', errors='replace')
            output = result.stdout + result.stderr
            assert (result.returncode == 0) == ok, (label, output)
            if needle:
                assert needle in output, (label, output)
            print(f'PASS: {label}')

        run('full clean, optional YAML absent')
        run('local skill without YAML', [skill], needle='global coverage/index/showcase checks NOT RUN')
        write(yaml, 'interface:\n  default_prompt: "Use $sample"\n')
        run('existing valid UI metadata', [yaml])
        write(yaml, 'interface:\n  default_prompt: broken\n')
        run('invalid existing UI metadata', [skill], ok=False)
        write(yaml, 'interface:\n  default_prompt: "Use $sample"\n')
        write('docs/broken.md', '[missing](absent.md)\n')
        run('local ignores unrelated defect', ['docs/clean.md'])
        run('selected broken link fails', ['docs/broken.md'], ok=False)
        run('full retains broken-link check', ok=False)
        run('missing path fails', ['docs/absent.md'], ok=False)
        run('outside path fails', ['../outside.md'], ok=False)
        run('empty selection fails', [], ok=False)
        run('unsupported selection fails', ['docs/showcase/pages.json'], ok=False)


if __name__ == '__main__':
    main()
