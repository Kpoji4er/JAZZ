"""Audit WeaponComponent Icon / ChipIcon coverage vs disk PNG."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
CHIPS_DIR = ROOT / "Icons" / "Upgrades" / "Chips"
FULL_DIR = ROOT / "Icons" / "Upgrades" / "Full"
CSV = ROOT / "docs" / "technical" / "weapons" / "data" / "weapon-components.csv"

MOUNT_SLOTS = {"Mount", "Mount1", "Mount2", "Mountside", "Mountfront"}


def extract_field(block: str, name: str) -> str | None:
    # Icon = "path"  (preferred form in items.lua)
    m = re.search(rf"(?<![A-Za-z]){name}\s*=\s*\"([^\"]*)\"", block)
    if m:
        return m.group(1)
    m = re.search(rf"(?<![A-Za-z]){name}\s*=\s*'([^']*)'", block)
    if m:
        return m.group(1)
    m = re.search(rf"(?<![A-Za-z]){name}\s*=\s*(false|nil)", block, re.I)
    if m:
        return ""
    return None


def parse_components(text: str) -> list[dict]:
    # ModItemWeaponComponent blocks in items.lua
    parts = re.split(r"PlaceObj\('ModItemWeaponComponent'\s*,\s*\{", text)
    comps = []
    for part in parts[1:]:
        # Next sibling ModItemWeaponComponent (indented PlaceObj)
        end = re.search(r"\n\t+PlaceObj\('ModItemWeaponComponent'", part)
        block = part[: end.start() if end else 20000]

        cid = extract_field(block, "id")
        if not cid:
            continue

        slot = extract_field(block, "Slot") or ""
        icon = extract_field(block, "Icon")
        chip = extract_field(block, "ChipIcon")
        display = ""
        m = re.search(r"DisplayName\s*=\s*T\(\s*\d+\s*,\s*--\[\[[^\]]*\]\]\s*\"([^\"]+)\"", block)
        if m:
            display = m.group(1)
        else:
            m = re.search(r"DisplayName\s*=\s*T\(\s*\d+\s*,\s*\"([^\"]+)\"", block)
            if m:
                display = m.group(1)

        comps.append(
            {
                "Id": cid,
                "Slot": slot,
                "Icon": icon if icon is not None else None,
                "ChipIcon": chip if chip is not None else None,
                "DisplayName": display,
            }
        )
    return comps


def classify_path(path: str | None) -> str:
    if path is None:
        return "missing_field"
    if path == "" or path.lower() in ("false", "nil"):
        return "empty"
    if path.startswith("Mod/e6L4ECj/Icons/Upgrades/Full/"):
        return "jazz_full"
    if path.startswith("Mod/e6L4ECj/Icons/Upgrades/Chips/"):
        return "jazz_chip"
    if path.startswith("Mod/e6L4ECj/Icons/Upgrades/"):
        return "jazz_other"
    if path.startswith("UI/Icons/Upgrades/"):
        return "vanilla"
    if path.startswith("UI/"):
        return "vanilla_other"
    if path.startswith("Mod/"):
        return "other_mod"
    return "other"


def file_exists(path: str | None) -> bool | None:
    if not path:
        return None
    if path.startswith("Mod/e6L4ECj/"):
        rel = path[len("Mod/e6L4ECj/") :]
        return (ROOT / rel).is_file()
    if path.startswith("UI/"):
        # cannot verify vanilla on disk easily — mark unknown
        return None
    return None


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8", errors="replace")
    comps = parse_components(text)
    print(f"Parsed ModItemWeaponComponent count: {len(comps)}")

    chip_pngs = {p.stem for p in CHIPS_DIR.glob("*.png")}
    full_pngs = {p.stem for p in FULL_DIR.glob("*.png")} if FULL_DIR.is_dir() else set()
    # also root Upgrades pngs that aren't chips
    root_up = ROOT / "Icons" / "Upgrades"
    root_pngs = {p.stem for p in root_up.glob("*.png")}

    print(f"Disk Chip PNGs: {len(chip_pngs)}")
    print(f"Disk Full PNGs: {len(full_pngs)}")
    print(f"Disk root Upgrades PNGs: {len(root_pngs)}")

    icon_kinds = Counter()
    chip_kinds = Counter()
    by_slot = defaultdict(lambda: {"total": 0, "no_icon": 0, "no_chip": 0, "broken_jazz_icon": 0, "broken_jazz_chip": 0})

    missing_icon = []
    missing_chip = []
    broken_icon = []
    broken_chip = []
    empty_icon = []
    empty_chip = []
    jazz_chip_no_file = []
    jazz_full_no_file = []

    for c in comps:
        slot = c["Slot"] or "?"
        by_slot[slot]["total"] += 1
        ik = classify_path(c["Icon"])
        ck = classify_path(c["ChipIcon"])
        icon_kinds[ik] += 1
        chip_kinds[ck] += 1

        # Icon gaps: missing field or empty — need jazz full or leave vanilla
        if ik in ("missing_field", "empty"):
            by_slot[slot]["no_icon"] += 1
            empty_icon.append(c)
        else:
            exists = file_exists(c["Icon"])
            if exists is False:
                by_slot[slot]["broken_jazz_icon"] += 1
                broken_icon.append(c)
                if ik == "jazz_full":
                    jazz_full_no_file.append(c)

        # Chip gaps
        if slot in MOUNT_SLOTS:
            continue  # skip mount chips by design
        if ck in ("missing_field", "empty"):
            by_slot[slot]["no_chip"] += 1
            empty_chip.append(c)
        else:
            exists = file_exists(c["ChipIcon"])
            if exists is False:
                by_slot[slot]["broken_jazz_chip"] += 1
                broken_chip.append(c)
                if ck == "jazz_chip":
                    jazz_chip_no_file.append(c)

    print("\n=== Icon path kinds ===")
    for k, v in icon_kinds.most_common():
        print(f"  {k}: {v}")

    print("\n=== ChipIcon path kinds (all slots) ===")
    for k, v in chip_kinds.most_common():
        print(f"  {k}: {v}")

    print("\n=== By slot (totals / no Icon / no ChipIcon excl mounts) ===")
    for slot in sorted(by_slot.keys()):
        s = by_slot[slot]
        print(
            f"  {slot:20s} total={s['total']:3d}  no_icon={s['no_icon']:3d}  no_chip={s['no_chip']:3d}  "
            f"broken_icon={s['broken_jazz_icon']:3d}  broken_chip={s['broken_jazz_chip']:3d}"
        )

    print(f"\n=== Empty/missing Icon ({len(empty_icon)}) ===")
    for c in sorted(empty_icon, key=lambda x: (x["Slot"], x["Id"])):
        print(f"  [{c['Slot']}] {c['Id']}")

    print(f"\n=== Broken jazz Icon path (file missing) ({len(broken_icon)}) ===")
    for c in sorted(broken_icon, key=lambda x: (x["Slot"], x["Id"])):
        print(f"  [{c['Slot']}] {c['Id']} -> {c['Icon']}")

    # Wire vs generate split for missing ChipIcon
    need_wire = []  # PNG exists as <Id>.png but ChipIcon field absent
    need_generate = []  # no matching PNG
    for c in empty_chip:
        if c["Id"] in chip_pngs:
            need_wire.append(c)
        else:
            need_generate.append(c)

    print(f"\n=== Empty/missing ChipIcon excl Mount* ({len(empty_chip)}) ===")
    print(f"  -> NEED WIRE only (PNG on disk): {len(need_wire)}")
    print(f"  -> NEED GENERATE (no PNG):       {len(need_generate)}")

    print(f"\n--- NEED GENERATE Chip ({len(need_generate)}) ---")
    for c in sorted(need_generate, key=lambda x: (x["Slot"], x["Id"])):
        print(f"  [{c['Slot']}] {c['Id']}  Display={c['DisplayName']!r}  Icon={c['Icon'] or '-'}")

    print(f"\n--- NEED WIRE ChipIcon ({len(need_wire)}) ---")
    for c in sorted(need_wire, key=lambda x: (x["Slot"], x["Id"])):
        print(f"  [{c['Slot']}] {c['Id']}")

    print(f"\n=== Broken jazz ChipIcon path ({len(broken_chip)}) ===")
    for c in sorted(broken_chip, key=lambda x: (x["Slot"], x["Id"])):
        print(f"  [{c['Slot']}] {c['Id']} -> {c['ChipIcon']}")

    # Icon pointing at Chip PNG (mis-wired)
    icon_as_chip = [c for c in comps if classify_path(c["Icon"]) == "jazz_chip"]
    print(f"\n=== Icon field points at Chips/ (misuse, {len(icon_as_chip)}) ===")
    for c in sorted(icon_as_chip, key=lambda x: x["Id"]):
        print(f"  [{c['Slot']}] {c['Id']} -> {c['Icon']}")

    # other_mod icons
    other_mod = [c for c in comps if classify_path(c["Icon"]) == "other_mod"]
    print(f"\n=== Icon from other Mod/ path ({len(other_mod)}) ===")
    for c in sorted(other_mod, key=lambda x: x["Id"])[:30]:
        print(f"  [{c['Slot']}] {c['Id']} -> {c['Icon']}")
    if len(other_mod) > 30:
        print(f"  ... +{len(other_mod)-30}")

    # Orphan chip pngs not referenced
    referenced_chips = set()
    for c in comps:
        p = c["ChipIcon"] or ""
        if "/Chips/" in p:
            referenced_chips.add(Path(p).stem)
    # also count Id-matched unwired as "soft referenced"
    soft = {c["Id"] for c in need_wire}
    orphans = sorted(chip_pngs - referenced_chips - soft)
    jazz_orphans = [n for n in orphans if n.startswith("JAZZ_")]
    vanilla_name_orphans = [n for n in orphans if not n.startswith("JAZZ_")]
    print(f"\n=== Chip PNGs with no component ChipIcon and no matching unwired Id ===")
    print(f"  JAZZ_* orphans: {len(jazz_orphans)}")
    print(f"  non-JAZZ name orphans (legacy/vanilla-id copies): {len(vanilla_name_orphans)}")

    print(f"\n=== Empty/missing Icon ({len(empty_icon)}) ===")
    for c in sorted(empty_icon, key=lambda x: (x["Slot"], x["Id"])):
        has_chip = classify_path(c["ChipIcon"]) not in ("missing_field", "empty")
        print(f"  [{c['Slot']}] {c['Id']}  chip_wired={has_chip}  disk_chip={c['Id'] in chip_pngs}")

    print(f"\n=== Full/ production PNGs: {len(full_pngs)} (ModifyWeaponDlg Jazz Full icons) ===")
    print("  Note: cabinet Icon currently uses vanilla UI/Icons/Upgrades or other Mod paths;")
    print("  Icons/Upgrades/Full/ has references only — no production Full icons yet.")

    # Coverage summary
    non_mount = [c for c in comps if c["Slot"] not in MOUNT_SLOTS]
    chip_wired = [
        c
        for c in non_mount
        if classify_path(c["ChipIcon"]) not in ("missing_field", "empty")
    ]
    print(f"\n=== Coverage summary (excl Mount*) ===")
    print(f"  components: {len(non_mount)}")
    print(f"  ChipIcon wired: {len(chip_wired)} ({100*len(chip_wired)/max(1,len(non_mount)):.0f}%)")
    print(f"  ChipIcon missing, PNG ready to wire: {len(need_wire)}")
    print(f"  ChipIcon missing, need generate: {len(need_generate)}")
    print(f"  Icon missing: {len(empty_icon)}")
    print(f"  Icon vanilla: {icon_kinds['vanilla']}")
    print(f"  Icon other_mod: {icon_kinds['other_mod']}")
    print(f"  Icon jazz_chip (wrong folder): {icon_kinds['jazz_chip']}")

    # Write summary for follow-up
    out = ROOT / "docs" / "tools" / "_audit_attachment_icons_report.txt"
    lines = []
    lines.append(f"components={len(comps)}")
    lines.append(f"non_mount={len(non_mount)}")
    lines.append(f"chip_wired={len(chip_wired)}")
    lines.append(f"need_wire_chip={len(need_wire)}")
    lines.append(f"need_generate_chip={len(need_generate)}")
    lines.append(f"empty_icon={len(empty_icon)}")
    lines.append(f"full_production_pngs={len(full_pngs)}")
    lines.append("")
    lines.append("## NEED_GENERATE_CHIP")
    for c in sorted(need_generate, key=lambda x: (x["Slot"], x["Id"])):
        lines.append(f"{c['Slot']}\t{c['Id']}\t{c['DisplayName']}\ticon={c['Icon'] or ''}")
    lines.append("")
    lines.append("## NEED_WIRE_CHIP")
    for c in sorted(need_wire, key=lambda x: (x["Slot"], x["Id"])):
        lines.append(f"{c['Slot']}\t{c['Id']}")
    lines.append("")
    lines.append("## NEED_ICON")
    for c in sorted(empty_icon, key=lambda x: (x["Slot"], x["Id"])):
        lines.append(f"{c['Slot']}\t{c['Id']}\tchip={classify_path(c['ChipIcon'])}")
    lines.append("")
    lines.append("## ICON_POINTS_AT_CHIPS")
    for c in sorted(icon_as_chip, key=lambda x: x["Id"]):
        lines.append(f"{c['Slot']}\t{c['Id']}\t{c['Icon']}")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
