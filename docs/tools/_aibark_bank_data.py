# -*- coding: utf-8 -*-
"""Canon lines for combat AI barks. Five (ru, en) per (event, band).

Emit markdown: python docs/tools/_aibark_bank_data.py
Check: python docs/tools/_check_aibark_bank.py
"""
from __future__ import annotations

from pathlib import Path

# Tags (AND): line plays only if every tag is true. No tags = always eligible.
#   in     — target / impact is indoors (AICheckIndoors / unit.indoors)
#   out    — that point is outdoors
#   into   — speaker outdoors AND target indoors (window / door / into the house)
#   high   — speaker slab Z > target
#   houses — map has buildings (JazzAI_ShouldOccupyBuildings)
# Events order_buildings / order_heights are already gated by the directive picker;
# their place-nouns stay untagged.
TAGS = frozenset({"in", "out", "into", "high", "houses"})

# event, band, list of 5 (ru, en, tags)
# band: boss | officer | t1 | t2 | t4
BANK: list[tuple[str, str, list[tuple[str, str, frozenset[str]]]]] = []


def add(event: str, band: str, lines: list[tuple]) -> None:
    norm: list[tuple[str, str, frozenset[str]]] = []
    for item in lines:
        if len(item) == 2:
            ru, en = item
            tags: frozenset[str] = frozenset()
        elif len(item) == 3:
            ru, en, raw = item
            tags = frozenset(str(raw).split())
            bad = tags - TAGS
            assert not bad, (event, band, ru, bad)
        else:
            raise AssertionError((event, band, item))
        norm.append((ru, en, tags))
    assert len(norm) == 5, (event, band, len(norm))
    BANK.append((event, band, norm))


