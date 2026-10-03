# Оружие, боеприпасы и компоненты

## Повторная приёмка 28.09.2026

Установлено 19 файлов по семейным `REQ-VISUAL-028`; backup и SHA256-manifest находятся во внешней сборке `jazz_weapon_feedback_20260928`. Проверено офлайн; новый запуск игры и editor save/reload ещё не подтверждены.

- `Code/System_WeaponRemovableModify.lua`: существующий vanilla helper `GetComponentBlocksAnyOfAttachedSlots` трактует отсутствующий компонент как пустой. Раньше `BlockSlots={Side2}` короткого ствола ошибочно блокировал его предпросмотр у M4/M16A4 без Side2. Регрессия воспроизводит исходный blocked и проверяет исправление обоих классов; реально занятый несовместимый слот всё ещё блокируется. Модели стволов не заменялись: установленные short короче normal на 10.828/11 см.
- В `jazz_assets/Entities/Meshes/AKR_AK103_Mesh.m.hgm` дополнительно разделены стыки свыше 20°. Все 18999 треугольников и UV сохранены, custom normals отсутствуют. Сравнительный рендер показывает ровную плоскость коробки вместо прежних диагональных бликов; игровая оценка открыта.
- `JAZZ_M14_OpticsMount` — 742 грани прежней встроенной планки, выделенные из общего `JAZZ_M14`. Scope visuals для M14SAW/M21 включают эту сущность через нулевой spot OpticsMount; пустой Scope убирает планку, ART у M21 сохраняет её. Новая entity зарегистрирована в assets items/metadata/EntityData и использует существующий `Materials/JAZZ_M14_Mesh.mtl`.
- Сошки M14 на Under `(56,-0.425,7.295)` см: учтены боковой сдвиг газовой трубки и локальный центр хомута AK bipod. EBR Side `(44,-2.780,8.750)` см с поворотом 90° вокруг X, Under `(40,0,5.774)`, Bipod `(49,0,5.774)` см — по поверхностям существующих RIS. Старый SideMountM14 больше не добавляется к EBR; Side1 заменён прямым Side.
- `MK14EBR` исключает `JAZZ_GrenadeLauncher_M14` из Under в items и companion. Существующий setter и LoadGame/NewGame обход снимают прежний M203 вместе с его эффектами; другие обвесы сохраняются. Общая система отдельно покупаемых планок не добавлена.
- `JAZZ_VZ58_GripWood_Mesh.m.hgm`: исправлены UV 99 граней деревянной оболочки, ранее захватывавших серые участки общего атласа. Геометрия, верхняя накладка, нижний винт и DDS сохранены. VZ58/VektorR4 перемещены из корня items в ту же папку редактора, что AK47; свойства и companion этих оружий не менялись. Остаточный металл VZ/R4 сохранён по разрешению владельца.
- Пересняты `WeaponIcons/{AK103,M14,M21,VZ58,JAZZ_M14_MkIII}.png`. MkIII содержит цветной штатный камуфляж; ванильные scope/suppressor в offline-иконке используют точную геометрию с нейтральным металлическим материалом. Все иконки 324×165 RGBA, alpha внутри краёв.

Evidence: [замечания и изображения](../../design/weapon-visual-feedback-20260927.md), `_weapon_feedback_preview_test.py`, `_weapon_feedback_graph.py`, `_weapon_feedback_validate028.py`, четыре compiled geometry/winding PASS, strict normals PASS. Подробности прежнего прохода ниже являются историей, а не актуальной посадкой сошек.


## Визуальный ремонт по повторной приёмке 27.09.2026

Локально установлена правка из `docs/design/weapon-visual-feedback-20260927.md` (семейные specs, `REQ-VISUAL-027`). Это проверенное на диске состояние; новый процесс игры и editor round-trip ещё не проверены.

- В `jazz_assets/Entities/Meshes/{AKR_AK103,MK14EBR,JAZZ_VZ58,JAZZ_VZ58_Magazine}_Mesh.m.hgm` разделены стыки свыше 40° без custom normals. Удалены только одна/шесть микрограней АК-103/EBR, схлопывавшихся при сжатии координат; оставшиеся позиции и UV сохранены. Compiled geometry/winding и строгий normals gate PASS.
- `jazz_assets/Entities/Textures/AKR_AK103_0_Norm.dds` использует родной atlas (`ksk` для крышки) с tangent strength 0.5 вместо компенсационной перепечки под прежнее сглаживание. `MK14EBR_Norm.dds`: strength 0.55; соответствие atlas/UV сохранено. В обоих случаях обновлены `Fallbacks/`.
- `JAZZ_M14_Base.dds`: RGB дерева ×0.85; `JAZZ_VektorR4_3_Base.dds`: RGB металлических участков ×0.88. Alpha и пиксели вне маски сохранены до сжатия, RM не менялась. Существующие разрешения, mip-цепочки и ссылки материалов сохранены; fallback обновлены.
- В `items.lua` только visual обычного `M14SAW` у `JAZZ_Bipod_Under` заменён на `WeaponAttA_BipodAK47`, слот visual `Under`. `jazz_assets/Entities/JAZZ_M14.ent`: Under = (56, 0, 9.5) см, хомут на оси ствола. M21 сохраняет отдельный Bipod spot и модель M24. Двухракурсная offline-посадка проверена.
- Пересняты `WeaponIcons/{M4A1,AK103,M14,M21,MK14EBR,VZ58,VektorR4}.png`, 324×165 RGBA, с обводкой. Сборка использует entity-local меши и установленные spots.

M4: новый Lua-harness исполняет штатный `FirearmBase:UpdateVisualObj` с текущими определениями компонентов, проверяет normal→short→long→short→normal и присоединение дульника к выбранному Barrel. PASS; разница normal/short 10.828 см. Правки геометрии/кода M4 не делались: дефект одинакового вида в живой игре не воспроизведён офлайн и остаётся открытым. Сравнительные рендеры сняты общей камерой, без отдельного auto-fit.

Транзакция: 21 существующий файл, исходные/установленные SHA256 и backup проверены (`jazz_weapon_feedback_20260927/install-manifest.json`, внешняя сборка). ModItem менялся только в `items.lua`; у WeaponComponent нет отдельного companion. `metadata.lua`, регистрации EntityData, ID, баланс, локализация и сеть не менялись. Будущий экспорт старых исходников требует переноса исправлений; инструменты `_weapon_feedback_*` описаны в `docs/tools/README.md`. Игровая/human приёмка остаётся открытой. Следующий абзац описывает предыдущий проход ремонта M14, до этой коррекции Base/Normal.

Локальная правка M14 от 27.09.2026 (`JAZZ-WEAPON-M14-FAMILY-001`, REQ-013–015): `MK14EBR` маркирован Т3-1, отдельный Bobby shop Tier=4 сохранён. В M14SAW Under допускаются только `JAZZ_Bipod_Under` и пустой вариант; существующий setter и LoadGame/NewGame удаляют старые недопустимые компоненты с их эффектами. M14SAW больше не добавляет SideMountM14, фонари/лазеры используют прямой Side. В общем хосте M14/M21 исправлены Scope/Bipod/Side/Under spots: `jazz_assets/Entities/JAZZ_M14.ent`. Roughness деревянных участков `jazz_assets/Entities/Textures/JAZZ_M14_RM.dds` уменьшена на 12/255; линейный BC7 и fallback сохранены, Base/Norm/metalness не редактировались. Пересобраны `Entities/Meshes/MK14EBR{,_BarrelNormal}_Mesh.m.hgm` и `Entities/Meshes/JAZZ_M14_MkIII{,_BarrelNormal,_MagazineNormal,_MagazineShort}_Mesh.m.hgm` в jazz_assets. Число треугольников и loop UV сохранены, custom normals отсутствуют. Compiled geometry/winding и Lua harness PASS; editor save/reload и runtime/human ещё не подтверждены. Регистрации metadata/EntityData не менялись; WeaponComponent visuals хранятся в items.lua.

