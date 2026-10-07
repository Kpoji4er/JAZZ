param([string]$GameCsv, [string]$Build)
$ErrorActionPreference = 'Stop'
$ids = @((Get-Content (Join-Path $Build 'final-plan.localization.json') -Raw -Encoding UTF8 | ConvertFrom-Json).ID)
. (Join-Path $PSScriptRoot '../../scripts/localization/audit-localization.ps1') `
    -GameCsv $GameCsv -UpdateCatalog `
    -RussianCsv (Join-Path $Build 'Russian.csv') `
    -EnglishCsv (Join-Path $Build 'English.csv') `
    -RussianManualCsv (Join-Path $Build 'RussianManual.csv') `
    -EnglishManualCsv (Join-Path $Build 'EnglishManual.csv') `
    -CatalogPath (Join-Path $Build 'Strings.csv') `
    -CollisionPath (Join-Path $Build 'Collisions.csv')
$catalogRows = @($catalogRows | Where-Object { $_.ID -in $ids })
if ($catalogRows.Count -ne $ids.Count) { throw 'Incomplete mercenary catalog selection' }
Export-EngineLocalizationTable -Language Russian -Path (Join-Path $Build 'export-Russian.csv')
Export-EngineLocalizationTable -Language English -Path (Join-Path $Build 'export-English.csv')
