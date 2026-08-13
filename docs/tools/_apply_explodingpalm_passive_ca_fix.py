# Patch ExplodingPalm ModItemCombatAction: Passive 54 icon + HasPerk GetUIState.
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
items = ROOT / "items.lua"
text = items.read_text(encoding="utf-8")

old = """\t\t\t\tPlaceObj('ModItemCombatAction', {
\t\t\t\t\tActionType = "Passive",
\t\t\t\t\tActivePauseBehavior = "instant",
\t\t\t\t\tComment = "DrQ ExplodingPalm passive signature (id must match CE)",
\t\t\t\t\tConfigurableKeybind = false,
\t\t\t\t\tDisplayName = T(115026001164, --[[ModItemCombatAction ExplodingPalm DisplayName]] "<placeholder>"),
\t\t\t\t\tGetActionDescription = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDescription(self)
\t\t\t\t\tend,
\t\t\t\t\tGetActionDisplayName = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDisplayName(self)
\t\t\t\t\tend,
\t\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\t\tlocal unit = units[1]
\t\t\t\t\t\tlocal cost = self:GetAPCost(unit, args)
\t\t\t\t\t\tif cost < 0 then return "hidden" end
\t\t\t\t\t\tif not unit:UIHasAP(cost) then return "disabled" end
\t\t\t\t\t\treturn "enabled"
\t\t\t\t\tend,
\t\t\t\t\tIcon = "UI/Icons/Hud/perk_exploding_palm",
\t\t\t\t\tIdDefault = "ExplodingPalmdefault",
\t\t\t\t\tIsAimableAttack = false,
\t\t\t\t\tKeybindingFromAction = "actionRedirectSignatureAbility",
\t\t\t\t\tRequireState = "any",
\t\t\t\t\tRun = function (self, unit, ap, ...)
\t\t\t\t\t\treturn false
\t\t\t\t\tend,
\t\t\t\t\tShowIn = "SignatureAbilities",
\t\t\t\t\tSortKey = 100,
\t\t\t\t\tgroup = "SignatureAbilities",
\t\t\t\t\tid = "ExplodingPalm",
\t\t\t\t}),"""

new = """\t\t\t\tPlaceObj('ModItemCombatAction', {
\t\t\t\t\tActionType = "Passive",
\t\t\t\t\tActivePauseBehavior = "instant",
\t\t\t\t\tComment = "DrQ ExplodingPalm passive signature (id must match CE)",
\t\t\t\t\tConfigurableKeybind = false,
\t\t\t\t\tDisplayName = T(115026001164, --[[ModItemCombatAction ExplodingPalm DisplayName]] "<placeholder>"),
\t\t\t\t\tGetActionDescription = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDescription(self)
\t\t\t\t\tend,
\t\t\t\t\tGetActionDisplayName = function (self, units)
\t\t\t\t\t\treturn GetSignatureActionDisplayName(self)
\t\t\t\t\tend,
\t\t\t\t\tGetAPCost = function (self, unit, args)
\t\t\t\t\t\treturn 0
\t\t\t\t\tend,
\t\t\t\t\tGetUIState = function (self, units, args)
\t\t\t\t\t\tlocal unit = units and units[1]
\t\t\t\t\t\tif not unit or not HasPerk(unit, "ExplodingPalm") then
\t\t\t\t\t\t\treturn "hidden"
\t\t\t\t\t\tend
\t\t\t\t\t\treturn "enabled"
\t\t\t\t\tend,
\t\t\t\t\tIcon = "Mod/e6L4ECj/Perks/SignatureAbilities/ExplodingPalm.png",
\t\t\t\t\tIdDefault = "ExplodingPalmdefault",
\t\t\t\t\tIsAimableAttack = false,
\t\t\t\t\tKeybindingFromAction = "actionRedirectSignatureAbility",
\t\t\t\t\tRequireState = "any",
\t\t\t\t\tRun = function (self, unit, ap, ...)
\t\t\t\t\t\treturn false
\t\t\t\t\tend,
\t\t\t\t\tExecute = function (self, units, args)
\t\t\t\t\tend,
\t\t\t\t\tUIBegin = function (self, units, args)
\t\t\t\t\tend,
\t\t\t\t\tShowIn = "SignatureAbilities",
\t\t\t\t\tSortKey = 100,
\t\t\t\t\tgroup = "SignatureAbilities",
\t\t\t\t\tid = "ExplodingPalm",
\t\t\t\t}),"""

# Normalize tabs: file may use mix — find by unique Comment marker
idx = text.find('Comment = "DrQ ExplodingPalm passive signature')
if idx < 0:
    raise SystemExit("ExplodingPalm CA block not found")
# Find PlaceObj start before comment
start = text.rfind("PlaceObj('ModItemCombatAction'", 0, idx)
end = text.find("id = \"ExplodingPalm\",\n\t\t\t\t}),", idx)
if start < 0 or end < 0:
    # try alternate whitespace
    end = text.find('id = "ExplodingPalm",', idx)
    if end < 0:
        raise SystemExit(f"end not found start={start}")
    end = text.find("}),", end)
    end = end + 3
else:
    end = end + len("id = \"ExplodingPalm\",\n\t\t\t\t}),")

block = text[start:end]
if "SignatureAbilities/ExplodingPalm.png" in block:
    print("already patched")
else:
    text = text[:start] + new + text[end:]
    items.write_text(text, encoding="utf-8", newline="\n")
    print("patched ExplodingPalm CombatAction")

# bump metadata
meta = ROOT / "metadata.lua"
mt = meta.read_text(encoding="utf-8")
m = re.search(r"'version',\s*(\d+)", mt)
ver = int(m.group(1)) + 1
mt = re.sub(r"'version',\s*\d+", f"'version', {ver}", mt, count=1)
bullet = (
    "- UNITS-006: DrQ ExplodingPalm — OnAttack HP-tier statuses (not vanilla smash); "
    "Passive 54 icon; refresh perk reactions [no new game]\\n"
)
marker = "'last_changes', \""
i = mt.find(marker) + len(marker)
if "DrQ ExplodingPalm — OnAttack" not in mt[i : i + 180]:
    mt = mt[:i] + bullet + mt[i:]
meta.write_text(mt, encoding="utf-8", newline="\n")
print(f"version={ver}")
