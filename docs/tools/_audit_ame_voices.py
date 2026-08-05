"""Audit JAZZ_AME_* VoiceResponseId distribution in jazz-units UnitData."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

JU = Path(__file__).resolve().parents[2].parent / "jazz-units"
UD = JU / "UnitData"


def main() -> None:
    c: Counter[str] = Counter()
    details: list[tuple[str, str]] = []
    for p in sorted(UD.glob("JAZZ_AME_*.lua")):
        text = p.read_text(encoding="utf-8")
        vr = "?"
        for line in text.splitlines():
            if "VoiceResponseId" in line:
                vr = line.split("=", 1)[1].strip().rstrip(",").strip('"')
                break
        c[vr] += 1
        details.append((p.stem, vr))

    n = len(details)
    imp = sum(v for k, v in c.items() if k.startswith("IMP_"))
    jazz = sum(v for k, v in c.items() if k.startswith("Jazz_"))
    other = n - imp - jazz
    print(f"total={n}")
    print(f"IMP={imp} ({100 * imp / n:.1f}%)")
    print(f"Jazz_AME={jazz} ({100 * jazz / n:.1f}%)")
    print(f"other={other} ({100 * other / n:.1f}%)")
    print("breakdown:")
    for k, v in c.most_common():
        print(f"  {k}: {v}")
    print("slots:")
    for stem, vr in details:
        print(f"  {stem}: {vr}")


if __name__ == "__main__":
    main()
