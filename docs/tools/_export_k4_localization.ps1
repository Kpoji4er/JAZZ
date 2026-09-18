param([string]$GameCsv, [string]$Build)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '../../scripts/localization/audit-localization.ps1') -GameCsv $GameCsv -UpdateCatalog `
    -RussianManualCsv (Join-Path $Build 'RussianManual.csv') `
    -CatalogPath (Join-Path $Build 'Strings.csv') `
    -CollisionPath (Join-Path $Build 'Collisions.csv')
$k4Ids = @(101..109 | ForEach-Object { "761915400$_" })
$catalogRows = @($catalogRows | Where-Object { $_.ID -in $k4Ids })
if ($catalogRows.Count -ne 9) { throw 'Incomplete K4 catalog selection' }
foreach ($row in $catalogRows) {
    if ($row.Status -match 'collision|needs-russian|needs-english') { throw "Unresolved K4 row $($row.ID): $($row.Status)" }
}
Export-EngineLocalizationTable -Language Russian -Path (Join-Path $Build 'Russian.csv')
Export-EngineLocalizationTable -Language English -Path (Join-Path $Build 'English.csv')
