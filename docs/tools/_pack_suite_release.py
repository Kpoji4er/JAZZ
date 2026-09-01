"""Pack the four JAZZ suite archives from exact Git SHAs.

Never copies the active working tree. Materializes each package with
``git archive`` (committed blob bytes) and replaces Git LFS pointers
from the repo LFS object store.

Writes deterministic ZIP files (sorted names, fixed timestamps) plus
SHA256SUMS and an optional release manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1"
ZIP_EPOCH = (2020, 1, 1, 0, 0, 0)
FILE_ATTR = 0o644 << 16

PACKAGES = (
    {
        "name": "JAZZ",
        "folder": "jazz",
        "github": "Kpoji4er/JAZZ",
        "mod_id": "e6L4ECj",
        "artifact_prefix": "JAZZ",
        "local_names": ("jazz",),
    },
    {
        "name": "JAZZ-assets",
        "folder": "jazz_assets",
        "github": "Kpoji4er/JAZZ-assets",
        "mod_id": "pDGDhr",
        "artifact_prefix": "JAZZ-assets",
        "local_names": ("jazz_assets", "jazz-assets"),
    },
    {
        "name": "JAZZ-maps",
        "folder": "jazz-maps",
        "github": "Kpoji4er/JAZZ-maps",
        "mod_id": "FhNNYd",
        "artifact_prefix": "JAZZ-maps",
        "local_names": ("jazz-maps",),
    },
    {
        "name": "JAZZ-units",
        "folder": "jazz-units",
        "github": "Kpoji4er/JAZZ-units",
        "mod_id": "Dv3mFVN",
        "artifact_prefix": "JAZZ-units",
        "local_names": ("jazz-units",),
    },
)

ALWAYS_SKIP_TOP = {
    ".git",
    ".github",
    ".agents",
    ".cursor",
    ".tmp",
    "docs",
    "scripts",
    "release",
    "_localization",
    "__pycache__",
    "_review",
    "codex_worktrees",
}

ALWAYS_SKIP_NAMES = {
    "AGENTS.md",
    ".gitignore",
    ".gitattributes",
    ".ja3-root.local",
    "Thumbs.db",
    ".DS_Store",
}

ROOT_VERSION_RE = re.compile(r"(?m)^\t'(?P<key>version_major|version_minor|version|lua_revision|saved_with_revision)',\s*(?P<val>\d+)")
ROOT_STRING_RE = re.compile(r"(?m)^\t'(?P<key>id|title)',\s*\"(?P<val>[^\"]*)\"")
IGNORE_FILES_RE = re.compile(r"'ignore_files',\s*\{(?P<body>.*?)\}", re.S)
IGNORE_ITEM_RE = re.compile(r'"([^"]+)"')
LFS_OID_RE = re.compile(r"(?m)^oid sha256:([0-9a-f]{64})$")
LFS_SIZE_RE = re.compile(r"(?m)^size (\d+)$")


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_text(repo: Path, *args: str) -> str:
    return run_git(repo, *args).stdout.decode("utf-8").strip()


def parse_root_numbers(metadata: str) -> dict[str, int]:
    values = {"version_major": 0, "version_minor": 0, "version": 0}
    for match in ROOT_VERSION_RE.finditer(metadata):
        values[match.group("key")] = int(match.group("val"))
    return values


def parse_root_strings(metadata: str) -> dict[str, str]:
    return {match.group("key"): match.group("val") for match in ROOT_STRING_RE.finditer(metadata)}


def format_engine(major: int, minor: int, revision: int) -> str:
    return f"{major}.{minor:02d}-{revision:03d}"


def format_tag(major: int, minor: int, revision: int) -> str:
    return f"v{major}.{minor}.{revision}"


def parse_ignore_files(metadata: str) -> list[str]:
    match = IGNORE_FILES_RE.search(metadata)
    if not match:
        return []
    return IGNORE_ITEM_RE.findall(match.group("body"))


def is_lfs_pointer(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size > 1024:
        return False
    return path.read_bytes().startswith(LFS_POINTER_PREFIX)


def lfs_object_path(repo: Path, oid: str) -> Path:
    common = Path(git_text(repo, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    return common / "lfs" / "objects" / oid[:2] / oid[2:4] / oid


def hydrate_lfs(dest: Path, repo: Path, sha: str) -> None:
    pointers: list[Path] = []
    for path in dest.rglob("*"):
        if is_lfs_pointer(path):
            pointers.append(path)
    if not pointers:
        return
    run_git(repo, "lfs", "fetch", "origin", sha)
    for path in pointers:
        text = path.read_text(encoding="ascii")
        oid_match = LFS_OID_RE.search(text)
        size_match = LFS_SIZE_RE.search(text)
        if not oid_match or not size_match:
            raise RuntimeError(f"Malformed LFS pointer: {path}")
        oid = oid_match.group(1)
        size = int(size_match.group(1))
        obj = lfs_object_path(repo, oid)
        if not obj.is_file():
            rel = path.relative_to(dest).as_posix()
            run_git(repo, "lfs", "fetch", "-I", rel, "origin", sha)
        if not obj.is_file():
            raise RuntimeError(f"Missing LFS object {oid} for {path}")
        path.write_bytes(obj.read_bytes())
        if path.stat().st_size != size:
            raise RuntimeError(f"LFS size mismatch for {path}: {path.stat().st_size} != {size}")


def should_skip(rel_posix: str, ignore_patterns: list[str]) -> bool:
    parts = rel_posix.split("/")
    name = parts[-1]
    if parts[0] in ALWAYS_SKIP_TOP:
        return True
    if name in ALWAYS_SKIP_NAMES:
        return True
    if name.endswith((".bak", ".pyc", ".pyo", ".psd", ".zip")):
        return True
    if name.endswith(".md"):
        return True
    for pattern in ignore_patterns:
        if _match_ignore(rel_posix, name, parts, pattern):
            return True
    return False


def _match_ignore(rel_posix: str, name: str, parts: list[str], pattern: str) -> bool:
    from fnmatch import fnmatch

    if fnmatch(rel_posix, pattern) or fnmatch(name, pattern):
        return True
    if pattern.startswith("*") and pattern.endswith("/*"):
        token = pattern[1:-2]
        if token and token in parts:
            return True
    if pattern.startswith("*") and "/" not in pattern[1:]:
        return fnmatch(name, pattern)
    return False


def materialize(repo: Path, sha: str, dest: Path) -> None:
    if dest.exists():
        raise RuntimeError(f"Refusing to overwrite {dest}")
    dest.mkdir(parents=True)
    archive = run_git(repo, "archive", "--format=tar", sha)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as tar:
        tar.extractall(dest)
    hydrate_lfs(dest, repo, sha)


def collect_files(root: Path, ignore_patterns: list[str]) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if should_skip(rel, ignore_patterns):
            continue
        if is_lfs_pointer(path):
            raise RuntimeError(f"LFS pointer survived into archive set: {rel}")
        files.append(path)
    files.sort(key=lambda item: item.relative_to(root).as_posix())
    return files


def write_zip(zip_path: Path, folder: str, files: list[Path], root: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in files:
            rel = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{folder}/{rel}")
            info.date_time = ZIP_EPOCH
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = FILE_ATTR
            zf.writestr(info, path.read_bytes())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_repo(parent: Path, spec: dict, override: Path | None) -> Path:
    if override is not None:
        return override.resolve()
    for name in spec["local_names"]:
        candidate = parent / name
        if not candidate.is_dir():
            continue
        probe = subprocess.run(
            ["git", "-C", str(candidate), "rev-parse", "--git-dir"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if probe.returncode == 0:
            return candidate
    raise FileNotFoundError(f"Local repo for {spec['name']} was not found under {parent}")


def read_committed_metadata(repo: Path, sha: str) -> str:
    return run_git(repo, "show", f"{sha}:metadata.lua").stdout.decode("utf-8-sig")


def find_jazz_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "metadata.lua").is_file() and (parent / "Code").is_dir():
            return parent
    raise RuntimeError("Could not locate jazz package root")


def build_one(spec: dict, repo: Path, sha: str, out_dir: Path, tag: str, stage_root: Path) -> dict:
    metadata = read_committed_metadata(repo, sha)
    numbers = parse_root_numbers(metadata)
    strings = parse_root_strings(metadata)
    if strings.get("id") != spec["mod_id"]:
        raise RuntimeError(f"{spec['name']}: expected mod id {spec['mod_id']}, found {strings.get('id')!r}")
    ignore = parse_ignore_files(metadata)
    stage = stage_root / spec["folder"]
    materialize(repo, sha, stage)
    files = collect_files(stage, ignore)
    artifact = f"{spec['artifact_prefix']}-{tag}.zip"
    zip_path = out_dir / artifact
    write_zip(zip_path, spec["folder"], files, stage)
    digest = sha256_file(zip_path)
    display = format_engine(numbers["version_major"], numbers["version_minor"], numbers["version"])
    return {
        "name": spec["name"],
        "repository": spec["github"],
        "mod_id": spec["mod_id"],
        "commit": sha,
        "version_major": numbers["version_major"],
        "version_minor": numbers["version_minor"],
        "version": numbers["version"],
        "metadata_display": display,
        "artifact": artifact,
        "sha256": digest,
        "lua_revision": numbers.get("lua_revision", 0),
        "saved_with_revision": numbers.get("saved_with_revision", 0),
        "file_count": len(files),
        "zip_bytes": zip_path.stat().st_size,
    }


def write_sha256sums(out_dir: Path, records: list[dict]) -> None:
    lines = [f"{row['sha256']}  {row['artifact']}" for row in records]
    (out_dir / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="ascii")


def build_manifest(core: dict, records: list[dict], commonlib: dict) -> dict:
    return {
        "schema": 1,
        "release_version": {
            "display": core["metadata_display"],
            "tag": format_tag(core["version_major"], core["version_minor"], core["version"]),
            "source": f"{core['repository']}@{core['commit']}:metadata.lua",
            "version_major": core["version_major"],
            "version_minor": core["version_minor"],
            "revision": core["version"],
        },
        "game": {
            "lua_revision": core["lua_revision"],
            "saved_with_revision": core["saved_with_revision"],
        },
        "commonlib": commonlib,
        "packages": [
            {
                "name": row["name"],
                "repository": row["repository"],
                "mod_id": row["mod_id"],
                "commit": row["commit"],
                "version_major": row["version_major"],
                "version_minor": row["version_minor"],
                "version": row["version"],
                "metadata_display": row["metadata_display"],
                "artifact": row["artifact"],
                "sha256": row["sha256"],
            }
            for row in records
        ],
    }


def verify_manifest(manifest: dict, records: list[dict], expected_tag: str | None) -> None:
    tag = manifest["release_version"]["tag"]
    if expected_tag and expected_tag != tag:
        raise RuntimeError(f"GitHub ref {expected_tag} != metadata tag {tag}")
    by_name = {row["name"]: row for row in records}
    for package in manifest["packages"]:
        got = by_name[package["name"]]
        for key in ("commit", "sha256", "artifact", "mod_id", "metadata_display"):
            if package[key] != got[key]:
                raise RuntimeError(f"{package['name']} {key} mismatch: manifest {package[key]} != built {got[key]}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path(".tmp/suite-release"))
    parser.add_argument("--stage-dir", type=Path, default=Path(".tmp/suite-release-stage"))
    parser.add_argument("--jazz-root", type=Path, default=None)
    parser.add_argument("--jazz-sha", required=True)
    parser.add_argument("--assets-sha", required=True)
    parser.add_argument("--maps-sha", required=True)
    parser.add_argument("--units-sha", required=True)
    parser.add_argument("--assets-repo", type=Path, default=None)
    parser.add_argument("--maps-repo", type=Path, default=None)
    parser.add_argument("--units-repo", type=Path, default=None)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--verify-manifest", type=Path, default=None)
    parser.add_argument("--expected-tag", default=None)
    parser.add_argument("--commonlib-version", default="1.11")
    parser.add_argument("--commonlib-build", type=int, default=1060)
    parser.add_argument("--commonlib-commit", default="6758d82e5fccbf6bdd01b0173d2496b925982c3e")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    jazz_root = (args.jazz_root or find_jazz_root()).resolve()
    parent = jazz_root.parent
    shas = {
        "JAZZ": args.jazz_sha,
        "JAZZ-assets": args.assets_sha,
        "JAZZ-maps": args.maps_sha,
        "JAZZ-units": args.units_sha,
    }
    overrides = {
        "JAZZ": jazz_root,
        "JAZZ-assets": args.assets_repo,
        "JAZZ-maps": args.maps_repo,
        "JAZZ-units": args.units_repo,
    }
    out_dir = args.out_dir if args.out_dir.is_absolute() else jazz_root / args.out_dir
    stage_root = args.stage_dir if args.stage_dir.is_absolute() else jazz_root / args.stage_dir
    if stage_root.exists():
        import shutil

        shutil.rmtree(stage_root)
    out_dir.mkdir(parents=True, exist_ok=True)

    core_meta = read_committed_metadata(jazz_root, args.jazz_sha)
    core_nums = parse_root_numbers(core_meta)
    tag = format_tag(core_nums["version_major"], core_nums["version_minor"], core_nums["version"])
    if args.expected_tag and args.expected_tag != tag:
        raise RuntimeError(f"Expected tag {args.expected_tag}, metadata requires {tag}")

    records = []
    for spec in PACKAGES:
        repo = resolve_repo(parent, spec, overrides[spec["name"]])
        print(f"packing {spec['name']} {shas[spec['name']][:12]} from {repo}", flush=True)
        records.append(build_one(spec, repo, shas[spec["name"]], out_dir, tag, stage_root))
        print(
            f"  {records[-1]['artifact']} {records[-1]['metadata_display']} "
            f"files={records[-1]['file_count']} sha256={records[-1]['sha256']}",
            flush=True,
        )

    write_sha256sums(out_dir, records)
    commonlib = {
        "version": args.commonlib_version,
        "build": args.commonlib_build,
        "commit": args.commonlib_commit,
    }
    manifest = build_manifest(records[0], records, commonlib)
    manifest_text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    (out_dir / f"jazz-release-{tag}.json").write_text(manifest_text, encoding="utf-8")
    if args.manifest_out:
        dest = args.manifest_out if args.manifest_out.is_absolute() else jazz_root / args.manifest_out
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(manifest_text, encoding="utf-8")
    if args.verify_manifest:
        existing = json.loads(args.verify_manifest.read_text(encoding="utf-8"))
        verify_manifest(existing, records, args.expected_tag)
        print("manifest verification OK", flush=True)
    print(f"suite {manifest['release_version']['display']} -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr.decode("utf-8", errors="replace"))
        raise
