# Легион: лоадауты (оружие, броня, модули, патроны)

Design-only. Код не меняет. Runtime current-state: [`legion-units-equipment-tiers.md`](../technical/systems/legion-units-equipment-tiers.md). Канон тиров оружия: [`weapons.csv`](../technical/weapons/data/weapons.csv) / [`weapons/README.md`](../technical/weapons/README.md).

Статус: зафиксированные решения владельца (30 июля 2026). Реализация — [`JAZZ-UNITS-003`](../specs/active/JAZZ-UNITS-003.md) (**implemented**; runtime AC-008/009 — human). Exclusive: не параллелить чужой write на `jazz-units/items.lua` / `metadata.lua` во время regenerate.

---

## 0. Зафиксированные решения

| # | Решение |
| --- | --- |
| L1 | Две оси: **class T1–T4** (силаэт) и **campaign `JAZZ_Legion_Tier`** (поколение склада). Живой юнит не морфится в другой UnitData. |
| L2 | Носитель прогресса — quest `JAZZ_LegionTier` / `JAZZ_Legion_Tier`. Текущие TCE по `PlayerControlSectors` осознанны: **демо Ernie ≈ ~20 секторов**, сетка порогов растянута под этот остров; не «случайный сырой count». Улучшения триггеров — отдельный change, не обязательны для генератора лута. |
| L3 | Три **arch**: `1x` / `2x` / `3x`. Arch = скачок поколения. **Число sub и сетка `11–1N` / `21–2N` / `31–3N` = зеркало пула оружия** (`tier_label` в `weapons.csv`: сейчас `1-1…1-3`, `2-1…2-5`, `3-1…3-5`), не отдельная произвольная длина. |
| L4 | Кодировка тира оружия `tier_label` `X-Y` = число `XY` того же языка, что `JAZZ_Legion_Tier` (`1-2` → `12`, не «гибрид»). |
| L5 | Основной пул оружия на arch N = `balance_tier == N`. Прошлое поколение на следующем arch — **~1%** (WWII/`tier 1` на `2x`); на `3x` поколение `1` = 0%. |
| L6 | Класс задаёт **силуэт** (семейства, sidearm, melee, armor band, utility, mods_cap, ammo grade cap). Tier двигает **качество внутри силуэта**. |
| L7 | Midgame бафает **всех** (пол качества). **Carbine как норма** — хорошим штурмам / рейдерам, не всем low. |
| L8 | На arch3 low class может взять **АК / assault tier3–2** как primary: пистолет как основной уже не роляет. |
| L9 | Пистолеты и револьверы на mid+ — в основном **sidearm**, не primary. |
| L10 | Чем элитнее (class + arch) — тем больше **модулей** (пакеты M0–M4 через `LootEntryUpgradedWeapon`). |
| L11 | Отдельные стволы могут иметь **теги семейства** (напр. M2/FG42 ∈ `{carbine, assault}`). Это не `tier_label`. |
| L12 | Патроны: калибр от ствола; эволюционирует **grade/элитность** (`Poor → FMJ → Army → Match/EPR → AP`). Arch поднимает пол; class — потолок. |
| L13 | Канон сопровождения: **компактные recipes/keywords → генератор → LootDef**. Не плодить вручную варианты одной винтовки/брони/патронов. |
| L14 | Генератор распространяется на **весь кит**: primary (+mods), sidearm, melee, armor, ammo, utility, valuables, night, misc — не только обвес. |
| L15 | **Ночные светилки** (GlowStick / FlareStick / weapon flashlight%): упор на ночь; днём near-zero. Шанс/кол-во **чуть↑ с loot tier**. % — §5.4. |
| L16 | **FlareGun** — не всем; recon/flanker/leader/sniper. База §5.4; **лёгкий↑ с loot tier**. |
| L17 | **Misc low-roll**: очки, маски. % — §5.4 (в основном class band). |
| L18 | **Valuables ≈ цена юнита**: ≈ `JAZZ_GetLegionUnitPrice`, диапазон + шанс. Стартовые % — §5.4. TinyDiamonds **$500**. |
| L19 | **Карман ≠ груз логистики.** Груз `tax`/`shipment` лутается при грабеже. Карман L18 на логистике не клеить сверху. **Regen — open / as-is.** |
| L20 | **Гранаты:** специалистам — guaranteed (counts чуть↑ с loot tier); неспециалистам — шанс↑ с **class-tier и loot tier**. |
| L21 | **Pipe bomb** в пуле **low-class** даже на high loot tier (Roughneck с ~`21`); эволюция возможностей. |
| L22 | Часть слотов **открывается не с arch1**: sidearm / пайпы / часть utility — delayed unlock. |
| L23 | **Износ/condition оружия** влияет и на NPC; **не** часть starting-loadout генератора. Отдельная генерация **после смерти** (как сейчас по смыслу). |

