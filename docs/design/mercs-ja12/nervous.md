---
status: ready
priority: medium
origin: ja2
unit_id: Jazz_Nervous
portrait_id: Nervous
affiliation: MERC
role: Autorifleman
tier: Regular
specialization: Autoriflemen
gender: Male
nationality: USA
voice_source: ja2
starting_level: 3
will: 30
salary:
  starting: 700
  increase: 200
  lv1: 350
  max: 2200
medical_deposit: standard
haggling: normal
executable: true
---

# Нервный — Фрэнки «Нервный» Гордон

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Фрэнки «Нервный» Гордон | Frankie "Nervous" Gordon |
| Nick | Нервный | Nervous |
| AllCapsNick | НЕРВНЫЙ | NERVOUS |
| Title | Суперочередь | The Super Burst |
| Email | Nervous@merc.com | Nervous@merc.com |
| snype_nick | twitchy | twitchy |

## Bio

**RU:** Статы 60–70, Wisdom 58, Marksmanship 48, Explosives 31. Псих на постоянном взводе, стреляет длинными очередями и не умеет по-другому. Дружит с Бритвой и Рикошетом (родственные безумцы); терпеть не может Биффа за трусость.

**EN:** Stats in the 60-70 range, 58 Wisdom, 48 Marksmanship, 31 Explosives. A psycho who's permanently wound up and only knows how to shoot in long bursts. Friends with Blade and Ricochet (fellow lunatics); can't stand Biff's cowardice.

## Stats

| Stat | Value |
| --- | --- |
| Health | 65 |
| Agility | 70 |
| Dexterity | 60 |
| Strength | 60 |
| Wisdom | 58 |
| Will | 30 |
| Leadership | 15 |
| Marksmanship | 48 |
| Mechanical | 20 |
| Explosives | 31 |
| Medical | 10 |
| MaxHitPoints | 65 |
| StartingLevel | 3 |

## Perks

### StartingPerks

- `Jazz_Perk_Nervous`
- `Psycho`
- `AutoWeapons`
- `Flanker`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Nervous` |
| type | passive |
| DisplayName RU/EN | Суперочередь / Super Burst |
| Description RU/EN | Автоматная очередь Нервного длиннее и дешевле по ОД / Nervous's autofire bursts are longer and cheaper in AP |
| Mechanics | Auto attacks fire 2 extra bullets per burst compared to the base weapon's autofire count, and cost −20% AP. Accuracy penalty for the extra bullets follows the normal autofire falloff curve — no free accuracy. |

## Personality

- Quirks: Psycho (StartingPerk)
- Likes: `Jazz_Blade` (high wave — Mitigation/ExtraPartingWords live once Blade is generated), `Jazz_Ricochet` (planned merc — wiring activates once ready)
- Dislikes: `Jazz_Biff` (medium wave — Refusal wiring live once both are generated together)
- National hates: —
- Refusal / Haggle notes: refuses if Biff hired; standard MERC money/death-toll refusals; mitigation if Blade or Ricochet hired

## Hire

- Access: MERC roster
- MedicalDeposit: standard; Haggling: normal; DaysUntilOnline: 0

## Inventory

- Equipment loot id: `Loot_JAZZ_Nervous` → `JAZZ_Nervous50/35/25/20`
- *50: `JazzArmor_LeatherArmor`, `UZI`, `JAZZ_AMMO_9x19_FMJ`×80 (Double), `SmokeGrenade`×1
- *35: `JazzArmor_LeatherArmor`, `MP5A4`, `JAZZ_AMMO_9x19_FMJ`×60 (Double)
- *25: `JazzArmor_LeatherJacketBrn`, `MPL`, `JAZZ_AMMO_9x19_FMJ`×40 (Double)
- *20: `JazzArmor_LeatherJacketBrn`, `UZI`, `JAZZ_AMMO_9x19_FMJ`×40 (Double)

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](nervous.ja2-face.gif)

Файл: `nervous.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder (holstered pistol only as last resort). Role via **class kit**.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `nervous.ja2-face.gif` (same face identity). Twitchy, thin American ~28, wild eyes, ammo bandolier and hearing protection around neck — NO SMG in hands. Nervous, jittery energy.

