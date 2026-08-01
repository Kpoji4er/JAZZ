"""Wire SIG 550/552 stock Style B Icons + fix bad DefaultComponent UnfoldStocks."""
from __future__ import annotations

import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
ICON_U = "Mod/e6L4ECj/WeaponComponents/Stock/Sig_Stock_UnFolded_v2.png"
ICON_F = "Mod/e6L4ECj/WeaponComponents/Stock/Sig_Stock_Folded.png"
ICON_H = "Mod/e6L4ECj/WeaponComponents/Stock/Sig_Stock_Heavy.png"
SIGS = ("Sig550", "Sig550Custom", "Sig552")


def patch_comp(text: str, marker: str, old: str, new: str, label: str) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing marker")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if new in body and old not in body:
        print(label, "already")
        return text
    if old not in body:
        print(label, "needle missing")
        return text
    print(label, "ok")
    return text[:start] + body.replace(old, new, 1) + rest


def wire_visuals(text: str, marker: str, entity: str, icon: str, label: str) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    changed = 0
    for gun in SIGS:
        # without Icon
        old1 = (
            f'ApplyTo = "{gun}",\n'
            f'\t\t\t\t\t\t\t\tEntity = "{entity}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Stock",'
        )
        # with vanilla Icon (heavy)
        old2 = (
            f'ApplyTo = "{gun}",\n'
            f'\t\t\t\t\t\t\t\tEntity = "{entity}",\n'
            '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/g36_stock_heavy",\n'
            '\t\t\t\t\t\t\t\tSlot = "Stock",'
        )
        new = (
            f'ApplyTo = "{gun}",\n'
            f'\t\t\t\t\t\t\t\tEntity = "{entity}",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{icon}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Stock",'
        )
        if icon in body and f'ApplyTo = "{gun}"' in body and entity in body:
            # may already be wired for this gun
            chunk_start = body.find(f'ApplyTo = "{gun}"')
            while chunk_start >= 0:
                window = body[chunk_start : chunk_start + 220]
                if entity in window and icon in window:
                    print(label, gun, "already")
                    break
                if entity in window and old1.split("Entity")[0] in window[:80]:
                    pass
                chunk_start = body.find(f'ApplyTo = "{gun}"', chunk_start + 1)
        if old2 in body:
            body = body.replace(old2, new, 1)
            changed += 1
            print(label, gun, "ok (had vanilla icon)")
        elif old1 in body:
            body = body.replace(old1, new, 1)
            changed += 1
            print(label, gun, "ok")
        else:
            # try UnfoldStocks indent (fewer tabs)
            old1b = (
                f'ApplyTo = "{gun}",\n'
                f'\t\t\t\t\t\t\tEntity = "{entity}",\n'
                '\t\t\t\t\t\t\tSlot = "Stock",'
            )
            newb = (
                f'ApplyTo = "{gun}",\n'
                f'\t\t\t\t\t\t\tEntity = "{entity}",\n'
                f'\t\t\t\t\t\t\tIcon = "{icon}",\n'
                '\t\t\t\t\t\t\tSlot = "Stock",'
            )
            if old1b in body:
                body = body.replace(old1b, newb, 1)
                changed += 1
                print(label, gun, "ok (alt indent)")
            elif f'ApplyTo = "{gun}"' in body and entity in body and icon in body:
                pass
            else:
                print(label, gun, "needle missing")
    if changed:
        return text[:start] + body + rest
    return text[:start] + body + rest


def fix_default_in_items(text: str) -> str:
    # Fix ModItemInventoryItemCompositeDef DefaultComponent for Sig550Custom / Sig552
    for wid in ("Sig550Custom", "Sig552"):
        marker = f"'Id', \"{wid}\""
        pos = text.find(marker)
        if pos < 0:
            print("items", wid, "missing")
            continue
        # find Stock slot block nearby
        stock = text.find("'SlotType', \"Stock\"", pos)
        if stock < 0 or stock > pos + 8000:
            print("items", wid, "no stock slot")
            continue
        end = text.find("'SlotType'", stock + 10)
        chunk = text[stock:end]
        if 'DefaultComponent\', "JAZZ_UnfoldStocks"' in chunk or "'DefaultComponent', \"JAZZ_UnfoldStocks\"" in chunk:
            new_chunk = chunk.replace(
                "'DefaultComponent', \"JAZZ_UnfoldStocks\"",
                "'DefaultComponent', \"JAZZ_StockLightUnFolded\"",
                1,
            )
            text = text[:stock] + new_chunk + text[end:]
            print("items", wid, "default fixed")
        else:
            print("items", wid, "default already ok / other")
    return text


def fix_companion(name: str) -> None:
    path = ROOT / "InventoryItem" / f"{name}.lua"
    text = path.read_text(encoding="utf-8")
    old = "'DefaultComponent', \"JAZZ_UnfoldStocks\","
    new = "'DefaultComponent', \"JAZZ_StockLightUnFolded\","
    if new in text:
        print(name, "companion already")
        return
    if old not in text:
        print(name, "companion needle missing")
        return
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    print(name, "companion ok")


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    text = wire_visuals(text, 'id = "JAZZ_StockLightUnFolded"', "SIGUnfoldStock", ICON_U, "UnFolded")
    text = wire_visuals(text, 'id = "JAZZ_StockLightFolded"', "SIGdefFldStock", ICON_F, "Folded")
    text = wire_visuals(text, 'id = "JAZZ_StockHeavy"', "SigErgoStock", ICON_H, "Heavy")
    text = wire_visuals(text, 'id = "JAZZ_UnfoldStocks"', "SIGUnfoldStock", ICON_U, "UnfoldStocks")
    text = fix_default_in_items(text)

    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    for _ in range(25):
        try:
            os.replace(tmp, ITEMS)
            break
        except OSError:
            time.sleep(0.3)
    else:
        raise SystemExit("locked")

    fix_companion("Sig550Custom")
    fix_companion("Sig552")
    print("done")


if __name__ == "__main__":
    main()