# --- Orders: all CMD-001 directives. Bark on CHANGE only. ---
add("order_hold", "boss", [
    ("Стоим, не прём!", "Stay put! Don't push!"),
    ("Ни с места!", "Nobody moves!"),
    ("Двор наш — сидим", "Yard's ours. Sit.", "out"),
    ("Не лезем пока", "Don't go in yet"),
    ("Пусть сами приходят", "Let them come to us"),
])
add("order_hold", "officer", [
    ("Стоим.", "Hold."),
    ("Не лезем.", "Don't go in."),
    ("Здесь.", "Here."),
    ("Ждём.", "We wait."),
    ("Сидим.", "Sit tight."),
])
add("order_push", "boss", [
    ("Шевелитесь, падлы!", "Move, you dogs!"),
    ("Бейте уже, живо!", "Hit 'em already!"),
    ("Прём на них!", "We go at them!"),
    ("Не стойте — бейте!", "Don't stand. Hit!"),
    ("Давите, пока тёплые!", "Hit them while they're up!"),
])
add("order_push", "officer", [
    ("Вперёд, сказал.", "I said move."),
    ("На них. Сейчас.", "Now. Into them."),
    ("Прём.", "We go."),
    ("Сейчас на них.", "On them. Now."),
    ("Не ждите.", "Don't wait."),
])
add("order_envelop", "boss", [
    ("Зайдите сзади, не в лоб!", "Around back, not the front!"),
    ("По дворам гоните!", "Through the yards!", "out"),
    ("С боков зайдите!", "Come in from the sides!"),
    ("Не в улицу — сзади!", "Not the street. Behind!", "out"),
    ("Обходите хаты!", "Around the houses!", "houses"),
])
add("order_envelop", "officer", [
    ("Сзади зайдите.", "Around back."),
    ("Не толпой.", "Not in a bunch."),
    ("С краю.", "From the edge."),
    ("Обойдите.", "Go around."),
    ("Не в лоб.", "Not straight in."),
])
add("order_fallback", "boss", [
    ("Валите назад!", "Get back!"),
    ("Прячьтесь, сомнут!", "Down or you're next!"),
    ("Сматываемся!", "We're pulling out!"),
    ("Назад, кто цел!", "Back, if you're whole!"),
    ("Живыми надо!", "We need you alive!"),
])
add("order_fallback", "officer", [
    ("Сваливаем.", "We're out."),
    ("Назад. Живыми.", "Back. Alive."),
    ("Уходим.", "Leaving."),
    ("Назад.", "Back."),
    ("Хватит.", "Enough."),
])
add("order_focus", "boss", [
    ("Всех на <name>!", "All of you — <name>!"),
    ("<name> — и больше никого", "<name>. Nobody else."),
    ("На <name>, шмалите!", "On <name>. Shoot!"),
    ("<name> снимите!", "Drop <name>!"),
    ("Только <name>, я сказал!", "Only <name>, I said!"),
])
add("order_focus", "officer", [
    ("<name>. Всех.", "<name>. Everyone."),
    ("Только <name>.", "Only <name>."),
    ("<name>.", "<name>."),
    ("Огонь — <name>.", "Fire. <name>."),
    ("<name>. Снимите.", "<name>. Drop him."),
])
add("order_focus_anon", "boss", [
    ("Вот этого бейте!", "That one. Hit him!"),
    ("Не шмалите по всем!", "Stop spraying!"),
    ("Одного, всех на него!", "One man. All of you!"),
    ("Этот, только этот!", "This one. Only this!"),
    ("Не мазать — одного!", "Don't spray. One!"),
])
add("order_focus_anon", "officer", [
    ("Этого. Всех.", "That one. All of you."),
    ("Не по всем.", "Don't split it."),
    ("Одного.", "One of them."),
    ("Этот.", "This one."),
    ("Не мазать.", "Don't spray."),
])
add("order_buildings", "boss", [
    ("В хаты, из окон!", "Inside! Windows!"),
    ("С двора — в дом!", "Off the yard. Inside!"),
    ("По хатам!", "Into the houses!"),
    ("Бейте из окон!", "From the windows!"),
    ("Не во дворе — внутрь!", "Not the yard. Inside!"),
])
add("order_buildings", "officer", [
    ("В хаты.", "Inside."),
    ("Из окон.", "From the windows."),
    ("В дома.", "Indoors."),
    ("С двора прочь.", "Off the yard."),
    ("Окна.", "Windows."),
])
add("order_heights", "boss", [
    ("На крышу, кто живой!", "Up the roof!"),
    ("Сверху кладите!", "Drop them from up there!"),
    ("На холм, давайте!", "Up the hill!"),
    ("Крыши наши!", "Roofs are ours!"),
    ("Наверх, давайте!", "Up, come on!"),
])
add("order_heights", "officer", [
    ("Наверх.", "Up."),
    ("С холма.", "From the hill."),
    ("Крыши.", "Roofs."),
    ("Выше.", "Higher."),
    ("Сверху.", "From above."),
])
add("order_cover", "boss", [
    ("На брюхо, живо!", "Belly down!"),
    ("Ложись, пуль полно!", "Down, bullets flying!"),
    ("К земле!", "To the dirt!"),
    ("За угол!", "Get behind!"),
    ("Прячьте башки!", "Heads down!"),
])
add("order_cover", "officer", [
    ("На брюхо.", "Down."),
    ("Не маячь.", "Don't pop up."),
    ("К земле.", "To the dirt."),
    ("Ложись.", "Get down."),
    ("Не светиться.", "Don't show."),
])
add("order_lowvis", "boss", [
    ("В тёмное не лезьте!", "Don't walk into that dark!"),
    ("Стоим. Сами вылезут", "Stay. Let 'em show."),
    ("Не в черноту!", "Not into the black!"),
    ("Ждём, пусть покажутся", "Wait. Let them show."),
    ("Тихо стоим", "Quiet. We stay."),
])
add("order_lowvis", "officer", [
    ("Стоим.", "Stay put."),
    ("Без героев.", "No heroes."),
    ("Ждём света.", "Wait for light."),
    ("Не лезьте.", "Don't go in."),
    ("Тихо.", "Quiet."),
])
add("order_hidden", "boss", [
    ("В тень, тихо!", "Into the dark. Quiet!"),
    ("Затаились!", "Stay hidden!"),
    ("Не светиться!", "Don't show yourselves!"),
    ("В траву, ложись!", "In the grass. Down!", "out"),
    ("Тс-с. Сгинь.", "Shh. Vanish."),
])
add("order_hidden", "officer", [
    ("В тень.", "Into cover."),
    ("Тихо.", "Quiet."),
    ("Не светиться.", "Don't show."),
    ("Затаились.", "Stay hidden."),
    ("Сгинь.", "Vanish."),
])

