# Приёмка экспортов моделей — handoff для Астры

## Chainmail Body — 03.10.2026

Установлен новый Meshy-кандидат `JAZZ_Chainmail_Male`, теперь CharacterBodyMale: 22272 tri вместе с native торсом/руками/шеей, Base/Norm/RM/Color 2048, skin C1 сохраняет BodyColor юнита. Существующий `JAZZ_Legion_ArmorTest_Chainmail` — группа JAZZ Tests, MP40/120 FMJ; предмет/характеристики сохранены, оригинальная иконка возвращена. Исходники, 12 pose renders, baked front/back и backup: `jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/`. Offline normals/pose/compiled geometry+skin, ресурсные hashes и Body lifecycle mock PASS; root Body correction проверена live; финальный mesh в игре/editor ещё не проверен.

Проверить в новом процессе: цвет рук относительно головы, neck/head и Body/Pants швы, подмышки/низ рукава при aim, crouch/prone, напашник при движении ног, снятие/смена кольчуги с возвратом исходной куртки. Проверить сохранение со старой Armor-кольчугой: после обновления appearance остаётся только Body-вариант. Это новая игровая приёмка; старые замечания нельзя закрывать численным offline PASS.

Новая обратная связь 28.09.2026: пересечения спины HAV, задние ремни кольчуги без понятного крепления, по-прежнему неудовлетворительная посадка 6Б3. [Список и игровые скриншоты](../../../docs/design/armor-visual-feedback-20260928.md). Также открыто несоответствие тональности новых оружейных иконок старым (см. weapon feedback ниже). Прежние offline PASS эти замечания не закрывают; новых исправлений по этому дополнению пока нет.

Повторная приёмка 28.09.2026: установлен проход `REQ-VISUAL-028` (19 файлов, backup/SHA256). Исправлен UI blocked коротких стволов AR15, планка M14 выделена в OpticsMount, сошки на газовой трубке, EBR Side/Under на RIS без M203, UV каймы рукояти VZ58, сглаживание AK103 20°, папка VZ/R4 и цветная MkIII-иконка. [Контекст и изображения](../../../docs/design/weapon-visual-feedback-20260927.md). Новая игровая/editor приёмка открыта; нижеследующий проход 27.09 — история.

## Повторные замечания владельца — 27.09.2026

Свежие замечания по M4, АК-103, M14/сошкам, Mk14 EBR, Vz.58, металлу R4 и иконкам сохранены вместе с четырьмя скриншотами в [weapon-visual-feedback-20260927.md](../../../docs/design/weapon-visual-feedback-20260927.md). После паузы владелец разрешил продолжить: «можнго править». Прежние offline PASS не закрывают новые замечания; требуется новая игровая приёмка.

Установлен проход `jazz_weapon_feedback_20260927`: четыре HGM, четыре DDS с fallback, сошки M14/Under spot и семь иконок (21 файл, backup/SHA256 проверены). Строгие compiled normals и geometry/winding PASS после удаления одной/шести схлопнувшихся микрограней АК-103/EBR. Generated-sync: те же 6383 blocking issues, новых нет. **M4 не закрыт**: штатный UpdateVisualObj в offline Lua-harness корректно меняет ствол и дульник, short короче на 10.828 см; геометрия/код M4 не менялись. Новый запуск, editor round-trip и human acceptance ещё не выполнены. Детали/пути и остаточные проверки — в списке замечаний выше.

## 6Б3 по четырём ракурсам, 2026-09-27

По команде владельца «сделай также» установлен `vest-6b3-reference-v6-20260927`: плечи от краёв чехла с общей поверхностью накладок/ремешков, округлая горловина, передние клапаны, широкий верхний задний карман, коричневый пояс и боковые задние подсумки. Общий силуэт сохранён. Исправлено повторное изменение UV при сборке рига: SourceUV живёт до bake, в FBX остаётся ExportUV; перед bake выполняется prepare_export_mesh.

