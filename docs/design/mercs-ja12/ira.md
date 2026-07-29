---
status: ready
priority: high
origin: ja2
unit_id: Jazz_Ira
portrait_id: Ira
affiliation: Locals
role: Commander
tier: Regular
specialization: Leader
gender: Female
nationality: USA
voice_source: ja2
starting_level: 2
will: 70
salary:
  starting: 400
  increase: 200
  lv1: 200
  max: 1500
medical_deposit: none
haggling: normal
executable: true
---

# Айра — Айра Смит

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Айра Смит | Ira Smith |
| Nick | Айра | Ira |
| AllCapsNick | АЙРА | IRA |
| Title | Царица ополчения | Queen of the Militia |
| Email | Ira@arulco.reb | Ira@arulco.reb |
| snype_nick | givegun | givegun |

## Bio

**RU:** Слабые боевые статы и меткость 55, но для ополченцев Арулько — живой бог: любой встреченный ею новобранец учится быстрее. Leadership низкий на старте, компенсируется именным перком и статусом Locals. Дружит с Мигелем, Карлосом и Димитрием (местное сопротивление); не любит Злобного; не умеет плавать (флейвор, без игровой механики).

**EN:** Weak combat stats and 55 Marksmanship, but to the Arulco militia she's a living legend — every recruit she meets learns faster. Leadership starts low, offset by her named perk and Locals status. Friends with Miguel, Carlos, and Dimitri (fellow resistance); can't stand Vicious; never learned to swim (flavor only, no gameplay penalty).

## Stats

| Stat | Value |
| --- | --- |
| Health | 65 |
| Agility | 60 |
| Dexterity | 55 |
| Strength | 50 |
| Wisdom | 70 |
| Will | 70 |
| Leadership | 14 |
| Marksmanship | 55 |
| Mechanical | 20 |
| Explosives | 10 |
| Medical | 40 |
| MaxHitPoints | 65 |
| StartingLevel | 2 |

## Perks

### StartingPerks

- `Jazz_Perk_Ira`
- `Teacher`
- `ShoulderToShoulder`
- `MinFreeMove`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Ira` |
| type | passive |
| DisplayName RU/EN | Народный командир / People's Commander |
| Description RU/EN | Пока Айра стоит гарнизоном в секторе, обучение местного ополчения там идёт вдвое быстрее / While Ira is garrisoned in a sector, militia training there completes in half the normal time |
| Mechanics | Stacks additively with the base `Teacher` perk: militia training speed +50% in Ira's home sector (implementation detail — final numeric tuning happens at code time, but the design intent and floor value are fixed here so there is no open balance question). Applies only to Locals-affiliated squads, not to AIM/MERC training. |

## Personality

- Quirks: flavor-only "can't swim" line in Bio/AIM chat — JA3 has no swim-penalty system, so this is not implemented as a StartingPerk or hire condition
- Likes: Miguel, Carlos, Dimitri (all planned mercs — Mitigation/ExtraPartingWords wiring activates once each reaches `status: ready`)
- Dislikes: `Jazz_Vicious` (planned merc — Refusal wiring activates once ready)
- National hates: none mechanical — the "irony" of an American leading anti-American-funded excess is Bio flavor only, not a hire condition
- Refusal / Haggle notes: local hire, no AIM/MERC contract fee; refuses only if Vicious already hired

## Hire

- Access: Locals — unlocked after completing the "Meet the Resistance" quest contact in the first sector liberated from Legion control; recruits immediately once contact is made, no travel fee
- MedicalDeposit: none; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Ira` → `JAZZ_Ira50/35/25/20`
- *50: `JazzArmor_LeatherArmor`, `Colt1911`, `JAZZ_AMMO_45ACP_FMJ`×28 (Double), `FirstAidKit`, `Meds`×20, `Lockpick`
- *35: `JazzArmor_LeatherArmor`, `HiPower`, `JAZZ_AMMO_9x19_FMJ`×48 (Double), `FirstAidKit`
- *25: `JazzArmor_LeatherJacketBrn`, `P210`, `JAZZ_AMMO_9x19_FMJ`×60 (Double), `Meds`×10
- *20: `JazzArmor_LeatherJacketBrn`, `P210`, `JAZZ_AMMO_9x19_FMJ`×60 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](ira.ja2-face.gif)

Файл: `ira.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `ira.ja2-face.gif` (same face identity). Young determined American woman among rebels, dark hair tied back, militia instructor look, clipboard/map case and whistle on chest — NO rifle. Stern protective expression.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Militia instructor clipboard, map case, whistle, rebel armband

## Phrases — AIM chat

### Offline
- RU: Айра. Если это про пулемёт для ребят — говорите после сигнала.
- EN: This is Ira. If it's about a gun for the boys, talk after the beep.

### GreetingAndOffer
- RU: Ну? Пулемёта дашь или опять только советы?
- EN: Well? You bringing guns, or just more advice?

### ConversationRestart
- RU: Связь прервалась. Ополчение ждать не будет — давай к делу.
- EN: Line dropped. The militia won't wait — let's get to it.

### IdleLine
- RU: Война идёт — не мешкай, у меня люди на позициях.
- EN: There's a war on — don't dawdle, I've got people holding positions.

### PartingWords
- RU: Беру своих ребят и иду. Только скажи, где стрелять.
- EN: I'm bringing my people. Just tell me where to shoot.

### RehireIntro
- RU: Контракт заканчивается. Сектор ещё не спокоен — продлеваем?
- EN: Contract's ending. The sector's not settled yet — extending?

### RehireOutro
- RU: Остаюсь. Мои люди меня одну не отпустят.
- EN: I'm staying. My people won't let me go alone anyway.

### Refusals
- Vicious hired RU: Пока Злобный у вас — я в отряд не пойду. Он моих людей пугает.
- Vicious hired EN: Not while Vicious is on your payroll. He scares my people.

### Mitigations
- Miguel/Carlos/Dimitri hired RU: Раз кто-то из наших уже с вами — значит, вам можно доверять. Согласна.
- Miguel/Carlos/Dimitri hired EN: If one of our own is already with you, that tells me you're trustworthy. I'm in.

### ExtraPartingWords
- RU: Найдёте Мигеля, Карлоса или Димитрия — берите не думая, это наши лучшие люди.
- EN: If you find Miguel, Carlos, or Dimitri, take them without hesitation — our best people.

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Айра здесь.» / «Ira's here.»
  - AimAttack (1): «За Арулько!» / «For Arulco!»
  - AimAttack (2): «Держим позицию.» / «Holding the line.»
  - OpponentKilled: «Один меньше.» / «One less.»
  - DeathGeneral: «Простите, ребята...» / «Sorry, everyone...»
  - Downed: «Меня ранили — прикройте!» / «I'm hit — cover me!»
  - CombatStartDetected: «К оружию!» / «To arms!»
  - LevelUp: «Учусь на ходу.» / «Learning as I go.»
  - AmmoLow: «Патроны на исходе!» / «Running low on ammo!»
  - Idle: «Жду сигнала.» / «Waiting for the signal.»
  - MockDislike (Vicious): «Хоть бы Злобного тут не было.» / «Just glad Vicious isn't here.»
  - Praises (Miguel/Carlos/Dimitri present): «Рада драться рядом со своими.» / «Good to fight beside my own.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Ira |
| VoiceResponseId | Jazz_Ira |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Ira.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Ira_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
