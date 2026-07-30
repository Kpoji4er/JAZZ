---
status: ready
priority: low
origin: ja2
unit_id: Jazz_Highball
portrait_id: Highball
affiliation: AIM
role: Doctor
tier: Regular
specialization: Doctor
gender: Male
nationality: USA
voice_source: ja2
starting_level: 3
will: 40
salary:
  starting: 900
  increase: 150
  lv1: 400
  max: 2500
medical_deposit: small
haggling: normal
executable: true
---

# Скала — Клиффорд «Скала» Хайбол

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Клиффорд «Скала» Хайбол | Clifford "Highball" Hyball |
| Nick | Скала | Highball |
| AllCapsNick | СКАЛА | HIGHBALL |
| Title | Старый алкаш | The Old Drunk |
| Email | Highball@aim.com | Highball@aim.com |
| snype_nick | highball | highball |

## Bio

**RU:** Худшие боевые статы в каталоге AIM (~50–60), но Wisdom 87, Marksmanship 84, Medical 84 всё ещё держат марку. Держится нейтрально к остальному отряду — слишком занят собственной фляжкой, чтобы с кем-то ссориться.

**EN:** Some of the worst combat stats in the AIM roster (~50-60 range), but 87 Wisdom, 84 Marksmanship, and 84 Medical still get the job done. Stays neutral toward the rest of the roster — too busy with his flask to pick fights.

## Stats

| Stat | Value |
| --- | --- |
| Health | 55 |
| Agility | 50 |
| Dexterity | 55 |
| Strength | 55 |
| Wisdom | 87 |
| Will | 40 |
| Leadership | 20 |
| Marksmanship | 84 |
| Mechanical | 10 |
| Explosives | 10 |
| Medical | 84 |
| MaxHitPoints | 55 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Highball`
- `Savior`
- `OldDog`
- `JackOfAllTrades`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Highball` |
| type | passive |
| DisplayName RU/EN | Полевой химик / Field Chemist |
| Description RU/EN | Может скрафтить стимулятор из бинтов без доступа к сумке врача — раз в игровой день / Can craft a combat stimulant from Meds without access to a Doctor's Bag facility — once per in-game day |
| Mechanics | Once per in-game day, while in any sector, Highball may craft one `CombatStim` from 3× `Meds` using a Medical skill check (succeeds automatically at Medical ≥50); no Doctor's Bag facility or workbench required. |

## Personality

- Quirks: Alcoholic (bio flavor only — no matching JA3 status perk, not wired)
- Likes: —
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: no relationship triggers; standard AIM money and excessive death-toll refusals only

## Hire

- Access: AIM hire
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Highball` → `JAZZ_Highball50/35/25/20`
- *50: `JazzArmor_LeatherVest`, `Meds`×30, `FirstAidKit`, `CombatStim`×1, `SWModel19`, `JAZZ_AMMO_357_FMJ`×18 (Double)
- *35: `JazzArmor_UniformPants`, `Meds`×20, `FirstAidKit`, `Colt38Special`, `JAZZ_AMMO_38special_FMJ`×12 (Double)
- *25: `Meds`×15, `SWModel10`, `JAZZ_AMMO_38special_FMJ`×12 (Double)
- *20: `Meds`×10, `SWModel10`, `JAZZ_AMMO_38special_FMJ`×6 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](highball.ja2-face.gif)

Файл: `highball.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `highball.ja2-face.gif` (same face identity). Elderly alcoholic doctor ~60, red nose, stained medic coat with a hip flask and pill bottles, holstered revolver only — NO weapon in hands.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Flask, pill bottles, medic armband, battered bag

## Phrases — AIM chat

### Offline
- RU: Хайбол... икает... позже перезвонит.
- EN: This is Highball. Leave a message.

### GreetingAndOffer
- RU: Скала на линии. Ик. Что там у вас?
- EN: Highball here. What've you got?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Ещё по одной — и я весь ваш.
- EN: One more round, and I'm all yours.

### PartingWords
- RU: Ладно... фляжку с собой, и иду.
- EN: Alright... flask packed, I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Тут веселее, чем дома.
- EN: I'm staying. Livelier than home.

### Refusals
- Money RU: На такие деньги даже фляжку не наполнишь.
- Money EN: That wouldn't even fill my flask.
- Death toll RU: Слишком много крови для старого доктора.
- Death toll EN: Too much blood for an old doctor.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Скала слушает.» / «Highball's listening.»
  - AimAttack (1): «Рука твёрже, чем кажется.» / «Steadier hand than it looks.»
  - AimAttack (2): «За удачу.» / «For luck.»
  - OpponentKilled: «Ну вот и всё.» / «Well, that's that.»
  - DeathGeneral: «Последний глоток...» / «One last sip...»
  - Downed: «Аптечка... где аптечка...» / «Med kit... where's the kit...»
  - CombatStartPlayer: «О, бой. Некстати.» / «Oh, a fight. Bad timing.»
  - LevelUp: «Ещё не всё пропито.» / «Still got something left in me.»
  - AmmoLow: «Патроны кончаются.» / «Running low on ammo.»
  - Idle: «Ещё по одной?» / «One more round?»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Highball |
| VoiceResponseId | Jazz_Highball |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Highball.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Highball_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
