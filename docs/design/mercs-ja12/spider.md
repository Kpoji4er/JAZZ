---
status: ready
priority: high
origin: ja2
unit_id: Jazz_Spider
portrait_id: Spider
affiliation: AIM
role: Doctor
tier: Elite
specialization: Doctor
gender: Female
nationality: USA
voice_source: ja2
starting_level: 4
will: 47
salary:
  starting: 0
  increase: 0
  lv1: 400
  max: 4300
medical_deposit: large
haggling: none
executable: true
---

# Паук — Доктор Донна «Паук» Хьюстон

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Доктор Донна «Паук» Хьюстон | Doctor Donna "Spider" Houston |
| Nick | Паук | Spider |
| AllCapsNick | ПАУК | SPIDER |
| Title | Алмазная Донна полевой хирургии. | Diamond Donna of field surgery. |
| Email | HoustonMD@aim.com | HoustonMD@aim.com |
| snype_nick | HoustonMD | HoustonMD |

## Bio

**RU:** as-shipped `Jazz_Spider.lua` — полевой хирург, экспериментальные препараты, позывной от Статика, скрытность/ночное зрение.

**EN:** CSV Bio.

## Stats

| Stat | Value |
| --- | --- |
| Health | 81 |
| Agility | 76 |
| Dexterity | 56 |
| Strength | 68 |
| Wisdom | 90 |
| Will | 47 |
| Leadership | 16 |
| Marksmanship | 70 |
| Mechanical | 0 |
| Explosives | 0 |
| Medical | 94 |
| MaxHitPoints | 79 |
| StartingLevel | (default AIM doctor tier; confirm editor) |

## Perks

### StartingPerks

- `Jazz_Perk_Spider`
- `NightOps`
- `Stealthy`

### Named perk

| Field | Value |
| --- | --- |
| id | `Jazz_Perk_Spider` |
| type | passive |
| DisplayName RU/EN | Полевая хирургия / Field Surgery |
| Description RU/EN | Удваивает значение навыка медицины при лечении на глобальной карте |
| Mechanics | Satellite medical skill ×2 (`System_SectorOperations.lua`) |

## Personality

- Quirks: FearInsects (sheet)
- Likes: Vicki, Raven
- Dislikes: Buns
- Refusal: Buns hired; money; death toll 2+
- Mitigation: Vicki / Raven hired

## Hire

- Access: AIM
- MedicalDeposit: large

## Inventory

- `Loot_JAZZ_Spider` → `JAZZ_Spider50/35/25/10`
- *50: `ColtPeacemaker`, `JAZZ_AMMO_44CAL_FMJ`×24, `Meds`×50, `FirstAidKit`, FlakM69 unless VeryHard

## JA2 face reference

Лицо в портрете должно быть **похоже на этот JA2-референс** (сохранить возраст, этничность, причёску, ключевые черты):

![JA2 face](spider.ja2-face.gif)

Файл: `spider.ja2-face.gif`

## Portrait prompt

**Эталон class kit:** медицинские принадлежности развешаны + шеврон медика.

**CHARACTER_DESCRIPTION:** Match JA2 face reference `spider.ja2-face.gif` (same face identity). Young female field surgeon, elegant but practical, dark hair, white/olive medic vest with hanging med pouches, bandages, trauma shears, clear medic cross chevron on shoulder — NO firearm (Peacemaker only in inventory, not portrait). Calm professional warmth.

**Refs:** existing `Spider.png` / `Spider_Big.png`  
**Class kit:** med pouches, shears, bandage rolls, medic chevron

## Phrases — AIM chat

As-shipped UnitData (Offline clinic message, Greeting, Idle, Parting, Rehire, refusals/mitigations).

## Phrases — VoiceResponse

Full as-shipped `Jazz_Spider`.

## Wiring

| Field | Value |
| --- | --- |
| Appearance | Spider |
| VoiceResponseId | Jazz_Spider |
| pollyvoice | Amy |
| Portrait | Mod/Dv3mFVN/MercPortraits/Spider.png |
| Sources | `Jazz_Spider.lua`, `Jazz_Perk_Spider.lua`, `Loot_JAZZ_Spider` |

## Open blockers

- none