---

## 1. Формула

```
CreateLoadout(class, legion_tier) =
  silhouette(class)                       # что можно
  × generation(arch(legion_tier))         # какой склад открыт
  × polish(sub(legion_tier))              # веса внутри поколения
  × weapon.balance_tier gate              # 1/2/3 ↔ arch, хвост 1%
  × mods ≤ mods_cap(class, arch)
  × ammo_grade ∈ [floor(arch), cap(class)]
```

Одной фразой: **класс — силуэт; arch — поколение склада; sub — шлифовка; оружейный `X-Y` — тот же XY.**

---

## 2. Arch / sub и оружие

Длина sub **не выбирается отдельно**: Legion `JAZZ_Legion_Tier` шагает по тем же `X-Y`, что есть в оружейном каталоге.

| Arch | `tier_label` в пуле (сейчас) | Legion values |
| --- | --- | --- |
| `1x` | `1-1` … `1-3` (+ UNIQ) | `11`–`13` |
| `2x` | `2-1` … `2-5` | `21`–`25` |
| `3x` | `3-1` … `3-5` (пока тонко на `3-4`/`3-5`) | `31`–`35` по мере наполнения пула |

Появился `2-6` в CSV — можно добавить `26`; пустой sub без оружия не плодить.

| Legion | Основной пул | Хвост |
| --- | --- | --- |
| `1x` | `balance_tier == 1` | — |
| `2x` | `balance_tier == 2` | tier `1` ≈ **1%** |
| `3x` | `balance_tier == 3` (+ tier `2` как пол) | tier `1` = **0%** |

Sub внутри arch — веса в пользу своего `balance_subtier`. `engine_tier` / shop — не этот контракт.


### Теги семейства (отдельно от `1-2`)

Примеры гибридных allow-тегов (не путать с `tier_label`):

| ID | `tier_label` | Теги (дизайн) |
| --- | --- | --- |
| `M2Carbine` | `1-2` | `{carbine, assault}` |
| `FG42` | `1-3` | `{carbine, assault}` (+ battle) |
| `STG44` | `1-2` | `{assault}` |

Класс берёт ствол при пересечении allow-list с тегами. На `2x` M2/FG42 сидят в общем **1%-хвосте tier1**; нормальный carbine/AR штурма на `2x` — из **tier2** (`CAR15`, `M16A1`, `ZastavaM92`…).

---

## 3. Слои качества

| Слой | Arch-скачок | Sub-шлифовка |
| --- | --- | --- |
| Primary | новое поколение `balance_tier` | веса subtier / condition |
| Sidearm | pistol/revolver во 2-й слот mid+ | лучше grade/% |
| Armor | лучше предметы **внутри** Light/Middle/Heavy | веса |
| Mods | потолок пакета M↑ | шанс высшего пакета |
| Ammo | пол grade↑ | веса к Army/AP |
| Utility | плотнее у ролей, которым положено | count/% |

**Не** эволюционировать Light→Heavy от campaign tier: band выбирает класс.

### Пакеты модулей

| Cap | Пакет |
| --- | --- |
| M0 | bare |
| M1 | один слот (mag \| stock \| laser) |
| M2 | optic + mag |
| M3 | optic + mag + (laser \| suppressor \| bipod) |
| M4 | merc full kit |

Профиль модулей по роли (штурм ≠ sniper scope-only). Реализация — готовые `LootEntryUpgradedWeapon` варианты (`_AP_Reflex`, `_AP_Reflex_Drum`, …).

### Ammo grade

