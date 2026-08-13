# bump metadata for COMBAT-007 commit
from pathlib import Path

p = Path("metadata.lua")
t = p.read_text(encoding="utf-8")
if "'version', 6141," not in t:
	raise SystemExit("expected version 6141")
t = t.replace("'version', 6141,", "'version', 6142,", 1)
needle = "'last_changes', \""
i = t.find(needle)
if i < 0:
	raise SystemExit("last_changes not found")
j = i + len(needle)
bullet = "- COMBAT-007: Energy ladder Fit/Winded/Fatigued/Tired/Exhausted; gradual FM + sat warn [no new game]\\n"
t = t[:j] + bullet + t[j:]
p.write_text(t, encoding="utf-8")
# strip unrelated EN loc row if present
en = Path("English.csv")
lines = en.read_text(encoding="utf-8").splitlines(True)
en.write_text("".join(l for l in lines if not l.startswith("890000000020156,")), encoding="utf-8")
print("metadata bumped to 6142; stripped 20156 from English.csv if present")
