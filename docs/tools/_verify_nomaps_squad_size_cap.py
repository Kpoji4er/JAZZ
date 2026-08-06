"""Static checks for JAZZ-COMPAT-009 NoMaps InitialSquads size cap.

Run: python docs/tools/_verify_nomaps_squad_size_cap.py
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOMAPS = ROOT.parent / "jazz-nomaps" / "Code" / "NoMaps_Autonomy.lua"
GUARDPOST = ROOT / "Code" / "Guardpost.lua"

nomaps = NOMAPS.read_text(encoding="utf-8")
guardpost = GUARDPOST.read_text(encoding="utf-8")

assert 'local JAZZ_NOMAPS_INITIAL_SQUAD_MAX = 30' in nomaps, "NoMaps cap must be 30"
assert "lCapInitialSquadTemplates" in nomaps, "InitialSquads cap helper missing"
assert 'string.find(base_session_id, "InitialSquad", 1, true) ~= 1' in nomaps, (
    "cap must be gated to InitialSquad* sessions"
)
assert "local capped = {}" in nomaps, "cap must copy instead of mutating caller templates"
assert "for i = 1, JAZZ_NOMAPS_INITIAL_SQUAD_MAX do" in nomaps, "ordered capped copy missing"

assert 'rawget(_G, "GenerateUnitsFromTemplates")' in nomaps, "base lookup missing"
assert 'rawset(_G, "g_JAZZ_NoMapsBaseGenerateUnitsFromTemplates", base)' in nomaps
assert 'rawset(_G, "g_JAZZ_NoMapsGenerateUnitsFromTemplatesWrapped", true)' in nomaps
assert "function GenerateUnitsFromTemplates(" in nomaps, "runtime wrapper missing"
assert "if lShouldRun() then" in nomaps, "jazz-maps no-op gate missing"
assert "lInstallGenerateUnitsFromTemplatesWrapper()" in nomaps, "wrapper install missing"
assert "g_JAZZ_NoMapsBodyCountModifierWrapped" not in nomaps, "dynamic BodyCount must not be wrapped"
assert "g_JAZZ_NoMapsGenerateRandEnemySquadUnitsWrapped" not in nomaps, (
    "dynamic random squad generation must not be wrapped"
)

body_count = guardpost.index(
    "generated_unit_ids, generated_unit_names, generated_sources, generated_appearances = GameRuleBodyCountModifier"
)
unit_creation = guardpost.index("local units = GenerateUnitsFromTemplates", body_count)
assert body_count < unit_creation, "InitialSquads cap must run after BodyCount expansion"

assert "existing.StartingManpower = 40" in nomaps
assert "StartingManpower = 40" in nomaps

print("OK COMPAT-009 NoMaps InitialSquads cap=30; post-BodyCount; dynamic squads unchanged")
