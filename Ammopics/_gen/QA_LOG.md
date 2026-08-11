# Ammo icon QA log — RESTART

Pipeline: GenerateImage on **#FF00FF** → `_finalize_ammo_gen_batch.py`  
`--key magenta --alpha-from draft --choke 0 --soft-outline 0.3`  
Runtime `Ammopics/*.png` **not** replaced until owner says so.

## Batch 1 — 9×18 — OWNER REVIEW (cut PASS wave)

| file | marking | accent | cut IoU | status |
| --- | --- | --- | --- | --- |
| gen_9x18 | 9x18 + ПСО | grey band | 0.94 | REVIEW |
| gen_9x18AP | 9x18 + ПСТ | red band | 0.99 vs FMJ | REVIEW | shape-locked to gen_9x18 |
| gen_9x18APP | 9x18 + 7Н25 | red band | 0.93 | REVIEW |
| gen_9x18JHP | 9x18 + СП-7 | blue band | 0.98 | REVIEW |
| gen_9x18Crafted | marker 9x18 + ПМ | brown | 0.997 vs FMJ | REVIEW | shape-locked; no кустарный |
| gen_9x18substandart | 9x18 + 57-Н-181С | olive | 0.998 vs FMJ | REVIEW | dark index stamp (no tape overlay) |

Side all: **ПМ** + ★  
Next caliber only after owner PASS.

## Tooling
- `docs/tools/_lock_ammo_icon_silhouette.py` (`--key magenta`, soft AA choke)
- `docs/tools/_finalize_ammo_gen_batch.py`
- `Ammopics/_gen/QA.md`
