# -*- coding: utf-8 -*-
"""UNITS-006 Igor Nazdarovya: signature CD recharge_on_kill=1 (was every-turn / no CD)."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CE = ROOT / "CharacterEffect" / "Nazdarovya.lua"
CA_LUA = ROOT / "Code" / "CombatActions.lua"
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

ID_CE_DESC = "890000000009888"
ID_CA_DESC = "890000000009890"

CE_DESC_RU = (
    "Активка (2 ОД): снимает боль, лечит <healMin>–<healMax> HP, даёт стак опьянения (до <maxStacks>). "
    "За стак: <range_cth_mod> CTH, +<melee_damage_flat> урона в ближке. "
    "<color EmStyle>Заряжается после убийства.</color> "
    "Опьянение в долг — −1 стак каждые <hoursPerStack> ч."
)
CE_DESC_EN = (
    "Active (2 AP): clears Pain, heals <healMin>–<healMax> HP, adds an intoxication stack (max <maxStacks>). "
    "Per stack: <range_cth_mod> CTH, +<melee_damage_flat> melee damage. "
    "<color EmStyle>Recharges after a kill.</color> "
    "Debt wears off −1 stack every <hoursPerStack> h."
)
CA_DESC_RU = (
    "Снимает боль, лечит 15–20 HP, даёт стак опьянения (до 5). За стак: −15 CTH и +20 урона в ближке. "
    "2 ОД. <color EmStyle>Заряжается после убийства.</color> Опьянение сходит по 1 стаку / 3 ч."
)
CA_DESC_EN = (
    "Clears Pain, heals 15–20 HP, adds an intoxication stack (max 5). Per stack: −15 CTH and +20 melee damage. "
    "2 AP. <color EmStyle>Recharges after a kill.</color> Intoxication decays 1 stack / 3 h."
)

RECHARGE_PARAM = """\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t'Name', "recharge_on_kill",
\t\t\t\t\t\t'Value', 1,
\t\t\t\t\t\t'Tag', "<recharge_on_kill>",
\t\t\t\t\t}),
"""

ENSURE_FN = '''
--- Ensure Nazdarovya has recharge_on_kill=1 (ResolveValue reads g_PresetParamCache).
function Jazz_EnsureNazdarovyaRechargeOnKill()
	local ca = CombatActions and CombatActions.Nazdarovya
	if not ca then
		return false
	end
	local params = ca.Parameters or {}
	local has = false
	for _, p in ipairs(params) do
		if p and p.Name == "recharge_on_kill" then
			p.Value = 1
			has = true
			break
		end
	end
	if not has then
		params[#params + 1] = PlaceObj("PresetParamNumber", {
			"Name", "recharge_on_kill",
			"Value", 1,
			"Tag", "<recharge_on_kill>",
		})
		ca.Parameters = params
	end
	if type(rawget(_G, "g_PresetParamCache")) ~= "table" then
		return false
	end
	local cache = g_PresetParamCache[ca]
	if not cache then
		cache = {}
		g_PresetParamCache[ca] = cache
	end
	cache.recharge_on_kill = 1
	return true
end

Jazz_EnsureNazdarovyaRechargeOnKill()
'''


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def upsert_csv(path: Path, rows: dict[str, tuple[str, str, str]]) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    found: set[str] = set()
    out: list[str] = []
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in rows:
            ru, en, src = rows[rid]
            nl = "\r\n" if line.endswith("\r\n") else "\n"
            # Russian.csv: col2=EN? Wait project: Russian.csv often Text=EN TextTranslated=RU
            # English.csv: Text=EN TextTranslated=RU (same structure in this mod)
            # From English.csv grep: ID, RU-looking?, EN  — actually:
            # English.csv line: ID,"RU text","EN text",,source  OR ID,EN,RU?
            # Looking at English.csv: 890000000009888,"Активка...","Active each..."
            # So col2 = Russian/source display, col3 = English for English.csv? 
            # manage-jazz: Russian.csv Text=EN TextTranslated=RU typically but this mod's Russian.csv
            # line 12458: ID,"RU","RU" for Nazdarovya — duplicated.
            # English.csv: ID,"RU","EN"
            # RecklessAssault script: out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}")
            # So order is RU, EN for both files in that script.
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}{nl}")
            found.add(rid)
        else:
            out.append(line)
    missing = [rid for rid in rows if rid not in found]
    if missing:
        if out and not out[-1].endswith("\n"):
            out[-1] += "\n"
        for rid in missing:
            ru, en, src = rows[rid]
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}\n")
    path.write_text("".join(out), encoding="utf-8-sig")
    print(f"{path.name}: upsert {sorted(found)}; appended={missing}")


def patch_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    m = re.search(r'id = "Nazdarovya",\s*\}\),', text)
    if not m:
        raise SystemExit("Nazdarovya CA end marker missing")
    start = text.rfind("PlaceObj('ModItemCombatAction'", 0, m.start())
    if start < 0:
        raise SystemExit("Nazdarovya CA start missing")
    block = text[start : m.end()]

    if "'Name', \"recharge_on_kill\"" not in block:
        needle = """\t\t\t\tParameters = {
\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t'Name', "healMin",
\t\t\t\t\t\t'Value', 15,
\t\t\t\t\t\t'Tag', "<healMin>",
\t\t\t\t\t}),
"""
        if needle not in block:
            raise SystemExit("Nazdarovya Parameters healMin anchor missing")
        block = block.replace(needle, needle + RECHARGE_PARAM, 1)
        print("items: inserted recharge_on_kill")
    else:
        print("items: recharge_on_kill already present")

    # GetUIState: inject signature recharge check
    old_ui = """\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\tlocal unit = units and units[1]
