#!/usr/bin/env python3
"""Compatibility wrapper for the unified JAZZ-UI-RIS-002 apply pipeline.

This legacy entry point intentionally contains no editable R.I.S. prose.
It accepts the same dry-run, ``--check``, and ``--apply`` options as
``_apply_ris_editorial.py`` and always executes the complete projection.
"""

from __future__ import annotations

from _apply_ris_editorial import main


if __name__ == "__main__":
    raise SystemExit(main())
