# JA2 / NightOps / UB voice sources

Mapping: `jazz_to_ja2_profile.csv` (profile_id + speech_source + status).  
In-game ear-check: `VERIFY.md`.

## Caches (extracted archives, not committed audio intent — local workdirs)

| Folder | Source archive | Contents |
| --- | --- | --- |
| `ja2no-mercedt/` | NightOps `MERCEDT.SLF` | UTF-8 line texts; **filenames/nicks often lie** — trust greeting 108 / buddy lines |
| `_wav_cache/` | extracted from SLF during ship | working WAV before opus |
| `_horg_stogie_cache/` | `JA2 1.13 - оригинальная озвучка Бычка.rar` (Бычок) | profile `166_*` Speech+BattleSnds (alt Horg) |
| `_ub_cs_cache/` | `Озвучка для Цены Свободы.rar` (ЦС) | `U_59` Horg, `U_62` Kulba, `U_64` Tex, `U_73` Betty, `U_74` Raul, `056`, `159` Speck — **no Gaston** |
| `_wildfire_cache/` | `Jagged_Alliance_2_1_13_Wildfire_RUS.arc` (FreeArc; `docs/tools/_extract_wildfire_rus_arc.py`) | 1.13 RUS + WF **maps**; `Data-UB/058` = Gaston; AIM SPEECH still vanilla RU (not Allik/Monk/…) |

## Ship

```text
python docs/tools/_inject_vr_stubs_ja2_voices.py          # empty → 12-line stub (once)
python docs/tools/_expand_ja2_merc_vr_full.py             # stub → Colby-like combat slots
python docs/tools/_ship_ja2_merc_voices.py --queue        # opus for all VR T-ids
python docs/tools/_fill_ja12_chat_voices.py --apply       # AIM chat from Selection donor
python docs/tools/_audit_ja12_merc_voices.py              # verify
```

Gold pattern: `Jazz_Colby` — no `g_VoiceVariations`; `ModItemTranslatedVoices` → `Mod/Dv3mFVN/voices`; files `jazz-units/voices/<T-id>.opus`.

Never overwrite `spouke` (`done_manual`).
