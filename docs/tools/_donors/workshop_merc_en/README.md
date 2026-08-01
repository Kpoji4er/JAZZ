# Workshop merc English donors

Cached non-Cyrillic `T(id, …)` bodies for AIM workshop mercs when the local
`Merc_*` AppData pack is RU-baked (Carol) or otherwise missing English text.

| File | Source |
| --- | --- |
| `Merc_CarolThompson.tsv` | Steam Workshop item `3023246026` (`ModContent.hpk`), extracted Aug 2023 EN build |

Refresh Carol donor:

```text
steamcmd +login anonymous +workshop_download_item 1084160 3023246026 +quit
hpk extract <…>/3023246026/ModContent.hpk <extract_dir>
python docs/tools/_fix_workshop_merc_en_from_sources.py --cache-extract <extract_dir> --merc Merc_CarolThompson
```
