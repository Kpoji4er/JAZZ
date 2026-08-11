# JA3 / JAZZ status effect icons — style & prompts

Skill: `.agents/skills/create-jazz-status-icons/SKILL.md` (`$create-jazz-status-icons`).  
Style-референсы: **только** PNG в этой папке + runtime JAZZ в `Icons/StatusEffects/*.png`.  
Источник wiring: `<JA3_ROOT>/ModTools/Src/Lua/CharacterEffectCompositeDef/*.generated.lua`  
поле `type` (ClassDef): `System` (default) · `Buff` · `Debuff` · `AttackBased`.

Цвет **запечён в PNG** (движок не перекрашивает иконку по `type`). Художники ванили следуют polarity:

| Семья | Hex (доминанта) | Когда брать в промпт |
| --- | --- | --- |
| **Buff sand** | `#B8B880` … `#C0B880` | `type=Buff`, или System с позитивным смыслом (Heroic, Stimmed, Stabilized…) |
| **Debuff red** | `#D83838` … `#E04040` | `type=Debuff`, или System с негативным смыслом (Panicked, Berserk, Surprised…) |
| **Pain dark-red** | `#A02020` / `#981818` | травмы/подавление: `arms_pain`, `legs_pain`, `suppressed` |
| **Stealth cream** | `#E0D8C8` | только `Hidden` |
| **Medical cyan** | `#50A0C8` | только `BandageInCombat` / `treating` |

Правило для нового JAZZ-эффекта:

1. Задать `type` в CharacterEffect (`Buff` / `Debuff` / `System`).
2. Выбрать семью цвета по таблице выше (не по вкусу).
3. В промпт: `COLOR_HEX` + 2–3 рефа той же семьи (колонка «Реф»).
4. Severity-серии (как suppression) — исключение: один глиф, градиент своих hex.

## Canvas

| Свойство | Значение |
| --- | --- |
| Размер | **40×40** RGBA |
| Фон | прозрачный (`A=0`), не чёрная заливка кадра |
| Стиль | flat 2D HUD glyph, толстый силуэт, soft AA, без текста/рамки/фото |

## Vanilla: icon → CharacterEffect

`Icon` path = `UI/Hud/Status effects/<file>` (без расширения). Несколько Id на один файл = shared glyph.

| PNG | Hex | `type` | CharacterEffect Id (DisplayName) |
| --- | --- | --- | --- |
| `arms_pain` | `#A02020` | Debuff | `Inaccurate` (Inaccurate) |
| `bleeding` | `#E03838` | Debuff | `Bleeding` |
| `bleedingout` | `#D83838` | System | `BleedingOut`, `Downed` (оба «Downed») |
| `blinded` | `#D83838` | Debuff | `Blinded` |
| `bloodthirst` | `#B8B880` | System | `Bloodthirst` |
| `burning` | `#D83838` | Debuff | `Burning` |
| `choking` | `#D83838` | Debuff | `Choking` |
| `darkness` | `#C0B880` | System | `Darkness` (In Darkness) |
| `drunk` | `#C0B880` | System | `Drunk` (Inebriated), `Unwell` |
| `encumbered` | `#E03838` | Debuff | `Conscience_Guilty` (Guilty), `Conscience_Sinful` (Remorseful) |
| `exhausted` | `#E03838` | Debuff | `Exhausted` |
| `exposed` | `#E03838` | Debuff | `Exposed` |
| `flanked` | `#D83838` | Debuff | `Flanked` |
| `focused` | `#B8B880` | Buff | `Focused` |
| `hero` | `#B8B880` | System | `Heroic` |
| `hidden` | `#E0D8C8` | System | `Hidden` |
| `inspired` | `#C0B880` | Buff | `Inspired`, `AI_AdditionalAP` |
| `legs_pain` | `#A02020` | Debuff | `Slowed` |
| `marked` | `#E04040` | Debuff | `Marked` |
| `mobility` | `#B8B880` | Buff | `Mobile`, `FreeMove` (Free Move) |
| `numbness` | `#D83838` | Debuff | `Numbness` |
| `panic` | `#E03838` | System | `Panicked` |
| `protected` | `#B8B880` | Buff | `Protected` (Taking cover) |
| `rage` | `#E03838` | System | `Berserk` |
| `revealed` | `#D83838` | System | `Revealed` |
| `sidney_perk_buff` | `#B8B880` | System | `SidneyPerkBuff` (Smug) |
| `stabilized` | `#C0B880` | System | `Stabilized`, `ZombiePerk` (Infected) |
| `stimmed` | `#B8B880` | System | `Stimmed`, `DieselPerk` (Enhanced) |
| `suppressed` | `#981818` | Debuff | `Suppressed` |
| `surprised` | `#E03838` | System | `Surprised` |
| `suspicious` | `#C0B880` | System | `Suspicious` |
| `tired` | `#E03838` | Debuff | `Tired` |
| `treating` | `#50A0C8` | System | `BandageInCombat` (Treating) |
| `unaware` | `#E03838` | System | `Unaware` |
| `unconscious` | `#D83838` | System | `Unconscious`, `Distracted` |
| `vengeance_target` | `#D83838` | System | `VengeanceTarget` |
| `well_rested` | `#B8B880` | Buff | `WellRested`, `Conscience_Proud`, `Conscience_Righteous`, `BonecrusherEnraged` (Enraged) |
| `wounded` | `#E03838` | Debuff | `Wounded` |

### PNG без wire в CharacterEffect (Src)

В пакете UI есть, на `CharacterEffect.Icon` в ModTools Src не ссылаются — для промптов только как shape/color sample, не как Id:

