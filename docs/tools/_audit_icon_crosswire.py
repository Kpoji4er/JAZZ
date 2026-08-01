"""Audit accidental icon cross-wiring / content dupes for recent Style B batch."""
from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = (ROOT / "items.lua").read_text(encoding="utf-8")
WC = ROOT / "WeaponComponents"

FOCUS = (
    "G36_Stock",
    "Sig_Stock",
    "SVT_Mag",
    "AUG_Mag",
    "FAMAS_Mag",
    "AR10_Mag",
    "M72LAW",
    "AK74_Mag",
)


def md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def main() -> None:
    # --- identical PNG content ---
    by_hash: dict[str, list[str]] = defaultdict(list)
    for p in WC.rglob("*.png"):
        by_hash[md5(p)].append(str(p.relative_to(ROOT)).replace("\\", "/"))

    print("=== Exact duplicate PNG content (focus-related or cross-family) ===")
    shown = 0
    for h, files in sorted(by_hash.items(), key=lambda x: -len(x[1])):
        if len(files) < 2:
            continue
        focus = any(any(k in f for k in FOCUS) for f in files)
        stems = {Path(f).stem.split("_")[0] for f in files}
        if focus or len(stems) > 1:
            shown += 1
            print(f"\nmd5={h[:10]} n={len(files)}")
            for f in files:
                print(" ", f)
    if not shown:
        print("(none)")

    # Sig vs G36 specifically
    a = WC / "Stock" / "Sig_Stock_UnFolded.png"
    b = WC / "Stock" / "Sig_Stock_UnFolded_v2.png"
    g = WC / "Stock" / "G36_Stock_Normal.png"
    print("\n=== Sig UnFolded / G36 stock file check ===")
    for p in (a, b, g):
        print(f"  {p.relative_to(ROOT)} exists={p.exists()} size={p.stat().st_size if p.exists() else 0}")
    if a.exists() and b.exists():
        print(f"  UnFolded == UnFolded_v2: {md5(a) == md5(b)}")
    if b.exists() and g.exists():
        print(f"  UnFolded_v2 == G36: {md5(b) == md5(g)}")
    if a.exists() and g.exists():
        print(f"  UnFolded == G36: {md5(a) == md5(g)}")

    # Wired paths
    paths = set(re.findall(r'Mod/e6L4ECj/(WeaponComponents/[^"\']+\.png)', ITEMS))
    paths |= set(re.findall(r'Mod/e6L4ECj/(WeaponIcons/[^"\']+\.png)', ITEMS))
    print("\n=== Wired focus paths ===")
    for rel in sorted(p for p in paths if any(k in p for k in FOCUS)):
        on_disk = (ROOT / rel).exists()
        print(f"  {'OK' if on_disk else 'MISSING'} {rel}")

    # Orphan: UnFolded without v2 wired?
    print("\n=== Sig UnFolded path wiring ===")
    print("  UnFolded.png wired:", any(p.endswith("Sig_Stock_UnFolded.png") for p in paths))
    print("  UnFolded_v2.png wired:", any(p.endswith("Sig_Stock_UnFolded_v2.png") for p in paths))

    # Cross-family ApplyTo for focus icons
    print("\n=== Cross-family ApplyTo (should be empty) ===")
    expect = {
        "G36_Stock": {"G36", "G36c"},
        "Sig_Stock": {"Sig550", "Sig550Custom", "Sig552"},
        "SVT_Mag10": {"SVT40"},
        "SVT_MagLarge": {"AVT40"},
        "AUG_Mag": {"AUG"},
        "FAMAS_Mag": {"FAMAS"},
        "AR10_Mag": {"AR10", "AR10DMR"},
        "M72LAW": {"M72LAW"},
    }
    bad = 0
    for vm in re.finditer(r"PlaceObj\('WeaponComponentVisual', \{(.*?)\}\),", ITEMS, re.S):
        body = vm.group(1)
        icon_m = re.search(r'Icon\s*=\s*"([^"]+)"', body)
        if not icon_m:
            continue
        icon = icon_m.group(1)
        apply_m = re.search(r'ApplyTo\s*=\s*"([^"]+)"', body)
        apply = apply_m.group(1) if apply_m else "(default)"
        for key, allowed in expect.items():
            if key not in icon:
                continue
            if apply not in allowed and apply != "(default)":
                print(f"  BAD {icon} -> ApplyTo={apply} (expected {sorted(allowed)})")
                bad += 1
    if not bad:
        print("(none)")

    # Duplicate ApplyTo+Slot inside one component for focus icons
    print("\n=== Duplicate ApplyTo+Slot rows (focus icons) ===")
    parts = ITEMS.split("PlaceObj('ModItemWeaponComponent'")
    found = 0
    for part in parts[1:]:
        idm = re.search(r'id = "([^"]+)"', part)
        if not idm:
            continue
        cid = idm.group(1)
        buckets: dict[tuple[str, str], list[str]] = defaultdict(list)
        for vm in re.finditer(r"PlaceObj\('WeaponComponentVisual', \{(.*?)\}\),", part, re.S):
            body = vm.group(1)
            icon_m = re.search(r'Icon\s*=\s*"([^"]+)"', body)
            if not icon_m:
                continue
            icon = icon_m.group(1)
            if not any(k in icon for k in FOCUS):
                continue
            apply = re.search(r'ApplyTo\s*=\s*"([^"]+)"', body)
            slot = re.search(r'Slot\s*=\s*"([^"]+)"', body)
            a = apply.group(1) if apply else "(default)"
            s = slot.group(1) if slot else "?"
            buckets[(a, s)].append(icon)
        for (a, s), icons in buckets.items():
            if len(icons) > 1:
                found += 1
                print(f"  {cid} ApplyTo={a} Slot={s} x{len(icons)} -> {icons}")
    if not found:
        print("(none)")

    # SVT/AVT magazine map full
    print("\n=== SVT40/AVT40 magazine Visual Icons ===")
    for vm in re.finditer(r"PlaceObj\('WeaponComponentVisual', \{(.*?)\}\),", ITEMS, re.S):
        body = vm.group(1)
        if "SVT40" not in body and "AVT40" not in body:
            continue
        slot_m = re.search(r'Slot\s*=\s*"([^"]+)"', body)
        if not slot_m or slot_m.group(1) != "Magazine":
            continue
        apply = re.search(r'ApplyTo\s*=\s*"([^"]+)"', body)
        icon = re.search(r'Icon\s*=\s*"([^"]+)"', body)
        ent = re.search(r'Entity\s*=\s*"([^"]+)"', body)
        print(
            f"  ApplyTo={apply.group(1) if apply else '?'} "
            f"Entity={ent.group(1) if ent else '?'} "
            f"Icon={icon.group(1) if icon else '(none)'}"
        )


if __name__ == "__main__":
    main()
