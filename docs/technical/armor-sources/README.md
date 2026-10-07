# Исходники брони, касок и одежды

Каталог существующих локальных исходников. Обновление: `python docs/tools/_catalog_armor_sources.py`.

Сохранять оригинальный GLB с текстурами и metadata задания, очищенную геометрию, исходные карты, сцену с ригом и сцену экспорта. Новую посадку делать в отдельном каталоге под целевое тело; не перезаписывать оригинал или ранее принятый риг. Бинарные исходники лежат в `jazz_assets/Sources/Character`, ссылки и инвентарь — здесь. Наличие в каталоге не означает, что файл закоммичен или имеет внешнюю резервную копию.

Текущий импорт PASGT/RBA: `import-20261007/original` — неизменный оригинал и SHA256; `clean` — подгонка; `source` — Male rig; `clothed` — LegionGoon Shirt08 reference; `build` — финальная сцена и TGA. Для других тел требуется новая подгонка/риг. Helmet meshes — rigid Head attachments; их origin, offset и scale также нужно сохранять при переносе.

Старые варианты не считаются автоматически актуальными. Для выбора установленной версии сверяться с installation receipt, mapping и журналом игровой приёмки. Здесь не заявляется полнота архива для ванильных моделей или прежних HAV: отсутствующие исходники нужно восстановить отдельно.

## JAZZ_6B13_Male

<details>
<summary>Исходные файлы: 24</summary>

- [jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/6B13_clean.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/6B13_clean.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/6B13_clean.glb](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/6B13_clean.glb>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/6B13_raw.glb](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/6B13_raw.glb>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/6B13_textured.glb](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/6B13_textured.glb>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/working.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/meshy_output/20261003_131104_6b13-geometry_01a1013e/working.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/build/JAZZ_6B13_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/clean/JazzArmor_6B13.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/clean/JazzArmor_6B13.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/clean/JazzArmor_6B13_repaired.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/clean/JazzArmor_6B13_repaired.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/clothed/clothed.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/clothed/clothed.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/source/6B13.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/production-20261003/source/6B13.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/6B13_wider.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/6B13_wider.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B13_Male/width-review-20261003/build/JAZZ_6B13_Male_Rough.tga>)

</details>

## JAZZ_6B3_Male

<details>
<summary>Исходные файлы: 32</summary>

- [jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/build/JAZZ_6B3_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/source/6B3.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/cuirass-rig-20261003/source/6B3.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/build/JAZZ_6B3_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/clean/JazzArmor_6B3.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/clean/JazzArmor_6B3.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/source/6B3.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/source/6B3.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-rg-roughness/build/JAZZ_6B3_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/build/JAZZ_6B3_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/source/6B3.blend](<../../../../jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002-torso-shoulders/source/6B3.blend>)

</details>

## JAZZ_Chainmail_Male

<details>
<summary>Исходные файлы: 53</summary>

- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Color.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Color.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/build/JAZZ_Chainmail_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v10-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v10-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v11-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v11-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v12-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v12-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Color.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Color.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/build/JAZZ_Chainmail_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v13-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v2-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v2-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Color.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Color.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/build/JAZZ_Chainmail_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v3-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v4-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v4-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Color.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Color.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/build/JAZZ_Chainmail_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v5-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v6-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v6-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v7-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v7-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v8-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v8-20261003/source/Chainmail.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Color.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Color.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/build/JAZZ_Chainmail_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/source/Chainmail.blend](<../../../../jazz_assets/Sources/Character/JAZZ_Chainmail_Male/meshy-body-v9-20261003/source/Chainmail.blend>)

</details>

## JAZZ_IBAFull_Male

<details>
<summary>Исходные файлы: 2</summary>

- [jazz_assets/Sources/Character/JAZZ_IBAFull_Male/meshy-20261008/20261008_015743_ibafull_01a11895/original/model.glb](<../../../../jazz_assets/Sources/Character/JAZZ_IBAFull_Male/meshy-20261008/20261008_015743_ibafull_01a11895/original/model.glb>)
- [jazz_assets/Sources/Character/JAZZ_IBAFull_Male/meshy-20261008/20261008_015743_ibafull_01a11895/original/model.pre_remeshed.glb](<../../../../jazz_assets/Sources/Character/JAZZ_IBAFull_Male/meshy-20261008/20261008_015743_ibafull_01a11895/original/model.pre_remeshed.glb>)

