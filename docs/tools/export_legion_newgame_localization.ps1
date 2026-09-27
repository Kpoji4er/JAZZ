param([Parameter(Mandatory=$true)][string]$GameCsv, [Parameter(Mandatory=$true)][string]$Build,
    [string]$RussianManualCsv, [string]$EnglishManualCsv)
$ErrorActionPreference = 'Stop'
$audit = Join-Path $PSScriptRoot '../../scripts/localization/audit-localization.ps1'
# Keep full audit findings; export this feature's IDs without rewriting unrelated
# translations or concealing their pre-existing collisions.
. $audit -GameCsv $GameCsv -UpdateCatalog `
    -RussianManualCsv $RussianManualCsv -EnglishManualCsv $EnglishManualCsv `
    -CatalogPath (Join-Path $Build 'Strings.csv') `
    -CollisionPath (Join-Path $Build 'Collisions.csv')
$legionIds = 1..8 | ForEach-Object { '718927001{0:000}' -f $_ }
$catalogRows = @($catalogRows | Where-Object { $_.ID -in $legionIds })
if ($catalogRows.Count -ne 8) { throw 'Incomplete Legion new-game catalog selection' }
Export-EngineLocalizationTable -Language Russian -Path (Join-Path $Build 'Russian.csv')
Export-EngineLocalizationTable -Language English -Path (Join-Path $Build 'English.csv')
