# Patch Frag/HE AdditionalHint loc: chance concussion -> guaranteed.
# Updates Russian.csv + English.csv (RU source + EN translation columns).
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

OLD_RU = (
    "В центре взрыва: шанс <color EmStyle>контузии</color> "
    "и зональных <color EmStyle>травм</color>"
)
NEW_RU = (
    "Поражённые взрывом: гарантированная <color EmStyle>контузия</color>; "
    "шанс зональных <color EmStyle>травм</color>"
)
NEW_EN = (
    "Blast-hit units: guaranteed <color EmStyle>concussion</color>; "
    "chance of zone <color EmStyle>trauma</color>"
)

IDS = ("243383619902", "663236691841")


def patch_file(path: Path, *, english_col: bool) -> None:
    text = path.read_text(encoding="utf-8")
    if OLD_RU not in text:
        if NEW_RU in text:
            print(f"{path.name}: already patched (RU)")
            return
        raise SystemExit(f"{path.name}: old concussion phrase missing")
    # Always rewrite RU phrase wherever it still appears (both CSV columns may hold RU).
    text = text.replace(OLD_RU, NEW_RU)
    if english_col:
        # English.csv: replace EN column copies that still mirror the (new) RU phrase
        # for these grenade hint IDs only — leave other bilingual rows alone.
        for lid in IDS:
            idx = text.find(lid)
            if idx < 0:
                raise SystemExit(f"{path.name}: missing id {lid}")
            # Window covers the multiline quoted record.
            end = text.find("\n", idx + 1)
            # Multiline: find mag-hint-aligned terminator after id.
            term = text.find(",,mag-hint-aligned", idx)
            if term < 0:
                raise SystemExit(f"{path.name}: no mag-hint terminator for {lid}")
            chunk = text[idx : term + len(",,mag-hint-aligned")]
            # Two quoted fields: RU,EN — both currently NEW_RU after replace; fix EN field.
            # Pattern: "....NEW_RU","....NEW_RU",,mag-hint-aligned
            if chunk.count(NEW_RU) < 2:
                # Maybe EN already different — skip EN rewrite for this id.
                print(f"{path.name}: {lid} EN col not dual-RU after patch; leave as-is")
                continue
            # Replace only the second occurrence of NEW_RU inside this chunk with NEW_EN.
            first = chunk.find(NEW_RU)
            second = chunk.find(NEW_RU, first + len(NEW_RU))
            if second < 0:
                continue
            chunk2 = chunk[:second] + NEW_EN + chunk[second + len(NEW_RU) :]
            text = text[:idx] + chunk2 + text[term + len(",,mag-hint-aligned") :]
    path.write_text(text, encoding="utf-8")
    print(f"{path.name}: patched")


def main() -> None:
    patch_file(ROOT / "Russian.csv", english_col=False)
    patch_file(ROOT / "English.csv", english_col=True)
    for lid in IDS:
        for name in ("Russian.csv", "English.csv"):
            window = (ROOT / name).read_text(encoding="utf-8")
            i = window.find(lid)
            assert i >= 0, lid
            snippet = window[i : i + 700]
            assert "гарантированная" in snippet or "guaranteed" in snippet, (name, lid)
            assert "шанс <color EmStyle>контузии" not in snippet, (name, lid)
    print("OK")


if __name__ == "__main__":
    main()