</details>

## JAZZ_IBALight_Male

<details>
<summary>Исходные файлы: 2</summary>

- [jazz_assets/Sources/Character/JAZZ_IBALight_Male/meshy-20261008/20261008_015741_ibalight_01a11895/original/model.glb](<../../../../jazz_assets/Sources/Character/JAZZ_IBALight_Male/meshy-20261008/20261008_015741_ibalight_01a11895/original/model.glb>)
- [jazz_assets/Sources/Character/JAZZ_IBALight_Male/meshy-20261008/20261008_015741_ibalight_01a11895/original/model.pre_remeshed.glb](<../../../../jazz_assets/Sources/Character/JAZZ_IBALight_Male/meshy-20261008/20261008_015741_ibalight_01a11895/original/model.pre_remeshed.glb>)

</details>

## JAZZ_IBA_Male

<details>
<summary>Исходные файлы: 2</summary>

- [jazz_assets/Sources/Character/JAZZ_IBA_Male/meshy-20261008/20261008_015742_iba_01a11895/original/model.glb](<../../../../jazz_assets/Sources/Character/JAZZ_IBA_Male/meshy-20261008/20261008_015742_iba_01a11895/original/model.glb>)
- [jazz_assets/Sources/Character/JAZZ_IBA_Male/meshy-20261008/20261008_015742_iba_01a11895/original/model.pre_remeshed.glb](<../../../../jazz_assets/Sources/Character/JAZZ_IBA_Male/meshy-20261008/20261008_015742_iba_01a11895/original/model.pre_remeshed.glb>)

</details>

## JAZZ_LeatherArmor_Male

<details>
<summary>Исходные файлы: 18</summary>

- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/build/JAZZ_LeatherArmor_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/source/LeatherArmor.blend](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/cuirass-rig-20261003/source/LeatherArmor.blend>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/build/JAZZ_LeatherArmor_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/clean/JazzArmor_6B3.blend](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/clean/JazzArmor_6B3.blend>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/reduced.glb](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/reduced.glb>)
- [jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/source/LeatherArmor.blend](<../../../../jazz_assets/Sources/Character/JAZZ_LeatherArmor_Male/meshy-20261003/source/LeatherArmor.blend>)

</details>

## JAZZ_PASGT_Male

<details>
<summary>Исходные файлы: 56</summary>

- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/build/JAZZ_PASGT_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/clean/JazzArmor_PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/clean/JazzArmor_PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/clothed/clothed.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/clothed/clothed.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/source/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/fit-woodland-20261008/source/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/build/JAZZ_PASGT_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/clean/JazzArmor_PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/clean/JazzArmor_PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/clothed/clothed.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/clothed/clothed.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/original/PASGT.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/original/PASGT.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/source/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/import-20261007/source/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-20261004/clean/JazzArmor_PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-20261004/clean/JazzArmor_PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-20261004/clothed/clothed.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-20261004/clothed/clothed.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-20261004/rig/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-20261004/rig/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/20261008_002739_pasgt_01a11843/original/model.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/20261008_002739_pasgt_01a11843/original/model.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/20261008_002739_pasgt_01a11843/original/model.pre_remeshed.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/20261008_002739_pasgt_01a11843/original/model.pre_remeshed.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v1/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v1/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v1/PASGT.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v1/PASGT.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v2/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v2/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v2/PASGT.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v2/PASGT.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v3/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v3/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v3/PASGT.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/clean-v3/PASGT.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-large-v1/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-large-v1/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-large-v1/PASGT.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-large-v1/PASGT.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-masked-v1/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-masked-v1/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-masked-v1/PASGT.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-masked-v1/PASGT.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-masked-v1/PASGT_olive.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-masked-v1/PASGT_olive.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-reference-raw/model.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-reference-raw/model.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-reference-v2/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-reference-v2/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-reference-v2/PASGT.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-reference-v2/PASGT.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-v1/model.glb](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/meshy-regeneration-20261008/woodland-v1/model.glb>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-panel-20261008/clean/PASGT_rebuilt.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-panel-20261008/clean/PASGT_rebuilt.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-panel-20261008/clothed/clothed.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-panel-20261008/clothed/clothed.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-panel-20261008/source/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-panel-20261008/source/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/build/JAZZ_PASGT_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/clothed/clothed.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/clothed/clothed.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/source/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/rear-repair-20261008/source/PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/shape-preserved-20261007/clean/JazzArmor_PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/shape-preserved-20261007/clean/JazzArmor_PASGT.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/shape-preserved-20261007/clothed/clothed.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/shape-preserved-20261007/clothed/clothed.blend>)
- [jazz_assets/Sources/Character/JAZZ_PASGT_Male/shape-preserved-20261007/source/PASGT.blend](<../../../../jazz_assets/Sources/Character/JAZZ_PASGT_Male/shape-preserved-20261007/source/PASGT.blend>)

