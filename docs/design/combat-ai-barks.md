# Боевые окрики AI — канон текста

Текст над головой **врага**. Без голоса, без `BanterDef`.
Контракт: [`JAZZ-AI-BARK-001`](../specs/active/JAZZ-AI-BARK-001.md).

Канон строк — `docs/tools/_aibark_bank_data.py` (5 фраз на слот).
Таблицы ниже собираются: `python docs/tools/_aibark_bank_data.py`.
В бою не генерировать. Тултип ауры не пересказывать.

Английская колонка — строка для `English.csv`. Русский пишется первым.

## Голос

Легион — банда в чужой форме. Бригадир орёт на своих, как на шайку.
Капитан злее и короче, но это всё ещё не армия. Головорез орёт от страха
и жадности. Палач почти не раскрывает рот.

Окрик — одним дыханием, своим, не игроку.

### Нельзя

- Рация и устав: отход, сектор, завеса, фланг, понял, приём
- Канцелярит: занимаем, осуществляем, данный
- Московская феня: братва, ксива, стрелка
- Подпись предмета: «Граната», «Фаер», «Дымовая», «Пулемёт»
- Тултип: «Держать линию», «Сосредоточить огонь»
- Шутка в камеру, мем
- Пол в шаблоне (`его` / `him`) — только `<name>` или «этот / тот»
- Мат в каждой строке (`падлы` у бригадира — редко, не норма)

## QA-pass (лексика)

Пять проходов. Русский пишется первым и должен **быть** русской устной
фразой, не подписью к английскому.

1. **Поле.** Словарь банды, не устав / канцелярит / феня / UI-имя предмета.
2. **Калька.** Нет обрубка и нет английского порядка слов
   («чтоб морды видно», «этим в хату», «На ленту!» как switch).
3. **Повтор корня.** Не больше двух из пяти вариантов слота; не расползаться
   по разным событиям (`накро-`, `живо`).
4. **Рот / тир.** Головорез ≠ палач. Пять вариантов — разные рты, не синонимы.
5. **Вслух.** Целая фраза: рот так и орёт, без додумывания глагола.
   Обрубок («Пру.», «Серое.», «я уже!», «я рывком», «с этим» про ствол) — вычеркнуть.

Длина отдельно: RU ≤ 42, EN ≤ 48, `<name>` совпадает.

Машина: `python docs/tools/_check_aibark_bank.py`

## Ленты

| Лента | Кто |
| --- | --- |
| `boss` | Приказ. Сержант / `Leader` / аура **15** |
| `officer` | Приказ. Лейтенант, капитан, наёмный капитан, именные |
| `t1` | `_T1_` |
| `t2` | `_T2_` / `_T3_` |
| `t4` | `_T4_` |

Приказ — по званию. Остальное — по классу. Игрок / милиция / повстанцы молчат.

## Когда орём

Всегда **после** решения, видимый враг, не Fast-forward. Кап: 2 на команду за
ход, 1 на юнита за активацию. Пять фраз — пул, `unit:Random`.

| Событие | Стимул |
| --- | --- |
| `order_*` | Смена директивы ауры. Все 10 приказов CMD-001, плюс `order_focus_anon`. |
| `arch_panic` / `desert` / `berserk` / `medic` / `melee` | Смена динамического архетипа (once за бой на юнита). |
| `nade_flare` / `smoke` / `frag` / `fire` / `gas` | Бросок по `aoeType` (не имя предмета). |
| `wpn_*` | **Смена класса оружия** (A↔B / нож / тяжёлый), не каждый выстрел. |
| `mg_setup` | Сошки / посадка пулемёта, не смена класса. |
| `seq_press` | CMD-002 Late **press** / директива Push, путь ≥6. Боец бежит, не офицерский приказ. |
| `seq_flank` | Envelop / AI-007 probe, путь ≥6. |
| `move_long` | Путь ≥12, не FallBack (recontact, длинный рывок). |

Молчим: Dump, обычный выстрел тем же стволом, reload, overwatch, mobile shot,
stim, укрытие в конце хода, ack, пустые руки→ствол (починка слота),
короткий шаг, FallBack-перебежка (уже `order_fallback`).

Доктрина CMD-002: Early (фаер/дым/пулемёт/медик) → линия → Late Press.
Support уже орёт своими событиями; здесь слышно **волну Press** и обход.

Классы `wpn_*`: `rifle`, `shotgun`, `mg`, `sidearm`, `gl`, `rocket`, `sniper`,
`melee`. Барк только если класс **сменился**.

## Контекст

Не называем место, которого нет. Колонка `ctx` в таблицах:

| Тег | Когда правда |
| --- | --- |
| *(пусто)* | Всегда. В каждом слоте ≥2 таких — запас. |
| `in` | Цель / точка удара **в интерьере**. |
| `out` | Эта точка **снаружи** (улица, двор). |
| `into` | Говорящий снаружи, цель внутри (окно, дверь, «в хату»). |
| `high` | Говорящий **выше** цели (холм, крыша). |
| `houses` | На карте есть дома. |

