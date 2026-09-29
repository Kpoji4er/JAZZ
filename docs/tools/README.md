# `docs/tools` — скрипты агентов и аудита

## Повторная оружейная приёмка 28.09.2026

- `_weapon_feedback_islands.py`: Blender, read-only связанные поверхности и bounds (`--blend --entity --output`).
- `_weapon_feedback_parts.py`: Blender `--mode m14|grip --blend --islands --output --game-root`; отделяет 742 грани планки либо исправляет UV деревянной оболочки (`--base` decoded albedo). Исходники не перезаписывает.
- `_weapon_feedback_compile.py --only <entity>` повторяет compile/audit одного изменённого кандидата; сохраняет остальные завершённые audits.
- `_weapon_feedback_graph.py --game-root --output [--items --assets --setter]`: полный граф компонентов, реальный setter и vanilla UpdateVisualObj; AR15 normal/short, установка/снятие планки M14/M21.
- `_weapon_feedback_preview_test.py --game-root --module`: воспроизводит исходный UI blocked для отсутствующего Side2, проверяет исправленный helper и сохранённую блокировку занятого слота.
- `_weapon_feedback_icons.py`: JSON поддерживает blend/entity или точную vanilla Geometry JSON (нейтральный материал), parent/spot и поворот; `_weapon_feedback_views.py --blend --target X,Y,Z --scale --output` снимает крупные планы собранной сцены.
- `_weapon_feedback_stage028.py --build`: готовит адресную транзакцию, manifest и stage; `--apply` требует закрытой игры и исходных хэшей, сохраняет backup. `_weapon_feedback_validate028.py --build` перед установкой проверяет ModItem/companion, папку оружия, новую entity, compiled audits и цвет/границы иконок.

Порядок: отдельная сборка → compiled audit → stage → render/QA → повторный stage с иконками → validate → apply → sync audit. Backup содержит старые файлы; новый OpticsMount при откате исключается вместе с регистрацией. При повторном экспорте использовать сохранённые кандидаты или повторить этот pipeline. Это offline evidence, не editor round-trip.


## Визуальные замечания к оружию 27.09.2026

`_weapon_feedback_maps.py` декодирует установленные DDS для проверки материалов (BC5 Z восстанавливается); `_weapon_feedback_review.py` сравнивает оба бока с картой/без неё. `_weapon_feedback_mesh.py` разделяет жёсткие стыки без custom normals, проверяет сохранность поверхности/UV; `--compiled-prior` удаляет только измеренные микрограни, схлопнувшиеся в HGM. `_weapon_feedback_compile.py` выполняет официальный compile и geometry/winding audit. Пути игры и сборок передаются аргументами.

`_weapon_feedback_materials.py` готовит отдельные PBR-кандидаты (родной atlas АК-103, normal strength, маски дерева M14/металла R4); `_weapon_feedback_components.py` готовит сошки M14 и исполняет штатный `UpdateVisualObj` в Lua-harness для normal/short/long M4. `_weapon_feedback_bipod.py` проверяет посадку ванильных АК-сошек по декодированной геометрии.

`_weapon_feedback_icons.py --config <JSON> --assets <jazz_assets> --maps <decoded maps> --output <dir>` собирает детали из blend по установленным `.ent` spots и снимает 324×165 иконки. `_weapon_feedback_install.py --build <dir>` формирует manifest/stage; `--apply` проверяет закрытую игру, исходные хэши и сохраняет backup. Возврат — восстановить файлы из `install-backup` при закрытой игре. Исходные Blender/TGA не перезаписываются: будущий экспорт требует повторного применения кандидатов. Контекст и игровая приёмка: `docs/design/weapon-visual-feedback-20260927.md`.

- `_tune_ak_polymer_materials.py`: коррекция тона и шероховатости установленных АК-74М/АК-105, 24 Base/RM DDS с fallback и всеми mip. По умолчанию staging/backup/report в `tmp/ak-material/tune-v1`; `--apply` устанавливает, повторный запуск с тем же `--output` не накапливает коррекцию. Не меняет исходные Blender/TGA.

Рабочие утилиты для generated data, аттачей, CSV и design-артефактов.

`_diagnose_ak103_shading.py` — Blender: `--blend <rig.blend> --out <review>`; одинаковый свет и оба бока корпуса/приклада, исходная normal map, отключённая и инверсия X/Y. Корпус показан крупным планом; это не обзор всего оружия. Записывает bindings.json, не меняет исходник или игру.

`_rebake_ak103_tangent_basis.py` — Blender: `--native <native build> --out <новая сборка> --game-root <JA3_ROOT>`. Требует подтверждённый `--cover-prefix ksk` при native-импорте. Перепекает исходный шейдинг на подготовленный экспортный меш, сохраняя его геометрию, UV и пересчитанные нормали по хешам. Custom normals исходника доступны только для чтения при bake и не попадают в FBX. Выход — TGA, blend, FBX и отчёт; установка и runtime-приёмка отдельные.

`_fit_ak103_donor_cover.py` — Blender: `--donor <AK74M_JAZZ.blend> --out <отдельная сборка> --source-build <AK103 build> --game-root <JA3_ROOT> --render`; `--inspect` только описывает острова донора. Переносит крышку с родными UV/PBR, подгоняет передний край и цвет, сохраняет прочую геометрию/UV; отчёт, FBX и пары рендеров. Приёмка/установка: `docs/specs/active/JAZZ-WEAPON-AK103-001.md`.

`_restore_ak103_materials.py` — Blender: `--source-build <native> --out <отдельная сборка> --components <all-parts-audit.json> --game-root <JA3_ROOT> --render`. Восстанавливает материал крышки на отдельном участке атласа из однотонной родной краски, ограничивает чрезмерный блеск; сохраняет геометрию/нормали и проверяет их хеши. Выход: rig/FBX, TGA, отчёт и одинаково освещённые пары before/after; процедура и пределы приёмки — `docs/specs/active/JAZZ-WEAPON-AK103-001.md`.

`_import_ak103_native_maps.py` — Blender: `--archive <AK-103 (6П45).zip> --reference <предыдущий rig.blend> --build <отдельный каталог> --game-root <JA3_ROOT>`. Родные UV/PBR, прежние pivots/spots, безопасный corner budget и один материал-атлас на entity; clean/rigged сцены, FBX, PNG, JSON. `_check_ak103_native_stage.py --build <каталог>` проверяет staged entity/mesh/material/DDS/fallback, прежние spots и размеры иконок; DXGI DDS проверяются по заголовку, не выдаются за декодированный PNG. Установка — существующий `_integrate_ak103.py --replace-assets --apply` при закрытой игре, после сравнения HGM всех шести entity.

`_import_jaweapons_batch.py --audit <materials.json> --out <build> --blender <exe>` + Blender-worker `_import_jaweapons_scene.py` — изолированный импорт всех неотклонённых источников, SHA256, материалы, UV/mesh-аудит, clean blend и PNG. `--only N`, `--reimport`, `--summarize-only --report <stem>`; worker `--uv-review` показывает no-UV меши красным. Не устанавливает игровые предметы и не запускает JA3; неоднозначные карты сохраняет в material library без случайного назначения. `docs/design/weapons-import-batch-results.md` — текущие результаты.

`_audit_jaweapons_materials.py --list <weaponslist.txt> --out <report stem>` — весь список ZIP/RAR/GLB, вложенные ZIP, декодирование текстур, OBJ UV/MTL references и встроенные GLB-материалы. Пишет Markdown + JSON, отличает REJECT без материалов от текстур с невосстановленными назначениями; RAR читает через 7-Zip, JA3 не запускает.

`_prepare_hatchet_source.py` — Blender background: `--archive <Just A Hatchet.zip> --out <новый build-каталог>` после `--`. Сохраняет копию OBJ, clean/Hatchet.blend, SHA256/UV/mesh-аудит и три PNG; проверяет повторное открытие и неизменность архива. Без запуска JA3; текстуры отсутствуют, масштаб исходный, игровой импорт не выполнен.

`_apply_weapon_rollout.py --build <build> [--apply]` — WEAPON-ROLLOUT-001: согласованные статы/цены, адресный CSV, Ivan10 и только новые AK74M/AK105/SR3M/L42A1 записи в существующих пулах Легиона. Dry-run по умолчанию; SHA-backup, защита от конкурентной записи, проверка Lua и идемпотентность. Полную перегенерацию Легиона не запускает.

В том же rollout восстанавливается отдельно одобренная выдача ножа Crusher 40/55/70. `_audit_weapon_rollout.py --build <build>` сравнивает все прежние LootDef с резервной копией и проверяет сохранность старых записей пулов. `_runtime_weapon_rollout.py` — guarded DAP reload только items jazz/units и Lua, без перезагрузки карты/assets, без сохранения; останавливается при несохранённых editor edits, пишет AppData-report.

`_check_mosin_configurations.py --build <Mosin build> --game-root <JA3_ROOT>` дополнительно проверяет запрет ПУ на М38/обрезе: реальные штатные UI checks, JAZZ setter и возврат доступности Scope на длинном стволе. Оптические модификаторы в этой изолированной проверке заменены нейтральным тестовым прицелом; настоящие AP/visual проверяет `_runtime_weapon_imports.lua`.
`_restore_mosin_barrels.py [--apply]` возвращает три `ModItemWeaponComponent` (1891 / M38 / Obrez) перед `JAZZ_BarrelsDefs`, если слот Barrel их ещё перечисляет, а сами записи пропали из грязного `items.lua`. Dry-run по умолчанию; `--apply` при закрытой игре/редакторе.
Политика хранения: `.agents/docs/reference/agent-tooling.md`, `.cursor/rules/jazz-agent-tooling.mdc`.

Запуск из корня пакета `jazz/` (если не указано иное).

Кираса Легиона (`JAZZ-APPEAR-001`): `_build_legion_armor.py` — Blender bake + FBX и нативная render-иконка; вход `--source <v2.blend> --output <build> --game-root <JA3_ROOT>`. FBX обрабатывается AssetsProcessor, staging ресурсов — `_prepare_rifle_assets.py` (prefix `JAZZ_ImprovisedCuirass`, entity `JAZZ_ImprovisedCuirass_Male`). `_install_legion_armor.py --build <build>` — одноразовая установка согласованных ModItem/metadata/companion и тестового юнита с backup при закрытой игре/редакторе. `_check_legion_armor.py` — read-only executable Lua lifecycle mocks, gear и узкий resource-graph audit; не заменяет игровой прогон. `_install_vanilla_armor_visuals.py` — идемпотентные 19 тестовых UnitData для ванильных Flak/IBA и mapped шлемов (companion + items/metadata); dry-run по умолчанию, `--apply` при закрытой игре/редакторе. Runtime-карту `System_LegionArmorVisuals.lua` не переписывает. `_fix_eod_armor_name.py` — отделяет `JazzArmor_EOD` от клонированных ID/текстов Flak M69 (новые 890000000014200–203, RU/EN). `_repair_legion_armor_record.py` — идемпотентное исправление первоначальной записи тестового юнита в property/value array (`StoreAsTable=false`) и `Group`; открытый редактор после этого должен перечитать мод с диска.

СР-3М (`JAZZ-WEAPON-SR3M-001`): `_build_sr3m_assets.py` запускается через Blender `--background --factory-startup --python ... -- --source <SR_3M.blend> --output <build> --game-root <JA3_ROOT> --export`; сохраняет исходник, пересобирает модули, TGA, FBX и два preview. FBX обрабатывается установленным `ModTools/AssetsProcessor/AssetsProcessor.exe`.
`_integrate_sr3m.py --export-root <ExportedEntities> --build <build> --game-root <JA3_ROOT>` устанавливает только SR3M entities, DDS/fallbacks, иконку, предмет и пять visual bindings; требует закрытого редактора, сохраняет backup core-файлов. `_localize_sr3m.py --game-csv <Game.csv> --build <build>` добавляет translation memory и вызывает канонический RU/EN экспорт во staging для review.
`python docs/tools/_check_sr3m.py` — read-only Lua compile и сравнение ModItem/companion, проверка ресурсов, spots, DDS/fallbacks и переводов. Не заменяет проверку в JA3. Расширен под REQ-004/005: шесть слотов, spots `Scope` и `Side` с проверкой координат и поворота, запрет dovetail-оптики, `Muzzle` модифицируем и ровно с одним компонентом — последнее падает, когда появится глушитель 9А-91, и напоминает обновить spec.
`_build_sr3m_assets.py --top-rail` добавляет низкополигональную Picatinny на гребни крышки ресивера (20 пазов, +252 треугольника) и spots `Scope` на планке и `Side` на боковой площадке цевья; сохраняет `clean/SR3M.blend` и `rigged/SR3M_JA3.blend`, не затирая прежние продукты сборки. Без флага поведение старое. Нормали приводятся `recalc_face_normals` и охраняются утверждением о положительном знаковом объёме: ручная обмотка граней один раз уже уехала внутрь, и в Blender-превью это не читалось, а движок показал сразу; проверка «нормаль наружу от общего центра» для набора отдельных зубьев даёт ложные срабатывания и не годится. `--rail-uv project` (по умолчанию) берёт UV по ближайшей точке крышки, чтобы планка наследовала настоящие normal/roughness/AO и совпадала с крышкой по материалу; побочно подхватывает нарисованные рёбра крышки светлыми полосами. `--rail-uv flat` возвращает один тексель: планка чистая, но светлее и площе крышки.
`_build_sr3m_attachment_fit_scene.py --rigged <rigged blend> --report <build-report.json> --reference <_vanilla_reference> --assets <jazz_assets> --out <attach_renders>` — offline проверка посадки: реальная декодированная HGM-геометрия там, где она есть, и подписанный wireframe-бокс из `.ent` там, где её нет, без выдуманных мешей. Считает свес, прикус зажима и высоту над планкой в `fit-report.json`. Подмеши привязываются к собственному объявленному bbox: добавление центра bbox напрямую разбрасывает skinned-детали и даёт «усы» (эта же ошибка осталась в `_build_ak_attachment_fit_scene.py`).
`_apply_sr3m_slots.py --backup <dir> [--apply]` — одна транзакция на `items.lua` и companion: слоты `Scope` и `Side` с `CanBeEmpty`, разблокировка `Muzzle`. Ни одного `WeaponComponentVisual ApplyTo="SR3M"` не пишет — компоненты уже несут дефолтный визуал на нужный spot, как на M4A1. Dry-run по умолчанию.
`_apply_weapon_geometry_update.py --export-root <ExportedEntities> --backup <dir> --entity <name> [--apply]` — установка только меша и `.ent`, когда пересборка изменила лишь вершины и spots. Материалы, `.mtl` и DDS не трогаются, поэтому свежие числовые имена текстур в мод не попадают и `$rename-jazz-weapon-textures` не нужен. Чинит две вещи, которые AssetsProcessor оставляет и которые нельзя коммитить: пустой атрибут `name` и абсолютный `<src>` на локальный FBX. Сверяет число материальных слотов. Dry-run по умолчанию.
`_measure_ak_grip.py --build <label>=<JAZZ blend> --out <dir>` — замер пистолетной рукояти относительно origin (правая рука) и close-up. Эталон — принятый AK74, центр рукояти около +0.4/−2.2 см.
`_reanchor_ak_grip.py --blend <JAZZ blend> --entity AKR_<ID> --offset-game-cm dx,dy,dz --out <blend> --fbx <fbx> --game-root <JA3_ROOT> --write` — сдвигает только body mesh и spots, чтобы рукоять села на origin. Модули не переписывает. Дальше AssetsProcessor и `_apply_weapon_geometry_update.py` только на корпус.

Импорт оружия из локального архива (очередь `docs/design/weapons-import-plan-jaweapons.md`):
`_inspect_weapon_source.py` — read-only разбор папки исходников или готового `.blend` через Blender (`--source <dir>` либо `--blend <file>`, `--out <dir>`); печатает состав объектов, UV, материалы, текстуры, world bbox и рендерит три ортопроекции Workbench. `--shading TEXTURE` показывает base color, `--show-hidden` включает `hide_render` варианты (сложенный приклад), `--highlight <regex>` рендерит по кадру на деталь с подсветкой — так опознаются безымянные `Cube6_low`. Нужен до любого решения «архив пригоден».
`_build_weapon_scale_overlay.py --new <clean.blend> --name <ID> --ref <AK*_JAZZ.blend> --out <dir>` — обязательный гейт масштаба: совмещает новый ствол с принятыми АК по магазину и даёт side/top с подписанными длинами в метрах. Эталоны аппендятся вместе с Origin-empty: если тащить только меши, референс «усыхает» на 5–15%.
`_overlay_weapon_length.py --build <label>=<blend> [--scale <label>=<factor>] [--spots <label>=<report>] --entity <label>=<entity> --assets <jazz_assets> --out <dir>` + `_annotate_scale_overlay.py --out <dir> --reference <label>` — тот же гейт для случая «сравнить несколько кандидатов длины сразу». Строит N рядов в одном метрическом кадре, ставит метровую линейку с левым краем, привязанным к нулю, выравнивает по дулу и по `Hand_l_grip`, а `--scale` даёт примерить множитель без пересборки. Точки берёт из установленного `.ent` или, для ещё не установленной сборки, из build-отчёта. Требует `sensor_fit='HORIZONTAL'`: при высоком кадре Blender иначе применяет `ortho_scale` к высоте и режет стволы. **Пересекается с `_build_weapon_scale_overlay.py`** — два инструмента на одну задачу, консолидация не согласована.
`_render_weapon_icons.py --icon <label>=<blend> --out <dir>` + `_finalize_weapon_icons.py --out <dir> --reference AK74` — иконки инвентаря в формате рукодельных: 324×165 RGBA, дуло вправо, композиция `DilateErode` по альфе → почти чёрный слой → `AlphaOver` под картинку плюс размытый ореол. Рендер в 2× и LANCZOS вниз, иначе кольцо пикселит; `--ring 7 --halo 12` дают около 3 и 6 px на финале. Запас по краю кадра обязателен, иначе ореол срезается в плоскую линию. Finalize печатает профиль обводки по глубине и собирает листы сравнения на `#2a2a2a`; для чёрных корпусов цифры глубже 3 px завышены краской модели. **Пересекается с `_compose_icon_review.py`** в части листов сравнения. `_render_ak_icons.py` остаётся для 512×256 с `distance=2` и для иконок магазинов.
Нормали меша: `_ja3_mesh_prepare.prepare_export_mesh` — триангуляция без custom/split, всегда recalc. Успешный AssetsProcessor не ловит кривой weld. `python docs/tools/_check_mesh_export_normals.py` падает, если какой-то `docs/tools/*.py` снова ставит keep-custom; `--scan-dir` проверяет OBJ / HGM JSON; `--summary` — счётчики. Открытый `.blend`: `blender --background --factory-startup <file.blend> --python docs/tools/_audit_blender_normals.py`. Прогон `prepare_export_mesh` без записи: `_prepare_blender_normals_dryrun.py`. Playbook: `.agents/docs/playbooks/mesh-export-normals.md`.
AK-103 (`JAZZ-WEAPON-AK103-001`): `_build_ak103_assets.py --blend <frostoise/ak103 clean.blend> --build <build> --render` — clean-сцена из CC-BY «AK 103» (Frostoise), ориентация −Y/Z, масштаб по паспортным 943 мм, модули по материалам и loose-island (магазин/цевьё/приклад/дуло), опорные empties `LM_*`. `_export_ak103_assets.py --build <build> --game-root <JA3_ROOT>` — rigged: кадр привязан к `AKM.ent` по губкам магазина, оптика на собственной планке, подствол по смещениям АКМ от дула; Origin-empty, `prepare_export_mesh` (recalc, без custom normals), атласы Base/Normal/RM 2048 TGA и FBX. Повторная установка геометрии: `_integrate_ak103.py --replace-assets`.

`_audit_weapon_balance_runtime.py` — read-only аудит оружия: исполняет выбранные текущие Lua-методы через `lupa`, сверяет числовые поля CSV с companions, печатает воспроизведение shotgun/armor и изолированные recoil/range-пробы. Без записи данных; требуется `lupa`; не заменяет JA3 runtime. Отчёт: `docs/design/weapon-balance-audit-2026-09-15.md`.

DAP / live Lua в игре: `scripts/dap/` (не этот каталог). Playbook: `.agents/docs/playbooks/dap-runtime-debug.md`.

`_extract_save_lua_frames.py SAVE --out DIRECTORY` — read-only извлечение Zstandard-фреймов сохранения для диагностики; не исполняет Lua и не изменяет исходный сейв. Требует `zstandard`.

`_check_villa_effect_dispatch.py` — Lua-harness трёх ExecuteCode-вызовов осады K4 через установленный vanilla dispatch/CompileFunc; проверяет SaveAsText и доступ к maps env. Требует `lupa` и `.ja3-root.local`; не заменяет проверку в игре.

`_check_hud_condition_context.py` — Lua-harness контекста HUD: процент через GetConditionPercent(), исходный предмет не изменяется. Требует `lupa`.

`_check_emplacement_target_distance.py` — Lua-harness штатного MachineGunEmplacement.Update с JAZZ wrapper: authored дальность, Clamp, повторное создание оружия и ammo remap. Требует `lupa` и `.ja3-root.local`.

