"""Read-only catalog: which firearms expose Scope/Side/Under/Handguard and which mount meshes their components spawn.

Usage (from jazz/):
  python docs/tools/_audit_weapon_rails.py
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INV = os.path.join(ROOT, "InventoryItem")
ITEMS = os.path.join(ROOT, "items.lua")
INTERESTING = {
    "Scope", "Side", "Side1", "Side2", "Under", "Handguard",
    "Bipod", "Mount", "Mountside", "Grenadelauncher",
}
MOUNT_HINT = re.compile(r"Mount|Rail|Picatinny|RIS", re.I)


def parse_companions():
    slot_re = re.compile(r"'SlotType',\s*\"([^\"]+)\"")
    rows = []
    for fn in sorted(os.listdir(INV)):
        if not fn.endswith(".lua") or ".bak" in fn:
            continue
        path = os.path.join(INV, fn)
        text = open(path, encoding="utf-8", errors="replace").read()
        if "ComponentSlots" not in text:
            continue
        parts = text.split("PlaceObj('WeaponComponentSlot'")
        slots = {}
        for part in parts[1:]:
            match = slot_re.search(part)
            if not match:
                continue
            slot_type = match.group(1)
            if slot_type not in INTERESTING:
                continue
            chunk = part[:1600]
            fixed = "'Modifiable', false" in chunk[:500]
            can_empty = "'CanBeEmpty', true" in chunk[:600]
            avail_match = re.search(r"'AvailableComponents',\s*\{(.*?)\}", chunk, re.S)
            avail = re.findall(r"\"([^\"]+)\"", avail_match.group(1)) if avail_match else []
            default_match = re.search(r"'DefaultComponent',\s*\"([^\"]+)\"", chunk)
            default = default_match.group(1) if default_match else ""
            slots[slot_type] = {
                "fixed": fixed,
                "empty": can_empty,
                "default": default,
                "avail": avail,
            }
        if slots:
            rows.append((fn[:-4], slots))
    return rows


def parse_mount_visuals():
    text = open(ITEMS, encoding="utf-8", errors="replace").read()
    by_weapon = {}
    blocks = text.split("PlaceObj('WeaponComponentVisual'")
    apply_re = re.compile(r"ApplyTo\s*=\s*\"([^\"]+)\"")
    entity_re = re.compile(r"Entity\s*=\s*\"([^\"]+)\"")
    for block in blocks[1:]:
        chunk = block[:800]
        entity_match = entity_re.search(chunk)
        if not entity_match or not MOUNT_HINT.search(entity_match.group(1)):
            continue
        apply_match = apply_re.search(chunk)
        weapon = apply_match.group(1) if apply_match else "*"
        by_weapon.setdefault(weapon, set()).add(entity_match.group(1))
    return by_weapon


def main():
    rows = parse_companions()
    mounts = parse_mount_visuals()
    print(f"WEAPONS {len(rows)}")
    for name, slots in rows:
        bits = []
        for slot_type, info in slots.items():
            flags = []
            if info["fixed"]:
                flags.append("FIXED")
            if info["empty"]:
                flags.append("empty")
            if info["default"]:
                flags.append("def=" + info["default"])
            shown = ",".join(info["avail"][:6])
            extra = "" if len(info["avail"]) <= 6 else f"+{len(info['avail']) - 6}"
            bits.append(f"{slot_type}[{','.join(flags)}] {shown}{extra}")
        mount_bits = sorted(mounts.get(name, ()))
        print(f"{name} | {' || '.join(bits)}")
        if mount_bits:
            print("    mounts: " + ", ".join(mount_bits))


if __name__ == "__main__":
    main()
