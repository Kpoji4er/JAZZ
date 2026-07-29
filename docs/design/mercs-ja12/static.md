---
status: ready
priority: low
origin: ja2
unit_id: Jazz_Static
portrait_id: Static
affiliation: AIM
role: Mechanic
tier: Veteran
specialization: Mechanic
gender: Male
nationality: USA
voice_source: ja2
starting_level: 4
will: 50
salary:
  starting: 1400
  increase: 150
  lv1: 600
  max: 3500
medical_deposit: standard
haggling: normal
executable: true
---

# Статик — Кирк «Статик» Стивенсон

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Кирк «Статик» Стивенсон | Kirk "Static" Stevenson |
| Nick | Статик | Static |
| AllCapsNick | СТАТИК | STATIC |
| Title | Хиппи-механик | The Hippie Mechanic |
| Email | Static@aim.com | Static@aim.com |
| snype_nick | static | static |

## Bio

**RU:** Статы 60–80, Strength 59, Dexterity 95, Wisdom 60, Mechanical 99. Боится насекомых. Дружит со Спайдером и обкуренным Ларри; не любит трезвого Ларри, Ротмана, Блэйда; недолюбливает швейцарцев.

**EN:** Stats in the 60-80 range, 59 Strength, 95 Dexterity, 60 Wisdom, 99 Mechanical. Terrified of insects. Friends with Spider and a stoned Larry; can't stand a sober Larry, Rothman, or Blade; not fond of the Swiss.

## Stats

| Stat | Value |
| --- | --- |
| Health | 70 |
| Agility | 75 |
| Dexterity | 95 |
| Strength | 59 |
| Wisdom | 60 |
| Will | 50 |
| Leadership | 20 |
| Marksmanship | 55 |
| Mechanical | 99 |
| Explosives | 20 |
| Medical | 15 |
| MaxHitPoints | 70 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `Jazz_Perk_Static`
- `MrFixit`
- `JackOfAllTrades`
- `Scoundrel`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Static` |
| type | passive |
| DisplayName RU/EN | Экономия запчастей / Parts Saver |
| Description RU/EN | Ремонт и крафт обходятся дешевле по запчастям — бонус растёт с уровнем Статика / Repairing and crafting cost fewer Parts, and the discount grows with Static's level |
| Mechanics | Repair and craft actions performed by Static cost 5% fewer Parts per Static's current level (level 4 = −20%), capped at −25% at level 5+. |

## Personality

- Quirks: FearInsects (bio flavor only — no matching JA3 status perk, not wired)
- Likes: `Jazz_Spider` (planned merc — Mitigation/ExtraPartingWords wiring activates once Spider is generated), `Larry` (drugged/default persona)
- Dislikes: `Jazz_Rothman`, `Jazz_Blade` (both planned mercs — Refusal wiring activates once they are ready), `Larry_Clean` (sober Larry persona specifically, not the default `Larry`)
- National hates: Swiss — Haggle trigger when the active squad is full of Swiss-nationality mercs
- Refusal / Haggle notes: refuses if Rothman, Blade, or sober Larry (`Larry_Clean`) is hired; refuses on excessive death toll; haggles when squad is all-Swiss; mitigation and recommendation for Spider/Larry when hired

## Hire

- Access: AIM hire
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Static` → `JAZZ_Static50/35/25/20`
- *50: `JazzArmor_LeatherJacketBrn`, `Lockpick`, `Wirecutter`, `MicroUZI`, `JAZZ_AMMO_9x19_FMJ`×32 (Double), `Parts`×20
- *35: `JazzArmor_LeatherArmor`, `Lockpick`, `Scorpion`, `JAZZ_AMMO_762x25_FMJ`×30 (Double), `Parts`×15
- *25: `JazzArmor_LeatherArmor`, `Lockpick`, `Makarov`, `JAZZ_AMMO_9x18_FMJ`×24 (Double)
- *20: `JazzArmor_UniformPants`, `Lockpick`, `Makarov`, `JAZZ_AMMO_9x18_Poor`×16 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](static.ja2-face.gif)

Файл: `static.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `static.ja2-face.gif` (same face identity). Hippie mechanic ~35, longish hair, welding goggles pushed up on forehead, tool bandolier and multimeter on belt — NO gun. Laid-back grin.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Tool bandolier, welding goggles, multimeter, AIM pin

## Phrases — AIM chat

### Offline
- RU: Статик в отключке. Позвоните позже.
- EN: This is Static. Leave a message.

### GreetingAndOffer
- RU: Йо, Статик на проводе. Что чинить?
- EN: Static here. What needs fixing?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Мир... и гайки, чувак.
- EN: Peace... and wrenches, man.

### PartingWords
- RU: Окей, собираю чемодан с инструментами.
- EN: Okay, packing up my toolbox.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Тут ещё есть что чинить.
- EN: I'm staying. Still stuff to fix here.

### Refusals
- Rothman/Blade/sober Larry hired RU: Пока Ротман, Блэйд или трезвый Ларри у вас в отряде — я пас. Не моя вибрация.
- Rothman/Blade/sober Larry hired EN: Not while Rothman, Blade, or a sober Larry are on your team. Bad vibes, man.
- Death toll RU: Слишком много трупов вокруг вас. Не моя карма.
- Death toll EN: Too many bodies around you. That's not my karma.

### Haggles
- Swiss mercs hired RU: Отряд из одних швейцарцев? Ладно, но накинь сверху.
- Swiss mercs hired EN: A squad full of Swiss mercs? Fine, but it'll cost extra.

### Mitigations
- Spider/drugged Larry hired RU: О, Паук (или обдолбанный Ларри) уже здесь? Тогда я точно в деле.
- Spider/drugged Larry hired EN: Oh, Spider (or a drugged-up Larry) is already in? Then I'm definitely in.

### ExtraPartingWords
- RU: Если нужен ещё один спец по железу — зовите Паука.
- EN: If you need another gear-head, call Spider.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Статик на месте.» / «Static's here.»
  - AimAttack (1): «Целюсь... наверное.» / «Aiming... probably.»
  - AimAttack (2): «Ща разберёмся.» / «Let's sort this out.»
  - OpponentKilled: «Готово.» / «Done.»
  - DeathGeneral: «Отключаюсь...» / «Powering down...»
  - Downed: «Меня зацепило, чувак.» / «I'm hit, man.»
  - CombatStartDetected: «Ого, гости.» / «Whoa, company.»
  - LevelUp: «Прокачался, чувак.» / «Leveled up, man.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду сигнала.» / «Waiting for a signal.»
  - MockDislike (Rothman/Blade/sober Larry): «Хорошо, что этих зануд тут нет.» / «Glad those squares aren't here.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Static |
| VoiceResponseId | Jazz_Static |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Static.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Static_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
