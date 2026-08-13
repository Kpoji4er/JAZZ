#!/usr/bin/env python3
"""Static regression checks for JAZZ-HOTFIX-005 (no game runtime required)."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main() -> int:
    stacks = (ROOT / "Code" / "System_InventoryStacks.lua").read_text(encoding="utf-8")
    bag = (ROOT / "Code" / "System_OR_SquadBag.lua").read_text(encoding="utf-8")
    maint = (ROOT / "Code" / "System_WeaponResourceMaintenance.lua").read_text(encoding="utf-8")
    inv = (ROOT / "Code" / "Inventory.lua").read_text(encoding="utf-8")

    check("function JazzInventoryItemsCanStack" in stacks, "JazzInventoryItemsCanStack is a top-level function")
    check("RemovableComponentId" in stacks[stacks.find("function JazzInventoryItemsCanStack") : stacks.find("function JazzInventoryItemsCanStack") + 800],
          "CanStack compares RemovableComponentId")

    get_max = stacks.find("function JazzGetStackMax")
    check(get_max >= 0, "JazzGetStackMax exists")
    get_max_body = stacks[get_max : stacks.find("function JazzApplyStackContext")]
    check("IsKindOf(item, \"JAZZ_RemovableAttachment\")" not in get_max_body or "return 1" not in get_max_body,
          "JazzGetStackMax does not force remountable max=1")
    check("JazzIsStorageInventory" in get_max_body and "JazzStorageStackMax" in get_max_body,
          "storage still uses JazzStorageStackMax")

    mark = stacks.find("function JazzMarkSquadBagData")
    check(mark >= 0, "JazzMarkSquadBagData exists")
    mark_end = stacks.find("function OnMsg.LoadGame", mark)
    mark_body = stacks[mark:mark_end]
    check("Amount = 1" not in mark_body and "Amount=1" not in mark_body,
          "JazzMarkSquadBagData does not clip Amount to 1")
    check("JazzStorageStackMax" in mark_body, "JazzMarkSquadBagData still raises storage MaxStacks")

    merge = stacks.find("function MergeStackIntoContainer")
    check(merge >= 0, "MergeStackIntoContainer override exists")
    merge_body = stacks[merge : stacks.find("local JazzMoveItem_Original")]
    check("if IsKindOf(item, \"JAZZ_RemovableAttachment\") then" not in merge_body
          or "return false, item.Amount" not in merge_body,
          "MergeStackIntoContainer does not refuse all remountable merges")
    check("JazzInventoryItemsCanStack(item, item_at_dest)" in merge_body,
          "MergeStackIntoContainer uses CanStack")

    check("function InventoryStack:MergeStack" in stacks, "MergeStack override exists")
    ms = stacks.find("function InventoryStack:MergeStack")
    ms_body = stacks[ms : stacks.find("function InventoryStack:GetItemSlotUI")]
    check("JazzInventoryItemsCanStack(self, otherItem)" in ms_body, "MergeStack uses CanStack")
    check("RemovableComponentId" in stacks[stacks.find("local refund") : stacks.find("function InventoryStack:MergeStack")],
          "storage-to-personal refund copies RemovableComponentId")

    check("JazzInventoryItemsCanStack" in bag and "_SortItemsInBag" in bag,
          "bag sort consults CanStack")
    sort = bag.find("function _SortItemsInBag")
    sort_body = bag[sort : bag.find("function SquadBag:AddAndStackItem")]
    check("JazzInventoryItemsCanStack" in sort_body, "_SortItemsInBag merge uses CanStack")
    check("bag_item.class == item.class" not in sort_body,
          "_SortItemsInBag no longer class-only merges")

    norm = maint.find("function JAZZ_NormalizeRemovableAttachmentStack")
    check(norm >= 0, "JAZZ_NormalizeRemovableAttachmentStack exists")
    norm_body = maint[norm : maint.find("function JAZZ_CreateRemovableAttachment")]
    check("item.MaxStacks = 1" not in norm_body, "Normalize does not force MaxStacks=1")
    check("if not item.Amount or item.Amount < 1" in norm_body, "Normalize only floors Amount < 1")
    # Unconditional clip was `item.Amount = 1` on its own line after MaxStacks.
    check("\titem.Amount = 1\nend" not in norm_body.replace("\r\n", "\n"),
          "Normalize does not unconditionally set Amount=1")

    can_add = inv.find("function Inventory:CanAddItem")
    check(can_add >= 0, "Inventory:CanAddItem override exists")
    can_add_body = inv[can_add : inv.find("function InventoryItem:GetDeteriorationKeywordNoPrefix")]
    check("JazzInventoryItemsCanStack" in can_add_body, "CanAddItem uses CanStack")
    check("item.class == currentitem.class" not in can_add_body
          or "not JazzInventoryItemsCanStack" in can_add_body,
          "CanAddItem class equality is only a CanStack-missing fallback")

    print("RESULT: PASSED (JAZZ-HOTFIX-005 static audit)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