| Grade | Примеры | Ориентир |
| --- | --- | --- |
| Poor | `*_Poor` | arch1, low |
| FMJ | `*_FMJ` | arch1 late / arch2 line |
| Army | `*_Army` | arch2+ mid, T2–T3 |
| Match / EPR | `*_Match`, `*_EPR` | marksman/sniper, arch3 |
| AP / APP | `*_AP`, `*_APP` | arch3, T3–T4, merc |

Калибр от ствола. Пары лута `*_ammo` / `*_ammo_ap` = разный пол grade, не «только бронебой».

---

## 4. Unlock’ы поколений (сводка)

| Unlock | Кому | Когда |
| --- | --- | --- |
| Общий quality bump | всем | каждый arch + sub |
| Carbine как норма | Shock, Punisher, Headsman, Raider, Veteran, Merc*, Lt+, «хороший» assault | **arch2+** |
| АК / assault primary у low | Roughneck, Marauder, Pillager, Sgt line… | **arch3** |
| Pistol primary | early low; companion arty | arch1; дальше sidearm |
| Sidearm pistol/revolver | большинство non-sniper/MG | arch2+ чаще |
| Mods↑ | по class cap | arch↑ и class-tier↑ |
| Ammo grade↑ | пол от arch, потолок от class | как таблица выше |
| Weapon tier1 на arch2 | все пулы | **~1%** |
| Heavy armor band | Pyro, Skull, Punisher, Headsman, MG vet+ | class, не «всем на 31» |

---

## 5. Class kit recipes (37 боевых)

Легенда: Primary по arch; Sidearm = pistol/revolver rule; Mods = потолок; Arch2/3 = скачок силуэта.

### Штурм

| Класс | Primary | Sidearm | Melee | Armor | Utility | Mods | Arch2 | Arch3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Roughneck T1 | pistol→SMG | %→часто | knife часто | Light | нет | M0→M2 | SMG↑ + sidearm% | **assault/АК ок** + sidearm; без carbine-нормы |
| Grenadier T1 | SMG/pistol | % | — | Middle | HE + molotov% | M0–M1 | SMG/carbine% + HE | АК/SMG + HE; ≤M2 |
| Crusher T1 | shotgun | pistol mid+ | — | Middle | мало | M0–M1 | shotgun↑ | combat SG + sidearm; M2 |
| Pillager T2 | SMG | — | knife | Light | мало | M1–M2 | SMG↑, carbine редко | АК/SMG; light; M2 |
| ShockTrooper T2 | SMG→**carbine** | knife + sidearm% | knife | Middle | HE + smoke%/conc% | M1–M3 | **carbine норма** | AR/carbine + M2–M3 |
| Pyro T2 | SMG/carbine% | — | — | Heavy | **molotov** + HE% | M0–M2 | SMG↑ | АК/SMG + molotov; mods скромно |
| Punisher T3 | carbine→AR | sidearm | — | Heavy | HE + conc | M2–M3 | carbine/AR + AP ammo | AR+mods M3 |
| SkullCrusher T3 | shotgun/SMG | — | machete | Heavy | smoke% + molotov% | M1–M2 | shotgun↑ | SG/АК-CQB + machete |
| Headsman T4 | AR | sidearm | knife% | Heavy | HE + smoke/conc | M3–M4 | high AR | full kit M3–M4 |

### Front

| Класс | Primary | Sidearm | Melee | Armor | Utility | Mods | Arch2 | Arch3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rifleman T1 | bolt/semi | редко | — | Middle | нет | M0–M2 optic late | semi↑ | DMR/semi + optic |
| Bonemaker T1 | pistol→light carbine | — | — | Middle | **medkit** | M0–M2 | carbine/SMG + med | лёгкий AR/SMG + med |
| Marauder T1 | SMG/pistol | % | knife% | Middle | мало | M0–M2 | SMG↑ | **АК ок** + sidearm |
| Ambusher T2 | rifle/semi | редко | — | Light/Middle | smoke% | M1–M3 scope | semi + 2x% | DMR + scope |
| Raider T2 | SMG→**carbine** | sidearm% | knife% | Middle | HE% | M1–M3 | **carbine** | AR/carbine |
| Marksman T2 | semi/DMR | — | — | Middle | нет | M1–M3 optic | DMR↑ | DMR + scope |
| Sniper T3 | sniper only | нет / very rare | **нет** | Light/Middle | нет HE | M2–M3 scope | 2x/4x | elite + bipod%; Match ammo |
| Veteran T3 | carbine→AR | sidearm | — | Middle/Heavy | HE% | M2–M3 | AR/carbine | AR+mods; ammo↑ |
| Mercenary T4 | узкий AR | sidearm | — | Middle+ | HE% | **M3–M4** | high floor | contract kits |
| MercenarySniper T4 | узкий sniper | нет | нет | Middle | нет | **M3–M4** | high floor | elite scoped |

