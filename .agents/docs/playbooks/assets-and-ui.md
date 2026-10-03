# Assets, UI и эффекты

## Перед правкой

1. `.agents/docs/reference/project-scope.md`
2. `.agents/docs/reference/runtime-model.md`
3. Для Entity/ресурсов проверить межпакетные ссылки в metadata.

## Рекомендации

- Текстуры моделей (BC/NM/RM/AO), упаковка и инверсия каналов — [ja3-texture-preparation.md](ja3-texture-preparation.md). Для стандартного RM: R=G=roughness, B=metallic; весь RGB не инвертировать.

- Изменения в entity/ресурсах не должны отрывать контракты с юнитами и карты.
- `jazz` использует `jazz_assets`; любая новая ссылка `Mod/<id>/...` требует metadata-задекларированной зависимости.
- При работе с FX/UI избегать скрытых глобальных side effects, которые не очищаются при `reload`.
- Новые сателлитные role icons (`SquadsIcons/Enemy/<faction>/<faction>_<ROLE>_squad.png`) — по skill `$create-jazz-squad-icons`; каталог: `docs/technical/systems/squad-role-icons.md`.
- Status effect icons (`Icons/StatusEffects/*.png`, 40×40) — skill `$create-jazz-status-icons`; style/prompts — `Icons/StatusEffects/references/PROMPT.md`.
- HUD / hotbar **action** icons (`Perks/SignatureAbilities/*.png` 108×54 dual strip; medical subset `Icons/Med/`) — skill `$create-jazz-action-icons`; style bank `Icons/Hud/references/PROMPT.md`. Не путать с Personal perk tiles.
- Attachment icons — **два разных skill**:
  - `$create-jazz-component-icons` → полная `WeaponComponent.Icon` (`Icons/Upgrades/Full/`, кабинет моддинга)
  - `$create-jazz-chip-icons` → `ChipIcon` миниатюра (`Icons/Upgrades/Chips/`, inventory/HUD chips)
- Иконки именных перков (`Perks/Personal/*.png`, 68×68 RGBA) — skill `$create-jazz-perk-icons`; фон обязательно прозрачный, символ выводить из Description/Mechanics. Hotbar SignatureAbilities → `$create-jazz-action-icons`.
- Портреты мерков/NPC (PNG 300×300 + 2000×2000, стиль JA3) — пакет `jazz-units`, каталоги `MercPortraits/` и `NPCPortraits/`; генерация по `$create-jazz-merc-portraits`. `Images/` только для логотипа мода.
- Экспорт меша (оружие/броня): не кастомные нормали, всегда recalc — `.agents/docs/playbooks/mesh-export-normals.md`.
- После editor import оружия с numeric DDS — `$rename-jazz-weapon-textures` (`Entity_MapType.dds`, Fallbacks-пара, `.mtl`/`items.lua`; затем Mod Editor mtlbin rebuild).
- Свой Hat/Body/Pants/Armor на риг мерка — `$export-jazz-character-element`. Посадку и equipped appearance Легиона — `.agents/docs/playbooks/legion-armor-modeling.md`.
- Новый building slab (стены/пол/крыша со своими мешами и текстурами) — гайд: `docs/design/ja3-how-to-custom-slabs.md` (EN: `docs/design/ja3-how-to-custom-slabs.en.md`). Предпочтительно отдельный мод (не `jazz_assets`); комнаты на картах только выбирают `id`. Своих slab-материалов в JAZZ пока нет.

## После правки

- Технически зафиксировать изменённые поверхности (resource IDs, entity IDs, load-порядок).
- Если UI/звук меняется для игрока — `.cursor/rules/jazz-docs-sync.mdc` (technical + wiki + showcase RU/EN).

- Точечная цветокоррекция DDS мосинок без смены UV: `docs/tools/_repair_mosin_visuals.py` (hash-pinned baseline, preview перед `--apply`, сохраняет mip-цепочку и нейтральные BC1-блоки).
- Повторная коррекция светлоты M38/Obrez: `docs/tools/_match_mosin_wood.py` — маска дерева из RM, учёт linear/sRGB и диффузной доли старого материала; использовать прежний output с backup для идемпотентного запуска. Это offline приближение, точное совпадение требует осмотра в кабинете.
- Тон АК-74М/АК-105: `docs/tools/_tune_ak_polymer_materials.py` (staging перед `--apply`, backup, все mip/fallback; metallic сохранён). При повторном запуске сохранять прежний `--output`, чтобы не накапливать коррекцию.

- Послойные иконки всего арсенала: offline-прототип и будущая съёмка реальных сборок — `docs/design/weapon-layer-icons/README.md`, tooling `docs/tools/weapon_layer_icons/`. Не активировать через metadata; реальный M4 20-round использует прямой `WeaponAttA_MagazineCAR15_02`, а не Magazine20 из старой сцены.

- SquadBag performance (JAZZ-INV-006): `python docs/tools/test_squad_bag_performance.py` — offline Lua regression через lupa; merge, cache invalidation, respawn coalescing/retry. Не заменяет проверку drag/drop и задержек в игре.
