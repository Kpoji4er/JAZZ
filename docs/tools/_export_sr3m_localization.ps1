param([string]$GameCsv, [string]$Build)
$ErrorActionPreference = 'Stop'
$audit = Join-Path $PSScriptRoot '../../scripts/localization/audit-localization.ps1'
# Run the full audit and preserve its diagnostics, but export only this change's
# three IDs through the canonical exporter. Unrelated existing collisions are
# neither rewritten nor relabelled as passing.
. $audit -GameCsv $GameCsv -UpdateCatalog `
    -RussianManualCsv (Join-Path $Build 'RussianManual.csv') `
    -CatalogPath (Join-Path $Build 'Strings.csv') `
    -CollisionPath (Join-Path $Build 'Collisions.csv')
$sr3mIds = @('761915300101', '761915300102', '761915300103')
$catalogRows = @($catalogRows | Where-Object { $_.ID -in $sr3mIds })
if ($catalogRows.Count -ne 3) { throw 'Incomplete SR3M catalog selection' }
Export-EngineLocalizationTable -Language Russian -Path (Join-Path $Build 'Russian.csv')
Export-EngineLocalizationTable -Language English -Path (Join-Path $Build 'English.csv')