### Фланкеры

| Класс | Primary | Sidearm | Melee | Armor | Utility | Mods | Arch2 | Arch3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Warden T1 | bolt/winch/semi | редко | — | Light | нет | M0–M2 | semi↑ | light rifle/SMG; не full AR |
| Scout T2 | SMG | knife% | knife% | Light | smoke% | M1–M2 + **supp%** | SMG↑ + supp% | SMG/АК-CQB + supp |
| Skirmisher T2 | SMG/carbine light | sidearm% | — | Light | smoke%/HE% | M1–M2 | carbine light | SMG/carbine; не heavy AR |
| Recon T3 | SMG/carbine | sidearm% | knife% | Light | smoke | M2–M3 + supp | carbine/SMG+supp | +mods |
| Pathfinder T3 | carbine/SMG | — | knife% | Light/Middle | smoke | M2–M3 + supp | carbine | carbine+supp |
| Ranger T4 | carbine/SMG elite | sidearm% | knife% | Light/Middle | smoke | **M3–M4** supp | high floor | full scout kit |

### Пулемёты

| Класс | Primary | Sidearm | Melee | Armor | Utility | Mods | Arch2 | Arch3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gunner T1 | LMG | редко | **нет** | Middle | ammo-heavy | M0–M2 bipod% | LMG↑ | GPMG + bipod |
| GMPG T2 | GPMG | — | нет | Middle/Heavy | ammo | M1–M3 bipod | GPMG↑ | +optic rare |
| AssaultGunner T2 | SAW/LMG | sidearm% | нет | Middle | ammo | M1–M3 | SAW↑ | SAW + mag/bipod |
| VeteranGunner T3 | GPMG | — | нет | Heavy | ammo | M2–M3 | high MG | elite MG |
| MercGunner T4 | elite MG | — | нет | Heavy | ammo | **M3–M4** | high floor | full MG kit |

### Командиры

| Класс | Primary | Sidearm | Melee | Armor | Utility | Mods | Arch2 | Arch3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sergeant T1 | SMG/pistol | часто | — | Middle | smoke%/HE% | M0–M2 | SMG↑ | АК/SMG + sidearm |
| Lieutenant T2 | carbine/SMG | **часто** | — | Middle | smoke + HE% | M1–M3 | **carbine** | AR/carbine |
| Captain T3 | rifle/carbine | часто | — | Middle | smoke | M2–M3 optic | DMR/carbine | scoped mid |
| MercenaryCaptain T4 | AR/carbine elite | часто | — | Middle+ | smoke/HE% | **M3–M4** | high floor | contract leader |

### Артиллерия

| Класс | Primary | Sidearm | Melee | Armor | Utility | Mods | Arch2 | Arch3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rocketeer T1 | launcher + sidearm | **да** | нет | Middle | rockets | launcher bare; sidearm M0–M1 | launcher↑ | late launcher + better sidearm |
| HeavyGrenadier T2 | GL + sidearm/SMG | да | нет | Middle | GL rounds | M0–M2 на firearm | GL↑ | GL + SMG/АК short |
| Mortarman T3 | mortar + sidearm | да | нет | Middle | mortar ammo | sidearm M0–M2 | mortar kit↑ | late mortar + sidearm |

### 5.1 Night / flare / misc (поверх таблицы)

| Слой | Правило |
| --- | --- |
| **Night lights** | `GlowStick` / `FlareStick`; опц. gun flashlight. Ночь — on, день — near-zero. **Шанс и stack чуть↑ с loot tier** (§5.4). |
| **FlareGun** | Role bias §5.4; **база + лёгкий↑ с arch** (не midgame-баф всех). |
| **Misc low-roll** | Shared `Legion_MiscGear`. % по class band — §5.4 (loot tier почти не трогает). |
| **Valuables ($)** | ≈ unit price — §5.2 / §5.4. |
| **Grenades** | §5.3: specialist guaranteed; non-spec **chance↑ с class-tier и loot tier**; pipes — late unlock low-class. |

