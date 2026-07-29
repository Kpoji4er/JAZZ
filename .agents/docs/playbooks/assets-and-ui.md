# Assets, UI и эффекты

## Перед правкой

1. `.agents/docs/reference/project-scope.md`
2. `.agents/docs/reference/runtime-model.md`
3. Для Entity/ресурсов проверить межпакетные ссылки в metadata.

## Рекомендации

- Изменения в entity/ресурсах не должны отрывать контракты с юнитами и карты.
- `jazz` использует `jazz_assets`; любая новая ссылка `Mod/<id>/...` требует metadata-задекларированной зависимости.
- При работе с FX/UI избегать скрытых глобальных side effects, которые не очищаются при `reload`.
- Новые сателлитные role icons (`SquadsIcons/Enemy/<faction>_<ROLE>_squad.png`) — по skill `$create-jazz-squad-icons`; каталог: `docs/technical/systems/squad-role-icons.md`.
- Status effect icons (`Icons/StatusEffects/*.png`, 40×40) — skill `$create-jazz-status-icons`; style/prompts — `Icons/StatusEffects/references/PROMPT.md`.
- Attachment icons — **два разных skill**:
  - `$create-jazz-component-icons` → полная `WeaponComponent.Icon` (`Icons/Upgrades/Full/`, кабинет моддинга)
  - `$create-jazz-chip-icons` → `ChipIcon` миниатюра (`Icons/Upgrades/Chips/`, inventory/HUD chips)
- Иконки именных и сигнатурных перков (`Perks/Personal/*.png`, `Perks/SignatureAbilities/*.png`, 68×68 RGBA) — skill `$create-jazz-perk-icons`; фон обязательно прозрачный, символ выводить из Description/Mechanics.
- Портреты мерков/NPC (PNG 300×300 + 2000×2000, стиль JA3) — пакет `jazz-units`, каталоги `MercPortraits/` и `NPCPortraits/`; генерация по `$create-jazz-merc-portraits`. `Images/` только для логотипа мода.

## После правки

- Технически зафиксировать изменённые поверхности (resource IDs, entity IDs, load-порядок).
- Если UI/звук меняется для игрока — добавлять заметки в docs при последующей сборке wiki.