# --- Archetype switch (once per combat per unit, on change) ---
add("arch_panic", "t1", [
    ("Не надо…", "Please—"),
    ("Я домой, я домой", "I wanna go home"),
    ("Мама…", "Mama—"),
    ("Не стреляйте—", "Don't shoot—"),
    ("Я не хочу", "I don't want this"),
])
add("arch_panic", "t2", [
    ("Нас сомнут!", "They'll walk over us!"),
    ("Не стоим, валим", "We're not staying. Go!"),
    ("Это мясорубка", "This is a butcher shop"),
    ("Нас сложат", "They'll drop us"),
    ("Пора сматываться", "Time to go"),
])
add("arch_panic", "t4", [
    ("Чёрт…", "Damn it—"),
    ("Не сейчас", "Not now"),
    ("Плохо", "Bad"),
    ("Не сюда", "Not here"),
    ("Хватит", "Enough"),
])
add("arch_desert", "t1", [
    ("Жить охота", "I wanna live"),
    ("Сами деритесь", "Fight it yourselves"),
    ("Я сматываюсь", "I'm taking off"),
    ("Мне ещё жить", "I still wanna live"),
    ("Хватит с меня крови", "I've seen enough blood"),
])
add("arch_desert", "t2", [
    ("Хватит с меня", "I'm through"),
    ("Я своё отпахал", "I've done my share"),
    ("Ищите других", "Find someone else"),
    ("Я ухожу", "I'm leaving"),
    ("Дальше без меня", "You go on without me"),
])
add("arch_desert", "t4", [
    ("Ищите дураков", "Find another fool"),
    ("Мне тут ловить нечего", "Nothing left for me here"),
    ("Контракт кончен", "Job's done"),
    ("Я выхожу", "I'm out"),
    ("Не мой бой", "Not my fight"),
])
add("arch_berserk", "t1", [
    ("Убью! Убью!", "I'll kill you!"),
    ("А-а! Идите сюда!", "Aaah! Come here!"),
    ("Всех порву!", "I'll tear you all!"),
    ("Кровь! Ещё!", "Blood! More!"),
    ("Не остановить!", "Can't stop me!"),
])
add("arch_berserk", "t2", [
    ("Всех кладу!", "I'll drop you all!"),
    ("Хватит прятаться!", "Stop hiding!"),
    ("Иду на вас!", "Coming for you!"),
    ("Рубить!", "Cut them down!"),
    ("Никого живым!", "Nobody lives!"),
])
add("arch_berserk", "t4", [
    ("Всех.", "All of you."),
    ("Иду.", "Coming."),
    ("Дорежу.", "I'll finish it."),
    ("Хватит ждать.", "Enough waiting."),
    ("Вперёд.", "Forward."),
])
add("arch_medic", "t1", [
    ("Тихо ты", "Easy"),
    ("Кровь уйму, лежи", "I'll stop the blood"),
    ("Сейчас перевяжу", "I'll bind it"),
    ("Не дёргайся, живой", "Don't jerk. You're alive"),
    ("Лежи, я рядом", "Stay down. I'm here"),
])
add("arch_medic", "t2", [
    ("Не дёргайся", "Don't jerk"),
    ("Заткнись — проживёшь", "Shut up and you'll live"),
    ("Бинтую, не ори", "Binding. Don't yell"),
    ("Жить будешь", "You'll live"),
    ("Держись, зашью", "Hold on. I'll close it"),
])
add("arch_medic", "t4", [
    ("Лежи.", "Lie still."),
    ("Не мешай.", "Don't get in the way."),
    ("Тихо.", "Quiet."),
    ("Живой. Лежи.", "Alive. Stay down."),
    ("Руки.", "Hands."),
])
add("arch_melee", "t1", [
    ("Порежу!", "I'll cut you!"),
    ("Ближе, ближе", "Closer—"),
    ("Нож, нож!", "Knife, knife!"),
    ("В морду схожу!", "I'm coming in!"),
    ("Патронов жалко — режу", "Save the rounds. Cutting"),
])
add("arch_melee", "t2", [
    ("Вплотную проще", "Easier up close"),
    ("Иду на нож", "On the knife"),
    ("В упор", "Point blank"),
    ("Хватит стрелять — режем", "Enough shooting. Cut"),
    ("Иду вплотную", "Going in close"),
])
add("arch_melee", "t4", [
    ("Вплотную.", "Close in."),
    ("Хватит стрелять.", "Enough shooting."),
    ("Нож.", "Knife."),
    ("В упор.", "Point blank."),
    ("Ближе.", "Closer."),
])

