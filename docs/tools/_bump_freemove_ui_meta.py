# Bump jazz/metadata.lua: revision +1, prepend Free Move remaining-AP UI last_changes.
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"

BULLET = (
    "- UI: remaining Free Move AP on status icon, tooltip, and merc card [no new game]"
)


def main() -> None:
    text = META.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", text)
    if not m:
        raise SystemExit("version not found")
    old_v = int(m.group(1))
    new_v = old_v + 1
    text = re.sub(r"'version',\s*\d+", f"'version', {new_v}", text, count=1)

    key = "'last_changes', \""
    i = text.find(key)
    if i < 0:
        raise SystemExit("last_changes not found")
    start = i + len(key)
    if text.startswith(BULLET, start):
        print(f"already has bullet; version {old_v}->{new_v}")
    else:
        text = text[:start] + BULLET + "\\n" + text[start:]
        print(f"prepended last_changes; version {old_v}->{new_v}")

    j = start
    end = start
    while j < len(text):
        if text[j] == "\\" and j + 1 < len(text):
            j += 2
            continue
        if text[j] == '"':
            end = j
            break
        j += 1
    value = text[start:end]
    if "\n" in value or "\r" in value:
        raise SystemExit("raw newline inside last_changes")

    META.write_text(text, encoding="utf-8", newline="\n")
    print("OK", META)


if __name__ == "__main__":
    main()
