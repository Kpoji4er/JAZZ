# Patch Frag/M79 mishap hints: quarter→full ramp + Strength on thrown range.
import csv
from pathlib import Path

root = Path(__file__).resolve().parents[2]

FRAG_ID = "243383619902"
M79_ID = "397383171067"

FRAG_RU = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Взрывается при контакте\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дальность от Силы; чистота — Сила + Ловкость + Взрывчатка, плавно к краю круга (без обрыва на середине)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Поражённые взрывом: гарантированная <color EmStyle>контузия</color>; одна зональная <color EmStyle>травма</color> при уроне ≥ 20 (тяжёлая при ≥ 50% ОЗ)"
)
FRAG_EN = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Explodes on contact\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Strength sets throw range; Strength + Dexterity + Explosives keep it clean, smoothly to the edge (no mid-range cliff)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Units caught in the blast are guaranteed to suffer <color EmStyle>Concussion</color>; one zone <color EmStyle>Trauma</color> if after-armor damage ≥ 20 (heavy at ≥ 50% Max HP)"
)

M79_RU = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 40-мм гранатомёт.\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Риск растёт плавно к полному выстрелу (Меткость + Взрывчатка), без обрыва на середине."
)
M79_EN = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 40 mm grenade launcher.\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Risk rises smoothly toward a full shot (Marksmanship + Explosives), with no mid-range cliff."
)


def patch(path: Path, *, english: bool):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        found = set()
        for row in reader:
            if not row:
                rows.append(row)
                continue
            rid = row[0]
            if rid == FRAG_ID:
                row[1] = FRAG_RU
                row[2] = FRAG_EN if english else FRAG_RU
                found.add(FRAG_ID)
            elif rid == M79_ID:
                row[1] = M79_RU
                row[2] = M79_EN if english else M79_RU
                found.add(M79_ID)
            rows.append(row)
        missing = {FRAG_ID, M79_ID} - found
        if missing:
            raise SystemExit(f"{path.name}: missing IDs {missing}")
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(rows)
    print(f"patched {path.name}")


if __name__ == "__main__":
    patch(root / "Russian.csv", english=False)
    patch(root / "English.csv", english=True)
