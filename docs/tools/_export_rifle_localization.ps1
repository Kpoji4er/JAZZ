param([string]$GameCsv, [string]$Build, [string]$TextManifest)
$ErrorActionPreference = 'Stop'
$audit = Join-Path $PSScriptRoot '../../scripts/localization/audit-localization.ps1'
# Run the full audit and preserve its diagnostics, but export only this change's
# selected IDs through the canonical exporter. Unrelated existing collisions are
# neither rewritten nor relabelled as passing.
. $audit -GameCsv $GameCsv -UpdateCatalog `
    -RussianManualCsv (Join-Path $Build 'RussianManual.csv') `
    -CatalogPath (Join-Path $Build 'Strings.csv') `
    -CollisionPath (Join-Path $Build 'Collisions.csv')
$rifleTexts = Get-Content -LiteralPath $TextManifest -Raw -Encoding UTF8 | ConvertFrom-Json
$rifleIds = @($rifleTexts.PSObject.Properties | ForEach-Object { [string]$_.Value[0] })
$catalogRows = @($catalogRows | Where-Object { $_.ID -in $rifleIds })
if ($catalogRows.Count -ne $rifleIds.Count) { throw 'Incomplete rifle catalog selection' }
Export-EngineLocalizationTable -Language Russian -Path (Join-Path $Build 'Russian.csv')
Export-EngineLocalizationTable -Language English -Path (Join-Path $Build 'English.csv')