</details>

## JAZZ_RBA_Male

<details>
<summary>Исходные файлы: 14</summary>

- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/build/JAZZ_RBA_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/clean/JazzArmor_RBA.blend](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/clean/JazzArmor_RBA.blend>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/clothed/clothed.blend](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/clothed/clothed.blend>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/original/RBA.glb](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/original/RBA.glb>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/source/RBA.blend](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/import-20261007/source/RBA.blend>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/shape-preserved-20261007/clean/JazzArmor_RBA.blend](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/shape-preserved-20261007/clean/JazzArmor_RBA.blend>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/shape-preserved-20261007/clothed/clothed.blend](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/shape-preserved-20261007/clothed/clothed.blend>)
- [jazz_assets/Sources/Character/JAZZ_RBA_Male/shape-preserved-20261007/source/RBA.blend](<../../../../jazz_assets/Sources/Character/JAZZ_RBA_Male/shape-preserved-20261007/source/RBA.blend>)

</details>

## JAZZ_TireArmor_Male

<details>
<summary>Исходные файлы: 10</summary>

- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/build/JAZZ_TireArmor_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/clean/JazzArmor_6B3.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/clean/JazzArmor_6B3.blend>)
- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/reduced.glb](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/reduced.glb>)
- [jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/source/TireArmor.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireArmor_Male/meshy-20261003/source/TireArmor.blend>)

</details>

## JAZZ_TireBrigantine_Male

<details>
<summary>Исходные файлы: 26</summary>

- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/build/JAZZ_TireBrigantine_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/source/TireBrigantine.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-20261003/source/TireBrigantine.blend>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/build/JAZZ_TireBrigantine_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/source/TireBrigantine.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/cuirass-rig-v2-20261003/source/TireBrigantine.blend>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male.blend>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male.fbx](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male.fbx>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_Base.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_Base.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_Metal.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_Metal.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_Norm.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_Norm.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_RM.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_RM.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_Rough.tga](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/build/JAZZ_TireBrigantine_Male_Rough.tga>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/clean/JazzArmor_6B3.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/clean/JazzArmor_6B3.blend>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/reduced.glb](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/reduced.glb>)
- [jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/source/TireBrigantine.blend](<../../../../jazz_assets/Sources/Character/JAZZ_TireBrigantine_Male/meshy-20261003/source/TireBrigantine.blend>)

</details>

## JazzHat_6B7

<details>
<summary>Исходные файлы: 37</summary>

- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7.fbx](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7.fbx>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7_Base.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7_Base.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7_Norm.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7_Norm.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7_RM.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/build/JazzHat_6B7_RM.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/head-fit.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/head-fit.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_clean.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_clean.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_clean.glb](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_clean.glb>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_procedural.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_procedural.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_raw.glb](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_raw.glb>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_textured.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_textured.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_textured.glb](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/6B7_1M_textured.glb>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_Base.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_Base.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_Metal.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_Metal.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_Norm.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_Norm.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_ORM.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_ORM.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_RM.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_RM.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_Rough.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/textures/6B7_1M_Rough.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/working.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-1m-20261003/source/working.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7.fbx](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7.fbx>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7_Base.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7_Base.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7_Norm.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7_Norm.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7_RM.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/build/JazzHat_6B7_RM.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/head-fit.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/head-fit.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_clean.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_clean.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_clean.glb](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_clean.glb>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_procedural.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_procedural.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_raw.glb](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_raw.glb>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_textured.blend](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_textured.blend>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_textured.glb](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/6B7_textured.glb>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_Base.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_Base.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_Metal.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_Metal.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_Norm.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_Norm.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_ORM.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_ORM.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_RM.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_RM.tga>)
- [jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_Rough.tga](<../../../../jazz_assets/Sources/Character/JazzHat_6B7/meshy-20261003/source/textures/6B7_Rough.tga>)

