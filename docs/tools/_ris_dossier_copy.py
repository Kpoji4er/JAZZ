"""Compatibility facade for the canonical R.I.S. copy bank.

New tooling should import :mod:`_ris_copy_bank` directly.  This module keeps
older scripts working without retaining a second editable copy of the prose.
"""

from __future__ import annotations

try:  # Package import (for tests and editor tooling).
    from ._ris_copy_bank import (
        AAR_FIXES,
        DOSSIERS,
        MAJOR_STRATEGY,
        QUEST_DOSSIERS,
        STRING_FIXES,
        UI_FIXES,
        WELCOME_FIXES,
    )
except ImportError:  # Direct script import from docs/tools.
    from _ris_copy_bank import (  # type: ignore[no-redef]
        AAR_FIXES,
        DOSSIERS,
        MAJOR_STRATEGY,
        QUEST_DOSSIERS,
        STRING_FIXES,
        UI_FIXES,
        WELCOME_FIXES,
    )

__all__ = [
    "DOSSIERS",
    "QUEST_DOSSIERS",
    "WELCOME_FIXES",
    "UI_FIXES",
    "AAR_FIXES",
    "STRING_FIXES",
    "MAJOR_STRATEGY",
]
