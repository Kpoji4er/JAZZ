---
status: ready
priority: medium
origin: ja2
unit_id: Jazz_Biff
portrait_id: Biff
affiliation: MERC
role: Commander
tier: Regular
specialization: Leader
gender: Male
nationality: USA
voice_source: ja2
starting_level: 2
will: 35
salary:
  starting: 600
  increase: 200
  lv1: 300
  max: 2000
medical_deposit: small
haggling: normal
executable: true
---

# Бифф — Бифф Апскотт

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Бифф Апскотт | Biff Upscott |
| Nick | Бифф | Biff |
| AllCapsNick | БИФФ | BIFF |
| Title | Ссыкло MERC | The MERC Coward |
| Email | Biff@merc.com | Biff@merc.com |
| snype_nick | biff | biff |

## Bio

**RU:** Статы около 70, Strength 41, Wisdom 58, Marksmanship 57, Leadership 13. Кабинетный менеджер MERC, панически боится настоящего боя, но неплохо ведёт бумажную работу отряда. Дружит с Фло и трезвым Ларри; не выносит обдолбанного Ларри. В JA2 Бифф появлялся только после отдельного побочного квеста — в JAZZ этот сюжет не реализован, поэтому найм идёт как обычный контракт MERC, а история квеста осталась только в биографии.

**EN:** Stats around 70, 41 Strength, 58 Wisdom, 57 Marksmanship, 13 Leadership. A desk-bound MERC manager, terrified of real combat but decent at running the squad's paperwork. Friends with Flo and a clean Larry; can't stand Larry when he's using. In JA2, Biff only became available after a dedicated side quest — that quest line doesn't exist in JAZZ's current scope, so his hire is a standard MERC contract; the quest backstory survives only as Bio flavor.

## Stats

| Stat | Value |
| --- | --- |
| Health | 70 |
| Agility | 65 |
| Dexterity | 60 |
| Strength | 41 |
| Wisdom | 58 |
| Will | 35 |
| Leadership | 13 |
| Marksmanship | 57 |
| Mechanical | 20 |
| Explosives | 15 |
| Medical | 25 |
| MaxHitPoints | 70 |
| StartingLevel | 2 |

## Perks

### StartingPerks