### 5.3 Гранаты, пайпы, delayed slots

Два режима utility-взрывчатки:

| Кто | HE / frag / smoke (по профилю) | Pipe bomb |
| --- | --- | --- |
| **Специалист** (Grenadier, Pyro, Shock с HE-профилем, Punisher, Headsman, Raider/Veteran с HE, …) | **гарантированно**; counts **чуть↑ с loot tier** | по вкусу / редко |
| **Неспециалист** (Roughneck, Rifleman, Warden, line trash…) | **шанс↑** с class-tier **и** loot tier | в пуле low-class с ~`21`, chance тоже чуть↑ с arch |

Эволюция возможностей (не только «лучший ствол»):

| Unlock | Пример | Когда roughly |
| --- | --- | --- |
| Sidearm | Crusher/Roughneck pistol | не с `11`, а с mid sub / arch2 (как сейчас «не сразу») |
| Pipe bomb | Roughneck | с ~`21` (`2-1`) в пуле с шансом; на `1x` чаще нет |
| HE chance↑ | non-spec | каждый arch и class-tier поднимают % |
| Specialist HE | Grenadier/Pyro… | всегда, counts↑ с arch |

Черновые % для non-spec HE (тюнить в spec):

| | T1 | T2 | T3 | T4 |
| --- | ---: | ---: | ---: | ---: |
| arch1 | ~5–10% | ~15% | — | — |
| arch2 | ~15–25% | ~30–40% | ~50%+ | — |
| arch3 | ~30–40% | ~50% | ~60%+ | guaranteed-ish / high |

Pipe на Roughneck @ `21+`: отдельный вес в пуле (не вычищать, когда открывается frag).

В DSL:

```yaml
utility:
  he: { mode: chance, chance_by_arch: [10, 25, 40] }   # non-spec; class-tier adds more
  # he: { mode: guaranteed, count_by_arch: [3, 4, 5] } # specialist
  pipe: { unlock_tier: 21, chance_by_arch: [0, 20, 28] }
night:
  lights: { night_only: true, chance_by_arch: [45, 55, 65], stack_by_arch: ["3-6", "4-8", "5-10"] }
sidearm: { unlock_tier: 12, chance: 50 }
```

### 5.4 Предлагаемые % (тюнить playtest’ом)

Ориентир «редко, но заметно»; **светилки и гранаты — чутка↑ с loot tier**.

#### Night lights (ночь only; день ≈ 0)

| | arch1 | arch2 | arch3 |
| --- | ---: | ---: | ---: |
| шанс хоть чего-то (Glow/Flare stick) | **45%** | **55%** | **65%** |
| stack (если выпало) | 3–6 | 4–8 | 5–10 |
| gun flashlight keyword (если package позволяет) | 8% | 12% | 16% |

#### FlareGun (+ ammo при успехе)

База по роли; **× loot bump**: arch1 ×1.0, arch2 ×1.15, arch3 ×1.3 (cap 35%).

| Role bias | base chance |
| --- | ---: |
| MG / arty / Pyro / most assault | **0%** |
| Shock / Raider / Veteran | **5%** |
| Sergeant, Ambusher, Marksman | **8%** |
| Scout / Skirmisher / Recon / Pathfinder / Warden | **18%** |
| Ranger, Lieutenant, Sniper, MercCaptain | **22%** |

#### Non-spec HE / smoke chance (фрагмент; полная сетка class×arch)

Уже в §5.3 таблице; смысл: каждый loot arch заметно поднимает %, class-tier — сильнее. Specialist: guaranteed, `count_by_arch` напр. 3 → 4 → 5.

#### Pipe (low-class, unlock `21+`)

| | arch2 | arch3 |
| --- | ---: | ---: |
| Roughneck-like pipe chance | **20%** | **28%** |

#### Misc (очки / маска) — шанс хотя бы одного

| Class band | chance |
| --- | ---: |
| T1 line | **3%** |
| T2 | **5%** |
| T3 | **8%** |
| T4 / merc | **12%** |
| Flanker / leader | +**2%** |