Пул = фразы, у которых все теги истинны (пустые теги всегда проходят).
«Хата» на открытом поле не орём — берём нейтральную из того же слота.
Приказы `order_buildings` / `order_heights` уже отсекает picker директивы.

Машина: `python docs/tools/_check_aibark_bank.py` (место без тега = FAIL).

<!-- aibark-bank -->

### Приказ

**`order_hold`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | Стоим, не прём! | Stay put! Don't push! | `—` | 20157 |
| `boss` | Ни с места! | Nobody moves! | `—` | 20158 |
| `boss` | Двор наш — сидим | Yard's ours. Sit. | `out` | 20159 |
| `boss` | Не лезем пока | Don't go in yet | `—` | 20160 |
| `boss` | Пусть сами приходят | Let them come to us | `—` | 20161 |
| `officer` | Стоим. | Hold. | `—` | 20162 |
| `officer` | Не лезем. | Don't go in. | `—` | 20163 |
| `officer` | Здесь. | Here. | `—` | 20164 |
| `officer` | Ждём. | We wait. | `—` | 20165 |
| `officer` | Сидим. | Sit tight. | `—` | 20166 |

**`order_push`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | Шевелитесь, падлы! | Move, you dogs! | `—` | 20167 |
| `boss` | Бейте уже, живо! | Hit 'em already! | `—` | 20168 |
| `boss` | Прём на них! | We go at them! | `—` | 20169 |
| `boss` | Не стойте — бейте! | Don't stand. Hit! | `—` | 20170 |
| `boss` | Давите, пока тёплые! | Hit them while they're up! | `—` | 20171 |
| `officer` | Вперёд, сказал. | I said move. | `—` | 20172 |
| `officer` | На них. Сейчас. | Now. Into them. | `—` | 20173 |
| `officer` | Прём. | We go. | `—` | 20174 |
| `officer` | Сейчас на них. | On them. Now. | `—` | 20175 |
| `officer` | Не ждите. | Don't wait. | `—` | 20176 |

**`order_envelop`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | Зайдите сзади, не в лоб! | Around back, not the front! | `—` | 20177 |
| `boss` | По дворам гоните! | Through the yards! | `out` | 20178 |
| `boss` | С боков зайдите! | Come in from the sides! | `—` | 20179 |
| `boss` | Не в улицу — сзади! | Not the street. Behind! | `out` | 20180 |
| `boss` | Обходите хаты! | Around the houses! | `houses` | 20181 |
| `officer` | Сзади зайдите. | Around back. | `—` | 20182 |
| `officer` | Не толпой. | Not in a bunch. | `—` | 20183 |
| `officer` | С краю. | From the edge. | `—` | 20184 |
| `officer` | Обойдите. | Go around. | `—` | 20185 |
| `officer` | Не в лоб. | Not straight in. | `—` | 20186 |

**`order_fallback`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | Валите назад! | Get back! | `—` | 20187 |
| `boss` | Прячьтесь, сомнут! | Down or you're next! | `—` | 20188 |
| `boss` | Сматываемся! | We're pulling out! | `—` | 20189 |
| `boss` | Назад, кто цел! | Back, if you're whole! | `—` | 20190 |
| `boss` | Живыми надо! | We need you alive! | `—` | 20191 |
| `officer` | Сваливаем. | We're out. | `—` | 20192 |
| `officer` | Назад. Живыми. | Back. Alive. | `—` | 20193 |
| `officer` | Уходим. | Leaving. | `—` | 20194 |
| `officer` | Назад. | Back. | `—` | 20195 |
| `officer` | Хватит. | Enough. | `—` | 20196 |

**`order_focus`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | Всех на <name>! | All of you — <name>! | `—` | 20197 |
| `boss` | <name> — и больше никого | <name>. Nobody else. | `—` | 20198 |
| `boss` | На <name>, шмалите! | On <name>. Shoot! | `—` | 20199 |
| `boss` | <name> снимите! | Drop <name>! | `—` | 20200 |
| `boss` | Только <name>, я сказал! | Only <name>, I said! | `—` | 20201 |
| `officer` | <name>. Всех. | <name>. Everyone. | `—` | 20202 |
| `officer` | Только <name>. | Only <name>. | `—` | 20203 |
| `officer` | <name>. | <name>. | `—` | 20204 |
| `officer` | Огонь — <name>. | Fire. <name>. | `—` | 20205 |
| `officer` | <name>. Снимите. | <name>. Drop him. | `—` | 20206 |

**`order_focus_anon`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | Вот этого бейте! | That one. Hit him! | `—` | 20207 |
| `boss` | Не шмалите по всем! | Stop spraying! | `—` | 20208 |
| `boss` | Одного, всех на него! | One man. All of you! | `—` | 20209 |
| `boss` | Этот, только этот! | This one. Only this! | `—` | 20210 |
| `boss` | Не мазать — одного! | Don't spray. One! | `—` | 20211 |
| `officer` | Этого. Всех. | That one. All of you. | `—` | 20212 |
| `officer` | Не по всем. | Don't split it. | `—` | 20213 |
| `officer` | Одного. | One of them. | `—` | 20214 |
| `officer` | Этот. | This one. | `—` | 20215 |
| `officer` | Не мазать. | Don't spray. | `—` | 20216 |

