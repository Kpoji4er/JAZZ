# Как проверить голоса JA12 (Jazz ↔ JA2)

Канон-карта: `jazz_to_ja2_profile.csv` (+ пояснения в `jazz_vs_ja2no_alignment.md`).  
Статический аудит файлов: `python docs/tools/_audit_ja12_merc_voices.py` (из корня `jazz/`).

**Важно:** аудит проверяет «opus на месте», а не «это голос нужного персонажа». Несовпадение персонажа ловится только на слух.

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
| Simon | SJ Garandier | 066 SJ | Dynamo SLF 066 |
| Buzz (`tosca`) | Buzz / Тарболс | 016 | — |
| Spider | Dr Houston / Паук | 019 | файл `019_Scully` врёт |

## High-visibility spot (ожидание)

Ira 059 · Hobbit/Gumpy 045 · Hitman/Slay 064 · Spider/Houston 019 · Lynx 002 · Buzz 016 · Grom SJ 076 · Colby/Trevor 005.
