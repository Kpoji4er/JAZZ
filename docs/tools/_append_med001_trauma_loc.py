# -*- coding: utf-8 -*-
"""Append MED-001 trauma localization rows to English.csv / Russian.csv."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ENTRIES = [
    (890000000009226, "Arm Trauma (Light)", "Травма рук (лёгкая)"),
    (890000000009227, "Pain when shooting or using arms. No direct accuracy penalty.", "Боль при стрельбе или нагрузке на руки. Без прямого штрафа к точности."),
    (890000000009228, "Arm Trauma (Medium)", "Травма рук (средняя)"),
    (890000000009229, "Accuracy penalty <color EmStyle><cth_penalty>%</color>. Pain when using arms.", "Штраф точности <color EmStyle><cth_penalty>%</color>. Боль при нагрузке на руки."),
    (890000000009230, "Arm Trauma (Heavy)", "Травма рук (тяжёлая)"),
    (890000000009231, "Severe accuracy penalty <color EmStyle><cth_penalty>%</color>. Nearly unable to fight. Pain rises each turn.", "Жёсткий штраф точности <color EmStyle><cth_penalty>%</color>. Почти небоеспособен. Боль растёт каждый ход."),
    (890000000009232, "Leg Trauma (Light)", "Травма ног (лёгкая)"),
    (890000000009233, "Pain when moving. No direct move-cost penalty.", "Боль при движении. Без прямого штрафа к стоимости хода."),
    (890000000009234, "Leg Trauma (Medium)", "Травма ног (средняя)"),
    (890000000009235, "Move cost <color EmStyle>+<move_ap_modifier>%</color>. No Free Move / sprint. Pain when moving.", "Стоимость движения <color EmStyle>+<move_ap_modifier>%</color>. Нет Free Move / спринта. Боль при движении."),
    (890000000009236, "Leg Trauma (Heavy)", "Травма ног (тяжёлая)"),
    (890000000009237, "Move cost <color EmStyle>+<move_ap_modifier>%</color>. Almost immobile. Pain rises each turn.", "Стоимость движения <color EmStyle>+<move_ap_modifier>%</color>. Почти не ходит. Боль растёт каждый ход."),
    (890000000009238, "Rib Trauma (Light)", "Травма рёбер (лёгкая)"),
    (890000000009239, "Pain at the start of the turn. No Tiredness from ribs. No direct AP penalty.", "Боль в начале хода. Без Tired от рёбер. Без прямого −ОД."),
    (890000000009240, "Rib Trauma (Medium)", "Травма рёбер (средняя)"),
    (890000000009241, "Start-of-turn AP <color EmStyle>-<APLoss></color>. No Free Move. Pain at the start of the turn. No Tiredness.", "ОД на старте хода <color EmStyle>-<APLoss></color>. Нет Free Move. Боль в начале хода. Без Tired."),
    (890000000009242, "Rib Trauma (Heavy)", "Травма рёбер (тяжёлая)"),
    (890000000009243, "Start-of-turn AP <color EmStyle>-<APLoss></color>. Combat-ineffective. Pain rises each turn. No Tiredness.", "ОД на старте хода <color EmStyle>-<APLoss></color>. Небоеспособен. Боль растёт каждый ход. Без Tired."),
    (890000000009244, "Head Trauma (Light)", "Травма головы (лёгкая)"),
    (890000000009245, "Pain when aiming or firing. Eye trauma folded into head for v1.", "Боль при прицеливании/стрельбе. Травма глаза в v1 включена в голову."),
    (890000000009246, "Head Trauma (Medium)", "Травма головы (средняя)"),
    (890000000009247, "Sight and accuracy penalties. Pain when aiming or firing.", "Штрафы зрения и точности. Боль при прицеливании/стрельбе."),
    (890000000009248, "Head Trauma (Heavy)", "Травма головы (тяжёлая)"),
    (890000000009249, "Severe sight/accuracy loss. Nearly combat-ineffective. Pain rises each turn.", "Сильная потеря зрения/точности. Почти небоеспособен. Боль растёт каждый ход."),
    (890000000009250, "Burn Trauma (Light)", "Ожоговая травма (лёгкая)"),
    (890000000009251, "Lingering burn after fire. Pain on exertion. Bandage does not clear burns.", "Долг после огня. Боль при нагрузке. Бинт ожог не снимает."),
    (890000000009252, "Burn Trauma (Medium)", "Ожоговая травма (средняя)"),
    (890000000009253, "Moderate burn debt. Pain on exertion. Infection risk deferred.", "Средний ожоговый долг. Боль при нагрузке. Инфекция — позже."),
    (890000000009254, "Burn Trauma (Heavy)", "Ожоговая травма (тяжёлая)"),
    (890000000009255, "Severe burn debt. Pain rises each turn. Infection/hospital clear deferred.", "Тяжёлый ожоговый долг. Боль растёт каждый ход. Инфекция/госпиталь — позже."),
]

ZONE_LIST = [(z, t) for z in ("Arms", "Legs", "Ribs", "Head", "Burn") for t in ("Light", "Medium", "Heavy")]


def esc(s: str) -> str:
    if any(c in s for c in ',"\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def append_csv(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    if "jazz:CharacterEffect/TraumaArmsLight.lua" in text:
        print(f"{path.name}: trauma rows already present")
        return
    lines = []
    for i, (eid, en, ru) in enumerate(ENTRIES):
        val = en if lang == "en" else ru
        z, t = ZONE_LIST[i // 2]
        src = f"jazz:CharacterEffect/Trauma{z}{t}.lua"
        lines.append(f"{eid},{esc(val)},{esc(val)},,{src}")
    path.write_text(text.rstrip("\n") + "\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"{path.name}: appended {len(lines)} rows")


def main() -> None:
    append_csv(ROOT / "English.csv", "en")
    append_csv(ROOT / "Russian.csv", "ru")


if __name__ == "__main__":
    main()