**`order_buildings`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | В хаты, из окон! | Inside! Windows! | `—` | 20217 |
| `boss` | С двора — в дом! | Off the yard. Inside! | `—` | 20218 |
| `boss` | По хатам! | Into the houses! | `—` | 20219 |
| `boss` | Бейте из окон! | From the windows! | `—` | 20220 |
| `boss` | Не во дворе — внутрь! | Not the yard. Inside! | `—` | 20221 |
| `officer` | В хаты. | Inside. | `—` | 20222 |
| `officer` | Из окон. | From the windows. | `—` | 20223 |
| `officer` | В дома. | Indoors. | `—` | 20224 |
| `officer` | С двора прочь. | Off the yard. | `—` | 20225 |
| `officer` | Окна. | Windows. | `—` | 20226 |

**`order_heights`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | На крышу, кто живой! | Up the roof! | `—` | 20227 |
| `boss` | Сверху кладите! | Drop them from up there! | `—` | 20228 |
| `boss` | На холм, давайте! | Up the hill! | `—` | 20229 |
| `boss` | Крыши наши! | Roofs are ours! | `—` | 20230 |
| `boss` | Наверх, давайте! | Up, come on! | `—` | 20231 |
| `officer` | Наверх. | Up. | `—` | 20232 |
| `officer` | С холма. | From the hill. | `—` | 20233 |
| `officer` | Крыши. | Roofs. | `—` | 20234 |
| `officer` | Выше. | Higher. | `—` | 20235 |
| `officer` | Сверху. | From above. | `—` | 20236 |

**`order_cover`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | На брюхо, живо! | Belly down! | `—` | 20237 |
| `boss` | Ложись, пуль полно! | Down, bullets flying! | `—` | 20238 |
| `boss` | К земле! | To the dirt! | `—` | 20239 |
| `boss` | За угол! | Get behind! | `—` | 20240 |
| `boss` | Прячьте башки! | Heads down! | `—` | 20241 |
| `officer` | На брюхо. | Down. | `—` | 20242 |
| `officer` | Не маячь. | Don't pop up. | `—` | 20243 |
| `officer` | К земле. | To the dirt. | `—` | 20244 |
| `officer` | Ложись. | Get down. | `—` | 20245 |
| `officer` | Не светиться. | Don't show. | `—` | 20246 |

**`order_lowvis`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | В тёмное не лезьте! | Don't walk into that dark! | `—` | 20247 |
| `boss` | Стоим. Сами вылезут | Stay. Let 'em show. | `—` | 20248 |
| `boss` | Не в черноту! | Not into the black! | `—` | 20249 |
| `boss` | Ждём, пусть покажутся | Wait. Let them show. | `—` | 20250 |
| `boss` | Тихо стоим | Quiet. We stay. | `—` | 20251 |
| `officer` | Стоим. | Stay put. | `—` | 20252 |
| `officer` | Без героев. | No heroes. | `—` | 20253 |
| `officer` | Ждём света. | Wait for light. | `—` | 20254 |
| `officer` | Не лезьте. | Don't go in. | `—` | 20255 |
| `officer` | Тихо. | Quiet. | `—` | 20256 |

**`order_hidden`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `boss` | В тень, тихо! | Into the dark. Quiet! | `—` | 20257 |
| `boss` | Затаились! | Stay hidden! | `—` | 20258 |
| `boss` | Не светиться! | Don't show yourselves! | `—` | 20259 |
| `boss` | В траву, ложись! | In the grass. Down! | `out` | 20260 |
| `boss` | Тс-с. Сгинь. | Shh. Vanish. | `—` | 20261 |
| `officer` | В тень. | Into cover. | `—` | 20262 |
| `officer` | Тихо. | Quiet. | `—` | 20263 |
| `officer` | Не светиться. | Don't show. | `—` | 20264 |
| `officer` | Затаились. | Stay hidden. | `—` | 20265 |
| `officer` | Сгинь. | Vanish. | `—` | 20266 |
### Смена архетипа

**`arch_panic`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Не надо… | Please— | `—` | 20267 |
| `t1` | Я домой, я домой | I wanna go home | `—` | 20268 |
| `t1` | Мама… | Mama— | `—` | 20269 |
| `t1` | Не стреляйте— | Don't shoot— | `—` | 20270 |
| `t1` | Я не хочу | I don't want this | `—` | 20271 |
| `t2` | Нас сомнут! | They'll walk over us! | `—` | 20272 |
| `t2` | Не стоим, валим | We're not staying. Go! | `—` | 20273 |
| `t2` | Это мясорубка | This is a butcher shop | `—` | 20274 |
| `t2` | Нас сложат | They'll drop us | `—` | 20275 |
| `t2` | Пора сматываться | Time to go | `—` | 20276 |
| `t4` | Чёрт… | Damn it— | `—` | 20277 |
| `t4` | Не сейчас | Not now | `—` | 20278 |
| `t4` | Плохо | Bad | `—` | 20279 |
| `t4` | Не сюда | Not here | `—` | 20280 |
| `t4` | Хватит | Enough | `—` | 20281 |

