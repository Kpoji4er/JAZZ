# Static checks for JAZZ-STRATEGY-017 money cargo sync.
# Run: python docs/tools/_test_legion_money_cargo.py

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
patrols = (ROOT / "Code" / "Guardpost_Patrols.lua").read_text(encoding="utf-8")
util = (ROOT / "Code" / "UtilityFunc.lua").read_text(encoding="utf-8")

assert "jazz_legion_ai_cargo" in patrols, "cargo tag missing"
assert "lSyncMoneyCargo" in patrols, "sync helper missing"
assert "lClearTaggedMoneyCargo" in patrols, "clear helper missing"
assert "lResyncManagedMoneyCargo" in patrols, "resync helper missing"
assert "JAZZ_LegionAIResyncMoneyCargo" in patrols, "public resync missing"
assert "lSyncMoneyCargo(squad, squad_state.payload.money)" in patrols, "tax collect must sync"
assert 'role == "shipment" or role == "supply"' in patrols, "supply spawn must load cargo"
assert "JAZZ_LegionAIResyncMoneyCargo" in util, "loot regen must resync cargo"
assert "OnMsg.ConflictStart" in patrols, "ConflictStart resync missing"

print("OK STRATEGY-017 money cargo static checks")
