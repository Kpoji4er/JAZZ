# Stage items.lua with only Frag/M79 AdditionalHint updates (preserve WIP elsewhere).
from pathlib import Path
import subprocess
import shutil

root = Path(__file__).resolve().parents[2]
items = root / "items.lua"
wip = root / "items.lua.wip_officer"

FRAG_OLD = (
    "'AdditionalHint', T(243383619902, --[[ModItemInventoryItemCompositeDef FragGrenade AdditionalHint]] "
    "\"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Взрывается при контакте\\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> На близкой дистанции только разброс (Ловкость + Взрывчатка; уверенно примерно с 30)\\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Поражённые взрывом: гарантированная <color EmStyle>контузия</color>; шанс зональных <color EmStyle>травм</color>\"),"
)
FRAG_NEW = (
    "'AdditionalHint', T(243383619902, --[[ModItemInventoryItemCompositeDef FragGrenade AdditionalHint]] "
    "\"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Взрывается при контакте\\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> До ~¼ дальности только разброс; к половине риск высокий; на максимуме элита (~90) всё ещё кидает уверенно (Ловкость + Взрывчатка; уверенно примерно с 50)\\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Поражённые взрывом: гарантированная <color EmStyle>контузия</color>; шанс зональных <color EmStyle>травм</color>\"),"
)

M79_OLD = (
    "'AdditionalHint', T(397383171067, --[[ModItemInventoryItemCompositeDef M79 AdditionalHint]] "
    "\"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 40-мм гранатомет.\\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> На близкой дистанции только разброс; шанс провала растёт с дальностью (Меткость + Взрывчатка).\"),"
)
M79_NEW = (
    "'AdditionalHint', T(397383171067, --[[ModItemInventoryItemCompositeDef M79 AdditionalHint]] "
    "\"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 40-мм гранатомет.\\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> До ~¼ дальности только разброс; к половине — высокий риск; на максимуме элита (~90) всё ещё точна (Меткость + Взрывчатка; уверенно примерно с 50).\"),"
)

shutil.copy2(items, wip)
head = subprocess.check_output(["git", "show", "HEAD:items.lua"], cwd=root)
text = head.decode("utf-8")
if FRAG_OLD not in text or M79_OLD not in text:
    raise SystemExit("HEAD items.lua hint anchors not found")
text = text.replace(FRAG_OLD, FRAG_NEW, 1).replace(M79_OLD, M79_NEW, 1)
items.write_text(text, encoding="utf-8", newline="\n")
print("items.lua = HEAD + Frag/M79 hints only; WIP saved to items.lua.wip_officer")
