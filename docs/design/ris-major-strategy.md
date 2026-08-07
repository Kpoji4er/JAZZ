# R.I.S. — «Стратегия Майора» / The Major's Strategy

Канон серии полевых записок о том, **как Майор управляет Легионом на стратегической карте**. Это отдельный слой разведки: брифы снабжения рассказывают, чем вооружены люди Майора; досье — кто именно сражается; «Стратегия Майора» — зачем его отряды выходят на дороги и откуда берутся.

- Название раздела и семейства писем: **Стратегия Майора** / **The Major's Strategy**.
- Тон: спокойная аналитическая записка полевого отдела R.I.S., основанная на наблюдениях, перехватах и дорожных донесениях.
- Подача: постепенно, только после события, которое игрок уже мог увидеть и осмыслить.
- Фактический источник: [`docs/wiki/legion-global-ai.md`](../wiki/legion-global-ai.md). Технический текст оттуда не переносится в письма дословно.

Это **design-канон текста и раскрытия**. Runtime-подключение, состояние и хуки
реализованы по `JAZZ-UI-RIS-002`; актуальное поведение описано в
[`ris-intelligence.md`](../technical/systems/ris-intelligence.md).

## Правила голоса

- R.I.S. объясняет наблюдаемую закономерность, а не игровую систему.
- Письмо начинается с факта или осторожного вывода, затем объясняет его значение и заканчивается практическим выводом.
- Допустимы формулировки «по нашим наблюдениям», «судя по дорожным донесениям», «похоже». Уверенность должна соответствовать тому, что R.I.S. действительно могла узнать.
- Русский и английский тексты передают один смысл, но пишутся самостоятельно. Дословная калька не нужна.
- В каждом письме — одна новая мысль. Никаких энциклопедических перечней.
- Не использовать учебный тон: «наведите курсор», «посмотрите иконку», «игра считает», «система создаёт».
- Не выводить игроку внутренние термины и идентификаторы: `Heat`, `QRF`, `REINFORCE`, `Global AI`, `tier`, `MapVar`, `role`, `spawn`, `tick`, имена preset-ов и профилей пакетов.
- Внутримировые слова допустимы и желательны: форт, округ, гарнизон, патруль, разведгруппа, конвой, штаб, донесение, пополнение.
- Ориентир по объёму: 60–100 слов по-русски или 75–120 по-английски, два коротких абзаца и подпись полевого отдела.

## Постепенное раскрытие

Первая записка объясняет общую картину. Остальные появляются только после соответствующего наблюдаемого события и могут открываться в разном порядке.

| № | Design id | Когда становится доступно | Что узнаёт игрок |
| ---: | --- | --- | --- |
| 0 | `strategy_network` | Welcome прочитан, затем произошёл первый контакт с Легионом или доставлен первый бриф снабжения | Легион устроен как сеть округов вокруг фортов, а не как одна армия |
| 1 | `strategy_roads` | Патруль или другой мобильный отряд Легиона впервые вошёл в подконтрольный игроку район либо был там встречен в бою | Смена власти не закрывает Легиону знакомые дороги |
| 2 | `strategy_villages` | Впервые замечен, перехвачен или ограблен сборщик налогов либо вербовщик | Деревни дают Легиону деньги и людей; рейсы повторяются |
| 3 | `strategy_eyes` | Разведгруппа заметила игрока и вернулась с донесением о его местоположении | Разведка опасна прежде всего тем, что наводит следующие отряды |
| 4 | `strategy_answer` | Впервые встречен местный отряд быстрого ответа или усиление границы | Ближайший форт отвечает на конкретную угрозу силами своего округа |
| 5 | `strategy_cargo` | Впервые замечен, перехвачен или разграблен конвой с деньгами, алмазами либо пополнением | Ценный груз стараются вести в обход позиций игрока |
| 6 | `strategy_wounded` | Впервые замечен отход поредевшего отряда на форт или ожидание пополнения | Отряды не исчезают: они восстанавливаются на базе и возвращаются |
| 7 | `strategy_red` | Впервые встречен тяжёлый отряд возмездия, отправленный штабом Майора | Помимо местной реакции существует редкий удар из центрального резерва |
| 8 | `strategy_sleep` | Впервые наблюдается оживление ранее малоподвижного материкового округа после получения помощи от штаба | Дальние форты набирают силу только после того, как до них доходит снабжение |

