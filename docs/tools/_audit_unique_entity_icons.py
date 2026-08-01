"""Map unique Visuals Entity sets vs shared Icon — backlog for Icon style B."""
from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
OUT = ROOT / "docs" / "tools" / "_audit_unique_entity_icons_report.txt"
MOUNT = {"Mount", "Mount1", "Mount2", "Mountside", "Mountfront"}


def extract_field(block: str, name: str) -> str | None:
    m = re.search(rf"(?<![A-Za-z]){name}\s*=\s*\"([^\"]*)\"", block)
    return m.group(1) if m else None


def parse_components(text: str) -> list[dict]:
    parts = re.split(r"PlaceObj\('ModItemWeaponComponent'\s*,\s*\{", text)
    comps = []
    for part in parts[1:]:
        end = re.search(r"\n\t+PlaceObj\('ModItemWeaponComponent'", part)
        block = part[: end.start() if end else 30000]
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
            display = m.group(1) if m else ""

        # Collect Entity= from WeaponComponentVisual blocks
        entities = []
        for vm in re.finditer(
            r"PlaceObj\('WeaponComponentVisual',\s*\{(.*?)\}\)",
            block,
            re.S,
        ):
            vb = vm.group(1)
            # avoid matching nested braces badly: stop at first Entity if block huge
            ent = extract_field(vb, "Entity")
            vslot = extract_field(vb, "Slot") or ""
            apply = extract_field(vb, "ApplyTo")
            if ent:
                entities.append((vslot, ent, apply or ""))

        # Stable signature of visual mesh set (entity names only, ignore ApplyTo variants for uniqueness of "look")
        ent_names = tuple(sorted({e for _, e, _ in entities if e}))
        # Also signature including ApplyTo-specific mesh swaps (more precise uniqueness)
        ent_full = tuple(sorted({(s, e, a) for s, e, a in entities}))

        comps.append(
            {
                "Id": cid,
                "Slot": slot,
                "Icon": icon,
                "DisplayName": display,
                "entities": entities,
                "ent_names": ent_names,
                "ent_sig": ent_names,  # primary uniqueness key
            }
        )
    return comps


def icon_kind(path: str | None) -> str:
    if path is None:
        return "missing"
    if path.startswith("UI/Icons/Upgrades/"):
        return "vanilla"
    if path.startswith("Mod/e6L4ECj/WeaponComponents/"):
        return "wc"
    if path.startswith("Mod/e6L4ECj/Icons/Upgrades/Full/"):
        return "full"
    if path.startswith("Mod/"):
        return "mod_other"
    return "other"


def suggested_wc_path(c: dict) -> str:
    slot = c["Slot"] or "Misc"
    # map slots to WC subdirs used today
    folder = {
        "Scope": "Optics",
        "Side": "Side",
        "Side2": "Side",
        "Muzzle": "Muzzle",
        "Barrel": "Barrel",
        "Magazine": "Magazine",
        "Stock": "Stock",
        "Under": "Under",
        "Handguard": "Handguard",
        "Handgrip": "Handgrip",
        "Bipod": "Bipod",
        "General": "General",
        "Grenadelauncher": "Under",
        "Trigger": "Carbine",
        "Freeswap": "General",
        "Mountfront": "Mount",
    }.get(slot, slot)
    # Prefer short name without JAZZ_ for WC legacy, but Id is safer for uniqueness
    return f"Mod/e6L4ECj/WeaponComponents/{folder}/{c['Id']}.png"


