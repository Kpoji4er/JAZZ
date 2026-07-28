---
name: create-jazz-merc
description: >-
  Собрать полностью готового наёмника JAZZ из generation-статьи
  docs/design/mercs-ja12/<slug>.md: UnitData, именной перк, loot, портреты,
  AIM-чат, VoiceResponse, RU/EN локализация. Использовать при команде
  «сгенерируй мерка», create-jazz-merc, или когда статья executable и нужна
  реализация. Не использовать для design-only правок статей без генерации.
---

# Создание мерка из generation-статьи

Пакеты: `jazz-units` (UnitData, loot, portraits, VR), `jazz` (именной perk CharacterEffect, shared loc CSV).

Эталон готовых статей: `docs/design/mercs-ja12/lynx.md`, `tosca.md`, `spider.md`, `spouke.md`.  
Контракт: [references/article-contract.md](references/article-contract.md), checklist: [references/unitdata-checklist.md](references/unitdata-checklist.md).  
Шаблон: `docs/design/mercs-ja12/_template.md`. Фразы: `docs/design/mercs-ja12/_phrase-checklist.md`.

## Вход

1. Путь к статье или slug (`colby` → `docs/design/mercs-ja12/colby.md`).
2. Явное подтверждение генерации (не invent из пустой статьи).

## Preflight

```text
- [ ] 1. Прочитать статью целиком
- [ ] 2. frontmatter.executable == true и Open blockers = none
- [ ] 3. Validate секции по article-contract + phrase-checklist
- [ ] 4. unit_id / portrait_id свободны (нет конфликта в jazz-units)
- [ ] 5. Если нет approved spec на волну/мерка — $specify-jazz-change и DoR
```

Стоп, если `needs-design`, пустые статы/перк/инвентарь/AIM chat, или в Portrait prompt есть оружие в руках.

## Оркестрация

```text
- [ ] A. Именной perk → jazz/CharacterEffect + items/metadata ($sync-jazz-generated-data)
- [ ] B. Loot defs Loot_JAZZ_* + tier presets → jazz-units
- [ ] C. UnitData companion + ModItemUnitDataCompositeDef + VoiceResponse block
- [ ] D. $create-jazz-merc-portraits (CHARACTER_DESCRIPTION, no-weapons + class kit)
- [ ] E. Wiring Portrait/BigPortrait в UnitData/items
- [ ] F. $manage-jazz-localization — Russian.csv + English.csv (needs=0)
- [ ] G. Static audit по unitdata-checklist
- [ ] H. Evidence / DoD в spec волны
```

Портреты: skill `$create-jazz-merc-portraits` + [style-and-naming.md](../create-jazz-merc-portraits/references/style-and-naming.md). Промпт из статьи; запрет стволов в кадре; класс-кит обязателен. Если в статье есть ``*.ja2-face.*`` — лицо в Portrait/BigPortrait должно быть похоже на этот JA2-референс (`reference_image_paths` + явный Match JA2 face в CHARACTER_DESCRIPTION).

## Запреты

- Не генерировать из неполной / non-executable статьи.
- Не пушить, не force-push, не релизить без отдельного одобрения.
- Не смешивать с mass format / несвязанным Lua.
- Не класть портреты мерков вне `jazz-units/MercPortraits`.
- Не активировать dormant код неявно.

## После успеха

- Обновить `status: ready` в статье и указать пути UnitData/loot/perk/portraits.
- Индекс `docs/design/mercs-ja12/README.md` — перенести slug в Ready.
- Technical note при изменении публичных ID/load: `$document-jazz-systems`.
