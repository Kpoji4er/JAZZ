# One-shot: rewrite JazzGetBaseJamScore (Rel 5..95 / Rel95 zero base).
from pathlib import Path
import shutil
import time

root = Path(__file__).resolve().parents[2]
path = root / "Code" / "System_OR_Weapons.lua"
new_path = root / "Code" / "System_OR_Weapons.lua.jamrel.new"

text = path.read_text(encoding="utf-8")
start = text.find("local function JazzGetBaseJamScore(item)")
if start < 0:
    raise SystemExit("JazzGetBaseJamScore not found")
comment = text.rfind("-- JamScore scale", 0, start)
if comment < 0:
    comment = start
end = text.find("\nend\n", start)
if end < 0:
    raise SystemExit("end not found")
end += len("\nend\n")

new = (
    "-- JamScore scale 0..1000 matches ReliabilityCheck roll; display % = DivRound(score, 10).\n"
    "-- Reliability authored range is 5..95. At Rel 95 the platform base jam is 0 even with\n"
    "-- Poor/Crafted ammo. Below that, positive BaseJamChance is scaled by unreliability so\n"
    "-- high-Rel guns are not washed out by ammo BaseJam floors. Negative BaseJamChance\n"
    "-- remains a quality bonus. Serviceable base risk is still capped at 10% later.\n"
    '-- Read via GetProperty so ammo/component AddModifier ("ammo") applies.\n'
    "local function JazzGetBaseJamScore(item)\n"
    '\tlocal reliability = Clamp(item:GetProperty("Reliability") or 50, 5, 95)\n'
    '\tlocal base_jam = item:GetProperty("BaseJamChance") or 0\n'
    "\tif reliability >= 95 then\n"
    "\t\treturn 0\n"
    "\tend\n"
    "\tlocal reliability_score = Max(0, 100 - reliability)\n"
    "\tlocal score\n"
    "\tif base_jam >= 0 then\n"
    "\t\tlocal scaled = MulDivRound(base_jam, reliability_score, 95)\n"
    "\t\tscore = Max(reliability_score, scaled)\n"
    "\telse\n"
    "\t\tscore = reliability_score + base_jam\n"
    "\tend\n"
    "\treturn Clamp(score, 0, 100)\n"
    "end\n"
)

payload = text[:comment] + new + text[end:]
new_path.write_text(payload, encoding="utf-8")

for attempt in range(10):
    try:
        shutil.move(str(new_path), str(path))
        print("patched", path)
        break
    except PermissionError:
        time.sleep(0.5)
else:
    raise SystemExit(f"could not replace locked file; left at {new_path}")
