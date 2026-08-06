# -*- coding: utf-8 -*-
"""Replace stub LegionTier Emails with R.I.S. welcome + Legion briefs; append loc; sync metadata."""
from pathlib import Path
import csv
import io
import re

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"

# Brief EN/RU bodies keyed by tier value
BRIEFS = {
    11: (
        "R.I.S. field note — Legion supply\n\n"
        "The Major is still emptying old warehouses. We are seeing PPSh-style submachine guns, Mosin rifles, MAT-49s and other wartime leftovers. Ammo is thin; armor is mostly wishful thinking.\n\n"
        "Early Legion patrols are poorly equipped — but there are a lot of them. Do not mistake rust for safety.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Майор всё ещё вычищает старые склады. На руках бойцов — ППШ, винтовки Мосина, MAT-49 и прочий военный хлам. Патронов мало; про броню лучше не шутить — её почти нет.\n\n"
        "Ранние патрули Легиона слабо экипированы — но их много. Не путайте ржавчину с безопасностью.\n\n"
        "— Recon Intelligence Services",
        "Major emptying warehouses: PPSh, Mosin, MAT-49",
        "Майор вычищает склады: ППШ, Мосин, MAT-49",
    ),
    12: (
        "R.I.S. field note — Legion supply\n\n"
        "Shipments look a little less desperate. Grease Guns, Sterlings and better pistols are mixing into the same old generation of arms — still nothing modern, but less scrap-metal roulette.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Поставки чуть менее нищие. В ту же «старую» волну оружия подмешиваются Grease Gun, Sterling и нормальные пистолеты — ещё не современность, но уже не сплошной хлам.\n\n"
        "— Recon Intelligence Services",
        "Wartime SMGs and better pistols in the mix",
        "Винтажные ПП и нормальные пистолеты",
    ),
    13: (
        "R.I.S. field note — Legion supply\n\n"
        "Early-issue kit is peaking: PPS-43s, Colt 1911s, service pistols that actually fire when asked. Still generation-one gear — but the Major has stopped handing out pure museum pieces as standard.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Ранняя экипировка выходит на потолок: ППС-43, Colt 1911, служебные пистолеты, которые стреляют с первого раза. Это всё ещё первое поколение — но Майор уже не раздаёт сплошной музейный хлам как норму.\n\n"
        "— Recon Intelligence Services",
        "PPS-43 and service pistols — early kit peaks",
        "ППС-43 и служебные пистолеты — пик ранней волны",
    ),
    21: (
        "R.I.S. field note — Legion supply\n\n"
        "Second wave. Compact SMGs — UZI, MAC-10 — and Hi-Power pistols are showing up. Roughnecks have started carrying pipe bombs. This is no longer a scavenger parade.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Вторая волна. Компактные ПП — UZI, MAC-10 — и пистолеты Hi-Power. У отморозков появляются самодельные бомбы. Это уже не парад мародёров.\n\n"
        "— Recon Intelligence Services",
        "Second wave: UZI, MAC-10, pipe bombs",
        "Вторая волна: UZI, MAC-10, самодельные бомбы",
    ),
    22: (
        "R.I.S. field note — Legion supply\n\n"
        "Carbines and battle rifles in the crates: CAR-15, FAMAS, M14-pattern guns. Someone is buying for a real fight, not a roadblock shakedown.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "В ящиках — карабины и боевые винтовки: CAR-15, FAMAS, стволы семейства M14. Кто-то закупается под настоящий бой, а не под поборы на блокпосте.\n\n"
        "— Recon Intelligence Services",
        "CAR-15, FAMAS, M14-pattern rifles arriving",
        "Идут CAR-15, FAMAS, винтовки M14",
    ),
    23: (
        "R.I.S. field note — Legion supply\n\n"
        "Kalashnikovs. AK-47, AKM, the occasional Bizon. The Legion is finally looking like an army that owns rifles, not a militia that borrows them.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Калашниковы. АК-47, АКМ, иногда «Бизон». Легион наконец выглядит как сила, у которой есть автоматы, а не как ополчение, которое их одалживает.\n\n"
        "— Recon Intelligence Services",
        "AKs in volume — Legion looks like an army",
        "АК пачками — Легион уже похож на армию",
    ),
    24: (
        "R.I.S. field note — Legion supply\n\n"
        "Western SMGs and carbines: MP5 family, M4A1, serious sidearms. Expect tighter fire and fewer jams when you push a fortified position.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Западные ПП и карабины: семейство MP5, M4A1, серьёзные пистолеты. На укреплённых позициях ждите более плотный и надёжный огонь.\n\n"
        "— Recon Intelligence Services",
        "MP5 family and M4A1 in Legion hands",
        "У Легиона MP5 и M4A1",
    ),
    25: (
        "R.I.S. field note — Legion supply\n\n"
        "Late second-wave spike: G36c, VSS, modern pistols. Quality jumped again — treat veteran squads as properly armed, not upgraded scavengers.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Поздний скачок второй волны: G36c, ВСС, современные пистолеты. Качество снова выросло — ветеранов стоит считать нормально вооружёнными, а не «чуть лучшими мародёрами».\n\n"
        "— Recon Intelligence Services",
        "G36c, VSS — late second-wave spike",
        "G36c, ВСС — поздний скачок второй волны",
    ),
    31: (
        "R.I.S. field note — Legion supply\n\n"
        "Third wave. Sig 550 rifles, M60E4 machine guns, better optics. The Major is issuing kit meant to hold ground against professionals.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Третья волна. Винтовки Sig 550, пулемёты M60E4, нормальная оптика. Майор выдаёт снаряжение, которым можно держать позицию против профессионалов.\n\n"
        "— Recon Intelligence Services",
        "Third wave: Sig 550, M60E4, real optics",
        "Третья волна: Sig 550, M60E4, нормальная оптика",
    ),
    32: (
        "R.I.S. field note — Legion supply\n\n"
        "Precision and special weapons: custom Sigs, SVU, Arctic Warfare rifles. Marksmen and assault elements are no longer an afterthought.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Точность и «особые» стволы: кастомные Sig, СВУ, Arctic Warfare. Снайперы и штурмовые группы — уже не случайность в отряде.\n\n"
        "— Recon Intelligence Services",
        "Custom Sigs, SVU, Arctic Warfare",
        "Кастомные Sig, СВУ, Arctic Warfare",
    ),
    33: (
        "R.I.S. field note — Legion supply\n\n"
        "Top shelf. Barrett anti-materiel rifles, PSG-1 precision guns, AA-12 shotguns. If you see this kit in the field, assume the Major wants someone dead — permanently.\n\n"
        "— Recon Intelligence Services",
        "Заметка R.I.S. — снабжение Легиона\n\n"
        "Верхняя полка. Barrett, PSG-1, дробовики AA-12. Если такое в поле — считайте, что Майор хочет кого-то убрать всерьёз и надолго.\n\n"
        "— Recon Intelligence Services",
        "Barrett, PSG-1, AA-12 — top-shelf threats",
        "Barrett, PSG-1, AA-12 — угроза верхней полки",
    ),
}

