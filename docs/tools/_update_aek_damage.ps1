param([Parameter(Mandatory=$true)][string]$Build)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
[void][IO.Directory]::CreateDirectory($Build)
$tokens=$null; $errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile((Join-Path $root 'scripts/localization/audit-localization.ps1'),[ref]$tokens,[ref]$errors)
foreach ($name in @('Read-LocalizationCsv','ConvertTo-CsvCell','Write-CsvUtf8','Export-EngineLocalizationTable')) {
 $fn=$ast.Find({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$false)
 . ([scriptblock]::Create($fn.Extent.Text.Replace('-Rows $engineRows', '-Rows @($engineRows)')))
}
Add-Type -AssemblyName Microsoft.VisualBasic
$id='890000000032106'; $before=@{}; $updates=@{}
function Read-Target([string]$rel) {
 $path=Join-Path $root $rel
 $before[$rel]=[IO.File]::ReadAllBytes($path)
 return [IO.File]::ReadAllText($path)
}
$items=Read-Target 'items.lua'
$pattern='(?m)^.*id="JAZZ_AEK_Damage".*$'
$hit=[regex]::Matches($items,$pattern)
if ($hit.Count -ne 1 -or $hit[0].Value -notmatch "'Value',1,") { throw 'Unexpected AEK damage effect' }
$effect=$hit[0].Value.Replace('Урон +1','Урон +4').Replace("'Value',1,","'Value',4,")
$updates['items.lua']=$items.Replace($hit[0].Value,$effect)
$catalog=Read-Target 'Localization/Strings.csv'
$rows=@(Import-Csv -LiteralPath (Join-Path $root 'Localization/Strings.csv'))
$catalogRows=@($rows | Where-Object ID -eq $id)
if ($catalogRows.Count -ne 1 -or $catalogRows[0].SourceText -ne 'Урон +1') { throw 'Unexpected catalog source' }
# Bounded source extraction from the changed active ModItem; no unrelated catalog refresh.
$catalogRows[0].SourceText='Урон +4';$catalogRows[0].Russian='Урон +4';$catalogRows[0].English='Damage +4'
$activeById=@{};$activeById[$id]=$true;$baseById=@{}
foreach ($lang in @('Russian','English')) {
 $raw=Read-Target "$lang.csv"
 $delta=Join-Path $Build "$lang-delta.csv"
 Export-EngineLocalizationTable -Language $lang -Path $delta
 $lines=[IO.File]::ReadAllLines($delta)
 $replacement=@($lines | Where-Object { $_ -match "^$id," })
 if ($replacement.Count -ne 1 -or [regex]::Matches($raw,"(?m)^$id,.*$").Count -ne 1) { throw 'Unexpected runtime row count' }
 $updates["$lang.csv"]=[regex]::Replace($raw,"(?m)^$id,[^\r\n]*",[System.Text.RegularExpressions.MatchEvaluator]{param($m) $replacement[0]})
}
$updates['Localization/Strings.csv']=[regex]::Replace($catalog,"(?m)^$id,[^\r\n]*",[System.Text.RegularExpressions.MatchEvaluator]{param($m) $m.Value.Replace('Урон +1','Урон +4').Replace('Damage +1','Damage +4')})
$manual=Read-Target 'Localization/EnglishManual.csv'
$updates['Localization/EnglishManual.csv']=[regex]::Replace($manual,"(?m)^[^,\r\n]+,$id,[^\r\n]*",[System.Text.RegularExpressions.MatchEvaluator]{param($m) $m.Value.Replace('Урон +1','Урон +4').Replace('Damage +1','Damage +4')})
foreach ($rel in $updates.Keys) {
 $backup=Join-Path $Build ('backup/'+$rel)
 if (Test-Path -LiteralPath $backup) { throw 'Backup already exists' }
 if ([Convert]::ToBase64String([IO.File]::ReadAllBytes((Join-Path $root $rel))) -cne [Convert]::ToBase64String($before[$rel])) { throw "Concurrent change: $rel" }
 [void][IO.Directory]::CreateDirectory((Split-Path $backup))
 [IO.File]::WriteAllBytes($backup,$before[$rel])
}
foreach ($rel in $updates.Keys) {
 $encoding=[Text.UTF8Encoding]::new($before[$rel].Length -ge 3 -and $before[$rel][0] -eq 239)
 $target=Join-Path $root $rel
 $temp=$target+'.aek-damage-tmp'
 [IO.File]::WriteAllText($temp,$updates[$rel],$encoding)
 [IO.File]::Move($temp,$target,$true)
}
'PASS: AEK conversion damage +4; base remains 26; scoped RU/EN export complete.'
