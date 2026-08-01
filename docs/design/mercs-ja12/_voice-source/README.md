# JA2 / NightOps / UB voice sources

Mapping: `jazz_to_ja2_profile.csv` (profile_id + speech_source + status).

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
python docs/tools/_inject_vr_stubs_ja2_voices.py
python docs/tools/_ship_ja2_merc_voices.py --only slug1,slug2
```

Never overwrite `spouke` (`done_manual`).
