---
status: ready
priority: high
origin: ja2
unit_id: Jazz_Lynx
portrait_id: Lynx
affiliation: AIM
role: Sniper
tier: Elite
specialization: Marksmen
gender: Male
nationality: USA
voice_source: ja2
starting_level: 4
will: 76
salary:
  starting: 2650
  increase: 0
  lv1: 1400
  max: 6200
medical_deposit: large
haggling: none
executable: true
---

# Рысь — Руди Робертс «Рысь»

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Руди Робертс «Рысь» | Rudy Roberts "Lynx" |
| Nick | Рысь | Lynx |
| AllCapsNick | РЫСЬ | LYNX |
| Title | Известен не за красивые глаза | Not famous for his pretty eyes |
| Email | Lynx@aim.com | Lynx@aim.com |
| snype_nick | Iseeyou | Iseeyou |

## Bio

**RU:** (as-shipped UnitData) `"У всех проблем одно начало - сидела женщина, скучала". Жизнь Руди Робертса до его работы в Организации была лишена каких-то потрясений...` — полный текст в `jazz-units/UnitData/Jazz_lynx.lua`.

**EN:** см. `jazz/English.csv` / localization id Bio.

## Stats

| Stat | Value |
| --- | --- |
| Health | 81 |
| Agility | 79 |
| Dexterity | 86 |
| Strength | 77 |
| Wisdom | 82 |
| Will | 76 |
| Leadership | 39 |
| Marksmanship | 99 |
| Mechanical | 29 |
| Explosives | 50 |
| Medical | 34 |
| MaxHitPoints | 94 |
| StartingLevel | 4 |

## Perks

### StartingPerks

- `AutoWeapons`
- `NightOps`
- `MrFixit`
- `Jazz_Perk_Lynx`
- `Pessimist`
- `Deadeye`
- `Killzone`
- `Counterfire`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Lynx` |
| type | passive |
| DisplayName RU/EN | Рысий взгляд / Lynx's Eye |
| Description RU/EN | Дальность видимости днем повышена, а штрафы за дальность - понижены |
| Mechanics | As-shipped CharacterEffect; day visibility bonus (see `docs/technical/systems/visibility-weather-appearance.md`) |

## Personality

- Quirks: Pessimist
- Likes: Ice
- Dislikes: Jazz_Buzz
- National hates: —
- Refusal / Haggle: refuses if Buzz hired; death-toll/money/combat rehire refusals; Ice mitigation 100%; recommends Ice in ExtraPartingWords

## Hire

- Access: AIM
- MedicalDeposit: large; Haggling: (default); DaysUntilOnline: 0

## Inventory

- Equipment: `Loot_JAZZ_Lynx` → `JAZZ_Lynx50/35/25/20`
- *50: `JazzArmor_LeatherJacketBrn`, `JazzArmor_SwatPads`, `HE_Grenade`, `SmokeGrenade`, `Knife_Sharpened`, `JAZZ_AMMO_556_EPR`×40, `Mini14` + `JAZZ_CombatScope_2x`

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](lynx.ja2-face.gif)

Файл: `lynx.ja2-face.gif`

## Portrait prompt

**Rules:** no weapons in hands/on shoulder. Class kit.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `lynx.ja2-face.gif` (same face identity). Male Caucasian sniper mid-30s, short dark hair, wary eyes, brown leather jacket, spotting-scope pouch and rangefinder on chest harness, ghillie scrap on shoulder — NO rifle. Calm professional.

**Preferred refs:** existing `MercPortraits/Lynx.png` / `Lynx_Big.png`; marksman refs in `References/`

**Class kit:** spotting pouch, rangefinder, ghillie scrap

## Phrases — AIM chat

As-shipped in UnitData (RU):

- Offline: «Это Руди Робертс. Меня прозвали Рысь...»
- GreetingAndOffer: «Рысь! Что случилось?»
- ConversationRestart: «Слушай, я ведь от времени моложе не делаюсь!»
- IdleLine: «Я не люблю обращаться за рекомендациями...»
- PartingWords: «Окей, я в твоем распоряжении.»
- RehireIntro / Outro: as in UnitData
- Refusals / Mitigations / ExtraPartingWords: as in UnitData (Buzz / Ice)

## Phrases — VoiceResponse

Full as-shipped set: `jazz-units/items.lua` `ModItemVoiceResponse Jazz_Lynx`. Do not regenerate.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Lynx |
| VoiceResponseId | Jazz_Lynx |
| pollyvoice | Russell |
| Portrait | Mod/Dv3mFVN/MercPortraits/Lynx.png |
| BigPortrait | Mod/Dv3mFVN/MercPortraits/Lynx_Big.png |
| Sources | `UnitData/Jazz_lynx.lua`, `CharacterEffect/Jazz_Perk_Lynx.lua`, loot `Loot_JAZZ_Lynx` |

## Open blockers

- none
