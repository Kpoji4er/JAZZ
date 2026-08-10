import importlib.util
import re
from pathlib import Path

bank_path = Path(__file__).with_name("_ris_copy_bank.py")
spec = importlib.util.spec_from_file_location("bank", bank_path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

ud_root = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\UnitData")
out = Path(__file__).resolve().parents[1] / "design" / "_legion_units_catalog_dump.md"

sample = next(iter(m.DOSSIERS.values()))
fam_order = ["Recruit", "Assault", "Front", "Flanker", "Gunner", "Heavy", "Leader"]


def sort_key(uid: str):
    for i, f in enumerate(fam_order):
        if f in uid:
            return (i, uid)
    return (9, uid)


lines = [
    "# JAZZ Legion UnitData — dossier catalog",
    "",
    "Source: `docs/tools/_ris_copy_bank.py` DOSSIERS + UnitData `comment`.",
    f"Entry keys: {list(sample.keys())}",
    "",
]

for uid in sorted(m.DOSSIERS.keys(), key=sort_key):
    d = m.DOSSIERS[uid]
    comment = ""
    f = ud_root / f"{uid}.lua"
    if f.exists():
        t = f.read_text(encoding="utf-8")
        cm = re.search(r'comment = "([^"]*)"', t)
        if cm:
            comment = cm.group(1)
    title = d.get("title_ru") or d.get("title_en") or uid
    body = (
        d.get("body_ru")
        or d.get("dossier_ru")
        or d.get("text_ru")
        or d.get("ru")
        or d.get("body_en")
        or ""
    )
    lines.append(f"## {title} (`{uid}`)")
    if comment:
        lines.append(f"- Kit: `{comment}`")
    lines.append("")
    lines.append(body.strip() if isinstance(body, str) else str(body))
    lines.append("")

out.write_text("\n".join(lines), encoding="utf-8")
print("keys", list(sample.keys()))
print("wrote", out)
print("count", len(m.DOSSIERS))