| `_check_lua_wrap_cycles.py` | Два wrap на один `Class:Method` / глобал в suite `Code/` → FAIL (cycle / stack overflow). Allowlist только install-once цепочек. `python docs/tools/_check_lua_wrap_cycles.py`. Правило: `.cursor/rules/jazz-lua-wrap-no-cycle.mdc`. |
| `_audit_ja3_log_errors.py` | Сводка `[LUA ERROR]` / `[UI WARNING]` / missing assets из последнего `logs/JA3.exe-*.log`. `python docs/tools/_audit_ja3_log_errors.py [path]`. |
| `_audit_xtemplate_idcontainer.py` | Все `'Id', "idContainer"` в `items.lua` с XTemplate id (поиск nested collision). |
| `_fix_xtemplate_idcontainer_and_canholdplate.py` | Boolean `CanHoldPlate`/`BlockFaceSlot` больше не BindTo PercentValue. **Не** снимает `idContainer` с mode-окон live `SquadsAndMercs` (это ломает инвентарь). |
| `_check_inv005_meds_salvage.py` | INV-005: `Jazz_FieldMedicineSalvageMeds` даёт 1 Meds с бинта/морфина; аптечки не в таблице; wrap + UI patch на месте. |
| `_test_combat_009_ow_cone.py` | COMBAT-009 AC-001: якоря угла OW (Glock/MP5/AK/M1897/Mosin/ПКМ квадрат на d_min, MinRange 50% BDR). `python docs/tools/_test_combat_009_ow_cone.py`. |
| `_gen_vanilla_beast_ai.py` | Вырезает ванильный `CombatAI.lua` в `Code/System_AI_VanillaBeasts.lua` (`JazzAI_Vanilla*`). Вход: JA3 `ModTools/Src/Lua/Tactical/CombatAI.lua`. Перезапускать после смены диапазонов в скрипте. |
| `_audit_specs_index.py` | Сводка всех `docs/specs/**`: status, Evidence PASS/FAIL/BLOCKED, TBD, cross-refs, folder mismatch. |
| `_aibark_bank_data.py` | Канон боевых окриков AI: 5 (RU, EN) на слот. `python docs/tools/_aibark_bank_data.py` собирает таблицы в `docs/design/combat-ai-barks.md` после `<!-- aibark-bank -->`. |
| `_strip_jazz_legion_spiritual.py` | Снять `Spiritual` со `StartingPerks` всех `JAZZ_Legion_*` (companion `UnitData/` + `jazz-units/items.lua`). Ребелы/наёмники/бандиты не трогает. |
| `_check_aibark_bank.py` | 5 QA-pass лексики банка окриков: поле/калька/корни/тир-рот/вслух + длина + ctx-теги. `python docs/tools/_check_aibark_bank.py`. |
| `_emit_aibark_runtime.py` | Банк → Lua-таблица в `Code/System_AI_CombatBarks.lua` + строки `890000000020157–20596` в `Russian.csv` / `English.csv` / `Localization/Strings.csv` и manuals. Идемпотентно. |
| `_audit_ai_mobile_shot.py` | Count `AIActionMobileShot` in `jazz-units/items.lua`: `action_id` / BiasId / RequiredKeywords + jazz action mentions. |
| `_audit_ai_rng_wiring.py` | Brace-aware RunAndGun wiring audit: real vs default MobileShot, keyword gates, `AIAttackSingleTarget` action_ids. |
| `_apply_ai_packet1b_items.py` | Packet 1B: sync `jazz-units/items.lua` UnitData PickCustom/archetype to companions; wire POL-002 AllyRoleAnchor+AvoidPeekVoxel into Front/Assault Legion+Rebels OptLoc; leave live TakeCover weights. |
| `_apply_units009_melee_unitstat.py` | UNITS-009: `UnitStat=Strength` on seven melee companions + `items.lua` (machete family, bayonet, shovel, unarmed). Knives stay Dexterity. |
| `_apply_units009_loc.py` | UNITS-009: append RU/EN `890000000010900` / `010901` practice rollover to runtime CSV, catalog, manuals. |
| `_append_units009_units_loc.py` | UNITS-009: same practice IDs into `jazz-units` runtime `Russian.csv` / `English.csv` (package loctables). |
| `_test_units009_skill_xp.py` | UNITS-009 static AC-001..004/016: T(s), cumulatives, Wisdom mul, no InteractionRand on award, melee UnitStat, helpers. |
| `_audit_ai_packet1b.py` | Static 1B: live OptLoc TakeCover (Front 20+40 / Assault 10 / Flank 15), POL-002 on four archetypes, Flanker UnitData IDs, no panic/Hide/Melee@10 in JAZZ_Legion_/Rebel* PickCustom; ROLE-001 weak Flanker AI 80/150 on Assault/Front (true Flanker 500/1000). |
| `_apply_ai_role001_weak_flank.py` | ROLE-001 REQ-005: Assaulter/Frontliner Legion+Rebels Flanker AI branches → Weight 80 / Flanking 150; Assaulter `Flanks`→`Flank`. Does not touch Flanker presets. |
| `_apply_bandage_cumulative_loc.py` | MED-001: update `890000000010013` / `010021` RU+EN for cumulative field bandage (1 bandage × bleed stack). |
| `_apply_med005_field_ap_loc.py` | MED-005: RU+EN runtime CSV for bandage/morphine AP ladder (`890000000010013` / `010016` / `010028` / `010201`). |
| `_audit_med005_field_ap.py` | Static MED-005: Medical AP table 5/4/3/2/1 and 3/2/1; `GetAPCost` helper; GetUIState/CombatAI; companion/`items.lua`/CSV parity. |
| `_apply_mobile_action_damage_ui.py` | Fix AimType=mobile `GetActionDamage` (RnG/Carbine/SMGStorm/ManeuverAR/MobileShot) + RnG `GetActionResults` num_shots; uses `Jazz_GetMobileActionDamage` in `Code/CombatActions.lua`. |
| `_normalize_ernie_flare_carriers.py` | Set Ernie island `Min/MaxFlareCarriers` to 12/15 in `jazz-maps/items.lua` (ModItemSector + HotDiamonds SatelliteSector). |
| `_probe_autofire_attacks.py` | List `InventoryItem/*.lua` whose `AvailableAttacks` have jazz autofire aliases (`AbakanAutoFire` / `JAZZ_LargeAutoFire` / …) but not vanilla `AutoFire`/`MGBurstFire` (BulletHell gate audit). |
| `_check_bullethell_autofire_gate.py` | Static: `JazzWrapBulletHellAutofireGate` present; AN94 keeps `AbakanAutoFire` without vanilla `AutoFire`. |
| `_check_bullethell_projectiles.py` | Static COMBAT-006 v2: `FirearmAttack` + hits LoF the cone unit (no `SetTerrainZ(far)`); miss fan at chest height; cone-wide Will. |
| `_bump_bullethell_hit_lof_meta.py` | COMBAT-006 playtest: revision +1 and prepend `last_changes` (escape `\n` only). |
| `_fix_zastava_m92_csv.py` | WEAPONS-003 hotfix: `ZastavaM92` `burst_shots=4` `auto_shots=7` `cyclic_rpm=700` in `weapons.csv`. |
| `_scan_saves_broken_placecharacterffect.py` | Scan JA3 `.sav` under Saved Games: extract zstd `game_session`, count `PlaceCharacterEffect('Id', )` (empty props — load-breaking). |
| `_extract_ja3_game_session.py` | Extract concatenated zstd frames of `game_session` from BPUL `.sav` to `.lua` for syntax debug. |
| `_audit_ame_appearance_clothes_qa.py` | AME appearance clothes QA vs appearance-map (bank/channel checks). |
| `_audit_ame_hat_not_blue.py` | Flag AME hats that violate no-blue accent policy. |
| `_patch_ame_appearance_clothes_from_map.py` | Apply clothes fields from `ame-appearance-map.json` into generated appearance data. |
| `_export_ammo_stats.py` | Parse `InventoryItem/JAZZ_AMMO_*.lua` → `Ammopics/_gen/ammo_stats.json` + `.csv` (pen/dmg/jam/crit/BR). |
| `_audit_ammo_pen_mul_zero.py` | Fail if `JAZZ_AMMO_*` has `PenetrationBonus` `mod_mul=0` (engine zeros `mod_add`). Class-level `mul=0` (saltshot) is allowed. |
| `_gen_ammo_stats_canvas.py` | Rebuild `canvases/ammo-stats.canvas.tsx` from `ammo_stats_compact.json`. |
| `_normalize_ammo_icon_bbox.py` | Crop near-black, fit ammo-box content into fixed `fit_w`×`fit_h` on 110×110 black canvas (series size lock). |
| `_lock_ammo_icon_silhouette.py` | Silhouette lock per caliber. Cut: `--key auto\|magenta\|black\|alpha`, `--choke` after downscale, `--alpha-from draft\|sil`, `--thr`, `--hard-alpha`. Soft edge: `--soft-outline 0.45` / `--outline-only`. Prefer **magenta plate** gens. |
| `_finalize_ammo_gen_batch.py` | Batch: lock Cursor `assets/gen_*.png` → `Ammopics/_gen` + soft outline + `--key` + optional `--purge-assets` (only listed files). |
| `_paint_ammo_carton_family.py` | EXPERIMENT only — paint onto blank plate. Visual QA rejected for 9×18 (looks procedural). Prefer GenerateImage + `_lock_ammo_icon_silhouette.py`. |
| `_list_jazz_helms.py` | List `JazzArmor_*` Head-slot items (id/DisplayName/comment) for JAZZ-APPEAR-001 mapping. |
| `_list_jazz_legion_appearances.py` | List Jazz Legion appearance IDs for portrait tooling. |
| `_scan_ame_hats.py` / `_dump_ame17.py` | Hat scan / AME-17 dump helpers for appearance audits. |
| `_bump_metadata_revision.py` | `metadata.lua` Revision +1 + prepend `last_changes` bullet (`--bullet`, escape `\\n` only). |
| `_diff_list2_sheet.py` (alias `_tmp_diff_list2_sheet.py`) | Diff Google Sheet Лист2 perk cols (fresh TSV export vs prior WebFetch) for JAZZ-UNITS-006. |
| `_apply_units006_batch1_items_loc.py` | UNITS-006 §A batch1: sync `items.lua` ModItem CE from companions + `Jazz_OrderAP`/`Jazz_CombatMedicBuff`, metadata.code, RU/EN CSV for touched perk/status IDs. |
| `_apply_units006_batch1_hooks.py` | UNITS-006 batch1: register `System_NamedPerks_006` in metadata.code; Vince skip-consume wrap in `Systems_Medicine.lua`. |
| `_apply_units006_batch2_items_loc.py` | UNITS-006 §C batch2: sync vanilla personal CE companions (`GruntyPerk_JAZZ`, `GrizzlyPerk`, Ivan/Gus/Nails/Wolf/Magic/Scully/Steroid/Ice), metadata.code, RU/EN CSV (`6500+` + Grizzly/Grunty desc). Refuses VoiceResponse overwrite. |
| `_apply_steroidpunch_passive.py` | UNITS-006 SteroidPunch: sync companion → `items.lua` + RU/EN `890000000009930/9931` (passive knockback text). Restores Gamos VR `6512/6513` if overwritten. |
| `_bump_steroidpunch_passive_aimtype_meta.py` | SteroidPunch Passive: metadata bump for AimType=none (no melee-range rollover). |
| `_bump_steroidpunch_hotfix_meta.py` | Bump jazz Revision + prepend SteroidPunch Passive/knockback/CrossHairUI hotfix bullet in `last_changes` (escape `\n` only). |
| `_bump_bullethell_rok_cache_meta.py` | Bump jazz Revision + prepend Spike BulletHell `recharge_on_kill` cache fix bullet. |
| `_bump_bullethell_cone_will_meta.py` | Bump jazz Revision + prepend Spike BulletHell honest-CTH / cone-wide Will dump bullet. |
| `_bump_killingwind_hotfix_meta.py` | Bump jazz Revision + prepend Fauda KillingWind grit/`OnGearChanged` FM tax fix bullet. |
| `_bump_barry_craft_discount_meta.py` | Bump jazz Revision + prepend Barry DesignerExplosives CraftAmmo/Explosives −30% Parts (sector-wide) bullet. |
| `_fix_passive_sig_icons_54_blue.py` | Rebuild Passive `Jazz_Perk_*` Signature icons to 54×54 cool blue (fix 108 dual SetColumns=1 squash). |
| `_build_passive_signature_icon_54.py` | **Passive** Signature hotbar icon = **54×54** (`SetColumns(1)`), cool **blue** from Hud **LEFT** half (not cream). Active = **108×54** dual (`SetColumns(2)`). → `Perks/SignatureAbilities/<ActionId>.png`. |
| `_build_lynx_sig_icon_glow.py` | Lynx Passive hotbar: 54×54 cool blue from `Perks/Personal/Lynx.png`, keep high-luma glowing eyes (standard 54 recolor would flatten them). |
| `_units006_namedperks_notes.md` | UNITS-006 batch2: shipped effects + soft cuts (Ice deferred, Wolf ops wrap scope). |
| `_gen_units006_batch3.py` | UNITS-006 §C batch3: generate signature CE companions + items/metadata/loc (`9861+`). |
| `_audit_jazz_perk_combat_actions.py` | Audit `Jazz_Perk_*` CE vs `ModItemCombatAction` SignatureAbilities companions; flags missing CA and `GetUIState→hidden` stubs. |
| `_gen_jazz_perk_passive_combat_actions.py` | Generate/fix Passive `SignatureAbilities` CombatAction companions for `Jazz_Perk_*` (skip `00` Toggle + OfficerAuraInfluence); sync metadata presets. Prefer `Perks/SignatureAbilities/<id>.png` for CA Icon when present. |
| `_build_jazz_perk_sig_icons_from_personal.py` | Builds **108×54 dual** from Personal — for **Active** Signature. **Passive** needs 54×54 via `_build_passive_signature_icon_54.py` (`CombatActionBarButton` `SetColumns(1)`). |
| `_fix_thegrim_recharge_cache.py` | Reaper TheGrim: docs/meta bump for `g_PresetParamCache` + wrap-reinstall fix (runtime in System_NamedPerks). |
| `_apply_thegrim_recharge_5kills.py` | UNITS-006 Reaper `TheGrim`: ensure RU/EN loc for 5-kill recharge tooltip; runtime is `Code/System_NamedPerks.lua` (`Jazz_TheGrimKillsToRecharge`). |
| `_fix_units006_batch3_loc.py` | UNITS-006 batch3: rewrite RU CE/CSV via unicode-escapes (encoding-safe). |
| `_gen_units006_batch4.py` | UNITS-006 §B batch4: Flo/Static/Cougar + cheap §B CE text/hooks sync. |
| `_units006_namedperks_notes.md` | UNITS-006 batch4: shipped Flo/Static/Cougar + soft cuts → batch5. |
| `_units006_audit_followup.md` | UNITS-006 post-batch audit: Mike PinDown/Vince/MD heal fixes + remaining gaps. |
| `_gen_units006_batch4.py` | UNITS-006 §B batch4: Flo/Static/Cougar + Grace/Kulba/… CE text+hooks; sync items/metadata/loc (reuse CE IDs). |
| `_units006_namedperks_notes.md` | UNITS-006 batch4: before→after + soft cuts (HARD → batch5). |
| `_gen_units006_batch5.py` | UNITS-006 batch5 HARD/satellite + batch6 §D: Rothman/Miguel/Barry/… CE + Miguel aura statuses + Benny/Simon; items/metadata/loc (`9885+`/`9920+`). |
| `_merge_units006_namedperks.py` | Merge Batch3–6 into `System_NamedPerks_006.lua`; relocate Benny/Simon/Miguel aura ModItems; add ModItemCode. |
| `_build_system_namedperks.py` | Rebuild single `Code/System_NamedPerks.lua` (no BatchN Code files). |
| `_units006_perk_moditem_params.py` | Add ModItem Parameters to UNITS-006 perks; wire Code via Jazz_NamedPerkParam; sync items. |
| `_units006_namedperks_notes.md` | UNITS-006 batch5: before→after + soft cuts (Biff economy, ECON-001 Livewire op, Thor recipes). |
| `_add_doubletoss_pocket_cas.py` | Fidel: insert `DoubleTossAG–DG` (GrenadesInventory) ModItemCombatAction + metadata presets. |
| `_fix_grunty_morale_visibility.py` | Grunty: CombatLog on morale AP proc (chance/roll); clarify personal-BD desc; sync CE/items/CSV/meta. |
| `_fix_grunty_passive_ca.py` | Grunty: Passive CA `GruntyPerk_JAZZ` + HUD icon; strip AdditionalAP double `GainAP`; metadata bump. |
| `_apply_explodingpalm_drq.py` | DrQ: ExplodingPalm unarmed HP-tier statuses + sat debt +30% + WoundInfected block + Passive CA. |
| `_apply_explodingpalm_passive_ca_fix.py` | ExplodingPalm Passive CA: 54×54 icon, HasPerk GetUIState, stub Execute/UIBegin; metadata bump. |
| `_apply_makethembleed_buff_icon.py` | Flay: `Jazz_MakeThemBleedBuff` HUD stacks = visible bleeding enemies (cap 5). |
| `_apply_dangerclose_larry.py` | Larry: DangerClose List2 (explosives ≥8 +40%, blast +2 bleed, stim immune) + loc IDs + items sync. |
| `_apply_gloryhog_pierre.py` | Pierre: GloryHog CE override + `Jazz_PierreRecruit` signature CA (1 recruit/combat) + loc/metadata. |
| `_fix_pierre_recruit_uibegin.py` | Pierre recruit: fix `Jazz_PierreRecruit` UIBegin (Unit choices + default Execute); Charge tooltip loc; metadata bump. |
| `_check_pierre_recruit_targeting.py` | Static: recruit HUD `ShowCombatActionTargetChoice` (talk icon); no `IModeCombatAttack`; UI restore after Interrupt. |
| `_fix_pierre_loc_collision_9942.py` | Restore RecklessAssault `9935/9936`; Pierre combat-log/Charge tooltip → `9942/9943`. |
| `_fix_gloryhog_loc_collision.py` | Restore SteroidPunch 9930/9931 if overwrite; remap Pierre recruit desc/used → 9933/9934. |
| `_apply_recklessassault_smiley.py` | Smiley: RecklessAssault List2 — 4 mobile attacks, SMG/carbine/AR, +15 CTH, no Tiredness; CA+CE+loc. |
| `_apply_recklessassault_recharge_on_kill.py` | Smiley RecklessAssault: `recharge_on_kill=1` like RunAndGun; CE/loc mention kill recharge; metadata bump. |
| `_patch_buildingconfidence_loc.py` / `_patch_explodingpalm_metadata.py` / `_patch_hawkseye_loc.py` / `_patch_nazdarovya_loc.py` | UNITS-006 loc/metadata helpers for MD / DrQ / Scope / Igor. |
| `_bump_metadata_thegrim.py` / `_fix_last_changes_head.py` | Bump jazz Revision + prepend TheGrim / SignatureAbilities bullets in `last_changes`. |
| `_bump_metadata_hotfix004.py` | HOTFIX-004: Revision +1 and prepend stationary-MG last_changes bullet (`\\n` only). |
| `_bump_metadata_hotfix007.py` | HOTFIX-007: Revision +1 + salt Pain / GrizzlyPerk last_changes (`\\n` only). |
| `_bump_metadata_hotfix005.py` | HOTFIX-005: Revision +1 and prepend remountable squad-bag stack last_changes bullet (`\\n` only). |
| `_bump_units_meltdown_meta.py` | Bump jazz-units Revision + Meltdown `[skip discord]` last_changes bullet. |
| `_units006_namedperks_notes.md` | UNITS-006 §D: Benny/Simon CE + StartingPerks; CombatAction soft-cut. |
| `_units006_batch6_startingperks.py` | Prepend `Jazz_Perk_Benny`/`Jazz_Perk_Simon` to jazz-units UnitData + items StartingPerks. |
| `_tmp_list2_perks_fresh.tsv` / `_tmp_list2_sheet_diff.md` | Snapshot + human diff notes for Лист2 perk sync. |
| `_restore_metadata_code_load.py` | После Mod Editor `SaveDef`: wrapper на `_restore_dropped_metadata_code.py --from-items` — вернуть в `metadata.code` все `ModItemCode` из `items.lua`; убрать плоские дубликаты `InventoryItem/vanillunique`. |
| `_restore_dropped_metadata_code.py` | Починка выпавшего load list. `--from-items` (после ресейва metadata): восстановить из `ModItemCode`. Без флага: git historic + дописать отсутствующие `ModItemCode` в `items.lua` (иначе следующий SaveDef снова выкинет). |
| `_audit_metadata_code_coverage.py` | Disk `Code/**/*.lua` ↔ `metadata.code` **и** `items.lua` ModItemCode. Unexpected MISS / META_ONLY / ITEMS_MISS = FAIL. Allowlist dormant/source-only (`AME_Browser_Template`, `MERC_Browser_Template`, `WeaponIconBake`, empty stubs). Импортируется из `_validate_items_quick.py`. |
| `_check_grandchien_map_lfs.py` | `../jazz-maps/Images/GrandChien2.png`: real PNG (~70MB) vs Git LFS pointer (чёрная sat map). Игрокам — `…/releases/download/playable/jazz-maps-playable.zip`, не archive ZIP. |
| `_fix_metadata_utf8_mojibake.py` | Аудит/обратимое исправление одного ошибочного прохода UTF-8→Windows-1251 в `title`, `description`, `last_changes`; `--check` / `--apply`, BOM сохраняется. |
| `_audit_hotfix_003.py` | HOTFIX-003 static regression: Unjam on CombatActions with WeaponResource jam gate; pinned OnAdded/OnBeginTurn + BeginTurn/ApplySuppressionStatus interrupt permanent MG OW; shotgun pellet pack one FX; tooltip ID `890000000001235` catalog + RU/EN. |
| `_audit_ui002_weapon_chips.py` | UI-002 static: Fold/Flash `ShowIn = false`, Unjam stays CombatActions; `idFoldStockButton`/`idFlashlightButton` GridX=2; HUD helpers + GetUIState zzFoldingPair. |
| `_audit_combat_bar_slots.py` | Two-row HUD: Recalc 24+25 **and** `Jazz_RegisterExtraCombatBarSlots` (`Action14`–`Action24` combat, `Action25` signature). Recalc padding alone does not spawn buttons. |
| `_audit_craft_ammo_homemade.py` | INV-003: CraftAmmo allow-list (`JAZZ_AMMO_*_Crafted` + saltshot), FillItemsToCraft filter, AdditionalResources wrap, `JAZZ_9x39_Crafted` in items+metadata, батч 100 Parts + qty по калибру. |
| `_audit_inv004_powder.py` | INV-004: BlackPowder на гренадерах/ГЛ (Legion+Army/Adonis/Rebel), RecipeDef TNT/C4/PETN→порох, `Jazz_TrySalvageMineCharge` 40%. |
| `_rebuild_weapon_chip_icons.py` | UI-002: rebuild thin 54×54 Fold/Flash chip glyphs from old dual-strip `Icons/stock_*.png` / `flash_*.png` (left half, pad, light thin). |
| `_match_weapon_manip_icon_pairs.py` | UI-002: derive `weapon_flash_off` / `weapon_stock_unfold` from ON/Fold masters so HUD pairs share the same silhouette (beams/arrow only differ). |
| `_rebuild_stock_chip_glyphs.py` | UI-001: replace photo stock `ChipIcon` PNGs with flat `#C8C0A8` glyphs (`--finalize-dir` drafts or `--flatten-only`). |
| `_apply_combat_005_weight_items.py` | JAZZ-COMBAT-005: sync `Weight_*Class` Description + `OnCalcMoveModifier` → `JazzArmorWeightPainOnMove` in `items.lua`. |
| `_apply_ironclad_killingwind_fm_stack.py` | COMBAT-005/UNITS-006: Ironclad companion + items/metadata; KillingWind loc `890000000009876`; Ironclad Description `890000000013124`. Additive −50%/−50% FM tax. |
| `_check_ironclad_killingwind_fm_stack.py` | Static: `fm_mul - 50` twice; no shared OR-half; Ironclad loaded; cumbersome BeginTurn unchanged. |
| `_check_scrap_eject_no_setcomponent.py` | Scrap eject must not `SetWeaponComponent` (SCRAP ALL on loaded loot); ScrapItem special-scrap nil-safe. |
| `_check_meltdown_portraits.py` | Meltdown `MercPortraits/Meltdown.png` + `_Big.png` shipped; UnitData/items wire `Mod/Dv3mFVN/...`. |
| `_build_vengeful_temperament_sig_icon.py` | Meltdown active CA: 108×54 dual from vanilla Personal perk (`Perks/references/vanilla/VengefulTemperament.png`, skull in flame); wire jazz-units CombatAction.Icon (CE stays `UI/Icons/Perks/VengefulTemperament`). Do not use HUD `perk_vengeful_temperament`. |
| `_apply_combat_007_energy_items.py` | JAZZ-COMBAT-007: insert energy ladder ModItems (`Fit`/`Winded`/`Fatigued`/Tired/Exhausted/WellRested/FreeMove) + `System_EnergyLadder` into `items.lua`/`metadata.lua`. |
| `_apply_combat_007_energy_loc.py` | JAZZ-COMBAT-007/008 energy loc: upsert RU/EN CSV for Fit→Exhausted + travel logs + legs-trauma breakdown + Free Move UI (`890000000013100`–`13123`). `Text`=T() source, `Translation`=language (JA3 shows Translation). |
| `_audit_russian_csv_swapped_columns.py` | Find `Russian.csv` rows where English-source T() has RU in `Text` and EN in `Translation` (displays English in Russian UI). Exit 1 if any. |
| `_apply_freemove_remaining_ap_loc.py` | Remaining Free Move AP UI: RU/EN `890000000013122` (status tooltip) + `890000000013123` (merc-card AP suffix). Same column contract: `Text`=EN source. |
| `_check_freemove_remaining_ap_ui.py` | Static needles: `JazzFormatFreeMoveDescription`, icon overlay, PDAMercRollover AP suffix, save-safe `GetDescription`. |
| `_bump_freemove_ui_meta.py` | Remaining Free Move AP UI: revision +1 and prepend `last_changes` (escape `\n` only). |
| `_bump_metadata_combat008.py` | JAZZ-COMBAT-008: revision +1 and prepend `last_changes` bullet (escape `\n` only). |
| `_patch_combat_005_weight_loc.py` | JAZZ-COMBAT-005: RU/EN CSV text for five `Weight_*Class` Description IDs. |

## FortifyErnie / stationary MG

| Скрипт | Назначение |
| --- | --- |
| `_audit_hotfix_004.py` | Static HOTFIX-004: EnterEmplacement wrap, LoadGame/EnterSector reseat, HUD nil-guards. |
| `_audit_m3_entrance_sight.py` | M3 (`isJdmPy`): UnitMarker distances to Entrance markers vs `UnawareSightRange` 22 / `AwareSightRange` 46 (instant-combat triage). |
| `_audit_m3_unitmarker_flags.py` | M3 UnitMarker property keys + suspect Aware/Combat/status_effects lines (forced-combat triage). |
| `_audit_m3_unit_z.py` | M3 UnitMarker missing Z / local Z outliers vs Entrance heights (floating-spawn triage). |
| `_replace_steam_last_changes.py` | Full-replace `metadata.lua` `last_changes` for Steam Workshop upload (`--apply`). Default text: `_steam_last_changes_since_aug12.txt`. No Revision bump; no raw LF in quotes. |
| `_steam_last_changes_since_aug12.txt` | Player-facing Steam changelog bullets (12 Aug 2026 → current). |
| `_steam_last_changes_since_aug8.txt` | Older Steam draft (8 Aug window); kept for reference. |
| `_check_last_changes_preview.py` | Print decoded `metadata.lua` `last_changes` (escape check + bullet dump). |
| `_print_metadata_version.py` | Корневая engine-версия `metadata.lua` (`major.minor-revision`, не dependency CommonLib). `--engine` — только строка для Discord. |
| `_pack_suite_release.py` | Четыре GitHub-архива комплекта из exact SHA (`git archive` + LFS), детерминированный ZIP, SHA256SUMS, manifest. Никогда не копирует working tree. `python docs/tools/_pack_suite_release.py --jazz-sha … --assets-sha … --maps-sha … --units-sha …`. |
| `_audit_steam_editor_resave.py` | Diff Steam/Mod Editor resave vs HEAD: lost `ResolveValue`, EN→RU T() fallbacks, FreeMove damage. |
| `_audit_hotfix_005.py` | Static HOTFIX-005: remountable CanStack by RemovableComponentId; no Amount=1 clip on bag mark/normalize. |
| `_audit_mg_emplacement.py` | Сводка `MachineGunEmplacement` в `jazz-maps/Maps/*/objects.lua` (weapon/ammo heuristics). |
| `_audit_emplacement_cone_range.py` | Static: станковый MG конус = MaxRange ствола (`Jazz_EmplacementConeDist`) и **45°** (`Jazz_EmplacementConeAngle`); не map slider / MinRange / sight / COMBAT-009 `1/d`; `GetMaxAimRange` без зрения только на станке. |
| `_count_emplacement_ammo.py` | Счётчик `ammo_template` / `weapon_template` по всем `MachineGunEmplacement` в `jazz-maps/Maps`. |
| `_fix_fortify_ernie_mg_handin.py` | GreasyBasil `FortifyErnie`: `MG42` → `Jazz_Browning_MuchineGun`+`Jazz_Browning_Bench` (has/take); I5 `ubRwFgf` ammo_template → `JAZZ_AMMO_50BMG_Basic`. |
| `_patch_ernie_counterattack_heavies.py` | `jazz-units` EnemySquadDef `ErnieCounterAttack`: 1× Rocketeer + 2× AssaultT1_Grenadier + 1× Mortarman (no HeavyT2 hand GL). |

## CTH / cover

| Скрипт | Назначение |
| --- | --- |
| `_calc_cover_cth_gewehr.py` | Static Gewehr98 mid-merc cover CTH (open / full / half / stance); reads `RangeAttackTargetStanceCover` from `items.lua`. |
| `_check_cover_params_items.py` | Assert Cover/Exposed/Crouch/Prone params (−45/−12/−12/−23) and unique `DustStormCoverCTHPenalty = −40`. |
| `_audit_cth_mod_require_action.py` | List CTHMod `RequireActionType` (missing → class default `Any Attack`). |

## JAZZ-MED-001 / медицина