\t\t\t\t\tif not unit then
\t\t\t\t\t\treturn "hidden"
\t\t\t\t\tend
\t\t\t\t\tlocal cost = self:GetAPCost(unit, args)
"""
    new_ui = """\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\tlocal unit = units and units[1]
\t\t\t\t\tif not unit then
\t\t\t\t\t\treturn "hidden"
\t\t\t\t\tend
\t\t\t\t\tlocal recharge = unit:GetSignatureRecharge(self.id)
\t\t\t\t\tif recharge then
\t\t\t\t\t\tif recharge.on_kill then
\t\t\t\t\t\t\treturn "disabled", AttackDisableReasons.SignatureRechargeOnKill
\t\t\t\t\t\tend
\t\t\t\t\t\treturn "disabled", AttackDisableReasons.SignatureRecharge
\t\t\t\t\tend
\t\t\t\t\tlocal cost = self:GetAPCost(unit, args)
"""
    if "GetSignatureRecharge(self.id)" in block:
        print("items: GetUIState recharge check already present")
    elif old_ui in block:
        block = block.replace(old_ui, new_ui, 1)
        print("items: GetUIState recharge check added")
    else:
        raise SystemExit("Nazdarovya GetUIState anchor missing")

    # CA description string in items
    old_ca = (
        "Снимает боль, лечит 15–20 HP, даёт стак опьянения (до 5). За стак: −15 CTH и +20 урона в ближке. "
        "Без перезарядки — каждый ход (2 ОД). Опьянение сходит по 1 стаку / 3 ч."
    )
    if CA_DESC_RU in block:
        print("items: CA Description already new")
    elif old_ca in block:
        block = block.replace(old_ca, CA_DESC_RU, 1)
        print("items: CA Description updated")
    else:
        print("WARN: CA Description not found in items block")

    text = text[:start] + block + text[m.end() :]

    # CE ModItem description
    old_ce = (
        "Активка каждый ход: снимает боль, лечит <healMin>–<healMax> HP, даёт стак опьянения (до <maxStacks>). "
        "За стак: <range_cth_mod> CTH, +<melee_damage_flat> урона в ближке. "
        "Опьянение в долг — −1 стак каждые <hoursPerStack> ч."
    )
    if CE_DESC_RU in text:
        print("items: CE Description already new")
    elif old_ce in text:
        text = text.replace(old_ce, CE_DESC_RU, 1)
        print("items: CE Description updated")
    else:
        print("WARN: CE Description not found in items")

    ITEMS.write_text(text, encoding="utf-8")


def patch_ce() -> None:
    text = CE.read_text(encoding="utf-8")
    old_ce = (
        "Активка каждый ход: снимает боль, лечит <healMin>–<healMax> HP, даёт стак опьянения (до <maxStacks>). "
        "За стак: <range_cth_mod> CTH, +<melee_damage_flat> урона в ближке. "
        "Опьянение в долг — −1 стак каждые <hoursPerStack> ч."
    )
    if CE_DESC_RU in text:
        print("CE: Description already new")
    elif old_ce in text:
        text = text.replace(old_ce, CE_DESC_RU, 1)
        print("CE: Description updated")
    else:
        # already partially updated companion from earlier write?
        m = re.search(
            rf'(Description = T\({ID_CE_DESC}, --\[\[[^\]]*\]\] ")([\s\S]*?)("\))',
            text,
        )
        if not m:
            raise SystemExit("CE Description T() missing")
        text = text[: m.start(2)] + CE_DESC_RU + text[m.end(2) :]
        print("CE: Description force-replaced via T()")
    CE.write_text(text, encoding="utf-8")


def patch_combat_actions() -> None:
    text = CA_LUA.read_text(encoding="utf-8")
    old_fn = """-- Igor Nazdarovya: every-turn drink — clear Pain, heal 15–20 HP, stack Drunk (≤5). No signature recharge.
