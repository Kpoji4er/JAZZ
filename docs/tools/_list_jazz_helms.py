# -*- coding: utf-8 -*-
"""List JAZZ helmet / head armor for appearance mapping."""
from __future__ import annotations

import re
from pathlib import Path

jazz = Path(__file__).resolve().parents[2]
items_text = (jazz / "items.lua").read_text(encoding="utf-8", errors="replace")
inv = jazz / "InventoryItem"

# Index ModItem blocks by Id
block_re = re.compile(
    r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{(.*?)\n\t\}\),",
    re.S,
)
blocks_by_id: dict[str, str] = {}
for m in block_re.finditer(items_text):
    body = m.group(1)
    idm = re.search(r"'Id',\s*\"([^\"]+)\"", body)
    if idm:
        blocks_by_id[idm.group(1)] = body

HELM_NAME = re.compile(
    r"Helm|Helmet|Cap|Altyn|Mich|Stahl|STSH|ProTec|Wielding|Adrian|6b7|"
    r"SovietHelm|PASGTHelm|SpectraHelm|UHMWPEHelm|GuardianHelm|MetalHelm|"
    r"M1Helm|Construction",
    re.I,
)

rows = []
for p in sorted(inv.glob("JazzArmor*.lua")):
    t = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"DefineClass\.(\w+)\s*=", t)
    if not m:
        continue
    iid = m.group(1)
    if "Plates" in iid:
        continue

    body = blocks_by_id.get(iid, "")
    slot = None
    for src in (t, body):
        sm = re.search(r"['\"]Slot['\"],\s*['\"]([^'\"]+)['\"]", src)
        if not sm:
            sm = re.search(r"Slot\s*=\s*['\"]([^'\"]+)['\"]", src)
        if sm:
            slot = sm.group(1)
            break

    dn = re.search(
        r"DisplayName\s*=\s*T\(\d+,\s*--\[\[.*?\]\]\s*\"([^\"]+)\"\)", t, re.S
    )
    if not dn:
        dn = re.search(r"DisplayName\s*=\s*T\(\d+,\s*\"([^\"]+)\"\)", t)
    comment = re.search(r'comment\s*=\s*"([^"]*)"', t)

    is_head = slot == "Head"
    is_name_helm = bool(HELM_NAME.search(iid))
    if not (is_head or (slot is None and is_name_helm) or (slot == "HeadGear" and is_name_helm)):
        # include all Slot=Head; exclude HeadGear cosmetics unless helm-named
        if slot != "Head":
            continue

    rows.append(
        {
            "slot": slot or "Head?",
            "id": iid,
            "name": dn.group(1) if dn else "",
            "comment": comment.group(1) if comment else "",
        }
    )

print(f"count={len(rows)}")
for r in rows:
    print(f"{r['slot']}\t{r['id']}\t{r['name']}\t{r['comment']}")
