# JA2 / NightOps / UB voice sources

Mapping: `jazz_to_ja2_profile.csv` (profile_id + speech_source + status).  
Folder crosswalk: `jazz_to_ja2mercs_folders.csv` (from `docs/tools/_ja2mercs_folder_map.py`).  
Speech ID bands (Bayun + схема реплик): `JA2_SPEECH_ID_RANGES.md`, `schemas/AIM-stem-roles.md`.  
In-game ear-check: `VERIFY.md`.

## Preferred source: `Downloads/ja2mercs (1)/ja2mercs`

Pid-prefixed folders (`аимовцы/005 trevor`, `цс/165 gaston`, …) + `схема реплик *.xlsx` (copied under `schemas/`).  
Fallback: `Downloads/ja2mercs/ja2mercs` (legacy unprefixed names; ship resolves both).

```text
python docs/tools/_inventory_ja2mercs.py
python docs/tools/_apply_ja2mercs_profile_map.py          # write folders CSV + profile speech_source
python docs/tools/_inject_vr_stubs_ja2_voices.py          # empty VR → stub (need_pack fill)
python docs/tools/_expand_ja2_merc_vr_full.py --only …
python docs/tools/_ship_ja2_merc_voices.py --ja2mercs-remesh --include-done --aim-chat
python docs/tools/_wire_ja12_chat_voice_tags.py --apply   # WIP chat T() → voice:Jazz_*
python docs/tools/_fill_ja12_chat_voices.py --apply       # = ship --aim-chat-only
python docs/tools/_clear_ja12_selection_chat_donors.py --apply  # drop ATTN-as-hire leftovers
python docs/tools/_audit_ja12_merc_voices.py
```

`speech_source=ja2mercs:<cat>/<merc>[|battle=<pid>][|merge_speech]`

Pack remaps in ja2mercs (1) (file prefixes, not Jazz identity):

| Slug | profile_id | Notes |
| --- | --- | --- |
| Gaston / Horg / Biggens | 165 / 166 / 168 | ЦС consolidated (was U_58+165, …) |
| Kulba | 164 | was 062; Simon took 062 |
| Benny / Simon | 040 / 062 | SJ remapped (≠ Biff data_slf 040, ≠ Dynamo 066) |
| Grom | 047 + `R_047` | ex-076 → `R_047_*`; `\|battle=R_047\|merge_speech` |
| Manuel | 167 | was skip (old folder 060=Dimitri) |

Do not mix co-folder banks (Carlos≠Gaston, Shank≠Benny, Dynamo≠Simon).

### Owner leftovers (not remeshed)

| Slug | Why |
| --- | --- |
| `mike` | `локался/074 mike` — identity unclear |
| `biff` | no ja2mercs folder — keep `data_slf` |
| `lynx` / `tosca` / `spider` / `spouke` | `done_manual` — original JA3 VO; never overwrite |
| Workshop `Merc_*` | different packs — do not touch |

## Schemas (speech ↔ role ↔ merc)

| Path | What |
| --- | --- |
| `schemas/схема реплик AIM.xlsx` (+ IMP/MERC/RPC *.xlsx) | Stem → role text (from pack) |
| `schemas/AIM-stem-roles.md` | Markdown export of AIM schema |
| Per-merc `*.txt` in pack folders | Line transcripts (subtitle / STT ref) |

## Caches (extracted archives, not committed audio intent — local workdirs)

| Folder | Source archive | Contents |
| --- | --- | --- |
| `ja2no-mercedt/` | NightOps `MERCEDT.SLF` | UTF-8 line texts; **filenames/nicks often lie** — trust greeting 108 / buddy lines |
| `_wav_cache/` | extracted from SLF / ja2mercs during ship | working WAV/OGG before opus |
| `_horg_stogie_cache/` | `JA2 1.13 - оригинальная озвучка Бычка.rar` | superseded by ja2mercs `цс/166 stogie` when remeshed |
| `_ub_cs_cache/` | `Озвучка для Цены Свободы.rar` | superseded by ja2mercs `цс/*` |
| `_wildfire_cache/` | `Jagged_Alliance_2_1_13_Wildfire_RUS.arc` | Data-UB alt; WF AIM VO in ja2mercs `вилдфаер/*` |
| `_sj_cache/` | Shady Job | prior SJ ship; ja2mercs `но-шж/*` preferred |
| `_stt/` | generated | optional STT samples |

## Ship notes

Gold pattern: `Jazz_Colby` — hire from `081–120` (`AIM_CHAT_WAV`); combat from battle + `000–080`.  
Never overwrite `spouke` / `lynx` / `tosca` / `spider` (`done_manual` — original JA3 VO).  
MERK / локался without hire files: combat only; AIM chat stays silent (do not copy Selection).
