#!/usr/bin/env python3
"""Apply savannah AME chrome to System_AME_Browser_Template.lua (safe, ASCII-only)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Code" / "System_AME_Browser_Template.lua"

MARK = "Mod/e6L4ECj/Icons/PDA/AME_Mark.png"
BANNER = "Mod/e6L4ECj/Icons/PDA/AME_BannerPad.png"
BACKDROP = "Mod/e6L4ECj/Icons/PDA/AME_PdaBackdrop.png"


def main() -> None:
    t = SRC.read_text(encoding="utf-8")
    if "AME_Mark.png" in t:
        print("already themed?")
        return

    # 1) Full-bleed backdrop: keep vanilla pda_background but tint + swap image to AME
    t = t.replace(
        """\t\tPlaceObj('XTemplateWindow', {
\t\t\t'comment', \"bkg frame\",
\t\t\t'__class', \"XImage\",
\t\t\t'Margins', box(-50, -1, -50, 0),
\t\t\t'Dock', \"box\",
\t\t\t'Image', \"UI/PDA/pda_background\",
\t\t\t'ImageFit', \"stretch\",
\t\t}),""",
        f"""\t\tPlaceObj('XTemplateWindow', {{
\t\t\t'comment', \"bkg frame savannah\",
\t\t\t'__class', \"XImage\",
\t\t\t'Margins', box(-50, -1, -50, 0),
\t\t\t'Dock', \"box\",
\t\t\t'Image', \"{BACKDROP}\",
\t\t\t'ImageFit', \"stretch\",
\t\t}}),
\t\tPlaceObj('XTemplateWindow', {{
\t\t\t'comment', \"warm OS grain\",
\t\t\t'__class', \"XImage\",
\t\t\t'Margins', box(-50, -1, -50, 0),
\t\t\t'Dock', \"box\",
\t\t\t'Transparency', 160,
\t\t\t'Image', \"UI/PDA/pda_background\",
\t\t\t'ImageFit', \"stretch\",
\t\t\t'ImageColor', RGBA(210, 168, 96, 255),
\t\t}}),""",
        1,
    )

    # 2) Filter header rail tint
    t = t.replace(
        """\t\t\t\t\tPlaceObj('XTemplateWindow', {
\t\t\t\t\t\t'comment', \"bg\",
\t\t\t\t\t\t'__class', \"XFrame\",
\t\t\t\t\t\t'Dock', \"box\",
\t\t\t\t\t\t'Image', \"UI/PDA/os_header\",
\t\t\t\t\t\t'FrameBox', box(3, 5, 3, 5),
\t\t\t\t\t}),""",
        """\t\t\t\t\tPlaceObj('XTemplateWindow', {
\t\t\t\t\t\t'comment', \"bg khaki\",
\t\t\t\t\t\t'__class', \"XFrame\",
\t\t\t\t\t\t'Dock', \"box\",
\t\t\t\t\t\t'Image', \"UI/PDA/os_header\",
\t\t\t\t\t\t'FrameBox', box(3, 5, 3, 5),
\t\t\t\t\t\t'ImageColor', RGBA(168, 128, 72, 255),
\t\t\t\t\t}),""",
        1,
    )

    # 3) Filter button default ImageColor + selected tint in SetSelected
    t = t.replace(
        """\t\t\t\t\t\t\t'Image', \"UI/PDA/os_header_disable\",
\t\t\t\t\t\t\t'FrameBox', box(3, 5, 3, 5),
\t\t\t\t\t\t\t'SqueezeX', true,""",
        """\t\t\t\t\t\t\t'Image', \"UI/PDA/os_header_disable\",
\t\t\t\t\t\t\t'FrameBox', box(3, 5, 3, 5),
\t\t\t\t\t\t\t'ImageColor', RGBA(148, 110, 58, 255),
\t\t\t\t\t\t\t'SqueezeX', true,""",
        1,
    )
    t = t.replace(
        """\t\t\t\t\t\t\t\t\tself:SetImage(img)
