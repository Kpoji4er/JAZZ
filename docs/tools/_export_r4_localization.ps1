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
$r4Ids = @('890000000019401', '890000000019402', '890000000019403')
$catalogRows = @($catalogRows | Where-Object { $_.ID -in $r4Ids })
if ($catalogRows.Count -ne 3) { throw 'Incomplete VektorR4 catalog selection' }
Export-EngineLocalizationTable -Language Russian -Path (Join-Path $Build 'Russian.csv')
Export-EngineLocalizationTable -Language English -Path (Join-Path $Build 'English.csv')
