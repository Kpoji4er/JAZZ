"""Copy committed last_changes (+ version if lower) into dirty metadata.lua WIP."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

LC_RE = re.compile(r"'last_changes',\s*\"((?:\\.|[^\"])*)\"")


def sync(repo: Path) -> None:
    head = subprocess.check_output(
        ["git", "show", "HEAD:metadata.lua"], cwd=repo, encoding="utf-8"
    )
    path = repo / "metadata.lua"
    wip = path.read_text(encoding="utf-8")
    hm = LC_RE.search(head)
    wm = LC_RE.search(wip)
    if not hm or not wm:
        raise SystemExit(f"last_changes parse fail in {repo.name}: head={bool(hm)} wip={bool(wm)}")
    wip2 = wip[: wm.start()] + hm.group(0) + wip[wm.end() :]
    hv = int(re.search(r"'version',\s*(\d+)", head).group(1))
    wv = int(re.search(r"'version',\s*(\d+)", wip2).group(1))
    if wv < hv:
        wip2 = re.sub(r"'version',\s*\d+", f"'version', {hv}", wip2, count=1)
        print(f"{repo.name}: version {wv} -> {hv}")
    path.write_text(wip2, encoding="utf-8")
    print(f"{repo.name}: last_changes synced from HEAD ({hm.group(1)[:60]}...)")


if __name__ == "__main__":
    sync(Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz"))
    sync(Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units"))