Offline: 16460 triangles, max 4 influences, v7 rest skeleton, четыре синтетические позы PASS (deep_lean p99 1.71855), strict normals 0 fatal, HGM round-trip <0.1 мм. Просмотрены четыре studio-ракурса и отдельные front/back на запечённых Base/Norm/RM. Девять ресурсов заменены с backup; registration/unit/icon сохранены. На увеличенном baked front есть мелкие тёмные стыки по кромкам — игровая видимость не проверена. **Runtime/human acceptance остаётся открытой**, P0 A08 не закрыт численными тестами.

Присланный владельцем `runtime-before-owner.png` показывает старые ресурсы. JA3 закрыта штатно по разрешению владельца, после установки не запускалась. Assets generated-sync baseline до/после 142 errors / 13 warnings. HAV и оружие в этом проходе не менялись; прежние незакрытые P0/P1 сохранены. Отчёт: `%USERPROFILE%/.codex/artifacts/model-repair-20260927/repair-report.md`; сборка и backup: `%USERPROFILE%/.codex/artifacts/armor-prototype/vest-6b3-reference-v6-20260927/`.

## Ремонт после приёмки 2026-09-26 (игра закрыта)

HAV: исправлены только текстуры. В 21 RM DDS были ошибочно продублированы одиночные grayscale-карты: Guardian metalness, Twaron/Zylon roughness. `_repair_hav_armor_materials.py` восстанавливает R=исходный G и B=исходный B из HAV, добавляет 84 fallback. Геометрия/веса из remote сохраняются; клиппинг A04–A07 не исправлялся по указанию владельца. Offline материалы не закрывают runtime.

Оружие: W03–W05 исправлены в FlashlightOff через Mountside ApplyTo трёх M14, M21 сохранён. W01/02: только IK attach positions, обрез −70 мм по длине, L42A1 +25 мм по высоте. Новая игровая проверка обязательна. АК-103 исключён из этого ремонта: владелец сообщил о замене другим агентом.

6Б3: установлена `vest-6b3-shoulders-v3-20260926`: цельные ровные плечевые накладки, ремни с люверсами, сохранён согласованный силуэт. 16856 треугольников, четыре синтетические позы, strict normals и compiled HGM round-trip <0.1 мм PASS. Это не runtime/human acceptance; плечи/спина в JA3 ещё требуют проверки. Отчёт: `%USERPROFILE%/.codex/artifacts/model-repair-20260926/repair-report.md`.

## Дополнение приёмки 2026-09-26

После pull `jazz_assets` до `b485065` проверены в JA3Debug/ModEditor все 9 HAV и 16 оружейных предметов из таблицы ниже на отдельном `JAZZ_Legion_ArmorTest_6B3_WeaponQA` / Shirt08. Результат **не принят**: Guardian Light/Medium/Full чрезмерно глянцевые; Twaron и Zylon Medium/Full пересекаются с рубашкой; новая 6Б3 пересекает плечи/спину. У установленной кирасы тоже есть пересечение в Aim; её compiled mesh ещё не сверен с эталонным v7.

Оружие: старые дыры ложи M14 в осмотренных ракурсах не воспроизвелись, ART виден. Остались хват обреза Мосина у дульного среза, ладонь ниже ложи L42A1 в Prone Aim, исчезновение Mountside при FlashlightOff + GL у M14SAW/MK14EBR/MkIII (у M21 сохраняется). M4/M16: плоские 20-round отображаются, ACOG снимает мушку, Long M4 не меняет цевьё; RIS ограничения подтверждены отдельно в обоих направлениях. Стрельба/reload/земля/save-reload в этом проходе **не смотрели**.

Полная таблица P0/P1 и скриншоты: `%USERPROFILE%/.codex/artifacts/model-qa-20260926/acceptance-report.md`. Runtime scan: 406 конфигураций, 9140 пар; это не 9140 визуально принятых сборок. У 84 уникальных DDS новых HAV нет fallback, но связь этого с глянцем не доказана. В этом проходе ассеты не правились.

