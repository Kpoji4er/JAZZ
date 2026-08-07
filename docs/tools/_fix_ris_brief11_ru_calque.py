#!/usr/bin/env python3
"""Compatibility wrapper for the unified JAZZ-UI-RIS-002 apply pipeline.

The one-off Brief 11 wording repair has been absorbed into the canonical
brief bank. Running this historical command now checks or applies the complete
R.I.S. projection instead of restoring obsolete localization IDs or prose.
"""

from __future__ import annotations

from _apply_ris_editorial import main


if __name__ == "__main__":
    raise SystemExit(main())