## Vektor R4 — локальный ввод 26.09.2026

`JAZZ-WEAPON-R4-001`: `InventoryItem/VektorR4.lua`, `items.lua` и `metadata.code` регистрируют AssaultRifle 5.56, балансный Tier 2-1. Урон 21, магазин 35, выстрел/перезарядка 6/6 AP, надёжность 85, масса 4.3 кг. Штатная конфигурация без сменных компонентов; FX используют `Galil`. Bobby: in, BR Tier 2, RestockWeight 70, MaxStock 2, Cost 5500, AssaultRifles.

В `jazz-units/items.lua` добавлены только рассчитанные каноническим генератором R4-записи восьми подходящих пулов и три оружейно-патронные комбинации `JAZZ_GenW_VektorR4_*`. Amount 21–29, вес 101000: обычная массовая выдача, сопоставимая с АК того же большого тира. Новый калибр, изменения составов отрядов и special/unique выдача отсутствуют.

Ресурсы: `jazz_assets/Entities/JAZZ_VektorR4.ent`, `Entities/Meshes/JAZZ_VektorR4_Mesh.m.hgm`, `Entities/Materials/JAZZ_VektorR4_Mesh.mtl`, `Entities/Textures/JAZZ_VektorR4_*.dds` и парные fallbacks; иконка `WeaponIcons/VektorR4.png` (324×165). Сохранены native UV/PBR предоставленного архива; 13508 треугольников после удаления 14 исходных вырожденных граней и одной почти коллинеарной грани при коррекции 27.09.2026, длина 1.005 м. Compiled HGM проверен против Blender: совпадают число граней и поверхность, максимальное отклонение вершины 0.026 мм.

Уровень подтверждения: static и offline visual. Save/reload Mod Editor, материалы в игре, хват, перезарядка, стрельба и звук требуют игровой приёмки; успешная компиляция её не заменяет.

## Исправления моделей 23.09.2026 — runtime не принят

По `JAZZ-WEAPON-M14-FAMILY-001` у M14SAW/M21/MK14EBR/JAZZ_M14_MkIII фиксирован `JAZZ_BarrelNormal`: выбора длины нет. Существующий setter и обработчики LoadGame/NewGame переводят оружие в инвентарях юнитов/отрядов на фиксированные компоненты со снятием прежних эффектов. M1A и GoldenGun не входят в эту правку. Корпус M14 и ART пересобраны после сварки совпадающих вершин; обе стороны проверены с backface culling и сравнением с HGM, но повторной игровой проверки ещё нет.

По `JAZZ-WEAPON-AR15-FAMILY-001` M4A1/M16A4 имеют фиксированную пистолетную рукоять, M16A4 — штатный фиксированный приклад. Привязка магазина на 20 использует ванильный `WeaponAttA_MagazineCAR15_02`. Мушка — отдельный визуал Gassblock в компонентах механического прицела; оптика его не добавляет. Длинный ствол M4 не заменяет цевьё. Side/Under требуют RIS: ограничения встроены в существующие `ModifyWeaponDlg:CanModifySlot` и `FirearmBase:SetWeaponComponent`, в обоих порядках установки, без нового wrap; Scope независим. Вертикальная рукоять M4 использует Under.

Корректировка посадки AR15 (2026-09-27): существующие `jazz_assets/Entities/M16R_M16A4*.ent`, `M4R_M4A1*.ent` и соответствующие `Entities/Meshes/*_Mesh.m.hgm` увеличены на 10% вместе с собственными модулями и spots. Размеры магазинов сохранены; прямой ванильный и изогнутый донорский магазин имеют скорректированную посадку. Короткая труба M16A4 восстановлена из обычной после ошибочного удаления при отделении мушки; её дульный срез ближе к цевью на 11 см. M4 Scope дополнительно перенесён вперёд на 3.5 см с компенсацией в CarryHandle. Общий RearSight не масштабируется. Материалы/DDS/ModItem не менялись. 27 HGM прошли round-trip и winding audit. Runtime DAP подтвердил новые spots и attachment Muzzle→Barrel при переключении 2/3 длин; визуальная оценка кабинета и хватов после этого обновления остаётся human acceptance. Исторические размеры ниже относятся к предыдущей сборке.


Lua behavioral harness, строгая подготовка мешей и compiled-geometry audit пройдены. Кабинет, точная посадка магазинов/рукояти, сохранённые конфигурации и editor save/reload требуют чистого запуска. Это не закрывает human/runtime AC: повторный запуск в этой сессии запрещён владельцем.

## Назначение и эффект для игрока

Тестовый ввод оружия (JAZZ-WEAPON-ROLLOUT-001): AK105 получает Damage=27 как AKSU; AK74 и AK74M — CyclicRPM=600. AK74M заменяет AK74 в `jazz-units/items.lua` / Ivan10 с сохранением условий сложности и модулей. AK74M/AK105 входят в соответствующие существующие пулы с T3-1, SR3M с T3-2, L42A1 только в снайперские с T2-1. Добавлены 23 weapon/ammo-комбинации в 27 существующих пулов; записи Mosin сохранены; последующее уточнение MOSIN-001 REQ-009 задаёт M38/обрез с T1-1, длинную/ПУ с T1-3. Bobby: AK74M BR4/RW45/Cost16000, AK105 BR4/RW40/14500, SR3M BR4/RW20/22000, L42A1 BR2/RW35/10000; MaxStock=1. Это базовая цена, витрина применяет свои множители. Модель, текстуры и доступные модули не меняются. Статическая проверка пройдена; runtime/editor evidence — в [спецификации](../../specs/active/JAZZ-WEAPON-ROLLOUT-001.md).

АК-47: `CyclicRPM=600`, `BurstShots=3`, `AutoShots=6` (JAZZ-WEAPON-AK47-001). Короткая очередь следует RPM/200, длинная — RPM/100. Синхронизированы ModItem и runtime companion; подтверждение static, editor round-trip и бой не выполнялись. Asset contract без изменений.

JAZZ превращает оружие из набора vanilla-статов в систему индивидуальной баллистики, ресурса состояния, надёжности и компонентов. Кучность, дальность, recoil, число выстрелов, стоимость действий, углы overwatch и модификации зависят от класса и конфигурации конкретного экземпляра.

## Происхождение по слоям

В рамках того же тестового ввода восстановлены отсутствовавшие записи ножа `Crusher_Inventory`: 40%/55%/70% по трём диапазонам прогрессии, строго по действующему рецепту. Общая статическая проверка Легиона проходит 37/37 контрактов; прочий инвентарь Crusher сохранён.

Mosin: ПУ доступен только с `JAZZ_Mosin1891`. В двух ModItemWeaponComponent (`JAZZ_MosinM38`, `JAZZ_MosinObrez`) задан `BlockSlots={"Scope"}` — тот же механизм, что `BlockSlots={"Muzzle"}` у штатного ствола APS. В интерфейсе установленный ПУ блокирует переход на короткий ствол до снятия прицела; короткий ствол блокирует установку оптики. Прямой setter при смене на короткий ствол очищает Scope. Код класса/companion/metadata не менялся: WeaponComponent загружается непосредственно из items.lua. Lupa-проверка использует реальный JAZZ setter и штатные UI functions: PASS; новая визуальная проверка в игре не выполнена.

| Слой | Вклад |
|---|---|
| Vanilla | `Firearm`, `Weapon`, `Ammo`, component slots/effects, jam/degrade, attack API и InventoryItem serialization |
| CommonLib | Даёт общие mod helpers и исправления, но в проверенном срезе нет подтверждённой одноимённой коллизии с центральными weapon-resource методами JAZZ |
| JAZZ | Добавляет свойства, классы, калибры, предметы, component effects, ресурс/износ, собственную jam-формулу, scrap и рецепты |

