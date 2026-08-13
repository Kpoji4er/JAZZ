# Bump jazz metadata for Fauda KillingWind hotfix (grit + armor FM tax once).
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
meta = ROOT / "metadata.lua"
text = meta.read_text(encoding="utf-8")
if "'version', 6149" not in text and "'version', 6150" not in text:
    raise SystemExit(f"unexpected version in {meta}")
text = text.replace("'version', 6149", "'version', 6150", 1)
bullet = (
    "- UNITS-006: Fauda KillingWind — grit via unit_damage+default gritPerEnemyHit; "
    "armor FM tax once (OnGearChanged no ConsumeAP) [no new game]\\n"
)
marker = "'last_changes', \""
i = text.find(marker)
if i < 0:
    raise SystemExit("last_changes marker not found")
insert_at = i + len(marker)
# Avoid duplicate prepend
if text.startswith(bullet, insert_at) or text[insert_at : insert_at + 40].startswith(
    "- UNITS-006: Fauda KillingWind — grit via"
):
    print("last_changes already has KillingWind grit bullet")
else:
    text = text[:insert_at] + bullet + text[insert_at:]
meta.write_text(text, encoding="utf-8", newline="\n")
# Verify no raw LF inside last_changes value
start = text.find(marker) + len(marker)
end = text.find('",', start)
chunk = text[start:end]
if "\n" in chunk or "\r" in chunk:
    raise SystemExit("RAW newline inside last_changes — abort")
print("OK version=6150 last_changes prepended")
