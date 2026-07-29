---
status: ready
priority: medium
origin: ub
unit_id: Jazz_Horg
portrait_id: Horg
affiliation: MERC
role: HeavyWeapons
tier: Veteran
specialization: HeavyWeapons
gender: Male
nationality: USA
voice_source: ub
starting_level: 4
will: 60
salary:
  starting: 2700
  increase: 200
  lv1: 1100
  max: 6500
medical_deposit: standard
haggling: normal
executable: true
---

# Сигара — Лейтенант Хорг «Сигара»

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Лейтенант Хорг «Сигара» | Lieutenant Horg "Cigar" |
| Nick | Сигара | Horg |
| AllCapsNick | СИГАРА | HORG |
| Title | Сигара | The Cigar |
| Email | Horg@merc.com | Horg@merc.com |
| snype_nick | cigar | cigar |

## Bio

**RU:** Urban Brawl. Health 98, Strength 94, Agility 78, Marksmanship 89, Mechanical 74, Wisdom 77. Агрессивный лейтенант, никогда не расстаётся с сигарой. Дружит с Быком, Гасом и Биффом; терпеть не может Колби и относится с презрением к слухам про Лаву.

**EN:** Urban Brawl. Health 98, Strength 94, Agility 78, 89 Marksmanship, 74 Mechanical, 77 Wisdom. An aggressive lieutenant who never puts down his cigar. Friends with Bull, Gus, and Biff; can't stand Colby, and dismisses the Lava rumors as talk.

## Stats

| Stat | Value |
| --- | --- |
| Health | 98 |
| Agility | 78 |
| Dexterity | 75 |
| Strength | 94 |
| Wisdom | 77 |
| Will | 60 |
| Leadership | 35 |
| Marksmanship | 89 |
| Mechanical | 74 |
| Explosives | 50 |
| Medical | 20 |
| MaxHitPoints | 98 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `Jazz_Perk_Horg`
- `HeavyWeaponsTraining`
- `Hardened`
- `ShoulderToShoulder`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Horg` |
| type | passive |
| DisplayName RU/EN | Тяжёлая рука / Heavy Hand |
| Description RU/EN | Меньше отдачи и штрафов точности от тяжёлого оружия / Reduced recoil and accuracy penalties from heavy weapons |
| Mechanics | Horg's `HeavyWeapons`-category attacks (grenade launchers, RPGs, machineguns) get -30% to the normal recoil/CTH penalty they apply to his next shot, and he ignores the Strength requirement penalty for heavy weapons entirely (treated as if he always met the Strength threshold). |

## Personality

- Quirks: Aggressive
- Likes: `Bull` (planned merc — Mitigation/ExtraPartingWords wiring activates once ready), `Gus`, `Biff`
- Dislikes: `Jazz_Colby` (Refusal wiring live immediately, both already generated)
- National hates: —
- Refusal / Haggle notes: refuses if Colby hired; standard MERC money/death-toll refusals; mitigation if Bull, Gus, or Biff hired; the Lava rumor is flavor-only and not wired

## Hire

- Access: MERC roster (Urban Brawl origin)
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Horg` → `JAZZ_Horg50/35/25/20`
- *50: `JazzArmor_FlakM1955`, `M79`, `JAZZ_AMMO_40mmFragGrenade`×8, `M16A1`, `JAZZ_AMMO_556_FMJ`×60 (Double)
- *35: `JazzArmor_FlakM1955`, `M79`, `JAZZ_AMMO_40mmFragGrenade`×5, `M16A1`, `JAZZ_AMMO_556_FMJ`×40 (Double)
- *25: `JazzArmor_LeatherArmor`, `M16A1`, `JAZZ_AMMO_556_FMJ`×40 (Double), `FragGrenade`×2
- *20: `JazzArmor_LeatherArmor`, `M16A1`, `JAZZ_AMMO_556_FMJ`×30 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](horg.ja2-face.jpg)

Файл: `horg.ja2-face.jpg`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `horg.ja2-face.jpg` (same face identity). Huge American LT ~40 with cigar, heavy flak vest and grenade bandolier — NO launcher in hands. Aggressive grin.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Cigar, grenade bandolier, heavy flak vest, LT shoulder bars

## Phrases — AIM chat

### Offline
- RU: Сигара курит — не мешать. Пиши, отвечу позже.
- EN: Horg's smoking — don't interrupt. Leave a message, I'll answer later.

### GreetingAndOffer
- RU: Хорг. Говори, что надо.
- EN: Horg here. Say what you need.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Ну? Сигара сама себя не докурит.
- EN: Well? This cigar won't finish itself.

### PartingWords
- RU: Беру тяжёлое и еду.
- EN: Grabbing the heavy gear and moving out.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Ещё есть, что взрывать.
- EN: I'm staying. Still stuff to blow up.

### Refusals
- Colby hired RU: Пока Колби в отряде — нет. Не выношу этого типа.
- Colby hired EN: Not while Colby's on the team. Can't stand the guy.
- Death toll RU: Слишком много наших полегло. Мне это не нравится.
- Death toll EN: Too many of ours went down. I don't like it.

### Mitigations
- Bull/Gus/Biff hired RU: Бык, Гас или Бифф уже здесь? Тогда я точно в деле.
- Bull/Gus/Biff hired EN: Bull, Gus, or Biff already in? Then I'm definitely in.

### ExtraPartingWords
- RU: Возьмите ещё Гаса — с ним и потяжелее груз не проблема.
- EN: Grab Gus too — even the heaviest load's no problem with him around.

## Phrases — VoiceResponse

- `voice_source: ub` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Сигара на месте.» / «Horg's in position.»
  - AimAttack (1): «Заряжаю тяжёлое!» / «Loading the heavy stuff!»
  - AimAttack (2): «Получите гранату!» / «Take a grenade!»
  - OpponentKilled: «Разнесло в клочья.» / «Blown to pieces.»
  - DeathGeneral: «Сигара догорела...» / «The cigar's burned out...»
  - Downed: «Зацепило! Но сигара при мне.» / «Got hit! But the cigar's still with me.»
  - CombatStartDetected: «Контакт! К бою!» / «Contact! Stand to!»
  - LevelUp: «Ещё сильнее бью.» / «Hitting even harder now.»
  - AmmoLow: «Гранаты кончаются!» / «Running low on grenades!»
  - Idle: «Жду команды.» / «Waiting for orders.»
  - MockDislike (Colby): «Только бы Колби не путался под ногами.» / «Just hope Colby doesn't get underfoot.»
  - Praises (Bull/Gus/Biff present): «С такими ребятами любое дело по плечу.» / «With guys like these, any job's doable.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Horg |
| VoiceResponseId | Jazz_Horg |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Horg.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Horg_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ub |

## Open blockers

- none