QA helper: `armor <JazzArmor_ID>` меняет только Torso отдельного QA-юнита (9 HAV, 6Б3, кираса); whitelist не допускает произвольных предметов. Для Prone Aim выполнить `pose Prone`, дождаться перехода, затем `pose Aim` и подтвердить `inspect`: один `pose Prone` оставляет переходную анимацию. После смены компонента дать внешности обновиться перед скриншотом.

Снимок **2026-09-21**. Нейросети 15–20 сентября собрали оружие и броню, поставили entity на диск и прогнали offline QA. **`PASS_OFFLINE` / успешный AssetsProcessor ≠ принято в игре.**

Задача Астры: **проверить в игре то, что уже стоит**, записать дефект (предмет / entity / поза / скрин) и только потом чинить подтверждённое. Новые семейства и новые архивы не начинать, пока владелец не даст список.

Канон нормалей: `.agents/docs/playbooks/mesh-export-normals.md`. Канон брони: `.agents/docs/playbooks/legion-armor-modeling.md`. Игру запускает **владелец через Steam**; агент JA3 не стартует.

## Жёсткие запреты

1. Не `AsyncLoadAdditionalEntities` — уже был native crash (Access violation).
2. Не hot reload / `ReloadEntityResource` для приёмки. После правки entity — полный перезапуск модов.
3. Не писать и не оставлять custom/split normals. Не `shade_auto_smooth`. Только `prepare_export_mesh` → recalc + `shade_smooth`.
4. Не ставить снова `JAZZ_SpecOpsBody_Male` / `JAZZ_Legion_SpecOpsTest` (REQ-023, риг снят).
5. Не объявлять семейство готовым по PASS кирасы или по одному Goon.
6. Не `git push`, не теги, не Steam. Коммит — только если владелец явно попросит.
7. Не смешивать визуальный фикс с mass regen `items.lua`.
8. Абсолютный `<JA3_ROOT>` в git не писать.

## Что в итоге стоит на диске

Большая часть свежих entity **не закоммичена** (`jazz_assets` working tree). Предметы и mapping уже в `jazz` / `jazz-units`. После reload модов игра увидит локальные файлы.

### Оружие