**`arch_desert`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Жить охота | I wanna live | `—` | 20282 |
| `t1` | Сами деритесь | Fight it yourselves | `—` | 20283 |
| `t1` | Я сматываюсь | I'm taking off | `—` | 20284 |
| `t1` | Мне ещё жить | I still wanna live | `—` | 20285 |
| `t1` | Хватит с меня крови | I've seen enough blood | `—` | 20286 |
| `t2` | Хватит с меня | I'm through | `—` | 20287 |
| `t2` | Я своё отпахал | I've done my share | `—` | 20288 |
| `t2` | Ищите других | Find someone else | `—` | 20289 |
| `t2` | Я ухожу | I'm leaving | `—` | 20290 |
| `t2` | Дальше без меня | You go on without me | `—` | 20291 |
| `t4` | Ищите дураков | Find another fool | `—` | 20292 |
| `t4` | Мне тут ловить нечего | Nothing left for me here | `—` | 20293 |
| `t4` | Контракт кончен | Job's done | `—` | 20294 |
| `t4` | Я выхожу | I'm out | `—` | 20295 |
| `t4` | Не мой бой | Not my fight | `—` | 20296 |

**`arch_berserk`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Убью! Убью! | I'll kill you! | `—` | 20297 |
| `t1` | А-а! Идите сюда! | Aaah! Come here! | `—` | 20298 |
| `t1` | Всех порву! | I'll tear you all! | `—` | 20299 |
| `t1` | Кровь! Ещё! | Blood! More! | `—` | 20300 |
| `t1` | Не остановить! | Can't stop me! | `—` | 20301 |
| `t2` | Всех кладу! | I'll drop you all! | `—` | 20302 |
| `t2` | Хватит прятаться! | Stop hiding! | `—` | 20303 |
| `t2` | Иду на вас! | Coming for you! | `—` | 20304 |
| `t2` | Рубить! | Cut them down! | `—` | 20305 |
| `t2` | Никого живым! | Nobody lives! | `—` | 20306 |
| `t4` | Всех. | All of you. | `—` | 20307 |
| `t4` | Иду. | Coming. | `—` | 20308 |
| `t4` | Дорежу. | I'll finish it. | `—` | 20309 |
| `t4` | Хватит ждать. | Enough waiting. | `—` | 20310 |
| `t4` | Вперёд. | Forward. | `—` | 20311 |

**`arch_medic`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Тихо ты | Easy | `—` | 20312 |
| `t1` | Кровь уйму, лежи | I'll stop the blood | `—` | 20313 |
| `t1` | Сейчас перевяжу | I'll bind it | `—` | 20314 |
| `t1` | Не дёргайся, живой | Don't jerk. You're alive | `—` | 20315 |
| `t1` | Лежи, я рядом | Stay down. I'm here | `—` | 20316 |
| `t2` | Не дёргайся | Don't jerk | `—` | 20317 |
| `t2` | Заткнись — проживёшь | Shut up and you'll live | `—` | 20318 |
| `t2` | Бинтую, не ори | Binding. Don't yell | `—` | 20319 |
| `t2` | Жить будешь | You'll live | `—` | 20320 |
| `t2` | Держись, зашью | Hold on. I'll close it | `—` | 20321 |
| `t4` | Лежи. | Lie still. | `—` | 20322 |
| `t4` | Не мешай. | Don't get in the way. | `—` | 20323 |
| `t4` | Тихо. | Quiet. | `—` | 20324 |
| `t4` | Живой. Лежи. | Alive. Stay down. | `—` | 20325 |
| `t4` | Руки. | Hands. | `—` | 20326 |

**`arch_melee`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Порежу! | I'll cut you! | `—` | 20327 |
| `t1` | Ближе, ближе | Closer— | `—` | 20328 |
| `t1` | Нож, нож! | Knife, knife! | `—` | 20329 |
| `t1` | В морду схожу! | I'm coming in! | `—` | 20330 |
| `t1` | Патронов жалко — режу | Save the rounds. Cutting | `—` | 20331 |
| `t2` | Вплотную проще | Easier up close | `—` | 20332 |
| `t2` | Иду на нож | On the knife | `—` | 20333 |
| `t2` | В упор | Point blank | `—` | 20334 |
| `t2` | Хватит стрелять — режем | Enough shooting. Cut | `—` | 20335 |
| `t2` | Иду вплотную | Going in close | `—` | 20336 |
| `t4` | Вплотную. | Close in. | `—` | 20337 |
| `t4` | Хватит стрелять. | Enough shooting. | `—` | 20338 |
| `t4` | Нож. | Knife. | `—` | 20339 |
| `t4` | В упор. | Point blank. | `—` | 20340 |
| `t4` | Ближе. | Closer. | `—` | 20341 |
### Граната

