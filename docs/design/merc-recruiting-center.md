# M.E.R.C. — More Economic Recruiting Center

Design companion for [`JAZZ-UI-MERC-001`](../specs/active/JAZZ-UI-MERC-001.md). Normative acceptance lives in the spec; this page is the human-readable mirror for design/implement.

## Fantasy

| Market | Sells |
| --- | --- |
| **AIM** | Ready professionals (brand, perks, kit, voice) |
| **AME** | Local fighters — cheap growth market |
| **M.E.R.C.** | Named JA2-style contractors on Speck’s credit account — cheaper rival to AIM, not a clone |

Speck is **UI/mail persona only** (not hireable). Welcome mail: M.E.R.C. is open again **and** please find Biff (co-founder out of contact). JA3 lore-safe: AIM still exists; no Arulco/Deidranna campaign facts.

## PDA site

- Browser mode id: `merc`
- URL: `http://www.merc.com/`
- Org / Affiliation: `MERC`
- UI class: `PDAMERCBrowser` (subclass of `PDAAIMBrowser`) + XTemplate skin
- Hire card **Loadout**: Equipment / Backpack **with** Perks strip (AIM-parity `GetPerks` / `PDAPerk`; AME still hides Traits)
- Hire pipeline: vanilla chat / `HireMerc`; credit remap via `JAZZ_MERC_OnHired` after success
- Tab **locked** until Day-2 Speck welcome mail (`unlocked` / `welcome_sent`); then docked with AIM when unlocked

### Chrome (shipped targets)

- Mark: `Icons/PDA/MERC_Mark.png`
- Banner: `Icons/PDA/MERC_BannerPad.png`
- Backdrop: `Icons/PDA/MERC_PdaBackdrop.png`
- **Theme:** JA2 MERC — teal/cyan «дешёвый 90s-сайт», не ochre AME и не AIM blue-grey
- Concepts: `docs/design/_merc-logo/` (v2 JA2 teal)

## Roster v1

### Shelf-immediate (14) — Available after unlock

`Jazz_Flo`, `Jazz_Cougar`, `Jazz_Madman`, `Jazz_Blade`, `Jazz_Conrad`, `Jazz_Dynamo`, `Jazz_Gaston`, `Jazz_Nervous`, `Jazz_Ricochet`, `Jazz_Cord`, `Jazz_Hobbit`, `Jazz_Horg`, `Jazz_Meat`, `Jazz_Shank`

### World-gated — hidden until meet

| id | Notes |
| --- | --- |
| `Jazz_Biff` | Our Biff; RescueBiff / meet → Available or Hired |
| `Larry` / `Larry_Clean` | Vanilla F7 + Metaviron; either persona marks both |
| `Smiley` | Vanilla Smiley questline |

**Excluded:** `Flay`, `Pierre` (Locals); no second vanilla `Biff` hireable slot.

### Visibility

- Show: Available, Hired (My Team), Dead/MIA (grayed)
- Hide: world-gated until `JAZZ_MERC_MarkMet`
- AIM All: no Available MERC; Hired may appear in AIM My Team

Filters on site: **All**, **Available**, **My Team** (no AME category tabs).

## Credit account

`gv_JAZZ_MERC_Account`: `balance`, `paid_total`, `last_reminder_day`, `warning_stage`, `welcome_sent` / `welcome_read`, `unlocked`, `met`

| Rule | Behavior |
| --- | --- |
| Hire | Vanilla prepaid refunded; first day (`StartingSalary` / daily wage) → `balance`. Messenger `CanAffordMerc` always true for `Affiliation=MERC` (Offer works at $0 cash). Medical deposit waived on credit hire (`MedicalPaidWhenHired=0`) so end-of-contract deposit does not double-refund. |
| Daily | Each Hired `Affiliation=MERC` adds daily wage to `balance` |
| Pay Account | Spend player money → −`balance`, +`paid_total`; clears warning if paid off |
| Reminder | ~7 days with unpaid balance → `MERC_AccountReminder` |
| Quit | +3 days grace → `MERC_QuitWarning` + release hired MERC |
| AIM/AME | Prepaid paths untouched (`CanAffordMerc` base) |

## Mail

| Email id | Role |
| --- | --- |
| `MERC_Welcome` | Day 2 unlock + Biff ask (prose) |
| `MERC_AccountReminder` | Overdue balance |
| `MERC_QuitWarning` | Contractors walking |

Sender: Speck / M.E.R.C. Loc inline IDs: `890000000009903+` (avoid AME `6900`s).

**Save-compat:** `JAZZ_MERC_MigrateWelcomeFromSave` on `LoadGame` — if Welcome already in inbox, recover `welcome_sent`/`unlocked`; else if campaign day ≥ 2 and not yet sent, deliver Speck mail once (pre-MERC / mid-campaign saves). Day 1 new games still wait for Day 2.

## Code map

| File | Role |
| --- | --- |
| `Code/System_MERC_Filters.lua` | Roster tables, filters, listing |
| `Code/System_MERC_Account.lua` | GameVar, accrual, Pay, quit |
| `Code/System_MERC_Mail.lua` | Welcome / reminder / quit + MarkEmail chain |
| `Code/System_MERC_Browser.lua` | Tab, `PDAMERCBrowser`, wraps, init |
| `Code/System_MERC_World.lua` | `JAZZ_MERC_MarkMet` + meet hooks |
| `Code/System_MERC_Browser_Template.lua` | Editable XTemplate source → items via install script |

## Related

- Spec: [`JAZZ-UI-MERC-001`](../specs/active/JAZZ-UI-MERC-001.md)
- AME (separate market): [`ame-mercenary-exchange.md`](ame-mercenary-exchange.md)
- Biff design: [`mercs-ja12/biff.md`](mercs-ja12/biff.md)
