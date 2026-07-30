---
status: ready
priority: low
origin: ub
unit_id: Jazz_Kulba
portrait_id: Kulba
affiliation: Locals
role: Autorifleman
tier: Regular
specialization: Autoriflemen
gender: Male
nationality: USA
voice_source: ub
starting_level: 3
will: 60
salary:
  starting: 800
  increase: 150
  lv1: 350
  max: 2200
medical_deposit: small
haggling: normal
executable: true
---

# Кульба — Джон Кульба

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Джон Кульба | John Kulba |
| Nick | Кульба | Kulba |
| AllCapsNick | КУЛЬБА | KULBA |
| Title | Патриот-дед | The Patriot Gramps |
| Email | Kulba@ub.mil | Kulba@ub.mil |
| snype_nick | kulba | kulba |

## Bio

**RU:** Ветеран Urban Brawl. Статы 55–60, Marksmanship 95, Mechanical 88. Жена умерла от рака вскоре после спасения из Арулко. Ультра-патриот, любит Гаса, недолюбливает Ивана, Игоря и Рикошета.

**EN:** An Urban Brawl veteran. Stats in the 55-60 range, 95 Marksmanship, 88 Mechanical. His wife died of cancer shortly after the Arulco rescue. An ultra-patriot who's fond of Gus but can't stand Ivan, Igor, or Ricochet.

## Stats

| Stat | Value |
| --- | --- |
| Health | 58 |
| Agility | 55 |
| Dexterity | 55 |
| Strength | 60 |
| Wisdom | 70 |
| Will | 60 |
| Leadership | 35 |
| Marksmanship | 95 |
| Mechanical | 88 |
| Explosives | 20 |
| Medical | 25 |
| MaxHitPoints | 58 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Kulba`
- `AutoWeapons`
- `MrFixit`
- `OldDog`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Kulba` |
| type | passive |
| DisplayName RU/EN | Оружейник старой закалки / Old-School Gunsmith |
| Description RU/EN | Автоматическое оружие Кульбы стреляет точнее и реже заклинивает / Kulba's automatic weapons hit harder and jam less |
| Mechanics | Full-Auto and burst attacks fired by Kulba gain +10% CTH on the first bullet of the burst, and any automatic weapon he carries has a 50% reduced chance to jam. |

## Personality

- Quirks: Patriot (flavor; no dedicated JA3 status — expressed via dialogue and mitigation below)
- Likes: `Gus`
- Dislikes: `Ivan`, `Igor`, `Jazz_Ricochet`
- National hates: —
- Refusal / Haggle notes: refuses if Ivan or Igor are in the active squad roster; haggles down when Jazz_Ricochet is present (grudging tolerance, not outright refusal); mitigation and rate discount when Gus is hired

## Hire

- Access: Locals (UB veteran network)
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Kulba` → `JAZZ_Kulba50/35/25/20`
- *50: `JazzArmor_UniformPants`, `M60`, `JAZZ_AMMO_762x51_FMJ`×100 (Double), `Parts`×5, `Wirecutter`
- *35: `RPK`, `JAZZ_AMMO_762x39_FMJ`×80 (Double), `Parts`×3
- *25: `M2Carbine`, `JAZZ_AMMO_30_FMJ`×40 (Double)
- *20: `Winchester1894`, `JAZZ_AMMO_30_P`×30 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](kulba.ja2-face.jpg)

Файл: `kulba.ja2-face.jpg`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `kulba.ja2-face.jpg` (same face identity). Elderly American patriot, gray hair, flag patch and gunsmith tools — NO rifle in hands. Sad resolve.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** US flag patch, gunsmith tools, mourning band

## Phrases — AIM chat

### Offline
- RU: Кульба на службе. Перезвоните.
- EN: Kulba's on duty. Leave a message.

### GreetingAndOffer
- RU: Кульба слушает. За свободу.
- EN: Kulba here. For freedom.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Старое оружие ещё послужит.
- EN: Old guns still have some fight in them.

### PartingWords
- RU: За свободу. Я в деле.
- EN: For freedom. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Есть ещё порох в пороховницах.
- EN: I'm staying. Still got some fight left.

### Refusals
- Ivan or Igor hired RU: С этими двумя я не работаю. Точка.
- Ivan or Igor hired EN: I don't work with those two. Period.
- Money RU: Маловато для ветерана.
- Money EN: Not enough for a veteran.

### Haggles
- Ricochet hired RU: Рикошет? Ладно, но держите его подальше от меня.
- Ricochet hired EN: Ricochet? Fine, just keep him away from me.

### Mitigations
- Gus hired RU: Гас в деле? Тогда я тоже — и по старой цене.
- Gus hired EN: Gus is in? Then count me in too — old rate stands.

## Phrases — VoiceResponse

- `voice_source: ub` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Кульба готов.» / «Kulba's ready.»
  - AimAttack (1): «Очередь пошла.» / «Burst away.»
  - AimAttack (2): «Держи строй.» / «Hold the line.»
  - OpponentKilled: «За свободу.» / «For freedom.»
  - DeathGeneral: «Простите, ребята...» / «Sorry, boys...»
  - Downed: «Ранен, но не сдаюсь.» / «Hit, but not done.»
  - CombatStartDetected: «Противник на позиции.» / «Enemy in position.»
  - LevelUp: «Опыт не пропьёшь.» / «Experience doesn't fade.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду сигнала.» / «Waiting for the signal.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Kulba |
| VoiceResponseId | Jazz_Kulba |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Kulba.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Kulba_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm (two-handed auto) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ub |

## Open blockers

- none