| Предмет | Entity | Спека | Static | В игре | Что смотреть |
| --- | --- | --- | --- | --- | --- |
| `AK74` / `AKM` | ванильные `AK74` / `AKM` | `JAZZ-WEAPON-AK-FAMILY-001` | ремастер **снят** с предметов | ремастер отвергнут владельцем (разрез магазина, ГП/оптика/сошки) | не считать AKR_ «текущим» АК74/АКМ |
| `AK74M` | `AKR_AK74M` | та же | иконки/хват static; кабинет навесного не закрыт | хват правили 2026-09-20, нужен reload | рука на рукояти, не на магазине; модули |
| `AK105` | `AKR_AK105` | та же | то же | то же | то же |
| `AK103` | `AKR_AK103` + 5 модулей | `JAZZ-WEAPON-AK103-001` | длина 0.943 м, fit 18 кадров | **не запускалась**; EN/RU строк в CSV нет | шероховатость уже чинили дважды; приклад fold; ГП/сошки/ПСО |
| `SR3M` | `SR3M` | `JAZZ-WEAPON-SR3M-001` | RIS сверху, spots Scope/Side | руки/земля/стрельба **BLOCKED**; планку один раз намотали внутрь | нормали зубьев RIS, прицелы над планкой, Side сбоку; FX пока от AK74 |
| `L42A1` | `L42A1` + `L42A1_Scope` | `JAZZ-WEAPON-L42A1-001` | длина ×1.10 vs AK74, `ModifyRightHandGrip` | AC-006 **BLOCKED** | длина рядом с АК, винтовочный хват, родной прицел |
| `Mosin` | существующий предмет, Barrel 1891/M38/Obrez | `JAZZ-WEAPON-MOSIN-001` | UI-блок ПУ на коротких static PASS | визуальный smoke после правок не гоняли | смена ствола снимает ПУ; `_check_weapon_imports.py` падает на отсутствии `CanAppearInShop` — **не чинить в этой задаче** |
| `M16A4` | `M16R_M16A4` + модули | `JAZZ-WEAPON-AR15-FAMILY-001` | 28 сущностей, слоты PASS | владелец уже дважды смотрел; после последней правки — **снова reload** | левая рука на цевье, carry handle дефолт, короткий ствол/рукоять видны, RIS A4, компенсатор не стопкой, metalness |
| `M4A1` | `M4R_M4A1` + модули | та же | длины 100.6 / 84.0 см | то же | масштаб, fold, Mountfront для вертикальной рукояти |
| `FNFAL` | ванильный `Weapon_FNFAL` + Para stock | `JAZZ-WEAPON-FAL-FAMILY-001` | Tier 2, два состояния приклада | приклад «сидит» (human PARTIAL); стрельба **BLOCKED** | складка на петле, без щели; AssetsProcessor уже ругался на **нормали нулевой длины** |
| `JAZZ_FNFAL_Tactical` | тот же хост, Tac HG/Stock | та же | loot T2–4 / Adonis | runtime **BLOCKED**; строки `990002700–704` в CSV **нет** | RIS-цевьё по приёмному торцу, полимерный приклад |
| `M14SAW` / `M21` | `JAZZ_M14` (+ ART у M21) | `JAZZ-WEAPON-M14-FAMILY-001` | grip/stock static PASS | **BLOCKED** | без пистолетной рукояти; M21 несёт ART |
| `MK14EBR` | `MK14EBR` | та же | Bobby T4 | **BLOCKED** | шасси Sage; **3 вырожденных треугольника** в export-mesh |
| `JAZZ_M14_MkIII` | `JAZZ_M14_MkIII` | та же | не в магазине | **BLOCKED**; не путать с `GoldenGun` | камуфляж/рейка; Gold Fever не трогать |

Иконки 324×165 с обводкой: AK74M / AK105 / SR3M / L42A1 переснимали. ChipIcon `JAZZ_CarryHandle_AR15.png`, `JAZZ_Handguard_RIS.png` лежат untracked в `jazz/Icons/Upgrades/Chips/`.

### Броня Легиона (Male Torso)

Mapping: `jazz/Code/System_LegionArmorVisuals.lua`. Тестовые юниты: `jazz-units/UnitData/JAZZ_Legion_ArmorTest*.lua`, группа **JAZZ Tests**, MP40 + 120 FMJ, вне боевых пулов.

| Предмет | Entity | Offline | Владелец в игре | Что смотреть |
| --- | --- | --- | --- | --- |
| `JazzArmor_ImprovisedCuirass` | `JAZZ_ImprovisedCuirass_Male` | v7 `qa-v7-01` PASS, эталон рига | вид в целом принят; crouch/prone/equip/save **не закрыты** | лямки к пластине (не внутрь), низ спины, наклон |
| `JazzArmor_Chainmail` | `JAZZ_Chainmail_Male` | `soft-final-v5` install | **NOT_RUN** | иконка: две грудные пластины + один передний щиток; текущая модель этому ещё не равна |
| `JazzArmor_TireBrigantine` | `JAZZ_TireBrigantine_Male` | то же | **NOT_RUN** | горизонтальные полосы, не сетка 3×3 |
| `JazzArmor_TireArmor` | `JAZZ_TireArmor_Male` | то же | **NOT_RUN** | глубокий протектор, плечи, руки; не плоские плитки |
| Twaron / Guardian / Zylon Light–Full (9) | `JAZZ_*Light/Medium/Full_Male` | heavy-rig-v3 на диске | **зад/плечи отрываются в боевой позе**; риг кирасы лучше; offline PASS не принимать | тот же lean/aim, что показал владелец |
| `JazzArmor_6B3` | `JAZZ_6B3_Male` | `vest-6b3-v6-10`, 14312 тр. | **NOT_RUN**; юнит `JAZZ_Legion_ArmorTest_6B3` есть, в `jazz-units` ещё untracked | подсумки не «пузыри»; зазор к LegionGoon Shirt08 |
| Flak / IBA / шлемы | ванильные меши + tint | 19 тестовых юнитов | **NOT_RUN** | смена общего меша, Hide Hair, restore |
| `JAZZ_SpecOpsBody_Male` | снят | — | отвергнут | не возвращать |

