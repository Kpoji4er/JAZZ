#!/usr/bin/env python3
"""Strip illegal ImageColor from XFrame nodes in AME browser template."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Code" / "System_AME_Browser_Template.lua"


def strip_frame_imagecolors(text: str) -> str:
    """Remove ImageColor lines that sit on XFrame windows (XFrame has no ImageColor)."""
    # Split by PlaceObj windows roughly: for each ModItem/XTemplateWindow block
    parts = re.split(r"(PlaceObj\('XTemplateWindow', \{)", text)
    out = [parts[0]]
    i = 1
    while i < len(parts):
        header = parts[i]  # PlaceObj('XTemplateWindow', {
        body = parts[i + 1] if i + 1 < len(parts) else ""
        # body runs until we can't easily know end — instead scan first ~40 lines of props
        # Simpler approach: if '__class', "XFrame" appears before next PlaceObj child content's ImageColor at prop level
        chunk = header + body
        # Only strip ImageColor in the property section before the children `}, {` or `}),`
        m = re.match(
            r"(PlaceObj\('XTemplateWindow', \{)(.*?)(\n\t+\}, \{|\n\t+\}\),)",
            chunk,
            re.S,
        )
        if m:
            props = m.group(2)
            rest = chunk[len(m.group(0)) :]
            if "'__class', \"XFrame\"" in props or "'__class', 'XFrame'" in props:
                props2 = re.sub(
                    r"\n[ \t]*'ImageColor', RGBA\([^)]+\),",
                    "",
                    props,
                )
                chunk = m.group(1) + props2 + m.group(3) + rest
            else:
                chunk = m.group(0) + rest
            out.append(chunk)
        else:
            out.append(chunk)
        i += 2
    return "".join(out)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    # Also remove SetImageColor calls on filter buttons (XTextButton may lack it)
    text2 = text.replace(
        "\n\t\t\t\t\t\t\t\t\tself:SetImageColor(selected and RGBA(196, 148, 72, 255) or RGBA(148, 110, 58, 255))",
        "",
    )
    text2 = strip_frame_imagecolors(text2)
    # remove ImageColor immediately after FrameBox on lines that are XFrame - brute force:
    # any ImageColor after Image UI/PDA/os_header or os_background on XFrame was added by us
    lines = text2.splitlines()
    out = []
    i = 0
    in_frame = False
    while i < len(lines):
        ln = lines[i]
        if "PlaceObj('XTemplateWindow'" in ln:
            in_frame = False
        if "'__class', \"XFrame\"" in ln:
            in_frame = True
        if in_frame and "'ImageColor'," in ln:
            i += 1
            continue
        if in_frame and (ln.strip() == "}," or ln.strip().startswith("}, {") or ln.strip() == "}),"):
            in_frame = False
        # also strip ImageColor on XTextButton filter Image (button uses frame image)
        out.append(ln)
        i += 1
    text2 = "\n".join(out) + "\n"
    # Remove ImageColor on filter button that uses os_header_disable (XTextButton Image is frame-like)
    text2 = text2.replace(
        "\n\t\t\t\t\t\t\t'ImageColor', RGBA(148, 110, 58, 255),",
        "",
    )
    SRC.write_text(text2, encoding="utf-8")
    # count remaining ImageColor - should only be on XImage
    print("ImageColor left", text2.count("'ImageColor'"))
    print("SetImageColor left", text2.count("SetImageColor"))
    print("XFrame ImageColor leftover check...")
    for m in re.finditer(
        r"'__class', \"XFrame\"[\s\S]{0,400}?'ImageColor'", text2
    ):
        print("WARN still on frame", m.start())


if __name__ == "__main__":
    main()
