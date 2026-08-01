# Apply Steam ignore_files + bump revision for JAZZ suite packages.
# Idempotent for ignore_files block replacement; bumps version once per run.
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods")

IGNORE_BLOCK = """\t'ignore_files', {
\t\t-- VCS / IDE / agent (tracked in git, not for Steam pack)
\t\t\"*.git/*\",
\t\t\"*.svn/*\",
\t\t\"*.github/*\",
\t\t\"*.agents/*\",
\t\t\"*.cursor/*\",
\t\t\"*.tmp/*\",
\t\t\"*codex_worktrees/*\",
\t\t-- Dev docs & tooling (in git, not runtime)
\t\t\"*docs/*\",
\t\t\"*scripts/*\",
\t\t\"*_localization/*\",
\t\t-- Intermediates / backups (also listed in .gitignore)
\t\t\"*__pycache__/*\",
\t\t\"*_review/*\",
\t\t\"*_raw/*\",
\t\t\"*_neural/*\",
\t\t\"*_wip/*\",
\t\t\"*MercPortraits/References/*\",
\t\t\"*MercPortraits/style-ja3-match/*\",
\t\t\"*MercPortraits/newrules2/*\",
\t\t\"*MercPortraits/wip-regen*/*\",
\t\t\"*.psd\",
\t\t\"*.psd/*\",
\t\t\"*.bak\",
\t\t\"*.bak_*\",
\t\t\"*.pyc\",
\t\t\"*.pyo\",
\t\t\"*.zip\",
\t\t\"*.md\",
\t\t\"*.md/*\",
\t\t\"*.ja3-root.local\",
\t\t\"*.gitignore\",
\t\t\"*.gitattributes\",
\t\t\"*Thumbs.db\",
\t\t\"*.DS_Store\",
\t},
"""

LAST_CHANGES_LINE = (
    "- Packaging: expand .gitignore + metadata ignore_files for Steam upload"
)

COMMON_GITIGNORE = """# Local / agent scratch (keep Steam ignore_files in metadata.lua in sync for overlapping patterns)
.agents/cache/
.tmp/
.tmp_*
codex_worktrees/
.ja3-root.local

# Backups & Python
*.bak
*.bak_*
__pycache__/
*.pyc
*.pyo

# Editor / OS
*.psd
Thumbs.db
.DS_Store
"""

PACKAGE_GITIGNORE_EXTRA = {
    "jazz": """
# Dev-only icon review intermediates (not runtime)
Icons/Upgrades/_review/

# Scratch tool outputs
docs/tools/_tmp_*
docs/tools/*_report.txt
docs/tools/_last_validate_wave.txt
""",
    "jazz-units": """
# Local JA3 style references for portrait generation (not shipped)
MercPortraits/References/

# Gen intermediates (opaque raw + rembg neural) — keep finals only
MercPortraits/**/_raw/
MercPortraits/**/_neural/
NPCPortraits/**/_raw/
NPCPortraits/**/_neural/

# Portrait WIP / regen batches (not shipped — ship is MercPortraits/*.png only)
MercPortraits/**/*.zip
MercPortraits/style-ja3-match/
MercPortraits/newrules2/
MercPortraits/wip-regen/
MercPortraits/wip-regen-v4/
MercPortraits/_wip/
""",
    "jazz-maps": """
# Too large for GitHub (>100MB); also excluded via metadata ignore_files *.psd
Images/GrandChienMap.psd
""",
}


def replace_or_insert_ignore_files(text: str) -> str:
    if re.search(r"'ignore_files'\s*,\s*\{", text):
        return re.sub(
            r"\t'ignore_files',\s*\{.*?\n\t\},",
            IGNORE_BLOCK.rstrip("\n"),
            text,
            count=1,
            flags=re.S,
        )
    # Insert before dependencies, else before id, else before code/entities
    for anchor in ("dependencies", "id", "code", "entities", "loctables"):
        needle = f"\t'{anchor}',"
        idx = text.find(needle)
        if idx != -1:
            return text[:idx] + IGNORE_BLOCK + text[idx:]
    raise RuntimeError("no insertion anchor found")


def bump_version(text: str) -> tuple[str, int, int]:
    m = re.search(r"'version',\s*(\d+)", text)
    if not m:
        raise RuntimeError("version field missing")
    old = int(m.group(1))
    new = old + 1
    text = text[: m.start(1)] + str(new) + text[m.end(1) :]
    return text, old, new


def append_last_changes(text: str, line: str) -> str:
    # Prefer double-quoted last_changes (jazz style)
    m = re.search(r"'last_changes',\s*\"((?:\\.|[^\"\\])*)\"", text, re.S)
    quote = '"'
    if not m:
        m = re.search(r"'last_changes',\s*'((?:\\.|[^'\\])*)'", text, re.S)
        quote = "'"
    if not m:
        raise RuntimeError("last_changes missing")
    body = m.group(1)
    if "ignore_files for Steam" in body or "metadata ignore_files" in body:
        return text
    if body and not body.endswith("\\n"):
        body = body + "\\n"
    body = body + line
    return text[: m.start(1)] + body + text[m.end(1) :]


def write_gitignore(pkg: str, path: Path) -> None:
    content = COMMON_GITIGNORE
    extra = PACKAGE_GITIGNORE_EXTRA.get(pkg, "")
    if extra:
        content = content.rstrip() + "\n" + extra.lstrip("\n")
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8", newline="\n")


def detect_newline(raw: bytes) -> str:
    return "\r\n" if raw.count(b"\r\n") >= raw.count(b"\n") // 2 else "\n"


def main() -> None:
    packages = ["jazz", "jazz_assets", "jazz-units", "jazz-maps", "jazz-nomaps"]
    for pkg in packages:
        meta = ROOT / pkg / "metadata.lua"
        raw = meta.read_bytes()
        nl = detect_newline(raw)
        text = raw.decode("utf-8")
        # Normalize to \n for edits, restore on write
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = replace_or_insert_ignore_files(text)
        text = append_last_changes(text, LAST_CHANGES_LINE)
        text, old_v, new_v = bump_version(text)
        out = text.replace("\n", nl)
        if not out.endswith(nl):
            out += nl
        meta.write_bytes(out.encode("utf-8"))
        gi = ROOT / pkg / ".gitignore"
        write_gitignore(pkg, gi)
        # gitignore: LF is fine for all packages
        print(f"{pkg}: version {old_v} -> {new_v}; ignore_files + gitignore OK")


if __name__ == "__main__":
    main()