**`nade_flare`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Гори, зараза! | Burn, damn you! | `—` | 20342 |
| `t1` | Рожи на свет! | Faces into the light! | `—` | 20343 |
| `t1` | Свет, свет! | Light, light! | `—` | 20344 |
| `t1` | Гори им в глаза! | Burn in their eyes! | `—` | 20345 |
| `t1` | Чтоб видно было! | So we can see! | `—` | 20346 |
| `t2` | Свет им в глаза | In their eyes | `—` | 20347 |
| `t2` | Вылезайте, гады | Come out, you bastards | `—` | 20348 |
| `t2` | Подсветил | Lit them | `—` | 20349 |
| `t2` | Теперь видно | Now we see | `—` | 20350 |
| `t2` | Не прячьтесь | No more hiding | `—` | 20351 |
| `t4` | Свет. | Light. | `—` | 20352 |
| `t4` | Видно будет. | They'll show. | `—` | 20353 |
| `t4` | Гори. | Burn. | `—` | 20354 |
| `t4` | В глаза. | Eyes. | `—` | 20355 |
| `t4` | Вижу. | I see. | `—` | 20356 |

**`nade_smoke`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | В дым! | Into the smoke! | `—` | 20357 |
| `t1` | Сейчас не увидят | They won't see | `—` | 20358 |
| `t1` | Прячемся в дыму | We hide in the smoke | `—` | 20359 |
| `t1` | Прячьтесь в дым! | Hide in the smoke! | `—` | 20360 |
| `t1` | Чтоб не видели! | So they don't see! | `—` | 20361 |
| `t2` | Дымом закрою | I'll cover us | `—` | 20362 |
| `t2` | Через дым прём | Through the smoke | `—` | 20363 |
| `t2` | Закрой двор | Cover the yard | `out` | 20364 |
| `t2` | Под дым идём | We go under the smoke | `—` | 20365 |
| `t2` | Не видят — прём | They can't see. Go | `—` | 20366 |
| `t4` | Дым — и сразу | Smoke. Then we go. | `—` | 20367 |
| `t4` | Закрыл. Прём. | Covered. Go. | `—` | 20368 |
| `t4` | Дым. | Smoke. | `—` | 20369 |
| `t4` | Закрой. | Cover it. | `—` | 20370 |
| `t4` | Идём. | We go. | `—` | 20371 |

**`nade_frag`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Нате, гады! | Here, you bastards! | `—` | 20372 |
| `t1` | Держите! | Catch! | `—` | 20373 |
| `t1` | Вам туда! | That's for you! | `—` | 20374 |
| `t1` | Ловите! | Catch this! | `—` | 20375 |
| `t1` | Сейчас бахнет! | This one's gonna bang! | `—` | 20376 |
| `t2` | Летит! | It's in the air! | `—` | 20377 |
| `t2` | Ложись — не ты | Down — not you | `—` | 20378 |
| `t2` | Под ноги им | At their feet | `—` | 20379 |
| `t2` | Двор чищу | Clearing the yard | `out` | 20380 |
| `t2` | В кучу им | Into the bunch | `—` | 20381 |
| `t4` | Под ноги. | At their feet. | `—` | 20382 |
| `t4` | Лови. | For them. | `—` | 20383 |
| `t4` | Туда. | There. | `—` | 20384 |
| `t4` | Чищу. | Clearing. | `—` | 20385 |
| `t4` | Бах. | Bang. | `—` | 20386 |

**`nade_fire`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Горите! | Burn! | `—` | 20387 |
| `t1` | Жар им! | Heat for them! | `—` | 20388 |
| `t1` | Хату палю! | I'm torching the house! | `in` | 20389 |
| `t1` | Огонь, огонь! | Fire, fire! | `—` | 20390 |
| `t1` | Пусть жарятся! | Let them fry! | `—` | 20391 |
| `t2` | Жгу двор | Torching the yard | `out` | 20392 |
| `t2` | Огнём их! | Fire on them! | `—` | 20393 |
| `t2` | Пусть бегут | Let them run | `—` | 20394 |
| `t2` | Хату зажигаю | Lighting the house | `in` | 20395 |
| `t2` | Жарко будет | It'll get hot | `—` | 20396 |
| `t4` | Жги. | Burn it. | `—` | 20397 |
| `t4` | Огонь. | Fire. | `—` | 20398 |
| `t4` | Хату. | The house. | `in` | 20399 |
| `t4` | Жарко. | Heat. | `—` | 20400 |
| `t4` | Гори. | Burn. | `—` | 20401 |

