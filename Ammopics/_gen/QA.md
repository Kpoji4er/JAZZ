# Ammo icon generation — QA pass (обязательно)

Маркировка и типы — из Google Sheet / design table (колонки **Маркировка** + **Тип** + цвет легенды), не «от балды».

## Силуэт = на калибр

**У каждого калибра свой канонический силуэт.**  
Типы внутри калибра (FMJ / AP / Poor / Crafted / …) шарят **один** outline; чужой калибр не подмешивать.

| Калибр (серия) | Канон силуэта (alpha-реф) |
| --- | --- |
| 9×19 | `Ammopics/919FMJ.png` |
| 9×18 | `Ammopics/9x18.png` |
| .45 ACP | `Ammopics/45ACP.png` |
| 5.7×28 | `Ammopics/57.png` |
| 4.6×30 | `Ammopics/46.png` |
| 7.62×25 | `Ammopics/762x25.png` |
| .38 Spl | `Ammopics/38Sp.png` |
| .357 | `Ammopics/357.png` (сначала довести до 110×110) |
| .44 | `Ammopics/44FMJ.png` |
| .50 AE | `Ammopics/50AE.png` |
| .30 Carbine | `Ammopics/30cal.png` (сначала 110×110) |
| 5.45×39 | `Ammopics/545.png` |
| 5.56×45 | `Ammopics/556.png` |
| 7.62×39 | `Ammopics/762x39PS.png` |
| 7.62×51 | `Ammopics/762NATO.png` |
| 7.62×54R | `Ammopics/762x54RLPS.png` |
| 7.92×33 | `Ammopics/792x33.png` (сначала 110×110) |
| 7.92×57 | `Ammopics/792x57.png` |
| 9×39 | `Ammopics/939SP5.png` |
| 12 Gauge | `Ammopics/12gBUCKSHOT.png` |
| 7.5×54 | `Ammopics/75.png` |
| .30-06 | `Ammopics/3006.png` |

Новый калибр → взять лучший существующий PNG этой серии как `--silhouette` (обычно базовый FMJ/Army).  
Не лочить 5.45 на `919FMJ` и т.п.

## После GenerateImage

1. `Read` итогового PNG (не только описание в чате).
2. Чеклист:
   - [ ] ¾ коробка, прозрачный/чёрный фон, canvas **110×110**
   - [ ] silhouette-lock на **реф этого калибра**; IoU alpha vs ref ≥ 0.99
   - [ ] семья упаковки верная (NATO metal / surplus / craft / Warsaw / shotgun…)
   - [ ] **Substandard** = грязно-зелёная доминанта + читаемая маркировка из таблицы
   - [ ] **Crafted** = грязно-коричневая доминанта
   - [ ] цвет **полосы/акцента** = тип из легенды
   - [ ] боковой/лицевой код = **Маркировка** таблицы
   - [ ] **текст читается** (2 крупных штампа; нет каши/микропечати на крышке)
   - [ ] соседние типы серии не путаются
3. FAIL → re-gen с узким промптом → lock → Read снова.
4. На один файл допускать **до 10 QA-проходов** (gen/lock/Read). После 10 FAIL — стоп и эскалация владельцу, не «принять как есть». Статус по файлам — `Ammopics/_gen/QA_LOG.md`.
5. PASS → `_gen/` или replace runtime.

```text
GenerateImage on solid **#FF00FF magenta** plate (not black — shadows merge with void)
→ Read QA (цвет / маркировка / семья)
→ python docs/tools/_finalize_ammo_gen_batch.py drafts... \
     --silhouette Ammopics/<CANON_FOR_CALIBER>.png \
     --key magenta --fit contain --choke 2 --rim-plate 0 --soft-outline 0.35
→ Read (силуэт / soft alpha как у vanilla; **без** `--hard-alpha` — бинарный край рвёт на чёрном UI)
```

`--key magenta` — chroma-key `#FF00FF` (авто, если углы уже magenta). `--choke` после downscale. `--rim-plate` обычно 0 (светлый cardboard-rim = ореол на чёрном UI).
Пример 9×19: `--silhouette Ammopics/919FMJ.png`.  
Пример 9×18: `--silhouette Ammopics/9x18.png` (семейство ПМ-картона; тип — mid wrap band, не пунктир/нижняя полоска).

Маркировка 9×18 (таблица): `57-Н-181С` / `ПСО` / кустарный / `СП-7` / `ПСТ` / `7н25` + бок `ПМ`★.

## Текст на иконке (обязательно)

На 110×110 AI часто **ломает кириллицу** до нечитаемых клякс — поэтому **крупно** и мало строк.

1. **Максимум 2 крупных штампа:** калибр + код типа.
2. **Запрет:** мелкая «полиграфия» на крышке, псевдо-кириллица/каракули, 3+ строк, barcode-текст.
3. **Русские/Warsaw патроны** (9×18, 9×19 7н*, 5.45, 7.62×39, 7.62×54R, 9×39, 7.62×25…): штампы **кириллицей** как в DisplayName/таблице (`ПСО`, `ПСТ`, `СП-7`, `7н25`, `ПС`, `БП`…). Цифры калибра (`9x18`) ок латиницей/арабскими.
4. **NATO/US** серии: латиница (`FMJ`, `M855`, `AP`…).
5. FAIL по читаемости → re-gen (до 10 проходов), не «добивать» мелким stamp поверх всей коробки.
6. Идём **батчами по калибру**; следующий батч только после PASS текущего.