| Скрипт | Назначение |
| --- | --- |
| `_apply_med002_statuses.py` | MED-002: insert `WoundInfected` + `BloodLoss50`…`1` companions/items/metadata + RU/EN loc rows. |
| `_audit_med004.py` | Static MED-004: trauma floor 20 / Heavy 50% MaxHP; no d100 `thr_light`; Frag/HE center without `*shot`; NewHour catch-up. |
| `_apply_med004_grenade_shot.py` | MED-004: strip Frag/HE `CenterAppliedEffects` `*shot` in companions+`items.lua`; update blast trauma hints RU/EN. |
| `_audit_med001_kit_requirements.py` | Static MED-001: IFAK/Medkit Medical 30/50 gates, full bleeding clear, Medkit +50% healing, low-skill rollover warning, and companion/`items.lua` parity. |
| `_audit_med003_kits.py` | Static MED-003 (+MED-006 heal supersede): Medical 30/50/80, MaxStacks 5/10/15, trauma ranks, full bleed, Analgesia+infection, Large Bobby soft-tail, Bonemaker 5% medium; heal via `JazzKitHealAtFullMedical`. |
| `_audit_med006_kits_stabilize.py` | Static MED-006: stabilize helpers, heal% 30/60/100, MaxHP debt, icon PNGs, no kit→healing in GetBandaged; `JazzTraumaResolveNum` (no Lua `0 or preset`). |
| `_audit_med007_debt_fatigue.py` | Static MED-007: skip-debt in combat, CombatStart/End recalc, no grit-on-debt, travel from current HitPoints vs 100, loc 010293. |
| `_gen_trauma_status_icons.py` | Pillow: from each `Icons/StatusEffects/Trauma{Zone}{Tier}.png` write `*Stabilized` (sand badge) and `*Healing` (cyan badge) corner variants (30 PNGs). |
| `_apply_med006_trauma_ce.py` | MED-006: Trauma* Medium/Heavy reactions use effective-tier helpers; insert `System_Medicine_MED006.lua` in metadata. |
| `_apply_med006_kit_loc.py` | MED-006: kit AdditionalHint stabilize/%HP; strip heal_modifier +50/+100. |
| `_fix_med006_loc_id_collision.py` | MED-006: move stabilize/debt T-IDs off VoiceResponse `010220–222` onto `010290–292`. |
| `_polish_med006_loc.py` | MED-006 polish: kit Medical phrasing + Bandage CA `010213` stabilize (no kit trauma heal); Manual `010290–292`. |
| `_sync_med006_loc_to_lua.py` | Sync polished EN `T()` fallbacks into kit companions + `items.lua` (`010024/027/030/213`). |
| `_cleanup_med006_manual_loc.py` | Dedupe Manual MED-006 rows; drop stale Bandage CA; RU «кита»→«аптечки». |
| `_check_med006_loc.py` | Gate: polished RU/EN kits + stabilize IDs; no healing-on-kit in `010213`; VR IDs clean. |
| `_apply_med003_kits.py` | Apply MED-003 companion parity into `items.lua` + Bonemaker FirstAidKit/5% Medkit. |
| `_list_merc_medkits.py` | List Mercs loot defs with FirstAidKit/Medkit/Reanimationsset (`_merc_medkits_list.txt`). |
| `_audit_merc_med_loot_redistribute.py` | Static MED-003 hire loot: Med&lt;20 bandages-only, kit cascade, AME Small, bandage/morphine spreads vs plan. |
| `_audit_legion_med_loot_redistribute.py` | Static MED-003 Legion class loot: T2 bandage 1–2, T3 morphine 30%, medic 1–10/0–3 + kits. |
| `_audit_med001_large_kit_trauma.py` | Static MED-001 AC-017: Large Medkit (`Reanimationsset`) marks heaviest unhealed Trauma* with `jazz_healing`; targeting + GetBandaged + loc/hint wiring. Superseded for kits by MED-006 stabilize (TreatWounds healing remains). |
| `_check_trauma_unit_ud_sync.py` | Trauma* clear/apply/NewHour must sync Unit↔UnitData (sat portrait icons after «cleared»). |
| `_check_smoke_no_bleed.py` | Smoke/tear/toxic/fire skip ballistic bleed (JazzTryRollBleedFromHit, AppliedEffects, DangerClose). |
| `_check_melee_pain_trauma_cth.py` | Legacy/melee CTH applies Pain/trauma after accuracy clamp; Arms trauma Pain on melee/throw. |
| `_check_barry_craft_discount.py` | Barry DesignerExplosives −30% Parts on CraftAmmo/Explosives: recipe UI, consume wrap, queued total. |
| `_apply_localization_copy_edit.py` | Validates and applies reviewed RU/EN waves to manual memory; optional `AllIDs` propagates one source-identical review to every listed localization ID. |
| `_apply_maps_quest_repairs.py` | Идемпотентная generated-транзакция JAZZ-QUESTS-001: quest/conversation graph, companions и `jazz-maps/ModTextsMaps.csv`; map-object exports проверяются отдельным аудитом. |
| `_audit_dirty_lua_syntax.py` | Компилирует через `lupa` все modified/untracked `*.lua` в `jazz`, `jazz-maps`, `jazz-units`; read-only pre-commit gate для синтаксиса. |
| `_audit_maps_quest_contract.py` | Static JAZZ-QUESTS-001: компилирует затронутые Lua через `lupa`, проверяет quest wiring, шесть `objects.lua`, Barry Seal, wounded/ally markers, ModTexts и одинаковый RU/EN runtime ID set. |
| `_audit_maps_vanilla_quest_sectors.py` | Inventory/contract для JAZZ-QUESTS-002: stale HotDiamonds landmark refs в `jazz-maps` QuestsDef; `--strict` = exit 1 если Wave A+B ещё stale; Ernie-local I2/I3 и crocodile H14 отдельно. |
| `_apply_maps_vanilla_quest_sector_remap.py` | Идемпотентный apply JAZZ-QUESTS-002: remap sector refs в in-scope QuestsDef + `Pierre_2`/`FlagHill_Corazon_1` и `ModTextsMaps.csv` по transfer table (+ I3→J7, Elliot H14→P17); `--check` / `--apply`. |
| `_apply_maps_outpost_sector_remap.py` | Follow-up после перестановки карт: `TargetSectors` аванпостов, sector Events (A4/F13/L15), leftover outpost IDs в helper-квестах (`F7→E10`, `G10→L15`, `F19→K21`, `E16→G22` только outpost) и `ModTextsMaps.csv`. `--check` / `--apply`. Не трогает descr_id, Pantagruel E16, crocodile I18/I19. |
| `_audit_maps_stale_sector_refs.py` | Read-only inventory TargetSectors / quests / `effect_target_sector_ids` vs leftover vanilla landmark keys. |
| `_apply_maps_vendor_stall_ammo_remap.py` | Копирует ванильные `Banters_Vendors_Stalls` в `jazz-maps` Stall Banters и override vendor `LootDef` на `JAZZ_AMMO_*`. `--audit-only` ещё проверяет I5 `ubRwFgf` бартеры (`JAZZ_AMMO_762x39_FMJ` / `12gauge_Buckshot`, не `Drop_*`). `--apply` / `--audit-only`. Вход: dump `Data/BantersDef` + `LootDef.lua`. |
| `_bump_package_metadata.py` | Безопасно повышает package Revision на +1 и prepend-ит `last_changes` через literal `\n`, сохраняя UTF-8 BOM; default — dry-run, запись с `--apply`. |
| `_install_localization_exports.py` | Проверяет `sep=,`, схему, numeric/unique IDs и равенство RU/EN export sets; с `--apply` атомарно устанавливает парные runtime CSV. |
| `localization-copy-edits/quests_001.csv` | Канонические RU/EN строки ремонта квестов и разговора Barry Seal; вход для `_apply_localization_copy_edit.py`. |
| `localization-copy-edits/ame_runtime_statuses.csv` | Закрывает восемь накопленных AME status/filter строк RU/EN, чтобы парный runtime export был полным. |
| `_check_ai_medic_bandage.py` | Static: Medic/Medic_Low Healer exclusive + Early + MaxHp 85; `JazzAI_ShouldBecomeMedic` (no blanket bandage→Medic); Bandage Precalc. |
| `_check_sniper_hold_001.py` | Static JAZZ-AI-SNIPER-001: ExtremeRange; stay-hold; useless streak soft HighGround/stay weights (no hard escape). |
| `_check_ai_dbg_001.py` | Static JAZZ-AI-DBG-001: `AIDebugLog` option default off; CombatLog short gated; dest/attack/abort hooks; no extra `AIPlayAttacks` wrap. |
| `_check_ai_008_egress_perch.py` | Static JAZZ-AI-008: line perch holder + dest CheckLOS to shared Fallback OW egress; stay +180; hold wrap skips useless streak; no GetLoFData. |
| `_check_ai_009_break_los_ow.py` | Static JAZZ-AI-009: FallBack peel dest (break player LoS, +220, wrap after 008 hold) + OW on vacated stay; skip TakeCover/BunkerDown; no GetLoFData. |
| `_check_grenade_mishap_chance_curve.py` | Static JAZZ-GRENADES-001: throw blend Str+Dex+Expl; Strength `GetMaxAimRange`; smoothstep 0→full; no threshold/¼ cliff. |
| `_patch_grenade_mishap_hint_fullrange.py` | Frag/M79 RU+EN hints: Strength range + Str/Dex/Expl smoothness. |
| `_check_legion_support_024.py` | Static JAZZ-STRATEGY-024: support role recipe/archetypes/director/icon/loc; mixed specialist pool + `support_archetype = "mixed"`. |
| `_check_legion_rest_025.py` | Static JAZZ-STRATEGY-025: city/bunker/outpost rest helpers, top-up gate, loc/wiki smoke. |
| `_check_strategy026_tier_convoys.py` | Static JAZZ-STRATEGY-026: tier Msg, skip-pool pulse, T2 all-outpost money+people, docs/wiki/showcase smoke. |
| `_check_strategy027_tier_retake.py` | Static JAZZ-STRATEGY-027: T2/T2-3/T2-5 Major retake on player-captured outposts, skip pool/Heat, docs smoke. |
| `_reorg_squad_icons_folders.py` | One-shot: move `SquadsIcons/Enemy/*.png` into `_shields/`, `_misc/`, `<faction>/`. |
| `_rewrite_squad_icon_doc_paths.py` | Rewrite `squad-role-icons.md` image links after folder reorg. |
| `_bump_sniper001_meta.py` | Revision +1 + prepend `last_changes` bullet for SNIPER-001 commit. |
| `_apply_medic_heal_first.py` | Patch `jazz-units/items.lua` Medic/Medic_Low: combat behaviors Score=0 when heal needed; Healer Early/Weight 1000; Priority Bandage before MobileShot; SelfHealMod 100. |
| `_key_med_item_icons.py` | Flood-fill near-black → alpha для `Icons/Items/JAZZ_{Bandage,Morphine,IFAK,Medkit,SurgicalKit}.png` (не трогает тёмные молнии/ремни). |
| `_key_merc_mark_white_bg.py` | Flood-fill near-white → alpha для `Icons/PDA/MERC_Mark.png` (белый studio plate; жёлтый `$`/teal не трогает). |
| `_check_merc_credit_hire_gate.py` | Static: `System_MERC_Account.lua` — `CanAffordMerc` wrap для MERC + waive `MedicalPaidWhenHired`. |
| `_apply_med001_loot_jazz_units.py` | В `jazz-units/items.lua` к LootDef с `FirstAidKit`/`Medkit`/`Meds`/`MedsDrop` добавляет `JAZZ_Bandage` / `JAZZ_Morphine` / редко `JAZZ_SurgicalKit`. Идемпотентен (сначала снимает старые JAZZ med entries). |
| `_apply_med001_loot_equipment_kits.py` | Phase 2: бинт/морфий (± IFAK у мерков) в Equipment-киты без медицины (`loot=all` враги + Mercs leaf tiers). Не трогает ammo/Drop_/Armor. Merc insert: Bandage 10, IFAK 5. |
| `_apply_merc_med_full_stacks.py` | Mercs `group=Mercs` в `jazz-units/items.lua`: существующий `JAZZ_Bandage` → stack 10; `FirstAidKit` → 5; `Medkit` → 10; `Reanimationsset` → 15 (MaxStacks). Идемпотентен. |
| `_apply_merc_med_loot_redistribute.py` | Hire medicine by Medical/Doctor/Tier (MED-003): Med&lt;20 bandages only; kit cascade; AME Small; bandage/morphine spreads. Idempotent. |
| `_apply_legion_med_loot_redistribute.py` | Legion class inventories (recipes.json): T2 Bandage 1–2; T3 Morphine 30%; medic Bandage 1–10 + Morphine 0–3; strip Mortarman_Launcher junk. Idempotent. |
| `_apply_enemy_med_stacks_min.py` | Не-Mercs LootDef: `JAZZ_Bandage` / Morphine / Surgical / FirstAidKit / Medkit → `stack_min/max = 1`. Mercs не трогает. |
| `_fix_med001_loot_drop_lists.py` | Снимает ошибочные JAZZ med entries с `Drop_*` / Comment=list ammo pools; патчит `PierreGuard_Ordnance`. |
| `_audit_med001_loot_jazz_units.py` / `_audit_med001_unit_kits.py` | Аудит покрытия Bandage по medical LootDef и UnitData Equipment. |
| `_audit_loot_missing_items.py` | `jazz-units` `item=` vs known InventoryItem IDs (jazz `InventoryItem/` + vanilla ModTools defs). Exit 1 если есть MissingItem-кандидаты. |
| `_patch_med_stack_kit_loc.py` | MED stack kits: RU/EN hint «refill with Meds» → «one use = one item»; append `890000000010030` (Reanimationsset). |
| `_apply_med006_kit_loc.py` | MED-006: kit AdditionalHint stabilize/%HP (companions + `items.lua`); strip MED-003 `heal_modifier` +50/+100; RU/EN for `010024/027/030` and stabilize/debt `010290–292`. |
| `_fix_med001_loot_braces.py` | Чинит `}}),` → `}),` на строках JAZZ med loot (баг f-string). |
| `_bump_units_med_loot_meta.py` | Bump `jazz-units/metadata.lua` Revision + `last_changes` после loot apply. |
| `_wire_med001_traumas.py` / `_append_med001_trauma_loc.py` | Wiring/loc зональных Trauma* эффектов. |
| `_apply_grenade_concussion.py` / `_append_grenade_concussion_loc.py` / `_patch_he_grenade_concussion_hint_loc.py` / `_fix_concussion_loc_ids_items.py` / `_patch_grenade_concussion_guaranteed_loc.py` | Playtest: `Concussion` CharacterEffect + items/metadata; RU/EN loc `890000000010277–280`; Frag/HE hints. Runtime: `JazzTryApplyExplosionConcussionAndTrauma` (concussion guaranteed). Loc patch: chance→guaranteed on IDs `243383619902` / `663236691841`. |
| `_patch_grenade_mishap_hint_loc.py` | RU/EN Frag `243383619902` + M79 `397383171067` AdditionalHint: quarter/half mishap curve, thr ~50, elite max-range note. |
| `_patch_grenade_mishap_magnitude_90.py` | **Superseded (2026-08-24).** Historical: half≈old max / full≈+25% scatter; skill floor 10% on **both** bands. Do not re-run — would shrink mishap again. Current: Max-band is a miss (`GetMishapDeviationBounds` in `System_OR_Weapons.lua`). |
| `_bump_metadata_grenade_mishap.py` / `_stage_items_grenade_hints_only.py` | Commit helpers: metadata revision+last_changes; items.lua = HEAD + Frag/M79 hints only (officer WIP aside). |
| `_apply_officer_aura_loc.py` | CMD-001 UI: RU/EN `890000000006100–6125` (OfficerAura / Influence; directives; buff labels; order-effect + FocusFire target tooltip). |
| `_apply_jazz_trauma_effect_parent.py` | Trauma* → parent/`object_class` `JazzTraumaEffect` (companions + `items.lua`); paired with early `Code/System_JazzTraumaEffect.lua`. |
| `_audit_trauma_loc_ids.py` | Trauma* + medicine timing T() IDs vs `Russian.csv`/`English.csv` (Text match, non-empty Translation, no garbage). Exit 1 if broken. |
| `_patch_med001_hit_pain_ac.py` | MED-001: insert AC-012 (+ fix REQ-010 backticks) for `JazzPainOnDamagingHit` contract. |
| `_fix_med001_runtime_csv.py` | MED-001: чинит `Russian.csv` Text/Translation (EN source / RU translation) + literal `\\n` → реальные переносы в AdditionalHint. |
| `_fix_med_en_in_ru_loc.py` | Playtest: восстанавливает RU Translation для MED AdditionalHint (`010013/016/019/024/027/030`) + Concussion `010277–280`; снимает `mag-hint-aligned` vanilla stomps EN-in-RU. |
| `_scan_en_in_ru_loc.py` | Read-only: Cyrillic Text + English Translation в `Russian.csv` (perk/CA vs other vs both-EN). |
| `_alloc_mod_loc_id.py` | Следующий свободный ID в `890000000000000..890000000099999` (скан Lua/CSV, без `Maps/`). |
| `_insert_runtime_loc_row.py` | Точечная вставка одной однострочной loc-строки в RU/EN + Strings + manuals (без перезаписи всего CSV). |
| `_fix_en_in_ru_ability_loc.py` | Playtest: `Russian.csv` Translation=Text для perk/signature CA (UNITS-006 `upsert_csv` писал EN в RU). `--apply`. Не трогает VR/InventoryItem. |
| `_fix_med001_loc_append.py` | Перезаписывает RU/EN строки `890000000010200+` (JazzBandage / trauma timing / kit Bandage desc); Text=EN, Translation=язык. |
| `_patch_combat_status_ui.py` | CombatBadge: 2–3 critical icons у ника; party combat `idWounded` → `JazzGetPartyPortraitStatusEffects` (parity с satellite). |
| `_recenter_med_action_icons.py` | Recenter+upscale dual-strip 108×54: `--dir Icons/Med` (default) или `Perks/SignatureAbilities`. Мелкие/съехавшие к центру полосы → fill≈48px. `--dry-run` / `--pad`. |
| `_audit_action_icon_center.py` | Аудит bbox/dx/dy dual-strip в `Perks/SignatureAbilities` + `Icons/Med` (+ list лишних 108×54). WARN если \|dx\|/\||dy\|>2.5. |

## JAZZ-ATTACH-001 / оружие–обвесы

