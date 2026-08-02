# Plan: voice ↔ subtitles ↔ merc (2026-08)

Evidence from `Downloads/ja2mercs (1)/ja2mercs` + shipped `jazz-units/voices`.

## Diagnosis (owner reports)

| Merc | Symptom | Root cause (static) | Fix |
| --- | --- | --- | --- |
| **Mike** | No VO | Never shipped: CSV `status=need_pack`, `speech_source=missing`; Selection opus **missing** (0/11). Pack folder `локался/074 mike` exists (074 + R_074). | Un-skip → `ja2mercs:локался/074 mike\|battle=R_074\|merge_speech` → remesh combat (+ chat if hire appears). |
| **Vince** | No / empty VO | Remeshed, but **NEW pack swapped bare↔R_**: `069_000`=15KB stub, `R_069_000`=44KB full (OLD was opposite). Ship preferred bare → tiny chirps. Chat cleared (no hire 081–120). | Prefer longer of bare/`R_*` (merge_speech); remesh Vince. |
| **Kulba** | Wrong VO | Bank **is** old 062 renamed to 164 (same sizes). Combat often **stub on 164_***, full on **R_164_*** (`000`: 5KB vs 66KB). Co-folder `118_*` present but **not** selected when pid=164. Feels “wrong/empty” = stubs. | `\|battle=R_164\|merge_speech` (or global longer-of-R); remesh; ignore 118. |
| **Biggens** | Wrong VO | Same pattern: NEW `168_*` = OLD `U_61_*` rename (hire OK). Full lines often on **R_168_*** (`000` 13KB vs 61KB). | `\|battle=R_168\|merge_speech`; remesh. |
| **Rothman** | OK | Clean single prefix `030_*`, no stub/`R_` trap. Control sample. | Leave alone. |

## Phase A — audio resolve (do first)

1. **Ship resolve:** for numeric stems, always pick **longer** of `pid` vs `R_pid` vs `D_pid` (same as Grom `merge_speech`, but default-on for ja2mercs). Named battle (ATTN/OK/HIT) stay on bare/battle pid (usually no R_ duplicate).
2. **Map updates** (`_ja2mercs_folder_map.py` + apply):
   - `mike`: remesh `локался/074 mike`, pid `074`, `battle=R_074`, `merge_speech`
   - `vince`: add `battle=R_069|merge_speech`
   - `kulba`: `battle=R_164|merge_speech` (still ignore 118)
   - `biggens`: `battle=R_168|merge_speech`
3. Remesh **only** mike, vince, kulba, biggens (dry-run sizes → apply). Spot-check Rothman unchanged.
4. Ear-check checklist: Selection, AimAttack, Greeting (if hire), 2–3 combat lines.

## Phase B — subtitles (txt → Jazz T() / loc)

Sources in pack (cp1251 / mixed):

- Per-merc `NNN_name.txt`: line index `i` ↔ stem `i` (blanks = missing stem). Confirmed Kulba: `[0]=Черти!` (=000), `[108]=…` (=greeting band).
- `схема реплик *.xlsx` already in `_voice-source/schemas/` — role of each stem (not character lines).

Pipeline (new tool, keep in `docs/tools/`):

1. `_import_ja2mercs_subtitle_bank.py`  
   - Read each `*.txt` (try utf-8 / cp1251 / utf-16).  
   - Emit `docs/design/mercs-ja12/_voice-source/subtitles/<slug>.csv`: `stem,ru_text,bytes_wav,has_audio`.
2. `_apply_ja12_subtitles.py` (careful, slot-scoped):  
   - Map Jazz VR slot → stem via `SLOT_WAV` / `AIM_CHAT_WAV` (first preferred stem with text).  
   - Update UnitData companion **and** `items.lua` `T(id, … "text")` RU string for that line.  
   - Sync `Russian.csv` + `English.csv` via `$manage-jazz-localization` (EN: keep existing Jazz EN if good; else mercedt/EN stub marked WIP — **do not** invent lore).  
   - **Never** overwrite Name/Nick/Bio from speech txt.  
   - Start scope: mercs with txt **and** shipped VO: kulba, biggens, gaston, horg, + WF AIM with txt; then SJ (benny/simon/grom/escimo). Mike/Vince: only if txt exists (Mike: none in pack → skip text or use RPC schema + mercedt later).
3. Validate: `_validate_items_quick.py` on `jazz-units`; loc auditor `needs Russian=0` / `needs English=0` for touched IDs.

## Phase C — docs / verify

- Update `VERIFY.md` ear-check rows for Mike/Vince/Kulba/Biggens.  
- Alignment CSV notes: R_ fuller-bank rule.  
- Owner ear-check before mass subtitle apply beyond ЦС+WF pilot.

## Out of scope / do not

- Spouke, workshop Merc_*.  
- Biff/Lynx/Buzz/Spider (no ja2mercs folder).  
- Blind Selection→chat fill.  
- Mixing 118 into Kulba.  
- Mass-rewriting all Jazz merc bios from speech txt.

## Status

| Phase | State |
| --- | --- |
| A1 longer(R_) resolve | **done** (numeric stems pick fullest bare/`R_`/`D_`) |
| A2 map mike/vince/kulba/biggens | **done** |
| A3 remesh 4 | **done** (Mike VR expanded 11→74; Vince/Kulba/Biggens AimAttack sizes up) |
| B1 import subtitle CSV | **done** (`_voice-source/subtitles/*.csv`, 16 banks) |
| B2/B3 apply subtitles | **done** for ЦС+WF+SJ with txt (stem index = line index; blanks keep alignment) |
| C docs / ear-check | **owner** — VERIFY Mike/Vince/Kulba/Biggens in-game |

Note: UB hire slots (`108` etc.) often contain campaign lines, not classic AIM greetings — subtitles match **audio**, not idealized hire copy.

## Order of work

```text
A1 resolve longer(R_)  →  A2 map mike/vince/kulba/biggens  →  A3 remesh 4
→ ear-check
→ B1 import subtitle CSV  →  B2 apply pilot (kulba+biggens+gaston)  →  B3 expand
→ C docs
```

## Acceptance

- Mike: Selection plays non-silent opus from 074/R_074.  
- Vince/Kulba/Biggens: AimAttack/Selection duration clearly > stub chirp; identity matches txt self-lines where present.  
- Rothman: bit-identical / unchanged.  
- Pilot subtitles: Greeting/Selection/AimAttack RU in-game matches pack txt for that stem.  
- Loc tables balanced for touched IDs.