Loot tier misc почти не качает (или +1% на arch3 max).

#### Valuables `drop_chance` (карман; не logistics cargo)

| Class band | `drop_chance` | `mult` при успехе |
| --- | ---: | --- |
| T1 | **35%** | 0.4–1.2 × P |
| T2 | **45%** | 0.5–1.4 × P |
| T3 | **55%** | 0.5–1.5 × P |
| T4 / merc / leader | **65%** | 0.6–1.5 × P |

Специалисты (sniper/MG) опц. +5% к chance (P уже выше).

### 5.5 Износ (condition)

**Вне** starting-loadout генератора. Condition влияет на NPC в бою; генерация износа — **отдельный проход после смерти**. Recipes/arch не задают condition на спавне.

### 5.2 Valuables ≈ unit price

Якорь: `TinyDiamonds = $500`, `BigDiamond = $5000` (roadmap). Цены классов — `Code/LegionUnitPrices.lua` (Roughneck **300** … MercGunner/MercSniper **4500**).

Черновые параметры — §5.4; ниже смысл и cargo-разделение.

| Параметр | Смысл |
| --- | --- |
| `drop_chance` / `mult` | см. §5.4 |
| `expected` | ≈ `drop_chance × ~P` — средний лут с трупа ниже полной цены |
| размен | TinyDiamonds @500; при value ≥ ~4000 можно 1× BigDiamond + остаток Tiny; без портфелей на обычных бойцах |

Примеры порядка величины:

| Класс | `P` | типичный дроп при успехе |
| --- | --- | --- |
| Roughneck | 300 | 0–1× Tiny (часто пусто) |
| ShockTrooper | 1000 | 1–3× Tiny |
| Sniper T3 | 2800 | 3–8× Tiny |
| Merc / MercGunner | 3500–4500 | 4–10× Tiny или 1× Big + Tiny |

В DSL:

```yaml
valuables:
  mode: unit_price
  # drop_chance / mult from class band table §5.4
```

Генератор читает `P` из того же каталога, что STRATEGY-004/008.

#### Разделение с Global AI cargo (обязательно)

Два разных смысла одних и тех же предметов:

| Канал | Кто | Что | При бое / грабеже |
| --- | --- | --- | --- |
| **Карман бойца** | combat / обычный Legion | Tiny/Big ≈ unit `$`, шанс+диапазон | лут с трупа |
| **Груз миссии** | `shipment`, `tax`, (supply `$`), носители | `DiamondBriefcase` / Tiny на **сумму payload** | **игрок залутывает эту сумму** |

Правила:

1. Class recipe **никогда** не выдаёт `DiamondBriefcase` и не подменяет payload миссии.  
2. На managed-логистике — **`valuables: none`** в смысле L18 (карман); груз кладёт только Global AI (`lEnsureMoneyCargo`).  
3. Груз **лутаемый** в тактике — награда за перехват сборщика/конвоя.  
4. **Regen** — open / as-is (L19); не blocker.  
5. Один UI-предмет (`TinyDiamonds`) ок; карман ≠ tax payload.

Ссылки: roadmap / STRATEGY-007/009, `Guardpost_Patrols.lua` → `lEnsureMoneyCargo`.

---

## 6. Сопровождение: recipes → генератор → LootDef

## 6. Сопровождение: recipes → генератор → LootDef

Ручной зоопарк `M16A1_AP_Reflex` / копий брони / ammo-веток на каждый класс **не** целевой процесс. Целевой:

```
class recipes + shared catalogs (keywords/tags)
        ↓ build-time script
generated LootDef / LootEntry*  (в т.ч. UpgradedWeapon)
        ↓
CreateStartingEquipment (runtime как сейчас)
```

Правим **recipes и каталоги**; `items.lua` — артефакт (с оговоркой sync/Mod Editor в spec). Merc/boss hand-tuned острова допустимы как исключения.

### Что генерится из keywords (весь кит)

