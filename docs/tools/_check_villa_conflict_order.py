"""K4 Guests must not create a conflict before or after dispatch."""
from pathlib import Path
import runpy
root=Path(__file__).resolve().parents[2]
items=(root.parent/'jazz-maps/items.lua').read_text(encoding='utf-8')
start=items.index('FuncCode = "Mods.FhNNYd.env.Jazz_VillaCounterAttack_Start()"')
phrase=items[items.rfind("PlaceObj('ConversationPhrase'",0,start):items.index('GoTo =',start)]
assert "PlaceObj('SectorEnterConflict'" not in phrase
runpy.run_path(str(Path(__file__).with_name('_check_villa_waiting_recovery.py')),run_name='__main__')