## Реализация и load-state

Загружаемые файлы `jazz`:

- `Code/System_Firearm_AddProperties.lua` — свойства firearm, расчётные helpers и `JAZZ_GetWeaponCloseRangeRolloverTexts` для строки ближней зоны на карточке;
- `Code/System_OR_Weapons.lua` — расширенная runtime-логика оружия, износ и заклинивание;
- `Code/System_EmplacementAmmo.lua` — `MachineGunEmplacement:Update` remaps cut `_50BMG_*` `ammo_template` → `JAZZ_AMMO_50BMG_*` (и generic caliber mismatch → `GetAmmosWithCaliber`); **HOTFIX-004:** wrap `Unit:EnterEmplacement` (no `SetPos(nil)` if weapon/visual missing) + delayed `LoadGame`/`EnterSector` reseat (`Jazz_ReseatMannedEmplacements`: bind weapon, HUD, Idle `MGTarget` cone); **cone (JAZZ-WEAPONS-EMPLACEMENT-001):** runtime длина любого станка = `WeaponRange` / MaxRange ствола (`Jazz_EmplacementConeDist`); угол = **45°** (`Jazz_EmplacementConeAngle`, `45 * 60`), не COMBAT-009 `1/d`. Не map `target_dist`, не 50% BDR, не зрение. Editor preview по-прежнему ванильный MinRange. `Overwatch.GetMaxAimRange` без зрения только при `emplacement_weapon` / `ManningEmplacement`. Тот же dist helper в `EndInteraction` и Idle reseat (`MGRotate` на станке скрыт).
- `Code/System_WeaponResourceMaintenance.lua` — JAZZ-WEAPONS-002 late override: resource helpers, max-wear, jam type (no `GetRolloverHint` jam append), removable `JAZZ_RemovableAttachment` create/API (`JAZZ_ResolveRemovableComponentId` vanilla↔`JAZZ_` twins; `JAZZ_CreateRemovableAttachment` prefers catalog class `Id == component id`), remove-fail break (`P=Clamp(100−resourcePct,0,95)` → ScopeParts salvage / destroy), presentation sync, **rollover title** = compatible weapon DisplayNames + component name (`JAZZ_FormatCompatibleWeaponsForTitle`), install/remove Mech = best-in-squad (`JAZZ_GetSquadMechanical`); repair debits `JAZZ_BarrelParts` + `JAZZ_ScopeParts` when remountable Scope installed; `JAZZ_IsRemovableWeaponComponent` excludes irons / MagNormal / `*SuppressorIntegrated` (integral muzzle stays on scrap); **scrap eject** clones remountables into the bag **without** `SetWeaponComponent` (loaded loot + Magazine unload/`ReloadWeapon` on `weapon.owner` aborted SCRAP ALL); **`GetSpecialScrapItems`** returns only `AdditionalCosts` of `JAZZ_BarrelParts`/`JAZZ_ScopeParts` (never `component.Cost` — that is install Parts price);
- `items.lua` `RolloverInventoryWeaponBase` — UI «Шанс Клина» (`GetDisplayJamChancePercent`) и «Ближняя зона» (`JAZZ_GetWeaponCloseRangeRolloverTexts`: resolved−base Factor boost или штраф базы);
- `Code/System_WeaponRemovableModify.lua` — ModifyWeapon/DnD remountables; fold craft filter (`*Folded` без `UnFolded` скрыт в popup); Unfolded↔Folded swap бесплатно; `GetWeaponComponentDescription` всегда показывает DisplayName и для опций без эффектов — «базовый вариант» вместо голого «Без изменений»;
- `Code/System_InventoryStacks.lua` — **HOTFIX-005:** identical remountables (same `RemovableComponentId`) stack in SquadBag/SectorStash; mixed IDs never merge (`JazzInventoryItemsCanStack`). Do not clip `Amount` to 1 on load/sort (that deleted extra bipods). Personal loadout still uses def `MaxStacks=1`;
- generated `InventoryItem/<JAZZ_*>.lua` remountable catalog (~144) + folder `RemovableAttachments` in `items.lua` (editor spawn); refresh: `docs/tools/_gen_removable_attachment_items.py --apply`; **Bobby Ray temp:** `CanAppearInShop=true` RestockWeight=10 MaxStock=1 Tier=1 via `_enable_remountable_bobby_ray.py` (skip integ suppressor);
- `InventoryItem/JAZZ_ScopeParts.lua` — детали прицелов (лом / repair surcharge);
- `Code/WeaponClasses.lua` — grenade/rocket/mortar и другие weapon class extensions; после `UndefineClass('FlareGun')` снова заданы ванильные `GetBaseDamage` / `ValidatePos` / `GetAttackResults` (area-aim `FireFlare`; без них targeting зовёт nil `ValidatePos`);
- `Code/Systems_Compontents_FoldingStocks.lua` — свойства пары складного приклада;
- `Code/GetScrapParts.lua` — scrap-значения;
- `Code/AmmoRolloverHint.lua` — UI эффектов и модификаций патронов;
- `Code/Inventory.lua` и `Code/InventoryUI.lua` — применение предметов/боеприпасов; **`HighlightWeaponsForAmmo`** также подсвечивает совместимое оружие для `JAZZ_RemovableAttachment` (hover + drag, включая магазины);
- `Code/WeaponAttachChips.lua` — JAZZ-UI-001: очистка отключённых overlay-чипов на тайле/HUD; `Code/WeaponIconBake.lua` **dormant** (не в `metadata.code`, не перехватывает `g_HgnvCompressPath`);
- generated InventoryItem, Caliber, WeaponType, WeaponComponent, WeaponComponentEffect, WeaponPropertyDef и recipe ModItems.

## Снимок данных

В core-пакете зарегистрировано 558 `InventoryItem` definitions. Крупные оружейные семейства: 24 pistol, 24 SMG, 18 assault rifle, 17 sniper rifle, 14 battle rifle, 13 carbine, 13 revolver, 12 shotgun, 10 machine gun, 9 LMG, 6 autopistol и 4 grenade launcher. Также присутствуют ammo, armor, ordnance, misc/quest items и melee.

Определены 11 типов оружия: `Pistol`, `Autopistol`, `Revolver`, `SMG`, `AssaultRifle`, `Carbine`, `BattleRifle`, `Shotgun`, `LightMachineGun`, `MachineGun`, `Sniper`; 27 калибров; 236 `WeaponComponent`; 64 `WeaponComponentEffect`; 13 `WeaponPropertyDef`.

Устаревшие `CompactSMG` и `CompactSubmachineGun` удалены, а компактные образцы входят в единый класс `SMG` / `SubmachineGun`. `LightMachineGun` соответствует лёгкому пулемёту, а `MachineGun` — тяжёлому/позиционному. Назначение, компромиссы и будущие перковые действия всех классов зафиксированы в [ролях классов оружия](../weapons/class-roles.md).

Публичные weapon properties:

- `Recoil`, `MaxAimActions`;
- `BurstShots`, `AutoShots`, `WeaponMass`, `CyclicRPM`, `WeaponSizeClass`, `BurstLimiter`, `OverwatchAngle`, `CloseRange`, `CloseRangeFactor`;
- `BuckshotProjectiles` — база числа дробин на патрон для `Shotgun` (JAZZ-WEAPONS-006; ammo `CaliberModification`, не путать с `AutoShots`);
- `WeaponRange`, `BulletDropRange`, `Grouping`;
- `BaseJamChance`, `PenetrationBonus`;
- `WeaponResource`, `WeaponResourceMax`, `DegradePerShot`;
- `ReloadStyle`: `Magazine` (default), `Tube`, `Break` or `Revolver`;
- `DisposableLauncher`, `EmbeddedOrdnance` (только `RocketLauncher`: одноразовая пусковая и её встроенный ordnance);
- `WeaponName`, `WeaponIconMod`, reticle images и `UnitSubStat`.

