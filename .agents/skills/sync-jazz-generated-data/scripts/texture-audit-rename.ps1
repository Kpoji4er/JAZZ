#Requires -Version 5.1
<#
.SYNOPSIS
  Audit / rename / dedupe / purge DDS textures in jazz_assets.

.DESCRIPTION
  Index Entities/Materials/*.mtl -> Name="*.dds", map slot->suffix, own by entity,
  content-hash dedupe, delete unused Textures(+Fallbacks), rename used numeric
  to Entity_MapType.dds, rewrite .mtl and items.lua 'texture' lists.

  Does NOT patch BinAssets/*.mtlbin - rebuild in Mod Editor after Apply.

.EXAMPLE
  .\texture-audit-rename.ps1 -AssetsRoot ..\jazz_assets -DryRun
  .\texture-audit-rename.ps1 -AssetsRoot ..\jazz_assets -Apply
  .\texture-audit-rename.ps1 -AssetsRoot ..\jazz_assets -EntityFilter AA52 -Apply
#>
[CmdletBinding(DefaultParameterSetName = 'DryRun')]
param(
  [Parameter(Mandatory = $true)]
  [string]$AssetsRoot,

  [Parameter(ParameterSetName = 'DryRun')]
  [switch]$DryRun,

  [Parameter(ParameterSetName = 'Apply')]
  [switch]$Apply,

  [string]$EntityFilter = '',

  [string]$ReportDir = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $DryRun -and -not $Apply) { $DryRun = $true }
if ($DryRun -and $Apply) { throw "Use either -DryRun or -Apply, not both." }

$AssetsRoot = (Resolve-Path -LiteralPath $AssetsRoot).Path
$texDir = Join-Path $AssetsRoot 'Entities\Textures'
$fbDir = Join-Path $texDir 'Fallbacks'
$mtlDir = Join-Path $AssetsRoot 'Entities\Materials'
$entDir = Join-Path $AssetsRoot 'Entities'
$itemsPath = Join-Path $AssetsRoot 'items.lua'

if (-not (Test-Path -LiteralPath $texDir)) { throw "Textures dir missing: $texDir" }
if (-not (Test-Path -LiteralPath $mtlDir)) { throw "Materials dir missing: $mtlDir" }

if (-not $ReportDir) {
  $ReportDir = Join-Path $AssetsRoot 'docs'
}
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

$slotSuffix = @{
  'BaseColorMap'    = 'Base'
  'NormalMap'       = 'Norm'
  'RMMap'           = 'RM'
  'AOMap'           = 'AO'
  'SpecialMap'      = 'SPEC'
  'SIMap'           = 'SI'
  'ColorizationMap' = 'Color'
}

$attachRe = [regex]'Mag|Barrel|Bipod|Stock|Grip|Scope|Iron|Optic|Muzzle|Knife|Flash|Suppress|Compens|Mount|Rail|Cover|Lid|Bolt|Hand|Receiver|Sight|Laser|Light|Gl|Under|Fold|Unfld|Fld'

function Test-IsNumericBasename([string]$name) {
  return $name -match '^\d+$'
}

function Get-OwnerScore([string]$name) {
  $penalty = 0
  if ($attachRe.IsMatch($name)) { $penalty += 10 }
  $penalty += ([regex]::Matches($name, '_')).Count
  $penalty += [Math]::Min($name.Length, 200) / 1000.0
  return $penalty
}

function Get-BestOwner {
  param([AllowEmptyCollection()][object[]]$Names = @())
  $flat = New-Object System.Collections.ArrayList
  foreach ($n in @($Names)) {
    if ($null -eq $n) { continue }
    # Never let a bare string be cast to char[]; keep whole tokens
    if ($n -is [string]) {
      if ($n.Length -gt 0) { [void]$flat.Add($n) }
    }
    else {
      foreach ($x in @($n)) {
        if ($null -ne $x -and "$x".Length -gt 0) { [void]$flat.Add("$x") }
      }
    }
  }
  $uniq = @($flat | Select-Object -Unique)
  $prefer = @($uniq | Where-Object { $_.Length -gt 1 })
  if ($prefer.Count -gt 0) { $uniq = $prefer }
  if ($uniq.Count -eq 0) { return 'Unknown' }
  return @($uniq | Sort-Object @{ Expression = { Get-OwnerScore $_ } }, @{ Expression = { $_.Length } }, @{ Expression = { $_ } })[0]
}

function Get-PlannedName([string]$basename, $rows) {
  if (-not (Test-IsNumericBasename $basename)) {
    return $basename
  }
  $allEnts = New-Object System.Collections.ArrayList
  $suffixes = New-Object System.Collections.ArrayList
  # Do not wrap Generic.List with @() - PSToObjectArrayBinder can throw ArgumentException
  $rowEnum = $rows
  if ($null -eq $rowEnum) { $rowEnum = @() }
  foreach ($row in $rowEnum) {
    if ($null -eq $row) { continue }
    $entVal = $row.Entities
    if ($entVal -is [string]) {
      [void]$allEnts.Add($entVal)
    }
    elseif ($null -ne $entVal) {
      foreach ($e in $entVal) {
        if ($null -ne $e -and "$e".Length -gt 0) { [void]$allEnts.Add("$e") }
      }
    }
    if ($row.Suffix) { [void]$suffixes.Add([string]$row.Suffix) }
  }
  $owner = Get-BestOwner -Names $allEnts.ToArray()
  $grouped = @($suffixes | Group-Object | Sort-Object Count -Descending)
  $suf = if ($grouped.Count -gt 0) { [string]$grouped[0].Name } else { 'Base' }
  $name = ($owner + '_' + $suf)
  return ($name -replace '_+', '_')
}

Write-Host "Indexing .ent -> material..."
$mtlToEntities = @{}
Get-ChildItem -LiteralPath $entDir -Filter '*.ent' -File | ForEach-Object {
  $entName = $_.BaseName
  $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
  foreach ($m in [regex]::Matches($content, 'Materials/([^"/]+\.mtl)')) {
    $mtlFile = $m.Groups[1].Value
    if (-not $mtlToEntities.ContainsKey($mtlFile)) {
      $mtlToEntities[$mtlFile] = New-Object System.Collections.Generic.List[string]
    }
    if (-not $mtlToEntities[$mtlFile].Contains($entName)) {
      $mtlToEntities[$mtlFile].Add($entName)
    }
  }
}

Write-Host "Indexing .mtl texture refs..."
# refRows: list of @{ Basename; Slot; Suffix; MtlFile; MtlStem; Entities }
$refRows = New-Object System.Collections.Generic.List[object]
$mtlFiles = Get-ChildItem -LiteralPath $mtlDir -Filter '*.mtl' -File
foreach ($mf in $mtlFiles) {
  $mtlFile = $mf.Name
  $mtlStem = $mf.BaseName
  if ($EntityFilter) {
    $ents = @()
    if ($mtlToEntities.ContainsKey($mtlFile)) { $ents = @($mtlToEntities[$mtlFile]) }
    $hit = ($mtlStem -like "*$EntityFilter*") -or ($ents | Where-Object { $_ -like "*$EntityFilter*" })
    if (-not $hit) { continue }
  }
  $text = Get-Content -LiteralPath $mf.FullName -Raw -Encoding UTF8
  foreach ($m in [regex]::Matches($text, '<(\w+Map)\s+Name="([^"]+\.dds)"')) {
    $slot = $m.Groups[1].Value
    $dds = $m.Groups[2].Value
    $base = [System.IO.Path]::GetFileNameWithoutExtension($dds)
    if (-not $slotSuffix.ContainsKey($slot)) {
      Write-Warning "Unknown slot $slot in $mtlFile ($dds) - skip"
      continue
    }
    $ents = @()
    if ($mtlToEntities.ContainsKey($mtlFile)) {
      $ents = @($mtlToEntities[$mtlFile] | ForEach-Object { "$_" })
    }
    if ($ents.Count -eq 0) {
      # Material stem often Entity_Mesh - take duplicate stem or first token
      if ($mtlStem -match '^(.+)_\1$') { $ents = @([string]$Matches[1]) }
      else {
        # Prefer full stem without trailing _mesh duplicate pieces: use material left side
        $ents = @([string]$mtlStem)
      }
    }
    $refRows.Add([pscustomobject]@{
        Basename = $base
        Slot     = $slot
        Suffix   = $slotSuffix[$slot]
        MtlFile  = $mtlFile
        MtlStem  = $mtlStem
        Entities = $ents
      })
  }
}

$referenced = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($r in $refRows) { [void]$referenced.Add($r.Basename) }

$texFiles = @(Get-ChildItem -LiteralPath $texDir -Filter '*.dds' -File)
$fbFiles = @()
if (Test-Path -LiteralPath $fbDir) {
  $fbFiles = @(Get-ChildItem -LiteralPath $fbDir -Filter '*.dds' -File)
}
$texSet = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$fbSet = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($f in $texFiles) { [void]$texSet.Add($f.BaseName) }
foreach ($f in $fbFiles) { [void]$fbSet.Add($f.BaseName) }

$unusedTex = @($texSet | Where-Object { -not $referenced.Contains($_) } | Sort-Object)
$fbOnly = @($fbSet | Where-Object { -not $texSet.Contains($_) } | Sort-Object)
$missing = @($referenced | Where-Object { -not $texSet.Contains($_) } | Sort-Object)

Write-Host ("Refs={0} Textures={1} Fallbacks={2} UnusedTex={3} FbOnly={4} Missing={5}" -f `
    $referenced.Count, $texSet.Count, $fbSet.Count, $unusedTex.Count, $fbOnly.Count, $missing.Count)

# Known broken MP7 ironsight -> reuse IronUnfld maps (exist on disk)
$missingRetarget = @{
  '8758000' = '8720001'  # Norm
  '8758001' = '8720002'  # Base
  '8758002' = '8720003'  # RM
}

if ($missing.Count -gt 0) {
  foreach ($m in $missing) {
    if ($missingRetarget.ContainsKey($m)) {
      Write-Host "Will retarget missing $m -> $($missingRetarget[$m])"
    }
    else {
      Write-Warning "Missing texture referenced by MTL with no retarget: $m"
    }
  }
}

# Apply retarget in-memory to refRows / referenced
foreach ($r in $refRows) {
  if ($missingRetarget.ContainsKey($r.Basename)) {
    $r.Basename = $missingRetarget[$r.Basename]
  }
}
$referenced = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($r in $refRows) { [void]$referenced.Add($r.Basename) }
$unusedTex = @($texSet | Where-Object { -not $referenced.Contains($_) } | Sort-Object)
$missing = @($referenced | Where-Object { -not $texSet.Contains($_) } | Sort-Object)

# Group refs by basename for owner/suffix
$byBase = @{}
foreach ($r in $refRows) {
  if (-not $byBase.ContainsKey($r.Basename)) {
    $byBase[$r.Basename] = New-Object System.Collections.ArrayList
  }
  [void]$byBase[$r.Basename].Add($r)
}

$planned = @{}  # basename -> planned name (pre-collision)
foreach ($bn in $byBase.Keys) {
  $planned[$bn] = Get-PlannedName $bn $byBase[$bn]
}

Write-Host "Hashing used textures (MD5)..."
$hashOf = @{}      # basename -> hash
$byHash = @{}      # hash -> list basenames
$usedOnDisk = @($referenced | Where-Object { $texSet.Contains($_) })
$i = 0
foreach ($bn in $usedOnDisk) {
  $i++
  if (($i % 200) -eq 0) { Write-Host "  hashed $i / $($usedOnDisk.Count)" }
  $path = Join-Path $texDir ($bn + '.dds')
  $h = (Get-FileHash -LiteralPath $path -Algorithm MD5).Hash
  $hashOf[$bn] = $h
  if (-not $byHash.ContainsKey($h)) {
    $byHash[$h] = New-Object System.Collections.Generic.List[string]
  }
  if (-not $byHash[$h].Contains($bn)) { $byHash[$h].Add($bn) }
}

# Content merge: only within the SAME planned suffix (never Norm<->Base etc.)
$finalOf = @{}  # basename -> final basename
foreach ($h in $byHash.Keys) {
  $group = @($byHash[$h])
  # Bucket by planned suffix (last _segment of planned name), else whole planned
  $bySuf = @{}
  foreach ($bn in $group) {
    $plan = if ($planned.ContainsKey($bn)) { $planned[$bn] } elseif (-not (Test-IsNumericBasename $bn)) { $bn } else { $bn }
    $sufKey = 'unk'
    if ($plan -match '_(Base|Norm|RM|AO|SPEC|SI|Color)(_\d+)?$') {
      $sufKey = $Matches[1]
    }
    elseif ($plan -match '_([^_]+)$') {
      $sufKey = $Matches[1]
    }
    if (-not $bySuf.ContainsKey($sufKey)) {
      $bySuf[$sufKey] = New-Object System.Collections.ArrayList
    }
    [void]$bySuf[$sufKey].Add($bn)
  }
  foreach ($sufKey in $bySuf.Keys) {
    $sub = @($bySuf[$sufKey])
    $candidatePlans = @()
    foreach ($bn in $sub) {
      if ($planned.ContainsKey($bn)) { $candidatePlans += $planned[$bn] }
      elseif (-not (Test-IsNumericBasename $bn)) { $candidatePlans += $bn }
    }
    $human = @($candidatePlans | Where-Object { $_ -and -not (Test-IsNumericBasename $_) } | Sort-Object @{ Expression = { Get-OwnerScore $_ } }, @{ Expression = { $_.Length } }, @{ Expression = { $_ } })
    if ($human.Count -gt 0) {
      $canon = $human[0]
    }
    else {
      $canon = if ($planned.ContainsKey($sub[0])) { $planned[$sub[0]] } else { $sub[0] }
    }
    foreach ($bn in $sub) { $finalOf[$bn] = $canon }
  }
}

# Basenames only in planned (all refs)
foreach ($bn in $planned.Keys) {
  if (-not $finalOf.ContainsKey($bn)) {
    $finalOf[$bn] = $planned[$bn]
  }
}

# Disambiguate collisions: multiple hashes wanting same final name
$desiredToHash = @{}  # finalName -> set of hashes that want it
foreach ($bn in $finalOf.Keys) {
  $fn = $finalOf[$bn]
  $h = if ($hashOf.ContainsKey($bn)) { $hashOf[$bn] } else { "NOHASH:$bn" }
  if (-not $desiredToHash.ContainsKey($fn)) {
    $desiredToHash[$fn] = New-Object System.Collections.Generic.HashSet[string]
  }
  [void]$desiredToHash[$fn].Add($h)
}

$nameRemap = @{}  # oldFinal -> disambiguated final (for colliding finals)
foreach ($fn in @($desiredToHash.Keys)) {
  $hashes = @($desiredToHash[$fn])
  if ($hashes.Count -le 1) { continue }
  $sortedH = $hashes | Sort-Object
  for ($idx = 0; $idx -lt $sortedH.Count; $idx++) {
    $h = $sortedH[$idx]
    $newName = if ($idx -eq 0) { $fn } else { ($fn + '_' + ($idx + 1)) }
    # find any basename with this hash currently mapped to $fn
    foreach ($bn in @($finalOf.Keys)) {
      if ($finalOf[$bn] -ne $fn) { continue }
      $bh = if ($hashOf.ContainsKey($bn)) { $hashOf[$bn] } else { "NOHASH:$bn" }
      if ($bh -eq $h) {
        $finalOf[$bn] = $newName
      }
    }
  }
}

# Ensure no two different hashes share a final name; ensure target files don't clash wrongly
# Also: if final name equals an existing unused file name that isn't being deleted as same content - handle via unused delete first

$renameMap = @()  # old -> new where different
foreach ($bn in ($finalOf.Keys | Sort-Object)) {
  $fn = $finalOf[$bn]
  if ($bn -ne $fn) {
    $renameMap += [pscustomobject]@{ Old = $bn; New = $fn; Hash = $(if ($hashOf.ContainsKey($bn)) { $hashOf[$bn] } else { '' }) }
  }
}

# Survivors: unique finals that need a file on disk
$survivorSource = @{}  # finalName -> preferred source basename (prefer already==final, else first)
foreach ($bn in $finalOf.Keys) {
  $fn = $finalOf[$bn]
  if (-not $survivorSource.ContainsKey($fn)) {
    $survivorSource[$fn] = $bn
  }
  else {
    $cur = $survivorSource[$fn]
    # prefer source that already has the final name on disk, else human, else shorter
    if ($bn -eq $fn -and $cur -ne $fn) { $survivorSource[$fn] = $bn }
    elseif ((-not (Test-IsNumericBasename $bn)) -and (Test-IsNumericBasename $cur)) { $survivorSource[$fn] = $bn }
  }
}

$dupGroups = @($byHash.GetEnumerator() | Where-Object { $_.Value.Count -gt 1 })
Write-Host ("Rename ops={0} Content-dup groups={1}" -f $renameMap.Count, $dupGroups.Count)

# Reports
$mapPath = Join-Path $ReportDir 'texture-rename-map.csv'
$unusedPath = Join-Path $ReportDir 'texture-unused-candidates.txt'
$dupPath = Join-Path $ReportDir 'texture-content-dupes.csv'
$summaryPath = Join-Path $ReportDir 'texture-audit-summary.txt'

$renameMap | Sort-Object Old | Export-Csv -LiteralPath $mapPath -NoTypeInformation -Encoding UTF8

$unusedTex | Set-Content -LiteralPath $unusedPath -Encoding UTF8
@(
  "fb_only:"
  $fbOnly
) | Set-Content -LiteralPath (Join-Path $ReportDir 'texture-fallbacks-only.txt') -Encoding UTF8

$dupRows = foreach ($g in $dupGroups) {
  [pscustomobject]@{
    Hash      = $g.Key
    Count     = $g.Value.Count
    Basenames = ($g.Value -join ';')
    Final     = $finalOf[$g.Value[0]]
  }
}
$dupRows | Export-Csv -LiteralPath $dupPath -NoTypeInformation -Encoding UTF8

@(
  "AssetsRoot=$AssetsRoot"
  "Mode=$(if ($Apply) { 'Apply' } else { 'DryRun' })"
  "EntityFilter=$EntityFilter"
  "Referenced=$($referenced.Count)"
  "Textures=$($texSet.Count)"
  "Fallbacks=$($fbSet.Count)"
  "UnusedTex=$($unusedTex.Count)"
  "FallbacksOnly=$($fbOnly.Count)"
  "MissingAfterRetarget=$($missing.Count)"
  "RenameRows=$($renameMap.Count)"
  "ContentDupGroups=$($dupGroups.Count)"
  "UniqueFinals=$($survivorSource.Count)"
) | Set-Content -LiteralPath $summaryPath -Encoding UTF8

Write-Host "Wrote reports to $ReportDir"
Get-Content -LiteralPath $summaryPath | ForEach-Object { Write-Host "  $_" }

if ($DryRun) {
  Write-Host "DryRun complete - no files changed."
  exit 0
}

# ---------- APPLY ----------
Write-Host "APPLY: retarget missing MP7 refs in .mtl..."
foreach ($kv in $missingRetarget.GetEnumerator()) {
  $oldDds = $kv.Key + '.dds'
  $newDds = $kv.Value + '.dds'
  Get-ChildItem -LiteralPath $mtlDir -Filter '*.mtl' -File | ForEach-Object {
    $raw = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
    if ($raw -and $raw.Contains($oldDds)) {
      $raw2 = $raw.Replace("Name=`"$oldDds`"", "Name=`"$newDds`"")
      if ($raw2 -ne $raw) {
        Set-Content -LiteralPath $_.FullName -Value $raw2 -Encoding UTF8 -NoNewline
      }
    }
  }
}

Write-Host "APPLY: delete unused textures + fallbacks..."
$deleted = New-Object System.Collections.Generic.List[string]
foreach ($bn in $unusedTex) {
  $p1 = Join-Path $texDir ($bn + '.dds')
  $p2 = Join-Path $fbDir ($bn + '.dds')
  if (Test-Path -LiteralPath $p1) {
    Remove-Item -LiteralPath $p1 -Force
    $deleted.Add("Textures/$bn.dds")
  }
  if (Test-Path -LiteralPath $p2) {
    Remove-Item -LiteralPath $p2 -Force
    $deleted.Add("Fallbacks/$bn.dds")
  }
}
foreach ($bn in $fbOnly) {
  # orphans only in Fallbacks and not referenced
  if ($referenced.Contains($bn)) { continue }
  $p2 = Join-Path $fbDir ($bn + '.dds')
  if (Test-Path -LiteralPath $p2) {
    Remove-Item -LiteralPath $p2 -Force
    $deleted.Add("Fallbacks/$bn.dds")
  }
}
$deletedPath = Join-Path $ReportDir 'texture-unused-deleted.txt'
$deleted | Set-Content -LiteralPath $deletedPath -Encoding UTF8
Write-Host "Deleted $($deleted.Count) files"

Write-Host "APPLY: materialize survivors / renames (two-phase via .__ren)..."
# Phase 1: move sources that need rename to temp
$tempMoves = @()
foreach ($fn in ($survivorSource.Keys | Sort-Object)) {
  $srcBn = $survivorSource[$fn]
  $srcTex = Join-Path $texDir ($srcBn + '.dds')
  $dstTex = Join-Path $texDir ($fn + '.dds')
  $srcFb = Join-Path $fbDir ($srcBn + '.dds')
  $dstFb = Join-Path $fbDir ($fn + '.dds')

  if ($srcBn -eq $fn) {
    # already correct name
    continue
  }
  if (-not (Test-Path -LiteralPath $srcTex)) {
    Write-Warning "Survivor source missing: $srcBn for final $fn"
    continue
  }
  $tmpTex = Join-Path $texDir ($fn + '.__ren.dds')
  $tmpFb = Join-Path $fbDir ($fn + '.__ren.dds')
  if (Test-Path -LiteralPath $tmpTex) { Remove-Item -LiteralPath $tmpTex -Force }
  Move-Item -LiteralPath $srcTex -Destination $tmpTex -Force
  if (Test-Path -LiteralPath $srcFb) {
    if (Test-Path -LiteralPath $tmpFb) { Remove-Item -LiteralPath $tmpFb -Force }
    Move-Item -LiteralPath $srcFb -Destination $tmpFb -Force
  }
  $tempMoves += [pscustomobject]@{ Final = $fn; TmpTex = $tmpTex; TmpFb = $tmpFb; DstTex = $dstTex; DstFb = $dstFb }
}

# Delete non-survivor sources that mapped into another final (dedupe leftovers)
foreach ($bn in $finalOf.Keys) {
  $fn = $finalOf[$bn]
  $surv = $survivorSource[$fn]
  if ($bn -eq $surv) { continue }
  if ($bn -eq $fn) { continue } # shouldn't
  $p1 = Join-Path $texDir ($bn + '.dds')
  $p2 = Join-Path $fbDir ($bn + '.dds')
  # skip if already moved to temp as something else
  if (Test-Path -LiteralPath $p1) {
    Remove-Item -LiteralPath $p1 -Force
    $deleted.Add("dedupe:Textures/$bn.dds -> $fn")
  }
  if (Test-Path -LiteralPath $p2) {
    Remove-Item -LiteralPath $p2 -Force
    $deleted.Add("dedupe:Fallbacks/$bn.dds -> $fn")
  }
}

# Phase 2: temp -> final (overwrite if leftover)
foreach ($tm in $tempMoves) {
  if (Test-Path -LiteralPath $tm.DstTex) { Remove-Item -LiteralPath $tm.DstTex -Force }
  Move-Item -LiteralPath $tm.TmpTex -Destination $tm.DstTex -Force
  if (Test-Path -LiteralPath $tm.TmpFb) {
    if (Test-Path -LiteralPath $tm.DstFb) { Remove-Item -LiteralPath $tm.DstFb -Force }
    New-Item -ItemType Directory -Force -Path $fbDir | Out-Null
    Move-Item -LiteralPath $tm.TmpFb -Destination $tm.DstFb -Force
  }
}

Write-Host "APPLY: rewrite .mtl Name= attributes..."
# Build old.dds -> new.dds replacement map (longest keys first)
$repl = @{}
foreach ($bn in $finalOf.Keys) {
  $fn = $finalOf[$bn]
  if ($bn -ne $fn) {
    $repl[$bn + '.dds'] = $fn + '.dds'
  }
}
foreach ($kv in $missingRetarget.GetEnumerator()) {
  # already applied earlier, but ensure chain: if retarget target also renamed
  $from = $kv.Key + '.dds'
  $mid = $kv.Value
  $toBn = if ($finalOf.ContainsKey($mid)) { $finalOf[$mid] } else { $mid }
  $repl[$from] = $toBn + '.dds'
}

$replKeys = $repl.Keys | Sort-Object { $_.Length } -Descending
$mtlChanged = 0
Get-ChildItem -LiteralPath $mtlDir -Filter '*.mtl' -File | ForEach-Object {
  $raw = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
  if (-not $raw) { return }
  $orig = $raw
  foreach ($k in $replKeys) {
    $raw = $raw.Replace("Name=`"$k`"", "Name=`"$($repl[$k])`"")
  }
  if ($raw -ne $orig) {
    Set-Content -LiteralPath $_.FullName -Value $raw -Encoding UTF8 -NoNewline
    $mtlChanged++
  }
}
Write-Host "Materials updated: $mtlChanged"

Write-Host "APPLY: rewrite items.lua texture string IDs..."
if (Test-Path -LiteralPath $itemsPath) {
  $items = Get-Content -LiteralPath $itemsPath -Raw -Encoding UTF8
  $origItems = $items
  # Replace quoted basenames; longest first
  $idKeys = @($finalOf.Keys | Where-Object { $_ -ne $finalOf[$_] } | Sort-Object { $_.Length } -Descending)
  foreach ($oldId in $idKeys) {
    $newId = $finalOf[$oldId]
    $items = $items.Replace('"' + $oldId + '"', '"' + $newId + '"')
  }
  foreach ($kv in $missingRetarget.GetEnumerator()) {
    $mid = $kv.Value
    $toBn = if ($finalOf.ContainsKey($mid)) { $finalOf[$mid] } else { $mid }
    $items = $items.Replace('"' + $kv.Key + '"', '"' + $toBn + '"')
  }
  if ($items -ne $origItems) {
    Set-Content -LiteralPath $itemsPath -Value $items -Encoding UTF8 -NoNewline
    Write-Host "items.lua updated"
  }
  else {
    Write-Host "items.lua unchanged"
  }
}

$deleted | Set-Content -LiteralPath $deletedPath -Encoding UTF8

Write-Host ""
Write-Host "APPLY complete."
Write-Host "NEXT: open jazz_assets in Mod Editor and Save/re-export materials so BinAssets/*.mtlbin pick up new paths."
Write-Host "Then runtime-smoke AA52 / M2Carbine / MP7 / BerettaM12."
Write-Host "Reports: $ReportDir"
