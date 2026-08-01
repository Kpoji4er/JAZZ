# -*- coding: utf-8 -*-
"""Side tiers: Flashlight light+dark, Dot light+OW/Mark, Laser CTH+falloff, UV night stealth laser.

Canon: docs/design/side-tiers.md
Also patches Laser CTH CalcValue for falloff after LaserFullRange (default 5).
Fixes FlashlightOn/Off to recognize JAZZ_Flashlight* ids.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write, list_region

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

# id -> kind
PROFILES: dict[str, str] = {
    "JAZZ_Flashlight": "flashlight",
    "JAZZ_Flashlight_aa12": "flashlight",
    "JAZZ_Flashlight_PSG_M1": "flashlight",
    "JAZZ_FlashlightDot": "dot",
    "JAZZ_FlashlightDot_aa12": "dot",
    "JAZZ_FlashlightDot_PSG_M1": "dot",
    "JAZZ_FlashlightDot_Anaconda": "dot",
    "JAZZ_LaserDot": "laser",
    "JAZZ_LaserDot_aa12": "laser",
    "JAZZ_LaserDot_PSG_M1": "laser",
    "JAZZ_LaserDot_Anaconda": "laser",
    "JAZZ_UVDot": "uv",
    "JAZZ_UVDot_aa12": "uv",
    "JAZZ_UVDot_PSG_M1": "uv",
    "JAZZ_UVDot_Anaconda": "uv",
}


def _field_span(text: str, name: str) -> tuple[int, int] | None:
    region = list_region(text, name)
    if region is None:
        return None
    m = re.search(rf"\b{re.escape(name)}\s*=\s*\{{", text)
    if not m:
        return None
    end = region[1]
    if end < len(text) and text[end] == ",":
        end += 1
    while end < len(text) and text[end] in " \t":
        end += 1
    if end < len(text) and text[end] == "\n":
        end += 1
    return m.start(), end


def _replace_field(text: str, name: str, replacement: str | None) -> str:
    span = _field_span(text, name)
    if span is None:
        if replacement is None:
            return text
        if name == "Parameters":
            fx = _field_span(text, "ModificationEffects")
            if fx:
                return text[: fx[1]] + replacement + "\n" + text[fx[1] :]
        return re.sub(
            r"(DisplayName = T\([^\n]+\),)",
            rf"\1\n\t\t\t\t\t\t{replacement}",
            text,
            count=1,
        )
    start, end = span
    if replacement is None:
        return text[:start] + text[end:]
    body = replacement if replacement.endswith("\n") else replacement + "\n"
    return text[:start] + body + text[end:]


def effects_block(names: list[str]) -> str:
    body = ",\n".join(f'\t\t\t\t\t\t\t"{n}"' for n in names)
    return "ModificationEffects = {\n" + body + ",\n\t\t\t\t\t\t},"


def param_num(name: str, value: int) -> str:
    return (
        "\t\t\t\t\t\t\tPlaceObj('PresetParamNumber', {\n"
        f"\t\t\t\t\t\t\t\t'Name', \"{name}\",\n"
        f"\t\t\t\t\t\t\t\t'Value', {value},\n"
        f"\t\t\t\t\t\t\t\t'Tag', \"<{name}>\",\n"
        "\t\t\t\t\t\t\t}),"
    )


def param_pct(name: str, value: int) -> str:
    return (
        "\t\t\t\t\t\t\tPlaceObj('PresetParamPercent', {\n"
        f"\t\t\t\t\t\t\t\t'Name', \"{name}\",\n"
        f"\t\t\t\t\t\t\t\t'Value', {value},\n"
        f"\t\t\t\t\t\t\t\t'Tag', \"<{name}>%\",\n"
        "\t\t\t\t\t\t\t}),"
    )


def params_block(parts: list[str]) -> str:
    return "Parameters = {\n" + "\n".join(parts) + "\n\t\t\t\t\t\t},"


def ensure_enable_aim_fx(text: str) -> str:
    if re.search(r"EnableAimFX\s*=\s*true", text):
        return text
    return re.sub(
        r"(DisplayName = T\([^\n]+\),)",
        r"\1\n\t\t\t\t\t\tEnableAimFX = true,",
        text,
        count=1,
    )


def profile_for(kind: str) -> tuple[list[str], list[str], int, int, str]:
    if kind == "flashlight":
        return (
            ["IgnoreInTheDark"],
            [],
            20,
            -25,
            "Side Flashlight — dark ignore + light FX (EnableAimFX)",
        )
    if kind == "dot":
        return (
            [
                "IgnoreInTheDark",
                "IncreaseOverwatchAngle",
                "MarkWhenFullyAimed",
                "StealthKillBonusPerAim",
            ],
            [
                param_num("OverwatchAngleIncrease", 130),
                param_pct("stealth_kill_bonus", 2),
                param_num("maxaims", 1),
                param_pct("aim_bonus", 1),
            ],
            35,
            0,
            "Side Tac Device — light + OW + mark + mild SK",
        )
    if kind == "laser":
        return (
            [
                "LaserMark",
                "IncreaseOverwatchAngle",
                "MarkWhenFullyAimed",
                "IncreaseCritChangeScaled",
            ],
            [
                param_num("LaserCTH", 15),
                param_num("LaserDistance", 10),
                param_num("LaserFullRange", 5),
                param_num("OverwatchAngleIncrease", 130),
                param_num("CritChangeScaledIncrease", 10),
            ],
            40,
            10,
            "Side Laser — flat CTH with falloff after 5 tiles",
        )
    if kind == "uv":
        return (
            ["LaserMark", "StealthKillBonusPerAim"],
            [
                param_num("LaserCTH", 12),
                param_num("LaserDistance", 8),
                param_num("LaserFullRange", 5),
                param_num("NightOnly", 1),
                param_pct("stealth_kill_bonus", 5),
            ],
            25,
            10,
            "Side UV — night laser CTH + stealth kill",
        )
    raise ValueError(kind)


def patch_comp(text: str, kind: str) -> str:
    fx, params, cost, diff, comment = profile_for(kind)
    text = ensure_enable_aim_fx(text)
    text = _replace_field(text, "ModificationEffects", effects_block(fx))
    if params:
        text = _replace_field(text, "Parameters", params_block(params))
    else:
        text = _replace_field(text, "Parameters", None)
    if re.search(r"Cost = \d+,", text):
        text = re.sub(r"Cost = \d+,", f"Cost = {cost},", text, count=1)
    if re.search(r"ModificationDifficulty = -?\d+,", text):
        text = re.sub(
            r"ModificationDifficulty = -?\d+,",
            f"ModificationDifficulty = {diff},",
            text,
            count=1,
        )
    if re.search(r'comment = "[^"]*"', text):
        text = re.sub(r'comment = "[^"]*"', f'comment = "{comment}"', text, count=1)
    else:
        text = re.sub(
            r"(\n\t\t\t\t\t\t(?:group|Slot) = )",
            f'\n\t\t\t\t\t\tcomment = "{comment}",\\1',
            text,
            count=1,
        )
    return text


LASER_CALC = r'''CalcValue = function (self, attacker, target, body_part_def, action, weapon1, weapon2, lof, aim, opportunity_attack, attacker_pos, target_pos)
					if attacker and IsKindOf(weapon1, "Firearm") then
						local modifyVal = GetComponentEffectValue(weapon1, "LaserMark", "LaserCTH")
						if modifyVal then
							-- UV: NightOnly=1 → only night / underground
							local night_only = GetComponentEffectValue(weapon1, "LaserMark", "NightOnly")
							if night_only and night_only > 0 and not (GameState.Night or GameState.Underground) then
								return false, 0
							end
							local attacker_pos = attacker:GetPos()
							local target_pos = IsPoint(target) and target or target:GetPos()
							local dist = Max(1, attacker_pos:Dist(target_pos) / const.SlabSizeX)
							local laserdist = GetComponentEffectValue(weapon1, "LaserMark", "LaserDistance") or 0
							if dist > laserdist then
								return false, 0
							end
							local full = GetComponentEffectValue(weapon1, "LaserMark", "LaserFullRange") or 5
							if dist <= full then
								return true, modifyVal
							end
							-- linear falloff full→max: bonus down to ~40%
							local span = Max(1, laserdist - full)
							local t = MulDivRound(dist - full, 1000, span)
							local scaled = Max(1, MulDivRound(modifyVal, 1000 - MulDivRound(600, t, 1000), 1000))
							return true, scaled
						end
					end
					return false, 0
				end,'''


def patch_laser_cth(text: str) -> str:
    # Replace CalcValue of id = "Laser" ChanceToHitModifier
    m = re.search(
        r"(PlaceObj\('ModItemChanceToHitModifier', \{\s*\n\s*CalcValue = function \(self, attacker, target,[\s\S]*?\n\s*end,)(\s*\n\s*Parameters = \{[\s\S]*?\nid = \"Laser\",)",
        text,
    )
    if not m:
        # try looser: find id = "Laser" and walk back to CalcValue
        idx = text.find('\nid = "Laser",')
        if idx < 0:
            print("WARN Laser CTH modifier not found")
            return text
        start = text.rfind("CalcValue = function", 0, idx)
        end = text.find("\n\t\t\t\tend,", start)
        if start < 0 or end < 0:
            print("WARN Laser CalcValue span not found")
            return text
        end = end + len("\n\t\t\t\tend,")
        text = text[:start] + LASER_CALC + text[end:]
        print("patched Laser CTH CalcValue (span)")
        return text
    text = text[: m.start(1)] + LASER_CALC + text[m.end(1) :]
    print("patched Laser CTH CalcValue")
    return text


def patch_flashlight_actions(text: str) -> str:
    """Recognize JAZZ_Flashlight / Off pairs in FlashlightOn/Off GetUIState."""
    # FlashlightOn: currently checks FlashlightOff / Flashlight_Grip_Off
    old_on = '''if weapon1.components.Side == "FlashlightOff" or weapon1.components.Side == "Flashlight_Grip_Off" then'''
    new_on = '''local side = weapon1.components.Side
						        if side == "FlashlightOff" or side == "Flashlight_Grip_Off" or side == "JAZZ_FlashlightOff" then'''
    if old_on in text:
        text = text.replace(old_on, new_on, 1)
        print("patched FlashlightOn UI")
    old_off = '''if weapon1.components.Side == "Flashlight" or weapon1.components.Side == "Flashlight_Grip" then'''
    new_off = '''local side = weapon1.components.Side
						        if side == "Flashlight" or side == "Flashlight_Grip" or side == "JAZZ_Flashlight" or side == "JAZZ_Flashlight_aa12" or side == "JAZZ_Flashlight_PSG_M1" then'''
    if old_off in text:
        text = text.replace(old_off, new_off, 1)
        print("patched FlashlightOff UI")
    # zzFoldingPair on JAZZ_Flashlight points to FlashlightOff — keep if that id exists; else note
    return text


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    n = 0
    for b in reversed(placeobj_blocks(text, "ModItemWeaponComponent")):
        cid = prop(b.text, "id")
        kind = PROFILES.get(cid or "")
        if not kind:
            continue
        new = patch_comp(b.text, kind)
        text = text[: b.start] + new + text[b.end :]
        n += 1
        print("patched", cid, kind)
    text = patch_laser_cth(text)
    text = patch_flashlight_actions(text)
    atomic_write(ITEMS, text)
    print("total comps", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