| Слой | Вход генератора | Источник совместимости / пула |
| --- | --- | --- |
| Primary | allow-tags + `balance_tier` gate + package `M0–M4` | `weapons.csv`, `weapon-component-options.csv` |
| Mods | package keywords (`reflex`, `mag_large`, `supp`…) ∩ слоты ствола | тот же CSV компонентов |
| Sidearm | rule `none \| % \| always` + pistol/revolver tags + tier gate | `weapons.csv` |
| Melee | `knife \| machete \| none` + % | item IDs / малый каталог |
| Armor | band `Light\|Middle\|Heavy` + arch/sub quality | каталог брони с tier/tags |
| Ammo | caliber от выбранного ствола + grade floor/cap | `JAZZ_AMMO_*` + grade |
| Utility | profile + `guaranteed\|chance` + pipe unlock_tier | HE/smoke/molotov/pipe item IDs |
| Night | `lights: night_only`, optional gun flashlight keyword | GlowStick / FlareStick + time condition |
| Flaregun | `never \| rare \| sometimes` + ammo | `FlareHandgun`, `FlareAmmo` |
| Misc | low-roll table + class chance bias | sunglasses, gas/ballistic mask, … |
| Valuables | `unit_price` × mult range × drop_chance | `JAZZ_LegionUnitPrices` + Tiny/Big diamonds |

Классовый recipe остаётся тонким (как §5): tags, caps, %, band, package id — без списка конкретных суффиксов ствола.

### Пример формы recipe (идея DSL)

```yaml
ShockTrooper:
  primary: { tags: [smg, carbine, assault], packages: [assault_m1, assault_m2] }
  sidearm: { chance: 50 }
  melee: { knife: 50 }
  armor: { band: Middle }
  utility: { he: { mode: guaranteed, count: "3-5" }, smoke: 50 }
  # Roughneck instead:
  # utility: { he: { mode: chance, chance_by_arch: [10, 25, 40] }, pipe: { unlock_tier: 21, chance: 20 } }
  # sidearm: { unlock_tier: 12, chance: 50 }
  ammo: { floor: FMJ, cap: Army }
  night: { lights: night_only }
  flaregun: never
  misc: { chance: 5 }
  valuables: { mode: unit_price, drop_chance: 50, mult_min: 0.5, mult_max: 1.5 }
  arch:
    2: { primary_bias: [carbine, assault], packages: [assault_m2] }
    3: { packages: [assault_m3], ammo: { floor: Army, cap: AP } }

Scout:
  primary: { tags: [smg], packages: [flanker_m1] }
  night: { lights: night_only, flashlight_on_gun: 15 }
  flaregun: sometimes
  misc: { chance: 8 }
```

Генератор сам режет `balance_tier`↔arch, хвост tier1≈1% на `2x`, совместимые upgrades, ammo bundle.

### Почему так проще держать

- Одно место меняет «всем штурмам carbine на 2\*» или «WWII 1%».
- Новый ствол в `weapons.csv` + компоненты → попадает в пулы по tags/tier без 20 ручных LootDef.
- Новый модуль в CSV → подхватывается packages, где keyword совпал.
- Class identity правится в recipe-таблице, не в сотнях весов.

Предпочтительно **build-time** (детерминированный лут, меньше runtime-риска). Runtime-аттач — только если spec явно выберет его вместо генерации entries.

---

## 7. Quest signal и regen

- Var остаётся `JAZZ_Legion_Tier`.
- Текущие пороги по `PlayerControlSectors` завязаны на **демо Ernie (~20 секторов)** — сетка осмысленна для острова; не считать багом «сырого count» без контекста.
- Материк / significant-POI триггеры — отдельный follow-up, не блокер генератора.
- **Regen:** open / as-is (L19).

---

## 8. Non-goals этого дизайна

- Новые UnitData «ради другого ружья».
- Смена AI archetypes (см. [`tactical-ai-archetypes.md`](tactical-ai-archetypes.md)).
- Стратегический generator / `$` / officer density (STRATEGY-004/005/008) — ортогонально; class composition ≠ gear generation.
- Выдавать этот документ за current-state technical.
- Править generated Legion loot вручную как основной workflow (после появления генератора).

---

## 9. Следующие шаги реализации

Контракт: [`JAZZ-UNITS-003`](../specs/active/JAZZ-UNITS-003.md). Generator: `jazz/scripts/legion-loadouts/` (README + TESTING). Current-state: [`legion-units-equipment-tiers.md`](../technical/systems/legion-units-equipment-tiers.md).