| Скрипт | Назначение |
| --- | --- |
| `_apply_steam_ignore_files.py` | Синхронизирует `ModDef.ignore_files` + `.gitignore` по всем пакетам suite (`jazz`, `jazz_assets`, `jazz-units`, `jazz-maps`, `jazz-nomaps`): Steam pack exclusions + bump Revision + append `last_changes`. Запуск из любого cwd; пути абсолютные к `Mods/`. |
| `_apply_attach_001.py` | Основная миграция ATTACH-001: strip Handling-effects, CloseRange wiring, Mount purge, `JAZZ_` rename, unused delete. `--dry-run` (default) / `--apply` (+ `.bak`). |
| `_export_attach_csv.py` | Экспорт `weapon-components*.csv` / `weapons.csv` из **working tree** (`items.lua` + companions; weapons без companion — из ModItem). Нужен когда нет `JA3_ROOT` для `weapons-docs.mjs import`. |
| `_build_ar15_assets.py` | JAZZ-WEAPON-AR15-FAMILY-001, фаза 2: сборка `M16A4` и `M4A1` из сохранённого источника tigg. Запуск `blender --background --factory-startup --python docs/tools/_build_ar15_assets.py -- --source <tigg_ar15variants_2015.blend> --output <build> --game-root <JA3_ROOT> [--export]`. Режет только целые острова: ствол = дульник+труба+мушка, дельта-кольцо на хосте, цевьё отдельно, альтернативные длины с соседних хостов той же локальной рамки. Линейка — реальная длина (k = 1.0). Слот `Muzzle` ставится на каждую сущность ствола. Превью конфигураций и `build-report.json`. В пакеты мода ничего не пишет. |
| `_integrate_ar15_family.py` | Первичная установка графа `M16R_*`/`M4R_*`. Повторная доустановка видимых стволов/цевий — `_wire_ar15_visible_modules.py`. |
| `_wire_ar15_visible_modules.py` | Доустановка видимых стволов, цевья A4, `JAZZ_Handguard_RIS` и `JAZZ_CarryHandle_AR15`. `python docs/tools/_wire_ar15_visible_modules.py --build <build> [--apply]`. Обновляет хосты (ствол больше не впечён), регистрирует новые сущности, слоты и визуалы. Dry-run по умолчанию. |
| `_audit_ar15_entity_graph.py` | Read-only проверка установленного графа AR15 (20 сущностей): `.ent` без `<src>`, меши/материалы, `ModItemEntity`, `metadata.entities`/`code`, текстуры ≤ 2048 и fallback'и ≤ 64. |
| `_audit_ar15_slots.py` | JAZZ-WEAPON-AR15-FAMILY-001: сверяет слоты пяти эмок (`M16A1`/`M16A2`/`M16A4`/`M4A1`/`CAR15`) между `items.lua` и companion, проверяет, что каждый компонент существует с тем же `Slot` и что `DefaultComponent` входит в свои опции. Read-only, exit 1 при расхождении. |
| `_export_fal_assets.py` | JAZZ-WEAPON-FAL-FAMILY-001: ранний сборщик Para-приклада из архива. Разложенное состояние с архива не село на спот `Stock` — для unfolded используем ванильный `WeaponAttA_StockFNFal_01`, складку собирает `_export_fal_folded_vanilla.py`. |
| `_export_fal_folded_vanilla.py` | JAZZ-WEAPON-FAL-FAMILY-001: складывает ванильный `WeaponAttA_StockFNFal_01` (10 островов, петля по `max Y`). Пишет только `FNFAL_ParaStk_fld`. Дальше `AssetsProcessor` + `_apply_weapon_geometry_update.py`. |
| `_fix_fal_stock_seat.py` | JAZZ-WEAPON-FAL-FAMILY-001: unfolded visual → `WeaponAttA_StockFNFal_01`, дефолт классического `FNFAL` → `JAZZ_StockLightUnFolded`. |
| `_export_fal_tactical_assets.py` | JAZZ-WEAPON-FAL-FAMILY-001: то же для тактических цевья и приклада из архива `FN FAL _Tactical_`. Сваривает вершины донора, масштабирует см→м. Цевьё сажает по заднему (приёмному) торцу `max-Y`; приклад — по переднему `min-Y`. `--only` ограничивает сущности. Пишет `FNFAL_Tactical.fbx` + `fal-tactical-report.json`. |
| `_inspect_fal_tactical_handguard.py` | Read-only bbox/торцы ванильного `HandguardFNFal_01` и донора `model_2`. |
| `_preview_fal_tactical_handguard.py` | Overlay ванильного цевья и RIS: старая посадка по дулу vs новая по приёмному торцу. В пакет не пишет. |
| `_install_fal_assets.py` | JAZZ-WEAPON-FAL-FAMILY-001: раскладывает собранные сущности FAL в `jazz_assets` и регистрирует их в `items.lua` + `metadata.entities`/`code`. |
| `_apply_fal_family.py` | JAZZ-WEAPON-FAL-FAMILY-001: переводит классический `FNFAL` на Tier 2 со складным Para-прикладом и чинит иконки предметов-магазинов FAL. |
| `_add_fal_tactical_item.py` | JAZZ-WEAPON-FAL-FAMILY-001: создаёт `JAZZ_FNFAL_Tactical` — ModItem, companion, `metadata.code` и зеркалирование визуалов с `FNFAL` на новый ID. Идемпотентен: повторный запуск схлопывает дубли визуалов. |
| `_render_fal_tactical_icon.py` | JAZZ-WEAPON-FAL-FAMILY-001: инвентарная иконка 324×165 тактического FAL прямо из собранной сцены архива (споты движка не нужны). Рисует только штатную конфигурацию — ствольная коробка, RIS-цевьё, полимерный приклад, магазин. Два шага: Blender рендерит raw, системный Python (`--post`) кадрирует и накладывает контурный градиент серии. |
| `_fix_fal_mag_component_icons.py` | JAZZ-WEAPON-FAL-FAMILY-001: переводит `ModItemWeaponComponent` FAL-магазинов с галиловской и M16-иконок на ванильные `fnfal_mag_ergo_*`. Правит только Icon уровня компонента внутри именованного блока; декларативен и безопасен для повторного запуска. |
| `_fix_fal_tactical_indent.py` | JAZZ-WEAPON-FAL-FAMILY-001: восстанавливает отступ заголовка `PlaceObj` у блока `JAZZ_FNFAL_Tactical`. `check-generated-sync.ps1` ищет ModItem по совпадению отступов открывающей и закрывающей скобок, поэтому блок в нулевой колонке парсится, но аудиту не виден. |
| `_apply_fal_legion_stock_loot.py` | JAZZ-WEAPON-FAL-FAMILY-001 REQ-007: в `jazz-units/items.lua` фиксирует обычный приклад на легионных FAL-дефах, чинит `BattleRifles_FNFALLight` на `JAZZ_StockLightUnFolded` и подключает его в три пула Легиона. `--apply`. |
| `_apply_m14_family_grip_stock.py` | JAZZ-WEAPON-M14-FAMILY-001: `ModifyRightHandGrip` на `M14SAW`/`M21`; визуалы Heavy/Plastic → `WeaponAttA_StockM14_Standard`. `--apply`. |
| `_extract_m14_family_sources.py` | JAZZ-WEAPON-M14-FAMILY-001: уникальные OBJ/PNG из M14 zip во временный каталог, архивы не меняет. |
| `_export_m14_family_assets.py` | JAZZ-WEAPON-M14-FAMILY-001: Blender, посадка Lego-дерева, ART, Sage EBR и уника на ванильный `Weapon_M14`. Доворот по Y, атлас для EBR/уника. Пишет FBX в build, в пакеты не ставит. |
| `_m14_inspect_parts.py` | Blender: read-only галерея `part_*.obj` в исходных осях, `--source <dir> --output <png>`. Помогает отличать альтернативные сборки от недостающих деталей. |
| `_m14_repair_ebr.py` | Заменяет ошибочную EBR-ветку старого exporter: полный Sage, правильные карты деталей, явная ориентация, normal/short/long barrel. `--source <mk14> --output <new build> --game-root <JA3_ROOT>`, строгий mesh QA, blend/FBX и previews; в мод не пишет. |
| `_m14_repair_classic.py` | По одной entity: `--source <blend> --entity JAZZ_M14|JAZZ_M14_ART|JAZZ_M14_MkIII --output <new build> --game-root <JA3_ROOT>`. Исправляет ориентацию классики/ART, отделяет barrel/magazine, убирает запечённый обвес Mk III; возвращает его magazine/bolt из исходного part_03 с правильной UV-картой. Строгая подготовка, FBX, отчёт и assembled preview. |
| `_m14_install_ebr_repair.py` | После AssetsProcessor: `--host MK14EBR|JAZZ_M14|JAZZ_M14_MkIII --export-root <ExportedEntities> --build <repair> --game-root <JA3_ROOT> [--apply]`. Точечные ресурсы, ApplyTo и регистрации, backup при закрытой игре. Классика/MkIII сохраняют текущие DDS; EBR получает исправленный atlas. MkIII: штатные сменные 12x/Suppressor по умолчанию, винтовочный хват. ART ставится через `_apply_weapon_geometry_update.py`. |
| `_integrate_m14_family.py` | JAZZ-WEAPON-M14-FAMILY-001: стейдж сущностей, `M14SAW`/`M21` → `JAZZ_M14`, предметы `MK14EBR` и `JAZZ_M14_MkIII`, ART как дефолт M21, зеркало визуалов. Требует закрытой игры. |
| `_render_m14_family_icons.py` | JAZZ-WEAPON-M14-FAMILY-001: иконки 324×165 с обводкой серии. Blender raw, затем `--post`. |
| `_apply_fal_tactical_loot.py` | JAZZ-WEAPON-FAL-FAMILY-001 REQ-008: `JAZZ_FNFAL_Tactical` в легионные T2-4 пулы и `Adonis_AssaultRifle` / `AdonisElite_AssaultRifle`. Пишет `items.lua` + metadata resources. `--apply`. |
| `_analyze_weapons_balance.py` | Аудит баланса по `weapons.csv`: within-family z-score, residual vs tier, rare `AvailableAttacks`, peaks → `.tmp/weapon_analysis.json`. |
| `_analyze_weapons_followup.py` | Печать срезов (AR/SMG/sniper/uniques) из `.tmp/weapon_analysis.json` для ручного разбора. |
| `_apply_weapon_role_tweaks.py` | Ролевые твики FAMAS/Agram/Sig550*/PSG1 → companions + `items.lua` + `weapons.csv`. `--apply`. |
| `_update_role_tweak_loc.py` | RU/EN AdditionalHint для тех же стволов в `Russian.csv`/`English.csv`. |
| `_verify_role_tweaks.py` | Быстрая проверка props в `items.lua` после role tweaks. |
| `_remove_cancelshot_attacks.py` | Убирает `CancelShot` из `AvailableAttacks` оружия в `items.lua` + `weapons.csv` (не трогает grenade AreaAppliedEffects / CancelShotCone). |
| `sync-reload-style-csv.py` | JAZZ-WEAPONS-004: добавляет `reload_style` в канонический `weapons.csv` и проставляет Magazine/Tube/Break/Revolver по утверждённому списку ID. |
| `_promote_vanilla_refs.py` | **Устарело / опасно:** тонкие stubs без Visuals. Не запускать. |
| `_promote_vanilla_refs_visuals.py` | AC-008: поднять 9 dangling vanilla_ref в `JAZZ_*` ModItem **с Visuals** из `Data.hpk` (`WeaponComponentSharedClass.lua`); rename AvailableComponents/DefaultComponent + metadata resources. Требует `.tmp/data-extract/` после `hpk extract Packs/Data.hpk`. |
| `_remove_handling_stat.py` | Удалить Firearm property `Handling` + данные оружия + WeaponPropertyDef/GameTerm/CTH modifier + колонку CSV. Idempotent. |
| `_fix_items_lone_commas.py` | Починить дыры `{ a, , b }` после PlaceObj-delete (одиночные `,`), откатить пустые stub-ID → vanilla, удалить stub ModItems. Запускать если `items.lua` не грузится / GPU assert после массового delete. |
| `_fix_akm_scope_mount_visuals.py` | Добавить Visual `WeaponAttA_MountAK47` `ApplyTo=AKM` на западные прицелы (`Scope_12x`/`6x`/`NightScope`), у которых не было переходника (слот Mount не нужен — меш в Visuals оптики). |
| `_rebalance_reflex_tiers.py` | `JAZZ_Reflex_*`: Precision/OW/Universal; AA% + CloseRange soft + MinAim/−1 MaxAim. Канон: `docs/design/reflex-collimator-tiers.md`. |
| `_rebalance_combat_scopes.py` | Combat: mid near/OW + AimAccuracy% 125…155. Канон: `docs/design/combat-scope-tiers.md`. |
| `_rebalance_long_scopes.py` | Длинная/entry/night: far reach, ShotAP+Crit, harsh near, cost tiers. Канон: `docs/design/long-scope-tiers.md`. |
| `_rebalance_barrel_tiers.py` | Стволы: BDR% + CloseRange* + Recoil; R ±1. Канон: `docs/design/barrel-tiers.md`. |
| `_rebalance_muzzle_tiers.py` | Дуло: Recoil vs Silent; choke pattern; без R/BDR. Канон: `docs/design/muzzle-tiers.md`. |
| `_rebalance_magazine_tiers.py` | Магазины: small / standard / expanded(no-tax) / large(tax). Канон: `docs/design/magazine-tiers.md`. |
| `_apply_mag_size_set.py` | JAZZ-ATTACH-001 MagSizeSet: добавляет effect/resource/localization, разрезает generic `JAZZ_MagLarge` на абсолютные варианты, rewires items + companions и проверяет отсутствие live mag multiplier. `--apply` пишет `.bak`. |
| `_apply_mp40_mag_normal_only.py` | MP40: только `JAZZ_MagNormal` (32). Убирает `JAZZ_MagLarge_50_MP40` из слота/компонента/remountable/metadata и из GenW `LootEntryUpgradedWeapon` в `jazz-units`. `--apply`. |
| `_verify_mp40_mag_normal_only.py` | Smoke: MP40 MagNormal-only, no MagLarge_50_MP40 in jazz/jazz-units, LoadGame reseat map present. |
| `_verify_mp40_mag_normal_only.py` | Smoke: нет `JAZZ_MagLarge_50_MP40` в jazz/units data; GenW assault_m1 = InventoryItem; reseat map в `System_WeaponComponent_Set.lua`. |
| `_gen_setweaponcomponent_override.py` | Генерирует `Code/System_WeaponComponent_Set.lua` из vanilla `FirearmBase:SetWeaponComponent` + ветка `ModificationType=Set` (`mul=1000`, `add=N−base`). |
| `_apply_grizzly_perk_full_damage.py` | GrizzlyPerk: `dmg_penalty` −50→0 + sync CE description in `items.lua`. |
| `_restore_grizzly_perk_hud_icon_and_rok.py` | GrizzlyPerk CA: stock `UI/Icons/Hud/perk_grizzly_perk` + `recharge_on_kill=1` (undo SignatureAbilities glyph swap). |
| `_apply_saltshot_pain_cap.py` | HOTFIX-007: saltshot `AppliedEffects` → `Pain` (+ cut-content hint); runtime fill-to-cap in `Systems_Medicine.lua`. |
| `_fix_haveablast_grenade_pockets.py` | Red HaveABlast: docs/meta for GrenadesInventory AG–DG retaliate (runtime `System_HaveABlast.lua`). |
| `_apply_haveablast_fix.py` | HaveABlast: sync CE reactions/description into `items.lua` (optional helper; primary edit is companion + items). |
| `_patch_haveablast_loc.py` | HaveABlast: patch RU/EN description rows in `English.csv`/`Russian.csv` without full CSV rewrite. |
| `_apply_nazdarovya_recharge_on_kill.py` | Igor Nazdarovya: CA `recharge_on_kill=1`, `Unit:Nazdarovya` AddSignatureRechargeTime, GetUIState CD, Ensure cache, loc/docs. |
| `_patch_nazdarovya_loc.py` | Nazdarovya/Drunk: upsert RU/EN rows for perk, status, CombatAction strings. |
| `_patch_buildingconfidence_loc.py` | MD BuildingConfidence: upsert RU/EN perk description (Inspired turns + heal level-diff). |
| `_rollback_hawkseye_vanilla.py` | Scope HawksEye: remove JAZZ CE/items/metadata override (back to vanilla PinDown+biscuits). |
| `_restore_hawkseye_jazz.py` | Restore Scope HawksEye JAZZ CE: sniper OW 1 AP, suppress ×2, biscuits 96h×7 + hire; items/metadata/RU/EN. |
| `_check_hawkseye_ow_suppress.py` | Static: HawksEye companion + OW branch + suppress hook + 96h×7 loc. |
| `_audit_mag_size_set_defaults.py` | Список оружия с default-магазином на `MagazineSizeSet` (поверхность бага MagSize=1 при `mul=0`). |
| `_validate_wave_weapons.py` | Статическая валидация волны ATTACH-001 MagSizeSet + WEAPONS-002..005 (якоря, metadata load, loc, CSV). |
| `_peek_mag45_kobra.py` / `_peek_mag45_kobra2.py` / `_list_reload_effects.py` | Peek Mag45 / Reflex_Cobra effects+params и Reload* effect presets в `items.lua`. |
| `_fix_stock_barrelparts_costs.py` | WEAPONS-002: `JAZZ_BarrelParts` в AdditionalCosts только у Slot=Barrel; остальное → `Parts`. `--apply` + `.bak_stock_barrelparts`. |
| `_make_barrelparts_icon.py` | Иконка `JAZZ_BarrelParts`: extract `fine_steel_pipe.dds` из `UI.hpk`, charcoal recolor → `Icons/Items/JAZZ_BarrelParts.png`, wiring companion/`items.lua`. |
| `_purge_legacy_gunsmith_parts.py` | WEAPONS-002: безопасный remap только `'Type'`/`'item'` в costs (`FineSteelPipe`→`JAZZ_BarrelParts`, lens/chip→`Parts`); **не** трогает `'Id'`. `--restore-bak` из `items.lua.bak_legacy_parts`; dormant shop на legacy defs. `--apply`. |
| `_verify_gap_fixes.py` | Smoke после wave gaps: Id uniqueness Parts/BarrelParts, Type leftovers, unique WeaponMass. |
| `_verify_nomaps_unit_remap_named_skip.py` | COMPAT-004: static mirror remap families — Bastien skip; `WeakFlagHill`→assault; `*_Tutorial` stems; Hyena skip. |
| `_verify_nomaps_fortress_pierre_squad.py` | NoMaps: `FortressPierre` must stay out of `SQUAD_REMAP` (vanilla Pierre boss; not `LegionJAZZSquadT2`). |
| `_verify_nomaps_story_quest_skip.py` | COMPAT-010/011: skip class-remap for `LegionWaterWell` / `DiamondRedSquad` / F5 beach / `FortressPierre`; Pierrot `conflict_ignore`. I1 is not a keep-vanilla sector. |
| `_retire_legion_fortress_defenders.py` | Удаляет `LegionFortressDefenders`; добавляет `FortressDefenders_NoMaps` (~16); NoMaps remap/garrison → half-size pack. |
| `_apply_ernie_counterattack_nomaps.py` | Adds `ErnieCounterAttack_NoMaps` (20, no mortar) + NoMaps `SQUAD_REMAP` from `ErnieCounterAttack`. |
| `_dump_villa_squads.py` | Dump min–max composition of AroundVilla Sentry + VillaAttackers_K3/K5/L3/L4/L5 and sector Init totals. |
| `_tighten_villa_squads.py` | Set Villa Sentry=10 + Attackers 12/13/14/15/16 (sector Normal 22–26); Easy/Hard ±10 documented in baseline. |
| `_rewrite_legion_ernie_village.py` | Rewrite `LegionErnieVillage` (I5=60 meat+10 Pillager) + `Shooters_Easy_Ernie` (J5=40); strip Extra stacking from I5/J5 Init. |
| `_ernie_init_dump.py` | Dump Ernie ModItemSector `InitialSquads` + **design-Normal** sums (gated: engine Hard; ungated always). Does not cross ModItemSector boundaries. |
| `_sync_ernie_campaign_inits.py` | Sync HotDiamonds CampaignPreset Ernie Init → ModItemSector canon (UNITS-007 + locked hubs); clear map-only I6/J6/L7/K4/K6. Dry-run / `--apply`. Edits only CampaignPreset span + ModItem clears. |
| `_audit_ernie_empty_squad_risk.py` | Ernie Init empty-spawn risk + Campaign vs ModItem drift (boundary-safe). |
| `_rollback_units006_vanilla_merc_perks.py` | Remove jazz CE overrides for listed vanilla merc personal perks (ModItem+companion+metadata+loc); also jazz-units `TheGrim`. |
| `_apply_ernie_overflow_inits.py` | UNITS-007 Ernie overflow Init: base packs + Extra + I7 FortressDefenders. `--extras-only` rewrites `LegionExtra_Ernie_*` as per-unit slots (vanilla clones `UnitCount` of one rolled class). |
| `_fix_ernie_mixed_per_unit.py` | Historical Mixed-only split. Canon: `_apply_ernie_overflow_inits.py --extras-only`. |
| `_fix_checkdifficulty_storeastable.py` | Mass-fix `CheckDifficulty` `'Difficulty', "X"` → `Difficulty = "X"` (FunctionObject StoreAsTable=true; prevents load assert). Also syncs CampaignPreset M4 Init + Extra. Dry-run / `--apply`. |
| `_audit_units_squad_load.py` | Audit jazz-units CheckDifficulty format + M4 InitialSquads ModItemSector vs CampaignPreset drift. |
| `_apply_ernie_i2_lighthouse.py` | Earlier I2 lighthouse draft (superseded by overflow apply). |
| `_probe_ernie_init_blocks.py` | Probe `InitialSquads` by `sectorId`. |
| `_purge_k4_house_ambushers.py` | Remove K4 `HouseAmbushers`+`Legion` AdvanceTo; insert `VillaSiege_Wave2`×25 gated by `Jazz_VillaCounterAttack.Wave2Spawn`. Consumes `, nil, HANDLE)` so leftover closers do not break `LoadObjects`. |
| `_check_k4_objects_syntax.py` | K4 `objects.lua`: no orphan `, nil, HANDLE)` lines, Wave2=25, balanced braces, file ends with `LoadPersistFlagTables()`. |
| `_add_villa_attackers_ernie.py` | Insert `JAZZ_Legion_VillaAttackers_Ernie` base 30 + metadata. |
| `_wire_villa_counterattack.py` | Quest `Jazz_VillaCounterAttack` + FlagHill Guests + ModItemCode/metadata. |
| `_verify_villa_counterattack_static.py` | Static: Ernie size, Wave2 count, old siege remaining=0. |
| `_verify_guardpost_scripted_attack.py` | Guardpost: `ForceSet` does not call `CanSpawnNewSquad`; managed early-out kept on CanSpawn/Update/Spawn (scripted Ernie attack OK, vanilla auto muted). |
| `_verify_nomaps_early_squad.py` | COMPAT-005: `LegionJAZZSquadT1_Early` all `T1_`; metadata Id; NoMaps remap/cap wiring. |
| `_verify_nomaps_globals_predeclare.py` | NoMaps wrap flags predeclared at file top + `rawset` + `lQuestVarSafeSet`. |
| `_verify_nomaps_region_radius.py` | COMPAT-007: `AUTO_REGION_RADIUS=false` (unbounded Voronoi), `AI_REGION_REV=2`, multi-outpost refresh; no legacy `<= 8`. |
| `_verify_nomaps_squad_size_cap.py` | COMPAT-009: только `InitialSquad*` NoMaps capped at 30 в `GenerateUnitsFromTemplates`, после BodyCount; dynamic squads/economy unchanged. |
| `_audit_loot_item_case.py` | `jazz-units` LootEntry `item=` vs `InventoryItem` DefineClass (ловит `Mas36`≠`MAS36`). Exit 1 при mismatch. |
| `_audit_faction_overlay_static.py` | Static AC hooks for STRATEGY-014/018: matrix API, ownership, avoid-player routing, load registration. |
| `_apply_hotfix006_difficulty_loc.py` | HOTFIX-006: rewrite Normal/Hard/VeryHard GameDifficultyDef tooltips in `items.lua` + Russian.csv/English.csv (copy limits, medics, starting funds). |
| `_test_legion_class_caps.py` | HOTFIX-006: same-id (except `JAZZ_LegionUncappedLineIds`) + escort Front specialists + Marksman deny; STRATEGY-008 bucket formulas unchanged. |
| `_test_legion_medic_density.py` | STRATEGY-015: static mirror `JAZZ_GetLegionMaxMedics` (Normal +1 / Hard 0 / VeryHard −1) + generator wiring markers. |
| `_test_legion_spawn_pool.py` | Static STRATEGY-019: global spawn pool + tax/recruiter 72h gate + tax/recruiter → combat → supply order. |
| `_test_legion_squad_growth.py` | STRATEGY-016: early→mature sizes, economy ×0.25 markers, cadence defaults; NoMaps size override. |
| `_test_legion_money_cargo.py` | STRATEGY-017: tagged cargo sync / tax collect / regen resync markers. |
| `_dump_sergeant_firearm.py` | Read-only: dump `Sergeant_Firearm` primary unlocks (weapon / Amount band / weight / package) from `jazz-units/items.lua` after legion-loadouts regenerate. |
| `_insert_reload_combat_action.py` | WEAPONS-004: вставляет full `ModItemCombatAction` `Reload` в `items.lua` + `ModResourcePreset` в `metadata.lua`. |
| `_insert_rebels_flanker.py` | ROLE-001 repair: clone `Legion_Flanker` → `Rebels_Flanker` in `jazz-units/items.lua` (metadata Id already present). Idempotent. |
| `_set_flanker_optloc.py` | Set `OptLocSearchRadius` on `Legion_Flanker` / `Rebels_Flanker` (default 55). |
| `_count_aiarchetypes.py` | List/count `ModItemAIArchetype` ids in `jazz-units/items.lua`. |
| `_fix_weaponmod_untranslated.py` | ModifyWeaponDlg: заменить `Untranslated("<bullet_point> "..)` на `T{990002014,…}` в XTemplate (assert IsLookupTag). |
| `_fix_unique_reload_style.py` | WEAPONS-004: `ReloadStyle` на `InventoryItem/vanillunique/*` quest/unique. |
| `_rebalance_stock_tiers.py` | Приклады: Normal/Heavy/Light/Folded. Канон: `docs/design/stock-tiers.md`. |
| `_rebalance_under_grip_tiers.py` | Рукоятки: Vertical Recoil / Tac·Wrap CloseFactor / Ergo AA%. Канон: `docs/design/under-grip-tiers.md`. |
| `_rebalance_bipod_tiers.py` | Сошки: один `JAZZ_Bipod` + Under; cut Fold/MG42/KSP. Канон: `docs/design/bipod-tiers.md`. |
| `_rebalance_side_tiers.py` | Side: Flashlight/Dot/Laser/UV. Канон: `docs/design/side-tiers.md`. |
| `_fix_dup_bipod.py` | Убрать дубли `JAZZ_Bipod` после cut-remap. |
| `_fix_flashlight_off_opts.py` | Добавить `JAZZ_FlashlightOff` в AvailableComponents + stock fold pair JAZZ_ ids. |
| `_list_stock_profiles.py` | Dump текущих `JAZZ_Stock*` effects/params. |
| `_peek_stock_costs.py` | Peek `JAZZ_Stock*` `Cost` / difficulty из `items.lua` (после `_rebalance_stock_tiers`). |
| `_gen_removable_attachment_items.py` | WEAPONS-002: каталог InventoryItem на каждый remountable `JAZZ_*` component (`Id` = component id, folder RemovableAttachments). `--apply` → items/metadata/companions/loc. Hyphenated ids → `DefineClass("Id-With-Hyphen", {…})`. |
| `_split_mag_families.py` | Режет shared `JAZZ_Mag*` по mag-well семьям (`…_AK` / `…_AR15` / …); клоны WeaponComponent + InventoryItem companions. |
| `_union_mag_family_options.py` | После split: union Magazine options внутри семьи (магазин АК → РПК). |
| `_remove_mag_50_ak.py` | Убрать ошибочный `JAZZ_MagLarge_50_AK`; канон АК expanded = `JAZZ_MagLarge_30_40` (40). |
| `_fix_hyphen_defineclass.py` | One-shot: `DefineClass.Name-With-Hyphen = {` → string form (load error «syntax error near '-'»). |
| `_fix_removable_metadata_presets.py` | Починить metadata stubs каталога → `ModResourcePreset` InventoryItemCompositeDef. |
| `_add_scopeparts_loc.py` / `_fix_scopeparts_loc_schema.py` | Loc для `JAZZ_ScopeParts` + remove-fail messages (RU/EN full schema). |
| `_cut_muzzle_booster.py` | One-shot: вырезать `JAZZ_MuzzleBooster` из items/metadata/companions. |
| `_list_mag_profiles.py` | Dump текущих `JAZZ_Mag*` effects/params из `items.lua`. |
| `_cmp_optic_cth.py` | Матрица CTH по архетипам оптики; default `--weapon DragunovSVD` (`*` = слот на пушке). |
| `_audit_long_scopes.py` | Снимок long-scope профилей (данные). |
| `_calib_optic_targets.py` | Старая калибровка рычагов ×1.2 (исторически АКМ). |
| `_rebalance_long_scope_ow.py` | Длинная оптика: `ScopeOverwatchAngle`% уже по кратности (больше зум → уже OW). |
| `_validate_items_quick.py` | Быстрый структурный check `items.lua`/`metadata.lua` (lone commas, braces, stacked closers, **missing comma before PlaceObj**, **raw newline inside quoted strings**, **CheckDifficulty StoreAsTable-false**, UTF-8/Windows-1251 mojibake в metadata, corrupt `id = }),`) **плюс** для пакета `jazz`: intended `Code/*.lua` есть и в `metadata.code`, и как `ModItemCode` (иначе editor resave выкидывает файл). Без JA3. **Обязателен после mass apply / family split / editor SaveDef**. Опционально: `python docs/tools/_validate_items_quick.py [pkg…]`. |
| `_fix_bobbyray_string_tier.py` | Bobby Ray: `Tier = "4"`/`'Tier', "5"` → numeric в `items.lua` + `InventoryItem/*.lua` (иначе `PrepareShopItemsForRestock` Assert string≤number). Dry-run / `--apply`. |
| `_fix_ame_callsign_in_name.py` | AME callsign в `Name`: `Didier Mbemba`+Nick `Smoke` → `Didier "Smoke" Mbemba` / `Дидье "Дым" Мбемба` (vanilla single-quoted `T`). Companions + `jazz-units/items.lua` + RU/EN. Dry-run / `--apply`. |
| `_apply_strategy_021_great_desert.py` | STRATEGY-021: `GreatDesert` Region + PortCacao `LateAwakenMinTier`/Starting* =0 в `jazz/items.lua` + metadata resource. |
| `_apply_mountain_steppe_region.py` | Trim GreatDesert (drop A9–A12/B9–B12/C8–C12) + add `MountainSteppe` / D18; metadata resource. |
| `_fix_savanna_west_from_steppe.py` | Owner fix: restore A9–A12/B9–B12/C8–C12 to `GreatDesert`; MountainSteppe from A13…; drop D11–D12 overlap. |
| `_add_great_desert_sectors.py` | Append sectors to `GreatDesert` (overlap check vs other Regions). |
| `_apply_fleatown_environs_region.py` | Add `FleatownEnvirons` / H19; drop F18 from MountainSteppe (overlap). |
| `_apply_labarrier_region.py` | Add `LaBarrier` / L15 + Ernie `MajorSupplyPriority`; wire L15 Global AI lists. |
| `_apply_great_forest_region.py` | Add `GreatForest` / G22+K21 shared dual-outpost; wire Global AI lists. |
| `_verify_late_awaken_regions.py` | Print `LateAwakenMinTier` / `LegionAIEnabled` per authored Region in `jazz/items.lua`. |
| `_restore_ernie_sectors.py` | Restore `ErnieIsland.Sectors` from `HEAD` (keeps `MajorSupplyPriority`). |
| `_fix_metadata_last_changes_and_audit_code.py` | HOTFIX-001: чинит raw newline в `metadata.lua` `last_changes` (иначе local mod не грузится → Steam packed); аудитит все `metadata.code` пути vs disk/git (missing/case). |
| `_append_imp001_loc.py` | JAZZ-IMP-001: RU/EN строки `890000000001931–936` (Russian.csv: Translation=RU; English.csv: Translation=EN). |
| `_append_close_range_rollover_loc.py` | CloseRange card-row values RU/EN `890000000001937–938` (`+N (tiles)` / `−N% (tiles)`); label = `982641736210`. |
| `_upsert_grizzly_perk_loc.py` | JAZZ-WEAPONS-012: upsert `272740235755` GrizzlyPerk Description RU/EN (signature ignores unsupported penalties). |
| `_bump_close_range_stg_anchor.py` | Scale Firearm `CloseRange` by StG-44 anchor (6→8, ×4/3 tiers: 2→3, 4→5, 6→8, 8→11, 12→16); companions + `items.lua` + `BASE_CLOSE_RANGE`. Dry-run / `--apply`; idempotent if STG already 8. |
| `_check_imp_certificate_fix.py` | Static: IMP loc Translation columns + Sniper `Perk-Specialization` + Veteran `OldDog` + personal wrap. |
| `_insert_imp_personality_perks.py` | JAZZ-IMP-001: вставляет `Jazz_Perk_{Mimicry,Veteran,Sniper}` в Personality-папку `items.lua`. |
| `_check_imp_perk_items.py` | Проверяет наличие трёх IMP Personality ModItems и Icon. |
| `_ensure_imp001_metadata.py` | Гарантирует code/CharacterEffect/ModResourcePreset записи IMP-001 в `metadata.lua` + revision bump. |
| `_bump_units_imp001_meta.py` | Bump `jazz-units/metadata.lua` Revision после placeholder `IMP_equipment_basic`. |
| `_list_perk_icons.py` | Список vanilla CharacterEffect Icon paths (для подбора IMP perk icons). |
| `_audit_imp001_ids.py` | JAZZ-IMP-001: static audit class IDs (оружие/перки/расходники) в jazz+jazz-units. |
| `_bump_imp001_fix_meta.py` | Revision bump + last_changes bullet после hotfix Sniper/LMG. |
| `_bump_metadata_for_commit.py` | Универсальный Revision +1 и prepend `last_changes` bullet (literal `\\n` only). `--path` для sibling packages. |
| `_audit_region_descriptions.py` | Печатает DisplayName/Description_len для mainland Region presets в `items.lua` (Ernie/PortCacao/…). |
| `_bump_suite_018.py` | One-shot: suite display → `0.18` (`version_minor` 18, rev 6015), title `v0.18`, prepend `last_changes` (literal `\\n` only). |
| `_wire_med001_traumas.py` | MED-001: генерирует `Trauma*` CharacterEffect companions + inserts ModItems/metadata; патчит `*shot` / `Unconscious` / `Burning` → trauma API. |
| `_append_med001_trauma_loc.py` | MED-001: дописывает RU/EN строки `890000000009226`–`009255` для Trauma* DisplayName/Description. |
| `_lupa_load_items.py` | Реальный Lua parse `items.lua`/`metadata.lua` через lupa (stubs PlaceObj/T). Ловит syntax как игра. |
| `_audit_items_structure.py` | Аудит: `})` без `,` перед `PlaceObj`, PlaceObj@col0, brace depth. |
| `_fix_maglarge_50_ak_remnant.py` | Удалить битый remnant `MagLarge_50_AK` (`id = }),`). `--apply`. |
| `_strip_lone_commas.py` | Только вырезать lone-comma строки из `items.lua`/`metadata.lua` (артефакт insert). Атомарная запись через `.tmp`. |
| `_rename_mag_hyphen_ids.py` | Public id MagBelt/MagDrum: `-` → `_` (DefineClass-safe). items/metadata/companions/CSV. `--apply`. |
| `_clean_broken_comp_ids.py` | Убрать битые `DefaultComponent`/`AvailableComponents` (`su`, пустые/multiline id). |
| `_attach_classify.py` | Классификатор comps/effects (`live` / `legacy_handling` / …) для catalog/audits. |
| `_audit_attach_ids.py` | Audit: prefix `JAZZ_`, Mount, unused comps (читает CSV). |
| `_audit_attach_effects.py` | Audit: Handling/orphan effect presets (читает CSV + `items.lua`). |
| `_audit_attachment_icons.py` | Audit `Icon`/`ChipIcon` vs disk: wired / need-wire / need-generate; пишет `_audit_attachment_icons_report.txt`. |
| `_audit_component_icon.py` | Audit только `WeaponComponent.Icon` (кабинет ModifyWeaponDlg): missing / vanilla / `WeaponComponents/` / Full; `_audit_component_icon_report.txt`. |
| `_audit_unique_entity_icons.py` | Unique Entity-set vs shared Icon backlog (style B). Scope/Magazine priority; barrels optional. |
| `_finalize_icon_style_b.py` | Style B Icon: magenta/rembg cut (incl. enclosed cutouts) → heal → Anaconda soft edge → 100×100. Canon: `WeaponComponents/references/PROMPT.md`. |
| `_punch_enclosed_dark_holes.py` | Punch closed near-black fills inside skeleton stocks (triangle/trapezoid cutouts). |
| `_apply_fix_batch_icons.py` | Fix-batch: FAMAS/SIG/G36/SVT/AUG42/AR10 finalize + M72 WeaponIcon. |
| `_audit_icon_crosswire.py` | Проверка: content-dup PNG, cross-family ApplyTo, orphan Sig UnFolded, SVT/AVT map. |
| `_qa_icon_style_b.py` | QA preview Icon: size/opaque/soft-AA/corners/bright-fringe. Fail → regen. |
| `_wire_ak74_mag_icons.py` | MagNormal/MagLarge_30_45 ApplyTo AK74+RPK74+AKSU+AN94 → `AK74_Mag30` / `AK74_Mag45_long`; MagQuick_AK AN94 → Mag30. |
| `_wire_g36_mag_icons.py` | MagNormal ApplyTo G36 + G36c → `Magazine/G36_Mag30.png`. |
| `_wire_g36_stock_icons.py` | StockNormal ApplyTo G36 → `Stock/G36_Stock_Normal.png` (базовый скелетный). |
| `_wire_vss_val_mag_icons.py` | MagNormal VSS/AS_Val → VSS_Mag10; MagLarge_10_20_VAL → VSS_Mag20. |
| `_wire_sig_icons.py` | MagNormal Sig550/Custom/552/SWAT → Sig_Mag30; SigDefHandGuard + SigErgoHandGrip Icons. |
| `_wire_sig_stock_icons.py` | SIG Stock Folded/UnFolded/Heavy Style B; fix Sig550Custom/Sig552 DefaultComponent → StockLightUnFolded. |
| `_fix_ak_mag_caliber_options.py` | AK 7.62 vs 5.45: `MagLarge_30_40`/drum только на АКМ/АК47/…; `MagLarge_30_45` только на АК74/…. Companions+items. `--apply`. |
| `_hide_fold_only_stock_slots.py` | `Modifiable=false` на Stock, если options только `StockLightFolded`+`StockLightUnFolded`. Companions + `items.lua`. `--apply`. |
| `_strip_freeswap_wiki.py` | После strip: убрать Freeswap из `docs/wiki/weapons/*` по CSV options; оставить MP5K/MicroUZI/Scorpion; обновить count в `components.md`. |
| `_wire_ak74_stock_icon.py` | Wire `JAZZ_StockNormal` ApplyTo=AK74 → `WeaponComponents/Stock/AK74_StockNormal.png`. |
| `_wire_ak74_stock_fold_icon.py` | Wire AK74 fold stock on UnFolded/Folded/StockLight/UnfoldStocks → `AK74_StockFold_v2.png` (folded shares art until distinct). |
| `_wire_akm_stock_icons.py` | Wire AKM wood `StockNormal` + underfolder Folded/UnFolded/UnfoldStocks → `AKM_StockNormal/Fold.png`. |
| `_wire_mag_762_vanilla.py` | MagNormal 7.62 (AK47/AKM/RPK/Type56/Zastava_M70/ZastavaM92) → vanilla `UI/Icons/Upgrades/AK47_magazine`. |
| `_wire_stanag_mag_icons.py` | CAR15/M4/M16/AR15: MagNormal+MagSmall30_20 → `m16_magazine`; MagQuick gaps → `quick_STANAG_magazine`. |
| `_wire_p210_ironsight.py` | `JAZZ_IronSight` ApplyTo=P210 → vanilla `UI/Icons/Upgrades/ironsights`. |
| `_wire_p210_ironsight_aim.py` | `JAZZ_IronSight_AIM` P210 → `Optics/P210_IronSight_AIM.png`; comp Icon `ironsights_hands`. |
| `_wire_p210_handgrip_default.py` | `JAZZ_Handgrip_Default` ApplyTo=P210 → `Handgrip/P210_Handgrip_Default.png`. |
| `_wire_p210_handgrip_ergo.py` | `JAZZ_Handgrip_Ergo` ApplyTo=P210 → `Handgrip/P210_Handgrip_Ergo.png`. |
| `_wire_1911_mag_icons.py` | MagNormal Colt1911 (+Kimber) → `Magazine/Colt1911_MagNormal.png` (style B). |
| `_wire_p220_mag_icons.py` | MagNormal P220 → `P220_Mag8.png`; MagLarge_8_10 → `P220_Mag10.png`. |
| `_wire_kimber_mag_icons.py` | MagLarge_7_10 ApplyTo Kimber → `Magazine/Kimber_Mag10.png`. |
| `_wire_p226_mag_icons.py` | MagNormal P226 → `P226_Mag15.png`; MagLarge_18_20 → `P226_Mag20.png`. |
| `_wire_p226_handgrip_icons.py` | Handgrip Default/Ergo ApplyTo P226 → `Handgrip/P226_Handgrip_*.png`. |
| `_wire_p226_ironsight.py` | `JAZZ_IronSight` ApplyTo P226 (rear) → `Optics/P226_IronSight.png`. |
| `_wire_p226_ironsight_aim.py` | `JAZZ_IronSight_AIM` ApplyTo P226 → `Optics/P226_IronSight_AIM.png`. |
| `_wire_p226_ironsight_fast.py` | `JAZZ_IronSight_FAST` ApplyTo P226 → `Optics/P226_IronSight_FAST.png`. |
| `_wire_p226_ironsight_night.py` | `JAZZ_IronSight_NIGHT` ApplyTo P226 → `Optics/P226_IronSight_NIGHT.png`. |
| `_wire_fiveseven_mag_icons.py` | MagNormal ApplyTo FiveSeven → `Magazine/FiveSeven_Mag20.png` (slot later). |
| `_wire_barrel_normal_icons.py` | `JAZZ_BarrelNormal` Icon Style B + ChipIcon (was empty Chip / vanilla default_barrel). |
| `_wire_scorpion_icons.py` | MagNormal + StockLight Folded/UnFolded ApplyTo Scorpion → Mag20/Stock PNG. |
| `_wire_mac10_icons.py` | MagNormal + StockLight Folded/UnFolded ApplyTo MAC10 → Mag30/Stock PNG. |
| `_wire_aps_icons.py` | MagNormal APS → Mag18; BarrelNormal_Sil → APS_BarrelSil (comp Icon too). |
| `_wire_mat49_mag_icons.py` | MagNormal ApplyTo MAT49 → `Magazine/MAT49_Mag32.png`. |
| `_wire_mp40_mag_icons.py` | MagNormal ApplyTo MP40 → `Magazine/MP40_Mag32.png` (was magpictures). |
| `_wire_m3_mag_icons.py` | MagNormal ApplyTo M3GreaseGun → `Magazine/M3_Mag30.png` (no Mag slot yet). |
| `_wire_sterling_mag_icons.py` | MagNormal ApplyTo Sterling → `Magazine/Sterling_Mag34.png` (no Mag slot yet). |
| `_wire_stg44_mag_icons.py` | MagNormal ApplyTo STG44 → `Magazine/STG44_Mag30.png` (no Mag slot; mag in mesh). |
| `_wire_thompson_mag_icons.py` | MagNormal Thompson → Mag30; MagDrum_30_50_THOMPSON → MagDrum. |
| `_wire_pps43_mag_icons.py` | MagNormal ApplyTo PPS43 → `Magazine/PPS43_Mag35.png` (no Mag slot yet). |
| `_wire_mpl_mag_icons.py` | MagNormal ApplyTo MPL → `Magazine/MPL_Mag30.png`. |
| `_wire_m45_mag_icons.py` | MagNormal ApplyTo M45 (Carl Gustaf) → `Magazine/M45_Mag32.png`. |
| `_wire_agram_mag_icons.py` | MagNormal ApplyTo Agram2000 → `Magazine/Agram_Mag32.png`. |
| `_wire_famas_mag_icons.py` | MagNormal ApplyTo FAMAS → `Magazine/FAMAS_Mag25.png` (прямой F1). |
| `_wire_fg42_mag_icons.py` | MagNormal ApplyTo FG42 → `Magazine/FG42_Mag20.png` (no Mag slot; mag in mesh). |
| `_wire_svt_mag_icons.py` | MagNormal: SVT40→`SVT_Mag10`; AVT40→`SVT_MagLarge`. |
| `_wire_ar10_mag_icons.py` | MagNormal Visual AR10+AR10DMR → `Magazine/AR10_Mag20.png` (no Mag slot). |
| `_wire_m72law_icon.py` | M72LAW InventoryItem Icon → `WeaponIcons/M72LAW.png`. |
| `_wire_aug_mag_icons.py` | AUG MagNormal→Mag30; MagLarge_30_42→Mag42; MagQuick_AUG→MagQuick (+ remountable Inv Icons). |
| `_wire_hk33_icons.py` | HK33 Mag30/MagDrum + Handguards Style B; fix default HG Entity `HK33_HandGuardStock` (был `HK_33_Lower`). |
| `_wire_m16a2_handguard_icons.py` | JAZZ_Handguard ApplyTo M16A2 → `Handguard/M16A2_Handguard.png` (A2 ribbed). |
| `_wire_m1garand_enbloc_icons.py` | MagNormal ApplyTo M1Garand → `Magazine/M1Garand_Enbloc.png` (обойма; no Mag slot). |
| `_wire_uzi_icons.py` | MagDrum_30_50_UZI → UZI_MagDrum; StockLight Folded/UnFolded UZI → UZI_Stock. |
| `_wire_mp5_mag_icons.py` | MagNormal → MP5_Mag30; MagSmall30_15_MP5 → MP5_Mag15 на MP5/MP5K/MP5A2/MP5A4/MP5SD (+ ApplyTo MP5). |
| `_wire_berettam12_mag_icons.py` | MagNormal ApplyTo BerettaM12 → `Magazine/BerettaM12_Mag32.png`. |
| `_wire_spectrem4_mag_icons.py` | MagNormal ApplyTo SpectreM4 → `Magazine/SpectreM4_Mag50.png`. |
| `_wire_tmp_icons.py` | MagNormal/MagSmall30_15_TMP → TMP Mag30/Mag15; HolsterBelt Icon (был битый `belt.png`) + TMP Visual. |
| `_wire_holsterbelt_m16_icon.py` | HolsterBelt ApplyTo M16A1 Visual Icon (пустое General без ghost, если Icon только на компоненте). |
| `_wire_ump45_mag_icons.py` | MagNormal ApplyTo UMP45 → `Magazine/UMP45_Mag25.png` (insert Visual). |
| `_wire_p90_mag_icons.py` | MagNormal ApplyTo P90 → `Magazine/P90_Mag50.png`. |
| `_wire_mp7_mag_icons.py` | MagNormal ApplyTo MP7 → `Magazine/MP7_Mag30.png`. |
| `_wire_mini14_mag_icons.py` | MagNormal → Mini14_Mag20; MagLarge_20_30_MINI14 → Mini14_Mag30. |
| `_enable_remountable_bobby_ray.py` | Временный shop-pass: `CanAppearInShop` + Restock/MaxStock/Tier на remountable InventoryItems (dry-run / `--apply`). |
| `_apply_bobby_catalog.py` | ECON-004: apply Cost/Tier/RW/CAS/CategoryPair из `.tmp/bobby_*_prices.json` в companions + `items.lua`. `--dry-run` / `--apply`. |
| `_patch_bobby_econ004_items.py` | ECON-004: ModItemCode + Other SubCategories (Optics/…) + `TCE_Tier4/5Unlock` в `items.lua`. Idempotent. |
| `_audit_bobby_weapon_prices.py` | Аудит `Cost` active оружия (`weapons.csv` + GL/RL). `proposed` = канон `InventoryItem.Cost` для **Bobby и world** buy/sell; `shop=out_*` только вне витрины. `--json` / `--tsv`. |
| `_annotate_bobby_cas.py` | К `.tmp/bobby_weapon_prices.json` добавляет `cas_action`/`cas_label` (нужен ли `CanAppearInShop=false`). |
| `_gen_bobby_price_canvas.py` | Сборка canvas `bobby-ray-weapon-prices.canvas.tsx` из `.tmp/bobby_weapon_prices.json`. |
| `_audit_bobby_armor_prices.py` | Аудит брони: JazzArmor + plates + NVG/GasMask; `out_legion` (импровиз/рейдер), `out_special`, stubs. BR 1–5 + proposed Cost. `--json` / `--tsv`. |
| `_audit_bobby_ammo_prices.py` | Аудит `JAZZ_AMMO_*` + Flare: BR 1–5 по grade×caliber; out_craft/mortar/antique/dupe. `proposed` = stack Cost. `--json` / `--tsv`. |
| `_gen_bobby_ammo_canvas.py` | Сборка canvas `bobby-ray-ammo-prices.canvas.tsx` из `.tmp/bobby_ammo_prices.json`. |
| `_audit_bobby_consumables_prices.py` | Аудит медицины / инструментов / Meds·Parts: flat staples; specialty Surgical/Stim/Metaviron soft-tail. `--json` / `--tsv`. |
| `_audit_bobby_attach_prices.py` | Аудит remountable аттачей: Optics BR из design tiers; Mag/Muzzle/Side/Under heuristic; Cost=Parts×100; out integral/GL/irons. `--json` / `--tsv`. |
| `_gen_bobby_attach_canvas.py` | Сборка canvas `bobby-ray-attach-prices.canvas.tsx` из `.tmp/bobby_attach_prices.json`. |
| `_audit_bobby_explosive_prices.py` | Аудит TNT/C4/PETN + fused + grenades/demo/Warhead: soft-tail BR; cross BlackPowder/40mm/mortar. `--json` / `--tsv`. |
| `_gen_bobby_explosive_canvas.py` | Сборка canvas `bobby-ray-explosive-prices.canvas.tsx` из `.tmp/bobby_explosive_prices.json`. |
| `_audit_chip_palette.py` | Палитра/размер `Icons/Upgrades/Chips/JAZZ_*.png` (sanity для generation). |
| `_write_attach_design_human.py` | Пересбор `docs/design/attachments-by-category.md` из CSV. |
| `_build_attachments_catalog.py` | HTML-каталог `docs/tools/attachments-catalog.html`. |
| `_attach_live_summary.py` | JSON-сводка live comps (вспомогательный). |
| `_export_merc_salary_json.py` | Roster зарплат: vanilla AIM (`IsMercenary`) + Jazz/AME из `jazz-units` → `merc-salary-data.json` (Affiliation из `items.lua`). Нужен `JA3_ROOT`/ModTools для vanilla. |
| `_gen_merc_salary_calculator.py` | HTML-калькулятор `merc-salary-calculator.html`: `GetMercPrice` / daily / medical / duration discount (JAZZ maxDay=30) / squad sum. |