def main() -> None:
    comps = parse_components(ITEMS.read_text(encoding="utf-8", errors="replace"))

    # Group by entity signature
    by_ent: dict[tuple, list] = defaultdict(list)
    for c in comps:
        by_ent[c["ent_sig"]].append(c)

    # Group by icon path
    by_icon: dict[str, list] = defaultdict(list)
    for c in comps:
        by_icon[c["Icon"] or ""].append(c)

    missing = [c for c in comps if not c["Icon"]]
    # Unique entity sets that share a vanilla icon with other different entity sets
    # Rule: if component has non-empty unique ent_sig, its Icon should not be shared
    # with a different ent_sig (unless both empty / same).

    need_unique: list[dict] = []
    # For each icon used by >1 distinct ent_sigs → all those comps need unique icons
    # except if they truly share the same mesh set
    shared_icon_conflicts = []
    for icon, group in by_icon.items():
        if not icon or icon_kind(icon) == "missing":
            continue
        sigs = {c["ent_sig"] for c in group}
        # filter empty entity components separately
        nonempty = [c for c in group if c["ent_sig"]]
        nonempty_sigs = {c["ent_sig"] for c in nonempty}
        if len(nonempty_sigs) > 1:
            shared_icon_conflicts.append((icon, nonempty))

    # Components whose ent_sig appears only once (unique mesh) but Icon is vanilla
    # OR missing OR shared with other sigs
    unique_mesh_comps = []
    for sig, group in by_ent.items():
        if not sig:
            continue
        if len(group) == 1:
            unique_mesh_comps.append(group[0])

    # Need icon if: missing OR (unique mesh AND icon shared with different mesh) OR (unique mesh AND vanilla)
    # User rule: unique entity => unique icon
    # So: for every unique ent_sig (appearing once), Icon path must be unique to that component
    # (or at least not shared with another different sig — same sig can share).

    backlog = []
    reasons = Counter()
    for c in comps:
        if c["Slot"] in MOUNT and c["Slot"] != "Mountfront":
            continue  # mounts usually not shown; Mountfront U100 is in missing list
        kind = icon_kind(c["Icon"])
        sig = c["ent_sig"]
        same_sig = by_ent[sig]
        icon_users = by_icon[c["Icon"] or ""]
        other_sigs_same_icon = {
            x["ent_sig"] for x in icon_users if x["ent_sig"] != sig and x["ent_sig"]
        }

        reason = None
        if kind == "missing":
            reason = "missing_icon"
        elif not sig:
            # no entity — skip uniqueness rule (defaults / abstract)
            reason = None
        elif len(same_sig) == 1 and kind == "vanilla":
            # unique mesh but vanilla (likely shared stock art)
            # still need unique only if icon is reused by other meshes OR user wants all unique meshes unique icons
            if other_sigs_same_icon or len(icon_users) > 1:
                reason = "unique_mesh_shared_vanilla"
            else:
                # unique mesh, vanilla icon used only by this one — OK-ish but still not "own" asset
                reason = "unique_mesh_solo_vanilla"
        elif len(same_sig) == 1 and kind == "wc":
            # unique mesh with WC icon — check if WC path shared
            if other_sigs_same_icon:
                reason = "unique_mesh_shared_wc"
            else:
                reason = None  # already unique
        elif len(same_sig) > 1:
            # several comps share same mesh set — OK to share icon among them
            if kind == "missing":
                reason = "missing_icon"
            elif other_sigs_same_icon:
                reason = "mesh_group_shares_icon_with_other_meshes"
            else:
                reason = None

        if reason:
            reasons[reason] += 1
            backlog.append({**c, "reason": reason, "suggest": suggested_wc_path(c)})

    # Deduplicate priority lists
    must = [b for b in backlog if b["reason"] in (
        "missing_icon",
        "unique_mesh_shared_vanilla",
        "unique_mesh_shared_wc",
        "mesh_group_shares_icon_with_other_meshes",
    )]
    nice = [b for b in backlog if b["reason"] == "unique_mesh_solo_vanilla"]

    print(f"components={len(comps)}")
    print(f"unique entity signatures (non-empty): {sum(1 for s,g in by_ent.items() if s)}")
    print(f"empty-entity comps: {len(by_ent.get(tuple(), []))}")
    print(f"icon paths with multi-mesh conflict: {len(shared_icon_conflicts)}")
    print("reasons:", dict(reasons))
    print(f"\nMUST generate/replace Icon (shared or missing): {len(must)}")
    print(f"NICE (unique mesh, solo vanilla — still not own WC asset): {len(nice)}")

    print("\n=== MUST by slot ===")
    by_slot = defaultdict(list)
    for b in must:
        by_slot[b["Slot"]].append(b)
    for slot in sorted(by_slot):
        print(f"\n[{slot}] ({len(by_slot[slot])})")
        for b in sorted(by_slot[slot], key=lambda x: x["Id"]):
            ents = ",".join(b["ent_sig"][:3])
            if len(b["ent_sig"]) > 3:
                ents += f",+{len(b['ent_sig'])-3}"
            print(
                f"  {b['Id']:40s} {b['reason']:36s} icon={b['Icon'] or '-'}  "
                f"ents=[{ents}]"
            )

    print(f"\n=== NICE unique_mesh_solo_vanilla ({len(nice)}) sample ===")
    for b in sorted(nice, key=lambda x: (x["Slot"], x["Id"]))[:40]:
        print(f"  [{b['Slot']}] {b['Id']}  icon={b['Icon']}")
    if len(nice) > 40:
        print(f"  ... +{len(nice)-40}")

    # Existing WC icons inventory
    wc = ROOT / "WeaponComponents"
    wc_png = list(wc.rglob("*.png")) if wc.is_dir() else []
    print(f"\nExisting WeaponComponents PNG: {len(wc_png)}")

    lines = []
    lines.append(f"style=B WeaponComponents 100x100 3D")
    lines.append(f"must={len(must)}")
    lines.append(f"nice_solo_vanilla={len(nice)}")
    lines.append("")
    lines.append("## MUST")
    for b in sorted(must, key=lambda x: (x["Slot"], x["Id"])):
        lines.append(
            f"{b['Slot']}\t{b['Id']}\t{b['reason']}\t{b['Icon'] or ''}\t{b['suggest']}\t"
            + "|".join(b["ent_sig"])
        )
    lines.append("")
    lines.append("## NICE_SOLO_VANILLA")
    for b in sorted(nice, key=lambda x: (x["Slot"], x["Id"])):
        lines.append(
            f"{b['Slot']}\t{b['Id']}\t{b['Icon'] or ''}\t{b['suggest']}\t"
            + "|".join(b["ent_sig"])
        )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
