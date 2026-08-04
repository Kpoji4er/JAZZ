# Jazz ↔ JA2/NO/UB voice alignment

Canonical map: `jazz_to_ja2_profile.csv`. Identity from mercedt **text** (greeting/buddy), not EDT filenames.

| slug | JA2 match | pid | status |
| --- | --- | --- | --- |
| colby | Trevor | 005 | done |
| lynx | Rudy Roberts / Рысь | 002 | done_manual (original JA3 VO) |
| blade | Razor / Бритва | 043 | shipped |
| ira | Ira (RPC) | 059 | shipped |
| dimitri | Dimitri (RPC) | 060 | shipped |
| madman | Maddog / Бешеный | 072 | shipped |
| conrad | Conrad Gillett | 070 | shipped |
| mike | — (JA1/NO battlefield) | — | need_pack |
| grom | SJ Sergey Gromov | 047 (+R_047 ex-076) | shipped (ja2mercs `047 gromov`) |
| benny | SJ Alexandra Benedict | 040 (pack remap; ≠ Biff) | shipped (ja2mercs `040 benni`) |
| simon | SJ Simon Garandier | 062 (pack remap; ≠ Dynamo) | shipped (ja2mercs `062 simon`) |
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
| gaston | UB Gaston Cavalier | 165 (was U_58+165) | shipped |
| horg | UB Stogie / Сигара (ЦС) | 166 (was U_59+166) | shipped |
| manuel | NO/UB Manuel | 167 | shipped (ja2mercs `167 manuel`) |
| monk | Wildfire AIM | 170 | shipped |
| allik | Wildfire AIM | 171 | shipped |
| henning | Wildfire AIM | 173 | shipped |
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
| biggens | UB Colonel Biggens | 168 | shipped |
| kulba | UB John Kulba (ЦС) | 164 (was 062) | shipped |
| vilde | Wildfire AIM | 172 | shipped |
| grace | Wildfire AIM | 176 | shipped |
| steiger | Wildfire AIM | 177 | shipped |
| lucky | Wildfire AIM | 174 | shipped |
| laura | Wildfire AIM | 175 | shipped |
| eskimo | NO overlay | 065 | shipped |
| tosca | Тоска / Jazz_Buzz | 016 | done_manual (original JA3 VO) |
| spider | Dr Houston / Паук | 019 | done_manual (original JA3 VO) |
| spouke | JA3 manual VO | — | done_manual |

## Notes

- «Алле, алле!» = Malice **032** (`Jazz_Vicious`), not Gaston.
- `039_Gaston.csv` filename lies → Lava texts; do not ship as Gaston.
- Gaston = UB **058** (`ub_wildfire_folder` → `_wildfire_cache/.../Data-UB`). Self-ID «Я, Гастон Кавалье». Do **not** use NO/data_slf 058 (Carlos) or Malice 032.
- Carlos stays `data_slf` **058** — same numeric id, different pack; ship sources must not cross.
- Wildfire RUS `.arc` (`_extract_wildfire_rus_arc.py`): 1.13 RUS + WF **maps** only. AIM slots 001/003/005/010/012/022/032/037 in that pack are still Blood/Grizzly/Trevor/…/Malice/Wolf — **not** Allik/Henning/Laura/Lucky/Grace/Monk/Steiger/Vilde. Need commercial WF DE voice pack for those.
- External caches: `_ub_cs_cache` (ЦС), `_horg_stogie_cache` (Бычок), `_wildfire_cache` (WF RUS arc).
