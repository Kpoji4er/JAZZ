# R.I.S. battle-report editorial slot map

Canonical RU/EN copy: `docs/tools/_ris_copy_bank.py`. Existing AAR localization
IDs are the contiguous range `890000000011097…11156` (60 strings). The
additional approved strings use `890000000011341…11346`.

Editorial review completed 7 August 2026. The approved source copy is projected
to Lua and both runtime CSV tables by `_apply_ris_editorial.py`; live JA3
acceptance remains tracked separately in `JAZZ-UI-RIS-002`.

## Assembly order

1. Deterministic headline: outcome × intensity, one of 3 parallel variants.
2. Localized sector and optional point of interest.
3. Localized assignment context.
4. Weather observation.
5. Intensity assessment.
6. Approximate cumulative strength observed across all phases.
7. Outcome reading, with ambush and assignment-specific overrides.
8. Neutral numeric casualty line.
9. Auto-resolve limitation when applicable.
10. One line per named opponent.
11. Closing assessment.

Facts come before interpretation. Every interpretive line keeps the degree of
certainty supported by the snapshot. Headlines distinguish outcome and
intensity without tabloid language, jokes, or claims that the whole sector was
cleared.

## Headline banks

Each row contains exactly 3 semantically parallel variants. Selection remains
deterministic; the variant changes phrasing, never outcome or severity.

| Outcome | Intensity | Localization IDs | Editorial meaning |
| --- | --- | --- | --- |
| win | low | `11097…11099` | Favorable result after brief or limited resistance |
| win | mid | `11100…11102` | Favorable result after sustained fighting |
| win | high | `11103…11105` | Favorable result with heavy losses or severe fighting |
| loss | low | `11106…11108` | Adverse result after brief resistance, limited losses |
| loss | mid | `11109…11111` | Ground lost after sustained pressure |
| loss | high | `11112…11114` | Adverse result at heavy cost |
| retreat | low | `11115…11117` | Early or orderly disengagement with limited losses |
| retreat | mid | `11118…11120` | Withdrawal after sustained pressure |
| retreat | high | `11121…11123` | Costly withdrawal under severe fire |

## Existing paragraph slots

| Slot | Key | Localization ID | Selection and claim boundary |
| --- | --- | ---: | --- |
| Weather | `clear` | `11124` | Final report sampled clear conditions and good visibility |
| Weather | `rain` | `11125` | Final report sampled rain; no duration claim |
| Weather | `night` | `11126` | Darkness limited visibility; also covers underground maps |
| Weather | `fog` | `11127` | Final report sampled fog and reduced visibility |
| Weather | `heat` | `11128` | Final report sampled extreme heat; no invented consequence |
| Weather | `dust` | `11129` | Final report sampled dust and reduced visibility |
| Weather | `default` | `11130` | Final report identified no notable weather condition |
| Intensity | `low` | `11131` | Brief exchange, probably little attention outside the area |
| Intensity | `mid` | `11132` | Sustained fighting likely to draw wider attention |
| Intensity | `high` | `11133` | Scale difficult for hostile commanders to ignore |
| Forces | `forces` | `11134` | Approximate cumulative participants via `<player>` / `<enemy>` |
| Sector | `line` | `11135` | Localized `<sector>` only |
| Sector | `poi` | `11136` | Localized `<sector>` plus `<poi>` |
| Assignment | `one` | `11137` | `<quest>` plus confirmed `<note>` |
| Assignment | `one_nonote` | `11138` | Confirmed link to `<quest>` |
| Assignment | `many` | `11139` | Localized list `<quests>` |
| Assignment | `active` | `11140` | Retained localization slot; new snapshots do not infer a link from the globally active quest |
| Assignment | `none` | `11141` | No active assignment tied to the area; no inferred motive |
| Outcome | `win` | `11142` | Engagement ended in the team's favor; no sector-clear claim |
| Outcome | `loss` | `11143` | Engagement ended in the hostile force's favor |
| Outcome | `retreat` | `11144` | Team broke contact and withdrew |
| Outcome | `ambush` | `11145` | Opening pattern is consistent with an ambush |
| Outcome | `quest_win` | `11146` | Favorable result may support assignment work; no completion claim |
| Outcome | `quest_loss` | `11147` | Adverse result may complicate later work |
| Outcome | `quest_retreat` | `11148` | Withdrawal from assignment-linked area |
| Losses | `losses` | `11149` | `<pkia>`, `<pwia>`, `<ekia>`, `<ewia>` with neutral numeric grammar |
| Named opponent | `killed` | `11150` | Confirmed death of `<name>` |
| Named opponent | `wounded` | `11151` | Confirmed wound; later condition unknown |
| Named opponent | `escaped` | `11152` | `<name>` withdrew from the engagement; future contact possible |
| Named opponent | `threat` | `11153` | `<name>` remained combat-capable |
| Closing | `quiet` | `11154` | Limited scale unlikely to alter activity by itself |
| Closing | `noise` | `11155` | Sustained fighting may draw closer hostile attention |
| Closing | `disaster` | `11156` | Heavy losses may draw hostile command attention beyond the area |

## Additional approved slots

| Purpose | Localization ID | Runtime use |
| --- | ---: | --- |
| Auto-resolve limitation | `11341` | Appended for remote reports |
| Legacy AAR fallback title | `11342` | Fallback when no preserved outcome can be reconstructed |
| Legacy AAR fallback body | `11343` | Localized partial-record notice; preserved facts follow when available |
| Objective achieved with living hostiles | `11344` | Overrides generic win/quest-win when confirmed hostiles remain |
| Legacy unidentified fighter | `11345` | Sighting fallback when no stable type/title can be recovered |
| Legacy unidentified opponent | `11346` | Obituary fallback when no stable NPC/name can be recovered |

The `11344` line has precedence over `win` and `quest_win`: it records that the
immediate objective was achieved while explicitly preserving the continuing
hostile presence. It must not be followed by a sentence claiming that the
sector is clear.

## Placeholder and grammar constraints

- Allowed in existing AAR: `<player>`, `<enemy>`, `<sector>`, `<poi>`,
  `<quest>`, `<quests>`, `<note>`, `<pkia>`, `<pwia>`, `<ekia>`, `<ewia>`,
  `<name>`.
- Legacy fallback adds no new placeholder beyond `<sector>`.
- RU casualty grammar remains numeric and neutral:
  `погибших: <pkia>, раненых: <pwia>`; no runtime declension is required.
- Named-opponent RU lines use impersonal constructions and do not infer gender
  from `<name>`.
- Sector, POI, assignment names, and character names must arrive localized;
  raw quest, unit, session, or sector IDs are not report prose.
- Auto-resolve wording describes limited evidence in-world and never mentions
  a button, screen, simulation mode, or hidden calculation.
