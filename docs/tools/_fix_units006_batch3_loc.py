# -*- coding: utf-8 -*-
"""Fix batch3 CE/CSV Russian strings (unicode-escape safe)."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CE = ROOT / "CharacterEffect"

PERKS = [
    (
        "MakeThemBleed",
        "\u041f\u0443\u0441\u0442\u044c \u043a\u0440\u043e\u0432\u043e\u0442\u043e\u0447\u0430\u0442",
        "Make Them Bleed",
        "\u0423\u0434\u0430\u0440\u044b \u0432 \u043f\u0430\u0445 \u0438 \u043f\u043e \u0436\u0438\u0432\u043e\u0442\u043d\u044b\u043c \u0432\u044b\u0437\u044b\u0432\u0430\u044e\u0442 \u043a\u0440\u043e\u0432\u043e\u0442\u0435\u0447\u0435\u043d\u0438\u0435. +10% \u0443\u0440\u043e\u043d\u0430 \u0437\u0430 \u043a\u0430\u0436\u0434\u043e\u0433\u043e \u0432\u0440\u0430\u0433\u0430 \u0441 \u043a\u0440\u043e\u0432\u043e\u0442\u0435\u0447\u0435\u043d\u0438\u0435\u043c \u0432 \u0437\u043e\u043d\u0435 \u0432\u0438\u0434\u0438\u043c\u043e\u0441\u0442\u0438 (\u043c\u0430\u043a\u0441. +50%).",
        "Groin and animal hits cause bleeding. +10% damage per bleeding enemy in sight (cap +50%).",
    ),
    (
        "DedicatedCamper",
        "\u041e\u0441\u0435\u0434\u043b\u044b\u0439 \u0441\u0442\u0440\u0435\u043b\u043e\u043a",
        "Dedicated Camper",
        "\u041f\u043e\u043a\u0430 \u043d\u0435 \u0441\u0434\u0432\u0438\u043d\u0443\u043b\u0441\u044f \u0441 \u043c\u0435\u0441\u0442\u0430 \u0432 \u044d\u0442\u043e\u043c \u0445\u043e\u0434\u0443: +25% \u0443\u0440\u043e\u043d\u0430. \u0415\u0441\u043b\u0438 \u0430\u0442\u0430\u043a\u0430 \u043d\u0430\u043d\u0435\u0441\u043b\u0430 \u226525 \u0443\u0440\u043e\u043d\u0430 \u2014 +15 \u0421\u0438\u043b\u044b \u0432\u043e\u043b\u0438 (Grit).",
        "While stationary this turn: +25% damage. Dealing >=25 damage grants +15 Grit.",
    ),
    (
        "TagTeam",
        "\u041f\u0430\u0440\u043d\u044b\u0439 \u0437\u0430\u0445\u043e\u0434",
        "Tag Team",
        "+15% \u0442\u043e\u0447\u043d\u043e\u0441\u0442\u0438 \u043f\u043e \u0446\u0435\u043b\u044f\u043c \u043f\u043e\u0434 Pin Down \u0441\u043e\u044e\u0437\u043d\u0438\u043a\u0430.",
        "+15% chance to hit vs targets under an ally's Pin Down.",
    ),
    (
        "BunsPerk",
        "\u0414\u043e\u0431\u0438\u0442\u044c",
        "Finish Them",
        "+10% \u0442\u043e\u0447\u043d\u043e\u0441\u0442\u0438 \u043f\u043e \u0446\u0435\u043b\u044f\u043c, \u043a\u043e\u0442\u043e\u0440\u044b\u0445 \u0432 \u044d\u0442\u043e\u043c \u0445\u043e\u0434\u0443 \u0443\u0436\u0435 \u0440\u0430\u043d\u0438\u043b \u0441\u043e\u044e\u0437\u043d\u0438\u043a.",
        "+10% chance to hit vs targets already damaged by an ally this turn.",
    ),
    (
        "HawksEye",
        "\u042f\u0441\u0442\u0440\u0435\u0431\u0438\u043d\u044b\u0439 \u0433\u043b\u0430\u0437",
        "Hawk's Eye",
        "Pin Down / Focus Fire \u0441\u0442\u043e\u0438\u0442 1 \u041e\u0414. \u0421\u043d\u0430\u0439\u043f\u0435\u0440\u0441\u043a\u0438\u0435 \u0430\u0442\u0430\u043a\u0438 \u0434\u0430\u044e\u0442 \u0432\u0434\u0432\u043e\u0435 \u0431\u043e\u043b\u044c\u0448\u0435 \u043f\u043e\u0434\u0430\u0432\u043b\u0435\u043d\u0438\u044f. \u041f\u0435\u0447\u0435\u043d\u044c\u0435 \u043f\u0440\u0438\u043b\u0430\u0433\u0430\u0435\u0442\u0441\u044f.",
        "Pin Down / Focus Fire costs 1 AP. Sniper attacks apply double suppression. Biscuits included.",
    ),
    (
        "Spotter",
        "\u041d\u0430\u0432\u043e\u0434\u0447\u0438\u043a",
        "Spotter",
        "Pin Down \u043f\u043e\u043c\u0435\u0447\u0430\u0435\u0442 \u0446\u0435\u043b\u044c (Marked). \u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u0435 \u043f\u043e\u043f\u0430\u0434\u0430\u043d\u0438\u0435 \u043f\u043e \u043f\u043e\u043c\u0435\u0447\u0435\u043d\u043d\u043e\u0439 \u0446\u0435\u043b\u0438 \u2014 \u0433\u0430\u0440\u0430\u043d\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u043a\u0440\u0438\u0442.",
        "Pin Down marks the target. The next hit on a marked Spotter target is a guaranteed crit.",
    ),
    (
        "HaveABlast",
        "\u0412\u0437\u0440\u044b\u0432\u043d\u043e\u0439 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440",
        "Have a Blast",
        "\u041f\u0435\u0440\u0435\u043a\u043b\u044e\u0447\u0430\u0442\u0435\u043b\u044c: \u043a\u043e\u043d\u0442\u0440\u0430\u0442\u0430\u043a\u0430 \u0433\u0440\u0430\u043d\u0430\u0442\u043e\u0439. \u041f\u043e\u043b\u0443\u0447\u0430\u0435\u0442 \u0442\u043e\u043b\u044c\u043a\u043e 50% \u0443\u0440\u043e\u043d\u0430 \u043e\u0442 \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0445 \u0432\u0437\u0440\u044b\u0432\u043e\u0432.",
        "Toggle: retaliate with a grenade. Takes only 50% damage from own blasts.",
    ),
    (
        "KillingWind",
        "\u0423\u0431\u0438\u0439\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0439 \u0432\u0435\u0442\u0435\u0440",
        "Killing Wind",
        "\u0415\u0441\u043b\u0438 \u0430\u0442\u0430\u043a\u0430 \u0437\u0430\u0434\u0435\u0432\u0430\u0435\u0442 \u22652 \u0446\u0435\u043b\u0435\u0439 \u2014 +8 Grit. \u0422\u044f\u0436\u0451\u043b\u0430\u044f \u0431\u0440\u043e\u043d\u044f \u0434\u0430\u0451\u0442 \u043f\u043e\u043b\u043e\u0432\u0438\u043d\u0443 \u0448\u0442\u0440\u0430\u0444\u0430 Free Move; \u0433\u0440\u043e\u043c\u043e\u0437\u0434\u043a\u043e\u0435 \u043e\u0440\u0443\u0436\u0438\u0435 \u043d\u0435 \u0448\u0442\u0440\u0430\u0444\u0443\u0435\u0442 FM.",
        "Hitting >=2 targets grants +8 Grit. Heavy armor Free Move penalty halved; cumbersome weapons ignore FM penalty.",
    ),
    (
        "BuildingConfidence",
        "\u0423\u0432\u0435\u0440\u0435\u043d\u043d\u043e\u0441\u0442\u044c \u0440\u0430\u0441\u0442\u0451\u0442",
        "Building Confidence",
        "\u041d\u0430 2-\u043c \u0445\u043e\u0434\u0443 \u0431\u043e\u044f \u0438 \u043a\u0430\u0436\u0434\u043e\u043c 3-\u043c \u0445\u043e\u0434\u0443 \u2014 Inspired. \u041b\u0435\u0447\u0435\u043d\u0438\u0435 \u00b110% \u0437\u0430 \u0443\u0440\u043e\u0432\u0435\u043d\u044c (\u043c\u0430\u043a\u0441. \u00b150%) \u0432 \u0431\u043e\u044e \u0438 \u043d\u0430 \u0441\u043f\u0443\u0442\u043d\u0438\u043a\u0435.",
        "Inspired on combat turn 2 and every 3rd turn. Healing +/-10% per level (cap +/-50%) in combat and satellite.",
    ),
    (
        "SidneyPerk",
        "\u0421\u0430\u043c\u043e\u0434\u043e\u0432\u043e\u043b\u044c\u0441\u0442\u0432\u043e",
        "Smug",
        "+2 \u041e\u0414 \u0432 \u043d\u0430\u0447\u0430\u043b\u0435 \u0445\u043e\u0434\u0430, \u043f\u043e\u043a\u0430 \u043d\u0435 \u043f\u0440\u043e\u043c\u0430\u0445\u043d\u0451\u0442\u0441\u044f \u0438 \u043d\u0435 \u043f\u043e\u043b\u0443\u0447\u0438\u0442 \u0443\u0440\u043e\u043d.",
        "+2 AP at turn start until a miss or taking damage.",
    ),
    (
        "BulletHell",
        "\u0410\u0434\u0441\u043a\u0438\u0439 \u043b\u0438\u0432\u0435\u043d\u044c",
        "Bullet Hell",
        "\u041a\u043e\u043d\u0443\u0441\u043d\u044b\u0439 dump 15\u201330 \u043f\u0443\u043b\u044c \u0441 \u043e\u0431\u044b\u0447\u043d\u044b\u043c CTH \u0438 \u043f\u043e\u0434\u0430\u0432\u043b\u0435\u043d\u0438\u0435\u043c Will. \u041f\u0435\u0440\u0435\u0437\u0430\u0440\u044f\u0434\u043a\u0430 \u0441\u043f\u043e\u0441\u043e\u0431\u043d\u043e\u0441\u0442\u0438 \u2014 \u043f\u043e\u0441\u043b\u0435 \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u0430.",
        "Cone dump of 15-30 rounds with normal CTH and Will suppression. Ability recharges on kill.",
    ),
    (
        "OnMyTarget",
        "\u041f\u043e \u043c\u043e\u0435\u0439 \u0446\u0435\u043b\u0438",
        "On My Target",
        "\u041e\u0442\u0440\u044f\u0434 \u0430\u0442\u0430\u043a\u0443\u0435\u0442 \u043e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u0443\u044e \u0446\u0435\u043b\u044c. \u0421\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c: 10 \u041e\u0414.",
        "Squad attacks the marked target. Cost: 10 AP.",
    ),
]

LOC_START = 890000000009861


def main() -> None:
    loc: dict[str, tuple[str, str, str]] = {}
    lid = LOC_START
    for class_id, ru_n, en_n, ru_d, en_d in PERKS:
        name_id = lid
        desc_id = lid + 1
        lid += 2
        loc[str(name_id)] = (ru_n, en_n, f"jazz:CharacterEffect/{class_id}.lua")
        loc[str(desc_id)] = (ru_d, en_d, f"jazz:CharacterEffect/{class_id}.lua")
        path = CE / f"{class_id}.lua"
        text = path.read_text(encoding="utf-8")
        ru_n_esc = ru_n.replace("\\", "\\\\").replace('"', '\\"')
        ru_d_esc = ru_d.replace("\\", "\\\\").replace('"', '\\"')
        out_lines = []
        for line in text.splitlines(True):
            if "DisplayName = T(" in line and class_id in line:
                line = (
                    f'\tDisplayName = T({name_id}, '
                    f'--[[ModItemCharacterEffectCompositeDef {class_id} DisplayName]] "{ru_n_esc}"),\n'
                )
            elif "Description = T(" in line and class_id in line:
                line = (
                    f'\tDescription = T({desc_id}, '
                    f'--[[ModItemCharacterEffectCompositeDef {class_id} Description]] "{ru_d_esc}"),\n'
                )
            out_lines.append(line)
        path.write_text("".join(out_lines), encoding="utf-8", newline="\n")
        print("fixed", class_id, ru_n)

    spec = importlib.util.spec_from_file_location(
        "b2", ROOT / "docs/tools/_apply_units006_batch2_items_loc.py"
    )
    b2 = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(b2)
    b2.upsert_csv(ROOT / "Russian.csv", loc, "ru")
    b2.upsert_csv(ROOT / "English.csv", loc, "en")
    # Resync items ModItems from companions
    b2.PERKS = [(p[0], "Perk-Personal") for p in PERKS]
    b2.EXISTING = set()
    b2.sync_items()
    print("sample", (CE / "MakeThemBleed.lua").read_text(encoding="utf-8").split("DisplayName = T")[1][:80])


if __name__ == "__main__":
    main()
