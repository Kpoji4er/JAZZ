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
- Портреты мерков/NPC (PNG 300×300 + 2000×2000, стиль JA3) — пакет `jazz-units`, каталоги `MercPortraits/` и `NPCPortraits/`; генерация по `$create-jazz-merc-portraits`. `Images/` только для логотипа мода.

## После правки

- Технически зафиксировать изменённые поверхности (resource IDs, entity IDs, load-порядок).
- Если UI/звук меняется для игрока — добавлять заметки в docs при последующей сборке wiki.
