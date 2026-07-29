---
status: ready
priority: medium
origin: ub
unit_id: Jazz_Manuel
portrait_id: Manuel
affiliation: Locals
role: Scout
tier: Regular
specialization: Stealth
gender: Male
nationality: Arulco
voice_source: nightops
starting_level: 3
will: 60
salary:
  starting: 600
  increase: 200
  lv1: 300
  max: 2000
medical_deposit: standard
haggling: normal
executable: true
---

# Мануэль — Мануэль

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Мануэль | Manuel |
| Nick | Мануэль | Manuel |
| AllCapsNick | МАНУЭЛЬ | MANUEL |
| Title | Муж Фатимы | Fatima's Husband |
| Email | Manuel@arulco.reb | Manuel@arulco.reb |
| snype_nick | manuel | manuel |

## Bio

**RU:** Urban Brawl / Night Ops. Муж Фатимы, отец Пако. Внедрился в армию Арулько по просьбе Мигеля, был раскрыт и бежал в лес. Отряд встречает его блуждающим в лесах Тракона. Статы 70+, Dexterity 91. Одиночка, привыкший полагаться только на себя после провала операции.

**EN:** Urban Brawl / Night Ops. Husband of Fatima, father of Paco. Went undercover in the Arulco army at Miguel's request, was exposed, and fled into the forest. The squad finds him wandering the Tracona woods. Stats 70+, 91 Dexterity. A loner who's learned to rely only on himself since the operation fell apart.

## Stats

| Stat | Value |
| --- | --- |
| Health | 72 |
| Agility | 80 |
| Dexterity | 91 |
| Strength | 70 |
| Wisdom | 65 |
| Will | 60 |
| Leadership | 30 |
| Marksmanship | 70 |
| Mechanical | 30 |
| Explosives | 25 |
| Medical | 25 |
| MaxHitPoints | 72 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Manuel`
- `Stealthy`
- `Loner`
- `Flanker`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Manuel` |
| type | passive |
| DisplayName RU/EN | Под прикрытием / Undercover |
| Description RU/EN | Опыт разведки под прикрытием даёт бонус к скрытности вблизи вражеских патрулей / Undercover experience grants a stealth bonus near enemy patrols |
| Mechanics | +15% to Manuel's stealth detection-avoidance chance while within 2 tiles of an enemy unit that has not yet spotted him, reflecting his training at slipping past patrols undetected inside the Arulco army. |

## Personality

- Quirks: Loner (StartingPerk)
- Likes: `Jazz_Miguel` (already generated — Mitigation/ExtraPartingWords wiring live immediately)
- Dislikes: —
- National hates: —
- Refusal / Haggle notes: standard Locals money/death-toll refusals only; mitigation if Miguel hired (references the operation that got Manuel exposed)

## Hire

- Access: Locals — chance encounter in the Tracona forest sector once the player has scouted it; Manuel joins as a wandering local, no formal quest gate
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Manuel` → `JAZZ_Manuel50/35/25/20`
- *50: `JazzArmor_LeatherJacketBrn`, `SKS`, `JAZZ_AMMO_762x39_FMJ`×30 (Double), `Lockpick`
- *35: `JazzArmor_LeatherJacketBrn`, `SKS`, `JAZZ_AMMO_762x39_FMJ`×20 (Double)
- *25: `JazzArmor_LeatherPants`, `SKS`, `JAZZ_AMMO_762x39_FMJ`×20 (Double)
- *20: `JazzArmor_LeatherPants`, `SKS`, `JAZZ_AMMO_762x39_FMJ`×10 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](manuel.ja2-face.gif)

Файл: `manuel.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `manuel.ja2-face.gif` (same face identity). Lean Arulco scout ~30, tired eyes, binoculars and forest camo — NO gun. Cautious expression.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Binoculars, forest camo wrap, water skin, stealth cloth

## Phrases — AIM chat

### Offline
- RU: Мануэль... сейчас нет связи. Позже.
- EN: Manuel... no signal right now. Later.

### GreetingAndOffer
- RU: Это Мануэль. Слушаю.
- EN: This is Manuel. I'm listening.

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Тише. Мануэль слушает лес.
- EN: Quiet. Manuel's listening to the forest.

### PartingWords
- RU: Иду с вами. Фатима поймёт.
- EN: I'm coming with you. Fatima will understand.

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь. Лес подождёт.
- EN: I'm staying. The forest can wait.

### Refusals
- Death toll RU: Слишком много смертей. Мануэль уже видел, чем это кончается.
- Death toll EN: Too many deaths. Manuel's already seen how that ends.
- Money RU: Мало денег. У Мануэля семья — Фатима и Пако.
- Money EN: Not enough money. Manuel has a family — Fatima and Paco.

### Mitigations
- Miguel hired RU: Мигель уже здесь? Тогда ладно — он мне ещё должен объяснение.
- Miguel hired EN: Miguel's already here? Fine then — he still owes me an explanation.

### ExtraPartingWords
- RU: Если встретите Мигеля — скажите, Мануэль его не забыл.
- EN: If you run into Miguel — tell him Manuel hasn't forgotten.

## Phrases — VoiceResponse

- `voice_source: nightops` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Мануэль готов.» / «Manuel's ready.»
  - AimAttack (1): «Цель вижу.» / «I see the target.»
  - AimAttack (2): «Тихо и точно.» / «Quiet and precise.»
  - OpponentKilled: «Готово.» / «Done.»
  - DeathGeneral: «Фатима... прости...» / «Fatima... forgive me...»
  - Downed: «Ранен, но не сдамся.» / «Hit, but not giving up.»
  - CombatStartDetected: «Кто-то рядом. Осторожно.» / «Someone's near. Careful.»
  - LevelUp: «Учусь на своих ошибках.» / «Learning from my mistakes.»
  - AmmoLow: «Патроны на исходе.» / «Running low on ammo.»
  - Idle: «Мануэль ждёт в тени.» / «Manuel waits in the shadows.»
  - Praises (Miguel present): «С Мигелем спокойнее — несмотря ни на что.» / «It's calmer with Miguel around — despite everything.»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Manuel |
| VoiceResponseId | Jazz_Manuel |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Manuel.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Manuel_Big.png |
| CustomEquipGear | TryEquip Handheld A Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ub |

## Open blockers

- none
