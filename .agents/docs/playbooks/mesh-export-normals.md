# Нормали и сварка полигонов при экспорте меша

Канон для брони, одежды и оружия. Не оставлять и не писать кастомные / split normals.

## Правило

1. Перед FBX / HGE **всегда** пересчитать нормали (`normals_make_consistent`, наружу).
2. **Никогда** не держать и не создавать кастомные нормали: `TRIANGULATE.keep_custom_normals = False`, `customdata_custom_splitnormals_clear`. Не писать `normals_split_custom_set`. Не вызывать `shade_auto_smooth` / `shade_smooth_by_angle` — в Blender 4.1+ они сами пишут split-слой. Только `shade_smooth`.
3. Успешный exporter / AssetsProcessor **не** означает PASS. Плохая сварка (слияние с чужой вершиной, нулевая площадь) в статике может пройти, а в анимации выдать полигон на пол-экрана.
4. Общий helper: `docs/tools/_ja3_mesh_prepare.py` → `prepare_export_mesh(obj)`. Новый export-скрипт вызывает его, не копирует старый `keep_custom_normals = True`.
5. Валидатор: `python docs/tools/_check_mesh_export_normals.py` — падает, если какой-то `docs/tools/*.py` снова ставит `keep_custom_normals = True`. Геометрию: `--scan-dir` на OBJ или HGM JSON; `--summary` для счётчиков. Открытый `.blend`: `blender --background --factory-startup <file.blend> --python docs/tools/_audit_blender_normals.py`.

## Что ловить

- кастомные / split normals на объекте после подготовки;
- треугольники нулевой площади и нормали нулевой длины;
- «игла»: одно ребро ≫ остальных и сравнимо с bbox (типичный след кривого weld).

## Не путать

Bake **normal map** (текстура Norm/Normal) — это не custom mesh normals. Карты запекаем как обычно. Запрет только на custom/split слой геометрии.

Донорский OBJ из архива часто грязный (нулевая площадь после фана n-gon). Гейт — подготовленный export-mesh, не сырой source. Уже лежащие `*_JAZZ.blend` собраны со старым keep-custom; следующий экспорт через `prepare_export_mesh` снимает слой. Установленные HGM сами не пересчитаются.

Текущий инвентарь экспортов и чеклист игровой приёмки: `.agents/docs/playbooks/model-export-qa-handoff.md`.

## OBJ с разорванными UV-швами (VZ58/R4)

Разрозненные геометрические острова из OBJ нельзя принимать по одному успешному recalc: Blender может выбрать внутреннюю сторону для полос поверхности. Сначала соединить только совпадающие позиции с микроскопическим допуском, проверить неизменность количества треугольников и loop UV; затем пересчитать наружу. У открытого листа нет объёма, поэтому после recalc его сторону сверять с авторской стороной исходника. Реализация: `docs/tools/_prepare_weapon_open_surfaces.py`; регрессия: `_audit_vz58_winding.py`. Проверка compiled HGM должна учитывать также winding (`_audit_compiled_weapon_mesh.py --check-winding`), а визуальная приёмка — отсечение задних граней в игре, не только двусторонний Blender render.

R4: почти коллинеарная грань может пройти area-only gate и дать `FBXImporter::OptimizeElementNormals ... normals with 0 length`. `_weapon_material_finish.separate_hard_edges` удаляет только submicron slivers (area <1e-8 м² и area/longest-edge² <1e-4, меньше 10 граней), удаляет loose vertices и разделяет геометрические стыки >60° без custom normals. Затем обязательны recalc, проверка corner normals, лог компилятора и HGM/winding audit. `_check_weapon_surface_uv.py --allow-submicron-slivers` разрешает только это измеренное исключение; остальные position/UV пары должны совпадать. Повторяемая процедура материалов/превью/установки VZ58/R4 описана в `docs/tools/README.md`, раздел «VZ58/R4 — дерево, блики и боковая иконка».