В актуальном документальном контракте используются 12 weapon property definitions: `AimAccuracy`, `AutoShots`, `BaseDamage`, `BulletDropRange`, `BurstShots`, `Damage`, `Grouping`, `MaxAimActions`, `Noise`, `OverwatchAngle`, `Recoil`, `WeaponRange` (плюс JAZZ-only `CloseRange` / `CloseRangeFactor` / `BuckshotProjectiles` на FirearmProperties). `ModifyWeaponDlg` (`GetWeaponModifyProperties`) показывает `Recoil`/`BurstShots`/`AutoShots` при `CanBurstfire`/`CanAutofire` или authored shot counts > 0, а не только когда `GetBaseAttack` уже Auto/Burst.

В [модели стрельбы](../weapons/accuracy-model.md) `Handling` **удалён**. `Recoil` задаёт тяжесть множительного удержания точности последующих пуль и authorится из `WeaponMass` (десятые кг), `CyclicRPM` и `WeaponSizeClass`; они не читаются повторно в CTH runtime. `BurstShots`/`AutoShots` фиксированно выводятся из RPM при authoring (`/200`, `/100`) и `BurstLimiter` ограничивает только burst. Число дробин — `BuckshotProjectiles` (база 1 на стволе; картечь ×9, birdshot/salt ×20). Оптика переносит эффективную прицельную зону через aim progress, не увеличивает физическую дальность и больше не получает старые плоские CTH-effects.

Вырезанные, но всё ещё загруженные классы (`MP5`/`AR15`/`M4Commando`, vanilla `_*` ammo с `Ammopics/TEST.png`) перечислены в [вырезанном контенте](../weapons/cut-content.md). Их нельзя использовать в луте/магазине; живые калибры — только `JAZZ_Caliber_*` / `JAZZ_AMMO_*`.

## Канонический каталог

Полная таблица 164 технических weapon ID, 161 активную игроковую запись, balance-tier, характеристик и слотов находится в [каноническом каталоге оружия](../weapons/README.md). Тиры из профильных Google Sheets были использованы только для первичной миграции и выявили 25 расхождений с Lua-комментариями; после миграции источником истины является CSV. AR15, M4Commando и базовый MP5 отмечены как excluded_disabled и не публикуются в wiki.

## Компоненты

Канонические связи компонентов и эффектов находятся в `docs/technical/weapons/data/weapon-components.csv` и `weapon-component-effects.csv`. Runtime сначала использует resolved свойства оружия, поэтому component modifier `Recoil` не умножается второй раз при построении recoil profile.

Текущий working-tree snapshot содержит 50 mod-owned `WeaponComponentEffect` и 190 component records (включая 13 `vanilla_ref` stubs, нужных для join каталога). Живые JAZZ components и effects выгружаются из `items.lua`, а их option wiring — из `InventoryItem/*.lua`.

Эффекты покрывают:

- barrel/range/grouping/recoil, базовый урон и `CloseRange*`;
- bipod setup и позиционную эффективность;
- BMG/caliber и penetration;
- burst/automatic/run-and-gun варианты;
- aim actions, aim accuracy и максимальное прицеливание;
- число выстрелов и AP-стоимость;
- магазины, scopes, lasers, silencers и muzzle devices;
- folding stock и two-handed состояние.

`Systems_Compontents_FoldingStocks.lua` добавляет `zzFoldingPair`; runtime использует `zzStockEquipped` и actions `FoldStock`/`UnFoldStock`. Эти имена являются межфайловым контрактом generated components, UI и визуального состояния entity. В кабинете модификации сложенный half (`*Folded`, не `*UnFolded`) скрыт — крафтится разложенный; Cost Folded = UnFolded (= Light), `StockNormal` чуть дороже (см. `docs/design/stock-tiers.md`).

**UI surface (JAZZ-UI-002):** `FoldStock` / `UnFoldStock` / `FlashlightOn` / `FlashlightOff` имеют `ShowIn = false` и не входят в боевой hotbar. Чипы — вторая колонка `UIWeaponDisplay` `idButtons` (`GridX = 2`) рядом со Switch/Reload; helpers в `Code/System_WeaponCompHUD.lua`. При видимом Fold/Flash первая картинка активного комплекта сужается на 27 UI-пикселей (25 + spacing 2), сохраняя общую ширину блока рядом с центрированным hotbar; вычет один и для двух оружий.

После JAZZ-ATTACH-001 live components больше не используют `*Handling*` или `Cumbersome` effect presets; Firearm property `Handling` удалён вместе с UI/GameTerm/CTH-modifier presets. Все модифицируемые live component IDs, созданные JAZZ, используют канонический префикс `JAZZ_`; сохранённые `vanilla_ref` stubs отражают ссылки companion-файлов без JAZZ definition и не получают выдуманных effects. Четыре pure-ergo components (`JAZZ_TacGrip`, `JAZZ_Handgrip_Ergo`, `JAZZ_SigErgoHandGrip`, `JAZZ_HandlingWrap`) теперь дают `RecoilDecrease`.

`RocketLauncher.DisposableLauncher` имеет default `false`; `EmbeddedOrdnance` определяет единственный встроенный выстрел одноразового launcher. В v1 JAZZ-WEAPONS-005 этим контрактом пользуется только `M72LAW` (`Warhead_Frag`, magazine 1); RPG-7 не имеет флага и продолжает использовать отдельный ordnance.

Magazine data uses `MagazineSizeSet` with `ModificationType = "Set"` and an absolute `MagazineSize` parameter: named magazines, drums and belts no longer use a live `MagazineSizeMultiplier`. Runtime (`Code/System_WeaponComponent_Set.lua`): engine applies `MulDivRound(base + mod_add, mod_mul, 1000)`, so Set uses `mul=1000`, `add=N−base` (not `mul=0`, which always yielded MagSize 0/1 — e.g. stock CAR-15 / Glock 18 on Vicky/IMP). `LoadGame`/`NewGame` re-seat MagSizeSet magazines and refill ammo when the broken `mul=0` modifier is detected. The former generic `JAZZ_MagLarge` was split into `_50`, `_28`, `_27`, `_25`, `_13` and `_8` variants; PSG1 no longer offers `MagLargeFine`. The barrel-specific `JAZZ_Auto5_*_LMag` multiplier remains a tracked exception.

