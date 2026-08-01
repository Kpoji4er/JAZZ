# Audit/restore AdditionalHint newlines stripped from Russian.csv / English.csv.
# Source of truth for line breaks: InventoryItem/**/*.lua T() defaults (and items.lua).
from __future__ import annotations

import argparse
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]

# AdditionalHint = T(ID, --[[...]] "text with \n")
# AdditionalHint = T(ID, 'text')
HINT_RE = re.compile(
    r"AdditionalHint\s*=\s*T\(\s*(\d+)\s*,\s*(?:--\[\[.*?\]\]\s*)?(['\"])(.*?)\2",
    re.S,
)


def unescape_lua_string(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == "n":
                out.append("\n")
                i += 2
                continue
            if nxt == "t":
                out.append("\t")
                i += 2
                continue
            if nxt in ('"', "'", "\\"):
                out.append(nxt)
                i += 2
                continue
        out.append(s[i])
        i += 1
    return "".join(out)


def collect_lua_hints() -> dict[str, tuple[str, str]]:
    hints: dict[str, tuple[str, str]] = {}
    paths = list(ROOT.joinpath("InventoryItem").rglob("*.lua"))
    items = ROOT / "items.lua"
    if items.exists():
        paths.append(items)
    for p in paths:
        text = p.read_text(encoding="utf-8")
        for m in HINT_RE.finditer(text):
            tid = m.group(1)
            s = unescape_lua_string(m.group(3))
            if "\n" not in s:
                continue
            hints[tid] = (s, str(p.relative_to(ROOT)))
    return hints


def load_csv(path: pathlib.Path) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        raise SystemExit(f"empty csv: {path}")
    return rows[0], rows[1:]


def save_csv(path: pathlib.Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def flatten_spaces(s: str) -> str:
    # Compare ignoring newline-vs-space: CSV often replaced \n with space or nothing.
    return re.sub(r"\s+", " ", s.replace("\r\n", "\n").replace("\r", "\n")).strip()


def restore_newlines_into(csv_text: str, lua_text: str) -> str | None:
    """If csv_text matches lua_text ignoring whitespace/newlines, return lua_text newlines applied to csv content via lua structure."""
    if "\n" in csv_text:
        return None  # already has newlines
    if flatten_spaces(csv_text) != flatten_spaces(lua_text):
        # Try soft match: same bullet tags sequence
        return None
    return lua_text


def soft_restore(csv_text: str, lua_text: str) -> str | None:
    """Insert \\n before each bullet image/tag when CSV lost them but text otherwise matches."""
    if "\n" in csv_text:
        return None
    if flatten_spaces(csv_text) == flatten_spaces(lua_text):
        return lua_text

    # Fallback: split lua by newlines; for each non-first line, ensure preceding \\n in csv
    # by rebuilding from lua when tag sequence matches.
    bullet = "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120>"
    alt_bullet = "<bullet_point>"
    for marker in (bullet, alt_bullet):
        if marker not in lua_text:
            continue
        lua_parts = [p.strip() for p in lua_text.split("\n") if p.strip()]
        csv_flat = flatten_spaces(csv_text)
        rebuilt = []
        rest = csv_flat
        for i, part in enumerate(lua_parts):
            part_flat = flatten_spaces(part)
            idx = rest.find(part_flat)
            if idx < 0:
                rebuilt = []
                break
            rebuilt.append(part)  # use lua part (preserves tags + RU/EN text from lua)
            rest = rest[idx + len(part_flat) :].lstrip()
        if rebuilt and len(rebuilt) == len(lua_parts):
            # Prefer keeping CSV wording if parts equal after flatten; use csv slices
            # Simpler and safer: use lua_text when soft match of concatenated parts equals csv_flat
            if flatten_spaces(" ".join(rebuilt)) == csv_flat or flatten_spaces(lua_text) == csv_flat:
                return "\n".join(rebuilt)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write restored newlines into CSV")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    hints = collect_lua_hints()
    print(f"lua AdditionalHint with \\n: {len(hints)}")

    for name in ("Russian.csv", "English.csv"):
        path = ROOT / name
        header, rows = load_csv(path)
        by_id = {r[0]: r for r in rows if r}
        stripped = []
        already = []
        missing = []
        mismatch = []
        restored = 0
        for tid, (lua_s, src) in sorted(hints.items()):
            if tid not in by_id:
                missing.append((tid, src))
                continue
            row = by_id[tid]
            # columns: ID, Text, Translation, [Sound], [extra]
            while len(row) < 3:
                row.append("")
            text_col = row[1] or ""
            tr_col = row[2] or ""
            targets = []
            if text_col:
                targets.append(1)
            if tr_col:
                targets.append(2)
            if not targets:
                missing.append((tid, src))
                continue

            row_changed = False
            for col in targets:
                cur = row[col]
                if "\n" in cur:
                    already.append(tid)
                    continue
                # Prefer marker-based split (keeps EN/RU CSV wording); fall back to lua text.
                new = insert_nl_before_bullets(cur)
                if new is None:
                    new = soft_restore(cur, lua_s)
                if new is None or new == cur:
                    mismatch.append((tid, src, col, cur[:100]))
                    continue
                row[col] = new
                row_changed = True
            if row_changed:
                restored += 1
                stripped.append((tid, src))

        print(
            f"{name}: already_nl~{len(set(already))} need_fix={len(stripped)} "
            f"mismatch={len(mismatch)} missing_id={len(missing)}"
        )
        show = stripped if args.limit == 0 else stripped[: args.limit]
        for tid, src in show[:15]:
            print(f"  FIX {tid} ({src})")
        for tid, src, col, preview in mismatch[:10]:
            print(f"  MISMATCH {tid} col{col} ({src}): {preview!r}")

        if args.apply and stripped:
            save_csv(path, header, rows)
            print(f"  wrote {path} ({restored} rows updated)")

    return 0


def insert_nl_before_bullets(s: str) -> str | None:
    """Put each bullet marker on its own line (and leading plain text before first bullet)."""
    if "\n" in s:
        return None
    markers = [
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120>",
        "<bullet_point>",
    ]
    for marker in markers:
        if marker not in s:
            continue
        parts = s.split(marker)
        out = []
        if parts[0].strip():
            out.append(parts[0].rstrip())
        for frag in parts[1:]:
            out.append((marker + frag).rstrip())
        out = [p for p in out if p.strip()]
        # Need a real split: 2+ bullets, or plain lead-in + at least one bullet.
        if len(out) >= 2:
            return "\n".join(out)
    return None


if __name__ == "__main__":
    sys.exit(main())