Поножи Twaron/Guardian/Zylon нарезаны в исходниках HAV, **в игру не ставились**.

Пересечения rest-pose чужих Body (не чинить «одним overlay»): `EquipmentBiff_Top`, `Faction_Rebels_Top_Heavy`. Эталон примерки — `NPCCostumeMale_Shirt_08` (LegionGoon).

## Пайплайн нормалей (уже сделано, HGM не пересчитаны)

Сессия Blender / нормали `75d1ca78-1fd7-4310-9625-1412be7bc88a`:

- Helper `docs/tools/_ja3_mesh_prepare.py` → `prepare_export_mesh`.
- Все weapon/armor export-скрипты переведены; `python docs/tools/_check_mesh_export_normals.py` сейчас **OK**.
- Лежащие `*_JAZZ.blend` собраны со старым keep-custom. Custom/split есть почти везде. Снимается только следующим экспортом через helper.
- **Чистый без слоя — только AK-103.**
- Установленные `.m.hgm` сами не пересчитаются.

Настоящие дыры сварки, которые уронят **следующий строгий экспорт** (после `prepare_export_mesh`):

1. **AK74** корпус, face 1219 — нулевая площадь. Файл: `<WEAPON_SOURCE_ROOT>\Weapons\_ak_jazz_build\AK74_JAZZ.blend`. На активном предмете сейчас ванильный `AK74`, но blend/AKR_ живы.
2. **MK14 EBR** — три вырожденных треугольника, в т.ч. нулевое ребро. Файл: `<M14_BUILD>\rigged\MK14EBR.blend`. Это **активный** предмет.

Сырые донорские OBJ (~1.8 млн вырожденных граней) — не гейт. Гейт — подготовленный export-mesh.

В логе FAL tactical AssetsProcessor уже писал `normals with 0 length` и `Missmatched FBX file and SDK versions`. Второе у нас привычное; первое — смотреть полигон на пол-экрана в анимации.

## Приоритет проверки в игре

Владелец стартует JA3 через Steam, reload модов, чистая загрузка. Астра не запускает exe.

### P0 — сломать нельзя / уже болело

1. **Полигон на пол-экрана / чёрное зеркало** на любом новом меше в aim/run/crouch/prone. Особенно `MK14EBR`, FAL Tac, SR3M RIS, HAV.
2. **HAV** Light/Medium/Full (хотя бы Twaron): отрыв верха спины и наплечников в боевой позе. Сравнить с кирасой на том же юните/позе. Не копировать численные высоты кирасы слепо.
3. **Кираса v7**: standing уже смотрели; нужны crouch / prone / aim / run / turn, снять/надеть, save/reload.
4. **6Б3** на `JAZZ_Legion_ArmorTest_6B3`: посадка к рубашке, подсумки, те же позы.
5. **Новые стволы в руках и на земле**: AK103, SR3M, L42A1, M16A4, M4A1, оба FAL, M14 / M21 / EBR / Mk III. Стрельба, перезарядка, save/reload.

### P1 — посадка и кабинет

6. AR15 после последнего reload: видимые короткий ствол, рукоять, приклад A4; carry handle; Scope не стопкой сзади; ротик компенсатора.
7. AK74M / AK105: правая рука на пистолетной рукояти в idle.
8. FAL Para: смена folded/unfolded на петле без щели.
9. SR3M: прицел над RIS, Side на цевье, целик виден при пустом Scope.
10. L42A1: длина vs AK74, винтовочный хват.
11. M14: классика/M21 без пистолетной рукояти; EBR/уник с ней.

