# JA2 / NightOps / UB voice sources

Mapping: `jazz_to_ja2_profile.csv` (profile_id + speech_source + status).  
Folder crosswalk (ja2mercs): `jazz_to_ja2mercs_folders.csv` (from `docs/tools/_ja2mercs_folder_map.py`).  
In-game ear-check: `VERIFY.md`.

## Preferred source: `Downloads/ja2mercs/ja2mercs`

Same stems (`ATTN`/`OK`/`HIT`/`NNN_###`) as SLF ship. Prefer over old SLF/`_sj_cache` when folder identity is clear.

```text
python docs/tools/_inventory_ja2mercs.py
python docs/tools/_apply_ja2mercs_profile_map.py          # write folders CSV + profile speech_source
python docs/tools/_inject_vr_stubs_ja2_voices.py          # empty VR → stub (need_pack fill)
python docs/tools/_expand_ja2_merc_vr_full.py --only …
python docs/tools/_ship_ja2_merc_voices.py --ja2mercs-remesh --include-done
python docs/tools/_fill_ja12_chat_voices.py --apply
python docs/tools/_audit_ja12_merc_voices.py
```

`speech_source=ja2mercs:<cat>/<merc>[|battle=<pid>][|merge_speech]` — dual-bank ЦС (Gaston `U_58`+`165`, Horg `U_59`+`166`, Biggens `U_61`+`168`) uses battle pid for ATTN/OK/HIT only; speech pid never mixed with co-folder banks (Carlos≠Gaston, Shank≠Benny, Dynamo≠Simon). Same-merc dual prefixes: Grom `076`+`047` with `|battle=047|merge_speech` (owner: both are Grom).

### Owner leftovers (not remeshed)

| Slug | Why |
| --- | --- |
| `mike` | `локался/mike` pid **074?** — identity unclear |
| `manuel` | `цс/manuel` is pid **060** (= Dimitri), profile is **071** — do not mix |
| `biff` / `lynx` / `tosca` / `spider` | no ja2mercs folder — keep `data_slf` |
| `spouke` | `done_manual` — never overwrite |
| Workshop `Merc_*` | different packs — do not touch |

**Grom remesh (owner):** `но-шж/гром` holds **both** pid banks **076** and **047** as Grom (not a Larry misfile). Prefer full-folder ja2mercs remesh over keeping `sj_folder` as a blocker. Optional transcripts: `docs/tools/_stt_ja2mercs_sample.py` → `_voice-source/_stt/`.

## Caches (extracted archives, not committed audio intent — local workdirs)

| Folder | Source archive | Contents |
| --- | --- | --- |
| `ja2no-mercedt/` | NightOps `MERCEDT.SLF` | UTF-8 line texts; **filenames/nicks often lie** — trust greeting 108 / buddy lines |
| `_wav_cache/` | extracted from SLF / ja2mercs during ship | working WAV/OGG before opus |
| `_horg_stogie_cache/` | `JA2 1.13 - оригинальная озвучка Бычка.rar` (Бычок) | profile `166_*` Speech+BattleSnds (alt Horg) |
| `_ub_cs_cache/` | `Озвучка для Цены Свободы.rar` (ЦС) | `U_59` Horg, `U_62` Kulba, … — superseded by ja2mercs `цс/*` when remeshed |
| `_wildfire_cache/` | `Jagged_Alliance_2_1_13_Wildfire_RUS.arc` | Data-UB Gaston alt; commercial WF AIM VO lives in ja2mercs `вилдфаер/*` |
| `_sj_cache/` | Shady Job | prior Grom ship source; ja2mercs `гром` = Grom banks **076**+**047** (owner) for remesh |
| `_stt/` | generated | optional STT/reference transcript samples (`_stt_ja2mercs_sample.py`) |

## Ship (legacy SLF path)

```text
python docs/tools/_ship_ja2_merc_voices.py --queue
```

Gold pattern: `Jazz_Colby` — no `g_VoiceVariations`; `ModItemTranslatedVoices` → `Mod/Dv3mFVN/voices`; files `jazz-units/voices/<T-id>.opus`.

Never overwrite `spouke` (`done_manual`).
