# Как проверить голоса JA12 (Jazz ↔ JA2)

Канон-карта: `jazz_to_ja2_profile.csv` (+ пояснения в `jazz_vs_ja2no_alignment.md`).  
Диапазоны JA2 speech ID (Баюн): [`JA2_SPEECH_ID_RANGES.md`](JA2_SPEECH_ID_RANGES.md) — **000–080** бой/карта, **081–120** найм/AIM; MERK без hire; коллизии pid = по содержимому.  
Статический аудит файлов: `python docs/tools/_audit_ja12_merc_voices.py` (из корня `jazz/`).

**Важно:** аудит проверяет «opus на месте», а не «это голос нужного персонажа». Несовпадение персонажа ловится только на слух. AIM/Snype **hire chat**:
- classic `081–120` когда в папке есть hire-банк;
- MERK/RPC/Biff без hire → combat-proxy (`HIRE_FALLBACK_WAV`, не ATTN);
- UB ЦС (Gaston/Manuel/Biggens/Kulba/Horg) → `UB_HIRE_PROXY_WAV` (self-ID/readiness; в `081–120` там кампания, не найм);
- Mike hire: OLD pack `локался/mike` `R_074_08x` (`HIRE_ALT_BANKS`).

## В игре (быстрый чеклист)

1. Нанять мерка → AIM / Snype-чат: фразы найма/отказа (слот вокруг Selection / chat).
2. На тактике выделить юнита (клик по портрету / юниту) → **Selection**.
3. Дать приказ на движение в бою → **CombatMovement**.
4. Прицелиться / открыть огонь → **AimAttack**.
5. Сравнить 2–3 мерков подряд: один «эталон» (например Colby/Trevor) и подозреваемый.

### Тихий / нет файла vs чужой голос

| Симптом | Что это |
| --- | --- |
| Клик — тишина, UI жив | missing opus / слот без файла (`need_pack`, stub) |
| Голос есть, но «это не тот мужик/баба из JA2» | вероятно неверный **profile_id** или чужой pack (см. CSV) |
| Голос «тот», но текст AIM другой | нормально: текст Jazz, аудио с JA2-донора |

Сообщение владельцу: *«X должен быть Y (pid N), а звучит как Z»* — сослаться на строку в CSV.

## Известные ремапы (не путать с EDT-именами файлов)

| Jazz | Должен звучать как | pid | Не путать с |
| --- | --- | --- | --- |
| Hitman | Slay / Убийца Terry | 064 | Hennessey 022 |
| Nervous | Haywire / Нервный | 041 | Razor 043 (= Blade) |
| Rothman | Stefan Rothman | 030 | файл `030_Hitman` врёт |
| Vicious | La Malice («Алле») | 032 | Gaston |
| Blade | Razor / Бритва | 043 | Nervous |
| Gaston | UB Gaston Cavalier | 058 UB | Carlos `data_slf` 058 |
| Carlos | Carlos RPC | 058 SLF | Gaston UB |
| Benny | SJ Benedict | 067 SJ | Shank SLF 067 |
| Simon | SJ Grandier | 066 SJ | Dynamo SLF 066 |
| Buzz (`tosca`) | original JA3 VO | — | `done_manual` |
| Spider | original JA3 VO | — | `done_manual` |

## High-visibility spot (ожидание)

Ira 059 · Hobbit/Gumpy 045 · Hitman/Slay 064 · Spider/Lynx/Buzz = original JA3 (`done_manual`) · Grom ja2mercs 076+047 · Colby/Trevor 005.

## ja2mercs remesh (2026-08)

Preferred pack: `Downloads/ja2mercs (1)/ja2mercs` (pid-prefixed folders + `схема реплик`).  
Combat + AIM chat: `_ship_ja2_merc_voices.py --ja2mercs-remesh --aim-chat`.  
Ear-check **Gaston** (UB French, not Carlos) · **Benny** (female SJ, pack pid 040) vs **Shank** · **Simon** (pack 062) vs **Dynamo** · **Vicious** (Malice «Алле») · WF AIM hire (`108` greeting ≠ Selection).  
Leftovers: Biff = `data_slf` combat-proxy hire. Lynx/Buzz/Spider/`spouke` = `done_manual` (original JA3 VO; restored after accidental remesh 792d1c5).  
**Hire UI ear-check (2026-08):** silent MERK/RPC list + UB wrong-replica + Danny/Highball text↔audio.  
Tools: `_pour_ja12_design_hire_chat.py` (design phrases) · `_stt_hire_chat_lines.py` (Quinten/Highball) · `_fill_ja12_chat_voices.py --apply --only …`.  
**Re-check after R_-fullest remesh:** Mike `074`+OLD hire · Vince `R_069` · Kulba `R_164` · Biggens `R_168` (Rothman control).

### Grom / `но-шж/047 gromov`

Both `047_*` and `R_047_*` (ex-`076_*`) are Grom. `speech_source=ja2mercs:но-шж/047 gromov|battle=R_047|merge_speech`.