### P2 — не блокирует силуэт, но дыры есть

12. Локализация: `AK103` нет в `English.csv`/`Russian.csv` (EN пока покажет русское имя из companion). FAL Tactical `990002700–704` нет.
13. Иконки: новые стволы 324×165 с обводкой как у рукодельного AK74; ChipIcon AR15.
14. Кустарные три торса vs иконки (кольчуга — отдельные пластины).
15. Шлемы/Flak/IBA тестовые юниты — только если останется время.

Не закрывать AC runtime скриншотом Blender или CPU pose.

## Как спавнить и куда смотреть

- Броня: юниты `JAZZ_Legion_ArmorTest`, `_Chainmail`, `_TireBrigantine`, `_TireArmor`, `_Twaron*`, `_Guardian*`, `_Zylon*`, `_6B3`, плюс Flak/IBA/шлемы. Appearance `LegionGoon`, если в UnitData не сказано иначе. Несколько чужих Body потом, не вместо Goon.
- Оружие: выдать предмет мерку (инвентарь / консоль). Не добавлять в боевые пулы «чтобы проверить».
- Позы: standing, crouch, prone, aim, run, turn. Снять/надеть броню — Body должен вернуться. Кабинет модификации — каждый новый слот один раз.
- DAP не обязателен для визуальной приёмки. Если нужен live eval — playbook DAP, порт 8165, только `JA3Debug`. Retail Steam DAP не даёт.

## Рабочие blend (вне git)

### Повторяемый live-аудит оружия

`docs/tools/_run_weapon_model_live_qa.py` использует `_weapon_model_live_qa.lua` только на уже открытой карте ModEditor в JA3Debug. `scan` проверяет базовые сборки и каждый доступный компонент; `pairs` — оба порядка установки компонентов разных слотов через `ModifyWeaponDlg.CanModifySlot` (стоимость/ресурсы не проверяются). Эти отчёты не подтверждают визуальную посадку. `equip <item> [slot component]`, `component <item> <slot> <component>`, `pose Aim|Standing|Crouch|Prone` работают на отдельном runtime-юните `JAZZ_Legion_ArmorTest_6B3_WeaponQA`; `view 2300` показывает противоположный бок. После смены оружия дать ресурсам загрузиться перед скриншотом. `finish` возвращает QA-юнит в Idle. Выход: `AppData/jazz_weapon_model_qa.txt`. Без запуска игры, initialize, pause, reload, save и правки ассетов.

Для камеры и целей с высотой использовать `GetVisualPos()`: прибавление высоты к `GetPos()` с InvalidZ вызывает native assert. При таком assert прекращать приёмку native-stability до чистого перезапуска владельцем; не относить ошибку QA-камеры к дефектам моделей.

Не удалять, не затирать исходные архивы.