**`nade_gas`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Пусть давятся! | Let them choke! | `—` | 20402 |
| `t1` | Гадость им! | Filth for them! | `—` | 20403 |
| `t1` | Кашляйте, гады! | Cough, you bastards! | `—` | 20404 |
| `t1` | Дышите этим! | Breathe that! | `—` | 20405 |
| `t1` | Сейчас заплюются! | They'll spit blood! | `—` | 20406 |
| `t2` | Пусть хлебают | Let them drink it | `—` | 20407 |
| `t2` | Двор порчу | Spoiling the yard | `out` | 20408 |
| `t2` | Не дышать им | They don't get air | `—` | 20409 |
| `t2` | Выкурят сами | They'll cough themselves out | `—` | 20410 |
| `t2` | Гадкость полетела | The filth's in the air | `—` | 20411 |
| `t4` | Дышите. | Breathe. | `—` | 20412 |
| `t4` | Во двор. | The yard. | `out` | 20413 |
| `t4` | Кашляй. | Cough. | `—` | 20414 |
| `t4` | Гадкость. | Filth. | `—` | 20415 |
| `t4` | Всё. | That's it. | `—` | 20416 |
### Смена оружия

**`wpn_rifle`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Длинный беру! | Grabbing the long one! | `—` | 20417 |
| `t1` | Длинный в руки! | Long one in hand! | `—` | 20418 |
| `t1` | Короткий не тянет | The short one's useless | `—` | 20419 |
| `t1` | Меняю на дальний! | Switching to the far one! | `—` | 20420 |
| `t1` | Беру ствол! | Grabbing a gun! | `—` | 20421 |
| `t2` | Длинный | Long gun | `—` | 20422 |
| `t2` | Длинный обратно | Long one back | `—` | 20423 |
| `t2` | С этого дальше бью | This one reaches farther | `—` | 20424 |
| `t2` | Меняю ствол | Switching guns | `—` | 20425 |
| `t2` | Этот дальше | This one reaches | `—` | 20426 |
| `t4` | Длинный. | Long one. | `—` | 20427 |
| `t4` | Дальше. | Farther. | `—` | 20428 |
| `t4` | Вернул. | Back on. | `—` | 20429 |
| `t4` | Ствол. | Gun. | `—` | 20430 |
| `t4` | Беру. | Taking it. | `—` | 20431 |

**`wpn_shotgun`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Дробь беру! | Grabbing buckshot! | `—` | 20432 |
| `t1` | Короткий злой беру! | Grabbing the short mean one! | `—` | 20433 |
| `t1` | В хату бью! | Into the house! | `into` | 20434 |
| `t1` | Меняю — в упор! | Switching. Up close! | `—` | 20435 |
| `t1` | Дверь сниму! | I'll take the door! | `into` | 20436 |
| `t2` | Дробь | Buckshot | `—` | 20437 |
| `t2` | В упор бью | Up close now | `—` | 20438 |
| `t2` | Короткий ставлю | Putting the short one on | `—` | 20439 |
| `t2` | В хату бью | Into the house | `into` | 20440 |
| `t2` | Вблизи лучше | Better up close | `—` | 20441 |
| `t4` | Дробь. | Buckshot. | `—` | 20442 |
| `t4` | В упор. | Up close. | `—` | 20443 |
| `t4` | Короткий. | Short one. | `—` | 20444 |
| `t4` | В хату. | Into the house. | `in` | 20445 |
| `t4` | Ставлю. | Putting it on. | `—` | 20446 |

**`wpn_mg`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Ленту ставлю! | Setting the belt! | `—` | 20447 |
| `t1` | Ленту в руки! | Belt in hand! | `—` | 20448 |
| `t1` | Длинный злой беру! | Grabbing the long mean one! | `—` | 20449 |
| `t1` | Меняю — улицу крою! | Switching. Street's mine! | `out` | 20450 |
| `t1` | Всех держу! | I'll hold them all! | `—` | 20451 |
| `t2` | Ленту ставлю | Setting the belt | `—` | 20452 |
| `t2` | Длинный ставлю | Setting the long one | `—` | 20453 |
| `t2` | Улицу крою | This covers the street | `out` | 20454 |
| `t2` | Двор держу | This holds the yard | `out` | 20455 |
| `t2` | Меняю на длинный | Switching to the long one | `—` | 20456 |
| `t4` | Лента. | Belt. | `—` | 20457 |
| `t4` | Длинный. | The long one. | `—` | 20458 |
| `t4` | Улицу. | The street. | `out` | 20459 |
| `t4` | Двор мой. | The yard's mine. | `out` | 20460 |
| `t4` | Моя. | Mine. | `—` | 20461 |

