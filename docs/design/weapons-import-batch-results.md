# Пакетный импорт JaWeapons — 2026-09-23

**Это импорт исходников в Blender, не установка предметов в JA3.** Игра не запускалась, активные моды не менялись.

IMPORTED_SOURCE: сцена с назначенными материалами, UV и без оставшихся ошибок mesh-аудита; это ещё не rig/entity/InventoryItem. IMPORTED_REVIEW: сцена сохранена, но материалы/UV/геометрия требуют исправления.

Все 47 созданных сцен повторно открыты. Оригиналы не изменены. Сцена Mk 12 хранится только как диагностика отвергнутого источника.

Корень результатов: `Weapons/_batch_jazz_import/`; в каждой папке `source-state.json`, `source/`, `clean/Source.blend`, `review/`, `import-report.json`. Общие превью: `contact-01.png` … `contact-04.png`.

| # | Источник | Решение | Мешей | Без материала / UV | Ошибок геометрии | Причина |
| ---: | --- | --- | ---: | --- | ---: | --- |
| 1 | Walther PPK.zip | IMPORTED_SOURCE | 2 | 0 / 0 | 0 |  |
| 2 | _Paektusan_ Gifted Pistol.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 3 | Automag 5.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 4 | eft_mp-443_grach.glb | IMPORTED_SOURCE | 9 | 0 / 0 | 0 |  |
| 5 | Browning FN 1910.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 6 | AEK 919  Каштан.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 7 | 9A-91 Assault Rifle Gameready Lowpoly.zip | REJECT | 0 | 0 / 0 | — | No weapon textures or material definitions; geometry only |
| 8 | HK51 (MC51) - aka Full Auto Flashbang Dispenser.zip | IMPORTED_REVIEW | 6 | 6 / 0 | 0 |  |
| 9 | kiparis_sur.rar | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 10 | PP-91 Kedr.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 11 | PP-91-01 Kedr-B.zip | IMPORTED_REVIEW | 3 | 1 / 1 | 0 | Body and suppressor atlases restored; model_2 lacks UV (internal/auxiliary geometry visible in isolated review). Keep whole-source review; do not export untextured mesh. |
| 12 | PP-2000 submachine gun game model.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 13 | Beretta MX4 Storm.zip | IMPORTED_SOURCE | 27 | 0 / 0 | 0 |  |
| 14 | sa_vz._26.glb | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 15 | SA VZ. 25 And VZ. 23 Stock.zip | IMPORTED_REVIEW | 2 | 2 / 0 | 0 |  |
| 16 | Sterling L2A3.zip | IMPORTED_REVIEW | 2 | 2 / 0 | 0 |  |
| 17 | Sterling L34A1.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 18 | Sterling.zip | IMPORTED_SOURCE | 4 | 0 / 0 | 0 |  |
| 19 | Izhmash AK-103.zip | REJECT | 0 | 0 / 0 | — | No weapon textures or material definitions; geometry only |
| 20 | Drum_762x39_75rnd.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 21 | pbs-1-1.zip | IMPORTED_REVIEW | 1 | 0 / 0 | 48 |  |
| 22 | AEK - 973S.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 23 | AEK 971 Assault Rifle.zip | IMPORTED_REVIEW | 2 | 2 / 0 | 0 |  |
| 24 | Hk G11 K2.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 25 | HK416.zip | IMPORTED_REVIEW | 26 | 26 / 1 | 0 | model_17 without UV is a circular accessory detail; rest of weapon has UV. Material sets still require explicit mapping. |
| 26 | hk-xm39-oicw.zip | IMPORTED_SOURCE | 8 | 0 / 0 | 0 |  |
| 27 | FN F2000 Assault Rifle.zip | IMPORTED_SOURCE | 9 | 0 / 0 | 0 |  |
| 28 | FN SCAR Rifles.zip | IMPORTED_REVIEW | 73 | 73 / 1 | 0 | model_39 is a tiny planar strip (12 vertices/16 faces), not the receiver; main meshes have UV. Material sets still require explicit mapping. |
| 29 | H&K G36 Rifle Family.zip | IMPORTED_REVIEW | 14 | 14 / 0 | 0 |  |
| 30 | H&K XM8 Family.zip | IMPORTED_REVIEW | 57 | 57 / 0 | 0 |  |
| 31 | Polish FB Beryl pack.zip | IMPORTED_REVIEW | 41 | 41 / 0 | 0 |  |
| 32 | Carl Gustaf M2 Recoilless Rifle.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 33 | GM-94 Grenade Launcher.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 34 | HK69A1 _ Grenade Launcher.zip | IMPORTED_REVIEW | 2 | 2 / 0 | 0 |  |
| 35 | M1A1 Bazooka Anti-tank Rocket Launcher.zip | IMPORTED_REVIEW | 2 | 2 / 0 | 144 |  |
| 36 | M202 FLASH Rocket Launcher.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 37 | Panzerfaust 3 Anti-tank Rocket Launcher.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 38 | RPG-22 A.zip | IMPORTED_REVIEW | 1 | 0 / 0 | 60 |  |
| 39 | M72 LAW.zip | IMPORTED_REVIEW | 2 | 2 / 0 | 0 |  |
| 40 | M72 LAW light Anti Tank Weapon.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 41 | Just A Hatchet.zip | REJECT | 0 | 0 / 0 | — | No weapon textures or material definitions; geometry only |
| 42 | Sledge Hammer.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 43 | PKM.zip | IMPORTED_REVIEW | 1 | 1 / 0 | 0 |  |
| 44 | pkp_pecheneg_sur.rar | IMPORTED_REVIEW | 1 | 1 / 0 | 0 |  |
| 45 | SCP Secret Laboratory - Logicer LMG (HK MG5).zip | IMPORTED_REVIEW | 49 | 49 / 0 | 0 |  |
| 46 | 1404127105_lmg_m240_hrp3dm.ru.rar | SKIP_DUPLICATE | 0 | 0 / 0 | — | M240 duplicates existing MG58/FN MAG; source FBX 6100 also unsupported by Blender. No new item. |
| 47 | mg3.zip | IMPORTED_SOURCE | 11 | 0 / 0 | 0 |  |
| 48 | mg4.zip | IMPORTED_SOURCE | 15 | 0 / 0 | 0 |  |
| 49 | negev_counter_strike_2.glb | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 50 | MK14 AAA Game Ready PBR Low-poly 3D model.zip | IMPORTED_SOURCE | 1 | 0 / 0 | 0 |  |
| 51 | Mk 12 Special Purpose Rifle.zip | REJECT_INCOMPLETE | 13 | 13 / 11 | 0 | Visual check: 11 OBJ without UV include receiver, stock, handguard, barrel and magazine; only scope/bipod textured. Scene retained for diagnosis. |

## Следующий этап игрового импорта

Нужны отдельные решения по семействам/модулям, сборка разобранных моделей и ориентирование, масштаб по АК74М, привязка к руке, spots, строгий экспорт HGE/FBX → AssetsProcessor, проверки HGM/DDS, регистрация согласованных ModItem/metadata/companion, иконки и локализация. Существующие ID не дублировать. Editor/runtime-приёмка остаётся на последующий запуск владельцем.

Особые зависимости: PPK/FN1910 ждут .380 ACP; G11 — безгильзовых патронов; OICW — двухствольной механики; гранатомёты — боеприпасов; SCAR/G36/XM8 — матрицы модулей. Наличие clean.blend не закрывает эти требования.
