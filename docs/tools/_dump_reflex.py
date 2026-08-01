# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, "docs/tools")
from _apply_attach_001 import placeobj_blocks, prop

text = Path("items.lua").read_text(encoding="utf-8")
for b in placeobj_blocks(text, "ModItemWeaponComponent"):
    cid = prop(b.text, "id") or ""
    if not cid.startswith("JAZZ_Reflex_"):
        continue
    cost = re.search(r"Cost = (\d+)", b.text)
    aim = re.search(r"'Name', \"AimAccuracyPercent\"[\s\S]*?'Value', (\d+)", b.text)
    ow = re.search(r"'Name', \"ScopeOverwatchAngle\"[\s\S]*?'Value', (\d+)", b.text)
    extra = re.search(r"'Name', \"extra_attacks\"[\s\S]*?'Value', (\d+)", b.text)
    bonus = re.search(r"'Name', \"bonus_cth\"[\s\S]*?'Value', (\d+)", b.text)
    fx = re.findall(r'"((?:DecreaseMaxAimActions|MinAim|IncreaseAimAccuracy15Percent|ExtraOverwatchShots|ScopeOverwatchAngleIncreace(?:Big)?|OpportunityAttackBonusCth))"', b.text)
    print(
        f"{cid}: cost={cost and cost.group(1)} aim%={aim and aim.group(1)} "
        f"ow={ow and ow.group(1)} extra={extra and extra.group(1)} oa={bonus and bonus.group(1)} "
        f"fx={fx}"
    )
