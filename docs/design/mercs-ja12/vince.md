---
status: ready
priority: low
origin: ja2
unit_id: Jazz_Vince
portrait_id: Vince
affiliation: Locals
role: Doctor
tier: Veteran
specialization: Doctor
gender: Male
nationality: USA
voice_source: ja2
starting_level: 4
will: 70
salary:
  starting: 1200
  increase: 150
  lv1: 500
  max: 4000
medical_deposit: small
haggling: normal
executable: true
---

# Винс — Доктор Винсент «Винс»

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Доктор Винсент «Винс» | Doctor Vincent "Vince" |
| Nick | Винс | Vince |
| AllCapsNick | ВИНС | VINCE |
| Title | Ментор | The Mentor |
| Email | Vince@arulco.med | Vince@arulco.med |
| snype_nick | vince | vince |

## Bio

**RU:** Health 94, Dexterity 92, Agility 49, Marksmanship 35, Wisdom 94, Medical 94, Leadership 33. Быстро учится сам и легко учит других; одинаково хорошо стреляет и лечит обеими руками. Страдает клаустрофобией.

**EN:** 94 Health, 92 Dexterity, 49 Agility, 35 Marksmanship, 94 Wisdom, 94 Medical, 33 Leadership. A fast learner who's just as quick to teach others; shoots and treats wounds equally well with either hand. Suffers from claustrophobia.

## Stats

| Stat | Value |
| --- | --- |
| Health | 94 |
| Agility | 49 |
| Dexterity | 92 |
| Strength | 60 |
| Wisdom | 94 |
| Will | 70 |
| Leadership | 33 |
| Marksmanship | 35 |
| Mechanical | 20 |
| Explosives | 10 |
| Medical | 94 |
| MaxHitPoints | 94 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `Jazz_Perk_Vince`
- `Claustrophobic`
- `Ambidextrous`
- `Teacher`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Vince` |
| type | passive |
| DisplayName RU/EN | Полевой наставник / Field Mentor |
| Description RU/EN | Раз за бой лечение или подъём товарища возвращает ему ОД / Once per combat, healing or reviving an ally snaps them back into the fight with bonus AP |
| Mechanics | Once per combat, the first time Vince heals a wounded ally or revives a Downed ally, that ally immediately gains +4 AP that turn. |

## Personality

- Quirks: Claustrophobic
- Likes: —
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: no relationship triggers; standard local money and death-toll refusals only

## Hire

- Access: Locals hire
- MedicalDeposit: small; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Vince` → `JAZZ_Vince50/35/25/20`
- *50: `JazzArmor_PoliceVest`, `Meds`×30, `FirstAidKit`, `Medkit`, `HiPower`×2 (dual-wield, ambidextrous), `JAZZ_AMMO_9x19_FMJ`×32 (Double)
- *35: `JazzArmor_LeatherVest`, `Meds`×20, `FirstAidKit`, `Colt1911`×2, `JAZZ_AMMO_45ACP_FMJ`×24 (Double)
- *25: `Meds`×15, `FirstAidKit`, `Makarov`, `JAZZ_AMMO_9x18_FMJ`×16 (Double)
- *20: `Meds`×10, `SWModel10`, `JAZZ_AMMO_38special_FMJ`×12 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](vince.ja2-face.gif)

Файл: `vince.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**. Face must match JA2 reference above.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `vince.ja2-face.gif` (same face identity). Calm mentor doctor ~40, glasses, medical satchel and a worn textbook under one arm — NO gun.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Medical satchel, textbook, glasses, medic patch

## Phrases — AIM chat

### Offline
- RU: Доктор Винс на операции. Перезвоните.
- EN: This is Doctor Vince. Leave a message.

### GreetingAndOffer
- RU: Винсент слушает. Кого нужно подлатать?
- EN: Vincent here. Who needs patching up?

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Всегда рад научить чему-то новому.
- EN: Always happy to teach something new.

### PartingWords
- RU: Готов учить и лечить. Иду.
- EN: Ready to teach and to heal. I'm in.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Ещё многому могу научить.
- EN: I'm staying. Still plenty to teach.

### Refusals
- Money RU: Мой опыт стоит дороже.
- Money EN: My experience is worth more than that.
- Death toll RU: Слишком много раненых на вашем счету для спокойной практики.
- Death toll EN: Too many wounded on your record for a calm practice.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Винс на связи.» / «Vince is up.»
  - AimAttack (1): «Обеими руками, спокойно.» / «Both hands, steady.»
  - AimAttack (2): «Вижу цель.» / «Target in sight.»
  - OpponentKilled: «Чисто сработано.» / «Clean work.»
  - DeathGeneral: «Не смог откачать сам себя...» / «Couldn't save myself...»
  - Downed: «Ранен — сам себя не подниму.» / «I'm down — can't patch myself up.»
  - CombatStartPlayer: «Начинаем. Аптечка со мной.» / «Let's go. Kit's on me.»
  - LevelUp: «Учиться никогда не поздно.» / «Never too late to learn.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Жду. Пульс в норме.» / «Waiting. Pulse is fine.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Vince |
| VoiceResponseId | Jazz_Vince |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Vince.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Vince_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm (ambidextrous dual pistols) |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
