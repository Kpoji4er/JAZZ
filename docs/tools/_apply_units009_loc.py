from pathlib import Path

jazz = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
ID1 = "890000000010900"
ID2 = "890000000010901"
src = "Практика: <xp> / <need>"
en = "Practice: <xp> / <need>"
help_src = "<help>\n\n<practice>"


def q(s: str) -> str:
    return '"' + s.replace('"', '""') + '"'


def append(path: Path, text: str, needle: str) -> None:
    data = path.read_text(encoding="utf-8")
    if needle in data:
        print("skip", path.name)
        return
    if not data.endswith("\n"):
        data += "\n"
    path.write_text(data + text, encoding="utf-8")
    print("appended", path.name)


append(
    jazz / "Russian.csv",
    f"{ID1},{src},{src},,jazz-units:Code/StatGainRework.lua\n"
    f"{ID2},{q(help_src)},{q(help_src)},,jazz-units:Code/StatGainRework.lua\n",
    ID1,
)
append(
    jazz / "English.csv",
    f"{ID1},{src},{en},,jazz-units:Code/StatGainRework.lua\n"
    f"{ID2},{q(help_src)},{q(help_src)},,jazz-units:Code/StatGainRework.lua\n",
    ID1,
)
append(
    jazz / "Localization" / "Strings.csv",
    f"{ID1},{src},,{src},{en},russian-override;new-id,jazz-units:Code/StatGainRework.lua,jazz-units,jazz-units:Code/StatGainRework.lua,manual-translation-UNITS-009\n"
    f"{ID2},{q(help_src)},,{q(help_src)},{q(help_src)},russian-override;new-id,jazz-units:Code/StatGainRework.lua,jazz-units,jazz-units:Code/StatGainRework.lua,technical-copy\n",
    ID1,
)

em = jazz / "Localization" / "EnglishManual.csv"
em_txt = em.read_text(encoding="utf-8")
if ID1 not in em_txt:
    last_n = max(int(line.split(",", 1)[0]) for line in em_txt.splitlines()[1:] if line[:1].isdigit())
    if not em_txt.endswith("\n"):
        em_txt += "\n"
    em.write_text(
        em_txt
        + f"{last_n+1},{ID1},{src},{en},manual-translation-UNITS-009\n"
        + f"{last_n+2},{ID2},{q(help_src)},{q(help_src)},technical-copy\n",
        encoding="utf-8",
    )
    print("appended EnglishManual", last_n + 1)

rm = jazz / "Localization" / "RussianManual.csv"
rm_txt = rm.read_text(encoding="utf-8")
if ID1 not in rm_txt:
    last_n = max(int(line.split(",", 1)[0]) for line in rm_txt.splitlines()[1:] if line[:1].isdigit())
    if not rm_txt.endswith("\n"):
        rm_txt += "\n"
    rm.write_text(
        rm_txt
        + f"{last_n+1},{ID1},{src},{src},manual-translation-UNITS-009\n"
        + f"{last_n+2},{ID2},{q(help_src)},{q(help_src)},technical-copy\n",
        encoding="utf-8",
    )
    print("appended RussianManual", last_n + 1)