Правила очереди:

- Записка `strategy_network` всегда приходит первой.
- После неё остальные записки становятся независимыми: открывается только то, чему уже было свидетельство в игре.
- Все записки используют общую очередь R.I.S., но между двумя письмами «Стратегии Майора» проходит не меньше **24 campaign hours**.
- Если сработало несколько условий, письма становятся в очередь по времени первого наблюдения.
- При загрузке старого сохранения не отправлять накопившуюся серию. Разрешено поставить в очередь только одну уже заслуженную, но ещё не полученную записку; следующая появится не раньше отдельного интервала.
- В интерфейсе нет счётчика глав, пустых карточек и списка будущих тем. Игрок не должен видеть, сколько материалов ещё закрыто.

## Раздел на сайте

После доставки первой записки в «Оперативной сводке» появляется раздел **«Стратегия Майора» / “The Major's Strategy”**.

- В разделе видны только уже полученные материалы, в порядке доставки.
- Те же тексты остаются в почтовом архиве R.I.S.
- До первой записки раздел полностью скрыт.
- После открытия серии досье «Легион» может получить короткую ссылку: «Наблюдения за тем, как действует Майор, собраны в оперативной сводке.» / “Our observations of the Major's methods are collected in the bulletin.”

## Канонический текст писем

Заголовок используется как тема письма и название материала в сводке.

### 0 — Сеть опорных пунктов / A network of strongpoints

**RU — Стратегия Майора: сеть опорных пунктов**

По последним донесениям, Майор управляет Легионом не как одной армией. Он разделил страну на округа, и в центре каждого стоит форт. Оттуда выходят патрули, туда возвращаются потрёпанные отряды, там собирают деньги и новобранцев из окрестных поселений.

Уничтоженная колонна — серьёзная потеря, но не конец. Пока её опорный пункт действует, люди Майора со временем вернутся на дороги. Если хотите надолго успокоить район, следите не только за отрядами, но и за тем, куда они возвращаются.

— Полевой отдел R.I.S.

**EN — The Major's Strategy: a network of strongpoints**

Recent reports suggest that the Major does not run the Legion as one army. He has divided the country into districts, each centered on a fort. Patrols leave from it, battered units return to it, and money and recruits gathered from nearby settlements pass through its gates.

Destroying a column is a serious loss, but it does not end the system. As long as its strongpoint remains active, the Major's men will eventually return to the roads. If you want an area to stay quiet, watch where the units go home—not only where you meet them.

— R.I.S. Field Desk

### 1 — Смена флага не закрывает дорогу / A new flag does not close the road

**RU — Стратегия Майора: смена флага не закрывает дорогу**

Наши наблюдатели подтверждают: патрули Легиона продолжают пользоваться знакомыми маршрутами, даже когда территория уже перешла под ваш контроль. Особенно охотно они проходят там, где не видят постоянной охраны.

Для Майора дорога остаётся его дорогой, пока по ней можно пройти. Взять район и действительно успокоить его — разные задачи. Если маршрут для вас важен, одной смены флага недостаточно.

— Полевой отдел R.I.S.

**EN — The Major's Strategy: a new flag does not close the road**

Our observers confirm that Legion patrols continue to use familiar routes even after the ground has changed hands. They are especially willing to cross stretches where they see no permanent guard.

To the Major, a road is still his as long as his men can walk it. Taking an area and keeping it quiet are different jobs. If a route matters to you, changing the flag over it will not be enough.

— R.I.S. Field Desk

### 2 — Две дани / Two kinds of tribute

**RU — Стратегия Майора: две дани**

Легион требует от деревень не только деньги. Сборщики объезжают хозяйства и забирают выручку; по другим маршрутам идут вербовщики, которым нужны новые люди. Обоим обычно хватает небольшого эскорта: их задача — довезти собранное до форта, а не искать большой бой.

После рейса они возвращаются на базу, сдают деньги или приводят новобранцев, отдыхают и через некоторое время выходят снова. Перехваченный рейс лишит округ части дохода или пополнения, но сама система будет работать, пока форт держит окрестности.