Типичный post-migrate конвейер:

```text
python docs/tools/_apply_attach_001.py --apply   # если ещё не применено
# python docs/tools/_promote_vanilla_refs.py   # только осознанно; иначе vanilla_ref OK
python docs/tools/_remove_handling_stat.py       # если нужно снять stat Handling
python docs/tools/_fix_items_lone_commas.py    # если после delete остались lone commas / stubs
python docs/tools/_export_attach_csv.py
python docs/tools/_audit_attach_ids.py
python docs/tools/_audit_attach_effects.py
python docs/tools/_write_attach_design_human.py
python docs/tools/_build_attachments_catalog.py
```

Официальный CSV import через Node (нужен установленный JA3):

```text
$env:JA3_ROOT = '<JA3 install>'
node scripts/docs/weapons-docs.mjs import --force
```

Без `JA3_ROOT` использовать `_export_attach_csv.py`.

## Карта / сектора jazz-maps

| Скрипт | Назначение |
| --- | --- |
| `export-jazz-maps-sectors.py` | Парсит `ModItemSector` из `../jazz-maps/items.lua` (+ index `metadata.lua`); пишет `sectors-runtime.json/.csv` в `docs/technical/maps/data/`. **Не** обходит `Maps/`. `--maps-root` на диск: папка `JAZZ Maps`. |
| `build-sector-atlas-docs.py` | Собирает атлас / трансфер / сверку sheet↔runtime (MD+CSV) из runtime JSON + снимка Google Sheet «Карта». |
| `jazz-maps/docs/tools/_extract_vanilla_map_hpk.py` | Распаковка `Packs/Maps/<id>.hpk` в `Maps/<hash>/` (аналог editor `CopyMapFiles`). После копии — свой `mapdata.lua` с `id`/`ModMapPath`. |

```text
python docs/tools/export-jazz-maps-sectors.py
python docs/tools/build-sector-atlas-docs.py
```

Выход: `docs/technical/maps/sector-atlas.md`, `sector-transfer.md`, `sector-sheet-vs-runtime.md` и CSV в `docs/technical/maps/data/`.

## Прочие утилиты баланса / accuracy

