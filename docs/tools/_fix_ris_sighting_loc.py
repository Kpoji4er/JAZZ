#!/usr/bin/env python3
"""Compatibility wrapper for the unified JAZZ-UI-RIS-002 apply pipeline.

This entry point no longer carries a partial sighting/obituary copy bank.
It forwards dry-run, ``--check``, and ``--apply`` to
``_apply_ris_editorial.py``.
"""

from __future__ import annotations

from _apply_ris_editorial import main


if __name__ == "__main__":
    raise SystemExit(main())