**`wpn_sidearm`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Короткий из кармана! | Short one from the pocket! | `—` | 20462 |
| `t1` | Короткий в руки! | Short one in hand! | `—` | 20463 |
| `t1` | Длинный заклинило— | Long one's jammed— | `—` | 20464 |
| `t1` | Меняю на быстрый! | Switching to the quick one! | `—` | 20465 |
| `t1` | С коротким в хату! | Short one into the house! | `into` | 20466 |
| `t2` | Короткий достаю | Pulling the short one | `—` | 20467 |
| `t2` | Из кармана | From the pocket | `—` | 20468 |
| `t2` | Так быстрее | Faster this way | `—` | 20469 |
| `t2` | Вплотную — короткий | Short one up close | `—` | 20470 |
| `t2` | Длинный потом | Long one later | `—` | 20471 |
| `t4` | Короткий. | Short one. | `—` | 20472 |
| `t4` | Из кармана. | Pocket. | `—` | 20473 |
| `t4` | Быстро. | Quick. | `—` | 20474 |
| `t4` | Вплотную. | Close. | `—` | 20475 |
| `t4` | Достал. | Got it. | `—` | 20476 |

**`wpn_gl`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Коротыш беру! | Grabbing the short one! | `—` | 20477 |
| `t1` | Коротыш в руки! | Short one in hand! | `—` | 20478 |
| `t1` | В окно бью! | Through the window! | `into` | 20479 |
| `t1` | Меняю — в дверь! | Switching. At the door! | `into` | 20480 |
| `t1` | По хате бью! | Hitting the house! | `in` | 20481 |
| `t2` | Коротыш ставлю | Putting the short one on | `—` | 20482 |
| `t2` | Под ствол ставлю | Under the barrel now | `—` | 20483 |
| `t2` | В окно бью | This one at the window | `into` | 20484 |
| `t2` | Дверь вынесу | I'll take the door | `into` | 20485 |
| `t2` | По хате бью | Hitting the house | `in` | 20486 |
| `t4` | Коротыш. | Short one. | `—` | 20487 |
| `t4` | Под ствол. | Under the barrel. | `—` | 20488 |
| `t4` | В окно. | Window. | `into` | 20489 |
| `t4` | В дверь. | Door. | `into` | 20490 |
| `t4` | В хату. | House. | `in` | 20491 |

**`wpn_rocket`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Трубу беру! | Grabbing the pipe! | `—` | 20492 |
| `t1` | Большую в руки! | The big one in hand! | `—` | 20493 |
| `t1` | Отойди, жахнет! | Back, this bangs! | `—` | 20494 |
| `t1` | Меняю — хату снесу! | Switching. House comes down! | `in` | 20495 |
| `t1` | С плеча эту! | This one off the shoulder! | `—` | 20496 |
| `t2` | Трубу беру | Grabbing the pipe | `—` | 20497 |
| `t2` | Трубу поднимаю | Pipe's going up | `—` | 20498 |
| `t2` | Тяжёлый ставлю | Putting the heavy one on | `—` | 20499 |
| `t2` | Эту хату снесу | That house comes down | `in` | 20500 |
| `t2` | С плеча | Off the shoulder | `—` | 20501 |
| `t4` | Труба. | Pipe. | `—` | 20502 |
| `t4` | Тяжёлый. | Heavy. | `—` | 20503 |
| `t4` | Снесу. | Coming down. | `—` | 20504 |
| `t4` | Хату. | The house. | `in` | 20505 |
| `t4` | С плеча. | Shoulder. | `—` | 20506 |

**`wpn_sniper`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Дальний беру! | Grabbing the long eye! | `—` | 20507 |
| `t1` | Дальний в руки! | Long one in hand! | `—` | 20508 |
| `t1` | Лягу и бью! | I'll go prone and shoot! | `—` | 20509 |
| `t1` | Меняю — с холма! | Switching. From the hill! | `high` | 20510 |
| `t1` | Не дыши — целюсь! | Don't breathe. Aiming! | `—` | 20511 |
| `t2` | Дальний ставлю | Putting the long one on | `—` | 20512 |
| `t2` | С холма бью | This one from the hill | `high` | 20513 |
| `t2` | Лежу, бью | Down. Shooting | `—` | 20514 |
| `t2` | Достаю с края | I can reach from here | `—` | 20515 |
| `t2` | Один — и тишина | One. Then quiet | `—` | 20516 |
| `t4` | Дальний. | Long one. | `—` | 20517 |
| `t4` | С холма. | The hill. | `high` | 20518 |
| `t4` | Лежу. | Down. | `—` | 20519 |
| `t4` | Один. | One. | `—` | 20520 |
| `t4` | Тишина. | Quiet. | `—` | 20521 |

**`wpn_melee`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Нож достаю! | Knife's out! | `—` | 20522 |
| `t1` | Ствол бросил — режу! | Dropped the gun. Cutting! | `—` | 20523 |
| `t1` | Железо в руки! | Iron in hand! | `—` | 20524 |
| `t1` | Патронов нет — нож! | No rounds. Knife! | `—` | 20525 |
| `t1` | Меняю — ближе! | Switching. Closer! | `—` | 20526 |
| `t2` | Иду на нож | On the knife | `—` | 20527 |
| `t2` | Ствол в сторону | Gun aside | `—` | 20528 |
| `t2` | Железо | Iron | `—` | 20529 |
| `t2` | Вплотную режу | This one up close | `—` | 20530 |
| `t2` | Резать | Cut | `—` | 20531 |
| `t4` | Нож. | Knife. | `—` | 20532 |
| `t4` | Ствол. | Gun down. | `—` | 20533 |
| `t4` | Железо. | Iron. | `—` | 20534 |
| `t4` | Вплотную. | Close. | `—` | 20535 |
| `t4` | Резать. | Cut. | `—` | 20536 |
### Пулемёт: сошки

