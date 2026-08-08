import os
import io
import struct
import zstandard as zstd

SAVE_DIR = r"C:\Users\SsAnd\Saved Games\Jagged Alliance 3\76561198048984330"
OUT = r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\.tmp\save_extract"
os.makedirs(OUT, exist_ok=True)
MAGIC = bytes([0x28, 0xB5, 0x2F, 0xFD])


def find_frame_compressed_size(data, off):
    """Binary-search the end of one zstd frame starting at off."""
    dctx = zstd.ZstdDecompressor()
    # Upper bound: next magic or +8MB
    nxt = data.find(MAGIC, off + 4)
    hi = len(data) - off
    if nxt > 0:
        hi = min(hi, max(nxt - off + 500000, 64))
    # First try get_frame_parameters
    try:
        p = zstd.get_frame_parameters(data[off:])
        attrs = {a: getattr(p, a) for a in dir(p) if not a.startswith("_")}
        print(" frame params", {k: v for k, v in attrs.items() if not callable(v)})
        if getattr(p, "compressed_size", 0):
            return p.compressed_size
    except Exception as e:
        print(" params fail", e)

    # binary search length that decompresses exactly one frame
    lo = 16
    best = None
    # coarse then fine
    for length in list(range(64, min(hi, 2_000_000), 1024)) + ([nxt - off] if nxt > 0 else []):
        if length <= 0 or length > hi:
            continue
        try:
            out = dctx.decompress(data[off : off + length], max_output_size=20_000_000)
            best = length
            # try to find minimal
            break
        except zstd.ZstdError as e:
            msg = str(e)
            if "Unknown frame descriptor" in msg or "did not contain" in msg:
                # might be too long (extra garbage interpreted as next frame) or too short
                continue
            continue
        except Exception:
            continue

    # finer: find minimal length that works
    if best is None:
        # try decompress with content-size known from first successful small max
        try:
            out = dctx.decompress(data[off:], max_output_size=20_000_000)
            # can't know size
            return None, out
        except Exception as e:
            print(" decompress all fail", e)
            return None, None

    # shrink best
    low, high = 16, best
    last_ok = best
    last_out = dctx.decompress(data[off : off + best], max_output_size=20_000_000)
    while low < high:
        mid = (low + high) // 2
        try:
            out = dctx.decompress(data[off : off + mid], max_output_size=20_000_000)
            last_ok = mid
            last_out = out
            high = mid
        except Exception:
            low = mid + 1
    return last_ok, last_out


def rebuild(name):
    path = os.path.join(SAVE_DIR, name)
    data = open(path, "rb").read()
    # find start
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
        print(name, "no start")
        return
    print(name, "start", start)

    parts = []
    pos = start
    while pos + 4 < len(data) and data[pos : pos + 4] == MAGIC:
        csize, out = find_frame_compressed_size(data, pos)
        if out is None:
            print(" stop no out at", pos)
            break
        parts.append(out)
        print(" frame@%d csize=%s out=%d head=%r" % (pos, csize, len(out), out[:40]))
        if csize is None:
            # only got one frame via max_output; stop
            print(" no csize, stop after one")
            break
        pos += csize
        # skip padding zeros?
        while pos < len(data) and data[pos] == 0:
            pos += 1
        if len(parts) > 500:
            break
        # if next isn't magic, try scan forward a bit
        if pos + 4 < len(data) and data[pos : pos + 4] != MAGIC:
            nxt = data.find(MAGIC, pos)
            if nxt < 0 or nxt - pos > 4096:
                print(" next magic gap", nxt, "from", pos)
                break
            print(" skip gap", nxt - pos, "to next magic")
            pos = nxt

    session = b"".join(parts)
    print("TOTAL", len(session), "frames", len(parts))
    text = session.decode("utf-8", errors="replace")
    outp = os.path.join(OUT, name + ".game_session.lua")
    open(outp, "w", encoding="utf-8", newline="\n").write(text)
    lines = text.splitlines()
    print("lines", len(lines))
    for i in range(max(0, 4110), min(len(lines), 4135)):
        print("%d: %s" % (i + 1, lines[i][:240]))

    # syntax check with lupa stubs
    import lupa

    lua = lupa.LuaRuntime()
    lua.execute(
        """
        function PlaceObj(...) return {} end
        function PlaceInventoryItem(...) return {} end
        function PlaceUnitData(...) return {} end
        function PlaceCharacterEffect(...) return {} end
        function PlaceStatusEffect(...) return {} end
        function InvalidPos(...) return {} end
        function set(t) return t or {} end
        function point(...) return {} end
        function RGBA(...) return 0 end
        function o(...) return {} end
        function T(...) return '' end
        function Untranslated(...) return '' end
        function LoadShortcutInputs(...) return {} end
        """
    )
    load = lua.eval("load")
    # Lua 5.x load(string)
    try:
        result = load(text)
        # lupa may return function or (nil, err)
        if result is None:
            print("LOAD NIL")
        else:
            # check if it's a tuple
            print("LOAD type", type(result))
            try:
                fn = result
                fn()
                print("SYNTAX+RUN OK")
            except Exception as e:
                print("RUN/SYNTAX", e)
    except Exception as e:
        print("LOAD EXC", e)

    # Also try load with message
    try:
        ok = lua.eval("function(s) local f,e=load(s); return f~=nil, e end")(text)
        print("load ok/err", ok)
    except Exception as e:
        print("check exc", e)

    return outp


rebuild("M3_Turn15.savegame.sav")
