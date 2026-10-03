param([Parameter(Mandatory=$true)][string]$Build)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$audit=Join-Path $root 'scripts/localization/audit-localization.ps1'
$tokens=$null; $errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile($audit,[ref]$tokens,[ref]$errors)
if ($errors.Count) { throw 'Canonical localization script has parser errors' }
# Use the canonical parser, collision gate and CSV exporter for the scoped delta.
# Global audit failure remains recorded; unrelated translations are not regenerated.
foreach ($name in @('Read-LocalizationCsv','ConvertTo-CsvCell','Write-CsvUtf8','Export-EngineLocalizationTable')) {
 $function=$ast.Find({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$false)
 if (-not $function) { throw "Missing canonical function $name" }
 . ([scriptblock]::Create($function.Extent.Text))
}
Add-Type -AssemblyName Microsoft.VisualBasic
$catalogRows=@(Import-Csv -LiteralPath (Join-Path $Build 'localization-stage/Strings.csv') | Where-Object { $_.ID -match '^89000000003210[1-9]$' })
if ($catalogRows.Count -ne 9) { throw 'Expected all nine AEK localization IDs' }
$activeById=@{}; $baseById=@{}
foreach ($row in $catalogRows) {
 if (-not $row.Russian -or -not $row.English -or $row.Status -match 'collision') { throw "Invalid AEK translation $($row.ID)" }
 $activeById[$row.ID]=$true
}
$updates=@{}; $before=@{}
foreach ($lang in @('Russian','English')) {
 $deltaPath=Join-Path $Build "localization-stage/AEK-$lang.csv"
 Export-EngineLocalizationTable -Language $lang -Path $deltaPath
 $target=Join-Path $root "$lang.csv"
 $before[$target]=[IO.File]::ReadAllBytes($target)
 $existing=Read-LocalizationCsv $target
 $delta=Read-LocalizationCsv $deltaPath
 $rows=$existing.Rows.ToArray()
 foreach ($row in $rows) { if ($activeById.ContainsKey([string]$row.ID)) { throw 'AEK already localized' } }
 $merged=Join-Path $Build "localization-stage/Complete-$lang.csv"
 Write-CsvUtf8 -Path $merged -Columns @('ID','Text','Translation','VoiceActor','Context') -Rows ($rows+$delta.Rows.ToArray()) -Prefix @('sep=,')
 $verified=Read-LocalizationCsv $merged
 if ($verified.Rows.Count -ne $rows.Count+9) { throw 'Localization row count changed unexpectedly' }
 for ($i=0;$i -lt $rows.Count;$i++) {
  foreach ($field in @('ID','Text','Translation','VoiceActor','Context')) {
   if ([string]$rows[$i].$field -cne [string]$verified.Rows[$i].$field) { throw "Existing $lang translation changed" }
  }
 }
 $updates[$target]=[IO.File]::ReadAllBytes($merged)
}
$catalog=Join-Path $root 'Localization/Strings.csv'
$before[$catalog]=[IO.File]::ReadAllBytes($catalog)
$oldCatalog=@(Import-Csv -LiteralPath $catalog)
if (@($oldCatalog | Where-Object { $activeById.ContainsKey([string]$_.ID) }).Count) { throw 'AEK already in working catalog' }
$newCatalog=Join-Path $Build 'localization-stage/Complete-Strings.csv'
Write-CsvUtf8 -Path $newCatalog -Columns @('ID','SourceText','VanillaText','Russian','English','Status','Context','Packages','Locations','Notes') -Rows ($oldCatalog+$catalogRows)
$updates[$catalog]=[IO.File]::ReadAllBytes($newCatalog)
foreach ($target in $before.Keys) {
 if ([Convert]::ToBase64String([IO.File]::ReadAllBytes($target)) -cne [Convert]::ToBase64String($before[$target])) { throw "Concurrent edit: $target" }
}
foreach ($target in $updates.Keys) {
 $backup=Join-Path $Build ('localization-backup/'+[IO.Path]::GetFileName($target))
 if (Test-Path -LiteralPath $backup) { throw 'Localization backup already exists' }
 [void][IO.Directory]::CreateDirectory((Split-Path $backup))
 [IO.File]::WriteAllBytes($backup,$before[$target])
 [IO.File]::WriteAllBytes($target,$updates[$target])
}
Write-Output 'PASS scoped AEK catalog + RU/EN: nine IDs, existing runtime rows preserved. Global localization audit remains blocked by unrelated data.'
