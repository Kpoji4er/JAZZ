from pathlib import Path

UNITS = Path(__file__).resolve().parents[2].parent / "jazz-units"
JAZZ = Path(__file__).resolve().parents[2]
ID1 = "890000000010900"
ID2 = "890000000010901"
HELP = '"<help>\n\n<practice>"'

RU_LINE = (
    f"{ID1},Практика: <xp> / <need>,Практика: <xp> / <need>,,jazz-units:Code/StatGainRework.lua\n"
    f"{ID2},{HELP},{HELP},,jazz-units:Code/StatGainRework.lua\n"
)
EN_LINE = (
    f"{ID1},Практика: <xp> / <need>,Practice: <xp> / <need>,,jazz-units:Code/StatGainRework.lua\n"
    f"{ID2},{HELP},{HELP},,jazz-units:Code/StatGainRework.lua\n"
)


def append(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if ID1 in text:
        print("skip", path)
        return
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block, encoding="utf-8")
    print("appended", path)


def main() -> None:
    append(UNITS / "Russian.csv", RU_LINE)
    append(UNITS / "English.csv", EN_LINE)
    for name in ("Russian.csv", "English.csv"):
        text = (JAZZ / name).read_text(encoding="utf-8")
        print(name, "id1", text.count(ID1), "id2", text.count(ID2))
        assert "<xp>" in text and "<need>" in text
        if name == "English.csv":
            assert "Practice: <xp> / <need>" in text


if __name__ == "__main__":
    main()