# Loc IDs: 6920 tab, 6921-23 welcome, 6930+ briefs (title/sender/body per tier)
LOC_BASE = 890000000006920


def lua_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def email_block(eid: str, body_id: int, body_en: str, sender_id: int, sender: str, title_id: int, title_en: str, *, repeatable=False, delay=False) -> str:
    rep = "\n\t\t\trepeatable = true," if repeatable else ""
    delay_line = "\n\t\t\tdelayAfterCombat = false," if not delay else ""
    return (
        f"\t\tPlaceObj('ModItemEmail', {{\n"
        f"\t\t\tbody = T({body_id}, --[[ModItemEmail {eid} body]] \"{lua_escape(body_en)}\"),"
        f"{delay_line}{rep}\n"
        f"\t\t\tgroup = \"Default\",\n"
        f"\t\t\tid = \"{eid}\",\n"
        f"\t\t\tlabel = \"Important\",\n"
        f"\t\t\tsender = T({sender_id}, --[[ModItemEmail {eid} sender]] \"{lua_escape(sender)}\"),\n"
        f"\t\t\ttitle = T({title_id}, --[[ModItemEmail {eid} title]] \"{lua_escape(title_en)}\"),\n"
        f"\t\t}}),"
    )


def build_emails_lua() -> str:
    blocks = []
    # welcome
    w_sender = "R.I.S. <desk@ris-intel.net>"
    w_title = "R.I.S. — complimentary intelligence subscription"
    w_body = (
        "Commander,\n\n"
        "Recon Intelligence Services has activated your complimentary field subscription for this campaign. "
        "We will send assessments when Legion supply quality shifts, and later host dossiers and after-action notes on our PDA site.\n\n"
        "Read this message to unlock the R.I.S. browser tab.\n\n"
        "— Recon Intelligence Services"
    )
    blocks.append(
        email_block(
            "RIS_Welcome",
            890000000006923,
            w_body,
            890000000006921,
            w_sender,
            890000000006922,
            w_title,
            delay=False,
        )
    )
    sender = "R.I.S. <legion-desk@ris-intel.net>"
    for i, tier in enumerate(sorted(BRIEFS.keys())):
        en_body, _ru_body, en_title, _ru_title = BRIEFS[tier]
        # ids: 6930 + i*3 title, +1 sender reuse, +2 body — use 6940+i*3
        base = 890000000006940 + i * 3
        title_id, sender_id, body_id = base, 890000000006939, base + 2
        blocks.append(
            email_block(
                f"RIS_LegionBrief_{tier}",
                body_id,
                en_body,
                sender_id,
                sender,
                title_id,
                en_title,
                delay=False,
            )
        )
    return "\n".join(blocks)


