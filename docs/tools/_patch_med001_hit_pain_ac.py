# One-shot: add AC-012 for JazzPainOnDamagingHit to JAZZ-MED-001.md
from pathlib import Path
import re

p = Path(__file__).resolve().parents[1] / "specs" / "active" / "JAZZ-MED-001.md"
text = p.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)

# Fix backticks in REQ-010 if stripped
for i, l in enumerate(lines):
	if "JAZZ-MED-001-REQ-010" in l and "via JazzPainOnDamagingHit from ApplyDamageAndEffects" in l:
		lines[i] = l.replace(
			"via JazzPainOnDamagingHit from ApplyDamageAndEffects",
			"via `JazzPainOnDamagingHit` from `ApplyDamageAndEffects`",
		)
		print("fixed REQ-010 backticks")
		break

if any("JAZZ-MED-001-AC-012" in l for l in lines):
	print("AC-012 already present")
	p.write_text("".join(lines), encoding="utf-8")
	raise SystemExit(0)

crit_i = next(i for i, l in enumerate(lines) if "JAZZ-MED-001-AC-011" in l and "PASS" not in l)
ev_i = next(i for i, l in enumerate(lines) if "JAZZ-MED-001-AC-011" in l and "PASS" in l)

m = re.match(r"(- `JAZZ-MED-001-AC-011`)(\s*[—–-]\s*)(.*)", lines[crit_i])
if not m:
	raise SystemExit(f"cannot parse criteria: {lines[crit_i]!r}")
sep = m.group(2)
crit = (
	f"- `JAZZ-MED-001-AC-012`{sep}"
	"static: solid damaging hit -> `JazzPainOnDamagingHit` +1 (cap 8); "
	"graze excluded; no double with BAT when residual damage > 0.\n"
)
lines.insert(crit_i + 1, crit)

# evidence index may have shifted
ev_i = next(i for i, l in enumerate(lines) if "JAZZ-MED-001-AC-011" in l and "PASS" in l)
m2 = re.match(r"(- `JAZZ-MED-001-AC-011`: `PASS`)(\s*[—–-]\s*)(.*)", lines[ev_i])
if not m2:
	raise SystemExit(f"cannot parse evidence: {lines[ev_i]!r}")
ev = (
	f"- `JAZZ-MED-001-AC-012`: `PASS`{m2.group(2)}"
	"static: `JazzPainOnDamagingHit` (+1 Pain, damage>0, graze excluded) "
	"from `ApplyDamageAndEffects`; BAT full-absorb Pain only when residual<=0.\n"
)
lines.insert(ev_i + 1, ev)

p.write_text("".join(lines), encoding="utf-8")
print("OK AC-012 inserted")