</details>

## JazzHat_SSh68

<details>
<summary>Исходные файлы: 22</summary>

- [jazz_assets/Sources/Character/JazzHat_SSh68/JazzHat_SSh68.blend](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/JazzHat_SSh68.blend>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/JazzHat_SSh68_Base.tga](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/JazzHat_SSh68_Base.tga>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/JazzHat_SSh68_Norm.tga](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/JazzHat_SSh68_Norm.tga>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/JazzHat_SSh68_RM.tga](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/JazzHat_SSh68_RM.tga>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68.blend](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68.blend>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68.fbx](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68.fbx>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68_Base.tga](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68_Base.tga>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68_Norm.tga](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68_Norm.tga>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68_RM.tga](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/build/JazzHat_SSh68_RM.tga>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/head-fit.blend](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/head-fit.blend>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_finished.blend](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_finished.blend>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_procedural.blend](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_procedural.blend>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_raw.glb](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_raw.glb>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_shell.blend](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_shell.blend>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_textured.blend](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_textured.blend>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_textured.glb](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-20261003/source/SSh60_textured.glb>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68.blend](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68.blend>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68.fbx](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68.fbx>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68_Base.tga](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68_Base.tga>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68_Norm.tga](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68_Norm.tga>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68_RM.tga](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/build/JazzHat_SSh68_RM.tga>)
- [jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/head-fit.blend](<../../../../jazz_assets/Sources/Character/JazzHat_SSh68/ssh60-fit-20261003/head-fit.blend>)

</details>

## Originals and earlier candidates

<details>
<summary>Исходные файлы: 31</summary>