def patch_items():
    text = ITEMS.read_text(encoding="utf-8")
    # Remove old LegionTier1..5 and any prior AME/RIS block we re-insert carefully:
    # Replace from first AME_Welcome or LegionTier1 through LegionTier5 with AME emails (keep) + RIS emails.
    # Find AME_Welcome start if present, else LegionTier1.
    start_m = re.search(r"\t\tPlaceObj\('ModItemEmail', \{\n\t\t\tbody = T\(890000000006907,", text)
    if not start_m:
        start_m = re.search(r"\t\tPlaceObj\('ModItemEmail', \{\n\t\t\tbody = T\(890000000001015,", text)
    if not start_m:
        raise SystemExit("email block start not found")
    # end after LegionTier5 closing
    end_m = re.search(
        r"\t\tPlaceObj\('ModItemEmail', \{\n\t\t\tbody = T\(890000000001014,.*?title = T\(890000000000110,.*?\"LegionTier5\"\),\n\t\t\}\),",
        text,
        re.S,
    )
    # Also match if LegionTier already removed — end before BobbyRay quest
    if not end_m:
        end_m = re.search(r"\t\tPlaceObj\('ModItemQuestsDef', \{\n\t\t\tAuthor = \"Diogo\",", text)
        end_pos = end_m.start() if end_m else None
        # remove from start to end_pos, but keep AME emails if they're before Legion
        raise SystemExit("LegionTier5 end not found — manual check")
    end_pos = end_m.end()

    # Keep AME emails: extract if present
    ame_chunk = ""
    ame_m = re.search(
        r"(\t\tPlaceObj\('ModItemEmail', \{\n\t\t\tbody = T\(890000000006907,.*?\t\t\}\),\n"
        r"\t\tPlaceObj\('ModItemEmail', \{\n\t\t\tbody = T\(890000000006910,.*?\t\t\}\),)\n",
        text[start_m.start() : end_pos],
        re.S,
    )
    if ame_m:
        ame_chunk = ame_m.group(1) + "\n"

    new_block = ame_chunk + build_emails_lua() + "\n"
    text = text[: start_m.start()] + new_block + text[end_pos:]
    ITEMS.write_text(text, encoding="utf-8")
    print("items.lua: replaced LegionTier stubs with RIS emails")


def patch_metadata():
    text = META.read_text(encoding="utf-8")
    if "Code/System_RIS_Mail.lua" not in text:
        text = text.replace(
            '"Code/System_AME_Mail.lua",\n',
            '"Code/System_AME_Mail.lua",\n\t\t"Code/System_RIS_Mail.lua",\n',
        )
    # Replace LegionTier1-5 resource presets with RIS ones
    old = re.search(
        r"\t\tPlaceObj\('ModResourcePreset', \{\n\t\t\t'Class', \"Email\",\n\t\t\t'Id', \"AME_Welcome\",.*?'Id', \"LegionTier5\",\n\t\t\t'ClassDisplayName', \"Email\",\n\t\t\}\),",
        text,
        re.S,
    )
    ids = ["AME_Welcome", "AME_ListingUpdate", "RIS_Welcome"] + [f"RIS_LegionBrief_{t}" for t in sorted(BRIEFS)]
    parts = []
    for eid in ids:
        parts.append(
            "\t\tPlaceObj('ModResourcePreset', {\n"
            f"\t\t\t'Class', \"Email\",\n"
            f"\t\t\t'Id', \"{eid}\",\n"
            f"\t\t\t'ClassDisplayName', \"Email\",\n"
            f"\t\t}}),"
        )
    block = "\n".join(parts)
    if old:
        text = text[: old.start()] + block + text[old.end() :]
    else:
        # replace LegionTier1..5 only
        text2 = re.sub(
            r"\t\tPlaceObj\('ModResourcePreset', \{\n\t\t\t'Class', \"Email\",\n\t\t\t'Id', \"LegionTier[1-5]\",\n\t\t\t'ClassDisplayName', \"Email\",\n\t\t\}\),\n?",
            "",
            text,
        )
        if "RIS_Welcome" not in text2:
            text2 = text2.replace(
                "\t\tPlaceObj('ModResourcePreset', {\n\t\t\t'Class', \"Email\",\n\t\t\t'Id', \"AME_ListingUpdate\",\n\t\t\t'ClassDisplayName', \"Email\",\n\t\t}),",
                "\t\tPlaceObj('ModResourcePreset', {\n\t\t\t'Class', \"Email\",\n\t\t\t'Id', \"AME_ListingUpdate\",\n\t\t\t'ClassDisplayName', \"Email\",\n\t\t}),\n" + block.replace("AME_Welcome", "SKIP").replace("AME_ListingUpdate", "SKIP2"),
            )
            # messy — simpler rewrite of email resource section
        text = text2
        # Insert RIS resources after AME_ListingUpdate
        needle = (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            "\t\t\t'Class', \"Email\",\n"
            "\t\t\t'Id', \"AME_ListingUpdate\",\n"
            "\t\t\t'ClassDisplayName', \"Email\",\n"
            "\t\t}),"
        )
        ris_only = "\n".join(
            parts[2:]
        )  # skip AME
        if needle in text and "RIS_Welcome" not in text:
            text = text.replace(needle, needle + "\n" + ris_only)
    META.write_text(text, encoding="utf-8")
    print("metadata.lua: code + Email resources updated")