| Скрипт | Назначение |
| --- | --- |
| `_soft_nerf_smg_aa.py` | Точечный nerf SMG AimAccuracy |
| `_apply_tier_acc_buffs.py` | Tier accuracy buffs |
| `_build_accuracy_html.py` | HTML по accuracy-модели |
| `_apply_buckshot_projectiles.py` | JAZZ-WEAPONS-006: `BuckshotProjectiles=1` на SG, ammo `target_prop` → `BuckshotProjectiles`, CombatAction/CSV; Auto/Burst снова 0. `--apply`. |
| `_verify_buckshot_projectiles.py` | Static AC-001..003 для WEAPONS-006. Exit 1 при FAIL. |
| `_fix_shotgun_pellet_autoshots.py` | **Superseded by 006** — старый hotfix AutoShots=1; не использовать. |
| `_rebalance_recoil_physical.py` | JAZZ-WEAPONS-003/008: mass/RPM/size/limiter → Recoil/Burst/Auto; SMG floor 12; Carbine + select-fire sniper rpm holefix; G36 lim=2; M16A2/A4/FAMAS/AUG/HK33/Sig550*/G3 lim=3; M2Carbine component-gated JAZZ_Autofire shot counts; token-safe attack match. `--apply` → `.bak`. |
| `_audit_weapons_rpm_holes.py` | WEAPONS-003 hole scan: select-fire/`MGBurst` with `cyclic_rpm=0`, Auto/Burst=0 with mode, known BurstLimiter drift, CSV↔companion, SMG mass/Long placeholders, spec anchors. |
| `_soften_ammo_jam.py` | JAZZ-WEAPONS-008: смягчает Poor/Crafted `BaseJamChance`/`Reliability` в `items.lua` + companions. `--apply`. Исторический маппинг; актуальный Crafted band — `_apply_crafted_jam_band.py`. |
| `_apply_crafted_jam_band.py` | Owner 2026-08-23: все `*_Crafted` Rel −3 / jam +40 (хуже FMJ, лучше Poor). `items.lua` + companions. `--apply`. |
| `_audit_weapon_jam_balance.py` | JAZZ-WEAPONS-010 static audit: soft-stack wear, quadratic −5pp service softener at 100%, softer mid steps, Rel 5..95, MP40 0/2/7/100, Mosin mid 8%/17% capped; Poor/Crafted ≤5% at perfect resource. |
| `_patch_jam_reliability_score.py` | Rewrite `JazzGetBaseJamScore` in `System_OR_Weapons.lua` (Rel clamp + Rel95 zero + scaled BaseJamChance); writes `.jamrel.new` then replaces when the game unlocks the file. |
| `_tmp_audit_smg_jam_feedback.py` | Discord audit: SMG Recoil distribution + Poor/Crafted JamScore scenarios. |
| `_audit_recoil_dist.py` | Static AC audit полей active firearms, recoil anchors, 9×19 differentiation и M16A2/AN94 limiters. |
| `_fix_madman_salary.py` | Jazz_Madman: `StartingSalary`/`SalaryLv1`/`SalaryMaxLv` в `jazz-units/items.lua` (companion править отдельно). |
| `_fix_free_merc_salaries.py` | Jazz_Grom / Jazz_Hitman: paid hire salaries в companion + `jazz-units/items.lua`. |
| `_sync_grom_rehire_chat.py` | Гром RehireIntro: убрать «бесплатный» из `items.lua` + `Russian.csv`. |
| `_sync_madman_chat_salary_strings.py` | Синк AIM-фраз Бешеного (не «бесплатный») в `items.lua` + `Russian.csv`/`English.csv`. |
| `_ship_colby_voices_ja2_only.py` | Jazz_Colby: пересобрать `jazz-units/voices/<T-id>.opus` **только** из JA2 Trevor WAV (`trevor.rar` / `trevor_extract/trevor`); пробелы — дубли родственных реплик. `--dry-run` / apply. |
| `_ship_ja2_merc_voices.py` | Batch: JA2/NightOps/JA2 Gold SLF + folder packs **или** `ja2mercs:…`. Combat=`SLOT_WAV`; AIM chat via `--aim-chat` / `--aim-chat-only`: classic `081–120`, MERK/RPC/Biff=`HIRE_FALLBACK_WAV`, UB ЦС=`UB_HIRE_PROXY_WAV`, Mike hire alt OLD pack. Never ATTN as hire. Map: `jazz_to_ja2_profile.csv` + folders CSV. **Never overwrite** `done_manual`: `spouke` / `lynx` / `tosca` / `spider`. |
| `_restore_lynx_tosca_spider_voices.py` | Restore original JA3 opus for `Jazz_Lynx` / `Jazz_Buzz` / `Jazz_Spider` from pre-remesh commit `a626ebc` (after accidental overwrite in `792d1c5`). Spouke untouched. |
| `_gen_ame_roster_60.py` | Генерация design-карточек AME: `docs/design/ame-roster-60.md`. Voice pool: Jazz remesh majority + `PierreMerc` + IMP minority (~1/8; VR → `IMP_*_01`). Assert: line troops = AllRounder/Autoriflemen/HeavyWeapons/Marksmen; soft specs только у Specialists. Sparse personality map **12/60**. |
| `_apply_ame_personality_traits.py` | Пишет Personality-tier perk (~12/60) в `jazz-units` UnitData companions + `items.lua`, сохраняя common traits. Dry-run / `--apply`. |
| `_verify_ame_personality.py` | Static assert: ровно 12 AME companions + items.lua содержат mapped Personality. |
| `_bump_metadata_last_changes.py` | Commit helper: `version` +1 and prepend `last_changes` bullet with escaped `\\n` (no raw LF). Args: metadata path, bullet, optional `--version-minor`. |
| `_ame_copy_bank.py` | Importable канон 60 самостоятельных RU+EN биографий и двуязычных profile blurbs; сам ничего не пишет. |
| `_export_ame_bio_copy_edits.py` | Проецирует 60 AME biography ID из copy-bank в `localization-copy-edits/ame_bios_bilingual.csv` для безопасного обновления обеих manual memories. |
| `_patch_ame_specializations.py` | Синхронизирует `Specialization` в `jazz-units/UnitData/JAZZ_AME_*.lua` + `items.lua` из roster generator **без** перезаписи зарплат/loc. |
| `_apply_ame_voice_remap.py` | Патчит только `VoiceResponseId`/`FallbackMissingVR` в `jazz-units` UnitData companions + `items.lua` из `voice_for()` roster (без regen bios/kits). |
| `_audit_ame_voices.py` | Аудит `VoiceResponseId` по 60 UnitData + 114 generated T/audio: opus exists, managed Context-ID set точно совпадает с items, без faction slogans, EN совпадает с audible donor phrase, RU — с `_ame_voice_subtitles_ru.py`. |
| `_audit_ame_copy.py` | Проверяет 60 самостоятельных RU/EN биографий и profile blurbs: 3–4 предложения, 38–105 слов, без stat/tier/meta copy и повторов; сверяет точную проекцию в roster, а с `--generated` ещё runtime CSV и `jazz-units/UnitData`. |
| `_verify_ame_voice_items_sync.py` | Сверка AME VR в `items.lua` vs companions. |
| `_ame_names_ru.py` | RU Name/Nick для AME (кириллица); используется `_gen_ame_unitdata.py` в RU/EN loc. |
| `_gen_ame_unitdata.py` | JAZZ-UNITS-005: из roster → `jazz-units/UnitData/JAZZ_AME_01..60.lua`, fixed `Loot_*`, items/metadata markers, nationality presets, RU/EN loc (имена RU из `_ame_names_ru.py`), placeholder portraits. Idempotent (`JAZZ-UNITS-005-AME-*`). |
| `_test_ame_contract.py` | Targeted lupa-harness для реальных AME Lua: синтаксис, детерминированное окно ровно 15 кандидатов, отдельная soft-guarantee Medic/Instructor/Sniper, защита нанятых, AME-only `My Team`, idempotent mail wrapper и обязательные поля сайта. Read-only; live PDA acceptance не заменяет. |
| `_apply_ame_weekly_salaries.py` | Playtest salary ladder: weekly bands → `StartingSalary` (week≈×7); writes all `UnitData/JAZZ_AME_*.lua`. Ceiling below Igor/Barry daily. |
| `_sync_ame_salary_items.py` | Copies companion `StartingSalary` into `jazz-units/items.lua` ModItem `'Id',"JAZZ_AME_NN"` blocks. |
| `_import_legion_raider_alt_voices.py` | Импорт Legion Raider alt takes `*-1.opus` (rar или `--dir Downloads/1`) → `jazz-units/voices/` (донор голоса для AME Male_Low). |
| `_ame_voice_subtitles_ru.py` | Канонический RU-перевод фактически слышимой donor-фразы для shared AME voice banks; не подменяет реплику текстом gameplay event. Неизвестная новая фраза — hard fail генератора. |
| `_gen_ame_voice_responses.py` | Три shared VR: `Jazz_AME_Male_Low` (Legion alt `*-1.opus`, без Legion/Major/Grand Chien takes), `Jazz_AME_Male_Hard`, `Jazz_AME_Female`. Remesh только подходящие слоты; Selection/Order/CombatMovement **omit** → тишина. EN совпадает с audio, RU берётся из `_ame_voice_subtitles_ru.py`; generated loc принадлежит стабильному Context и переиспользует те же IDs даже после CSV round-trip без comment markers. |
| `_gen_ame_appearances.py` | 60 `JAZZ_AME_NN` full regen from **vanilla** AP only; **1** синий акцент; Af head bank; без Legion war-paint / `GrandChien_Top_05`; red/extra-blue→slate; map `ame-appearance-map.json`. Policy: `docs/design/ame-appearance-assets.md`. |
| `_patch_ame_appearance_clothes_from_map.py` | Clothing shuffle from map: jazz-units **canon `Legion*`** + Rebels/GC/keep; preserve Head/BodyC1/HeadColor; strip helmets/turbans/balaclavas/`Equipment*_Hat`; ~12 male **berets** (earth, never blue); blue accent on non-camo Shirt/Chest/Armor/BodyC2/scarf — **not** Hat, **not** Hip pouches; camo earth + Recon chest carrier; ♀ `NPCFemale_Hair_*` or empty if Hat/Hat2. `--dry-run` / `--write-map-only`. Do **not** replace with bare `_gen_ame_appearances.py` (wipes jazz clothing). |
| `_audit_ame_appearance_clothes_qa.py` | Static QA: Irregular jazz `Legion*` lean; no war-paint/AIM hair/hat+hair/helmets/balaclavas/blue hips; beret count. |
| `_list_jazz_legion_appearances.py` | List handcrafted jazz-units `Legion*` AppearancePreset ids (canon pool). |
| `_audit_patch_ame_heads.py` | Repair pass по `jazz-units/items.lua` AME: pale/AIM heads, ♀-on-♂, war-paint bodies, pale-hand `GrandChien_Top_05`, gloves Shirt, BodyColor C1, HeadColor 0. `--dry-run` / `--sync-map` / `--verbose`. Exit 0 ⇒ `bad_after=0`. |
| `_audit_loot_upgrade_ids.py` | Audit `LootEntryUpgradedWeapon` upgrade IDs in `jazz-units/items.lua` vs known `JAZZ_*` WeaponComponent map. |
| `_apply_loot_upgrade_id_remap.py` | Remap legacy vanilla upgrade IDs on loot entries to `JAZZ_*` companions (dry-run default). |
| `_emit_ame_live_patch.py` | Emit pasteable live-Lua AppearancePreset patches for in-session AME head/body repair. |
| `_gen_ja12_appearances.py` | JAZZ-UNITS-002: same-gender mixes from BigPortrait cues. Prefer **faction/NPC body + head**, or AIM clone; **warn on AIM×AIM**. Skips `KEEP_HANDCRAFTED` (Lynx/Buzz/Spider/JAZZ_Spouke/Ivanov + vanilla Biff/Hitman/Simon→Shadow) unless `--force`. Map `ja12-appearance-map.json`. |
| `_purge_ja12_app_dupes.py` | Removes listed `ModItemAppearancePreset` ids that appear **before** `JAZZ-UNITS-002-JA12-APP` (avoid duplicate Mike/Horg when moving into generated folder). |
| `_list_appearance_donors.py` | Каталог donor AppearancePreset по категории/полу (для подбора JA12 recipes). |
| (manual) `_appearance-preset-rules.md` | WIP rules: gender lock (♂/♀ skeletons incompatible), recipe shape, index; visual slots in `_appearance-donor-visual-catalog.md`. |
| (manual) `_appearance-donor-visual-catalog.md` | Working visual catalog: preset id → gender + slots + look (AME browse). Includes **jazz-units** Legion* (through Sniper) + named + merc skins batch7–8 (`*_Savana`/`*_Jungle`/`*_DustStorm`/`*_Hot`/`*_Forest`/`*_Snake`, `Buzz`, `Spider`). Scratch: `.tmp/ame-crops/batch{3…8}_*`. |
| `_audit_ja12_appearance_links.py` | UnitData `AppearancesList` → shipped/vanilla preset ids + gender lock on JA12 section. |
| `_gen_ame_flags.py` | PNG флаги 128×80 для новых AME Nationality (`Icons/Flags/f_*.png`). |
| `_gen_ame_portrait_prompts.py` | JSONL prompt-bank 60 слотов → `jazz-units/MercPortraits/_ame_face_refs/prompts.jsonl`. |
| `_process_ame_portraits.py` | rembg BiRefNet + resize 2000 + bust_crop 300 из `*_Big_raw.png` (assets/_raw). |
| `_append_ame_mail_loc.py` | JAZZ-UI-AME-001: RU/EN Email strings `890000000006900–6910` (welcome + listing update). Idempotent upsert; proper multiline CSV. |
| `_append_merc_mail_loc.py` | JAZZ-UI-MERC-001: RU/EN Speck mail + MERC PDA strings `890000000009900+`. Idempotent upsert; multiline CSV. |
| `_remap_merc_loc_ids.py` | One-shot: move MERC loc off VoiceResponse `007xxx` → `009900+`; restore stolen VR rows from `HEAD`. |
| `_restore_vanilla_aim_vr_ids.py` | Restore vanilla T-IDs for AIM `ModItemVoiceResponse` Raven/Thor/Vicki/Wolf from `bb6d97a^` (LOC remap broke VO). Then run `_purge_restored_aim_vr_loc.py`. Vanilla mercs must keep Game.csv IDs — never remap those phrases to `8900*`. |
| `_purge_restored_aim_vr_loc.py` | After VR id restore: delete orphaned `8900*` rows from jazz + jazz-units CSV by record (multiline-safe), no full CSV rewrite. |
| `_sync_units_vr_loctables.py` | Append missing *mod-only* VR/name IDs to jazz RU/EN; write `jazz-units/Russian.csv` + fill units English loctable. Does **not** copy vanilla Game.csv IDs into JAZZ CSV. |
| `_audit_aim_vr_vanilla_ids.py` | Gate: vanilla-looking `ModItemVoiceResponse` ids (Raven/Thor/Vicki/Wolf and any non-`Jazz_*`) must have `8900=0`. |
| `_apply_merc_affiliations.py` | UI-MERC-001: set `Affiliation = "MERC"` on Jazz shelf/world UnitData companions (+ Larry/Smiley overrides). |
| `_apply_ship_iggy.py` | UNITS-002: ship `Jazz_Iggy` (perk stub, loot clone Grom, UnitData+VR, Appearance, loc RU/EN, metadata bumps). Idempotent. Uses `_grom_snippets/`. |
| `_sync_merc_affiliation_items.py` | Sync same Affiliation into `jazz-units/items.lua` ModItem blocks. |
| `_fork_ame_template_to_merc.py` / `_polish_merc_template.py` | Fork/polish `System_MERC_Browser_Template.lua` from AME skin. |
| `_install_merc_xtemplate_moditem.py` | Install `PDAMERCBrowser` ModItemXTemplate + Emails + metadata code/resource (не Code-load шаблона). |
| `_update_ame_mail_sales_copy.py` | Канонические RU/EN письма AME + естественные listing pitches `6960–6984`; безопасно синхронизирует `AME_Welcome` / `AME_ListingUpdate`, сохраняя English source в `Text` обеих runtime CSV. |
| `_apply_ris_mail_emails.py` | Compatibility wrapper → полный `_apply_ris_editorial.py`; отдельный Phase A mail/copy bank удалён. |
| `_rewrite_ris_legion_briefs.py` | Отдельный канон 11 RU/EN supply briefs по loadout unlock map; loc IDs `11300…11321`. CLI делегирует полному `_apply_ris_editorial.py`, чтобы старый partial-run не рассинхронизировал CSV/catalog/items. |
| `_gen_legion_weapon_availability_map.py` | Build `docs/design/legion-weapon-availability-by-tier.md` from `weapons.csv` `tier_label` (11…33). |
| `_compose_legion_unit_portraits.py` | Compose 38 Legion unit Portrait PNGs (transparent 300×300, red-only): family mark inside shield at top-center, unified single-silhouette role glyph below it, tier dots under tip. Catalog + sheet/PSD masters → `jazz-units/EnemyPortraits/Legion/`. |
| `_audit_legion_unit_portraits.py` | Static + visual QA of all 38 portraits: alpha/color/slots/pip count/100px readability/duplicate types; writes design preview, `xN` overlay preview and QA report. |
| `_wire_legion_unit_portraits.py` | Set `Portrait` on all `JAZZ_Legion_*` UnitData companions + matching `items.lua` blocks to `Mod/Dv3mFVN/EnemyPortraits/Legion/<File>.png`. |
| `_dispatch_discord_player_update.ps1` | После agent `git push` в `main`: поллит до 90с; Discord run на SHA уже есть → exit. **Один пост на логическую фичу** (primary пакет); sibling с `[skip discord]`. `-SuitePackages` — список пакетов в Discord «Пакеты». `-SuiteVersions jazz:0.20-6206,jazz-units:0.19-2326` — полные engine-версии (если пусто, читает локальные `metadata.lua`). `-Force`/`-AlwaysDispatch` только для явной перепубликации одного диапазона — не на все репы suite. |
| `_ris_copy_bank.py` | Единственный importable RU+EN канон R.I.S.: identity/sender 3, welcome 3, UI 13, AAR 60, field mail 7, 38+4 досье, 9 Strategy mails (`11322…11339`) и 8 support strings (`11340…11347`); сам ничего не пишет. |
| `_ris_dossier_copy.py` | Compatibility facade: только переэкспортирует public bank из `_ris_copy_bank.py`, собственной прозы не содержит. |
| `_apply_ris_editorial.py` | Канонический generated apply JAZZ-UI-RIS-002: Content Lua, 24 Email, ровно 9 Strategy metadata resources (старые `LegionTier1…5` удаляются), RU/EN runtime CSV, Strings и обе manual memory. Default = dry-run; `--check` возвращает 1 при drift; запись только с `--apply`; повторный apply идемпотентен. |
| `_apply_ris_dossier_copy.py` | Compatibility wrapper → полный `_apply_ris_editorial.py`; отдельной прозы и partial-write больше нет. |
| `_audit_ris_copy.py` | Read-only editorial audit: все категории и 218 RU/EN IDs, включая identity/sender, contiguous AAR 60 / field mail 7, 11 briefs, exact placeholders/signatures/reserved range, factual retired-phrase guards, CSV writer orientation, per-row review coverage и exact 9 Strategy texts vs design. `python -B docs/tools/_audit_ris_copy.py`; stdout + exit 0/1, файлов не пишет. |
| `_test_ris_contract.py` | Targeted lupa-harness для реальных R.I.S. Lua: синтаксис пяти loaded-файлов, Strategy observability/Awakening и inbox gate, engine-like old-save mail migration, delivery-gated dossiers, concurrent auto-resolve, двухфазный tactical snapshot с quest params/named fate, late `UnitMarker` spawn / unseen corpse AAR и legacy AAR reconstruction. Read-only; live JA3/DAP не заменяет. |
| `../design/ris-editorial-style.md` | Канон голоса R.I.S.: бренд/подпись, RU/EN термины, placeholders, числа, уверенность, примеры mail/AAR и human-review checklist. |
| `_dump_ris_ru_strings.py` | Dump RIS-tagged Russian.csv strings for artistic review. |
| `_fix_ris_brief11_ru_calque.py` | Compatibility wrapper → полный `_apply_ris_editorial.py`; one-shot с устаревшим loc ID и текстом удалён. |
| `_audit_ris_brief_loc_ids.py` | Print brief Email T-ids vs Russian/English.csv columns (catch AME ID collisions). |
| `_apply_ris_phase_b.py` | Compatibility wrapper → полный `_apply_ris_editorial.py`; отдельный Phase B dossier/AAR bank удалён. |
| `_apply_ris_queue_field_mails.py` / `_fix_ris_sighting_loc.py` / `_fix_ris_english_csv_text_keys.py` | Compatibility wrappers → полный `_apply_ris_editorial.py`; старые partial copy/fix значения удалены. |

Порядок проверки и применения JAZZ-UI-RIS-002 (из корня `jazz/`):

```text
python -B docs/tools/_audit_ris_copy.py
python -B docs/tools/_apply_ris_editorial.py
# review полного dry-run; только после одобрения:
python -B docs/tools/_apply_ris_editorial.py --apply
python docs/tools/_validate_items_quick.py
python -B docs/tools/_apply_ris_editorial.py --check
python -B docs/tools/_test_ris_contract.py
```

`--check` до применения ожидаемо возвращает `1`, если есть drift; после успешного
apply обязан вернуть `0`. Legacy wrapper-команды не запускать для частичных волн:
они намеренно выполняют тот же полный pipeline.

| `_install_ame_xtemplate_moditem.py` | Ставит `PDAAIMEBrowser` как `ModItemXTemplate` в `items.lua` + `ModResourcePreset`; убирает Code-load шаблона (иначе XTemplate not found). После правок `System_AME_Browser_Template.lua` (в т.ч. savannah chrome). Replace через markers или, если editor их снял, по `id = "PDAAIMEBrowser"` (без дубля). Callable `re.sub` — plain string ломает Lua `\\n` в T(...). Затем `_validate_items_quick.py`. |
| `_theme_ame_pda_savannah.py` / `_fix_ame_xtemplate_imagecolor.py` | Helpers: savannah chrome на template; снять незаконный `ImageColor` с XFrame. |
| `_gen_ame_portrait_prompts.py` | AME identity prompt bank: roster → `jazz-units/MercPortraits/_ame_face_refs/prompts.jsonl` + README (60 unique `face_traits`, `big_prompt`/`bust_prompt` for GenerateImage; no image gen). |
| `_gen_ame_flags.py` | JAZZ-UNITS-005: Pillow → `Icons/Flags/f_{nigeria,kenya,angola,mali,congo,ghana,senegal,ethiopia}.png` (128×80 simplified UI flags). |
| `_audit_ame_kit_tiers.py` | Аудит китов `ame-roster-60.md` vs потолки `tier_label`: Irr ≤1-2, Fight ≤1-3, Hard/Spec ≤2-1 (`weapons.csv`). |
| `_ja2mercs_folder_map.py` | Canonical Jazz→ja2mercs (1) pid-prefixed folder map (remesh / skip_*). Writes `jazz_to_ja2mercs_folders.csv`. |
| `_apply_ja2mercs_profile_map.py` | Apply folder map onto `jazz_to_ja2_profile.csv` (`speech_source`/`profile_id`/`status`). `--dry-run`. |
| `_wire_ja12_chat_voice_tags.py` | WIP UnitData/items compact chat `T(id,"…")` → `voice:Jazz_*` comments. `--apply` / `--dry-run` / `--only`. |
| `_clear_ja12_selection_chat_donors.py` | Delete AIM-chat opus that byte-duplicates Selection; preserve owner-approved same-voice fallback remesh. `--strict-hire-only` restores no-081–120 purge; `--apply` / `--dry-run`. |
| `_import_ja2mercs_subtitle_bank.py` | Import ja2mercs `*.txt` → `_voice-source/subtitles/<slug>.csv` (line index = SPEECH stem; encoding utf-8/cp1251). |
| `_apply_ja12_subtitles.py` | Apply subtitle CSV → UnitData/items `T()` + `Russian.csv` via `AIM_CHAT_WAV`/`SLOT_WAV`. `--only` / `--slots chat,combat` / `--apply`. |
| `_integrate_sj_khalif_mercs.py` | Shady Job `Downloads/SJ/data`: кэш → `_sj_cache`, mercedt CSV, UnitData/VR stubs Benny+Simon, ship Grom/Benny/Simon opus. WF AIM в SJ SPEECH нет. |
| `_extract_sj_sti_faces.py` | Decode SJ `faces/bigfaces/{66,67}.sti` (+ `b66`/`b67`) → `docs/design/mercs-ja12/{simon,benny}.ja2-face.png` + `_face-source/sj/`. Indexed STCI ETRLE. |
| `_process_ja12_facefix_portraits.py` | Preserve eight generated JA12 face-fix raws, cut with local BiRefNet, emit 2000/300 RGBA candidates + contact sheet under `jazz-units/MercPortraits/_wip/ja12-facefix/`; `--crop-only`, explicit `--apply` for runtime art. |
| `_fill_sj_chat_voices.py` | Copy Selection opus onto missing Benny/Simon/Grom AIM-chat T-ids (`--apply`). |
| `_fill_ja12_chat_voices.py` | Wrapper: `_ship_ja2_merc_voices.py --aim-chat-only` (classic/fallback/ub-proxy; not Selection). `--apply` / `--dry-run` / `--only`. |
| `_pour_ja12_design_hire_chat.py` | Pour AIM-chat RU/EN from `docs/design/mercs-ja12/<slug>.md` → UnitData + `items.lua` + RU/EN CSV; sync missing PartingWords. `--apply` / `--only`. |
| `_pour_ja12_design_identity_bio.py` | JAZZ-LOC-002: source-aware pour of RU/EN `Identity.Name` + `Bio` for the 42 approved `ready`/`executable` JA12 mercs. Preserves T-ids and unrelated bytes in UnitData/`items.lua`, emits `localization-copy-edits/ja12_identity_bio.csv`, and never edits runtime RU/EN CSV. `--dry-run` / `--apply` / `--check`. |
| `_stt_hire_chat_lines.py` | faster-whisper STT of hire stems → UnitData chat text (Quinten/Highball). `--apply` / `--only` / `--model`. |
| `_expand_ja2_merc_vr_full.py` | Expand stub (~12-slot) Jazz_* VoiceResponse to Colby-like combat coverage (~52 slots / 74 lines); allocates T-ids + RU/EN. Skips Colby/Spouke/need_pack/full VR. Then run `_ship_ja2_merc_voices.py`. |
| `_audit_ja12_merc_voices.py` | Read-only audit: Jazz_* VR T-ids vs `voices/<tid>.opus`, CSV ship status, TranslatedVoices mount, `g_VoiceVariations`. `--critical` for Selection/Aim/Movement. |
| `_audit_ja12_hire_chat_voices.py` | Read-only AIM-chat audit: UnitData T-ids vs shipped opus, per-merc `OK`/`PARTIAL`/`SILENT`, source mode and missing-slot summary. `--only` / `--fail-on-silent`. |
| `_inject_sj_benny_simon_vr.py` | Inject missing Benny/Simon `ModItemVoiceResponse` folders into `jazz-units/items.lua` (UnitData already via companion). |
| `_fix_benny_simon_tid_collision.py` | Remap Benny/Simon T-ids if they collided with an expand batch (safe re-run). |
| `_inject_vr_stubs_ja2_voices.py` | Для ready-мерков с пустым `ModItemVoiceResponse` — Ira-like stub (12 линий) из mercedt/NO EDT + T-ids `8900…6300+` в `jazz-units/items.lua` и RU/EN CSV. UB/ЦС без текстов — fallback-строки. |
| `_repair_ja2_voice_remaps.py` | Repair remaps: снять wrong Malice opus с `Jazz_Gaston` (FallbackMissingVR); обновить VR-тексты + re-ship `nervous`→041 / `hitman`→064 (Slay). `--dry-run` / `--skip-ship`. |
| `_audit_nightops_speech_coverage.py` | Аудит SPEECH/BATTLESNDS/NO overlays + внешние `_ub_cs_cache` (ЦС) / `_horg_stogie_cache` (Бычок). Identity по RU greeting/self-ID в mercedt, **не** по EDT filename (они часто врут). |
| `_extract_ja2_mercedt.py` | Распаковать/расшифровать `MERCEDT.SLF` (JA2 / NightOps) → UTF-8 CSV субтитров `000`..`116` в `docs/design/mercs-ja12/_voice-source/ja2no-mercedt/`. |
| `_extract_wildfire_rus_arc.py` | FreeArc extract `Jagged_Alliance_2_1_13_Wildfire_RUS.arc` (7z не открывает) через PeaZip `Arc.exe` → `_voice-source/_wildfire_cache/` (SPEECH/MercEdt + Data-UB). Это 1.13 RUS+WF maps, не commercial WF AIM VO; Gaston = Data-UB/058. |
| `_inventory_ja2mercs.py` | Read-only inventory `Downloads/ja2mercs (1)/ja2mercs`: layout (flat/nested), audio counts/formats, profile-id guess, crosswalk к `jazz_to_ja2_profile.csv`. Не ship/convert. `--root` optional. Remesh: `_apply_ja2mercs_profile_map.py` + `_ship_ja2_merc_voices.py --ja2mercs-remesh`. |
| `_stt_ja2mercs_sample.py` | Pilot subtitles for ja2mercs: export XLSX/mercedt ref text + optional faster-whisper RU STT (ADPCM→PCM via ffmpeg). Default pilot `но-шж/гром` pids 076+047 (both Grom). `--no-stt` = refs only. Out: `_voice-source/_stt/`. |
| `_audit_truncated_voice_responses.py` | Find JA2-style ~80-char mid-cut VoiceResponse strings in `English.csv`; match full RU from `ja2mercs (1)` XLSX (+ known STT repairs for Carlos/Devin). Report only → `_tmp_truncated_vr_strict.txt`. |
| `_audit_vr_loc_ids.py` | VoiceResponse `T()` IDs in `jazz-units/items.lua` vs `jazz` RU/EN CSV and `jazz-units/English.csv`. |
| `_apply_trunc_vr_and_lore_names.py` | Apply Grandier/Грандье + Khalif lore canon and truncated VR repairs into `jazz-units` `T()` + `Russian.csv`/`English.csv` (+ Manual). Canon: Grandier / Кавалье / Khalif. |

## Артефакты

- `_attach_001_audit.tsv` — dry-run/apply audit от `_apply_attach_001.py`
- `attachments-catalog.html` — generated catalog
- `_attach_*.json` — промежуточные summary (можно регенерировать)
- `merc-salary-data.json` / `merc-salary-calculator.html` — калькулятор зарплат AIM/AME/MERC (`python docs/tools/_export_merc_salary_json.py` → `_gen_merc_salary_calculator.py`)

## Добавление нового скрипта

1. Положить в `docs/tools/` с говорящим именем (`_apply_…`, `_export_…`, `_audit_…`, `_remove_…`).
2. Docstring в шапке: что делает, dry-run/apply, откуда читать, куда писать.
3. Строка в этой таблице.
4. При системной процедуре — ссылка в `.agents/docs/playbooks/…` и при необходимости в `.agents/docs/index.md`.

| `_loc_csv_io.py` | Safe read/write for `Russian.csv`/`English.csv`: **never** `splitlines()` before `csv.DictReader` (that flattens multiline AdditionalHint / perk text). |
| `_fix_dup_loc_ids_ame_perk_mag.py` | CommonLib «duplicated loc IDs»: JA2 perks off AME `5009–5028` → `5029–5048`; AME copyright → `5049`; Bleeding Text=EN; nationalities T()=EN; mag/parts Text↔T() align. |
| `_fix_dup_loc_ids_ame_perk_wave2.py` | Wave2: Meat/Carlos/Devin/Shank off AME filter `5001–5008` → `5050–5057`; English.csv AME Text = T() source. |
| `_fix_mag_hint_loc_align.py` | Mag/parts `AdditionalHint` only (`JAZZ_Mag*`, Scope/Barrel parts): unify family-prefix vs short T() + RU/EN CSV. **Не** сканирует весь `InventoryItem/` (иначе EN→RU Translation у Bandage/Medkit и vanilla stomps). |
| `_audit_additionalhint_newlines.py` | Audit/restore weapon `AdditionalHint` bullets: compare `InventoryItem/**/*.lua` `\n` vs CSV; `--apply` inserts newlines before bullet markers. |
| `_restore_csv_newlines_from_head.py` | Restore any CSV cell newlines lost vs `HEAD` when wording still matches (whitespace-insensitive). `--apply`. |
| `_purge_workshop_aim_mercs.py` | One-shot purge of six Steam Workshop AIM mercs from jazz + jazz-units (ModItems, companions, voices, loc, design). |
| _dump_legion_unit_dossiers.py | Dump Legion UnitData dossiers for design catalog. |
| _check_carlos_iggy.py / _check_iggy_insert.py | Verify Iggy/Carlos UnitData insert integrity. |
| _find_grom_id.py / _probe_grom_loot.py | Locate Grom UnitData/loot wiring. |
| _purge_restored_aim_vr_loc.py / _restore_vanilla_aim_vr_ids.py | AIM VR localization ID restore/purge helpers. |

