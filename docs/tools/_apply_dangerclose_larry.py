# -*- coding: utf-8 -*-
"""Apply Larry DangerClose List2: CE/items/loc sync + CSV rows."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CE_PATH = ROOT / "CharacterEffect" / "DangerClose.lua"
ITEMS = ROOT / "items.lua"

DISPLAY_ID = "890000000009925"
DESC_ID = "890000000009926"

DISPLAY_RU = "Опасная дальность"
DISPLAY_EN = "Danger Range"
DESC_RU = (
    "Гранаты и взрывчатка на дистанции ≥<minRange> клеток: +<percent(damageBonus)> урона. "
    "Взрывы дополнительно накладывают <bleed_stacks> стака кровотечения. "
    "Нет штрафов от боевых стимуляторов."
)
DESC_EN = (
    "Grenades and explosives at ≥<minRange> tiles: +<percent(damageBonus)> damage. "
    "Explosions also apply <bleed_stacks> Bleeding stacks. "
    "No combat stim penalties."
)

ROWS = {
    DISPLAY_ID: (DISPLAY_RU, DISPLAY_EN, "jazz:CharacterEffect/DangerClose.lua"),
    DESC_ID: (DESC_RU, DESC_EN, "jazz:CharacterEffect/DangerClose.lua"),
}


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def patch_csv(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    found: set[str] = set()
    out: list[str] = []
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in ROWS:
            ru, en, src = ROWS[rid]
            nl = "\n" if line.endswith("\n") else ""
            if line.endswith("\r\n"):
                nl = "\r\n"
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}{nl}")
            found.add(rid)
        else:
            out.append(line)
    missing = [rid for rid in ROWS if rid not in found]
    if missing:
        if out and not out[-1].endswith("\n"):
            out[-1] = out[-1] + "\n"
        for rid in missing:
            ru, en, src = ROWS[rid]
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}\n")
    path.write_text("".join(out), encoding="utf-8-sig")
    print(f"{path.name}: upserted {sorted(ROWS)}; appended={missing}")


ITEMS_BLOCK = r"""					'Id', "DangerClose",
					'object_class', "Perk",
					'Parameters', {
						PlaceObj('PresetParamNumber', {
							'Name', "rangeThreshold",
							'Value', 8,
							'Tag', "<rangeThreshold>",
						}),
						PlaceObj('PresetParamPercent', {
							'Name', "damageMod",
							'Value', 40,
							'Tag', "<damageMod>%",
						}),
						PlaceObj('PresetParamNumber', {
							'Name', "minRange",
							'Value', 8,
							'Tag', "<minRange>",
						}),
						PlaceObj('PresetParamPercent', {
							'Name', "damageBonus",
							'Value', 40,
							'Tag', "<damageBonus>",
						}),
						PlaceObj('PresetParamNumber', {
							'Name', "bleed_stacks",
							'Value', 2,
							'Tag', "<bleed_stacks>",
						}),
					},
					'unit_reactions', {
						PlaceObj('UnitReaction', {
							Event = "OnCalcStimmedTiredness",
							Handler = function (self, target, value)
								return 0
							end,
						}),
						PlaceObj('UnitReaction', {
							Event = "OnModifyCTHModifier",
							Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
								if target ~= attacker then
									return
								end
								if id == "Stimmed" or id == "Stim" then
									data.mod_add = 0
									data.mod_mul = 100
								end
							end,
						}),
					},
					'DisplayName', T(890000000009925, --[[ModItemCharacterEffectCompositeDef DangerClose DisplayName]] "Опасная дальность"),
					'Description', T(890000000009926, --[[ModItemCharacterEffectCompositeDef DangerClose Description]] "Гранаты и взрывчатка на дистанции ≥<minRange> клеток: +<percent(damageBonus)> урона. Взрывы дополнительно накладывают <bleed_stacks> стака кровотечения. Нет штрафов от боевых стимуляторов."),
					'Icon', "UI/Icons/Perks/DangerClose",
					'Tier', "Personal",
				}),"""


def patch_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    pat = re.compile(
        r"\t\t\t\t\t'Id', \"DangerClose\",.*?'Tier', \"Personal\",\n\t\t\t\t\}\),",
        re.S,
    )
    m = pat.search(text)
    if not m:
        raise SystemExit("DangerClose ModItem block not found in items.lua")
    text = text[: m.start()] + ITEMS_BLOCK + text[m.end() :]
    ITEMS.write_text(text, encoding="utf-8")
    print("items.lua: DangerClose ModItem replaced")


def main() -> None:
    if not CE_PATH.is_file():
        raise SystemExit(f"missing {CE_PATH}")
    patch_items()
    patch_csv(ROOT / "English.csv")
    patch_csv(ROOT / "Russian.csv")
    print("OK DangerClose List2 apply")


if __name__ == "__main__":
    main()