| Семья | Clean / source | Rigged / export |
| --- | --- | --- |
| АК | `<WEAPON_SOURCE_ROOT>\Weapons\_ak_jazz_build\` | `AK74_JAZZ.blend`, `AK74M_JAZZ.blend`, `AK105_JAZZ.blend`, `AKM_JAZZ.blend` |
| AK-103 | `<WEAPON_SOURCE_ROOT>\Weapons\_ak103_jazz_build\` | `rigged\AK103_JA3.blend` |
| SR-3M | `<WEAPON_SOURCE_ROOT>\Weapons\_sr3m_jazz_build\` | `rigged\SR3M_JA3.blend` |
| L42A1 | `<WEAPON_SOURCE_ROOT>\Weapons\_l42a1_jazz_build\` | `rigged\L42A1_JA3.blend` |
| Мосин | `<WEAPON_SOURCE_ROOT>\Weapons\_mosin_jazz_build\` | `MOSIN_JAZZ.blend` |
| FAL | `<WEAPON_SOURCE_ROOT>\Weapons\_fal_jazz_build\` | `rigged\FNFAL_Tactical.blend`, `FNFAL_ParaStk.blend` |
| M14 | `<M14_BUILD>\` | `rigged\JAZZ_M14.blend`, `MK14EBR.blend` |
| Кираса эталон | внешний armor-prototype | `qa-v7-01/source/improvised_cuirass_v7.blend` |
| 6Б3 | QA-папка `vest-6b3-v6-10` | `clean/JazzArmor_6B3.blend` + rig из `_rig_6b3_vest.py` |

Аудит открытого blend:

```text
blender --background --factory-startup <file.blend> --python docs/tools/_audit_blender_normals.py
blender --background --factory-startup <file.blend> --python docs/tools/_prepare_blender_normals_dryrun.py
```

Второй скрипт **не пишет** файл. Повторный экспорт в `jazz_assets` — только после подтверждённого дефекта и закрытой игры.

## Спеки и чаты

- `docs/specs/active/JAZZ-APPEAR-001.md`
- `docs/specs/active/JAZZ-WEAPON-AK-FAMILY-001.md`
- `docs/specs/active/JAZZ-WEAPON-AK103-001.md`
- `docs/specs/active/JAZZ-WEAPON-SR3M-001.md`
- `docs/specs/active/JAZZ-WEAPON-L42A1-001.md`
- `docs/specs/active/JAZZ-WEAPON-MOSIN-001.md`
- `docs/specs/active/JAZZ-WEAPON-AR15-FAMILY-001.md`
- `docs/specs/active/JAZZ-WEAPON-FAL-FAMILY-001.md`
- `docs/specs/active/JAZZ-WEAPON-M14-FAMILY-001.md`
- Очередь архивов (устарела как todo): `docs/design/weapons-import-queue.md`

Чаты (id без `.jsonl`): броня `21014154-a683-455e-9340-e6cfe31d7ad7`, импорт стволов `c44d5dcb-cbbe-4ad1-b3a4-e45fe5e07998`, AR15 `5911bcde-aed6-4cbf-a768-f46e868ce848`, FAL `1ffa836a-d077-4e38-88ac-227997427a10`, M14 `74e9cc23-6ea1-4b04-85f8-af08e631dc55`, иконки/SR3M RIS `3a41cd04-4747-4aa1-a82e-c436abc3dc17`, нормали `75d1ca78-1fd7-4310-9625-1412be7bc88a`.

## Промпт Астре (вставить целиком)

```text
Ты — агент в репозиториях JAZZ. Задача: ПРИЁМКА уже экспортированных моделей, не новые стволы и не новые семейства брони.

Сначала прочитай и держись:
- .agents/docs/playbooks/model-export-qa-handoff.md
- .agents/docs/playbooks/mesh-export-normals.md
- .agents/docs/playbooks/legion-armor-modeling.md

Игру не запускай. Владелец стартует JA3 через Steam и делает reload модов. Ты смотришь то, что он пришлёт / DAP, если DAP уже слушает :8165 на JA3Debug.

Порядок:
1) Сверь диск с таблицами handoff (entity на предмете, uncommitted jazz_assets).
2) P0 чеклист handoff. На каждый дефект: ID предмета, entity, юнит/мерк, поза, что видно, скрин если есть.
3) Не чини «на всякий случай». Сначала список находок владельцу.
4) Если владелец сказал чинить конкретный пункт — один предмет за проход, prepare_export_mesh, без custom normals, без AsyncLoadAdditionalEntities.
5) HAV не принимать по offline PASS. Эталон рига — кираса v7.
6) JAZZ_SpecOpsBody_Male не возвращать.
7) Mosin CanAppearInShop и общий generated-sync baseline не чинить в этой задаче.
8) Не commit / push.