# --- Grenades by aoeType ---
add("nade_flare", "t1", [
    ("Гори, зараза!", "Burn, damn you!"),
    ("Рожи на свет!", "Faces into the light!"),
    ("Свет, свет!", "Light, light!"),
    ("Гори им в глаза!", "Burn in their eyes!"),
    ("Чтоб видно было!", "So we can see!"),
])
add("nade_flare", "t2", [
    ("Свет им в глаза", "In their eyes"),
    ("Вылезайте, гады", "Come out, you bastards"),
    ("Подсветил", "Lit them"),
    ("Теперь видно", "Now we see"),
    ("Не прячьтесь", "No more hiding"),
])
add("nade_flare", "t4", [
    ("Свет.", "Light."),
    ("Видно будет.", "They'll show."),
    ("Гори.", "Burn."),
    ("В глаза.", "Eyes."),
    ("Вижу.", "I see."),
])
add("nade_smoke", "t1", [
    ("В дым!", "Into the smoke!"),
    ("Сейчас не увидят", "They won't see"),
    ("Прячемся в дыму", "We hide in the smoke"),
    ("Прячьтесь в дым!", "Hide in the smoke!"),
    ("Чтоб не видели!", "So they don't see!"),
])
add("nade_smoke", "t2", [
    ("Дымом закрою", "I'll cover us"),
    ("Через дым прём", "Through the smoke"),
    ("Закрой двор", "Cover the yard", "out"),
    ("Под дым идём", "We go under the smoke"),
    ("Не видят — прём", "They can't see. Go"),
])
add("nade_smoke", "t4", [
    ("Дым — и сразу", "Smoke. Then we go."),
    ("Закрыл. Прём.", "Covered. Go."),
    ("Дым.", "Smoke."),
    ("Закрой.", "Cover it."),
    ("Идём.", "We go."),
])
add("nade_frag", "t1", [
    ("Нате, гады!", "Here, you bastards!"),
    ("Держите!", "Catch!"),
    ("Вам туда!", "That's for you!"),
    ("Ловите!", "Catch this!"),
    ("Сейчас бахнет!", "This one's gonna bang!"),
])
add("nade_frag", "t2", [
    ("Летит!", "It's in the air!"),
    ("Ложись — не ты", "Down — not you"),
    ("Под ноги им", "At their feet"),
    ("Двор чищу", "Clearing the yard", "out"),
    ("В кучу им", "Into the bunch"),
])
add("nade_frag", "t4", [
    ("Под ноги.", "At their feet."),
    ("Лови.", "For them."),
    ("Туда.", "There."),
    ("Чищу.", "Clearing."),
    ("Бах.", "Bang."),
])
add("nade_fire", "t1", [
    ("Горите!", "Burn!"),
    ("Жар им!", "Heat for them!"),
    ("Хату палю!", "I'm torching the house!", "in"),
    ("Огонь, огонь!", "Fire, fire!"),
    ("Пусть жарятся!", "Let them fry!"),
])
add("nade_fire", "t2", [
    ("Жгу двор", "Torching the yard", "out"),
    ("Огнём их!", "Fire on them!"),
    ("Пусть бегут", "Let them run"),
    ("Хату зажигаю", "Lighting the house", "in"),
    ("Жарко будет", "It'll get hot"),
])
add("nade_fire", "t4", [
    ("Жги.", "Burn it."),
    ("Огонь.", "Fire."),
    ("Хату.", "The house.", "in"),
    ("Жарко.", "Heat."),
    ("Гори.", "Burn."),
])
add("nade_gas", "t1", [
    ("Пусть давятся!", "Let them choke!"),
    ("Гадость им!", "Filth for them!"),
    ("Кашляйте, гады!", "Cough, you bastards!"),
    ("Дышите этим!", "Breathe that!"),
    ("Сейчас заплюются!", "They'll spit blood!"),
])
add("nade_gas", "t2", [
    ("Пусть хлебают", "Let them drink it"),
    ("Двор порчу", "Spoiling the yard", "out"),
    ("Не дышать им", "They don't get air"),
    ("Выкурят сами", "They'll cough themselves out"),
    ("Гадкость полетела", "The filth's in the air"),
])
add("nade_gas", "t4", [
    ("Дышите.", "Breathe."),
    ("Во двор.", "The yard.", "out"),
    ("Кашляй.", "Cough."),
    ("Гадкость.", "Filth."),
    ("Всё.", "That's it."),
])

