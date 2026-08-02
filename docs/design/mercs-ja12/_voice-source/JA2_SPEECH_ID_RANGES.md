# JA2 SPEECH line ID ranges (Bayun canon)

Источник: Discord / Баюн (пустой follow-up = принять как истину для JA2 speech IDs).  
Связано: `VERIFY.md`, `SLOT_WAV` / `AIM_CHAT_WAV` в `docs/tools/_ship_ja2_merc_voices.py`, эталон AIM у Colby (`_ship_colby_voices_ja2_only.py`).

## Диапазоны (один profile_id = один банк `NNN_###`)

| Line IDs | Назначение |
| --- | --- |
| **000–080** | Фразы юнитов **без найма** — бой, карта, тактический talk (`SPEECH` + рядом `BATTLESNDS` ATTN/OK/HIT/DIE…) |
| **081–120** | Фразы **найма** / AIM-chat style (greeting, refuse, rehire, parting…) |

Имена battle-стемов (`ATTN`, `OK1`, `HIT1`, `DIE`, `ENEMY`, `LMATTN`…) — не SPEECH-номера; они живут в battle-банке и **не** пересекаются с hire-диапазоном.

## MERK

Мерки из **MERK** (в ja2mercs часто папка `мерки/`: Razor, Haywire, Flo, Cougar, Gasket, Gumpy, Numb, Bubba…): **нет hiring phrases**.  
Не ждать полноценных `081–120` для AIM/Snype; chat либо молчит, либо осознанный fallback (не выдавать ATTN за «найм»).

## Коллизии адресов

Один и тот же numeric `profile_id` / префикс файла у **разных модов** может означать **разный контент**. Подстановка — **по содержимому** (голос/текст/STT), не по имени папки и не по EDT-нику в filename.  
Уже зафиксированные Jazz-кейсы: Carlos≠Gaston (`058`), Shank≠Benny (`067`), Dynamo≠Simon (`066`), Manuel≠Dimitri (`060`), Grom pack `076`+`047` (owner).

## Сборка из «базовых» фраз

В ja2mercs банки часто свалены по папкам. Следующий remesh/ship должен **собирать** слоты Jazz из базовых stems по таблице ниже (а не копировать чужой банк целиком и не кормить hire из Selection).  
Hire-файлы могут прийти отдельно (renamed) — маппить в `081–120` по слоту AIM, не в combat VR.

## Jazz impact (после remesh 2026-08)

Канон ролей стемов: `schemas/AIM-stem-roles.md` (= `схема реплик AIM.xlsx` из `Downloads/ja2mercs (1)`).

| Поток | Сейчас | Vs Bayun / схема |
| --- | --- | --- |
| Combat VR (`SLOT_WAV` → `000–080` + battle) | Selection=`ATTN`, AimAttack=`ENEMY`/`000`/`027`, … | **OK** |
| AIM chat (`--aim-chat` / `_fill_ja12_chat_voices.py`) | UnitData slots ← `AIM_CHAT_WAV` (`081–120`) | **OK** для AIM/ЦС/WF с hire-банком |
| Colby gold | Offline=`084`, Greeting=`108`, … | **OK** — эталон |
| Inject stubs | Selection prefs combat `072`/`000`/`027` | **OK** (hire больше не в Selection) |
| MERK / локался без `081–120` | combat remesh OK; chat opus cleared (silent > ATTN) | **OK** — не подставлять ATTN |

**Итог:** combat и hire разделены. Ship: `_ship_ja2_merc_voices.py --ja2mercs-remesh --aim-chat`. Legacy Selection-chat: `_clear_ja12_selection_chat_donors.py`.

---

## Предлагаемый remap (Jazz → JA2)

### Combat VoiceResponse → `000–080` + battle (как сейчас в `SLOT_WAV`)

| Jazz VR slot | JA2 stems (pref order) | Band |
| --- | --- | --- |
| Selection | ATTN, COOL, HUMM, OK1 | battle |
| SelectionStealth | LMATTN, LMOK1, LMOK2 | battle |
| Order / CombatMovement | OK1, OK2, GOTIT | battle |
| AimAttack | ENEMY, 000, 027 | battle + 0–80 |
| OpponentFound | 000, 001, ENEMY | 0–80 + battle |
| OpponentKilled | 027, 028, 032 | 0–80 |
| NoAmmo / AmmoLow | 013 | 0–80 |
| Pain | HIT1, HIT2, CURSE | battle |
| Wounded / SeriouslyWounded | 014, 021 / 024 | 0–80 |
| Downed / DeathGeneral | DIE, DYING / DIE, CURSE | battle |
| CombatStart* / CombatEnd* | 072, 001, ENEMY, 065, 059, 070 | 0–80 + battle |
| Idle | COOL, HUMM, 045, NOTH | battle + 0–80 |
| LevelUp | 046 | 0–80 |
| SectorArrived | 078 | 0–80 |
| …остальное | см. `SLOT_WAV` | ≤080 или battle |

Не класть `081–120` в Selection / AimAttack / Order.

### AIM / Snype chat → `081–120` (Colby / Bayun)

| Jazz chat slot | JA2 line | Notes |
| --- | --- | --- |
| Offline | **084** | answering machine |
| GreetingAndOffer | **108** | greeting |
| ConversationRestart | **096** | |
| IdleLine | **109** | |
| PartingWords | **091** | contract accept / parting |
| RehireIntro | **089** | |
| RehireOutro | **090** | |
| Refusal (death toll) | **081** | |
| Refusal (disliked / «Fidel») | **086** | closest Colby refuse |
| Refusal (money) | **097** | |
| Haggle / HaggleRehire | **116** | |
| Mitigation | **094** | |
| ExtraPartingWords (recommend) | **053** | исключение: buddy-praise из **0–80** |

MERK: таблицу hire **не применять**, пока нет отдельных hire WAV; не подставлять ATTN молча как «найм».

### Карта / повстанцы

У map-hired / `локался` в `081–120` часто conversation (не AIM-sheet). Секторный «гид» повстанцев — отдельные фразы на вход в сектор; маппить осознанно (не в AimAttack).

## Процесс (Kpoji4er)

1. Не копировать схему Trevor/Colby blindly на всех (первый проход = mess).  
2. Второй проход: **расшифровка слов** (STT / EDT text) → подтвердить, что stem совпадает с ролью слота и персонажем.  
3. Адреса коллизий — только после content-check.
