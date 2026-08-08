import os
import io
import re
import zstandard as zstd

SAVE_DIR = r"C:\Users\SsAnd\Saved Games\Jagged Alliance 3\76561198048984330"
MAGIC = bytes([0x28, 0xB5, 0x2F, 0xFD])
BROKEN = re.compile(r"PlaceCharacterEffect\('([^']+)',\s*\)")


def extract_session(path):
    data = open(path, "rb").read()
    dctx = zstd.ZstdDecompressor()
    start = None
    i = 0
    while True:
        j = data.find(MAGIC, i)
        if j < 0:
            break
        try:
            out = dctx.decompress(data[j:], max_output_size=200000)
            if out.startswith(b"return"):
                start = j
                break
        except Exception:
            pass
        i = j + 4
    if start is None:
        return None
    parts = []
    pos = start
    while pos + 4 < len(data) and data[pos : pos + 4] == MAGIC:
        try:
            p = zstd.get_frame_parameters(data[pos:])
            csize = getattr(p, "compressed_size", None)
        except Exception:
            csize = None
        if not csize:
            # binary search minimal
            lo, hi = 16, min(len(data) - pos, 2_000_000)
            best = None
            out = None
            while lo <= hi:
                mid = (lo + hi) // 2
                try:
                    out = dctx.decompress(data[pos : pos + mid], max_output_size=20_000_000)
                    best = mid
                    hi = mid - 1
                except Exception:
                    lo = mid + 1
            if not best:
                break
            csize = best
        else:
            try:
                out = dctx.decompress(data[pos : pos + csize], max_output_size=20_000_000)
            except Exception:
                # fallback binary
                out = dctx.decompress(data[pos:], max_output_size=20_000_000)
                parts.append(out)
                break
        parts.append(out)
        pos += csize
        while pos < len(data) and data[pos] == 0:
            pos += 1
        if pos + 4 >= len(data) or data[pos : pos + 4] != MAGIC:
            nxt = data.find(MAGIC, pos)
            if nxt < 0 or nxt - pos > 4096:
                break
            pos = nxt
        if len(parts) > 500:
            break
    return b"".join(parts).decode("utf-8", errors="replace")


names = [
    "M3_Turn15.savegame.sav",
    "M3_Turn14.savegame.sav",
    "M3_Turn13.savegame.sav",
    "M3_CombatStart(2).savegame.sav",
    "M3_CombatEnd(2).savegame.sav",
    "M3_SectorEnter.savegame.sav",
]
# also Day_10*
for f in os.listdir(SAVE_DIR):
    if f.startswith("Day_10") and f.endswith(".sav"):
        names.append(f)

for name in names:
    fp = os.path.join(SAVE_DIR, name)
    if not os.path.isfile(fp):
        print(name, "MISSING")
        continue
    try:
        text = extract_session(fp)
    except Exception as e:
        print(name, "EXTRACT FAIL", e)
        continue
    if not text:
        print(name, "NO SESSION")
        continue
    ms = list(BROKEN.finditer(text))
    print(name, "broken", len(ms), [m.group(1) for m in ms[:5]], "chars", len(text))
