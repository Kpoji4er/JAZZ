# -*- coding: utf-8 -*-
"""Pilot subtitles for ja2mercs folders (XLSX/mercedt first; optional STT).

Prefer XLSX / mercedt CSV text when present. Optional faster-whisper STT covers
lines without text (battle ATTN/OK, folders without xlsx). For Grom folder,
pids 076 and 047 are both Grom banks — label samples by pid, do not treat as
identity fight / remesh blocker.

Usage (jazz/):
  python docs/tools/_stt_ja2mercs_sample.py
  python docs/tools/_stt_ja2mercs_sample.py --folder но-шж/гром --pids 076,047
  python docs/tools/_stt_ja2mercs_sample.py --stems 000,001,002,011,012,033,040,ATTN,OK1
  python docs/tools/_stt_ja2mercs_sample.py --no-stt   # reference text export only
  python docs/tools/_stt_ja2mercs_sample.py --model tiny --no-xlsx

STT needs: working torch + `pip install faster-whisper`, ffmpeg (imageio_ffmpeg or PATH).
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
DEFAULT_ROOT = Path(r"C:\Users\SsAnd\Downloads\ja2mercs\ja2mercs")
OUT_DIR = JAZZ / "docs/design/mercs-ja12/_voice-source/_stt"
SJ_CSV = JAZZ / "docs/design/mercs-ja12/_voice-source/sj-mercedt/076_Gromov.csv"

FFMPEG_CANDIDATES = [
    Path(
        r"C:\Users\SsAnd\AppData\Local\Programs\Python\Python312\Lib\site-packages"
        r"\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
    ),
    Path(r"D:\py-voice\RVC-WebUI\ffmpeg.exe"),
]

AUDIO_EXTS = {".wav", ".ogg", ".mp3"}
STEM_RE = re.compile(
    r"^(?:[RrDd]_)?(?:U_)?(?P<pid>\d{2,3}|U_\d+)_(?P<stem>.+)$", re.IGNORECASE
)

# Identity-heavy AIM lines + a few battle cues.
DEFAULT_STEMS = [
    "000",
    "001",
    "002",
    "011",
    "012",
    "015",
    "023",
    "033",
    "040",
    "ATTN",
    "OK1",
]


def find_ffmpeg() -> Path:
    for p in FFMPEG_CANDIDATES:
        if p.is_file():
            return p
    which = shutil.which("ffmpeg")
    if which:
        return Path(which)
    try:
        import imageio_ffmpeg

        return Path(imageio_ffmpeg.get_ffmpeg_exe())
    except Exception:
        pass
    raise SystemExit(
        "ffmpeg not found — install ffmpeg or imageio-ffmpeg, "
        "or point FFMPEG_CANDIDATES in this script."
    )


def to_pcm_wav(ffmpeg: Path, src: Path, dest: Path) -> None:
    """ADPCM/OGG/etc → mono 16 kHz PCM wav for whisper."""
    cmd = [
        str(ffmpeg),
        "-y",
        "-i",
        str(src),
        "-acodec",
        "pcm_s16le",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(dest),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg failed on {src.name}: {r.stderr[-400:]}")


def load_xlsx_texts(merc_dir: Path) -> dict[str, str]:
    """Map stem (000 / ATTN) → RU text from first *.xlsx if openpyxl available."""
    xlsx_files = list(merc_dir.glob("*.xlsx")) + list(merc_dir.rglob("*.xlsx"))
    if not xlsx_files:
        return {}
    try:
        import openpyxl
    except ImportError:
        print("WARN: openpyxl missing — skip XLSX text export", file=sys.stderr)
        return {}
    out: dict[str, str] = {}
    wb = openpyxl.load_workbook(xlsx_files[0], read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return out
    # Heuristic: look for numeric line id + text columns.
    for row in rows[1:]:
        if not row:
            continue
        cells = [c for c in row if c is not None]
        if len(cells) < 2:
            continue
        key = None
        text = None
        for c in cells:
            s = str(c).strip()
            if key is None and re.fullmatch(r"\d{1,3}", s):
                key = s.zfill(3)
            elif key is None and re.fullmatch(r"[A-Za-z]+", s):
                key = s.upper()
            elif key is not None and isinstance(c, str) and len(s) > 0:
                text = s
                break
        if key and text and key not in out:
            out[key] = text
    return out


def norm_pid(pid: str) -> str:
    p = pid.strip()
    if re.fullmatch(r"\d{1,3}", p):
        return p.zfill(3)
    return p


def norm_stem(stem: str) -> str:
    s = stem.strip()
    if re.fullmatch(r"\d{1,3}", s):
        return s.zfill(3)
    return s.upper() if s.isalpha() else s


def load_sj_grom_texts() -> dict[str, str]:
    if not SJ_CSV.is_file():
        return {}
    out: dict[str, str] = {}
    with SJ_CSV.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            stem = (row.get("line") or "").strip()
            text = (row.get("text") or "").strip()
            if re.fullmatch(r"\d{1,3}", stem):
                out[stem.zfill(3)] = text
    return out


def resolve_audio(merc_dir: Path, pid: str, stem: str) -> Path | None:
    pid_n = pid.lstrip("0") or "0"
    candidates = [
        f"{pid}_{stem}.wav",
        f"{pid}_{stem}.WAV",
        f"{pid}_{stem}.ogg",
        f"r_{pid}_{stem}.wav",
        f"R_{pid}_{stem}.wav",
        f"{pid_n}_{stem}.wav",
    ]
    # Case-insensitive stem match for battle cues.
    lower_stem = stem.lower()
    for p in merc_dir.iterdir():
        if not p.is_file() or p.suffix.lower() not in AUDIO_EXTS:
            continue
        m = STEM_RE.match(p.stem)
        if not m:
            continue
        file_pid = m.group("pid")
        file_stem = m.group("stem")
        if file_pid.lstrip("0") != pid.lstrip("0") and file_pid != pid:
            continue
        if file_stem.lower() == lower_stem or file_stem.upper() == stem.upper():
            return p
    for name in candidates:
        p = merc_dir / name
        if p.is_file():
            return p
    return None


def transcribe_file(model, pcm_path: Path) -> str:
    segments, _info = model.transcribe(
        str(pcm_path),
        language="ru",
        beam_size=1,
        vad_filter=True,
    )
    parts = [seg.text.strip() for seg in segments if seg.text and seg.text.strip()]
    return " ".join(parts).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--folder", default="но-шж/гром", help="cat/merc under root")
    ap.add_argument("--pids", default="076,047")
    ap.add_argument("--stems", default=",".join(DEFAULT_STEMS))
    ap.add_argument("--model", default="base", help="faster-whisper model size")
    ap.add_argument("--no-xlsx", action="store_true")
    ap.add_argument("--no-stt", action="store_true", help="export reference text only")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    merc_dir = args.root / args.folder
    if not merc_dir.is_dir():
        raise SystemExit(f"folder not found: {merc_dir}")

    # PowerShell may strip leading zeros from unquoted 076/000 — re-pad numeric ids.
    pids = [norm_pid(p) for p in args.pids.split(",") if p.strip()]
    stems = [norm_stem(s) for s in args.stems.split(",") if s.strip()]
    out_dir = args.out or (OUT_DIR / merc_dir.name)
    out_dir.mkdir(parents=True, exist_ok=True)

    xlsx_texts = {} if args.no_xlsx else load_xlsx_texts(merc_dir)
    sj_texts = load_sj_grom_texts() if "076" in pids else {}

    rows: list[dict[str, str]] = []
    model = None
    ffmpeg = None
    if not args.no_stt:
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            raise SystemExit(
                "faster-whisper not installed. Run: pip install faster-whisper"
            )
        ffmpeg = find_ffmpeg()
        print(f"ffmpeg={ffmpeg}")
        print(f"loading whisper model={args.model} …")
        model = WhisperModel(args.model, device="cpu", compute_type="int8")

    with tempfile.TemporaryDirectory(prefix="jazz_stt_") as tmp:
        tmp_path = Path(tmp)
        for pid in pids:
            for stem in stems:
                audio = resolve_audio(merc_dir, pid, stem)
                ref = ""
                if pid == "076" and stem in sj_texts:
                    ref = sj_texts[stem]
                if not ref and stem in xlsx_texts:
                    ref = xlsx_texts[stem]
                stt = ""
                note = ""
                if audio is None:
                    note = "missing_audio"
                elif args.no_stt:
                    note = "stt_skipped"
                else:
                    assert model is not None and ffmpeg is not None
                    pcm = tmp_path / f"{pid}_{stem}.pcm.wav"
                    try:
                        to_pcm_wav(ffmpeg, audio, pcm)
                        stt = transcribe_file(model, pcm)
                    except Exception as e:
                        note = f"stt_error:{e}"
                rows.append(
                    {
                        "pid": pid,
                        "stem": stem,
                        "file": audio.name if audio else "",
                        "ref_text": ref,
                        "stt_text": stt,
                        "note": note,
                    }
                )
                print(
                    f"{pid}_{stem}: ref={ref!r} | stt={stt!r}"
                    + (f" [{note}]" if note else "")
                )

    csv_path = out_dir / "grom_076_vs_047_sample.csv"
    txt_path = out_dir / "grom_076_vs_047_sample.txt"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["pid", "stem", "file", "ref_text", "stt_text", "note"]
        )
        w.writeheader()
        w.writerows(rows)

    lines = [
        f"# STT/ref pilot: {args.folder} (Grom-folder banks — both pids are Grom)",
        f"# model={args.model} language=ru no_stt={args.no_stt}",
        f"# xlsx_keys={len(xlsx_texts)} sj_076_keys={len(sj_texts)}",
        "# Prefer mercedt/XLSX ref_text; stt_text empty until working torch+faster-whisper.",
        "",
    ]
    for r in rows:
        lines.append(
            f"{r['pid']}_{r['stem']}\tref={r['ref_text']}\tstt={r['stt_text']}"
            + (f"\t{r['note']}" if r["note"] else "")
        )
    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {csv_path}")
    print(f"wrote {txt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
