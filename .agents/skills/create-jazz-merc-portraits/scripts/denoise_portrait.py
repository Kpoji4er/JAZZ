# -*- coding: utf-8 -*-
"""DEPRECATED for fabric folds.

OpenCV bilateral made portraits mushy without removing wrinkle grids.
Use GPT image denoise via GenerateImage instead — see skill + jazz-merc-portraits rule.

Kept only for emergency grain (not folds). Prefer:
  GenerateImage with reference = noisy Big + OK_clean_folds_Laura_pants.png
  Prompt: keep sharp; remove dense micro-wrinkles; few large folds only.
"""
print("DEPRECATED: use GPT GenerateImage denoise (see create-jazz-merc-portraits skill).")
raise SystemExit(2)