# --- Weapon SWITCH (class change). Not every shot. ---
add("wpn_rifle", "t1", [
    ("Длинный беру!", "Grabbing the long one!"),
    ("Длинный в руки!", "Long one in hand!"),
    ("Короткий не тянет", "The short one's useless"),
    ("Меняю на дальний!", "Switching to the far one!"),
    ("Беру ствол!", "Grabbing a gun!"),
])
add("wpn_rifle", "t2", [
    ("Длинный", "Long gun"),
    ("Длинный обратно", "Long one back"),
    ("С этого дальше бью", "This one reaches farther"),
    ("Меняю ствол", "Switching guns"),
    ("Этот дальше", "This one reaches"),
])
add("wpn_rifle", "t4", [
    ("Длинный.", "Long one."),
    ("Дальше.", "Farther."),
    ("Вернул.", "Back on."),
    ("Ствол.", "Gun."),
    ("Беру.", "Taking it."),
])
add("wpn_shotgun", "t1", [
    ("Дробь беру!", "Grabbing buckshot!"),
    ("Короткий злой беру!", "Grabbing the short mean one!"),
    ("В хату бью!", "Into the house!", "into"),
    ("Меняю — в упор!", "Switching. Up close!"),
    ("Дверь сниму!", "I'll take the door!", "into"),
])
add("wpn_shotgun", "t2", [
    ("Дробь", "Buckshot"),
    ("В упор бью", "Up close now"),
    ("Короткий ставлю", "Putting the short one on"),
    ("В хату бью", "Into the house", "into"),
    ("Вблизи лучше", "Better up close"),
])
add("wpn_shotgun", "t4", [
    ("Дробь.", "Buckshot."),
    ("В упор.", "Up close."),
    ("Короткий.", "Short one."),
    ("В хату.", "Into the house.", "in"),
    ("Ставлю.", "Putting it on."),
])
add("wpn_mg", "t1", [
    ("Ленту ставлю!", "Setting the belt!"),
    ("Ленту в руки!", "Belt in hand!"),
    ("Длинный злой беру!", "Grabbing the long mean one!"),
    ("Меняю — улицу крою!", "Switching. Street's mine!", "out"),
    ("Всех держу!", "I'll hold them all!"),
])
add("wpn_mg", "t2", [
    ("Ленту ставлю", "Setting the belt"),
    ("Длинный ставлю", "Setting the long one"),
    ("Улицу крою", "This covers the street", "out"),
    ("Двор держу", "This holds the yard", "out"),
    ("Меняю на длинный", "Switching to the long one"),
])
add("wpn_mg", "t4", [
    ("Лента.", "Belt."),
    ("Длинный.", "The long one."),
    ("Улицу.", "The street.", "out"),
    ("Двор мой.", "The yard's mine.", "out"),
    ("Моя.", "Mine."),
])
add("wpn_sidearm", "t1", [
    ("Короткий из кармана!", "Short one from the pocket!"),
    ("Короткий в руки!", "Short one in hand!"),
    ("Длинный заклинило—", "Long one's jammed—"),
    ("Меняю на быстрый!", "Switching to the quick one!"),
    ("С коротким в хату!", "Short one into the house!", "into"),
])
add("wpn_sidearm", "t2", [
    ("Короткий достаю", "Pulling the short one"),
    ("Из кармана", "From the pocket"),
    ("Так быстрее", "Faster this way"),
    ("Вплотную — короткий", "Short one up close"),
    ("Длинный потом", "Long one later"),
])
add("wpn_sidearm", "t4", [
    ("Короткий.", "Short one."),
    ("Из кармана.", "Pocket."),
    ("Быстро.", "Quick."),
    ("Вплотную.", "Close."),
    ("Достал.", "Got it."),
])
add("wpn_gl", "t1", [
    ("Коротыш беру!", "Grabbing the short one!"),
    ("Коротыш в руки!", "Short one in hand!"),
    ("В окно бью!", "Through the window!", "into"),
    ("Меняю — в дверь!", "Switching. At the door!", "into"),
    ("По хате бью!", "Hitting the house!", "in"),
])
add("wpn_gl", "t2", [
    ("Коротыш ставлю", "Putting the short one on"),
    ("Под ствол ставлю", "Under the barrel now"),
    ("В окно бью", "This one at the window", "into"),
    ("Дверь вынесу", "I'll take the door", "into"),
    ("По хате бью", "Hitting the house", "in"),
])
add("wpn_gl", "t4", [
    ("Коротыш.", "Short one."),
    ("Под ствол.", "Under the barrel."),
    ("В окно.", "Window.", "into"),
    ("В дверь.", "Door.", "into"),
    ("В хату.", "House.", "in"),
])
add("wpn_rocket", "t1", [
    ("Трубу беру!", "Grabbing the pipe!"),
    ("Большую в руки!", "The big one in hand!"),
    ("Отойди, жахнет!", "Back, this bangs!"),
    ("Меняю — хату снесу!", "Switching. House comes down!", "in"),
    ("С плеча эту!", "This one off the shoulder!"),
])
add("wpn_rocket", "t2", [
    ("Трубу беру", "Grabbing the pipe"),
    ("Трубу поднимаю", "Pipe's going up"),
    ("Тяжёлый ставлю", "Putting the heavy one on"),
    ("Эту хату снесу", "That house comes down", "in"),
    ("С плеча", "Off the shoulder"),
])
add("wpn_rocket", "t4", [
    ("Труба.", "Pipe."),
    ("Тяжёлый.", "Heavy."),
    ("Снесу.", "Coming down."),
    ("Хату.", "The house.", "in"),
    ("С плеча.", "Shoulder."),
])
add("wpn_sniper", "t1", [
    ("Дальний беру!", "Grabbing the long eye!"),
    ("Дальний в руки!", "Long one in hand!"),
    ("Лягу и бью!", "I'll go prone and shoot!"),
    ("Меняю — с холма!", "Switching. From the hill!", "high"),
    ("Не дыши — целюсь!", "Don't breathe. Aiming!"),
])
add("wpn_sniper", "t2", [
    ("Дальний ставлю", "Putting the long one on"),
    ("С холма бью", "This one from the hill", "high"),
    ("Лежу, бью", "Down. Shooting"),
    ("Достаю с края", "I can reach from here"),
    ("Один — и тишина", "One. Then quiet"),
])
add("wpn_sniper", "t4", [
    ("Дальний.", "Long one."),
    ("С холма.", "The hill.", "high"),
    ("Лежу.", "Down."),
    ("Один.", "One."),
    ("Тишина.", "Quiet."),
])
add("wpn_melee", "t1", [
    ("Нож достаю!", "Knife's out!"),
    ("Ствол бросил — режу!", "Dropped the gun. Cutting!"),
    ("Железо в руки!", "Iron in hand!"),
    ("Патронов нет — нож!", "No rounds. Knife!"),
    ("Меняю — ближе!", "Switching. Closer!"),
])
add("wpn_melee", "t2", [
    ("Иду на нож", "On the knife"),
    ("Ствол в сторону", "Gun aside"),
    ("Железо", "Iron"),
    ("Вплотную режу", "This one up close"),
    ("Резать", "Cut"),
])
add("wpn_melee", "t4", [
    ("Нож.", "Knife."),
    ("Ствол.", "Gun down."),
    ("Железо.", "Iron."),
    ("Вплотную.", "Close."),
    ("Резать.", "Cut."),
])

