# -*- coding: utf-8 -*-
"""Generate/fix Passive SignatureAbilities CombatAction companions for Jazz_Perk_*.

- Missing CA: insert Passive stub before CE in items.lua + ModResourcePreset in metadata.
- Existing Lynx/Buzz/Spider/Colby: fix GetUIState hidden + strip copy-paste Toggle junk.
- Skip Jazz_Perk_00 (real Toggle) and Jazz_Perk_OfficerAuraInfluence (aura status).

Run from jazz root:
  python docs/tools/_gen_jazz_perk_passive_combat_actions.py
  python docs/tools/_validate_items_quick.py
  python docs/tools/_audit_jazz_perk_combat_actions.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CE_DIR = ROOT / "CharacterEffect"

SKIP = {"Jazz_Perk_00", "Jazz_Perk_OfficerAuraInfluence"}

# Shared placeholder DisplayName T-id (resolved via GetSignatureActionDisplayName → CE).
PLACEHOLDER_T = 115026001164

PASSIVE_UI = '''\
					GetUIState = function (self, units, args)
						local unit = units[1]
						local cost = self:GetAPCost(unit, args)
						if cost < 0 then return "hidden" end
						if not unit:UIHasAP(cost) then return "disabled" end
						return "enabled"
					end,'''

PASSIVE_RUN = '''\
					Run = function (self, unit, ap, ...)
						return false
					end,'''


def ce_icon(perk_id: str) -> str:
    # Prefer HUD dual-strip when present (Passive hotbar); CE Personal stays for perk tiles.
    sig = ROOT / "Perks" / "SignatureAbilities" / f"{perk_id}.png"
    if sig.exists():
        return f"Mod/e6L4ECj/Perks/SignatureAbilities/{perk_id}.png"
    path = CE_DIR / f"{perk_id}.lua"
    if path.exists():
        m = re.search(r'Icon\s*=\s*"([^"]+)"', path.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    short = perk_id.replace("Jazz_Perk_", "")
    return f"Mod/e6L4ECj/Perks/Personal/{short}.png"


def build_ca(perk_id: str) -> str:
    icon = ce_icon(perk_id)
    return f"""\t\t\t\tPlaceObj('ModItemCombatAction', {{
\t\t\t\t\tActionType = "Passive",
\t\t\t\t\tActivePauseBehavior = "instant",
\t\t\t\t\tComment = "passive",
\t\t\t\t\tConfigurableKeybind = false,
\t\t\t\t\tDisplayName = T({PLACEHOLDER_T}, --[[ModItemCombatAction {perk_id} DisplayName]] "<placeholder>"),
\t\t\t\t\tGetActionDescription = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDescription(self)
\t\t\t\t\tend,
\t\t\t\t\tGetActionDisplayName = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDisplayName(self)
\t\t\t\t\tend,
{PASSIVE_UI}
\t\t\t\t\tIcon = "{icon}",
\t\t\t\t\tIdDefault = "{perk_id}default",
\t\t\t\t\tIsAimableAttack = false,
\t\t\t\t\tKeybindingFromAction = "actionRedirectSignatureAbility",
\t\t\t\t\tRequireState = "any",
{PASSIVE_RUN}
\t\t\t\t\tShowIn = "SignatureAbilities",
\t\t\t\t\tSortKey = 100,
\t\t\t\t\tgroup = "SignatureAbilities",
\t\t\t\t\tid = "{perk_id}",
\t\t\t\t}}),
"""


def existing_ca_ids(text: str) -> set[str]:
    return set(re.findall(r"PlaceObj\('ModItemCombatAction'[\s\S]*?\bid\s*=\s*\"(Jazz_Perk_[^\"]+)\"", text))


def fix_existing_passive_stubs(text: str) -> tuple[str, int]:
    """Rewrite Lynx/Buzz/Spider/Colby-style hidden stubs into real Passive UI."""
    fixed = 0

    def repl_block(m: re.Match[str]) -> str:
        nonlocal fixed
        block = m.group(0)
        pid = m.group(1)
        if pid in SKIP or pid == "Jazz_Perk_00":
            return block
        if "ActionType = \"Passive\"" not in block:
            return block
        if 'return "hidden"' not in block and "IsToggledOn" not in block:
            return block
        # Rebuild clean Passive from id + Icon if present.
        icon_m = re.search(r'Icon\s*=\s*"([^"]+)"', block)
        icon = icon_m.group(1) if icon_m else ce_icon(pid)
        fixed += 1
        return build_ca(pid).rstrip("\n")

    # Match each Jazz_Perk CombatAction PlaceObj block (non-greedy to next id= line's closing).
    pattern = re.compile(
        r"PlaceObj\('ModItemCombatAction',\s*\{(?:(?!PlaceObj\('ModItemCombatAction').)*?\bid\s*=\s*\"(Jazz_Perk_[^\"]+)\"\s*,?\s*\}\),",
        re.S,
    )
    new_text, n = pattern.subn(repl_block, text)
    return new_text, fixed


def insert_missing_cas(text: str, missing: list[str]) -> tuple[str, int]:
    inserted = 0
    for perk_id in missing:
        # Insert CA immediately before the CE ModItem with this Id.
        needle = (
            f"PlaceObj('ModItemCharacterEffectCompositeDef', {{\n"
            f"\t\t\t\t\t'Group', \"Perk-Personal\",\n"
            f"\t\t\t\t\t'Id', \"{perk_id}\","
        )
        alt = (
            f"PlaceObj('ModItemCharacterEffectCompositeDef', {{\n"
            f"\t\t\t\t\t'Id', \"{perk_id}\","
        )
        ca = build_ca(perk_id)
        if needle in text:
            text = text.replace(needle, ca + "\t\t\t\t" + needle, 1)
            inserted += 1
        elif alt in text:
            text = text.replace(alt, ca + "\t\t\t\t" + alt, 1)
            inserted += 1
        else:
            # Broader: any CE Id line for this perk inside CharacterEffectCompositeDef.
            pat = re.compile(
                rf"(PlaceObj\('ModItemCharacterEffectCompositeDef',\s*\{{[^\}}]*?'Id',\s*\"{re.escape(perk_id)}\")",
                re.S,
            )
            m = pat.search(text)
            if not m:
                print(f"WARN: CE ModItem not found for {perk_id}", file=sys.stderr)
                continue
            # Find start of that PlaceObj
            start = text.rfind("PlaceObj('ModItemCharacterEffectCompositeDef'", 0, m.start() + 1)
            if start < 0:
                print(f"WARN: CE start not found for {perk_id}", file=sys.stderr)
                continue
            text = text[:start] + ca + "\t\t\t\t" + text[start:]
            inserted += 1
    return text, inserted


def sync_metadata(missing: list[str]) -> int:
    text = META.read_text(encoding="utf-8")
    added = 0
    for perk_id in missing:
        # Already has CombatAction resource?
        ca_pat = (
            r"PlaceObj\('ModResourcePreset',\s*\{\s*'Class',\s*\"CombatAction\",\s*'Id',\s*\""
            + re.escape(perk_id)
            + r"\""
        )
        if re.search(ca_pat, text, re.S):
            continue
        # Insert CombatAction preset before CharacterEffectCompositeDef for same Id.
        ce_preset = (
            f"\t\tPlaceObj('ModResourcePreset', {{\n"
            f"\t\t\t'Class', \"CharacterEffectCompositeDef\",\n"
            f"\t\t\t'Id', \"{perk_id}\",\n"
            f"\t\t\t'ClassDisplayName', \"Character effect\",\n"
            f"\t\t}}),"
        )
        ca_preset = (
            f"\t\tPlaceObj('ModResourcePreset', {{\n"
            f"\t\t\t'Class', \"CombatAction\",\n"
            f"\t\t\t'Id', \"{perk_id}\",\n"
            f"\t\t\t'ClassDisplayName', \"Combat Actions\",\n"
            f"\t\t}}),\n"
        )
        if ce_preset in text:
            text = text.replace(ce_preset, ca_preset + ce_preset, 1)
            added += 1
        else:
            ce_pat = re.compile(
                r"(PlaceObj\('ModResourcePreset',\s*\{\s*'Class',\s*\"CharacterEffectCompositeDef\",\s*'Id',\s*\""
                + re.escape(perk_id)
                + r"\",\s*'ClassDisplayName',\s*\"Character effect\",\s*\}\),)",
                re.S,
            )
            m = ce_pat.search(text)
            if not m:
                print(f"WARN: metadata CE preset missing for {perk_id}", file=sys.stderr)
                continue
            text = text[: m.start()] + ca_preset + m.group(1) + text[m.end() :]
            added += 1
    META.write_text(text, encoding="utf-8", newline="\n")
    return added


def main() -> int:
    ce_ids = sorted(
        p.stem
        for p in CE_DIR.glob("Jazz_Perk_*.lua")
        if p.stem not in SKIP
    )
    text = ITEMS.read_text(encoding="utf-8")
    have = existing_ca_ids(text)
    print(f"CE targets: {len(ce_ids)}; existing CA: {len(have & set(ce_ids))}")

    text, n_fixed = fix_existing_passive_stubs(text)
    print(f"Fixed existing Passive stubs: {n_fixed}")

    have = existing_ca_ids(text)
    missing = [p for p in ce_ids if p not in have]
    print(f"Missing CA to insert: {len(missing)}")
    text, n_ins = insert_missing_cas(text, missing)
    print(f"Inserted: {n_ins}")

    ITEMS.write_text(text, encoding="utf-8", newline="\n")

    # Recompute missing against disk for metadata
    have2 = existing_ca_ids(ITEMS.read_text(encoding="utf-8"))
    still_missing_meta = [p for p in ce_ids if p not in have2]
    # Also ensure metadata for all that now have CA
    need_meta = [p for p in ce_ids if p in have2]
    n_meta = sync_metadata(need_meta)
    print(f"Metadata CombatAction presets added: {n_meta}")
    if still_missing_meta:
        print("FAIL still missing CA:", still_missing_meta, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