Сдача: таблица «проверено / дыра / не смотрели» по P0 и P1. Без «в целом ок».
```


## После разрешённых исправлений, 2026-09-22

### Повторная приёмка и исправления, 2026-09-23

После игрового прохода владелец разрешил «меняй». Исходные наблюдения сохранены отдельно: внешний каталог `model-qa-20260923/acceptance-report.md` (81 скриншот, 434 конфигурации, 10790 пар). Новые файлы требуют следующего запуска владельцем; текущую игру повторно не запускать.

Установлено по одному предмету: сварка/winding M14 и ART (двусторонний culling и compiled round-trip); фиксированный normal Barrel четырёх M14; M4 Long без замены цевья; отдельные FrontSight M4/M16 только с механическим Scope; ванильные прямые 20-round CAR15_02; фиксированные рукоятки обоих и StockNormal M16; RIS gate для Side/Under в обоих порядках; общий Mountside у M21 GL+Side. Grip: L42 и MkIII подняты до нижней поверхности цевья, M4 VerticalGrip перенесён в Under, spot Obrez сдвинут назад с 16 до 12 см без замены его mesh.

Оружейные процедуры: `_m14_repair_winding.py`, `_m14_fixed_barrel.py`, `_ar15_revision_sights.py`, `_ar15_revision_install.py`, `_ar15_revision_visual_data.py`, `_weapon_grip_fix.py`; параметры в [README инструментов](../../../docs/tools/README.md). Старые family-exporters поверх них не запускать.

6Б3 последним: установлен `vest-6b3-revision-20260923-v3`, 16520 треугольников, Base/Norm/RM 2048, тонкие плечи и тканевые швы. Native shirt skin field сглажен; v7 проверяет rest skeleton. Четыре синтетические позы и compiled HGM PASS (<0.1 мм); это не приёмка пересечений или сходства в игре. HAV в этом проходе не менялся и не принят.

Generated baseline без новых ошибок: jazz 6241 errors / 1635 warnings, assets 142 / 13 (сумма 6383 / 1648). P0/P1 остаются открыты для новых моделей, полного цикла анимаций, земли, других мерков и настоящего кабинета.

Владелец закрыл игру и разрешил весь список находок, оружие сначала, 6Б3 последним. На диск установлены исправления AK103, M16A4/M4A1, M14/M21/EBR/MkIII/ART и ограничения Mosin PU; затем веса девяти HAV, посадка СШ68 и новая сборка 6Б3 `vest-6b3-reference-20260922-v4`. Уник MkIII теперь использует винтовочный хват по фактической форме donor stock и настоящие сменные 12x/Suppressor; EBR — пистолетный.

Старый HGM АК-103 портил топологию, хотя exporter завершался: новый corner budget и двусторонняя проверка центров граней устранили расхождение. Присланный Izhmash AK-103.zip содержит те же 13 OBJ, замена донора не требовалась. ГП25/ПСО/сошки дополнительно примерены в Blender.

Это **готовность к повторной игровой проверке**, не принятие P0/P1. Проверять в чистом запуске через Steam: все изменённые weapon host/attachment, HAV против v7 на одном юните/позе, 6Б3 с СШ68. Shooting/reload/ground/run/turn/save-reload и настоящий кабинет ещё не закрыты. Общий generated baseline сохранён: 6383 errors /1648 warnings, новых 0. Не возобновлять старый family exporter поверх исправленных рабочих blend.

## Кожаный плитник, 2026-09-28

Установлен `JAZZ_LeatherArmor_Male`, предмет `JazzArmor_LeatherArmor`, тест `JAZZ_Legion_ArmorTest_LeatherArmor` (JAZZ Tests). Полный нахлёст лямок, разрыв окантовки под ремнями, улучшенный leather shader → 2048 Base/Norm/RM. Контактный QA `_check_leather_armor_contacts.py` проверяет 58 точек на настоящих деформированных панелях: <0,5 мм в четырёх позах. Source: `tmp/leather-armor-v5/`, 11966 tri; native Male skin и HGM/winding PASS. Установка 16 файлов с backup, регистрацией и mock equip/unequip/loadout тестом; иконка сохранена. Runtime/editor/human NOT_RUN. При игровой приёмке осмотреть концы лямок спереди/сзади, кожу, crouch/prone/aim/run, снятие/надевание и восстановление Body. [Карточка производства](../../../docs/design/leather-armor-production.md).
