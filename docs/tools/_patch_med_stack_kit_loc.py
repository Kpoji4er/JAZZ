# -*- coding: utf-8 -*-
"""Patch MED kit stack hints in Russian.csv / English.csv."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REPLACEMENTS = [
    ("Consumed on use; refill with Meds", "One use = one item from the stack"),
    ("Тратится; рефил из Meds", "Один юз = одна штука из стака"),
]

HINT_EN = (
    '890000000010030,"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores lost HP and stabilizes dying characters\n'
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Required for Bandage\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage restores 60% more HP\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n"
    '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory",'
    '"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores lost HP and stabilizes dying characters\n'
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Required for Bandage\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage restores 60% more HP\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n"
    '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory",,jazz:stack-kits\n'
)

HINT_RU = (
    '890000000010030,"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores lost HP and stabilizes dying characters\n'
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Required for Bandage\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage restores 60% more HP\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n"
    '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory",'
    '"<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает потерянные ОЗ и стабилизирует умирающих\n'
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нужен для перевязки\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Перевязка восстанавливает на 60% больше ОЗ\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Один юз = одна штука из стака\n"
    '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически из инвентаря",,jazz:stack-kits\n'
)


def main() -> None:
    for name, append in (("English.csv", HINT_EN), ("Russian.csv", HINT_RU)):
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if "890000000010030" not in text:
            if not text.endswith("\n"):
                text += "\n"
            text += append
        path.write_text(text, encoding="utf-8")
        print("ok", name)


if __name__ == "__main__":
    main()
