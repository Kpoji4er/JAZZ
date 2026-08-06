# -*- coding: utf-8 -*-
"""Apply lore-name canon + truncated VoiceResponse repairs into units + runtime CSV.

Canon (owner 2026-08-06): Grandier / Грандье, Cavalier / Кавалье, Khalif / Халиф.

Usage (jazz/):
  python docs/tools/_apply_trunc_vr_and_lore_names.py
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"

# loc_id -> (ru, en)
REPAIRS: dict[str, tuple[str, str]] = {
    # lore names
    "890000000006628": ("Взломщица с Халифа", "Burglar from Khalif"),
    "890000000006650": ("Саймон Грандье", "Simon Grandier"),
    "890000000006657": ("Грандье недоступен.", "Grandier is unavailable."),
    # handoff truncated VR
    "890000000006347": (
        "Потрясающе, Биф! Ну разве удивительно, что ты мне нравишься... я хочу сказать, что мне так нравится с тобой работать!",
        "Amazing, Biff! Is it any wonder I like you... I mean, that I like working with you so much!",
    ),
    "890000000006372": (
        "Говорит Кирк Стивенсон. Известный по кличке Статик. Раньше я говорил только кличку, и все думали, что у меня плохой видеотелефон.",
        "This is Kirk Stevenson, better known as Static. I used to go only by my nickname, and everyone thought I had a bad video phone.",
    ),
    "890000000006556": (
        "Оуууу... Ох, господи, мне так последний раз было, когда я попробовал починить папашин шредер, знаешь.",
        "Ohhh... Oh, God, the last time I felt like this was when I tried to fix dad's shredder, you know.",
    ),
    "890000000006430": (
        "Я не доверяю Игги. Он был враг, стал друг. Что он будет завтра? Нельзя быть уверенным.",
        "I don't trust Iggy. He was an enemy, became a friend. What will he be tomorrow? You can never be sure.",
    ),
    "890000000006598": (
        "Эй, слушай и запоминай. Сдоба - пижонка, каких свет не видывал, и я не обещаю, что сумею удержать свою винтовку, пока она так лачивается. Нервишки не в порядке, понимаешь?",
        "Listen and remember. Buns is the biggest poser I've ever seen, and I don't promise I can keep my rifle off her while she's posing like that. Nerves aren't good, you know?",
    ),
    # additional XLSX completions
    "890000000006334": (
        "А-а-а, наш маленький сладенький Бифи хочет свою сладенькую бутылочку? Ой, не могу, ну что за котеночек! Дать бы ему по заднице.",
        "Aww, does sweet little Biffy want his sweet little bottle? Oh, I can't—what a kitten! Someone ought to spank him.",
    ),
    "890000000006341": (
        "На мгновение мне показалось, что я - среди ангелов. Теперь я вижу, что по-прежнему пребываю в преисподней. Мои страдания безграничны!",
        "For a moment I thought I was among angels. Now I see I'm still in hell. My suffering knows no bounds!",
    ),
    "890000000006382": (
        "Ларри стал какой-то не такой. Совсем не наш чувак. Когда-то он был крутым пацаном, а сейчас... Чмо какое-то.",
        "Larry's changed. He's not one of us anymore. Used to be a cool guy, and now... what a loser.",
    ),
    "890000000006383": (
        "Ларри свойский чувак. Вот вроде, не думает головой, и вдруг, раз, и у него получается.",
        "Larry's a cool guy. Looks like he never thinks, then—bam!—somehow he pulls it off.",
    ),
    "890000000006557": (
        "Я в порядке, потому что, типа, удары по голове до меня не доходят. В смысле, до вреда не доводят.",
        "I'm fine, 'cause, like, blows to the head don't get through to me. I mean, they don't do any real harm.",
    ),
    "890000000006562": (
        "Если я раз поймаю этого комуняку Ивана - не в форме, я хочу сказать, - он у меня весь будет красный с синим, русский, твою мать!",
        "If I ever catch that commie Ivan—out of uniform, I mean—he'll be red and blue all over, you Russian bastard!",
    ),
    "890000000006568": (
        "Похоже, я умираю... Я вижу яркий свет... о, боже, скажи мне, что это просто спецэффекты.",
        "Looks like I'm dying... I see a bright light... Oh God, tell me it's just special effects.",
    ),
    # STT completions (NEED_SOURCE)
    "890000000006454": (
        "С этой Фло таким как я невозможно работать. Она не идет мне на встречу. Я готов ее просто пристрелить.",
        "I can't work with Flo. She won't meet me halfway. I'm ready to just shoot her.",
    ),
    "890000000006520": (
        "Плохи мои дела... Не думаю, что теперь смогу отомстить. Передайте моей жене: мне жаль, что так вышло с нашим сыном. Умоляю, чтобы она меня простила.",
        "I'm in bad shape... I don't think I'll get my revenge now. Tell my wife: I'm sorry about what happened to our son. I beg her to forgive me.",
    ),
    "890000000006490": (
        "Нечего меня за нос водить. Ларри взялся за старое. Наркоман, а мне с ним работать?",
        "Don't jerk me around. Larry's using again. A junkie—and I'm supposed to work with him?",
    ),
}


def load_csv(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    prefix = ""
    if text.startswith("sep="):
        i = text.find("\n")
        prefix = text[: i + 1]
        body = text[i + 1 :]
    else:
        body = text
    return prefix, list(csv.reader(io.StringIO(body)))


def write_csv(path: Path, prefix: str, rows) -> None:
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    for row in rows:
        w.writerow(row)
    path.write_text(prefix + out.getvalue(), encoding="utf-8-sig")


def upsert_runtime(en_rows, ru_rows, loc_id: str, ru: str, en: str) -> None:
    def apply(rows, *, is_en: bool) -> None:
        for i, r in enumerate(rows):
            if not r or r[0] != loc_id:
                continue
            # preserve source path in last known column if present
            src = ""
            empty = ""
            if len(r) >= 5:
                empty = r[3]
                src = r[4]
            elif len(r) >= 4:
                empty = r[3]
            if is_en:
                rows[i] = [loc_id, ru, en, empty, src] if src or empty else [loc_id, ru, en, "", ""]
            else:
                rows[i] = [loc_id, ru, ru, empty, src] if src or empty else [loc_id, ru, ru, "", ""]
            # trim trailing empties to match style loosely — keep 5 cols if src existed
            if src:
                rows[i] = [loc_id, ru, en if is_en else ru, empty, src]
            return
        # append
        row = [loc_id, ru, en if is_en else ru, "", "jazz-units:items.lua:VoiceResponse"]
        rows.append(row)

    apply(en_rows, is_en=True)
    apply(ru_rows, is_en=False)


def lua_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def patch_t_strings_in_file(path: Path, repairs: dict[str, tuple[str, str]]) -> int:
    text = path.read_text(encoding="utf-8")
    n = 0
    for loc_id, (ru, _en) in repairs.items():
        # JA3: T(id, --[[comment]] "text")  OR  T(id, "text")
        pat = re.compile(
            rf'(T\({loc_id},\s*(?:--\[\[[^\]]*\]\]\s*)?")((?:\\.|[^"\\])*)("\))'
        )

        def sub(m: re.Match, ru: str = ru) -> str:
            nonlocal n
            old_plain = (
                m.group(2)
                .replace("\\n", "\n")
                .replace('\\"', '"')
                .replace("\\\\", "\\")
            )
            if old_plain == ru:
                return m.group(0)
            n += 1
            return f"{m.group(1)}{lua_escape(ru)}{m.group(3)}"

        text, _count = pat.subn(sub, text)
    if n:
        path.write_text(text, encoding="utf-8")
    return n


def patch_manual(path: Path, *, is_en: bool) -> int:
    if not path.exists():
        return 0
    prefix, rows = load_csv(path)
    changed = 0
    for i, r in enumerate(rows):
        if len(r) < 4:
            continue
        # common: seq, id, ru, en/ru, note
        loc_id = r[1] if r[1] in REPAIRS else (r[0] if r[0] in REPAIRS else None)
        id_col = 1 if r[1] in REPAIRS else (0 if r[0] in REPAIRS else None)
        if loc_id is None or id_col is None:
            continue
        ru, en = REPAIRS[loc_id]
        if id_col + 2 >= len(r):
            continue
        r[id_col + 1] = ru
        r[id_col + 2] = en if is_en else ru
        rows[i] = r
        changed += 1
    if changed:
        write_csv(path, prefix, rows)
    return changed


def main() -> int:
    en_prefix, en_rows = load_csv(JAZZ / "English.csv")
    ru_prefix, ru_rows = load_csv(JAZZ / "Russian.csv")
    for loc_id, (ru, en) in REPAIRS.items():
        upsert_runtime(en_rows, ru_rows, loc_id, ru, en)
    write_csv(JAZZ / "English.csv", en_prefix, en_rows)
    write_csv(JAZZ / "Russian.csv", ru_prefix, ru_rows)
    print(f"runtime CSV: {len(REPAIRS)} ids")

    targets = [UNITS / "items.lua"]
    targets.extend(sorted((UNITS / "UnitData").glob("Jazz_*.lua")))
    total = 0
    for p in targets:
        if not p.exists():
            continue
        n = patch_t_strings_in_file(p, REPAIRS)
        if n:
            print(f"  {p.relative_to(UNITS)}: {n}")
            total += n
    print(f"embedded T(): {total}")

    print(
        "manual EN:",
        patch_manual(JAZZ / "Localization/EnglishManual.csv", is_en=True),
    )
    print(
        "manual RU:",
        patch_manual(JAZZ / "Localization/RussianManual.csv", is_en=False),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
