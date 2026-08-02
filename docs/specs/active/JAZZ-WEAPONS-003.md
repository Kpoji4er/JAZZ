---
id: JAZZ-WEAPONS-003
status: implemented
owner: project-owner
systems:
  - weapons-ammo-components
  - combat-cth-actions
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/AccuracyRangeCTH.lua
  - jazz/Code/System_Firearm_AddProperties.lua
  - jazz/InventoryItem/*.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/CharacterEffect/AutoWeapons.lua
  - jazz/Localization/Russian.csv
  - jazz/Localization/English.csv
  - jazz/docs/specs/active/JAZZ-WEAPONS-003.md
  - jazz/docs/design/recoil-physical-scale.md
  - jazz/docs/tools/_audit_recoil_dist.py
  - jazz/docs/tools/_rebalance_recoil_physical.py
  - jazz/docs/tools/README.md
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/technical/weapons/combat-actions.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/data/weapons.csv
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-CTH-001
  - JAZZ-WEAPONS-001
  - JAZZ-ATTACH-001
approved_by: project-owner
---

# JAZZ-WEAPONS-003: отдача очереди + RPM→Burst/Auto (физика ствола + Marks + AutoWeapons)

## Проблема

1. **Очередь / авто слишком эффективны в плейтесте.** Retention уже multiplicative, но числа `Recoil` слабые под `retention = 1 − effective_recoil/100`.
2. Медиана `Recoil` ≈ **7**; при Str/Marks≈80 очередь AR почти не сыпется; автопистолеты с `Recoil=1` почти flat.
3. **Одинаковый калибр не различает платформы:** два 9×19 ПП (MicroUZI vs MP5 vs Sterling) почти не читаются по отдаче — нет массы/темпа/длины как авторских входов.
4. Контроль отдачи учитывает только **Strength** (+ stance/support/class/action) и `AutoWeapons` ×0.85; **Marksmanship** не входит.
5. Текст `AutoWeapons` врёт («с 5-го выстрела без отдачи»), runtime — только ×0.85.

Канон pipeline: `JAZZ-CTH-001` / `accuracy-model.md`. Этот spec — **физическая калибровка Recoil + новые статы Mass/RPM/Size + authored Burst/Auto из RPM + shooter Marks + честный AutoWeapons**, не смена модели на линейное −CTH.

## Текущая математика (runtime as-is, каркас остаётся)

Факторы severity **перемножаются**, затем геометрический decay:

```text
effective_recoil =
    action_recoil          # обычно = weapon.Recoil; MGBurst ×0.8; Fanning special
  × shooter_factor         # после этого spec: 0.5×Str + 0.5×Marks
  × stance_factor
  × support_factor
  × perk_factor            # AutoWeapons 0.85
  × action_factor
  × class_factor

retention = clamp(1 − effective_recoil/100, 0.15, 1)
P_bullet(i) = clamp(round(P_first × retention^(i−1−protected)), 2, 100)
```

**Mass / RPM / SizeClass не умножаются повторно в runtime** — они входят в **authored `Recoil`**, иначе двойной учёт.

## Цели

1. Добавить на Firearm авторские статы **`WeaponMass`**, **`CyclicRPM`**, **`WeaponSizeClass`**, **`BurstLimiter`** (механическая отсечка).
2. Пересчитать **`Recoil`** всех активных стволов по физической шкале (калибр-импульс × масса × размер × RPM), с валидацией якорей AK74 / AKM / FAL.
3. Два ствола одного калибра **должны отличаться**, если отличаются масса / длина / темп (пример: MicroUZI vs MP5 vs Sterling на 9×19).
4. Пересчитать **`BurstShots` / `AutoShots`** из `CyclicRPM` (+ отсечка): Auto≈RPM/100, Burst≈RPM/200.
5. Marksmanship в shooter-контроле (50/50 со Strength); `AutoWeapons` = снижение severity + честный RU/EN текст.
6. Floor **2%** на любую пулю очереди; FAL «плохо», но не в ноль.
7. Docs: technical + wiki + showcase RU/EN + design table.

## Non-goals

- Runtime-множитель Mass/RPM поверх Recoil (только authoring → Recoil).
- Смена делителя retention `/100` / линейное вычитание CTH.
- Масштаб абсолютных `Recoil±` на аттачах — follow-up (после нового base абсолютные −N станут относительно слабее).
- **Случайная / непредсказуемая длина очереди** (variance ±N) — отвергнуто как design; длина fixed и читаемая.
- Runtime-пересчёт Burst/Auto каждый выстрел из RPM (числа **authored** на preset, как Recoil).
- Полный IRL-симулятор импульса/дульной энергии; достаточно **относительной** шкалы внутри семейств.
- Новые перки / rename `AutoWeapons`; ребаланс Damage/AP/Accuracy.

## Новые свойства оружия

Добавить в `FirearmProperties` (`System_Firearm_AddProperties.lua`) + заполнить все активные `InventoryItem` / `items.lua`:

| Property | Тип | Единицы / значения | Назначение |
| --- | --- | --- | --- |
| `WeaponMass` | number | **десятые кг** (35 = 3.5 kg), empty+типичный mag IRL-округление | инерция платформы |
| `CyclicRPM` | number | выстр/мин циклический (600, 800, 1200…) | Recoil rpm_f + источник Burst/Auto |
| `WeaponSizeClass` | enum/text | `Compact` / `Carbine` / `Rifle` / `Long` | прокси длины ствола / OAL / рычага |
| `BurstLimiter` | number | **0** = нет отсечки; **2/3/…** = max пуль в `BurstFire` | механическая отсечка (M16A2=3, AN94=2) |

Правила авторства:

- Масса — **округлённый IRL** (не игровой «вес инвентаря»); одна цифра на preset (без магазинов-исключений).
- RPM — типичный cyclic rate платформы (не semi-only «0»: для чисто semi RPM может быть 0 → Burst/Auto=0 если нет режима).
- SizeClass: Compact (PDW/SMG-K/автопистолет), Carbine (ПП полный / короткий AR), Rifle (штатный AR/BR), Long (снайпер / удлинённый).
- BurstLimiter — только где есть железная отсечка; иначе 0.

UI карточки оружия: Mass/RPM/BurstLimiter **не** показывать игроку в этом spec (только editor / CSV / debug). SizeClass — editor-only. `BurstShots`/`AutoShots` как сейчас видны через режимы огня.

Экспорт: колонки `weapon_mass`, `cyclic_rpm`, `weapon_size_class`, `burst_limiter` (+ обновлённые `burst_shots` / `auto_shots`) в `weapons.csv`.

## BurstShots / AutoShots из RPM (authored)

Один apply вместе с Recoil (тот же physical script / design doc):

```text
AutoShots  = clamp(round(CyclicRPM / 100), AutoMin, AutoMax)     # default clamp 3..14
BurstShots = clamp(round(CyclicRPM / 200), BurstMin, BurstMax)   # default clamp 2..8

если BurstLimiter > 0:
  BurstShots = min(BurstShots, BurstLimiter)

если оружия нет BurstFire в available attacks → BurstShots может остаться 0 / неиспользуемым
если нет AutoFire / full-auto → AutoShots = 0
MG / belt: допускается AutoShots == BurstShots или семейный cap (не раздувать MG42 до 24)

Дробовики: число дробин **не** через AutoShots — см. `JAZZ-WEAPONS-006` (`BuckshotProjectiles` + ammo mods).
```


Примеры-ориентиры (до семейных cap):

| Ствол | RPM | Burst | Auto | Limiter |
| --- | ---: | ---: | ---: | ---: |
| AK74 | 650 | 3 | 7→clamp/round **6–7** | 0 |
| M4A1 | 800 | 4 | 8 | 0 |
| M16A2 | 700 | min(4,**3**)=**3** | 7 | **3** |
| MicroUZI | 1200 | 6 | 12 | 0 |
| AN94 | 1800 | min(9,**2**)=**2** | clamp(18→14)=**14** или family cap | **2** |

Точные `AutoMax` / MG caps — в `docs/design/recoil-physical-scale.md` при реализации; якорь ощущений: высокий RPM → заметно длиннее очередь, отсечка режет только Burst.

**Длина очереди детерминирована** (preset); без random variance.

## Физическая калибровка Recoil (generated)

Канон-таблица и скрипт: `docs/design/recoil-physical-scale.md` + `docs/tools/_rebalance_recoil_physical.py`.

### Формула (authored)

```text
impulse   = CaliberImpulse[caliber]          # таблица bands
mass_f    = clamp(MassRef / WeaponMass, 0.70, 1.45)   # MassRef≈35 (3.5 kg); легче → выше Recoil
size_f    = SizeFactor[WeaponSizeClass]      # Compact 1.15 / Carbine 1.00 / Rifle 0.92 / Long 0.85
rpm_f     = 1 + clamp((CyclicRPM − 700) / 2000, −0.08, 0.18)  # 700 RPM ≈ нейтраль
family_f  = optional tiny override (MG belt, roller-delayed note) — sparingly

Recoil = clamp(round(impulse × mass_f × size_f × rpm_f × family_f), RecoilMinFamily, 70)
```

`CaliberImpulse` bands — **приняты владельцем** как стартовая шкала (плейтест может подкрутить later); якоря ниже обязательны при любом тюнинге:

| Band | Примеры калибров | impulse (ориентир) |
| --- | --- | ---: |
| Pistol soft | 9×18, .380 | 8–10 |
| Pistol / SMG | 9×19, .45ACP, 7.62×25, 5.7, 4.6 | 11–14 |
| Intermediate light | 5.45, 5.56 | 16–18 |
| Intermediate heavy | 7.62×39 | 22–26 |
| Battle / full | 7.62×51, 7.62×54R | 36–42 |
| Heavy MG / .50 | 12.7 и т.п. | 48–55 |

После расчёта — **ручная проверка якорей**; при конфликте якорь побеждает, правят impulse/family_f, не ломают порядок.

### Профильные якоря (канон ощущения)

Референс: **стоя**, Str80 / Marks80 (`shooter_factor=0.85`), без `AutoWeapons`, без bipod.

| Профиль | Ощущение | Recoil | 3-я vs P0 | 6-я vs P0 | @P0=70 |
| --- | --- | ---: | ---: | ---: | --- |
| **AK74** | более-менее кучная | **14–15** | ~74–77% | ~50–53% | …→**53–54**→…→**35–37** |
| **AKM** | похуже | **24–26** | ~60–64% | ~29–34% | …→**42–45**→…→**20–24** |
| **FN FAL** | плохо | **42–44** | ~37–41% | ~10–12% | …→**27–29**→…→**7–8** |

Порядок: **AK74 > AKM > FAL** по удержанию.

### Дифференциация внутри калибра (обязательный контракт)

На одном калибре Recoil **не обязан быть одинаковым**. Пример-ожидание **9×19 SMG/PDW** (после физической шкалы, порядок строгий):

| Ствол | Size | Mass (ориентир) | RPM (ориентир) | Recoil vs соседей |
| --- | --- | ---: | ---: | --- |
| Sterling / Beretta M12 | Carbine | тяжелее / длиннее | ~550–650 | **ниже** (мягче очередь) |
| MP5 / UZI | Carbine | средние | ~600–800 | **середина** |
| MP5K / MicroUZI / MAC-10 (.45 отдельно) | Compact | легче / короче | высокий | **выше** (очередь сыпется сильнее) |

Exact числа — из Mass/RPM IRL + формулы; AC проверяет **порядок** внутри 9×19, не абсолютные IRL кг.

Простой ×2 старых Recoil **недостаточен** (сохраняет старые ошибки); ×2 допускается только как sanity-check vs якорей, не как основной apply.

### Floor шанса

```text
P_bullet(i) ≥ JAZZ_CTH_VALID_SHOT_FLOOR   # 2
min_retention = 0.15
```

«Плохо» ≠ «бессмысленно».

## Shooter factors (runtime)

```text
strength_factor = clamp(1.25 − Strength/200, 0.75, 1.25)
marks_factor    = clamp(1.25 − Marksmanship/200, 0.75, 1.25)
shooter_factor  = 0.5 × strength_factor + 0.5 × marks_factor
```

Dexterity не в retention. Debug profile отдаёт оба фактора + `shooter_factor`. Вес **50/50** утверждён владельцем.

## AutoWeapons

- `perk_factor = 0.85` — снижает `effective_recoil`; **не** protected shots с 5-й пули. Утверждено владельцем.
- RU/EN Description переписать под факт.

Черновик:

- RU: «Автоматическое оружие: очереди и автоогонь легче контролировать (отдача слабее).»
- EN: «Automatic weapons: bursts and autofire are easier to control (reduced recoil severity).»

## Требования

- `JAZZ-WEAPONS-003-REQ-001` — у всех активных firearm заполнены `WeaponMass`, `CyclicRPM`, `WeaponSizeClass`, `BurstLimiter`; companion + `items.lua` + CSV согласованы.
- `JAZZ-WEAPONS-003-REQ-002` — `Recoil` пересчитан физической формулой (+ якоря); AK74∈[14,15], AKM∈[24,26], FNFAL∈[42,44].
- `JAZZ-WEAPONS-003-REQ-003` — внутри одного калибра (минимум 9×19 SMG set) Recoil различается по Mass/Size/RPM; порядок Compact/высокий RPM ≥ Carbine/средний ≥ тяжёлый/низкий RPM (при равном калибре).
- `JAZZ-WEAPONS-003-REQ-004` — runtime CTH **не** читает Mass/RPM/Size в `JAZZ_CTHGetRecoilProfile` (только через authored Recoil).
- `JAZZ-WEAPONS-003-REQ-005` — `shooter_factor = 0.5×Str + 0.5×Marks`; Dexterity вне retention.
- `JAZZ-WEAPONS-003-REQ-006` — `AutoWeapons` = `perk_factor=0.85`; RU/EN без «с 5-й пули»; loc auditor clean.
- `JAZZ-WEAPONS-003-REQ-007` — retention `/100`, `min_retention=0.15`, bullet floor **2** сохранены.
- `JAZZ-WEAPONS-003-REQ-008` — `AutoShots` / `BurstShots` authored из `CyclicRPM` (/100 / /200) + `BurstLimiter`; длина **детерминирована**; без random variance.
- `JAZZ-WEAPONS-003-REQ-009` — docs: design physical scale + technical + wiki + showcase RU/EN.

## Инварианты и ограничения

- Одна application отдачи на пулю; miss vector не двойной penalty; CTH пули ≥ 2%.
- Deterministic; save schema без новых save-полей instance (только preset props).
- Exclusive: `items.lua`.
- Не трогать dormant code.

## Acceptance criteria

- `JAZZ-WEAPONS-003-AC-001` — static: все active firearms имеют Mass/RPM/SizeClass/BurstLimiter; CSV колонки на месте.
- `JAZZ-WEAPONS-003-AC-002` — static: якоря Recoil AK74/AKM/FNFAL в диапазонах; sim @P0=70 Str80/Marks80 — порядок удержания AK74 > AKM > FAL; 6-я ≥2.
- `JAZZ-WEAPONS-003-AC-003` — static: набор 9×19 (MicroUZI, MP5 или MP5A2, Sterling или M12) — Recoil не все равны; Compact/высокий RPM не мягче тяжёлого низкотемпового Carbine.
- `JAZZ-WEAPONS-003-AC-004` — static: `JAZZ_CTHGetRecoilProfile` не умножает Mass/RPM; Marks участвует в shooter_factor.
- `JAZZ-WEAPONS-003-AC-005` — static/loc: AutoWeapons текст + perk_factor.
- `JAZZ-WEAPONS-003-AC-006` — static: sample matrix — AutoShots≈RPM/100, BurstShots≈RPM/200 с clamp; M16A2 BurstLimiter=3 → BurstShots≤3; AN94 BurstLimiter=2 → BurstShots=2; нет RNG длины.
- `JAZZ-WEAPONS-003-AC-007` — human: очередь AK74 кучная, AKM хуже, FAL плохо но не zero; два ПП одного калибра ощущаются по-разному; высокий RPM даёт заметно длиннее авто.
- `JAZZ-WEAPONS-003-AC-008` — docs sync в том же change set.

## Impact и совместимость

- Новые preset fields; старые сейвы подтягивают defs.
- Attaches `Recoil±` absolute — относительный вес падает (follow-up).
- Rollback: revert write set + physical table.

## План и ownership

- Пакет: `jazz`
- Exclusive: `jazz/items.lua`

## Открытые решения для владельца (до approve)

*Нет открытых пунктов.* Spec **approved**; реализация — по отдельной команде.

**Закрыто направлением владельца:**

- Якоря AK74 кучная / AKM хуже / FAL плохо; floor 2%.
- Реалистичная дифференциация по массе/длине; **Mass + RPM + SizeClass** как статы (authored → Recoil).
- AutoWeapons: `perk_factor=0.85`; текст перка менять в spec.
- Вес Str/Marks: **50/50**.
- Mass/RPM в **player UI не показывать** (пока).
- `CaliberImpulse` bands — принять черновик.
- **Burst/Auto из RPM** (/100 / /200) + `BurstLimiter` — **в scope 003** (не отдельная 004); random длина очереди — **non-goal**.

## Решение владельца

- Статус: **approved** (scope expanded chat 2026-08-01: RPM→Burst/Auto folded into 003)
- Кто подтвердил: project-owner
- Дата: 2026-08-01
- Решение: принимать CaliberImpulse bands; Burst/Auto authored из RPM+отсечка в том же change set; variance длины отвергнута; implement по команде.

## Evidence

- `JAZZ-WEAPONS-003-AC-001`: `PASS` (static) — `_rebalance_recoil_physical.py --apply` populated 161 active catalog firearms in companions and matching ModItems; CSV exports the four new columns.
- `JAZZ-WEAPONS-003-AC-002`: `PASS` (static) — `_audit_recoil_dist.py`: AK74=15, AKM=25, FNFAL=43; retention wave remains runtime/human validation.
- `JAZZ-WEAPONS-003-AC-003`: `PASS` (static) — MicroUZI=21 > MP5K=18 and Sterling=18 with authored mass/RPM/size.
- `JAZZ-WEAPONS-003-AC-004`: `PASS` (static) — `AccuracyRangeCTH.lua` keeps physical inputs authored-only and applies the approved 50/50 Strength/Marksmanship shooter factor.
- `JAZZ-WEAPONS-003-AC-005`: `PASS` (static/loc) — AutoWeapons retains `perk_factor=0.85`; RU/EN text names reduced recoil severity.
- `JAZZ-WEAPONS-003-AC-006`: `PASS` (static) — authored deterministic RPM derivation; M16A2 limiter=3 and AN94 limiter=2.
- `JAZZ-WEAPONS-003-AC-007`: `BLOCKED` (human/runtime) — wave test in Mod Editor/game is required.
- `JAZZ-WEAPONS-003-AC-008`: `PASS` (static) — design, technical, wiki and RU/EN showcase updated.

## Documentation delta

При реализации:

- `docs/design/recoil-physical-scale.md` — impulse/mass/size/rpm + Burst/Auto (/100/200) + limiter + примеры SMG.
- `docs/technical/weapons/accuracy-model.md` — shooter Marks; Recoil authored from physical; floor.
- `docs/technical/systems/weapons-ammo-components.md` — новые свойства; Burst/Auto policy.
- `docs/technical/weapons/data/weapons.csv` — mass/rpm/size/limiter/recoil/burst/auto.
- `docs/wiki` + `docs/showcase` RU/EN — очередь, Marks+Str, различия платформ / темпа; **без** UI Mass/RPM; без random длины.
- `docs/tools/README.md` — physical rebalance + audit scripts.
