#!/usr/bin/env python3
"""Compatibility wrapper for the unified JAZZ-UI-RIS-002 apply pipeline.

English ``Text`` orientation is now enforced for every canonical R.I.S. row
by ``_apply_ris_editorial.py``. This legacy command forwards all modes to that
complete projection and contains no independent repair values.
"""

from __future__ import annotations

from _apply_ris_editorial import main


if __name__ == "__main__":
    raise SystemExit(main())
