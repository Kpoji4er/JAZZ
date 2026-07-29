---
status: ready
priority: medium
origin: ja2
unit_id: Jazz_Flo
portrait_id: Flo
affiliation: MERC
role: Support
tier: Regular
specialization: Negotiator
gender: Female
nationality: USA
voice_source: ja2
starting_level: 2
will: 40
salary:
  starting: 500
  increase: 200
  lv1: 200
  max: 1800
medical_deposit: standard
haggling: normal
executable: true
---

# Фло — Флоренс «Фло» Габриель

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Флоренс «Фло» Габриель | Florence "Flo" Gabrielle |
| Nick | Фло | Flo |
| AllCapsNick | ФЛО | FLO |
| Title | Безголовая курица | The Headless Chicken |
| Email | Flo@merc.com | Flo@merc.com |
| snype_nick | bargain | bargain |

## Bio

**RU:** Статы 40–50, Dexterity 60, Marksmanship 38 (худшая в отряде), Wisdom 82. Трусливая, но отличная торговка — знает, где выбить скидку и где продать хлам подороже. Дружит с Биффом и Рысью; до смерти боится некой Лавы (JA2-флейвор, не реализовано как игровая механика).

**EN:** Stats in the 40-50 range, 60 Dexterity, 38 Marksmanship (worst in the roster), 82 Wisdom. Cowardly, but an excellent haggler — knows where to squeeze a discount and where to sell junk for more. Friends with Biff and Lynx; scared stiff of someone named Lava (JA2 lore flavor, not implemented as a gameplay mechanic).

## Stats

| Stat | Value |
| --- | --- |
| Health | 48 |
| Agility | 45 |
| Dexterity | 60 |
| Strength | 40 |
| Wisdom | 82 |
| Will | 40 |
| Leadership | 40 |
| Marksmanship | 38 |
| Mechanical | 15 |
| Explosives | 5 |
| Medical | 20 |
| MaxHitPoints | 48 |
| StartingLevel | 2 |

## Perks

### StartingPerks

- `Jazz_Perk_Flo`
- `Negotiator`
- `Scoundrel`
- `CancelShotPerk`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Flo` |
| type | passive |
| DisplayName RU/EN | Барахольщица / The Bargain Hunter |
| Description RU/EN | Скидки у торговцев на покупку и продажу / Shop discounts on both buying and selling |
| Mechanics | −12% to buy prices and +12% to sell prices at all shops while Flo is in the active squad (stacks with the base `Negotiator` perk's own bonus, does not multiply with it). |

## Personality

- Quirks: Coward
- Likes: `Jazz_Biff` (medium wave — Mitigation/ExtraPartingWords live once both are generated together), `Jazz_Lynx`
- Dislikes: Lava (JA2-lore flavor only — not a valid unit id in this mod, so not wired as a hard Refusal; expressed as an Idle/VR joke instead)
- National hates: —
- Refusal / Haggle notes: standard MERC money/death-toll refusals; mitigation if Biff or Lynx hired

## Hire

- Access: MERC roster
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Flo` → `JAZZ_Flo50/35/25/20`
- *50: `JazzArmor_LeatherJacketBrn`, `Makarov`, `JAZZ_AMMO_9x18_FMJ`×16 (Double), `FirstAidKit`
- *35: `JazzArmor_LeatherJacketBrn`, `Makarov`, `JAZZ_AMMO_9x18_FMJ`×16 (Double)
- *25: `JazzArmor_LeatherPants`, `Makarov`, `JAZZ_AMMO_9x18_Poor`×12 (Double)
- *20: `Makarov`, `JAZZ_AMMO_9x18_Poor`×8 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](flo.ja2-face.gif)

Файл: `flo.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `flo.ja2-face.gif` (same face identity). Frazzled American woman ~35, messy hair, civilian-tactical hybrid outfit, shopping ledger and radio in hand — NO weapon. Worried, wide-eyed look.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Ledger, radio, bargain price tags, soft satchel

## Phrases — AIM chat

### Offline
- RU: Фло не может подойти! Пишите, перезвоню, если жива буду.
- EN: Flo can't come to the phone! Leave a message, I'll call back if I'm still alive.

### GreetingAndOffer
- RU: Ой! Фло слушает... Это же не боевое задание, да?
- EN: Oh! Flo here... this isn't a combat job, is it?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Можно я постою сзади, пожалуйста?
- EN: Can I just stand in the back, please?

### PartingWords
- RU: Ладно, только без стрельбы... наверное.
- EN: Okay, just no shooting... hopefully.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Скидки у местных торговцев того стоят.
- EN: I'm staying. The discounts from the local traders make it worth it.

### Refusals
- Death toll RU: Слишком много смертей. Мне и своей жизни хватит, чтобы бояться.
- Death toll EN: Too many deaths. I'm scared enough for my own life as it is.
- Money RU: Извините, но за такие копейки я лучше дома посижу.
- Money EN: Sorry, but for that little I'd rather stay home.

### Mitigations
- Biff/Lynx hired RU: О, Бифф или Рысь уже здесь? Тогда... немного спокойнее.
- Biff/Lynx hired EN: Oh, Biff or Lynx is already in? Then... a bit calmer.

### ExtraPartingWords
- RU: Возьмите ещё Биффа — вдвоём нам не так страшно.
- EN: Take Biff too — together we're less scared.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Ф-Фло здесь!» / «F-Flo's here!»
  - AimAttack (1): «Я целюсь, честно!» / «I'm aiming, I swear!»
  - AimAttack (2): «Пожалуйста, только не в меня!» / «Please, just not at me!»
  - OpponentKilled: «Я... я попала?!» / «I... I actually hit him?!»
  - DeathGeneral: «Я знала, что этим кончится...» / «I knew it would end like this...»
  - Downed: «МЕНЯ ПОДСТРЕЛИЛИ! ПОМОГИТЕ!» / «I'M SHOT! HELP!»
  - CombatStartDetected: «О нет, о нет, это же бой!» / «Oh no, oh no, it's a fight!»
  - LevelUp: «Кажется, я не такая уж и трусиха.» / «Guess I'm not such a coward after all.»
  - AmmoLow: «Патроны кончаются... как и моя смелость.» / «Running low on ammo... and courage.»
  - Idle: «Только бы тут не было Лавы...» / «Just hope Lava's not around...»
  - MockDislike (flavor): «Лава страшнее любого солдата.» / «Lava's scarier than any soldier.»
  - Praises (Biff/Lynx present): «Хорошо, что кто-то знакомый рядом.» / «Good to have someone familiar close by.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Flo |
| VoiceResponseId | Jazz_Flo |
| pollyvoice | Amy |
| Portrait | Mod/Dv3mFVN/MercPortraits/Flo.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Flo_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