def load_csv(path: Path):
    raw = path.read_text(encoding="utf-8-sig")
    sep = None
    body = raw
    if raw.startswith("sep="):
        nl = raw.find("\n")
        sep = raw[:nl]
        body = raw[nl + 1 :]
    rows = list(csv.reader(io.StringIO(body)))
    return sep, rows


def save_csv(path: Path, sep, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for row in rows:
        w.writerow(row)
    out = buf.getvalue()
    if sep:
        out = sep + "\n" + out
    if not out.endswith("\n"):
        out += "\n"
    path.write_text(out, encoding="utf-8")


def upsert_loc():
    rows_def = []
    # tab + welcome
    rows_def.append(("890000000006920", "R.I.S.", "R.I.S.", "R.I.S."))
    rows_def.append(
        (
            "890000000006921",
            "R.I.S. <desk@ris-intel.net>",
            "R.I.S. <desk@ris-intel.net>",
            "R.I.S. <desk@ris-intel.net>",
        )
    )
    rows_def.append(
        (
            "890000000006922",
            "R.I.S. — complimentary intelligence subscription",
            "R.I.S. — бесплатная подписка разведки",
            "R.I.S. — complimentary intelligence subscription",
        )
    )
    w_body_en = (
        "Commander,\n\n"
        "Recon Intelligence Services has activated your complimentary field subscription for this campaign. "
        "We will send assessments when Legion supply quality shifts, and later host dossiers and after-action notes on our PDA site.\n\n"
        "Read this message to unlock the R.I.S. browser tab.\n\n"
        "— Recon Intelligence Services"
    )
    w_body_ru = (
        "Командир,\n\n"
        "Recon Intelligence Services активировал вашу бесплатную полевую подписку в рамках этой кампании. "
        "Мы будем присылать оценки, когда изменится качество снабжения Легиона, а позже — вести досье и after-action сводки на сайте в КПК.\n\n"
        "Прочитайте это письмо, чтобы открыть вкладку R.I.S.\n\n"
        "— Recon Intelligence Services"
    )
    rows_def.append(("890000000006923", w_body_en, w_body_ru, w_body_en))
    rows_def.append(
        (
            "890000000006939",
            "R.I.S. <legion-desk@ris-intel.net>",
            "R.I.S. <legion-desk@ris-intel.net>",
            "R.I.S. <legion-desk@ris-intel.net>",
        )
    )
    for i, tier in enumerate(sorted(BRIEFS.keys())):
        en_body, ru_body, en_title, ru_title = BRIEFS[tier]
        base = 890000000006940 + i * 3
        rows_def.append((str(base), en_title, ru_title, en_title))
        rows_def.append((str(base + 2), en_body, ru_body, en_body))

    ids = {r[0] for r in rows_def}
    for path, kind in ((ROOT / "Russian.csv", "ru"), (ROOT / "English.csv", "en")):
        sep, rows = load_csv(path)
        cleaned = [r for r in rows if r and r[0] not in ids]
        for eid, en_src, ru, en in rows_def:
            if kind == "ru":
                cleaned.append([eid, en_src, ru, "", "JAZZ-UI-RIS-001"])
            else:
                cleaned.append([eid, ru, en, "", "JAZZ-UI-RIS-001"])
        save_csv(path, sep, cleaned)
        print(f"{path.name}: RIS loc upserted {len(rows_def)}")


def main():
    patch_items()
    patch_metadata()
    upsert_loc()


if __name__ == "__main__":
    main()
