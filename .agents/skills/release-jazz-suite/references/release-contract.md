# Релизный контракт JAZZ

## Репозитории

| Пакет | Локальный каталог | GitHub | Mod ID |
|---|---|---|---|
| Core | `jazz` | `Kpoji4er/JAZZ` | `e6L4ECj` |
| Assets | `jazz_assets` | `Kpoji4er/JAZZ-assets` | `pDGDhr` |
| Maps | `jazz-maps` | `Kpoji4er/JAZZ-maps` | `FhNNYd` |
| Units | `jazz-units` | `Kpoji4er/JAZZ-units` | `Dv3mFVN` |

Репозитории публичные. В каждом допустим только remote `origin`. Владелец — `Kpoji4er`; collaborators — `FruBayun` и `Doctorleevsy`. Это не требует переписывать Git authors или read-only поле `author` ModDef.

## Центральная версия и публикация

Core `metadata.lua` в tagged commit является единственным источником release version.

- release title использует engine display `MAJOR.MINOR-REVISION`;
- GitHub tag использует `vMAJOR.MINOR.REVISION`;
- workflow не принимает независимый номер версии, а только проверяет ожидаемый tag;
- package versions assets/maps/units фиксируются отдельно в manifest.

Создавать один GitHub Release в `Kpoji4er/JAZZ`. Для tag `v0.11.5899` он содержит:

- `JAZZ-v0.11.5899.zip`;
- `JAZZ-assets-v0.11.5899.zip`;
- `JAZZ-maps-v0.11.5899.zip`;
- `JAZZ-units-v0.11.5899.zip`;
- `jazz-release-v0.11.5899.json`;
- `SHA256SUMS`.

## Manifest

Хранить manifest в core-репозитории по пути `release/manifests/vMAJOR.MINOR.REVISION.json` до создания tag. Минимальная схема:

```json
{
  "schema": 1,
  "release_version": {
    "display": "0.11-5899",
    "tag": "v0.11.5899",
    "source": "Kpoji4er/JAZZ@40-character-sha:metadata.lua",
    "version_major": 0,
    "version_minor": 11,
    "revision": 5899
  },
  "game": {
    "lua_revision": 233360,
    "saved_with_revision": 366685
  },
  "commonlib": {
    "version": "1.11",
    "build": 1056,
    "commit": "40-character-sha"
  },
  "packages": [
    {
      "name": "JAZZ",
      "repository": "Kpoji4er/JAZZ",
      "mod_id": "e6L4ECj",
      "commit": "40-character-sha",
      "metadata_display": "0.11-5899",
      "artifact": "JAZZ-v0.11.5899.zip",
      "sha256": "64-character-sha256"
    }
  ]
}
```

В итоговом manifest должны присутствовать все четыре package records с собственными metadata fields. Manifest в tagged commit и приложенный release asset должны совпадать побайтно.

## Источник артефактов

Собирать каждый пакет из чистого checkout точного SHA из manifest. Никогда не копировать активный working tree и не читать release version из него.

Поддерживать явный packaging allow/exclude contract. Точно не включать:

- `.git`, `.github`, `.agents`, `AGENTS.md`;
- локальные editor/export/temp-файлы;
- исходники графики, явно помеченные development-only.

**Steam Workshop upload** (Mod Editor pack) читает `ModDef.ignore_files` в `metadata.lua` пакета и фильтрует через `MatchWildcard` (`GedModEditor.CreatePackageForUpload`). GitHub release archives собираются отдельно из clean checkout и своим exclude-list; для Steam канон — `ignore_files`. Локальный мусор (`.bak`, `__pycache__`, `_review`, `.tmp`, …) держать и в `.gitignore`, и в `ignore_files`. Каталоги вроде `docs/`, `.agents/`, `.github/`, `.cursor/`, `scripts/` в git остаются, но в Steam pack не входят.

Для LFS загрузить objects, проверить отсутствие pointer-файлов в runtime archive и сверить SHA-256.

`Images/GrandChienMap.psd` в maps является development source и должен быть перенесён в Git LFS до миграции GitHub, но не должен попадать в runtime archive.

## GitHub Actions

Центральный workflow должен:

1. Запускаться по metadata-derived tag `v*`.
2. Иметь минимальные права `contents: write`.
3. Прочитать core metadata из tagged commit.
4. Вывести engine display и нормализованный tag из трёх metadata fields.
5. Остановиться, если вычисленный tag не совпадает с GitHub ref.
6. Прочитать manifest и проверить совпадение source SHA, tag и metadata fields.
7. Checkout каждого публичного repo по exact SHA, включая LFS.
8. Сформировать deterministic archives, SHA-256 и draft release.
9. Публиковать release только после проверки assets.

Не брать `main` напрямую во время сборки: ветка может измениться между checkout пакетов.

## Предпубликационные блокеры

- версия взята из working tree или передана независимо от metadata;
- core title/description содержит hard-coded номер версии;
- core metadata не получила новый committed revision относительно предыдущего release;
- metadata изменена вручную или без объяснимых связанных изменений;
- dirty/untracked working tree используется как источник;
- выбранный SHA отсутствует в `origin/main`;
- tag или release уже существует;
- CommonLib main не проверен заново;
- runtime-тест или обязательный smoke-test провален;
- archive содержит LFS pointer или development-only source;
- checksums/manifest не совпадают.

## Восстановление после ошибки

Если draft ошибочен, исправить его до публикации. Если release уже опубликован, не заменять содержимое: сохранить metadata через Mod Editor для нового revision и выпустить новый tag. Tag не форсировать.