- `_check_agent_docs_validation.py` — изолированные fixtures для полного/локального check-system-docs.ps1 (JAZZ-AGENT-SKILLS-001); запуск `python docs/tools/_check_agent_docs_validation.py`, PASS/ненулевой exit, рабочие документы не меняет.
- `_check_suite_agents_overlays.py` — sibling `AGENTS.md` рядом с `jazz`: обязательные маршруты suite-gate + `jazz-docs-sync.mdc`, без `docs/wiki/` и «wiki не ведётся». `python docs/tools/_check_suite_agents_overlays.py`.
- `_rig_specops_model.py` — source-only Blender bind LDW soldier → Male sample. Не ставить `JAZZ_SpecOpsBody_Male` (снят REQ-023).
- `_remove_specops_body.py` — снять установленный SpecOpsBody + SpecOpsTest из assets/units items/metadata/companion. `python docs/tools/_remove_specops_body.py`.

- `_check_villa_conflict_order.py` — реальный EnterConflict и порядок эффектов Guests: воспроизводит прежнюю паузу до маршрутов и проверяет ожидание после них; `python docs/tools/_check_villa_conflict_order.py`, Lua-harness, без запуска игры.

- `_check_infection_nonlethal.py` — MED-008, проверка защиты квестовых/бессмертных NPC, таймеров Unit/UnitData и сохранения смертей обычных врагов/бойцов игрока; `python docs/tools/_check_infection_nonlethal.py`, требует lupa, игровые сейвы не меняет.


`python docs/tools/_check_region_description_translation.py` — реальный Lua-метод подсказки: plain/T/empty/nil и неизменность описания.

`python docs/tools/_check_hospital_eligibility.py` — реальный фильтр госпиталя и прогресс травмы без Wounded, сохранность остальных callbacks. Оба требуют Python + lupa; игровые сейвы не изменяют.
# Возврат прежних визуалов АК

## Ванильные оружейные референсы для Blender

- `_extract_vanilla_weapon_references.py --game-root <JA3> --hpk <hpk.exe> --output <reference>` — адресно извлекает Weapon_/WeaponAtt* из Meshes/Skeletons/BinAssets; пишет SHA-256 manifest. `--resume` продолжает собственную незавершённую выгрузку.
- `_decode_weapon_reference_meshes.py --reference <reference> --reader <armor-hgm-reader.exe> [--cached]` — HGM LOD0 → JSON и OBJ в метрах, оси Blender (-Y,-X,Z); геометрия без переноса UV/материалов. Ошибки отдельных мешей перечислены в decode-report.json.
- `_dump_weapon_reference_spots.py` — снимает ванильные точки АК74/АК47/АКС74У через временные объекты в live DAP без pause/initialize; пишет `AppData/jazz_vanilla_weapon_spots.tsv`.
- `_build_ak_attachment_fit_scene.py --build <AK build> --reference <reference> --assets <assets repo>` — собирает две Blender-сцены из рабочих АК и реальных HGM ГП/сошек/ПК-А/45-зарядного магазина на установленных точках крепления. Требуются CustomGeometry/{PKAA,AKSeriaMount,AK74_Backelite_45}.json из того же HGM reader. Рендерит отдельно GP30, GP45, Bipod30 с обеих сторон; это offline fit, без записи активных игровых ресурсов.

`python docs/tools/_apply_ak_visual_revision.py --build <AK build> --weapon AK74M` (или `AK105`) — применяет уже собранные ресурсы из `mod-assets-stage`, проверяет ссылки на meshes/materials/textures, запрещает незарегистрированные новые файлы и сохраняет изменяемые версии. `_export_ak_assets.py` и `_render_ak_icons.py` поддерживают `--weapon` для адресной пересборки. Загрузка сущностей не заменяет проверку посадки модулей в игре.

`python docs/tools/_restore_legacy_ak_visuals.py --build <AK build>` — восстанавливает АК74/АКМ из `integration-backup/jazz`: Entity, дульные слоты, адресные визуалы компонентов и исходные иконки. Сохраняет остальные изменения и новые АК74М/АК105; создаёт резервные копии изменяемых файлов. Не перезагружает игру: перед сохранением редактора загрузить данные с диска. Проверки: `_validate_items_quick.py`, `_check_weapon_imports.py`. Возврат не означает завершённую проверку новых моделей.

- `_model_legion_armor.py` — Blender: `--sample <official BlenderScene_Appearance.blend> --output <folder>`; создаёт сварную кирасу, привязку к Male, рендеры и FBX. Входы/выходы вне runtime, не запускает игру.
- `_refresh_legion_armor.py` — `--build <staged build> --assets <jazz_assets> --core <jazz> --mount <Mod/id/>`: адресно заменяет существующие ресурсы кирасы и иконку, сохраняет backup и reload.lua. Runtime mount читать из Mods; абсолютный путь диска для ReloadEntityResource не работает.
- `_armor_live_eval.py --file <Lua>` / `--expr <expression>` — одно live-evaluate на :8165 без initialize/pause; изменения только через GameTimeThread, результат >380 символов через AppData. Не выполняет reload автоматически.

- `_preview_legion_armor_pose.py` — Blender CPU: `--source <blend> --output <folder>`; проверяет до 4 нормализованных влияний и рендерит синтетический наклон/плечо. Не заменяет JA3 runtime acceptance.

- `_model_legion_soft_armor.py` — CPU source prototypes: `--sample <official blend> --output <folder> --kind chainmail|brigantine|tire`; реальная геометрия проволочных колец служит high-poly источником для последующего bake, не runtime-мешем. Не регистрирует сущности.
- `_stage_legion_armor_tests.py --output <folder>` — готовит companion + ModItem на Torso-предмет, исполняет loadout в Lua mock. 37 новых определений остаются вне активных пакетов до готовности соответствующих визуалов.

- `_qa_legion_armor.py --blender <exe> --game-root <JA3_ROOT> --export-root <ExportedEntities> --output <new folder> [--install-existing]` — offline QA-pass кирасы: source → 4 CPU pose/anchor/rim checks → bake/export → AssetProcessor → DDS staging → executable graph checks → optional existing-resource install with backup and hashes. Каждому проходу новый каталог; Blender errors stop the pass. Игра не запускается, reload.lua не исполняется. JSON/logs/8 renders и game-acceptance.md сохраняются; PASS_OFFLINE не заменяет игровую приёмку.
- `_model_legion_soft_armor.py` теперь ориентируется на ArmorIcons/Chainmail, TireBrigantine, TireArmor: криволинейные резиновые секции, горизонтальные полосы бригантины, ремни/клёпка и материалы кустарной брони. Это исходники на доработке, без регистрации и runtime acceptance.

- `_extract_legion_armor_references.py --game-root <JA3_ROOT> --hpk <hpk.exe> --output <new folder>` — адресно извлекает 10 Legion tops с LOD, Male skeleton и бинарные материалы; SHA256 manifest и appearance-map, без полной распаковки текстур/игры.
- `_audit_legion_armor_sample.py` — Blender `--sample <official scene> --output <json>`: read-only transforms, parents, hgskeleton, UV/materials, weights и bounds всех clothing meshes. Гайд: `.agents/docs/playbooks/legion-armor-modeling.md`.

- `_audit_legion_armor_presets.py --game-root <JA3_ROOT> --output <json>` — QA roster по JAZZ_Legion UnitData: vanilla presets с приоритетом JAZZ overrides, Body/Armor/Pants/accessories, unresolved вызывает FAIL. Включён в следующий полный `_qa_legion_armor.py` как stage 00.


`_fix_k4_feedback.py --game-csv <Game.csv> --build <staging>` applies the scoped K4 IDs/reward transaction with backups; `_export_k4_localization.ps1` exports its nine rows through the canonical exporter. `_check_villa_waiting_recovery.py` tests the real module and vanilla conflict flow: distant arrivals, old saves, repeat start, other conflicts and combat guards.

- `armor-hgm-reader/armor-hgm-reader.csproj` — headless HGM→JSON for offline fit, using external MIT mxtsdev/hgm-viewer parser at bbcd41c6d1416fcfe8e98dd3a75ffa6e90a9904c. Build `dotnet build <csproj> -p:HgmSourceRoot=<checkout> -o <outside-repo output>`; run `dotnet <dll> <hgm> <json>`. Preserves geometry, bone names/indices/weights; no material or animation round-trip claim.
- `_calibrate_armor_hgm.py` — Blender `--source <cuirass blend> --hgm-json <compiled same cuirass JSON> --output <report>` validates coordinate conversion against source (threshold 3 mm).
- `_preview_armor_jazz_bodies.py` — Blender CPU `--source <cuirass blend> --models <HGM JSON folder> --roster <JAZZ roster JSON> --output <folder>`: imports every actual Body, preserves available bone weights, creates fitting scene and 5×2 example renders. Signed-distance candidate counts need visual review; never runtime PASS.
- `_extract_legion_armor_references.py --roster <JAZZ roster JSON>` additionally selects all actual JAZZ Body names, rather than only Faction_Legion_Top.

- `_preview_armor_vest_source.py` — Blender CPU `--source <extracted HAV> --output <folder> [--textured]`: restores the three source materials from supplied PNGs and packs textures into a diagnostic blend; no runtime writes.
- `_qa_soft_legion_armor.py --blender <exe> --game-root <JA3_ROOT> --reference-shirt <HGM JSON> --output <new folder>` — последовательный CPU model → pose QA → bake/FBX → AssetsProcessor → staging трёх кустарных броней. Останавливается при ошибке; в игру не устанавливает.
- `_check_soft_armor_poses.py` — Blender `--source <blend> --output <folder>`: веса/кости, четыре синтетические позы × два ракурса, предел растяжения p99; отчёт явно не подтверждает игровые коллизии.
- `_render_soft_armor_icons.py` — Blender CPU `--build-root <QA folder>`: прозрачные 110×110 рендеры трёх моделей с опущенными руками и автоматическим кадрированием полного силуэта. Позу экспортируемых meshes не меняет.
- `_install_soft_legion_armor.py --build-root <QA folder> [--apply]` — адресная установка трёх entity/иконок/тестовых UnitData с согласованными ModItem/metadata, проверкой закрытой игры, backup и SHA256. Без `--apply` только preflight.
- `_check_soft_legion_armor.py --build-root <installed QA folder>` — проверка установленных хэшей, регистрации, pose reports и исполнение loadout из ModItem и companion. `_check_legion_armor.py` дополнительно проверяет переключение всех четырёх броней и восстановление baseline.
- `_fit_heavy_armor_vest.py` — Blender CPU `--source <modular-source.blend with reference shirt> --output <new folder>`: saves a separate unrigged Light fitting candidate for LegionGoon, with two renders and transform report. No game install; entry point described in the armor modeling playbook.
- `_prepare_heavy_armor_variants.py` — Blender CPU `--source <donor-textured.blend> --output <folder> [--body <calibrated HGM JSON>]`: separates connected parts with preserved UVs, produces five shared geometry configurations, renders and a source-only manifest. Optional body is an unrigged rest-fit reference; guide `.agents/docs/playbooks/legion-armor-modeling.md`.
- `_prepare_clean_hav_blends.py --source <modular-source.blend> --woodland <reference.png> --output <folder>` — Blender creates nine packed, editable Light/Medium/Full material variants with separate parts, no rig or morph; asserts unchanged shared donor geometry across colors. No game writes.
- `_prepare_hav_rig_scenes.py --source <clean nine blends folder> --reference <fitted source with official sample and shirt> --output <folder>` — adds the official Male skeleton/body and static Legion shirt to nine editable scenes, leaving armor unbound and unchanged. Removes approximate shirt weights; renders front/back once per geometry. No game writes.
- `_model_6b3_vest.py --sample <official BlenderScene_Appearance.blend> --shirt <calibrated NPCCostumeMale_Shirt_08 JSON> --output <new folder> [--skip-renders]` — Blender CPU: собирает 6Б3ТМ-01 как **clean** геометрию по фактической одежде LegionGoon и фото владельца, без арматуры, весов и деформеров. Гейтит зазор до рубашки (min > -1 мм, p95 < 35 мм). Пишет `clean/JazzArmor_6B3.blend`, preview-карты в `textures/` (чехол, подсумки, стропа, кожа, металл), studio-рендеры с этими картами, иконку, clay и wireframe. Это preview, не JA3 bake.
- `_rig_6b3_vest.py --sample <official scene> --clean <JazzArmor_6B3.blend> --output <folder>` — Blender: переносит веса с Male sample (торс как у кирасы, плечи через clavicle/twist), склеивает `TEST_6B3`, нормализует до 4 влияний. Не экспортирует и не ставит в игру.
- `_qa_6b3_vest.py --blender <exe> --game-root <JA3_ROOT> --shirt <HGM JSON> --output <new folder>` — clean → rig → CPU pose QA → bake/FBX → AssetsProcessor → staging. В активные моды не пишет.
- `_install_6b3_vest.py --build-root <qa folder> [--apply]` — одна транзакция: `JAZZ_6B3_Male`, mapping `JazzArmor_6B3`, тестовый `JAZZ_Legion_ArmorTest_6B3`. Иконку `ArmorIcons/6b3.png` не трогает. `--apply` только при закрытой игре/редакторе.
- `_preview_armor_icon.py <icon stems> [--output <scratch folder>] [--scale N] [--flatten R,G,B]` — апскейл `ArmorIcons/*.png` для чтения силуэта до моделирования: число пластин, ворот, плечи, низ, ремни. Пишет только в scratch-каталог, репозиторий не меняет. Очередь партии жилетов — `docs/design/armor-vest-batch-queue.md`.
- `_model_camo_uniform.py --source <extracted LDW archive> --output <folder>` — Blender restores supplied OBJ UVs and packed diffuse/normal textures and renders the donor before any cutting. Audit found a balaclava and inseparable tactical vest, no boonie hat; do not treat it as three ready clothing objects.


Обновлён `_check_villa_waiting_recovery.py`: проверяет вариант без подготовительного конфликта, сохранение/восстановление штатных ожиданий и реальный GetSectorTravelTime с ускорением только колонны Эрни x5.


`python docs/tools/_probe_inventory_hang.py` — read-only снимок уже запущенного JA3Debug: причины открытого loading screen, состояние окна инвентаря, его потоки и ограниченный список UI-предметов. Без initialize/pause, запуска игры и изменений инвентаря. Длинный отчёт: AppData/jazz_inventory_hang.txt; DAP envelope: .tmp/bug-triage/inventory-hang/dap-response.json. `--self-test` проверяет Lua, восстановление SafeEval и DAP framing/EOF без игры.

- `_model_heavy_legion_armor.py` — Blender CPU HAV fitter and material preview: `--source <modular-source.blend> --sample <official Male sample> --output <folder> --family Twaron|Guardian|Zylon --variant Light|Medium|Full|Legs|HeavyLegs`. Zylon additionally requires `--woodland <user reference image>`; the original image is packed unchanged into the blend. Emits model.blend, front.png, geometry hash and NOT_RUN runtime status. See `.agents/docs/playbooks/legion-armor-modeling.md`.

- `_qa_heavy_legion_armor.py` — nine HAV torso builds, skin QA, CPU bake, official export and staging. Requires `--blender --game-root --output --source --woodland --shirt <calibrated HGM JSON> --reference-armor <original Light blend>`; optional `--only` limits configurations. Clothing-fit morph gate is mandatory. No installation.
- `_morph_heavy_armor_fit.py` — Blender morph of existing HAV shell to a real Legion shirt: `--source --reference-armor --shirt --output`. Preserves UVs and thickness, reports rear clearance, renders four rest views plus two approximate clothed lean views, and saves model.blend. It does not prove native game animation fit.
- `_refresh_heavy_armor_fit.py --build-root <QA output> [--apply] [--live]` — checks nine fitted resource graphs, geometry equality across material families and skin reports; replaces only already installed binary resources with backup. `--live` requires explicit owner authorization to update the running game; resource reload remains a separate step. No generated metadata or unit ID changes.
- `_rebind_heavy_armor.py` — Blender `--source <fitted model.blend> --output <folder>`: rebinds torso after morph using cuirass-style front/back transitions, retains rigid limb panels, lowers collar and narrows shoulders. Rechecks rear garment clearance and saves the source and reports.
- `_qa_heavy_rebind.py --source-root --output --blender --game-root [--only ...]` — builds nine material variants, checks clothed synthetic poses only once for each Light/Medium/Full geometry, bakes and stages existing entity IDs. Reuses QA only after exact geometry, topology, weights, skeleton and transform hashes match within the current run; records the source report. No installation or native animation acceptance.
- `_install_soft_legion_armor.py --heavy-torso` and `_check_soft_legion_armor.py --heavy-torso` reuse the atomic registration/loadout checks for nine modern torso variants, preserving existing icons. Use `--build-root`; installer is staging-only unless `--apply`.

`_check_legion_armor.py`: проверяет также mapping советской каски на СШ-68 и Head+Torso loadout тестового 6Б3 в ModItem и companion (REQ-025); только mocks/static, без запуска игры.

`_run_weapon_model_live_qa.py` + `_weapon_model_live_qa.lua`: приёмка 16 стволов handoff в уже запущенном JA3Debug на ModEditor; scan всех доступных компонентов, equip/pose на отдельном временном QA-юните. Выход `AppData/jazz_weapon_model_qa.txt`; без initialize/pause/reload/save и изменения ассетов.
`pairs` проверяет последовательности двух компонентов разных слотов через runtime-правила кабинета, без стоимости и ресурса механика; визуальную посадку не заменяет. `view 2300` — другой бок, `finish` — Idle. Камера использует `GetVisualPos()`; подробности в playbook `model-export-qa-handoff.md`.

`armor JazzArmor_<family><variant>` — меняет Torso только отдельного WeaponQA-юнита: девять HAV, 6Б3 или кираса. Печатает actual parts/body/pose и ставит камеру; без сохранения, перезагрузки ресурсов или изменения ассетов.


Инструменты исправлений приёмки (2026-09-22; runtime остаётся отдельным этапом):

- `_m14_repair_winding.py` — Blender: `--entity` выбирает корпус или деталь M14/EBR/MkIII; сварка совпадающих вершин перед `prepare_export_mesh`, контроль числа граней и всех loop UV, отчёт о перевёрнутых гранях. Сохраняет отдельный blend/FBX; не устанавливает и не доказывает устранение дыр в игре.
- `_m14_fit_preview.py --assets DIR --vanilla DIR --output DIR [--revised]` — Blender: read-only сборка M14 с оптикой, сошками и фонарём из HGM для проверки посадки через `_m14_render_culling.py`.
- `_m14_stage_visual_revision.py --output DIR --build DIR --game-root DIR [--apply]` — правка 27.09.2026: шесть проверенных мешей EBR/MkIII, посадка M14, линейная RM-карта дерева (roughness −12/255), только сошки в Under, MK14 Т3-1. Staging/manifest/хэши/backup, установка при закрытой игре; регистрации и shop Tier не меняет.
- `_m14_fixed_barrel.py` — staging фиксированного normal Barrel для M14SAW/M21/MK14EBR/JAZZ_M14_MkIII: items.lua, четыре companion и исходные хэши. `--apply` применяет при закрытой игре/редакторе, с backup и проверкой исходных хэшей.
- `_m14_render_culling.py` — Blender, `--blend FILE --output DIR`: две противоположные стороны с backface culling; исходный blend не меняет. Offline диагностика, не игровая приёмка.
- `_ar15_revision_fixed_slots.py --output DIR [--apply]` — фиксированные Handgrip M4A1/M16A4 и Stock M16A4, items/companions вместе, backup и закрытая игра.
- `_ar15_revision_test.py [--setter FILE]` — настоящие Lua setter/CanModifySlot в минимальном harness: RIS в обоих порядках, снятие, независимость Scope, fixed parts, M14 Under только сошки и очистка старых рукоятей/GL через LoadGame, незатронутые семьи. `--setter` проверяет staged файл до установки.
- `_ar15_revision_inspect.py` — Blender read-only острова и spots: `--blend FILE --output JSON`.
- `_ar15_revision_sights.py` — Blender staging одного M4A1 или M16A4: отдельная FrontSight на Gassblock для механических прицелов, исправление целика, длинная труба M4 без замены цевья; `--weapon M4A1|M16A4 --blend FILE --output DIR --game-root ROOT`. Строгая подготовка без custom normals.
- `_ar15_revision_install.py` — установка одного собранного AR15: `--weapon M4A1|M16A4 --build DIR --export-root DIR [--apply]`; требует compiled audit, сохраняет backup, регистрирует FrontSight и использует существующие текстуры.
- `_ar15_revision_visual_data.py` — `--weapon M4A1|M16A4|M21 --output DIR [--apply]`: ванильный плоский магазин AR15 либо общий Side mount M21; `--fix-grip` для M4 переносит вертикальную рукоять на Under. Проверяет Lua и исходные байты, сохраняет backup.
- `_ar15_revision_magazine_preview.py` — Blender: галерея декодированных ванильных магазинов или примерка через `--blend`/`--target`; только внешний preview, без установки.
- `_weapon_grip_surface.py` — Blender read-only `--blend FILE --entity ID --output JSON`: raycast нижней поверхности цевья относительно Hand_l_grip.
- `_weapon_grip_fix.py` — Blender `--blend FILE --entity ID --output DIR --game-root ROOT [--y METERS]`: отдельный blend/FBX с grip на 2 мм ниже поверхности; установка отдельно после compiled audit.

Повторный 6Б3, 23.09: `_model_6b3_vest.py` строит чехол с тонкими плечами, тканью и проецированными швами (16520 треугольников, бюджет 17000). `_rig_6b3_vest.py --shirt JSON --reference V7_BLEND --native-only` использует сглаженное поле весов реальной рубашки; v7 проверяет rest skeleton, не подменяет игровые анимации. `_qa_6b3_vest.py` передаёт эти параметры и `--texture-size 2048` в `_build_legion_armor.py`. Для refresh обязательны отдельный HGM round-trip и pose-check; runtime остаётся NOT_RUN. См. playbook `model-export-qa-handoff.md`.

- `_repair_ak103_export.py --source <blend> --output <build> --game-root <JA3_ROOT> --assets <jazz_assets>` — ограничивает экспортный corner budget, пересобирает Base/Norm/RM и исправляет Scope/Mount. Запуск через Blender; исходник не перезаписывается.
- `_repair_ak103_visuals.py --backup <folder> [--apply]` — три отсутствовавших AK103 ApplyTo (GP25, Bipod, Mag40), точечно в items.lua, backup и проверка закрытой игры.
- `_audit_compiled_weapon_mesh.py --blend <blend> --entity <id> --decoded <HGM JSON> --report <json>` — Blender-сравнение вершин и центров треугольников до/после AssetsProcessor, включая обратное покрытие. Пригоден и для torso в rest pose; не проверяет игровые анимации. Старый AK103 даёт FAIL, новый PASS.
- `_repair_ar15_geometry.py --blend <blend> --weapon M16A4|M4A1 --output <folder> --game-root <JA3_ROOT>` — Blender, один предмет за проход: короткий ствол с rifle-position мушкой либо origin на рукояти M4. Экспортирует только изменённую entity. У M16 короткий barrel использует UV/material нормального barrel; при установке копируется соответствующий normal .mtl.
- `_repair_hav_armor_skin.py --source <export blend> --reference <cuirass v7 blend> --output <new folder> --game-root <JA3_ROOT>` — Blender, один HAV: сверка native skeleton с v7, веса верхней спины/плеч, сохранение геометрии/UV/материалов, before/after pose-рендеры, strict mesh gate, FBX. Не устанавливает и не закрывает live-приёмку.
- `_install_6b3_vest.py --build-root <QA folder> --refresh [--apply]` — обновление уже зарегистрированного 6Б3: требует pose-check и compiled-audit, заменяет только девять ресурсов с backup. Сохраняет UnitData, metadata, mapping и существующую иконку. Без `--refresh` остаётся первоначальная установка.
- `_model_6b3_vest.py` — актуальный фронтальный референс владельца: неглубокая горловина, тёмные верхние усиления, высокие подсумки и плечи по уклону Shirt08. Все части без custom normals. `_rig_6b3_vest.py` использует непрерывный переход torso/back/sample через швы и лямки.
- `_check_legion_armor.py` проверяет также однократное смещение СШ68 на −4 см и отсутствие переноса смещения на другой шлем; это mock, не доказательство посадки в игре.
- `_check_legion_armor.py` проверяет Head-привязку 6Б7 при исходном HatSpot=Origin, исправление сохранённой/кэшированной привязки и возврат исходного головного убора на Origin после снятия; уровень mocks/static.

### Rebuilt improvised armor review (2026-09-26)
`_model_rebuilt_legion_armor.py`: Blender CPU source builder for chainmail, brigantine, tire. Inputs `--sample`, `--reference-shirt` (HGM JSON), `--kind`, `--output`; writes editable/export-ready blends and four review views, without installing resources. Shared fitting utilities derive from the legacy builder; new components implement APPEAR REQ-026.

- `_optimize_ak103_mesh.py` — отдельные Blender-пробы planar/collapse для native АК-103; вход `--source`, выход `--out` (blend, числа треугольников и выборочные расстояния), `--render` даёт парные PBR/clay ракурсы. Ничего не устанавливает: успешный экспорт не означает приёмку; варианты 26.09.2026 отклонены по качеству.

- `_audit_ak103_interior.py` — read-only проверка native АК-103: вход `--build`, выход `--out` с группами исходных материалов, пробами видимости (96 направлений) и выделением Bolt_group/ksk. Невидимость центров граней не разрешает их удаление; внешние части ksk и затворной группы сохранять.

- `_repair_hav_armor_materials.py`: `--assets`, `--source` (HAV split G/B), `--output`, `--game-root`; собирает RM и с `--apply` исправляет 21 DDS/84 fallback девяти HAV. Проверяет исходные карты и хэши защищённой геометрии; сохраняет backup и JSON.
- `_rig_6b3_vest.py` / `_qa_6b3_vest.py`: `--surface-skin` сочетает перенос весов с ближайших треугольников рубашки и локальное сглаживание швов; исходная широкая область поиска не используется. Требуется runtime-приёмка; офлайн позы не проверяют JA3 IK.

- `_audit_ak103_hidden_geometry.py` — все шесть native entity по отдельности: `--build`, `--out`; связные острова, совпадающие грани и кандидаты по 192 направлениям/7 точкам, без изменения исходника.
- `_strip_ak103_hidden_geometry.py` — отдельный кандидат по `--source`, `--audit`, `--out`, `--rings 2`; удаляет только закрытые грани с защитой соседей, проверяет точные UV/координаты и нормали видимых граней. `--render` создаёт обзор и sweep; сам не устанавливает.
- `_compare_weapon_quality_renders.py` — каталоги пар `*_before.png`/`*_after.png` → `pixel-diff.json` для контроля RGB/alpha. Числа не заменяют визуальный осмотр. Процедура и приёмка: `docs/specs/active/JAZZ-WEAPON-AK103-001.md`.
## Vektor R4 import

