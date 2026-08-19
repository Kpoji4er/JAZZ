# -*- coding: utf-8 -*-
"""Quick structural checks for items.lua / metadata.lua (no JA3 required)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOJIBAKE_MARKERS = ("Р”Р", "РµР", "РѕР", "С‚Р", "СЂР", "вЂ", "в†", "в‰", "Г—")


def missing_comma_before_placeobj(text: str, name: str) -> list[str]:
    """Catch `})\\nPlaceObj` without comma — Mod Editor: `'}' expected ... near 'PlaceObj'`."""
    problems: list[str] = []
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        s = ln.rstrip()
        if not (s.endswith("})") or (s.endswith("}") and not s.endswith("},"))):
            continue
        if s.endswith("}),") or s.endswith("},") or s.endswith("),"):
            continue
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and lines[j].lstrip().startswith("PlaceObj("):
            problems.append(
                f"{name}: L{i+1} closes without comma before PlaceObj at L{j+1}"
            )
    return problems


def raw_newlines_in_quoted_strings(text: str, name: str, limit: int = 5) -> list[str]:
    """Catch illegal raw CR/LF inside '...' / \"...\" (Lua long strings [[ ]] are OK).

    Typical failure: a Python/theme script or editor paste turns `\\n\\n` into real
    newlines inside a T(...) default — entire items.lua then fails to load.
    """
    problems: list[str] = []
    i = 0
    n = len(text)
    line = 1
    while i < n and len(problems) < limit:
        c = text[i]
        if c == "\n":
            line += 1
            i += 1
            continue
        if c == "-" and i + 1 < n and text[i + 1] == "-":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c in ("'", '"'):
            q = c
            start_line = line
            i += 1
            while i < n:
                c2 = text[i]
                if c2 == "\\" and i + 1 < n:
                    i += 2
                    continue
                if c2 in ("\n", "\r"):
                    problems.append(
                        f"{name}: L{start_line} raw newline inside {q}...{q} string "
                        "(use \\\\n escapes; file will not load in JA3)"
                    )
                    j = i
                    while j < n and j < i + 800 and text[j] != q:
                        if text[j] == "\n":
                            line += 1
                        j += 1
                    i = j + 1 if j < n and text[j] == q else i + 1
                    break
                if c2 == q:
                    i += 1
                    break
                i += 1
            continue
        if c == "[" and i + 1 < n and text[i + 1] == "[":
            i += 2
            while i + 1 < n and not (text[i] == "]" and text[i + 1] == "]"):
                if text[i] == "\n":
                    line += 1
                i += 1
            i = min(i + 2, n)
            continue
        i += 1
    return problems


def check(path: Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    head = text.lstrip()[:80]
    if path.name == "metadata.lua":
        if not (head.startswith("return PlaceObj") or head.startswith("PlaceObj") or "'id'" in head[:200]):
            # ModDef / metadata may start with return PlaceObj('ModDef'...
            if "ModDef" not in text[:500] and "ModContent" not in text[:500]:
                problems.append(f"{path.name}: unexpected start: {head[:40]!r}")
        for marker in MOJIBAKE_MARKERS:
            if marker in text:
                line = text.count("\n", 0, text.index(marker)) + 1
                problems.append(
                    f"{path.name}: L{line} likely UTF-8/Windows-1251 mojibake "
                    f"{marker!r} (run _fix_metadata_utf8_mojibake.py --check)"
                )
                break
    elif not (head.startswith("return {") or head.startswith("return PlaceObj")):
        problems.append(f"{path.name}: unexpected start")
    lone = [i for i, ln in enumerate(text.splitlines(), 1) if ln.strip() == ","]
    if lone:
        problems.append(f"{path.name}: {len(lone)} lone-comma lines (e.g. {lone[:5]})")
    if "}),)," in text or re.search(r"\}\),\s*\),", text):
        problems.append(f"{path.name}: stacked closers" + " }),),")
    # Exact `}),,` (MagSizeSet split artifact). Avoid `\s*,` — false-positives on normal `}),\n...`.
    if "}),," in text:
        problems.append(f"{path.name}: double-comma after closer" + " }),,")
    if "\\1" in text:
        problems.append(f"{path.name}: regex-replace artifact \\1")
    brace = text.count("{") - text.count("}")
    if brace != 0:
        problems.append(f"{path.name}: brace imbalance {brace}")
    problems.extend(missing_comma_before_placeobj(text, path.name))
    problems.extend(raw_newlines_in_quoted_strings(text, path.name))
    # FunctionObject/Condition StoreAsTable=true: 'Difficulty', "X" asserts at load
    if path.name == "items.lua":
        cd_false = len(
            re.findall(r"PlaceObj\('CheckDifficulty',\s*\{\s*'Difficulty',", text)
        )
        if cd_false:
            problems.append(
                f"{path.name}: {cd_false} CheckDifficulty StoreAsTable-false props "
                f"(use Difficulty = \"...\"; see _fix_checkdifficulty_storeastable.py)"
            )
    # Corrupt id lines from partial MagLarge_50_AK remove / bad insert
    for i, ln in enumerate(text.splitlines(), 1):
        s = ln.strip()
        if re.match(r"^id\s*=\s*\}\),?\s*$", s) or re.match(r"^id\s*=\s*,?\s*$", s):
            problems.append(f"{path.name}: L{i} corrupt id line: {s!r}")
    return problems


def _code_load_problems(root: Path) -> list[str]:
    """Fail if intended Code/*.lua is missing from metadata.code or ModItemCode.

    Editor SaveDef rebuilds metadata.code from items.lua. A file only in
    metadata.code is dropped on the next resave (Steam 0.19-6183 inventory crash).
    """
    if not (root / "Code").is_dir():
        return []
    cov_path = Path(__file__).with_name("_audit_metadata_code_coverage.py")
    if not cov_path.exists() or root.resolve() != ROOT.resolve():
        return []
    import importlib.util

    spec = importlib.util.spec_from_file_location("jazz_code_cov", cov_path)
    if spec is None or spec.loader is None:
        return []
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(mod.coverage_problems(root))


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    roots = [Path(a) for a in argv] if argv else [ROOT]
    problems: list[str] = []
    for root in roots:
        root = root.resolve()
        for name in ("items.lua", "metadata.lua"):
            path = root / name
            if not path.exists():
                problems.append(f"{path}: missing")
                continue
            probs = check(path)
            # prefix with package folder for multi-root runs
            label = root.name
            problems.extend(f"[{label}] {p}" if len(roots) > 1 or root != ROOT.resolve() else p for p in probs)
        cov = _code_load_problems(root)
        if len(roots) > 1 or root != ROOT.resolve():
            problems.extend(f"[{root.name}] {p}" for p in cov)
        else:
            problems.extend(cov)
    if problems:
        print("FAIL")
        for p in problems:
            print(" -", p)
        return 1
    checked = ", ".join(str(r) for r in roots)
    print(f"OK items.lua + metadata.lua structural checks ({checked})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
