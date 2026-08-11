# Remaining ammo icon gen plan — DONE (preview only)

All JAZZ ammo types now have locked previews in `Ammopics/_gen/gen_*.png` (**97** files).
Pipeline used: GenerateImage → `_lock_ammo_icon_silhouette.py --structure 0`.
Runtime `Ammopics/*.png` **not** replaced (except existing 9×18/9×19 still old until you say replace).

Notes:
- `.38 JHP` preview = `gen_38SpJHP.png` (runtime currently shares `38Sp.png` for both).
- `.50 BMG` was MISSING — previews `gen_50bmg_{basic,incendiary,he}.png` + sil `_sil_50bmg.png`.
- Oversized bases normalized: `_sil_357`, `_sil_30cal`, `_sil_792x33`.
- Spot QA only (not full Read of all 97). Re-gen FAIL types on request.