— Полевой отдел R.I.S.

**EN — The Major's Strategy: two kinds of tribute**

The Legion demands more than money from the villages. Collectors make their rounds for cash, while recruiters follow other routes in search of new bodies. Both travel with small escorts: their job is to bring what they gather back to the fort, not to look for a major fight.

After each run they return to base, deliver the money or recruits, rest, and leave again. Intercepting one trip will cost the district money or manpower, but the system will continue as long as the fort controls the surrounding settlements.

— R.I.S. Field Desk

### 3 — Сначала — разведка / First, they look

**RU — Стратегия Майора: сначала — разведка**

Когда в округе становится неспокойно, Майор не всегда сразу отвечает силой. Сначала из форта выходит небольшая группа: проверить дороги, найти следы и понять, где вы остановились. Если она возвращается ни с чем, тревога постепенно стихает. Если замечает вас, местный командир получает уже не слухи, а координаты.

Такая группа опасна не числом. Её главное оружие — донесение, после которого другие отряды знают, куда идти. Если разведчики ушли после контакта, считайте, что время уже пошло.

— Полевой отдел R.I.S.

**EN — The Major's Strategy: first, they look**

When a district becomes unsettled, the Major does not always answer with force at once. A small party leaves the fort first—to check the roads, pick up a trail, and learn where you have stopped. If it returns empty-handed, the alarm gradually fades. If it sees you, the local commander receives coordinates instead of rumors.

The danger is not the size of the scouting party. Its real weapon is the report that tells the next unit where to go. If the scouts broke contact and headed home, assume the clock has already started.

— R.I.S. Field Desk

### 4 — Ответ ближайшего форта / The nearest fort answers

**RU — Стратегия Майора: ответ ближайшего форта**

Большинство срочных решений Майор оставляет местным командирам. Потерянная позиция или подтверждённое донесение заставляют ближайший форт укреплять подступы и высылать людей к месту угрозы.

Это не бесконечный резерв и не общее наступление. Такой ответ привязан к конкретной угрозе, а его размах зависит от людей и денег в данном округе. Если отдельная колонна уже движется в вашу сторону, исходите из того, что кто-то сообщил форту, где вас искать.

— Полевой отдел R.I.S.

**EN — The Major's Strategy: the nearest fort answers**

The Major leaves most urgent decisions to his local commanders. A lost position or a confirmed report prompts the nearest fort to reinforce its approaches and send men toward the threat.

This is not an endless reserve or a general offensive. The response is tied to a specific threat, and its size depends on the men and money available in that district. If a separate column is already moving your way, assume that someone has told the fort where to look.

— R.I.S. Field Desk

### 5 — Груз выбирает тихую дорогу / Cargo takes the quiet road

**RU — Стратегия Майора: груз выбирает тихую дорогу**

Боевые патрули могут идти прямо через подконтрольную вам территорию. Ценный груз ведут осторожнее. Конвои с деньгами, алмазами и пополнением стараются обходить ваши позиции, если остаётся другой путь.

Даже длинный крюк их не остановит. Но если все дороги проходят под вашими стволами, новый рейс могут вовсе не выпустить. Патруль готов рисковать встречей; груз ищет маршрут, на котором встречи не будет.

— Полевой отдел R.I.S.

**EN — The Major's Strategy: cargo takes the quiet road**

Combat patrols may cross ground under your control without hesitation. Valuable cargo is handled more carefully. Convoys carrying money, diamonds, or reinforcements will try to avoid your positions whenever another route remains open.

A long detour will not stop them. If every road passes under your guns, however, a new shipment may not leave at all. A patrol is prepared to risk contact; cargo looks for a route where contact never happens.

— R.I.S. Field Desk

### 6 — Они возвращаются / They come back

**RU — Стратегия Майора: они возвращаются**

Поредевший отряд Легиона не списывают после неудачного выхода. Если слишком много бойцов ранено или убито, он отходит к ближайшему форту, остаётся там до пополнения и лишь потом снова выходит на дорогу.

Поэтому затишье после удачной засады может оказаться временным. Знакомый патруль не исчез — он восстанавливает силы за стенами. Если хотите понять, действительно ли округ опустел, наблюдайте за дорогами, ведущими к форту.