- `Jazz_Perk_Biff`
- `Negotiator`
- `ShoulderToShoulder`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Biff` |
| type | operation |
| DisplayName RU/EN | Вербовка MERC / MERC Recruitment Drive |
| Description RU/EN | Пока Бифф гарнизоном стоит в секторе с активным набором ополчения, он может провести спецоперацию, вербующую бойца MERC вместо обычного ополченца / While Biff is garrisoned in a sector actively training militia, he can run a special operation that produces a MERC trooper instead of a standard militia recruit |
| Mechanics | Sector operation, usable once every 7 days while Biff is garrisoned in a sector with an active militia-training slot. Converts that training slot's output into 1 MERC trooper unit at the same resource/time cost as a normal militia recruit. Does not stack with itself in the same sector. |

## Personality

- Quirks: Coward
- Likes: `Jazz_Flo` (medium wave — Mitigation/ExtraPartingWords live once both are generated together), `Larry_Clean`
- Dislikes: `Larry` (drugged persona specifically, not `Larry_Clean`)
- National hates: —
- Refusal / Haggle notes: refuses if drugged Larry hired; standard money/death-toll refusals; mitigation if Flo or clean Larry hired

## Hire

- Access: **world-gated MERC** — Speck Day-2 mail unlocks the M.E.R.C. site and asks the player to find Biff; Biff is not on the shelf until RescueBiff/meet (`JAZZ_MERC_MarkMet`). Then hire on the spot **or** he returns as Available on MERC.
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0
- Affiliation: `MERC` (`Jazz_Biff`)

## Inventory

- Equipment loot id: `Loot_JAZZ_Biff` → `JAZZ_Biff50/35/25/20`
- *50: `JazzArmor_PoliceVest`, `Makarov`, `JAZZ_AMMO_9x18_FMJ`×16 (Double), `FirstAidKit`
- *35: `JazzArmor_LeatherJacketBrn`, `Makarov`, `JAZZ_AMMO_9x18_FMJ`×16 (Double)
- *25: `JazzArmor_LeatherJacketBrn`, `Colt38Special`, `JAZZ_AMMO_38special_FMJ`×12 (Double)
- *20: `JazzArmor_LeatherJacketBrn`, `Colt38Special`, `JAZZ_AMMO_38special_FMJ`×12 (Double)

## JA2 face reference

Нет файла в архиве `портировать.rar` для этого мерка. Перед генерацией портрета добавить `biff.ja2-face.*` или явно согласовать face ref.

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Nervous, overweight American desk merc ~40, sweaty brow, ill-fitting MERC uniform shirt, clipboard and MERC badge — holstered pistol only. Anxious, forced smile.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Clipboard, MERC badge, soft armor, holstered pistol

## Phrases — AIM chat

### Offline
- RU: Бифф... э-э... перезвоните, пожалуйста?
- EN: This is Biff. Uh, please call back?

### GreetingAndOffer
- RU: Э... Бифф на связи. Вы серьёзно насчёт боевого задания?
- EN: Uh... Biff here. You're serious about a combat job?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Можно... без стрельбы обойтись?
- EN: Can we... skip the shooting part?

### PartingWords
- RU: Ладно... я попробую. Только пусть кто-нибудь прикроет.
- EN: Okay... I'll try. Just make sure someone's got my back.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Наверное.
- EN: I'm staying. Probably.

### Refusals
- Larry (drugged) hired RU: Пока обдолбанный Ларри в отряде — нет, увольте. Мне и так страшно.
- Larry (drugged) hired EN: Not while a drugged-up Larry's on the roster — no thanks. I'm scared enough already.
- Money RU: Извините, но за такие деньги рисковать шкурой не готов.
- Money EN: Sorry, but I'm not risking my neck for that little.

### Mitigations
- Flo/Larry_Clean hired RU: О, Фло или трезвый Ларри уже здесь? Тогда... наверное, не так страшно.
- Flo/Larry_Clean hired EN: Oh, Flo or a clean Larry's already in? Then... maybe it's not so scary.

### ExtraPartingWords
- RU: Если найдёте Фло — берите, вместе нам как-то спокойнее.
- EN: If you find Flo, take her — somehow we're calmer together.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Б-бифф здесь!» / «B-Biff's here!»
  - AimAttack (1): «Ой... ладно, стреляю!» / «Oh... okay, firing!»
  - AimAttack (2): «Пожалуйста, промахнись мимо меня.» / «Please miss me.»
  - OpponentKilled: «Я... я попал?!» / «I... I actually hit him?!»
  - DeathGeneral: «Я же говорил, что это плохая идея...» / «I told you this was a bad idea...»
  - Downed: «МЕНЯ ПОДСТРЕЛИЛИ! ПОМОГИТЕ!» / «I'M SHOT! HELP!»
  - CombatStartDetected: «О нет, о нет, о нет...» / «Oh no, oh no, oh no...»
  - LevelUp: «Кажется, я не такой уж и трус.» / «Guess I'm not such a coward after all.»
  - AmmoLow: «Патроны кончаются, а страх — нет!» / «Running out of ammo, not out of fear!»
  - Idle: «Можно я постою тут, сзади?» / «Can I just stand back here?»
  - MockDislike (Larry drugged): «Только бы Ларри не притащил свои таблетки.» / «Just hope Larry didn't bring his pills.»
  - Praises (Flo present): «Хорошо, что Фло тоже нервничает — не так одиноко.» / «Good that Flo's nervous too — makes it less lonely.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Biff |
| VoiceResponseId | Jazz_Biff |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Biff.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Biff_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