function Unit:Nazdarovya(action_id, cost_ap, args)
	local action = CombatActions[action_id]
	local max_stacks = (action and action:ResolveValue("maxStacks")) or 5
	local drunk = self:GetStatusEffect("Drunk")
	local stacks = drunk and (drunk.stacks or 1) or 0
	if stacks >= max_stacks then
		return
	end

	local heal_min = (action and action:ResolveValue("healMin")) or 15
	local heal_max = (action and action:ResolveValue("healMax")) or 20
	local span = Max(0, heal_max - heal_min)
	local heal = heal_min + InteractionRand(span + 1, "NazdarovyaHeal")
	if type(self.HitPoints) == "number" and type(self.MaxHitPoints) == "number" then
		self.HitPoints = Min(self.MaxHitPoints, self.HitPoints + heal)
		ObjModified(self)
	end

	local refund_ap = rawget(_G, "JazzRefundPainStartTurnAP")
	if type(refund_ap) == "function" then
		refund_ap(self)
	end
	self:RemoveStatusEffect("Pain", "all")
	Msg("UnitAPChanged", self)

	self:AddStatusEffect("Drunk", 1)
	-- No AddSignatureRechargeTime — usable every turn (AP cost only).
end
"""
    new_fn = """-- Igor Nazdarovya: drink — clear Pain, heal 15–20 HP, stack Drunk (≤5); CD recharge_on_kill.
function Unit:Nazdarovya(action_id, cost_ap, args)
	local action = CombatActions[action_id]
	local max_stacks = (action and action:ResolveValue("maxStacks")) or 5
	local drunk = self:GetStatusEffect("Drunk")
	local stacks = drunk and (drunk.stacks or 1) or 0
	if stacks >= max_stacks then
		return
	end

	local heal_min = (action and action:ResolveValue("healMin")) or 15
	local heal_max = (action and action:ResolveValue("healMax")) or 20
	local span = Max(0, heal_max - heal_min)
	local heal = heal_min + InteractionRand(span + 1, "NazdarovyaHeal")
	if type(self.HitPoints) == "number" and type(self.MaxHitPoints) == "number" then
		self.HitPoints = Min(self.MaxHitPoints, self.HitPoints + heal)
		ObjModified(self)
	end

	local refund_ap = rawget(_G, "JazzRefundPainStartTurnAP")
	if type(refund_ap) == "function" then
		refund_ap(self)
	end
	self:RemoveStatusEffect("Pain", "all")
	Msg("UnitAPChanged", self)

	self:AddStatusEffect("Drunk", 1)

	local recharge_on_kill = action and action:ResolveValue("recharge_on_kill")
	if recharge_on_kill then
		self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
	end