# MG bipod deploy is not a class switch.
add("mg_setup", "t1", [
    ("Я тут сяду", "I'm sitting here"),
    ("С угла накрою!", "From this corner!"),
    ("Ставлю, прикройте", "Setting up. Cover me"),
    ("Сюда сяду, улица моя", "Sitting here. Street's mine", "out"),
    ("Ноги, тренога!", "Legs down!"),
])
add("mg_setup", "t2", [
    ("Улицу отсюда крою", "I'll take the street", "out"),
    ("Сюда ставлю", "Goes here"),
    ("С угла", "From the corner"),
    ("Двор закрою", "I'll shut the yard", "out"),
    ("Сел — улица моя", "Sat. Street's mine", "out"),
])
add("mg_setup", "t4", [
    ("Улица моя.", "This street's mine.", "out"),
    ("Сюда.", "Here."),
    ("С угла.", "Corner."),
    ("Сел.", "Sat."),
    ("Двор мой.", "Yard's mine.", "out"),
])

# --- CMD-002: Late press (Push execution). Not the officer order. ---
add("seq_press", "t1", [
    ("Бегу на них!", "I'm going at them!"),
    ("Я вперёд!", "I'm going in!"),
    ("Не стой — за мной!", "Don't stand. After me!"),
    ("Держитесь!", "Stay with me!"),
    ("Прём!", "We go!"),
])
add("seq_press", "t2", [
    ("Лезу", "Going in"),
    ("На них бегу", "Running at them"),
    ("Вперёд", "Forward"),
    ("Не ждите", "Don't wait"),
    ("Я первым", "I'll go first"),
])
add("seq_press", "t4", [
    ("Лезу.", "In."),
    ("Вперёд.", "Forward."),
    ("На них.", "At them."),
    ("Иду.", "Going."),
    ("Я первый.", "I'm first."),
])

