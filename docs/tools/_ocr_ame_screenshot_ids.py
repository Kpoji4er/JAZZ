"""OCR Entity/Appearance IDs from AME Win+PrintScreen shots."""
from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
import winocr

SRC = Path(r"C:\Users\SsAnd\Pictures\Screenshots")
DST = Path(__file__).resolve().parents[2] / ".tmp" / "ame-crops"
CATALOG = Path(__file__).resolve().parents[1] / "design" / "mercs-ja12" / "_appearance-donor-visual-catalog.md"

SKIP = {
    "Entity", "Appearance", "Animation", "Anim", "Weight", "Mask", "Static",
    "Speed", "Modifier", "Variation", "Viewer", "Blending", "false", "true",
    "Edit", "All", "Idle", "idle", "Step", "Duration", "Looping", "Disable",
    "Compensation", "Inverse", "Delta", "Revision", "pearance", "odifier",
    "difier", "Delete", "Reconfirm", "Wipe", "Out", "Deleted", "Blend", "Time",
    "Other", "AnimMI", "earance", "ion", "Ed", "xo", "ini", "zo",
}


def crop_id(im: Image.Image) -> Image.Image:
    w, h = im.size
    c = im.crop((int(w * 0.50), int(h * 0.38), int(w * 0.96), int(h * 0.54)))
    c = ImageOps.grayscale(c)
    c = ImageEnhance.Contrast(c).enhance(2.4)
    return c.resize((c.size[0] * 3, c.size[1] * 3), Image.Resampling.LANCZOS)


def parse_id(text: str) -> str | None:
    if not text:
        return None
    t = text.replace("\n", " ")
    # Best: "x PresetName idle"
    m = re.search(r"\bx\s+([A-Za-z][A-Za-z0-9_]{1,60})\s+idle\b", t, re.I)
    if m and m.group(1) not in SKIP:
        return m.group(1)
    # "PresetName idle Edit"
    m = re.search(r"\b([A-Za-z][A-Za-z0-9_]{2,60})\s+idle\s+Ed", t, re.I)
    if m and m.group(1) not in SKIP and m.group(1).lower() != "appearance":
        return m.group(1)
    toks = re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", t)
    cands = [x for x in toks if x not in SKIP and x.lower() not in {s.lower() for s in SKIP}]
    if not cands:
        return None
    cands.sort(
        key=lambda x: (("_" in x) + sum(1 for c in x if c.isupper()), len(x)),
        reverse=True,
    )
    return cands[0]


def catalog_headers(text: str) -> set[str]:
    headers: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("## "):
            continue
        head = line[3:].split(" ·")[0].strip()
        for part in re.split(r"[/,]", head):
            part = part.strip()
            part = re.sub(r"\s*\(.*$", "", part).strip()
            if part and part[0].isalnum():
                headers.add(part)
                # Legion_Artillery(+02/03) already stripped
                m = re.match(r"(.+?)_0\d+$", part)
                if m:
                    headers.add(m.group(1))
    return headers


async def ocr_img(im: Image.Image) -> str:
    r = await winocr.recognize_pil(im)
    return getattr(r, "text", "") or ""


async def main() -> int:
    DST.mkdir(parents=True, exist_ok=True)
    files = sorted(
        [p for p in SRC.glob("*.png") if p.stat().st_size > 50000],
        key=lambda p: p.stat().st_mtime,
    )
    headers = catalog_headers(CATALOG.read_text(encoding="utf-8"))
    rows = []
    for i, p in enumerate(files):
        im = Image.open(p).convert("RGB")
        c = crop_id(im)
        c.save(DST / f"{i:03d}_idcrop.png")
        text = await ocr_img(c)
        pid = parse_id(text)
        rows.append({"i": i, "src": p.name, "id": pid, "ocr": text})
        if i % 10 == 0:
            print(f"{i:03d} {pid}", flush=True)

    uniq: list[str] = []
    seen: set[str] = set()
    for r in rows:
        if r["id"] and r["id"] not in seen:
            seen.add(r["id"])
            uniq.append(r["id"])

    missing = [x for x in uniq if x not in headers]
    failed = [r for r in rows if not r["id"]]
    out = {
        "files": len(files),
        "uniq": uniq,
        "missing": missing,
        "failed_idx": [r["i"] for r in failed],
        "rows": rows,
    }
    (DST / "ids.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"files={len(files)} uniq={len(uniq)} missing={len(missing)} failed={len(failed)}", flush=True)
    print("UNIQ=" + ",".join(uniq), flush=True)
    print("MISSING=" + ",".join(missing), flush=True)
    print("FAILED=" + ",".join(str(i) for i in out["failed_idx"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