`_check_r4.py --build <build>` — read-only gate синхронизации Lua/metadata, графа entity/MTL/DDS, размеров иконки, тира, локализации RU/EN и восьми пулов Легиона. Проверяет сохранённый compiled-mesh audit; editor/runtime отмечает NOT_RUN.

`_build_r4_assets.py` — Blender: native OBJ/UV/PBR → метрическая сборка, пересчитанные нормали, FBX, два бока/3⁄4 и иконка; параметры `--source --build --game-root`. Исходник read-only. Затем штатный AssetsProcessor и `_prepare_rifle_assets.py` с prefix/entity `JAZZ_VektorR4`.
`_integrate_r4.py --build <build> [--apply]` — ограниченная установка предмета/каталога/ресурсов с backup; `_integrate_r4_loot.py` — только R4-записи канонического Legion generator, без mass regen. `_localize_r4.py --game-csv <Game.csv> --build <build>` и `_export_r4_localization.ps1` — канонический двуязычный экспорт трёх строк с сохранением остальных записей.
`_refresh_rebuilt_legion_armor.py --build-root <build>` validates only the three existing graphs/loadouts/poses; `--apply` replaces resources and icons with backup/rollback while the game is closed. No metadata, companion or test-unit edits.
`_check_soft_armor_poses.py --elbows` adds a bilateral elbow pose for the tire forearm guards; `--clothed` uses the explicitly approximate weighted LegionGoon reference.

`_audit_armor_views.py`: Blender read-only supplemental left/rear-left/top/bottom views of `--source` into `--output`; `--wide` includes tire forearm guards. Shows body and approximate reference shirt, never saves or modifies the source blend.
`_audit_armor_views.py --diagnostic --poses` adds neutral contrast materials, studio lights and clothed synthetic lean/deep-lean/twist views; render-only overrides, source stays unchanged.
`--shirt <decoded HGM JSON>` includes the real Shirt_08 geometry with native skin weights for clothed rest/pose inspection.
`_model_rebuilt_legion_armor.py`: repair pass welds imported garment seams before offset, uses a shared fitted envelope/skin for components, projects shoulder hangers and fasteners onto their supports, and connects the chainmail shield to its belt.
`_qa_rebuilt_armor_candidate.py --blender <exe> --game-root <JA3> --root <candidate> --shirt <JSON> --kind <kind> --phase review|export`: repeatable per-item clothed review or 2048 bake/compile/stage, without installation. Requires external visual review before refresh.

## VZ58 — JAZZ-WEAPON-VZ58-001

`_inspect_vz58_source.py <build>` (Blender) показывает состав двух архивов из `<build>/source/{classic,modern}`. `_build_vz58_assets.py --build <build> --game-root <JA3_ROOT>` (Blender) восстанавливает родные PBR/UV, выделяет 14 модульных сущностей и сохраняет FBX, blend, иконку и превью. `_compile_vz58_assets.py --build <build> --game-root <JA3_ROOT> --blender <exe> --decoder <legacy-reader>` компилирует/stage-ит и сравнивает HGM с Blender; `--skip-compile` повторяет только stage/audit. Встроенный `_decode_vz58_hgm.py` читает static HGM v14, учитывая float после сферы и общую систему квантования подмешей; старый reader оставлен аргументом совместимости.

`_integrate_vz58.py --build <build> [--apply]` добавляет предмет, визуалы, приватное цевьё, assets и каталог одной ограниченной транзакцией с бэкапами. `_integrate_vz58_loot.py` с теми же аргументами добавляет только generator-derived VZ58-записи. `_localize_vz58.py --game-csv <Game.csv> --build <build>` и `_export_vz58_localization.ps1` проводят канонический аудит и парный RU/EN-экспорт трёх новых ID; существующие строки сохраняются. `_check_vz58.py --build <build>` проверяет Lua, ресурсы, 160 конфигураций, каталог, loot, локализацию и compiled-audit; `--skip-localization` предназначен только для промежуточного запуска.

`_refresh_vz58_assets.py --build <build> [--apply]` обновляет только проверенный граф ресурсов VZ58, сохраняет бэкапы и удаляет только свои более не используемые DDS.
`_qa_rebuilt_armor_candidate.py --phase compiled --reader <armor-hgm-reader.exe>` verifies staged HGM topology/positions against the prepared export blend (both directions, 0.1 mm limit).

`_normalize_vz58_entity_records.py --build <build> [--apply]` переводит только 13 VZ58 ModItemEntity в многострочную форму, которую распознаёт sync-аудитор. Новая интеграция сразу пишет эту форму.
Refresh now requires `compiled-audit.json` plus `visual-review.json` (`REVIEWED_FOR_GAME_TEST`, matching source SHA256); numeric pose PASS alone cannot authorize a stale/unreviewed candidate. Native Shirt_08 skin drives clothed review; torso attachment layers sample one common radial fitting point.

`_build_vz58_folding.py --source <blend> --build <fold-build> --game-root <JA3_ROOT>` (Blender) создаёт сложенный металлический приклад с неподвижным креплением, FBX и превью. `_integrate_vz58_folding.py --build <fold-build> --base-build <build> [--apply]` устанавливает проверенную сущность и штатную пару компонентов с бэкапами. `_check_vz58_folding.py` проверяет настоящие Lua-действия и HUD на минимальном unit stub: оба направления, 4 AP, disabled/hidden и видимость в кабинете; игровой runtime не имитирует.

- 6Б3, ревизия по четырём ракурсам 27.09.2026: `_model_6b3_vest.py` выдаёт также `studio_back.png` и `studio_side.png`; задний верхний карман, боковые подсумки, поясной ремень, тонкие плечи и округлая горловина проверяются вместе. Источник референсов и backup сохраняются в каталоге сборки.
- `_preview_baked_armor.py --build <build folder> --entity <ID> --output <folder>` (Blender) — независимые front/back рендеры запечённых Base/Norm/RM на export mesh; проверяет единственную UV-развёртку. Для 6Б3 `_rig_6b3_vest.py` сохраняет SourceUV до bake, `_build_legion_armor.py` удаляет её после bake: в FBX остаётся только ExportUV.

### VZ58 / R4 — восстановление поверхностей (27.09.2026)

Перед recalc экспортёры соединяют только совпадающие позиции UV-швов (допуск 0.1 мкм в игровом масштабе), сохраняя loop UV и число треугольников. `_prepare_weapon_open_surfaces.py` вызывает общий normal gate и сохраняет исходную сторону открытых островов; custom normals не создаёт. `_audit_vz58_winding.py --build <build> --output <report.json>` сравнивает стороны подготовленных поверхностей с авторскими OBJ normals; `--r4-source <source>` включает R4. `_audit_compiled_weapon_mesh.py --check-winding` дополнительно проверяет ориентацию HGM с учётом отражения координат.

`_build_vz58_assets.py` принимает необязательные `<build>/material-overrides/Wood_Base.png` и `StockWood_Base.png` — готовые atlas edits с исходной UV-раскладкой; шероховатость неметаллической мебели ограничена снизу 0.72. `_refresh_weapon_surfaces.py --build <build> --export-root <ExportedEntities> --family vz58|r4 [--apply]` обновляет только существующие mesh/texture bytes и иконку, сохраняет имена DDS/материалы/регистрации, пишет backup и `reload-surfaces.lua` для штатного editor resource refresh. Путь игры передаётся переменной окружения `JA3_ASSET_GAME_ROOT`. Generated ModItem/companion transaction этим инструментом не выполняется.

- `_diagnose_ak103_material_uv.py` — отдельное before/flip-V сравнение native blend (`--source`, `--out`), без установки. Flip-V 27.09.2026 отвергнут; крышка model_9 получила неподтверждённую карту корпуса. `_import_ak103_native_maps.py` теперь требует явный проверенный `--cover-prefix`, вместо молчаливой подстановки карты корпуса.
- `_integrate_ak103.py` размещает новый AK103 рядом с AK74M в editor-папке `Items/Weapons/JAZZ - Firearm - Rifles-Assault`, Group `JAZZ - Firearm - Rifles-AR`; существующий ModItem перенесён туда 27.09.2026 без изменения runtime-параметров.

- `_repair_mosin_visuals.py`: точная коррекция красного дерева M38 прямо в BC1 DDS с сохранением mips и нейтральных блоков; preview по умолчанию, `--apply` пишет DDS/fallback и Hand_l_grip обреза X=8. Вход — исходные DDS из `--assets`, выход/backup — `--output`; исходные SHA256 защищают от повторной коррекции. Требует numpy/Pillow.
- `_match_mosin_wood.py`: следующая итерация M38 + Obrez; маска RM, учёт linear/sRGB и диффузной доли длинной винтовки. Вход `--assets`, preview/backup/report в `--output` (сохранять для повторных запусков), `--apply` устанавливает только четыре Base DDS. Заголовки/mips и блоки вне маски сохраняются; numpy/Pillow, игровые совпадения отдельно проверяет владелец.
- `_retier_mosin_loot.py`: точечно синхронизирует Mosin-записи существующих Legion LootDef с генератором (M38/Obrez 11, длинная 13), удаляет дубли и безусловные обходы; чужие записи сохраняет. Dry-run по умолчанию, `--apply` с backup (`--backup <path>` для следующей транзакции), `--check` проверяет установленный результат и идемпотентность; отсутствующий baseline Ranger_CQB не создаёт. Поддерживает ступени M38: 20000 на 11, 101000 на 12–19, 1400 на 20–29.

`_check_weapon_surface_uv.py --before <blend> --after <blend> --report <json>` (Blender) сравнивает весь набор треугольников по corner position/UV, игнорируя только индексы и winding; ловит потерю поверхности/UV при сварке. У `_audit_vz58_winding.py` флаг `--require-outward` включает gate по площади, допустимое расхождение с авторскими OBJ normals <0.1%.

`_retier_stg44.py --output <folder> [--apply]` готовит/сохраняет только comment StG44 `Tier 2-1` → `Tier 1-2` в ModItem и companion. Каталог/loot уже Т1-2 и не меняются. Lua проверяется до записи; apply требует закрытой игры/редактора и сохраняет backup.

- `_ar15_revision_fit.py` — Blender staging M16A4/M4A1: масштаб собственных деталей +10%, отдельная посадка прямого/изогнутого магазина, восстановление короткой трубы M16, Scope M4 вперёд с компенсацией CarryHandle. `--weapon --blend --output --game-root`; перед установкой `_audit_compiled_weapon_mesh.py --check-winding` для всех имён из `fit-report.json`, затем geometry-only installer.

### VZ58/R4 — дерево, блики и боковая иконка (27.09.2026)

`_weapon_material_finish.py` задаёт bounded normal amplitude/metal roughness и R4 hard-edge/sliver cleanup; вызывается обоими исходными экспортёрами. `_tune_vz58_r4_materials.py --blend <pre-fix.blend> --family vz58|r4 --build <dir> --game-root <JA3_ROOT> [--wood <dir>]` пересобирает материал из снимка **до** коррекции, не применять повторно к уже обработанным картам. Wood folder: ImageGen `Wood_Base.png`, `StockWood_Base.png`; sRGB учитывается ровно один раз. `_preview_vz58_r4_materials.py` делает original/no-normal/flip-green сравнение; `--final` также рендерит боковую VZ58 иконку.

После штатной компиляции `_install_vz58_r4_materials.py --vz58-build <dir> --r4-build <dir> --export-root <dir> --game-root <JA3_ROOT> --output <dir> [--icon <png>] [--apply]` заменяет только существующие DDS/fallbacks, проверенный R4 HGM и иконку, сохраняя backup. `_audit_vz58_r4_materials.py --install <dir>` проверяет установленные хэши, форматы, размеры и normal RMS. R4 обязан пройти HGM audit и `_check_weapon_surface_uv.py --allow-submicron-slivers`: исключение только для <10 граней с area<1e-8 м² и area/longest-edge²<1e-4, все остальные UV/поверхности совпадают.

`_update_vz58_optics.py --output <dir> [--apply]` готовит закрытый/компактный/EOTech/M68 в Scope, использует уже зарегистрированные generic visuals. Apply требует закрытой игры/редактора и синхронно меняет VZ58 ModItem + companion; metadata не меняется. Установлены все четыре варианта; VZ58 gate проверяет 352 конфигурации. Каталог обновляется в той же транзакции.

- `test_legion_newgame.py`: execute Legion start-tier and clock contracts in Lua via Python `lupa`; checks all starts/speeds/profiles, boundaries, legacy state and UI callbacks. Run `python docs/tools/test_legion_newgame.py`.
- `export_legion_newgame_localization.ps1 -GameCsv <Game.csv> -Build <staging>`: canonical audit plus paired RU/EN export of the eight PROGRESSION-001 IDs. Full unrelated audit findings remain visible; it does not replace runtime CSV automatically.

`_audit_armor_color_maps.py --assets <jazz_assets> --output <folder>` decodes the four installed albedo examples for inspection; handles DDS sRGB format tags without changing pixels.
`_stage_armor_colors.py --assets <jazz_assets> --output <fresh folder> --game-root <JA3_ROOT>` captures 22 albedo maps and protects the remaining resource graph. `_bake_armor_colors.py` (Blender; `--plan --chainmail --woodland`) bakes native black/green/woodland materials and brighter procedural mail. `_preview_armor_colors.py` (Blender; `--plan --hav --chainmail`) renders four offline previews. Finish with stage script `--apply`: compile full mip chains/fallbacks, shared-map guard, backup, hash validation and rollback. Requires closed game/editor; not repeat-applicable over its own output. No geometry/UV/RM/normal export.
Read-only final verification: `_stage_armor_colors.py` with the same arguments and `--verify` checks installed hashes, protected files, mip/fallback headers, and mean BC7 albedo error against the native bake (threshold 2/255). Reports `verification.json`; it does not validate game lighting.

- `_pack_suite_release.py` excludes Blender source/backup files (`.blend`, `.blend1`, `.blend2`, case-insensitive); use process-local Git `core.autocrlf=false` on Windows for matching Linux release hashes.

### Кожаный нагрудник: отдельная подготовка модели

`_model_leather_armor.py` (Blender CPU): `--sample BLEND --shirt JSON --output DIR` строит кожаный плитник по существующей `ArmorIcons/LeatherArmor.png`, сохраняет clean blend и пять материалов/посадочных видов. Никаких записей в runtime-пакеты.
`_qa_leather_armor.py`: `--blender EXE --sample BLEND --shirt JSON --reference V7_BLEND --output DIR [--views]` собирает rigged source, проверяет нормали и четыре синтетические позы; `--views` добавляет круговой осмотр и позы на реальной рубашке. Установка и игровой экспорт отдельно.
`_rig_6b3_vest.py --item LeatherArmor` задаёт ID source/report/mesh, сохраняя default 6B3. `_audit_blender_normals.py -- --mesh-prefix TEST_LeatherArmor` ограничивает проверку авторским мешем: неизменённый reference body разработчиков может содержать custom normals и не является экспортируемым ресурсом. Пустое совпадение — ошибка.
`--torso-carrier` в `_rig_6b3_vest.py` — отдельный native torso skin field для толстого кожаного плитника: центр переда/спины, вертикальное сглаживание, плавный переход к плечам; предотвращает попадание sleeve-весов в боковые ремни. Без флага поведение прежнее. Текущий source-only результат: `docs/design/leather-armor-production.md`.


### Weapon and armor feedback, 28 September, follow-up

`_weapon_feedback_inventory.py --output JSON` lists complete offered component visuals without modifying the game. `_weapon_feedback_stage029.py --build DIR` stages M14 spot casing, permanent FAL rail, AR15 attachment locations, Mosin names and compiled candidates with source hashes; it does not install.

Blender `_weapon_feedback_handguard.py --blend FILE --output DIR --game-root DIR` extends M16 RIS to the standard fore-end front while retaining barrel geometry. `_weapon_feedback_scope.py --source FILE --output DIR --game-root DIR` recovers the MkIII donor optic and reuses its atlas. `_weapon_feedback_mag_normal.py --source native.tga --output DIR --game-root DIR` compiles the magazine-only original normal map at reduced strength. `_weapon_feedback_icons.py --series-light` uses common physical light and zero display exposure; `--component` renders 100x100.

`_weapon_feedback_armor_skin.py --source FILE --shirt native.json --entity ID --output DIR --game-root DIR` prepares a clothed-donor skin candidate without changing positions/UV/materials. `_check_soft_armor_poses.py --entity ID` can inspect an existing baked source. These are candidate tools: compiled, visual and game acceptance remain separate. `_weapon_feedback_barrel.py` is the abandoned rear-cylinder experiment (export rejected by spike gate); do not install its outputs, the owner selected handguard extension instead.

Leather installation continuation: `_check_leather_armor_contacts.py` (Blender, `--source --output`) измеряет 58 маркированных точек пришитого нахлёста относительно настоящих деформированных панелей в четырёх позах. `_qa_leather_armor.py` включает этот gate. `_export_leather_armor.py --blender --game-root --root --reader` запекает 2048 Base/Norm/RM, вызывает штатный processor, stage и двусторонний HGM/winding audit. `_install_leather_armor.py --root candidate [--apply]` требует source/contact/compiled/visual gates, готовит ModItem/companion/metadata + mapping + isolated test unit, проверяет закрытую игру, делает backup и контролирует конкурентные изменения. Старая иконка сохранена. Общий `_check_legion_armor.py` теперь проверяет также lifecycle и loadout кожаного плитника.


Feedback round 2: `_weapon_feedback_chainmail.py` продлевает существующие ремни текущего v19 под пояс без смены atlas. `_weapon_feedback_decode_skin.py` адаптирует только временный v14 HGM для legacy-reader, проверяет ссылку на Male skeleton и использует native bone order; исходный HGM не меняется. `_weapon_feedback_skin_review.py` сравнивает compiled before/after с настоящей рубашкой в четырёх синтетических позах.

`_weapon_feedback_native_skin.py`, `_weapon_feedback_hgm_skin.py` и `_weapon_feedback_hav_batch.py` готовят эксперименты HAV: меняются только поля skin, геометрия/UV/нормали сохраняются. Эти эксперименты и кандидат 6Б3 **не приняты и не входят в установку**. `_weapon_feedback_icons.py --oblique` предназначен только для примерки, не для финальных иконок.

`_weapon_feedback_install029.py --build DIR` проверяет staging; `--apply` требует закрытой игры, проверяет concurrent hashes, сохраняет backup и откатывает собственные записи при ошибке. Состояние и незакрытые пункты: [второй проход](../design/weapon-visual-feedback-20260928-round2.md).

- `weapon_layer_icons/`: изолированный прототип послойных иконок; `audit.py` читает InventoryItem/items.lua, `render.py` читает assembled Blender + assets, `build_review.py` проверяет Lua selector/binder и пишет HTML/PNG. Только offline outputs; см. [контракт и съёмку в игре](../design/weapon-layer-icons/README.md).
- `weapon_layer_icons/test_names.py`: offline Lua-проверка названий по значимым модулям из `names.json`; сверяет текущие AK74/DragunovSVD slots, пишет `names-verification.json`. Общий стиль и границы переименования — [style-and-names.md](../design/weapon-layer-icons/style-and-names.md).
- `weapon_layer_icons/export_catalog.py`, `dispatch_capture.py`, `capture.lua`: live-каталог и временная съёмка на ModEditor через уже открытый DAP, без установки и inventory edits; вход — IDs/slots, выход — beauty/matte/background, реальный parts graph и отчёт восстановления.
- `weapon_layer_icons/process_live.py`, `survey_names.py`, `live_gallery.py`, `verify_live.py`: PNG → прозрачные 324×165 иконки, единые профили, полная матрица имён, HTML и проверка покрытия/файлов. Порядок и ограничения — [live/REPLAY.md](../design/weapon-layer-icons/live/REPLAY.md); SDD — [live/SDD.md](../design/weapon-layer-icons/live/SDD.md).
- `weapon_layer_icons/audit_live_visuals.py` сравнивает объявленные entities с фактическими vis.parts и пишет очередь ревью; `deliver_live.py` собирает сводку, PNG-сравнение и ZIP. `cleanup_probe.lua` читает восстановленную сцену; `finish_view.lua` скрывает только диагностический overlay, сохраняя лог.

- `weapon_layer_icons/install_presentation.py`: manifest → exact-match registry + PNG; scoped installation via `--active`, backups via `--backup`, preserves unrelated active changes.
- `weapon_layer_icons/test_installed_presentation.py`: installed Lua selector, unknown build fallback, existing getter branches, PNG hashes/format and compilation; JSON evidence via `--output`.

- `weapon_layer_icons/content_scope.py`: общий фильтр `excluded_disabled` из оружейного CSV для съёмки, установки и галереи.

- `weapon_layer_icons/icon_layout.py`: shared native-capture output recipe, original icon dimensions, silhouette fit and tone correction.
- `weapon_layer_icons/refit_live.py --backup <directory>`: rebuild active icons from preserved RGBA, retain previous icons, produce original/before/after comparison.
- `weapon_layer_icons/refit_review.py`: rebuild contact sheets and record alpha bounds for every active output.

- `weapon_layer_icons/calibrate_color.py`: fixed per-weapon luminance/saturation profiles from original icons; writes `live/color-profiles.json`.
- `weapon_layer_icons/test_color_match.py --before <backup> [--outline-expanded]`: verify dimensions, alpha/outline and tonal proximity to original icons; writes `live/color-verification.json`.

- `weapon_layer_icons/refit_silver_pistols.py --backup <directory>`: targeted 18-variant DesertEagle/HiPower rebuild with smooth tone profiles; verifies unchanged alpha and writes original/before/after comparison.

- `_merge_lf_conflicts.py`: resolves only clean three-way merges and CRLF-only conflicts in the current Git merge; leaves semantic conflicts for review.
- Generated-data audit uses `.agents/skills/sync-jazz-generated-data/scripts/parse-moditems.py`: lexical ModItem parsing supports inline/nested records without executing Lua. Development `tmp` directories are excluded from both the audit and runtime release archives.

- `_test_moditem_parser.py`: regression checks for inline/nested records, Lua strings/comments and malformed tables. Dormant duplicate companions are warnings only when the same class/ID has an actual metadata-loaded companion.

- `_pack_suite_release.py` streams exact-commit archives and skips development paths before staging; no full source tar is retained in memory.

- `weapon_layer_icons/dispatch_capture.py --layers --matte`: capture the full reference build plus isolated native host/attachment objects with the same camera and transforms. Combine `--prerequisite Slot=ID` for multi-module references. Outputs stay in the requested capture directory; no installed UI changes.
- `--resume-inventory-pause` temporarily removes only the inventory pause on ModEditor and restores it after capture. `plan_dependencies.py` lists additional barrel and RIS contexts; never dispatch overlapping camera capture batches.
- `weapon_layer_icons/audit_combinations.py` counts slot-domain combinations (an upper bound before compatibility). `compile_layers.py` compiles native signatures, shared coordinates and parent constraints into a layer library; `test_layers.py` checks Lua selection against captured graphs and enumerates slot domains.
- `weapon_layer_icons/layer_selector.lua` and `layer_binder.lua` are local modules embedded by `install_layers.py` into the existing InventoryUI binder. Installation requires selector test evidence and keeps a backup; `test_layer_binder.py` checks lifecycle offline, `probe_layer_binder.py` exercises disposable real XImage windows through DAP.
- `weapon_layer_icons/review_layers.py` compares a small isolated-layer pilot with its native full reference and searches draw order. Pilot evidence does not certify the whole arsenal. Procedure: [native layer replay](../design/weapon-layer-icons/live/LAYERS-REPLAY.md).
- `weapon_layer_icons/audit_native_graphs.py` records effective native attachment graphs for every pair of slot choices plus dense builds using disposable clones. `complete_capture.py` selects a finite supplement covering missing signatures, optionally waits for the initial batch and dispatches it; `run_dependencies.py` supports an explicit sequential prerequisite plan.
- `weapon_layer_icons/review_registry.py` compares composed native layers with full photographs and can optimize one consistent drawing order per weapon; outputs comparison sheets and error metrics for visual review. `icon_layout.fit` fits and outlines already graded compositions without applying color correction twice.
- `weapon_layer_icons/preview_layers.py` renders default and dense combined builds through the exact Lua selector; input is a compiled library and native graph audit, output is a PNG review sheet plus chosen component sets.
- `weapon_layer_icons/capture_settings.py` shares per-family camera distances between photography and native graph auditing. A changed distance requires fresh family captures and graphs.
- `weapon_layer_icons/inspect_templates.lua` reads loaded HUD callback provenance; `editor_transaction.py` backs up tracked Lua and calls `edit_template_bindings.lua` for official editor save/reload of both weapon-display binders, with a verification receipt.
- `weapon_layer_icons/probe_installed_ui.py` / `.lua` exercise the installed binder in real disposable XImages and photograph the inventory, then dispose temporary objects and restore pause; output is screenshots plus `verification.json`.

- `weapon_layer_icons/calibrate_layers.py` builds smooth family tone profiles from fresh default photographs and original icons; outputs JSON plus original/previous/smooth comparison. It preserves source geometry and alpha.
- `weapon_layer_icons/normalize_editor_save.py` preserves the verified two-callback editor delta and official generated fields while restoring pre-save formatting, unrelated companions and load order; archives all replaced post-save files. Follow with explicit editor reload validation.

- `weapon_layer_icons/test_layer_tone.py` verifies smooth monotonic profiles and exact alpha/dimension preservation against the previous installed layers; writes pixel evidence and a combined PNG hash.

- `weapon_layer_icons/reload_layers.py` reloads installed ModItems and UI, preserves metadata load order, verifies both HUD callbacks and optionally refreshes textures for explicitly named pilot families; does not load every arsenal texture into memory.


- `_prepare_release_assets.py` / `_test_release_assets.py`: независимые ZIP-части больших релизных пакетов, distribution manifest и проверка байтов/лимита.
- `weapon_layer_icons/edit_ak103_magazines.py`: официальный editor save списка магазинов АК-103 и барабана-донора АКМ, immutable baseline; `normalize_editor_save.py --ak103-magazines` сохраняет scoped delta.
