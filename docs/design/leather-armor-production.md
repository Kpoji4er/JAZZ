# Кожаный нагрудник-плитник

Предмет: `JazzArmor_LeatherArmor`. Основание — запрос владельца 2026-09-28 и существующая `ArmorIcons/LeatherArmor.png`. Владелец принял общий силуэт, попросил исправить стыки лямок, улучшить кожу и разрешил установку при закрытой игре. Установлен кандидат v5; игровая/editor приёмка открыта.

Исходники и отчёты: `tmp/leather-armor-v5/`. Игровой граф: `jazz_assets/Entities/JAZZ_LeatherArmor_Male.ent`, одноимённые Meshes/Materials, `Textures/JAZZ_LeatherArmor_*` и Fallbacks.

- `clean/JazzArmor_LeatherArmor.blend`: 53 раздельные детали без рига; 11 966 треугольников.
- `source/LeatherArmor.blend`: `TEST_LeatherArmor`, официальный Male skeleton, 6 422 вершины, до четырёх нормализованных влияний.
- `front.png`, `back.png`, `side.png`, `oblique.png`, `clothed.png`: материал и примерка на реальную `NPCCostumeMale_Shirt_08`.
- `clothed-audit/`: диагностические виды и синтетические позы с native skin рубашки.
- `model-report.json`, `source/rig-report.json`, `normals.log`, `poses/pose-check.json`, `contacts.json`, `qa-report.json`, `compiled-audit.json`, `visual-review.json`, `installation.json`: результаты сборки, QA и установки. Backup — `installation-backup/`.

Силуэт: округлый нагрудник с двойным кожаным краем, карман под бронеплиту с клапаном, две широкие плечевые лямки, небольшой кожаный задник, два боковых ремня с железными пряжками. Материалы: тёмная коричневая кожа с неоднородным тоном и зерном, металлическая клёпка, грубая ремонтная заплата со стежками. Плита скрыта в кармане; характеристики и визуальная реакция на установку плиты не изменялись.

Веса ремней и грудных слоёв используют одно непрерывное поле, полученное из native torso весов рубашки. Ниже плеч не захватываются ближайшие рукава; вертикальные переходы сглажены для толстой кожи. Плечевые лямки плавно переходят к native skin. Это отдельный режим `--torso-carrier`; прежний default 6Б3 не меняется.

Проверено: экспортируемый меш не содержит custom normals, нулевых треугольников и spikes; нет неназначенных вершин; rest/lean/deep_lean/twist проходят skin gate. P99 растяжения: 1.0002 / 1.2643 / 1.6864 / 1.4561 при пределе 1.8. Эти позы не являются игровыми анимациями JA3 и не закрывают игровую посадку или пересечения на других Body.

Исправление стыков: вся пришитая площадка каждой лямки проецируется на настоящий mesh панели, окантовка обрывается под лямкой; центральный клапан не пересекает её. 58 маркированных контактных точек во всех четырёх позах остаются ближе 0,5 мм к панели. Кожа имеет мелкое зерно, сеть складок и вариацию roughness; запечены Base/Normal/RM 2048×2048 с mipmaps и 64px fallback. После запекания остаётся только ExportUV. Источник и baked front/back просмотрены отдельно.

Штатные FBX/AssetsProcessor/HGM проходят round-trip: 11 966 треугольников, max vertex error 0,0959 мм, winding корректный. Установлено 16 файлов, backup и SHA256 проверены. `JazzArmor_LeatherArmor` подключён через существующий `armor_entities` только у мужчин JAZZ Легиона. `JAZZ_Legion_ArmorTest_LeatherArmor` (JAZZ Tests) носит этот Torso, MP40 и 120 FMJ; в боевые пулы не добавлен. Существующие предмет, иконка, баланс и локализация сохранены.

Editor round-trip и игровая приёмка не выполнены. Generated audit сохраняет исходные проблемы пакетов: assets 142 errors/13 warnings, units 81 errors/0 warnings; новых проблем leather-графа нет. Структурная проверка items/metadata и исполняемые Lua mock/loadout проверки проходят.

Воспроизведение: `_model_leather_armor.py` → `_qa_leather_armor.py --views` → `_export_leather_armor.py` → `_preview_baked_armor.py` → `_install_leather_armor.py`; параметры описаны в `docs/tools/README.md`. Абсолютные пути к игре задаются аргументами.