\t\t\t\t\t\t\t\t\trawset(self, \"selected\", selected)""",
        """\t\t\t\t\t\t\t\t\tself:SetImage(img)
\t\t\t\t\t\t\t\t\tself:SetImageColor(selected and RGBA(196, 148, 72, 255) or RGBA(148, 110, 58, 255))
\t\t\t\t\t\t\t\t\trawset(self, \"selected\", selected)""",
        1,
    )

    # 4) HazOS -> AME mark
    t = t.replace(
        """\t\t\t\tPlaceObj('XTemplateWindow', {
\t\t\t\t\t'__class', \"XImage\",
\t\t\t\t\t'Margins', box(0, 0, 15, 0),
\t\t\t\t\t'HAlign', \"right\",
\t\t\t\t\t'VAlign', \"center\",
\t\t\t\t\t'Image', \"UI/PDA/HazOS\",
\t\t\t\t}),""",
        f"""\t\t\t\tPlaceObj('XTemplateWindow', {{
\t\t\t\t\t'comment', \"AME mark\",
\t\t\t\t\t'__class', \"XImage\",
\t\t\t\t\t'Margins', box(0, 0, 12, 0),
\t\t\t\t\t'HAlign', \"right\",
\t\t\t\t\t'VAlign', \"center\",
\t\t\t\t\t'MinHeight', 64,
\t\t\t\t\t'MaxHeight', 72,
\t\t\t\t\t'Image', \"{MARK}\",
\t\t\t\t\t'ImageFit', \"height\",
\t\t\t\t}}),""",
        1,
    )

    # 5) Main content bg tint (first os_background after content comment)
    t = t.replace(
        """\t\t\t\tPlaceObj('XTemplateWindow', {
\t\t\t\t\t'comment', \"bg\",
\t\t\t\t\t'__class', \"XFrame\",
\t\t\t\t\t'Dock', \"box\",
\t\t\t\t\t'Image', \"UI/PDA/os_background\",
\t\t\t\t\t'FrameBox', box(3, 3, 3, 3),
\t\t\t\t}),""",
        """\t\t\t\tPlaceObj('XTemplateWindow', {
\t\t\t\t\t'comment', \"bg dusty\",
\t\t\t\t\t'__class', \"XFrame\",
\t\t\t\t\t'Dock', \"box\",
\t\t\t\t\t'Image', \"UI/PDA/os_background\",
\t\t\t\t\t'FrameBox', box(3, 3, 3, 3),
\t\t\t\t\t'ImageColor', RGBA(186, 150, 92, 255),
\t\t\t\t}),""",
        1,
    )

    # 6) Left list inner bg
    t = t.replace(
        """\t\t\t\t\t\t\tPlaceObj('XTemplateWindow', {
\t\t\t\t\t\t\t\t'comment', \"bg\",
\t\t\t\t\t\t\t\t'__class', \"XFrame\",
\t\t\t\t\t\t\t\t'Dock', \"box\",
\t\t\t\t\t\t\t\t'Image', \"UI/PDA/os_background_2\",
\t\t\t\t\t\t\t\t'FrameBox', box(3, 3, 3, 3),
\t\t\t\t\t\t\t}),""",
        """\t\t\t\t\t\t\tPlaceObj('XTemplateWindow', {
\t\t\t\t\t\t\t\t'comment', \"bg\",
\t\t\t\t\t\t\t\t'__class', \"XFrame\",
\t\t\t\t\t\t\t\t'Dock', \"box\",
\t\t\t\t\t\t\t\t'Image', \"UI/PDA/os_background_2\",
\t\t\t\t\t\t\t\t'FrameBox', box(3, 3, 3, 3),
\t\t\t\t\t\t\t\t'ImageColor', RGBA(172, 132, 74, 255),
\t\t\t\t\t\t\t}),""",
        1,
    )

    # 7) Replace AIM banner with AME brand strip
    t = t.replace(
        """\t\t\t\t\t\t\t\tPlaceObj('XTemplateTemplate', {
\t\t\t\t\t\t\t\t\t'__template', \"PDAAIMBrowserBanner\",
\t\t\t\t\t\t\t\t}),""",
        f"""\t\t\t\t\t\t\t\tPlaceObj('XTemplateWindow', {{
\t\t\t\t\t\t\t\t\t'comment', \"AME brand strip\",
\t\t\t\t\t\t\t\t\t'__class', \"XImage\",
\t\t\t\t\t\t\t\t\t'HAlign', \"left\",
\t\t\t\t\t\t\t\t\t'VAlign', \"top\",
\t\t\t\t\t\t\t\t\t'MinWidth', 260,
\t\t\t\t\t\t\t\t\t'MinHeight', 46,
\t\t\t\t\t\t\t\t\t'MaxHeight', 46,
\t\t\t\t\t\t\t\t\t'Image', \"{BANNER}\",
\t\t\t\t\t\t\t\t\t'ImageFit', \"stretch\",
\t\t\t\t\t\t\t\t}}),""",
        1,
    )

    # 8) Merc detail panel bg (second os_background without comment dusty)
    # Tint remaining plain os_background FrameBox closes that lack ImageColor
    lines = t.splitlines()
    out = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        if (
            lines[i].strip() == "'Image', \"UI/PDA/os_background\","
            or lines[i].strip() == "'Image', \"UI/PDA/os_background_2\","
        ):
            # next non-empty should be FrameBox; if no ImageColor after, add
            window = "\n".join(lines[i : i + 5])
            if "ImageColor" not in window and i + 1 < len(lines) and "FrameBox" in lines[i + 1]:
                out.append(lines[i + 1])
                tabs = lines[i + 1][: len(lines[i + 1]) - len(lines[i + 1].lstrip("\t"))]
                color = (
                    "RGBA(172, 132, 74, 255)"
                    if "os_background_2" in lines[i]
                    else "RGBA(186, 150, 92, 255)"
                )
                out.append(f"{tabs}'ImageColor', {color},")
                i += 1
        i += 1
    t = "\n".join(out) + "\n"

    # 9) Equip slot colors
    t = t.replace(
        "'BorderColor', RGBA(60, 63, 68, 255),\n\t\t\t\t\t\t\t\t\t\t\t'Background', RGBA(42, 45, 54, 120),",
        "'BorderColor', RGBA(90, 60, 28, 255),\n\t\t\t\t\t\t\t\t\t\t\t'Background', RGBA(55, 40, 22, 140),",
    )
    t = t.replace(
        "'BorderColor', RGBA(60, 63, 68, 255),\n\t\t\t\t\t\t\t\t\t\t'Background', RGBA(42, 45, 54, 120),",
        "'BorderColor', RGBA(90, 60, 28, 255),\n\t\t\t\t\t\t\t\t\t\t'Background', RGBA(55, 40, 22, 140),",
    )

    # 10) Class icon / stat icon warmer
    t = t.replace(
        "'ImageColor', RGBA(195, 189, 172, 255),",
        "'ImageColor', RGBA(186, 150, 90, 255),",
        1,
    )
    t = t.replace(
        "'ImageColor', RGBA(130, 128, 120, 128),",
        "'ImageColor', RGBA(148, 110, 58, 180),",
        1,
    )

    if "AME_Mark.png" not in t:
        raise SystemExit("theme apply failed: mark not present")
    if "PDAAIMBrowserBanner" in t:
        raise SystemExit("theme apply failed: AIM banner still present")

    SRC.write_text(t, encoding="utf-8")
    print("themed", SRC)


if __name__ == "__main__":
    main()
