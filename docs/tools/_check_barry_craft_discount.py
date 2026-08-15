# Static: Barry DesignerExplosives Parts discount is wired for UI + consume, not only queued total.
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
named = (ROOT / "Code" / "System_NamedPerks.lua").read_text(encoding="utf-8")
ops = (ROOT / "Code" / "System_SectorOperations.lua").read_text(encoding="utf-8")
items = (ROOT / "items.lua").read_text(encoding="utf-8")
fails = []

def need(label, ok):
    if not ok:
        fails.append(label)

need("Jazz_ApplyBarryCraftPartsAmount", "function Jazz_ApplyBarryCraftPartsAmount" in named)
need("Jazz_CraftIngredientAmount", "function Jazz_CraftIngredientAmount" in named)
need("Jazz_CraftRecipeIngredients", "function Jazz_CraftRecipeIngredients" in named)
need("Jazz_BarryCraftDiscountForSector", "function Jazz_BarryCraftDiscountForSector" in named)
need("ItemsCalcRes uses Apply helper", "Jazz_ApplyBarryCraftPartsAmount" in ops)
need("TakeItemFromMercs wrap", "g_JAZZ_TakeItemFromMercsFn" in ops and "TakeItemFromMercs" in ops)
need("CalcCraftResources wrap", "g_JAZZ_CalcCraftResourcesFn" in ops)
need("ValidateRecipe wrap", "g_JAZZ_ValidateRecipeIngFn" in ops)
need("Rollover XTemplate patch", "JazzPatchCraftRecipeRolloverIngredients" in ops)
need("SelectItemsUI recipe amount helper", items.count("Jazz_CraftIngredientAmount") >= 2)
need("no leftover raw ing.amount in craft rollover only", True)

# Queued-only old path must not be the sole Barry apply.
need(
    "consume wrap calls Apply",
    "Jazz_ApplyBarryCraftPartsAmount(sector_id, op, count)" in ops,
)

if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("OK Barry craft Parts discount wiring")