# Envelop / probe / NeedFlank — going around, not the officer order.
add("seq_flank", "t1", [
    ("Сбоку зайду!", "I'll come from the side!"),
    ("Не в лоб — в обход!", "Not the front. Around!"),
    ("Обойду их!", "I'll go around them!"),
    ("С края бегу!", "Running the edge!"),
    ("За мной сбоку!", "With me, from the side!"),
])
add("seq_flank", "t2", [
    ("Сбоку", "The side"),
    ("В обход", "Around"),
    ("Не в лоб", "Not the front"),
    ("С края", "The edge"),
    ("Обойду", "Around them"),
])
add("seq_flank", "t4", [
    ("Сбоку.", "The side."),
    ("В обход.", "Around."),
    ("Не в лоб.", "Not the front."),
    ("С края.", "The edge."),
    ("Обойду.", "Around."),
])

# Dest ≥12 tiles (AI-007 recontact / long path). Not FallBack.
add("move_long", "t1", [
    ("Далеко — бегу!", "It's far. I'm running!"),
    ("Сейчас добегу!", "I'll get there!"),
    ("Не стойте — я вперёд!", "Don't wait. I'm going!"),
    ("Глядите, через двор!", "Watch. Across the yard!", "out"),
    ("Перебегаю!", "Crossing now!"),
])
add("move_long", "t2", [
    ("Рывок", "Sprinting"),
    ("Добегу", "I'll get there"),
    ("Перебегаю", "Crossing"),
    ("К ним иду", "Closing in"),
    ("Далеко, но надо", "It's far. Still going"),
])
add("move_long", "t4", [
    ("Рывок.", "Sprint."),
    ("Добегу.", "I'll get there."),
    ("Бегу.", "Running."),
    ("Ближе.", "Closer."),
    ("Далеко, бегу.", "It's far. Going."),
])

ID0 = 20157
MD = Path(__file__).resolve().parents[1] / "design" / "combat-ai-barks.md"
MARK = "<!-- aibark-bank -->"

SECTION = {
    "order_": "### Приказ",
    "arch_": "### Смена архетипа",
    "nade_": "### Граната",
    "wpn_": "### Смена оружия",
    "mg_": "### Пулемёт: сошки",
    "seq_": "### Командная тактика",
    "move_": "### Дальняя перебежка",
}


def iter_rows():
    n = ID0
    for event, band, lines in BANK:
        for ru, en, tags in lines:
            yield event, band, ru, en, tags, n
            n += 1


def row_count() -> int:
    return sum(len(lines) for _, _, lines in BANK)


def emit_md() -> None:
    chunks: list[str] = []
    last_prefix = ""
    last_event = ""
    for event, band, ru, en, tags, n in iter_rows():
        prefix = "mg_" if event.startswith("mg_") else event.split("_")[0] + "_"
        if prefix != last_prefix:
            chunks.append(SECTION.get(prefix, f"### {event}"))
            last_prefix = prefix
        if event != last_event:
            chunks.append(f"\n**`{event}`**\n")
            chunks.append("| Лента | Русский | English | ctx | ID |")
            chunks.append("| --- | --- | --- | --- | ---: |")
            last_event = event
        ru_c = ru.replace("|", "\\|")
        en_c = en.replace("|", "\\|")
        ctx = ",".join(sorted(tags)) if tags else "—"
        chunks.append(f"| `{band}` | {ru_c} | {en_c} | `{ctx}` | {n} |")
    body = "\n".join(chunks) + "\n"
    text = MD.read_text(encoding="utf-8")
    if MARK not in text:
        raise SystemExit(f"missing {MARK} in {MD}")
    pre = text.split(MARK, 1)[0] + MARK + "\n\n"
    MD.write_text(pre + body, encoding="utf-8")


if __name__ == "__main__":
    emit_md()
    print(f"groups={len(BANK)} rows={row_count()} id={ID0}..{ID0 + row_count() - 1} wrote {MD}")
