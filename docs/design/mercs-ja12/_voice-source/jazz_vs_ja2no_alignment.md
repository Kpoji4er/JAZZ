# Jazz ↔ JA2/NO/UB voice alignment

Canonical map: `jazz_to_ja2_profile.csv`. Identity from mercedt **text** (greeting/buddy), not EDT filenames.

| slug | JA2 match | pid | status |
| --- | --- | --- | --- |
| colby | Trevor | 005 | done |
| lynx | Rudy Roberts / Рысь | 002 | shipped |
| blade | Razor / Бритва | 043 | shipped |
| ira | Ira (RPC) | 059 | shipped |
| dimitri | Dimitri (RPC) | 060 | shipped |
| madman | Maddog / Бешеный | 072 | shipped |
| conrad | Conrad Gillett | 070 | shipped |
| mike | — (JA1/NO battlefield) | — | need_pack |
| grom | SJ Sergey Gromov | 076 | shipped (`sj_folder`) |
| benny | SJ Alexandra Benedict | 067 | shipped (`sj_folder`; WIP UnitData) |
| simon | SJ Simon Garandier | 066 | shipped (`sj_folder`; WIP UnitData; ≠ Dynamo data_slf 066) |
| rothman | Stefan Rothman (not Hitman file) | 030 | shipped |
| quinten | Dr Quinten | 028 | shipped |
| vicious | La Malice / Злобный («Алле») | 032 | shipped |
| biff | Biff Upscott | 040 | shipped |
| nervous | Haywire / Нервный | 041 | shipped |
| flo | Flo | 044 | shipped |
| cougar | Jim Wallace / Пума | 048 | shipped |
| miguel | Miguel | 057 | shipped |
| gamos | Hamous / Гамос | 063 | shipped |
| dynamo | Greg Duncan | 066 | shipped |
| gaston | UB Gaston Cavalier | 058 | shipped |
| horg | UB Stogie / Сигара (ЦС) | U_59 | shipped |
| manuel | NO/UB Manuel | 071 | shipped |
| monk | Wildfire AIM only | — | need_pack |
| allik | Wildfire AIM | — | need_pack |
| henning | Wildfire AIM | — | need_pack |
| static | Kirk Stevenson | 026 | shipped |
| highball | Clifford Highball | 020 | shipped |
| bull | John Peters | 021 | shipped |
| cord | Gasket / Кардан | 042 | shipped |
| hobbit | Gumpy / Хоббит | 045 | shipped |
| ricochet | Numb / Рикошет | 049 | shipped |
| meat | Meat | 050 | shipped |
| carlos | Carlos (RPC) | 058 | shipped |
| devin | Devin Connell | 061 | shipped |
| shank | Briam Druse | 067 | shipped |
| vince | Dr Vince (not Thor) | 069 | shipped |
| hitman | Slay / Убийца Terry (not Hennessey 022) | 064 | shipped |
| biggens | UB Colonel Biggens | — | need_pack |
| kulba | UB John Kulba (ЦС) | U_62 | shipped |
| vilde | Wildfire AIM | — | need_pack |
| grace | Wildfire AIM | — | need_pack |
| steiger | Wildfire AIM | — | need_pack |
| lucky | Wildfire AIM | — | need_pack |
| laura | Wildfire AIM | — | need_pack |
| eskimo | NO overlay | 065 | shipped |
| tosca | Buzz / Тарболс | 016 | shipped |
| spider | Dr Houston | 019 | shipped |
| spouke | JA3 manual VO | — | done_manual |

## Notes

- «Алле, алле!» = Malice **032** (`Jazz_Vicious`), not Gaston.
- `039_Gaston.csv` filename lies → Lava texts; do not ship as Gaston.
- Gaston = UB **058** (`ub_wildfire_folder` → `_wildfire_cache/.../Data-UB`). Self-ID «Я, Гастон Кавалье». Do **not** use NO/data_slf 058 (Carlos) or Malice 032.
- Carlos stays `data_slf` **058** — same numeric id, different pack; ship sources must not cross.
- Wildfire RUS `.arc` (`_extract_wildfire_rus_arc.py`): 1.13 RUS + WF **maps** only. AIM slots 001/003/005/010/012/022/032/037 in that pack are still Blood/Grizzly/Trevor/…/Malice/Wolf — **not** Allik/Henning/Laura/Lucky/Grace/Monk/Steiger/Vilde. Need commercial WF DE voice pack for those.
- External caches: `_ub_cs_cache` (ЦС), `_horg_stogie_cache` (Бычок), `_wildfire_cache` (WF RUS arc).
