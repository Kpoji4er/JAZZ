# -*- coding: utf-8 -*-
"""After Mod Editor SaveDef: restore metadata.code from items.lua ModItemCode.

Supersedes the old hardcoded CRITICAL_CODE list. If the editor rewrote
metadata.lua without reloading items.lua, Code files that exist as
ModItemCode are re-inserted. Flat InventoryItem/*.lua aliases are dropped
when InventoryItem/vanillunique/*.lua is also listed.

    python docs/tools/_restore_metadata_code_load.py
    python docs/tools/_restore_metadata_code_load.py --dry-run

If items.lua itself lost ModItemCode, use git historic restore instead:

    python docs/tools/_restore_dropped_metadata_code.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SCRIPT = TOOLS / "_restore_dropped_metadata_code.py"


def main() -> int:
    extra = [a for a in sys.argv[1:] if a != "--from-items"]
    return subprocess.call([sys.executable, str(SCRIPT), "--from-items", *extra])


if __name__ == "__main__":
    raise SystemExit(main())