end
"""
    m = re.search(
        r"-- Igor Nazdarovya:[\s\S]*?function Unit:Nazdarovya\(action_id, cost_ap, args\)([\s\S]*?)\nend\n",
        text,
    )
    if not m:
        raise SystemExit("Unit:Nazdarovya block not found")
    if "AddSignatureRechargeTime" in m.group(1) and "recharge_on_kill" in m.group(1):
        print("CombatActions: Unit:Nazdarovya already has recharge")
    elif old_fn in text:
        text = text.replace(old_fn, new_fn, 1)
        print("CombatActions: Unit:Nazdarovya patched")
    else:
        # replace body even if comment drifted
        text = text[: m.start()] + new_fn + text[m.end() :]
        print("CombatActions: Unit:Nazdarovya force-replaced")

    if "Jazz_EnsureNazdarovyaRechargeOnKill" not in text:
        # insert after Unit:Nazdarovya end
        anchor = "function Unit:Nazdarovya(action_id, cost_ap, args)"
        i = text.find(anchor)
        if i < 0:
            raise SystemExit("Nazdarovya fn missing for ensure insert")
        # find end of function: matching end after AddStatusEffect Drunk / recharge
        j = text.find("\nend\n", i)
        if j < 0:
            raise SystemExit("Nazdarovya fn end missing")
        text = text[: j + 5] + ENSURE_FN + text[j + 5 :]
        print("CombatActions: EnsureNazdarovya inserted")
    else:
        print("CombatActions: EnsureNazdarovya already present")

    CA_LUA.write_text(text, encoding="utf-8")


def bump_meta() -> None:
    text = META.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", text)
    if not m:
        raise SystemExit("version missing")
    ver = int(m.group(1)) + 1
    text = re.sub(r"'version',\s*\d+", f"'version', {ver}", text, count=1)
    bullet = (
        "- UNITS-006: Igor Nazdarovya — signature CD recharge_on_kill=1 "
        "(was every-turn) [no new game]\\n"
    )
    m2 = re.search(r"'last_changes',\s*\"", text)
    if not m2:
        raise SystemExit("last_changes missing")
    i = m2.end()
    if "Nazdarovya — signature CD recharge_on_kill" not in text[i : i + 220]:
        text = text[:i] + bullet + text[i:]
    META.write_text(text, encoding="utf-8")
    print(f"metadata version -> {ver}")


def patch_docs() -> None:
    reps = [
        (
            ROOT / "docs/showcase/ru/perks.md",
            r"\| `Nazdarovya` \|[^\n]+\n",
            "| `Nazdarovya` | Igor | Активка **2 ОД**, CD **на убийство**: снимает боль, лечит **15–20** HP, стак опьянения ≤**5** (−15 CTH / +20 ближний урон за стак); −1 стак / **3 ч** |\n",
        ),
        (
            ROOT / "docs/showcase/en/perks.md",
            r"\| `Nazdarovya` \|[^\n]+\n",
            "| `Nazdarovya` | Igor | Active **2 AP**, CD **on kill**: clears Pain, heals **15–20** HP, intoxication stack ≤**5** (−15 CTH / +20 melee per stack); −1 stack / **3 h** |\n",
        ),
        (
            ROOT / "docs/wiki/combat-actions.md",
            r"\| `Nazdarovya` \|[^\n]+\n",
            "| `Nazdarovya` | Igor — «Наздаровье» | 2 ОД, CD после убийства: снимает боль, лечит 15–20 HP, стак опьянения ≤5 (−15 CTH / +20 ближний урон за стак). −1 стак / 3 ч на спутнике. |\n",
        ),
    ]
    for path, pat, line in reps:
        t = path.read_text(encoding="utf-8")
        t2, n = re.subn(pat, line, t, count=1)
        if n:
            path.write_text(t2, encoding="utf-8")
            print("doc", path.name)

    tech = ROOT / "docs/technical/systems/units-progression-specializations.md"
    t = tech.read_text(encoding="utf-8")
    t2, n = re.subn(
        r"- \*\*Igor `Nazdarovya`:\*\*[^\n]+",
        "- **Igor `Nazdarovya`:** signature (2 AP, `recharge_on_kill=1`): clear Pain, heal 15–20 HP, `Drunk` stacks ≤5 (−15 ranged CTH / +20 flat melee per stack); sat `OnNewHour` removes 1 stack / 3 h (`RemoveOnEndCombat=false`).",
        t,
        count=1,
    )
    if n:
        tech.write_text(t2, encoding="utf-8")
        print("doc units-progression")

    ca = ROOT / "docs/technical/weapons/combat-actions.md"
    t = ca.read_text(encoding="utf-8")
    t2, n = re.subn(
        r"(### `Nazdarovya` — Igor[^\n]*\n\n[\s\S]*?\*\*Тип:\*\*[^\n]+)\n",
        "### `Nazdarovya` — Igor («Наздаровье»)\n\n"
        "- **Пакет:** `jazz` ModItemCombatAction + CE perk + `Drunk` CE override; `Unit:Nazdarovya` в `Code/CombatActions.lua`.\n"
        "- **Тип:** именная **активка** (SignatureAbilities); **2 AP**; **`recharge_on_kill=1`**.\n",
        t,
        count=1,
    )
    # simpler replace of the no-CD line
    t = ca.read_text(encoding="utf-8")
    t = t.replace(
        "- **Тип:** именная **активка** (SignatureAbilities); **2 AP**; **без** signature recharge (каждый ход при наличии ОД).",
        "- **Тип:** именная **активка** (SignatureAbilities); **2 AP**; **`recharge_on_kill=1`** (CD до убийства).",
    )
    ca.write_text(t, encoding="utf-8")
    print("doc combat-actions technical")

    notes = ROOT / "docs/tools/_units006_namedperks_notes.md"
    if notes.exists():
        t = notes.read_text(encoding="utf-8")
        t2, n = re.subn(
            r"\| `Nazdarovya` \|[^\n]+\n",
            "| `Nazdarovya` | Wired: 2 AP drink; heal 15–20; clear Pain; Drunk ≤5; **recharge_on_kill=1**; sat −1 stack / 3h |\n",
            t,
            count=1,
        )
        if n:
            notes.write_text(t2, encoding="utf-8")

    spec = ROOT / "docs/specs/active/JAZZ-UNITS-006.md"
    t = spec.read_text(encoding="utf-8")
    t = t.replace(
        "| Igor                | `Nazdarovya`            | Active every turn (2 AP, no CD): clear Pain, heal 15–20 HP, Drunk stack≤5 (−15 CTH / +20 melee per stack); sat decay 1 stack / 3h | CHANGE  |",
        "| Igor                | `Nazdarovya`            | Active (2 AP, **recharge_on_kill=1**): clear Pain, heal 15–20 HP, Drunk stack≤5 (−15 CTH / +20 melee per stack); sat decay 1 stack / 3h | CHANGE  |",
    )
    spec.write_text(t, encoding="utf-8")
    print("spec UNITS-006 updated (owner request)")

    # showcase batch blurb
    for rel, old, new in (
        (
            "docs/showcase/ru/perks.md",
            "**Igor** (`Nazdarovya`): drink каждый ход — heal/Pain/Drunk stacks.",
            "**Igor** (`Nazdarovya`): drink 2 ОД, CD на убийство — heal/Pain/Drunk stacks.",
        ),
        (
            "docs/showcase/en/perks.md",
            "**Igor** (`Nazdarovya`): every-turn drink — heal/Pain/Drunk stacks.",
            "**Igor** (`Nazdarovya`): drink 2 AP, CD on kill — heal/Pain/Drunk stacks.",
        ),
    ):
        p = ROOT / rel
        t = p.read_text(encoding="utf-8")
        if old in t:
            p.write_text(t.replace(old, new, 1), encoding="utf-8")

    readme = ROOT / "docs/tools/README.md"
    entry = (
        "| `_apply_nazdarovya_recharge_on_kill.py` | Igor Nazdarovya: CA `recharge_on_kill=1`, "
        "`Unit:Nazdarovya` AddSignatureRechargeTime, GetUIState CD, Ensure cache, loc/docs. |\n"
    )
    rt = readme.read_text(encoding="utf-8")
    if "_apply_nazdarovya_recharge_on_kill.py" not in rt:
        if "| `_patch_nazdarovya_loc.py`" in rt:
            rt = rt.replace("| `_patch_nazdarovya_loc.py`", entry + "| `_patch_nazdarovya_loc.py`")
        else:
            rt += "\n" + entry
        readme.write_text(rt, encoding="utf-8")


def main() -> None:
    patch_items()
    patch_ce()
    patch_combat_actions()
    rows = {
        ID_CE_DESC: (CE_DESC_RU, CE_DESC_EN, "jazz:CharacterEffect/Nazdarovya.lua"),
        ID_CA_DESC: (CA_DESC_RU, CA_DESC_EN, "jazz:items.lua:Nazdarovya"),
    }
    upsert_csv(RU, rows)
    upsert_csv(EN, rows)
    bump_meta()
    patch_docs()
    r = subprocess.run(
        ["python", str(ROOT / "docs/tools/_validate_items_quick.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    if r.returncode:
        print(r.stderr)
        raise SystemExit(r.returncode)
    print("OK Nazdarovya recharge_on_kill")


if __name__ == "__main__":
    main()
