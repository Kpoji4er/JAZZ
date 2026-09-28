# VZ58 / Vektor R4 material pass — 2026-09-27

Installed locally: 24 DDS files (12 full-size + 12 fallback), VZ58 side icon, R4 mesh. Install backup and SHA256 manifest: install/backup and install/install-report.json. Audit: install/audit.json. No commit or publication.

VZ58: dark longitudinal walnut-style furniture referenced from installed AKMFullStock/AKMHandguard. Two albedo atlases replaced. Steel normal amplitude 0.22, magazine 0.30; wood 0.08; metal roughness floor 0.66. Existing wood roughness floor 0.72 preserved. Source UV/geometry unchanged. Icon RGBA 324x165, separate orthographic side camera.

R4: metal normal amplitude 0.22, nonmetal 0.45; metal roughness floor 0.62. Hard joins separated above 60 degrees without custom normals. Removed exactly one near-collinear triangle, area 1.5716e-9 m2. 13508 triangles remain. Other corner positions and UV pairs unchanged. Native AssetsProcessor no longer reports zero-length normals. HGM audit passes with max position error 0.026 mm and zero reversed-area fraction. All Blender corner normals nonzero.

Original PNGs compared byte-for-byte with user archives: 18 VZ58 classic + 5 R4 match. Direct green-channel flip did not resolve the shading in offline A/B. Reducing map amplitude and preserving mechanical edges improves the preview, but does not establish that the original bake's tangent basis is correct. Final game lighting/editor round-trip still unverified.

Optics: INSTALLED after the user confirmed closing the game and no game processes remained. Closed + compact + EOTech + M68, using existing generic Scope visuals. items/companion equality, Lua parse and 352 allowed configurations PASS. RIS requirement retained. Catalog updated from 13 to 16 options; generated wiki build/check PASS. Metadata unchanged. Editor/runtime round-trip still pending.

Validation: installed SHA256/format/size/fallback/normal RMS check PASS; VZ58 resource/static gate PASS; R4 compiled mesh/winding/surface/UV/corner-normal checks PASS. The broader existing _check_r4.py definition gate fails on missing explicit BurstShots (unmodified InventoryItem/VektorR4.lua); not an asset failure. Baseline suite generated sync: 6383 blocking / 1649 warnings before changes. No global cleanup attempted.

ImageGen used the built-in image tool. Final PNG sources copied to wood/Wood_Base.png and wood/StockWood_Base.png; consumed in compiled DDS. Prompts:

1. Edit image 1, a square UV texture atlas for a videogame rifle. Image 2 is ONLY wood color and grain reference. Output the edited atlas image 1 at 2048x2048. Replace all mottled orange granular particleboard/bakelite brown regions with dark reddish walnut laminated gunstock wood matching image 2, long flowing directional grain, subtle layers, matte oiled satin, subdued contrast. Absolutely eliminate curly speckles/chips. Preserve every UV island boundary, position, silhouette, screw hole and grey metal part EXACTLY in image 1. Do not copy layout of image 2. Every brown island is wood and should have long grain along its length; grey metal must be unchanged. Flat albedo texture, no new lighting, no perspective, no new objects, no text.

2. Edit image 1, square UV texture atlas of rifle stock. Image 2 is ONLY reference for dark reddish walnut laminated wood color and long grain. Output edited image 1 at 2048x2048. Replace every brown granular particleboard/bakelite area with dark reddish brown laminated walnut, long flowing grain parallel to each stock island length, subdued matte oiled finish matching image 2. Eliminate curly chip speckles. Preserve EXACT pixel layout and silhouettes of image 1 UV islands, all borders, holes and grey metal parts. Do not copy layout of image 2. Flat albedo atlas no added lighting no perspective no labels. Grey metal is unchanged.

Post-change global sync returned the same 6383 pre-existing blocking issues plus two review-copy artifacts under optics/staged and optics/backup. Snapshot copies were renamed to .txt, and the tool now uses .txt by default so they cannot be discovered as active Lua companions. There were no VZ58/R4 errors outside those review copies.

Final strict sync after snapshot correction: RESULT: FAILED (6383 blocking issue(s), 1649 warning(s)). Error multiset matches the pre-change baseline exactly; no new errors and no VZ58/R4-scoped errors. Spec DoD remains blocked only by existing AC-003 editor/runtime acceptance.
