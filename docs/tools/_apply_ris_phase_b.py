#!/usr/bin/env python3
"""Compatibility wrapper for the unified JAZZ-UI-RIS-002 apply pipeline.

The former Phase B generator is intentionally retired: keeping its separate
dossier and AAR prose would allow an old command to overwrite the canonical
copy bank. This entry point accepts the same dry-run, ``--check``, and
``--apply`` options as ``_apply_ris_editorial.py``.
"""

from __future__ import annotations

from _apply_ris_editorial import main


if __name__ == "__main__":
    raise SystemExit(main())
