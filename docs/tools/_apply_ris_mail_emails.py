#!/usr/bin/env python3
"""Compatibility wrapper for the unified JAZZ-UI-RIS-002 apply pipeline.

The former Phase A mail generator is intentionally retired: its independent
welcome and supply-brief copy predates the approved bilingual bank. This entry
point now executes the complete projection and accepts its dry-run, ``--check``,
and ``--apply`` options.
"""

from __future__ import annotations

from _apply_ris_editorial import main


if __name__ == "__main__":
    raise SystemExit(main())