Геометрия хай-тира AR15 (JAZZ-WEAPON-AR15-FAMILY-001, фаза 2): `M16A4` использует `Entity = "M16R_M16A4"`, `M4A1` — `"M4R_M4A1"`. Стволы — отдельные сущности со спотом `Muzzle` на резьбе; штатный пламегаситель — `JAZZ_DefMuzzle` (`_*_DefMuzzle`), компенсатор — `WeaponAttA_CompensatorM4`, без стопки на впечённый birdcage. Слот `Barrel` крепится к дельта-кольцу, не к мушке. `M16A4`: `_Barrel` (20"), `_BarrelShort` (14.5" с `m4`), `_Handguard` (A2), `_HandguardRIS` (карабинный RAS, растянут до окна A2), `_Stock` / `_StockLight`, `_Handgrip`, `_Magazine20`. `M4A1`: `_Barrel` (14.5"), `_BarrelShort` (10.3" с `mk18`), `_BarrelLong` (20" с `m16`) плюс `_HandguardRifle`, `_Handguard` / `_HandguardRIS`, `_Handgrip`, fold-пара приклада, `_Magazine20`. Оба имеют `_Magazine`, `_CarryHandle`, `_RearSight`. `Scope` не бывает пустым: дефолт `JAZZ_CarryHandle_AR15`, спот сдвинут на 3 см вперёд. Fold-слот `M4A1` не тронут. Длины: `M16A4` 100.6 см, `M4A1` 84.0 см. `Hand_l_grip` у A4 на 31.3 см; у `M4A1` своего нет. Старые сущности `M16A4` и `M4A1` остаются на диске неиспользуемыми.

Семья AR15 (JAZZ-WEAPON-AR15-FAMILY-001, фаза 1): `M16A4` имеет слоты `Barrel` (`JAZZ_BarrelNormal` / `JAZZ_BarrelShort`), `Stock` (`JAZZ_StockNormal` / `JAZZ_StockLight` / `JAZZ_StockHeavy`), `Handgrip` (`JAZZ_Handgrip_Default` / `JAZZ_Handgrip_Ergo`) и пустой по умолчанию `Trigger` (`JAZZ_Autofire` — `EnableFullAuto` + `EnableBurst` поверх `BurstLimiter = 3`); `M4A1` — `Barrel` (норма / короткий / длинный) и `Handgrip`. Визуалы для этих опций не объявлены: сущности `M16A4` и `M4A1` не имеют спотов `Barrel`, `Stock` и `Handgrip`, поэтому до ремастера геометрии модули действуют только статами. Fold-слот приклада `M4A1` (`Modifiable = false`, `JAZZ_StockLightUnFolded` / `*Folded`) не затронут; у `CAR15` слот `Side` стал `CanBeEmpty`. Парность `items.lua` и companion проверяется `docs/tools/_audit_ar15_slots.py`.

## Inventory icons (JAZZ-UI-001)

С 2026-10-02 overlay-чипы поверх оружия отключены по решению владельца (JAZZ-UI-001, REQ-007/008). Установленные компоненты показывает сама составная иконка. `JazzAttachChips_Apply` сохраняет API для HUD/inventory/stash: не создаёт row, очищает и скрывает прежний `idJazzAttachChips` при обновлении. Native layers не затрагиваются; generic `w_mod` на firearm скрыт. Кнопки Fold/Flash UI-002 остаются.

- `Code/WeaponAttachChips.lua` остаётся loaded; lookup/list helpers сохранены для совместимости. `WeaponIconBake.lua` остаётся dormant.
- `ChipIcon` и PNG `Icons/Upgrades/Chips/` не удаляются; полные `WeaponComponent.Icon` кабинета не меняются. Asset contract не менялся.
- Проверка: offline Lua — 27 вариантов ширины (hidden/enabled/disabled, один/два предмета), очистка legacy overlay, сохранение native layers; generated sync без ошибок. Новый editor round-trip и бой после правки не проверены: оба процесса закрылись до записи.


## Ресурс, кучность и износ

`WeaponResource` (current) ограничен `WeaponResourceMax` (max); `GetFactoryResource()` — неизменяемый factory reference. Обычный ремонт может поднимать только current до max. `DegradePerShot` уменьшает current после выстрелов. Текущая `Grouping` масштабируется integer condition/repair permille multipliers, поэтому повреждение сначала ухудшает дальний CTH, а затем повышает вероятность jam/поломки.

### RepairItems: `Parts` на шкале Condition %

UI (`SectorOperation_ItemsCalcRes` в `Code/System_SectorOperations.lua`) и debit тика (`ModItemSectorOperation RepairItems` / `SectorMercsTick` в `items.lua`) считают обычные **`Parts`** по **Condition % 0..100** (`GetConditionPercent` / `current÷max`), с параметрами операции `restore_condition_per_Part=5`, `parts_per_step=1` — как vanilla tick, не по абсолютным единицам `WeaponResource` (часто 1k–10k). Регрессия remountable-волны (убрали хак `*3`, оставили absolute scale) давала сотни Parts на одно оружие (пример: ~49% при WR≈8000 → ~825). При нехватке Parts тик откатывает `WeaponResource`/`ArmorResource` к значению до тика. **`JAZZ_BarrelParts` / `JAZZ_ScopeParts`** по-прежнему через `CeilDiv(restoredPct_of_factory, 10|20)` в `System_WeaponResourceMaintenance.lua` (отдельный debit; sector-op wiring AC ещё partial). Время операции по-прежнему на absolute resource × `RepairCost` (+ `sum_stat*3` для оружия).

JAZZ-WEAPONS-002 добавляет независимый 0.5% integer-roll на каждый выстрел: при успехе max теряет не более одной единицы. При jam max теряет минимум одну единицу от 0.5% (ordinary) или 3% (critical); `P(critical|jam) = clamp(5 + wear×35/100 + max(0,100−Mechanical)×25/100, 5, 65)`. Неудачный **player** Unjam (`FirearmBase:Unjam`): −**1..3% max** (`condLoss = Clamp(DivRound(Random(100−Mechanical), 10), 1, 3)`); current clamp ≤ new max; при `max≤1` или condition%≤0 — поломка. Боевое действие `Unjam` стоит **4…1 ОД** от Mechanical (`4 - MulDivRound(Clamp(mech,0,100), 3, 100)`; `MrFixit` — perk AP). **NPC/AI** clear jam через `AIReloadWeapons` → `RepairJammed(nil)` **без** записи `WeaponResource` (раньше баг: `RepairJammed(Condition)` трактовал 0..100% как абсолютные единицы и обнулял ствол, напр. 0/9695). Runtime wave остаётся BLOCKED.

Jam использует единую шкалу **JamScore** `0..1000` (те же единицы, что `attacker:Random(1000)` в `ReliabilityCheck`). Приведённый процент для UI/ammo rollover: `DivRound(JamScore, 10)`. Окно модификации оружия показывает **Reliability**, не Jam %.

Базовый weapon score (без стрелка) уважает шкалу **Reliability 5..95**
и читает свойства через `GetProperty` (ammo/component modifiers):

```text
Reliability = clamp(Reliability, 5, 95)
if Reliability >= 95:
  base = 0                    # даже Poor/Crafted не дают базовый клин
else:
  reliability_score = max(0, 100 - Reliability)
  if BaseJamChance >= 0:
    scaled = MulDivRound(BaseJamChance, reliability_score, 95)
    base = max(reliability_score, scaled)
  else:
    base = reliability_score + BaseJamChance
base = clamp(base, 0, 100)                 # максимум 10%

condition_percent = current / max
permanent_percent = max / factory
JamScore = base
  + max(pen(condition), pen(permanent))
  + DivRound(min(pen(condition), pen(permanent)), 2)
```

При **Rel ≥ 95** платформа «вывозит» плохие патроны на базовом риске 0%;
износ ресурса по-прежнему добавляет ступени. Ниже 95 положительный
`BaseJamChance` патронов/обвеса масштабируется ненадёжностью, а не
перебивает надёжный ствол абсолютным полом. Идеальный ствол с Rel 50
(MP40) по-прежнему даёт базовые 5%.

Текущее состояние (`current/max`) и постоянный остаток ресурса
(`max/factory`) считают **одну** таблицу ступеней; в сумму идёт полный
худший штраф и **половина** второго (soft stack), чтобы mid/mid + rain ×2
не удваивали mid-риск. Середина шкалы мягче полного double-add:

| Остаток ресурса | Надбавка JamScore | Надбавка к шансу |
|---:|---:|---:|
| 100% | 0 | +0% |
| 90–99% | 10 | +1% |
| 80–89% | 50 | +5% |
| 70–79% | 55 | +5.5% |
| 60–69% | 60 | +6% |
| 50–59% | 80 | +8% |
| 40–49% | 110 | +11% |
| 30–39% | 160 | +16% |
| 20–29% | 230 | +23% |
| 10–19% | 320 | +32% |
| 1–9% | 450 | +45% |
| 0% | итог 1000 | 100% |

Если оба остатка не ниже 80%, сумма до погоды дополнительно ограничена 10%.
Затем вычитается serviceability softener
`MulDivRound(50, service², 10000)` где `service = Min(condition, permanent)`:
до **−5%** на 100% состоянии (квадратично, mid почти без скидки).
Пока оба остатка >0, raw ≤990 (display 100% только при нуле). Дождь после
этих потолков. MP40 при полном постоянном ресурсе: **0% / 2% / 7%** на
100% / 90% / 80% текущего. Mid Mosin ≈ **8%** сухо; perfect + extreme ammo ≤ **5%**.
VSS + кустарный 9×39 на 100% ≈ **1%** (было ~6% до softener).

Mechanical снижает score **пропорционально** (`MulDivRound(score, Mechanical, 120)` у мерков + малый secondary Marks/Wisdom/Level; у AI знаменатель 150). Одиночный выстрел делит score пополам через `DivRound`. `FirearmBase:GetDisplayJamChancePercent(attacker?)` отдаёт приведённый %.

`Handling` («Эргономика») удалён из Firearm / WeaponPropertyDef; CTH-модификатор отсутствует, угол overwatch берётся только из `OverwatchAngle` (`JAZZ-WEAPONS-001` / `JAZZ-ATTACH-001`).

Jam/unjam способен необратимо снизить максимальный ресурс или окончательно сломать оружие (**только** путь `FirearmBase:Unjam` с Mechanical roll). `RepairJammed(resource?, owner)`: `nil` — снять jam без износа; число — абсолютный `WeaponResource`. Карточка оружия (`RolloverInventoryWeaponBase`) выводит `GetDisplayJamChancePercent` в строке «Шанс Клина»; в `AdditionalHint` / `GetRolloverHint` jam % не дублируется. Refactor обязан сохранять шкалу 0..1000, порядок проверок, RNG и побочные изменения экземпляра.

## Боеприпасы и crafting

Ammo ModItems наследуют `Ammo`; rollover выводит модификации и effects (`BaseJamChance` как `%` через `/10`), а reload использует специализированный `AmmoInventory`. Операция CraftAmmo в UI даёт только кустарные `JAZZ_AMMO_*_Crafted` и соль (`JAZZ-INV-003`); батч = 100 Parts + порох, выход от калибра. Задумка grade: **альтернатива FMJ** — Rel/jam **между Poor и FMJ** (`Reliability` −3 / `BaseJamChance` +40; Poor винтовка ≈−4/+70, пистолет −10/+100…120), крит ≈ JHP (`CritChance` +15…25 + `Bleeding` на большинстве), pen чуть выше FMJ на пистолетах (на винтовках сейчас часто 2.0 vs FMJ 2.2). 50 `CraftOperationsRecipe` на диске включают скрытые ванильные override. 36 `RecipeDef` — главным образом преобразования брони плюс INV-004 разбор TNT/C4/PETN на порох. Категории Bobby Ray включают 10 ammo subcategories.

### Поэлементная перезарядка (JAZZ-WEAPONS-004)
`ReloadStyle=Magazine` сохраняет обычную полную смену магазина. Для `Tube`, `Break` и `Revolver` пустое оружие использует полный Reload; при `0 < ammo < MagazineSize` тот же слот Reload переключается на `Top up` / «Дозарядить» и загружает ровно один совместимый патрон (`Unit:ReloadAction` → `ReloadWeapon(..., "one_round")` → `Firearm:Reload` с `max_add=1`). Полное оружие недоступно для reload.

Стоимость дозарядки вычисляется из уже модифицированного `ReloadAP`: `max(1 AP, DivCeil(ReloadAP, MagazineSize))`. R870 (`7000`, 6) платит `2000` (2 AP); шесть дозарядок не дешевле полного reload. Tube: M1897, Ithaca, R870, Auto5, SPAS12 и Winchester1894; Break: DoubleBarrelShotgun и Stoeger; Revolver: все active revolver presets. AA12 и USAS12 не имеют authored style и остаются `Magazine`.

### Пробитие патрона (`PenetrationClass` + `PenetrationBonus`)

Контракт данных и UI (канон skill `.agents/skills/jazz-penetration-scales/SKILL.md`):

```text
tenths = DivRound(mod_mul_or_1000, 100) + mod_add_bonus
display = "W.F"   -- 9 → 0.9, 22 → 2.2
```

Боевой pen: `GetAttackPenetrationClass` = `PenetrationClass + 0.1×PenetrationBonus` — см. [броня/урон](armor-damage-wounds-will.md).

`Ammo:GetRolloverHint` склеивает оба модификатора в одну строку и передаёт **`Untranslated` строку**, не Lua float: подстановка числа в `T{}` усекает к нулю (`0.9` → `0`). Форматтер патрона: `FormatAmmoPenetrationDisplay`. Карточка заряженного оружия (`RolloverInventoryWeaponBase`, bind `PenetrationClass`) показывает ту же дробь через `FormatWeaponPenetrationDisplay` (класс + десятые `PenetrationBonus`), не сырой целый класс.

Не ставить `mod_mul = 0` на `PenetrationBonus`: `MulDivRound(base+add, 0, 1000)` зануляет add в бою (`.30 Cal` FMJ tooltip 1.6 / карабин 1.0). Соль: `mod_mul = 0` только на `PenetrationClass`. Аудит: `docs/tools/_audit_ammo_pen_mul_zero.py`.

Не делать `DivRound(mul, 100) * 10 + bonus` (двойной масштаб → 202) и не путать с jam `%` (`/10`).

### Трассерные боеприпасы

Наличие `MarkedTraccers` в `Ammo.AppliedEffects` включает shot-level правило: выбранная unit-цель получает один stack за каждый фактически произведённый выстрел, если итоговый шанс этого выстрела `shot_cth > 0`. Попадание не требуется, поэтому маркер отражает трассирующий/подавляющий огонь; при невозможном выстреле с CTH `0`, jam или отсутствии произведённого выстрела stack не добавляется.

`MarkedTraccers` исключён из обычного `hit.effects`, чтобы попадание не добавляло второй stack. Остальные ammo/body-part effects остаются hit-level и применяются только при отсутствии закрывающей брони либо при её пробитии.

## Дубли и порядок загрузки

Канонические `FirearmBase:GetScrapParts` / `ItemWithCondition:AmountOfScrapPartsFromItem` живут в `GetScrapParts.lua` (грузится после `System_OR_Weapons.lua`); late override `AmountOfScrapPartsFromItem` (resource%) и `GetSpecialScrapItems` — в `System_WeaponResourceMaintenance.lua`. Штраф Condition/resource&lt;50 (`/20`) применяется только в `AmountOfScrapPartsFromItem`. **Scrap eject** (`JAZZ_EjectRemovableAttachmentsForScrap`) копирует remountables в сумку и **не** вызывает `SetWeaponComponent` (иначе loaded loot с Magazine делает `ReloadWeapon` на `weapon.owner` и рвёт SCRAP ALL). Special scrap: сумма `AdditionalCosts` типа `JAZZ_BarrelParts`/`JAZZ_ScopeParts` при успешном Mechanical roll — **без** `component.Cost`. `GrenadeLauncher`/`RocketLauncher`/`Mortar:GetBaseDegradePerShot` в `WeaponClasses.lua` (после `System_OR_Grenade.lua`) возвращают `self.DegradePerShot or const.Weapons.DegradePerShot_*`.

## Межпакетные зависимости

- core item definitions ссылаются на entities и состояния из `jazz_assets`;
- `jazz-units` выдаёт оружие и ammo через UnitData/loot definitions;
- `jazz-maps` размещает оружие, контейнеры и loot;
- sound/FX modules связывают weapon IDs с presets и аудиоресурсами.

Переименование item, caliber, component, effect, slot или entity ID требует поиска во всех четырёх репозиториях.

## Проверка

- текущее состояние и permanent max отдельно на 100/90/80/70/60/50/40/30/20/10/0; MP40 5/6/10% на 100/90/80, Mosin `3280/6507/7000` 27–36%; сухая погода/дождь;
- single/burst/auto, unjam, repair и окончательная поломка;
- деградация Grouping и совпадение CTH UI;
- установка/снятие каждого класса компонентов, folded/unfolded визуал;
- reload из правильного ammo slot и отказ для неподходящего калибра;
- ammo rollover: Penetration = `(mod_mul/1000) + (PenetrationBonus/10)` (не целое ×100), jam `%` через `/10`;
- трассерный одиночный/серийный огонь: попадание и промах при CTH больше нуля, CTH `0`, jam и нехватка патронов;
- обычные ammo effects при непробитой и пробитой броне;
- scrap и crafting recipes;
- save/load экземпляра с неполным и уменьшенным максимальным ресурсом;
- AI с модифицированным оружием.

## Сопровождение

При изменении свойств, component effects, калибров, jam/degrade или generated items обновлять эту страницу, соответствующие таблицы data snapshot и тесты. Для изменений duplicated methods обязательно проверить `metadata.lua`. Наблюдаемый игроком current-state контракт фиксируется на этой technical-странице; target behavior — в связанной spec.

## vz. 58 — локальный ввод 26.09.2026

`JAZZ-WEAPON-VZ58-001`: новый `InventoryItem/VZ58.lua`, items.lua и metadata.code регистрируют AssaultRifle 7.62x39, Tier 2-2. Damage 27, 30 патронов, ShootAP/ReloadAP 5/6 AP, Recoil 23, Reliability 85, масса 2.9 кг, RPM 800, очереди 4/8. Bobby in: BR Tier 2, RW 55, MaxStock 2, Cost 6000, AssaultRifles. Это стартовый баланс для плейтеста.

Основа — классический VZ.58P с родной мебелью и открытыми прицелами. Семь слотов: Scope, Magazine, Handguard, Handgrip, Under, Stock, Muzzle. Три приклада: штатный фиксированный (`JAZZ_StockNormal`), металлический VZ.58V (`JAZZ_StockLightUnFolded` / `JAZZ_StockLightFolded`), современный скелетный (`JAZZ_StockHeavy`). Металлический приклад складывается и раскладывается штатными FoldStock/UnFoldStock за 4 AP; используются существующие эффекты пары. Сложенный вариант скрыт в списке установки и включается через HUD. Старый ApplyTo для `JAZZ_StockLight` сохранён для уже созданных экземпляров, но в списке установки его заменяет складная пара. Modernized также даёт эргономичную пистолетную рукоять, цевьё RIS, переднюю рукоять, коллиматор, глушитель и петлю быстрой перезарядки на родном магазине. Использованы существующие эффекты 16 компонентов; новый частный `JAZZ_VZ58_HandguardWood` наследует штатное имя цевья и имеет `BlockSlots={Scope,Under}`. Кабинет требует сначала RIS для коллиматора/передней рукояти, а перед возвратом штатного цевья — снять их. Runtime setter дополнительно не изменялся.

Визуалы — только `ApplyTo=VZ58`, базовый корпус не содержит съёмную мебель. 14 сущностей `jazz_assets/Entities/JAZZ_VZ58*.ent`, соответствующие `Meshes/JAZZ_VZ58*_Mesh.m.hgm`, `Materials/JAZZ_VZ58*_Mesh.mtl`, 30 пар `Textures/JAZZ_VZ58_*.dds`/fallbacks, `WeaponIcons/VZ58.png` 324×165. Родные UV/PBR обоих архивов; исключение — металлический приклад, для которого предоставлена только одна почти белая scalar-карта: она используется как AO, а отсутствующий albedo заменён нейтральным gunmetal (.18/.19/.20), roughness .65, metallic .7. Классическая длина 0.845 м, без custom normals. Геометрия проверяется из HGM v14, включая модели с двумя материалами.

В восьми обычных пулах Легиона добавлены только рассчитанные генератором записи от Amount 22 до 29, вес 102000; три комбинации `JAZZ_GenW_VZ58_*` дают штатную сборку и существующие 7.62x39-патроны. Отдельных новых предметов обвеса/магазинных SKU нет; базовое цевьё — integral/default, Bobby out.

Уровень подтверждения: static и offline visual, включая Lua/метаданные, зависимости, 160 допустимых конфигураций и скомпилированную геометрию. Editor save/reload, игровой хват, материалы, звук, стрельба и смена компонентов в игре ещё не проверены. Незакоммиченное изменение трёх пакетов; публикации нет.

Визуальная корректировка Mosin (2026-09-27): `jazz_assets/Entities/Textures/MOSIN_7_Base.dds` и `Entities/Textures/Fallbacks/MOSIN_7_Base.dds` получили локальную цветокоррекцию красного дерева M38 в коричневый тон длинной Mosin. BC1 sRGB, UV, размеры 2048/64 и mip-цепочки 12/7 сохранены; нейтральные блоки побайтно прежние. `jazz_assets/Entities/MOSIN_Obrez.ent`: Hand_l_grip X=8 вместо текущего X=5 (30 мм вперёд), Y/Z прежние. Mesh/material references, items/metadata/companion не меняются. Static PASS; игровой вид и editor round-trip не проверены, существующий generated baseline имеет 142 ошибки / 13 предупреждений. Инструмент: `docs/tools/_repair_mosin_visuals.py`.

Повторная итерация 2026-09-27: скриншоты владельца подтвердили, что одной коррекции рыжины M38 недостаточно. `_match_mosin_wood.py` установлен на `jazz_assets/Entities/Textures/MOSIN_7_Base.dds`, `MOSIN_11_Base.dds` и одноимённые `Fallbacks/`. Маска дерева берётся из исходных RM (B < 24, R > 24) и уменьшается для всех mip/fallback. Светлота и оттенок сведены к диффузной доле старого материала: linear BC7 `Mosin_BASE.dds` × (1 − metallic из `Mosin_RM.dds`), затем sRGB; целевая медиана примерно 72/60/50. Это приближение диффузного цвета, не эквивалент полного BRDF: RM и различия отражения сохранены. BC1 endpoints изменены без перепаковки UV/индексов рисунка; перестановка индексов допускается только для сохранения режима BC1. Заголовки, размеры, mip-цепочки и блоки вне маски прежние. Рисунок древесины сохранён с уменьшением контраста тёмного зерна. Длинная модель, RM, геометрия, хват, регистрации и баланс прежние. Static PASS; совпадение под игровым освещением ещё требует human/runtime проверки (REQ-008, AC-007/008).

### Исправление визуалов VZ58 / R4, 27.09.2026

Установленные `JAZZ_VZ58*` (14 сущностей) и `JAZZ_VektorR4` пересобраны после обнаруженного в игре backface culling: recalc на разорванных UV-швах разворачивал полосы поверхности внутрь. Совпадающие позиции соединены с допуском 0.1 мкм, затем выполнен recalc наружу; сторона открытых островов сохранена по исходному winding. Число треугольников и пары position/UV каждого угла сохранены, custom normals отсутствуют. Проверка теперь сравнивает направления с донорскими OBJ и скомпилированный winding, а не только наличие треугольников.

У VZ58 две BaseColor atlas-карты мебели заменены приглушёнными коричневыми вариантами с прежней UV-раскладкой; минимальная roughness неметаллических участков 0.72. Обновлены иконки обоих предметов. Имена ресурсов, материалы, ModItem/metadata, параметры и компонентные контракты не менялись. Резервные копии и offline evidence: `_vz58_repair_20260927`, `_r4_repair_20260927`. Игровой дефект подтверждён скриншотами владельца; после установки визуальная приёмка не завершена: Computer Use остановлен Escape, позднее DAP :8165 уже не принимал соединение.

## Материалы VZ58/R4: повторная коррекция 27.09.2026

По дополнению JAZZ-WEAPON-VZ58-001 установлены две новые albedo-развёртки мебели VZ58 с тёмными продольными волокнами по референсу штатного AKM (`jazz_assets/Entities/Textures/JAZZ_VZ58_11_Base.dds`, `JAZZ_VZ58_26_Base.dds`, парные fallbacks). Рельеф normal maps VZ58 Steel/Mag/Wood/StockWood ослаблен с нормализацией tangent-векторов; metal roughness floor 0.66, существующий wood floor 0.72 сохранён. У R4 ослаблен normal map, metal roughness floor 0.62. Это художественная коррекция чрезмерного рельефа, не доказательство полной совместимости исходного bake с tangent basis.

У R4 разделены геометрические стыки с углом >60 градусов без custom normals. Удалён один почти коллинеарный треугольник площадью 1.57e-9 м², после чего исчезло предупреждение FBXImporter о нулевых нормалях. `jazz_assets/Entities/Meshes/JAZZ_VektorR4_Mesh.m.hgm` содержит 13508 треугольников; оставшиеся position/UV пары сохранены. HGM surface/winding audit PASS, отклонение <0.026 мм. MTL/ENT/ModItem/metadata и пути ресурсов не изменены.

`WeaponIcons/VZ58.png` 324×165 теперь рендерится отдельной горизонтальной боковой камерой; прежний экспорт по ошибке оставлял камеру после threequarter preview. Проверены 26 установленных файлов: хэши, DDS размеры/кодирование/fallback, снижение амплитуды normal maps, RGBA иконки. Уровень evidence: static/offline; новый материал в работающем процессе и editor save/reload ещё не проверены. Scope VZ58 расширен до четырёх вариантов: закрытый, компактный, EOTech и M68. Новые варианты используют уже зарегистрированные generic Scope visuals; требование RIS сохранено. items.lua/companion синхронизированы, metadata без изменений, каталог содержит 16 опций в семи слотах. `_check_vz58.py`: 352 допустимые конфигурации PASS; editor/runtime round-trip ещё не выполнен.

Кабинет модификации (`JAZZ-WEAPONS-002`, REQ-010/011): `JazzFindRemovableAttachmentItem` ищет съёмный модуль у владельца оружия, затем в общей сумке, затем у остальных бойцов того же отряда в порядке `squad.units`. Для бойцов применяется тот же `JazzGetOwnerUnit`, что и для владельца. Проверка доступности и установка используют этот helper; фактический контейнер передаётся `JAZZ_InstallRemovableAttachment` для списания. Склады и другие отряды не включены. Asset contract и формат сохранений не меняются. Уровень проверки дополнения: offline Lua; игровой UI ещё не проверен.

## Авторские карты и магазины АК103 — 03.10.2026

Установлен кандидат AEK971 (`JAZZ-WEAPON-AEK-001`): один InventoryItem, Barrel-комплекты `JAZZ_AEK_545` / `JAZZ_AEK_762`, авторские модели 971/973С, штатный магазин и пара StockLight. Калибр и числовые дельты принадлежат штатным WeaponComponentEffect; методы класса в `Code/Weapon_AEKModular.lua` меняют имя, Entity, части и Icon, не заменяя общий setter. Заряженный экземпляр без владельца/сумки отклоняет смену комплекта до мутации; штатный ChangeCaliber разгружает патроны владельца, clone не изменяет инвентарь. Непроверенный внешний обвес исключён. Source/compiled geometry+winding и offline Lua переходы PASS; editor round-trip, native save/load и осмотр в игре ещё не выполнены. [Отчёт](../../design/aek-import.md).

По уточнению владельца установлены исходные BC/NM/roughness/metallic VZ58/R4/АК103: отменены предыдущие художественные normal-strength/roughness floors и замена мебели VZ58. 50 карт, 100 DDS с fallbacks; RM=(rough,rough,metal), исходный Y сохранён без автоматического flip. АК103 использует первоначальные native UV-атласы. Ресурсный контракт и имена `jazz_assets/Entities/Textures/{JAZZ_VZ58,JAZZ_VektorR4,AKR_AK103}_*.dds` не изменились; меши/UV/MTL сохранены. Это установленный кандидат, не подтверждённое исправление всех теней.

Штатный JAZZ_MagNormal для АК103 в items.lua теперь использует AKMWaffleMag и его Icon. Существующий `Code/System_WeaponComponent_Set.lua` задаёт абсолютные offsets (мм): normal (6,-9,-9), quick/40 (3,-10,-2), drum (-9,-10,-8). Ёмкость и баланс прежние. Metadata не менялась, отдельного companion у WeaponComponent нет. Static/generated gates PASS; editor round-trip, новые фотографии составных иконок и визуальная приёмка владельца открыты. [Точные источники и аудит](../../design/weapon-texture-audit-20261003.md).

Дополнение того же прохода: по разрешению владельца ещё 35 RM (70 DDS/fallback) для AKM/74/74M/105, M4/M16, M14/Mk14, L42A1, Mosin и обвеса FAL приведены к R=G=roughness; B и исходная R сохранены на входе. BC/NM/AO/геометрия не менялись. Повторный аудит: отклонений упаковки RM нет; NM M14 MkIII требует отдельной диагностики.

Mosin (MOSIN-001 REQ-011, 03.10.2026): загруженный `Code/Weapon_MosinModular.lua` задаёт М38/обрезу `WeaponType=BattleRifle`, `object_class=BattleRifle`, `ImpactForce=2` и атаки `SingleShot/JAZZ_Salvo`; длинной — `Sniper/SniperRifle`, `ImpactForce=0`, `SingleShot/JAZZ_JokerShot/JAZZ_Bullseye`. Локальная копия `__ancestors` экземпляра переключает SniperRifle/BattleRifle без изменения общей Mosin. ID/метатаблица Mosin сохранены для сериализации, FX и модулей. Профиль восстанавливается в SetWeaponComponent, Setcomponents (загрузка/клонирование property list) и UpdateVisualObj. Статические Lua-проверки переходов, изоляции экземпляров и прежнего ПУ-контракта PASS; native IsKindOf, hotbar и полное save/load в игре ещё не проверены. Media/asset contract прежний.


03.10.2026, R4/VZ58: установлены `jazz_assets/Entities/Meshes/{JAZZ_VektorR4,JAZZ_VZ58}_Mesh.m.hgm` с восстановленными авторскими OBJ hard boundaries через разделение топологии без custom normals; 13508/9640 треугольников, поверхность/UV сохранены. Обновлены `WeaponIcons/{VektorR4,VZ58}.png`. 83 material/texture SHA guards неизменны. Public asset contract, spots, предметы и регистрация не менялись. Compile/surface/winding PASS; runtime/human PENDING. Кандидат с дополнительными фасками отклонён и не установлен. Evidence: [повторная проверка](../../design/weapon-shading-recheck-20261003.md).


Дополнение оптики/обвеса 03.10.2026: `InventoryItem/AEK971.lua` и его ModItem синхронно получают Scope с JAZZ_Reflex_Closed/Eotech/M68 и JAZZ_CombatScope_2x/ACOG, пустой по умолчанию и общий для 971/973С. HK416 получает Under (JAZZ_GrenadeLauncher/VerticalGrip/TacGrip) и Side (пять штатных лазерных/световых модулей). Для M203 и вертикальной рукоятки добавлены ApplyTo=HK416 visuals с WeaponAttA_GrenadeLauncherM14/VerticalGripCAR15. Нет новых preset ID или изменения регистрации. `jazz_assets/Entities/JAZZ_HK416_{Short,Standard,Long}.ent`: Scope/Mount Z=14.5 см, Under/Side spots добавлены; компиляция шести деталей завершена. Исправлен лишний разворот порядка MLOD corners после отражения Y/Z: открытые внешние панели прежде смотрели внутрь. UV corner pairing и все texture bytes сохранены. Передача на игровой тест: 11 offline проверок каждого семейства, M203 subweapon/grenade conservation, compiled winding, physical exterior regression и пять геометрических примерок; editor/runtime NOT_RUN. Подробности: [отчёт](../../design/weapon-shading-recheck-20261003.md).