— Полевой отдел R.I.S.

**EN — The Major's Strategy: they come back**

A depleted Legion unit is not written off after a failed mission. When too many of its men are wounded or dead, it falls back to the nearest fort, waits for replacements, and only then returns to the road.

The quiet after a successful ambush may therefore be temporary. A familiar patrol has not vanished; it is rebuilding behind the walls. If you want to know whether a district is truly empty, keep watching the roads that lead back to the fort.

— R.I.S. Field Desk

### 7 — Возмездие из штаба / Retribution from headquarters

**RU — Стратегия Майора: возмездие из штаба**

С большинством угроз разбираются ближайшие форты. Но когда потери и тревога накапливаются, донесения доходят до самого Майора. Тогда из его штаба выходит тяжёлая колонна — не для разведки и не для охраны дороги, а для возмездия.

Такие выходы редки, и именно поэтому важны. Они означают, что местных сил уже сочли недостаточными и Майор решил потратить собственный резерв. Такая тяжёлая колонна указывает не на ближайший форт, а на собственный резерв Майора.

— Полевой отдел R.I.S.

**EN — The Major's Strategy: retribution from headquarters**

The nearest forts handle most threats. When losses and alarm continue to mount, however, the reports eventually reach the Major himself. A heavy column then leaves his headquarters—not to scout or guard a road, but to exact retribution.

Such deployments are rare, which is precisely why they matter. They mean the local forces were judged insufficient and the Major chose to spend his own reserve. A column this heavy points beyond the nearest fort—to the Major's own reserve.

— R.I.S. Field Desk

### 8 — Не все округа просыпаются сразу / Not every district wakes at once

**RU — Стратегия Майора: не все округа просыпаются сразу**

Дальние форты Легиона живут не в одном ритме. Некоторые долго держатся на остатках: редко выводят новые отряды, берегут людей и почти не отвечают на тревогу. Это легко принять за слабость или нерешительность, но причина обычно проще — до округа ещё не дошла помощь из штаба.

После первой серьёзной поставки всё меняется. На дорогах появляются вербовщики и новые колонны, а местный командир начинает действовать увереннее. Если прежде тихий район внезапно пришёл в движение, вероятнее всего, до него наконец дотянулась линия снабжения.

— Полевой отдел R.I.S.

**EN — The Major's Strategy: not every district wakes at once**

The Legion's distant forts do not all move at the same pace. Some survive on what they have for a long time: they rarely send out new units, conserve their men, and make little response to trouble. It can look like weakness or indecision, but the cause is usually simpler—the district has not yet received help from headquarters.

The first serious delivery changes that. Recruiters and fresh columns appear on the roads, and the local commander begins to act with greater confidence. If a formerly quiet district suddenly comes alive, the Major's supply line has probably reached it.

— R.I.S. Field Desk

## Проверка текста

- [ ] Каждая записка раскрывает одну закономерность и опирается на событие, которое игрок мог наблюдать.
- [ ] В тексте нет внутренних терминов, чисел прогрессии, идентификаторов и упоминаний игрового интерфейса.
- [ ] Совет следует из разведданных и не звучит как подсказка из руководства.
- [ ] Русский текст естественен сам по себе; английский не копирует русскую фразу слово в слово.
- [ ] Оба языка сообщают одинаковые факты и одинаково обозначают степень уверенности.
- [ ] Факты соответствуют текущему поведению Legion Global AI.
- [ ] Письма не приходят серией за один день и не раскрывают названия будущих материалов.

## Runtime-контракт

- Семейство Email: `RIS_MajorStrategy_Network`, `Roads`, `Villages`, `Recon`,
  `Response`, `Cargo`, `Recovery`, `Retribution`, `Awakening`.
- Обнаруженные и доставленные материалы хранятся раздельно в `gv_JAZZ_RIS`.
- Observer читает существующие наблюдаемые сигналы Legion AI и не меняет решения,
  ресурсы или темп директора.
- Точные условия наблюдения, очередь, миграция старых сохранений и текущий статус
  acceptance зафиксированы в `JAZZ-UI-RIS-002` и технической документации.