| PNG | Hex | Заметка |
| --- | --- | --- |
| `battle_focus` | `#B8B880` | sand leftover |
| `concentrate` | `#B8B880` | sand leftover |
| `double_barrel` | `#C0B880` | sand leftover (CombatAction double barrel — другой path `UI/Icons/Hud/…`) |
| `mobile_shot` | `#C0B880` | sand leftover |
| `suppressive_barrage` | `#B8B080` | sand leftover |

## JAZZ runtime (`Icons/StatusEffects/`)

| PNG | Hex | Effect Id | Смысл / цвет |
| --- | --- | --- | --- |
| `suppressionLight.png` | `#C3FF00` | `suppressionLight` | severity ladder (не ваниль) |
| `suppressionMedium.png` | `#FAFF00` | `suppressionMedium` | |
| `suppressionHeavy.png` | `#FF0000` | `suppressionHeavy` | |
| `suppressionHeavy2.png` | `#990300` | `suppressionHeavy2` | |
| `suppressionPinned.png` | `#000000` | `suppressionPinned` | |
| `Jazz_OfficerAura.png` | olive + amber | `Jazz_Perk_OfficerAura` | source: badge, chevron + arcs |
| `Jazz_OfficerAuraInfluence.png` | steel + weak amber | `Jazz_Perk_OfficerAuraInfluence` | receiver: ring + mini soldier |
| `MarkedTraccers.png` | — | `MarkedTraccers` (+ shared `DamageReduction`) | помечен трассерами |
| `Bleeding.png` | `#E03838` | `Bleeding` | MED-001 light bleed: 1 drop |
| `BleedingMedium.png` | `#C82828` | `BleedingMedium` | MED-001 moderate: 2 drops |
| `BleedingHeavy.png` | `#A02020` | `BleedingHeavy` | MED-001 heavy: cascade + spray |
| `BloodLoss50.png` | `#E87878` | `BloodLoss50` | MED-002 Weakness: torso + 3↓ chevrons (not bleed drop) |
| `BloodLoss40.png` | `#E06060` | `BloodLoss40` | same glyph, darker |
| `BloodLoss30.png` | `#D84848` | `BloodLoss30` | |
| `BloodLoss20.png` | `#D03030` | `BloodLoss20` | |
| `BloodLoss10.png` | `#C02020` | `BloodLoss10` | |
| `BloodLoss5.png` | `#A01818` | `BloodLoss5` | |
| `BloodLoss1.png` | `#781010` | `BloodLoss1` | darkest critical |
| `Pain.png` | `#A02020` | `Pain` | MED-001 ache burst + zigzags (not bleed drop) |
| `Analgesia.png` | `#B8B880` | `Analgesia` | MED-001 buff: autoinjector + calm waves |
| `Concussion.png` | `#E03838` | `Concussion` | blast daze: head profile + swirl + impact rings (not TraumaHead cracked skull) |

Officer pair (final art brief):

- **Aura (source):** round JA3 badge (dark rim, muted kant); center chevron/hex command mark; short radio arcs outward; muted olive-khaki + cold amber on chevron; silhouette reads «chevron + rings».
- **Influence (receiver):** same badge language but secondary — weaker/smaller chevron; dominant steel ring around mini soldier (or ring alone); steel-gray + quieter amber; must not clone the commander glyph 1:1.

Ванильный якорь для suppression-смысла: `suppressed` (`Suppressed` / Debuff / `#981818`). JAZZ ladder — отдельная серия, не перекраска ванили.

Path: `Mod/e6L4ECj/Icons/StatusEffects/<file>.png`.

## Правила глифа

1. Один символ = одно состояние; толстый силуэт ~30–70% кадра.
2. Монохром семьи + опциональный тёмный inset (`#242424`), как у buff-иконок.
3. Не копировать чужой vanilla Id 1:1 без intentional override.
4. Shared icon в ванили (несколько Id → один PNG) — норма; новый JAZZ-эффект лучше со своим файлом.

## Промпт GenerateImage

Подставить `SYMBOL`, `COLOR_HEX`, `EFFECT_ID`, `EFFECT_TYPE`. Референсы — 2–3 PNG из той же цветовой семьи.

```text
Create ONE Jagged Alliance 3 HUD status-effect icon matching the reference images EXACTLY.

This icon is for CharacterEffect EFFECT_ID (type=EFFECT_TYPE).
Use the same color family as the attached references: solid fill COLOR_HEX.

Canvas: 40x40, square. Solid black draft background (keyed to alpha later).
Style: flat 2D minimalist tactical HUD glyph, thick silhouette, soft AA edges,
no gradients, no bevels, no drop shadows, no textures, no text, no numbers, no frames.

Subject centered, readable at tiny size. Monochrome COLOR_HEX only
(optional very dark inset cuts like vanilla buff icons).

SYMBOL: SYMBOL

Match line weight and simplicity of the attached JA3 status-effect references.
```

Severity-серия (suppression):

```text
Same glyph as the attached JAZZ suppression references: three horizontal bullets
stacked vertically, tips pointing right, short motion dashes behind each base.
Change ONLY the solid fill color to COLOR_HEX. Do not redesign the silhouette.
```

## Post-process DoD

```text
- [ ] 40×40 RGBA; углы A=0
- [ ] Цвет семьи совпадает с type/polarity (или осознанный severity exception)
- [ ] Рефы в промпте из той же семьи, что целевой hex
- [ ] Runtime: Icons/StatusEffects/<Id>.png + Icon path в CharacterEffect/items.lua
- [ ] Ванильные PNG в этой папке не править
```