- [jazz/meshy_output/armor-batch-20261002/20261002_010752_improvisedcuirass_01a0f982/ImprovisedCuirass.glb](<../../../../jazz/meshy_output/armor-batch-20261002/20261002_010752_improvisedcuirass_01a0f982/ImprovisedCuirass.glb>)
- [jazz/meshy_output/armor-batch-20261002/20261002_010811_chainmail_01a0f982/Chainmail.glb](<../../../../jazz/meshy_output/armor-batch-20261002/20261002_010811_chainmail_01a0f982/Chainmail.glb>)
- [jazz/meshy_output/armor-batch-20261002/20261002_010817_tirebrigantine_01a0f982/TireBrigantine.glb](<../../../../jazz/meshy_output/armor-batch-20261002/20261002_010817_tirebrigantine_01a0f982/TireBrigantine.glb>)
- [jazz/meshy_output/armor-batch-20261002/20261002_010902_tirearmor_01a0f982/TireArmor.glb](<../../../../jazz/meshy_output/armor-batch-20261002/20261002_010902_tirearmor_01a0f982/TireArmor.glb>)
- [jazz/meshy_output/armor-batch-20261002/20261002_010909_leatherarmor_01a0f983/LeatherArmor.glb](<../../../../jazz/meshy_output/armor-batch-20261002/20261002_010909_leatherarmor_01a0f983/LeatherArmor.glb>)
- [jazz/meshy_output/armor-feedback-20261003/cuirass-source/audit.blend](<../../../../jazz/meshy_output/armor-feedback-20261003/cuirass-source/audit.blend>)
- [jazz/meshy_output/armor-feedback-20261003/cuirass-source/improvised_cuirass_v7.blend](<../../../../jazz/meshy_output/armor-feedback-20261003/cuirass-source/improvised_cuirass_v7.blend>)
- [jazz/meshy_output/chainmail-cleanup-20261002/candidate/Chainmail.blend](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/candidate/Chainmail.blend>)
- [jazz/meshy_output/chainmail-cleanup-20261002/candidate/Chainmail.glb](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/candidate/Chainmail.glb>)
- [jazz/meshy_output/chainmail-cleanup-20261002/normals/Chainmail.blend](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/normals/Chainmail.blend>)
- [jazz/meshy_output/chainmail-cleanup-20261002/normals/Chainmail.glb](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/normals/Chainmail.glb>)
- [jazz/meshy_output/chainmail-cleanup-20261002/reconstructed/Chainmail.blend](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/reconstructed/Chainmail.blend>)
- [jazz/meshy_output/chainmail-cleanup-20261002/reconstructed/Chainmail.glb](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/reconstructed/Chainmail.glb>)
- [jazz/meshy_output/chainmail-cleanup-20261002/reconstructed-v2/Chainmail.blend](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/reconstructed-v2/Chainmail.blend>)
- [jazz/meshy_output/chainmail-cleanup-20261002/reconstructed-v2/Chainmail.glb](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/reconstructed-v2/Chainmail.glb>)
- [jazz/meshy_output/chainmail-cleanup-20261002/reconstructed-v3/Chainmail.blend](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/reconstructed-v3/Chainmail.blend>)
- [jazz/meshy_output/chainmail-cleanup-20261002/reconstructed-v3/Chainmail.glb](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/reconstructed-v3/Chainmail.glb>)
- [jazz/meshy_output/chainmail-cleanup-20261002/relaxed/Chainmail.blend](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/relaxed/Chainmail.blend>)
- [jazz/meshy_output/chainmail-cleanup-20261002/relaxed/Chainmail.glb](<../../../../jazz/meshy_output/chainmail-cleanup-20261002/relaxed/Chainmail.glb>)
- [jazz/meshy_output/chainmail-game-armor-20261002/20261002_012142_chainmail-game-armor_01a0f98e/Chainmail.glb](<../../../../jazz/meshy_output/chainmail-game-armor-20261002/20261002_012142_chainmail-game-armor_01a0f98e/Chainmail.glb>)
- [jazz/meshy_output/chainmail-multiview-20261002/20261002_013545_chainmail-multiview_01a0f99b/Chainmail.glb](<../../../../jazz/meshy_output/chainmail-multiview-20261002/20261002_013545_chainmail-multiview_01a0f99b/Chainmail.glb>)
- [jazz/meshy_output/chainmail-textured-20261003/20261003_000857_chainmail-textured_01a0fe72/Chainmail_textured.blend](<../../../../jazz/meshy_output/chainmail-textured-20261003/20261003_000857_chainmail-textured_01a0fe72/Chainmail_textured.blend>)
- [jazz/meshy_output/chainmail-textured-20261003/20261003_000857_chainmail-textured_01a0fe72/Chainmail_textured.glb](<../../../../jazz/meshy_output/chainmail-textured-20261003/20261003_000857_chainmail-textured_01a0fe72/Chainmail_textured.glb>)
- [jazz/meshy_output/chainmail-textured-20261003/20261003_000857_chainmail-textured_01a0fe72/model.glb](<../../../../jazz/meshy_output/chainmail-textured-20261003/20261003_000857_chainmail-textured_01a0fe72/model.glb>)
- [jazz/meshy_output/chainmail-textured-20261003/clean/Chainmail_clean.blend](<../../../../jazz/meshy_output/chainmail-textured-20261003/clean/Chainmail_clean.blend>)
- [jazz/meshy_output/chainmail-textured-20261003/clean/Chainmail_clean.glb](<../../../../jazz/meshy_output/chainmail-textured-20261003/clean/Chainmail_clean.glb>)
- [jazz/meshy_output/legion-armor-20261003/20261003_010254_tirebrigantine_01a0fea3/TireBrigantine.glb](<../../../../jazz/meshy_output/legion-armor-20261003/20261003_010254_tirebrigantine_01a0fea3/TireBrigantine.glb>)
- [jazz/meshy_output/legion-armor-20261003/20261003_010256_tirearmor_01a0fea3/TireArmor.glb](<../../../../jazz/meshy_output/legion-armor-20261003/20261003_010256_tirearmor_01a0fea3/TireArmor.glb>)
- [jazz/meshy_output/legion-armor-20261003/20261003_010259_leatherarmor_01a0fea4/LeatherArmor.glb](<../../../../jazz/meshy_output/legion-armor-20261003/20261003_010259_leatherarmor_01a0fea4/LeatherArmor.glb>)
- [jazz/meshy_output/pasgt-multiview-20261004/20261004_043154_pasgt_01a10489/PASGT.glb](<../../../../jazz/meshy_output/pasgt-multiview-20261004/20261004_043154_pasgt_01a10489/PASGT.glb>)
- [jazz/meshy_output/rba-multiview-20261006/20261006_020925_rba_01a10e53/RBA.glb](<../../../../jazz/meshy_output/rba-multiview-20261006/20261006_020925_rba_01a10e53/RBA.glb>)

</details>
