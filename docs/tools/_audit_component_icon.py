"""Audit WeaponComponent.Icon only (ModifyWeaponDlg) — not ChipIcon."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
FULL_DIR = ROOT / "Icons" / "Upgrades" / "Full"
WC_DIR = ROOT / "WeaponComponents"
OUT = ROOT / "docs" / "tools" / "_audit_component_icon_report.txt"


def extract_field(block: str, name: str) -> str | None:
    m = re.search(rf"(?<![A-Za-z]){name}\s*=\s*\"([^\"]*)\"", block)
    if m:
        return m.group(1)
    m = re.search(rf"(?<![A-Za-z]){name}\s*=\s*'([^']*)'", block)
    if m:
        return m.group(1)
    return None


def parse_components(text: str) -> list[dict]:
    parts = re.split(r"PlaceObj\('ModItemWeaponComponent'\s*,\s*\{", text)
    comps = []
    for part in parts[1:]:
        end = re.search(r"\n\t+PlaceObj\('ModItemWeaponComponent'", part)
        block = part[: end.start() if end else 20000]
        cid = extract_field(block, "id")
        if not cid:
            continue
        slot = extract_field(block, "Slot") or ""
        icon = extract_field(block, "Icon")
        display = ""
        m = re.search(
            r"DisplayName\s*=\s*T\(\s*\d+\s*,\s*--\[\[[^\]]*\]\]\s*\"([^\"]+)\"",
            block,
        )
        if m:
            display = m.group(1)
        else:
            m = re.search(r"DisplayName\s*=\s*T\(\s*\d+\s*,\s*\"([^\"]+)\"", block)
            if m:
                display = m.group(1)
        comps.append({"Id": cid, "Slot": slot, "Icon": icon, "DisplayName": display})
    return comps


def classify(path: str | None) -> str:
    if path is None:
        return "missing"
    if path == "":
        return "empty"
    if path.startswith("UI/Icons/Upgrades/"):
        return "vanilla_upgrades"
    if path.startswith("UI/"):
        return "vanilla_other"
    if path.startswith("Mod/e6L4ECj/Icons/Upgrades/Full/"):
        return "jazz_full"
    if path.startswith("Mod/e6L4ECj/Icons/Upgrades/Chips/"):
        return "jazz_chip_as_icon"
    if path.startswith("Mod/e6L4ECj/Icons/Upgrades/"):
        return "jazz_upgrades_root"
    if path.startswith("Mod/e6L4ECj/WeaponComponents/"):
        return "jazz_weaponcomponents"
    if path.startswith("Mod/e6L4ECj/"):
        return "jazz_other"
    if path.startswith("Mod/"):
        return "other_mod"
    return "other"


def main() -> None:
    comps = parse_components(ITEMS.read_text(encoding="utf-8", errors="replace"))
    kinds = Counter()
    by_slot: dict[str, Counter] = defaultdict(Counter)
    missing = []
    broken = []
    by_kind_examples: dict[str, list] = defaultdict(list)

    for c in comps:
        k = classify(c["Icon"])
        kinds[k] += 1
        by_slot[c["Slot"] or "?"][k] += 1
        if len(by_kind_examples[k]) < 5 and c["Icon"]:
            by_kind_examples[k].append(c)
        if k in ("missing", "empty"):
            missing.append(c)
            continue
        p = c["Icon"]
        if p.startswith("Mod/e6L4ECj/"):
            rel = ROOT / p[len("Mod/e6L4ECj/") :]
            if not rel.is_file():
                broken.append(c)

    full_pngs = {p.stem for p in FULL_DIR.glob("*.png")} if FULL_DIR.is_dir() else set()
    review = ROOT / "Icons" / "Upgrades" / "_review"
    review_pngs = list(review.glob("*.png")) if review.is_dir() else []
    root_pngs = list((ROOT / "Icons" / "Upgrades").glob("*.png"))

    wc_pngs = []
    if WC_DIR.is_dir():
        wc_pngs = list(WC_DIR.rglob("*.png"))

    print(f"ModItemWeaponComponent: {len(comps)}")
    print("Icon kinds:")
    for k, v in kinds.most_common():
        print(f"  {k}: {v}")

    print("\nBy slot (miss / vanilla / WC / full / other):")
    for slot in sorted(by_slot):
        c = by_slot[slot]
        miss = c["missing"] + c["empty"]
        van = c["vanilla_upgrades"] + c["vanilla_other"]
        wc = c["jazz_weaponcomponents"]
        full = c["jazz_full"]
        other = sum(c.values()) - miss - van - wc - full
        print(
            f"  {slot:16s} n={sum(c.values()):3d}  miss={miss:2d}  "
            f"vanilla={van:3d}  WC={wc:2d}  full={full}  other={other}"
        )

    print(f"\nMISSING Icon ({len(missing)}):")
    for c in sorted(missing, key=lambda x: (x["Slot"], x["Id"])):
        print(f"  [{c['Slot']}] {c['Id']}  Display={c['DisplayName']!r}")

    print(f"\nBROKEN Mod Icon paths ({len(broken)}):")
    for c in broken:
        print(f"  [{c['Slot']}] {c['Id']} -> {c['Icon']}")

    print("\nExamples by kind:")
    for k, samples in sorted(by_kind_examples.items()):
        print(f"  [{k}]")
        for c in samples:
            print(f"    {c['Id']} -> {c['Icon']}")

    print(f"\nIcons/Upgrades/Full production: {len(full_pngs)}")
    print(f"Icons/Upgrades/_review: {len(review_pngs)} -> {[p.name for p in review_pngs]}")
    print(f"Icons/Upgrades root slot_*: {[p.name for p in root_pngs]}")
    print(f"WeaponComponents PNG: {len(wc_pngs)}")
    if wc_pngs:
        by_dir = Counter(str(p.parent.relative_to(WC_DIR)).replace("\\", "/") for p in wc_pngs)
        for d, n in by_dir.most_common():
            print(f"  {d}: {n}")

    # Unique vanilla icon basenames used
    vanilla_names = Counter()
    for c in comps:
        p = c["Icon"] or ""
        if p.startswith("UI/Icons/Upgrades/"):
            vanilla_names[Path(p).name] += 1
    print(f"\nUnique vanilla upgrade icon files used: {len(vanilla_names)}")
    print("Top reused vanilla icons:")
    for name, n in vanilla_names.most_common(15):
        print(f"  {name}: {n}")

    lines = [
        f"components={len(comps)}",
        f"missing_icon={len(missing)}",
        f"broken_icon={len(broken)}",
        f"vanilla={kinds['vanilla_upgrades']+kinds['vanilla_other']}",
        f"weaponcomponents={kinds['jazz_weaponcomponents']}",
        f"jazz_full={kinds['jazz_full']}",
        "",
        "## NEED_ICON",
    ]
    for c in sorted(missing, key=lambda x: (x["Slot"], x["Id"])):
        lines.append(f"{c['Slot']}\t{c['Id']}\t{c['DisplayName']}")
    lines.append("")
    lines.append("## BROKEN")
    for c in broken:
        lines.append(f"{c['Slot']}\t{c['Id']}\t{c['Icon']}")
    lines.append("")
    lines.append("## VANILLA_REUSE")
    for name, n in vanilla_names.most_common():
        lines.append(f"{n}\t{name}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
