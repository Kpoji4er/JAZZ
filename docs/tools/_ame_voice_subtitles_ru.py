"""Canonical Russian subtitles for the shared AME combat voice banks.

The English key is the phrase actually present in the donor audio.  Subtitles
must translate that phrase rather than invent a line for the gameplay event
that happened to reuse it.
"""

from __future__ import annotations


RU_BY_ENGLISH: dict[str, str] = {
    "Take that!": "Получай!",
    "Die!": "Умри!",
    "MEURS!": "Умри!",
    "I have no cover here!": "Здесь негде укрыться!",
    "You won't break our spirit.": "Нас вам не сломить.",
    "Huh? Enemies!": "Что? Враги!",
    "Alerte! Alerte!": "Тревога! Тревога!",
    "They are all over me!": "Они меня окружили!",
    "We will water the soil with the blood of you all!": "Мы напоим эту землю вашей кровью!",
    "You will pay, foreign dogs. Now it is us that will bring the pain.": (
        "Вы заплатите, чужеземные псы. Теперь боль причинять будем мы."
    ),
    "Uff, that hurt!": "Уф, больно!",
    "Damn, they are hard to get. We need to aim better.": (
        "Чёрт, по ним трудно попасть. Надо лучше целиться."
    ),
    "(heavy breath)": "(тяжёлое дыхание)",
    "Keeping my head down!": "Не высовываюсь!",
    "Take this!": "Получай!",
    "Suppressive fire!": "Огонь на подавление!",
    "(climbing)": "(взбирается)",
    "(jumping over something)": "(перепрыгивает через препятствие)",
    "(coughing)": "(кашляет)",
    "That was a beloved pet, you bastards.": "Это был любимый зверь, ублюдки.",
    "They have breached my position!": "Они прорвались на мою позицию!",
    "Watch out. We are taking heavy fire.": "Осторожно! Нас прижали огнём.",
    "Sound the alarm!": "Поднимайте тревогу!",
    "Alert! Man your stations!": "Тревога! Всем по местам!",
    "They have me in a pincer.": "Они берут меня в клещи.",
    "They are taking casualties!": "Они несут потери!",
    "Good! Keep it up!": "Хорошо! Так держать!",
    "Agh.": "Агх.",
    "Ouch.": "Ай.",
    "I'm hit!": "В меня попали!",
    "Good. Now they know our might.": "Хорошо. Теперь они знают нашу силу.",
    "Agh Ugh!": "Агх!..",
    "Hagh Agh!": "Ах!..",
    "Digging in!": "Занимаю оборону!",
    "At least, we won't have to clean out the wildlife after the battle.": (
        "По крайней мере, после боя не придётся отстреливать зверьё."
    ),
    "For all we have lost!": "За всех, кого мы потеряли!",
    "You will all pay!": "Вы все заплатите!",
    "I have no protection against the enemy's attacks!": "Мне нечем прикрыться от их огня!",
    "Fight harder!": "Сражайтесь отчаяннее!",
    "We are under attack!": "На нас напали!",
    "Enemies!": "Враги!",
    "They come from all sides!": "Они со всех сторон!",
    "We are winning!": "Мы побеждаем!",
    "I am proud of all of you.": "Я горжусь вами.",
    "We are doing well! Keep it up!": "У нас всё получается! Так держать!",
    "Laying low!": "Не высовываюсь!",
    "Let's see how you like this!": "Посмотрим, как вам это понравится!",
    "Huh?": "Что?",
    "You are nothing but butchers!": "Да вы просто мясники!",
}


def russian_subtitle(english: str, preset_id: str) -> str:
    """Return a natural subtitle matching the audible phrase."""

    if english == "Je suis blessé!":
        return "Я ранена!" if preset_id == "Jazz_AME_Female" else "Я ранен!"
    try:
        return RU_BY_ENGLISH[english]
    except KeyError as error:
        raise KeyError(
            f"missing AME Russian subtitle for {preset_id}: {english!r}"
        ) from error