**`mg_setup`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Я тут сяду | I'm sitting here | `—` | 20537 |
| `t1` | С угла накрою! | From this corner! | `—` | 20538 |
| `t1` | Ставлю, прикройте | Setting up. Cover me | `—` | 20539 |
| `t1` | Сюда сяду, улица моя | Sitting here. Street's mine | `out` | 20540 |
| `t1` | Ноги, тренога! | Legs down! | `—` | 20541 |
| `t2` | Улицу отсюда крою | I'll take the street | `out` | 20542 |
| `t2` | Сюда ставлю | Goes here | `—` | 20543 |
| `t2` | С угла | From the corner | `—` | 20544 |
| `t2` | Двор закрою | I'll shut the yard | `out` | 20545 |
| `t2` | Сел — улица моя | Sat. Street's mine | `out` | 20546 |
| `t4` | Улица моя. | This street's mine. | `out` | 20547 |
| `t4` | Сюда. | Here. | `—` | 20548 |
| `t4` | С угла. | Corner. | `—` | 20549 |
| `t4` | Сел. | Sat. | `—` | 20550 |
| `t4` | Двор мой. | Yard's mine. | `out` | 20551 |
### Командная тактика

**`seq_press`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Бегу на них! | I'm going at them! | `—` | 20552 |
| `t1` | Я вперёд! | I'm going in! | `—` | 20553 |
| `t1` | Не стой — за мной! | Don't stand. After me! | `—` | 20554 |
| `t1` | Держитесь! | Stay with me! | `—` | 20555 |
| `t1` | Прём! | We go! | `—` | 20556 |
| `t2` | Лезу | Going in | `—` | 20557 |
| `t2` | На них бегу | Running at them | `—` | 20558 |
| `t2` | Вперёд | Forward | `—` | 20559 |
| `t2` | Не ждите | Don't wait | `—` | 20560 |
| `t2` | Я первым | I'll go first | `—` | 20561 |
| `t4` | Лезу. | In. | `—` | 20562 |
| `t4` | Вперёд. | Forward. | `—` | 20563 |
| `t4` | На них. | At them. | `—` | 20564 |
| `t4` | Иду. | Going. | `—` | 20565 |
| `t4` | Я первый. | I'm first. | `—` | 20566 |

**`seq_flank`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Сбоку зайду! | I'll come from the side! | `—` | 20567 |
| `t1` | Не в лоб — в обход! | Not the front. Around! | `—` | 20568 |
| `t1` | Обойду их! | I'll go around them! | `—` | 20569 |
| `t1` | С края бегу! | Running the edge! | `—` | 20570 |
| `t1` | За мной сбоку! | With me, from the side! | `—` | 20571 |
| `t2` | Сбоку | The side | `—` | 20572 |
| `t2` | В обход | Around | `—` | 20573 |
| `t2` | Не в лоб | Not the front | `—` | 20574 |
| `t2` | С края | The edge | `—` | 20575 |
| `t2` | Обойду | Around them | `—` | 20576 |
| `t4` | Сбоку. | The side. | `—` | 20577 |
| `t4` | В обход. | Around. | `—` | 20578 |
| `t4` | Не в лоб. | Not the front. | `—` | 20579 |
| `t4` | С края. | The edge. | `—` | 20580 |
| `t4` | Обойду. | Around. | `—` | 20581 |
### Дальняя перебежка

**`move_long`**

| Лента | Русский | English | ctx | ID |
| --- | --- | --- | --- | ---: |
| `t1` | Далеко — бегу! | It's far. I'm running! | `—` | 20582 |
| `t1` | Сейчас добегу! | I'll get there! | `—` | 20583 |
| `t1` | Не стойте — я вперёд! | Don't wait. I'm going! | `—` | 20584 |
| `t1` | Глядите, через двор! | Watch. Across the yard! | `out` | 20585 |
| `t1` | Перебегаю! | Crossing now! | `—` | 20586 |
| `t2` | Рывок | Sprinting | `—` | 20587 |
| `t2` | Добегу | I'll get there | `—` | 20588 |
| `t2` | Перебегаю | Crossing | `—` | 20589 |
| `t2` | К ним иду | Closing in | `—` | 20590 |
| `t2` | Далеко, но надо | It's far. Still going | `—` | 20591 |
| `t4` | Рывок. | Sprint. | `—` | 20592 |
| `t4` | Добегу. | I'll get there. | `—` | 20593 |
| `t4` | Бегу. | Running. | `—` | 20594 |
| `t4` | Ближе. | Closer. | `—` | 20595 |
| `t4` | Далеко, бегу. | It's far. Going. | `—` | 20596 |