**Preferred refs:** `MercPortraits/References/` matching gender/role

**Class kit:** Ammo bandolier, ear protection, MERC patch, fingerless gloves

## Phrases — AIM chat

### Offline
- RU: Нервный... занят... пиши, перезвоню, может.
- EN: Nervous... busy... leave a message, maybe I'll call back.

### GreetingAndOffer
- RU: Ч-чё надо? Стрелять будем?!
- EN: W-what do you need? We shooting something?!

### ConversationRestart
- RU: Связь прервалась. Вернёмся к делу.
- EN: Line dropped. Let's get back to it.

### IdleLine
- RU: Где враги, где враги, где враги...
- EN: Where's the enemy, where's the enemy...

### PartingWords
- RU: Уже бегу, уже бегу! Патроны есть, всё нормально!
- EN: I'm coming, I'm coming! Got ammo, it's fine!

### RehireIntro
- RU: Контракт заканчивается. Продлеваем?
- EN: Contract's ending. Extending?

### RehireOutro
- RU: Остаюсь! Ещё патроны не кончились!
- EN: I'm staying! Still got ammo left!

### Refusals
- Biff hired RU: Пока трусливый Бифф в отряде — нет! Он меня ещё больше нервирует!
- Biff hired EN: Not while cowardly Biff's on the team! He makes me even more jumpy!
- Death toll RU: Слишком много наших полегло! Я и так на нервах!
- Death toll EN: Too many of ours went down! I'm already on edge!

### Mitigations
- Blade/Ricochet hired RU: О, Бритва или Рикошет уже тут? Тогда ладно, веселее будет!
- Blade/Ricochet hired EN: Oh, Blade or Ricochet's already in? Then fine, this'll be fun!

### ExtraPartingWords
- RU: Возьмите ещё Рикошета — вдвоём мы очередями всё разнесём!
- EN: Grab Ricochet too — together we'll shred everything with bursts!

## Phrases — VoiceResponse

- `voice_source: ja2` — reuse legacy VO where available; RU/EN subtitle drafts for minimum slots:
  - Selection: «Н-нервный на месте!» / «N-Nervous is here!»
  - AimAttack (1): «Очередь! Очередь!» / «Burst! Burst!»
  - AimAttack (2): «Не могу остановиться!» / «Can't stop shooting!»
  - OpponentKilled: «Есть! Есть! ЕСТЬ!» / «Got him! Got him! GOT HIM!»
  - DeathGeneral: «Я знал, я знал...» / «I knew it, I knew it...»
  - Downed: «МЕНЯ ЗАДЕЛО! МЕНЯ ЗАДЕЛО!» / «I'M HIT! I'M HIT!»
  - CombatStartDetected: «Они здесь! ОНИ ЗДЕСЬ!» / «They're here! THEY'RE HERE!»
  - LevelUp: «Ха! Ещё быстрее теперь!» / «Ha! Even faster now!»
  - NoAmmo: «Патроны! ПАТРОНЫ КОНЧИЛИСЬ!» / «Ammo! I'M OUT OF AMMO!»
  - Idle: «Где враги где враги где враги» / «Where's the enemy where's the enemy»
  - MockDislike (Biff): «Бифф бы уже обделался.» / «Biff would've soiled himself by now.»
  - Praises (Blade/Ricochet present): «С этими психами веселее!» / «It's more fun with these lunatics around!»

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Nervous |
| VoiceResponseId | Jazz_Nervous |
| pollyvoice | Matthew |
| Portrait | Mod/Dv3mFVN/MercPortraits/Nervous.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Nervous_Big.png |
| CustomEquipGear | TryEquip Handheld A/B Firearm |
| FallbackMissingVR | Ice |
| Sources | AIM sheet «Наемники из JA1/2»; origin=ja2 |

## Open blockers

- none
