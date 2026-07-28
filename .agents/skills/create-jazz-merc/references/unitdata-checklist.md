# UnitData / packaging checklist

После генерации проверить:

## jazz-units

- [ ] `UnitData/<unit_id>.lua` companion существует
- [ ] `metadata.lua` code/items регистрируют UnitData + VoiceResponse + Loot
- [ ] `items.lua` ModItemUnitDataCompositeDef синхронен с companion
- [ ] `Equipment` → существующий `Loot_JAZZ_*`
- [ ] Tier loot items существуют (weapon/armor/ammo ids)
- [ ] `StartingPerks` ids существуют (включая `Jazz_Perk_*`)
- [ ] `Portrait` / `BigPortrait` → `Mod/Dv3mFVN/MercPortraits/<portrait_id>.png` (+ `_Big`)
- [ ] PNG на диске 300×300 и 2000×2000
- [ ] `Likes`/`Dislikes` target unit ids валидны
- [ ] `VoiceResponseId` совпадает; FallbackMissingVR при partial VR

## jazz

- [ ] `CharacterEffect/Jazz_Perk_<…>.lua` если именной перк новый
- [ ] Icon path валиден или placeholder отмечен
- [ ] `Russian.csv` + `English.csv`: все новые T-id, `needs Russian=0`, `needs English=0`

## Sync

- [ ] `$sync-jazz-generated-data` audit clean для затронутых пакетов
- [ ] Не смешивать с посторонним dirty state
