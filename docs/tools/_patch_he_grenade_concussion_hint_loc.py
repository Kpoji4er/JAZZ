from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = (
    "663236691841,<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> "
    "Взрывается при контакте,<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> "
    "Взрывается при контакте,,mag-hint-aligned"
)
NEW = (
    '663236691841,"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Взрывается при контакте\n'
    '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В центре взрыва: шанс <color EmStyle>контузии</color> и зональных <color EmStyle>травм</color>",'
    '"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Взрывается при контакте\n'
    '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В центре взрыва: шанс <color EmStyle>контузии</color> и зональных <color EmStyle>травм</color>",,mag-hint-aligned'
)

for name in ("Russian.csv", "English.csv"):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    idx = text.find("663236691841")
    if idx < 0:
        raise SystemExit(f"missing HE id in {name}")
    window = text[idx : idx + 500]
    if "контузии" in window:
        print(f"{name}: HE already patched")
        continue
    if OLD not in text:
        raise SystemExit(f"{name}: old HE line missing")
    path.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print(f"{name}: HE hint patched")
