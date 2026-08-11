# Soften Frag/M79 mishap hints after 90/90 max-range retune.
import csv
from pathlib import Path

root = Path(__file__).resolve().parents[2]

FRAG_ID = "243383619902"
M79_ID = "397383171067"

FRAG_RU_SRC = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Взрывается при контакте\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> До ~¼ дальности только разброс; к половине риск высокий; на максимуме элита (~90) всё ещё кидает уверенно (Ловкость + Взрывчатка; уверенно примерно с 50)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Поражённые взрывом: гарантированная <color EmStyle>контузия</color>; шанс зональных <color EmStyle>травм</color>"
)
FRAG_RU_TR = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Взрывается при контакте\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> До ~¼ дальности только разброс; к половине риск высокий; на максимуме элита (~90) всё ещё кидает уверенно (Ловкость + Взрывчатка; уверенно примерно с 50)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Поражённые взрывом гарантированно получают <color EmStyle>контузию</color>; возможны зональные <color EmStyle>травмы</color>"
)
FRAG_EN = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Explodes on contact\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Within ~1/4 range, only scatter; by half range risk is high; at max range elites (~90) still throw solidly (Dexterity + Explosives; reliable around 50)\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Units caught in the blast are guaranteed to suffer <color EmStyle>Concussion</color> and may suffer location-specific <color EmStyle>Trauma</color>"
)

M79_RU_SRC = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 40-мм гранатомет.\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> До ~¼ дальности только разброс; к половине — высокий риск; на максимуме элита (~90) всё ещё точна (Меткость + Взрывчатка; уверенно примерно с 50)."
)
M79_RU_TR = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 40-мм гранатомёт.\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> До ~¼ дальности только разброс; к половине — высокий риск; на максимуме элита (~90) всё ещё точна (Меткость + Взрывчатка; уверенно примерно с 50)."
)
M79_EN = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 40 mm grenade launcher.\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Within ~1/4 range, only scatter; by half range risk is high; at max range elites (~90) stay accurate (Marksmanship + Explosives; reliable around 50)."
)


def patch(path: Path, *, russian: bool):
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
                row[1] = FRAG_RU_SRC
                row[2] = FRAG_RU_TR if russian else FRAG_EN
                found.add(FRAG_ID)
            elif rid == M79_ID:
                row[1] = M79_RU_SRC
                row[2] = M79_RU_TR if russian else M79_EN
                found.add(M79_ID)
            rows.append(row)
        missing = {FRAG_ID, M79_ID} - found
        if missing:
            raise SystemExit(f"{path.name}: missing IDs {missing}")
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(rows)
    print(f"patched {path.name}")


patch(root / "Russian.csv", russian=True)
patch(root / "English.csv", russian=False)
