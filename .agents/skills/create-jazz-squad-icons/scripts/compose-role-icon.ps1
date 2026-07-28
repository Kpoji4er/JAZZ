# Composes a role symbol onto faction shield PNGs.
# Usage:
#   compose-role-icon.ps1 -Role TAX -SourceDraft "C:\path\draft.png" -Factions legion,army,adonis,rebels,smugglers
#   compose-role-icon.ps1 -Role TAX -SourceLegion -Factions army,adonis,rebels,smugglers
#
# Requires: System.Drawing (Windows PowerShell / Windows).

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$Role,

  [string]$SourceDraft = "",

  [switch]$SourceLegion,

  [string]$Factions = "legion,army,adonis,rebels,smugglers",

  [string]$EnemyDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

function Get-ChannelMax([byte]$a, [byte]$b, [byte]$c) {
  $m = $a; if ($b -gt $m) { $m = $b }; if ($c -gt $m) { $m = $c }; return $m
}
function Get-ChannelMin([byte]$a, [byte]$b, [byte]$c) {
  $m = $a; if ($b -lt $m) { $m = $b }; if ($c -lt $m) { $m = $c }; return $m
}

function Test-IsIvory([System.Drawing.Color]$c) {
  if ($c.A -lt 200) { return $false }
  if ($c.R -lt 165 -or $c.G -lt 145 -or $c.B -lt 105) { return $false }
  $max = Get-ChannelMax $c.R $c.G $c.B
  $min = Get-ChannelMin $c.R $c.G $c.B
  if (($max - $min) -gt 100) { return $false }
  if ((([int]$c.R - [int]$c.G) -gt 50) -and (([int]$c.R - [int]$c.B) -gt 50)) { return $false }
  return $true
}

function Test-IsOnShield([System.Drawing.Color]$c) {
  return ($c.A -ge 200)
}

function Find-IvoryColor([System.Drawing.Bitmap]$bmp) {
  $bestScore = -1
  $best = [System.Drawing.Color]::FromArgb(255, 230, 222, 202)
  for ($y = 8; $y -le 48; $y++) {
    for ($x = 16; $x -le 48; $x++) {
      $c = $bmp.GetPixel($x, $y)
      if (-not (Test-IsIvory $c)) { continue }
      $max = Get-ChannelMax $c.R $c.G $c.B
      $min = Get-ChannelMin $c.R $c.G $c.B
      $score = ([int]$c.R + [int]$c.G + [int]$c.B) - 2 * ($max - $min)
      if ($score -gt $bestScore) { $bestScore = $score; $best = $c }
    }
  }
  return [System.Drawing.Color]::FromArgb(255, $best.R, $best.G, $best.B)
}

function Find-OutlineColor([System.Drawing.Bitmap]$bmp) {
  for ($y = 10; $y -le 50; $y++) {
    for ($x = 18; $x -le 46; $x++) {
      $c = $bmp.GetPixel($x, $y)
      if ($c.A -lt 200) { continue }
      if ($c.R -gt 90 -or $c.G -gt 70 -or $c.B -gt 70) { continue }
      if ($c.R -lt 12 -and $c.G -lt 12 -and $c.B -lt 12) { continue }
      return [System.Drawing.Color]::FromArgb(255, $c.R, $c.G, $c.B)
    }
  }
  return [System.Drawing.Color]::FromArgb(255, 48, 28, 28)
}

function Ensure-64([System.Drawing.Bitmap]$bmp) {
  if ($bmp.Width -eq 64 -and $bmp.Height -eq 64) { return $bmp }
  $resized = New-Object System.Drawing.Bitmap 64, 64, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g = [System.Drawing.Graphics]::FromImage($resized)
  $g.Clear([System.Drawing.Color]::FromArgb(0, 0, 0, 0))
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $g.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
  $g.DrawImage($bmp, 0, 0, 64, 64)
  $g.Dispose()
  $bmp.Dispose()
  return $resized
}

function Get-IvoryMask([System.Drawing.Bitmap]$src) {
  $mask = New-Object bool[] 4096
  $count = 0
  for ($y = 0; $y -lt 64; $y++) {
    for ($x = 0; $x -lt 64; $x++) {
      $is = Test-IsIvory ($src.GetPixel($x, $y))
      $mask[($y * 64 + $x)] = $is
      if ($is) { $count++ }
    }
  }
  return @{ Mask = $mask; Count = $count }
}

function Save-Png([System.Drawing.Bitmap]$bmp, [string]$path) {
  $tmp = "$path.tmp.png"
  $bmp.Save($tmp, [System.Drawing.Imaging.ImageFormat]::Png)
  Move-Item -Force $tmp $path
}

function Compose-OntoShield {
  param(
    [bool[]]$Mask,
    [string]$ShieldPath,
    [string]$OutPath,
    [System.Drawing.Color]$IvoryColor,
    [System.Drawing.Color]$OutlineColor
  )

  $shield = Ensure-64 ([System.Drawing.Bitmap]::FromFile($ShieldPath))
  $out = New-Object System.Drawing.Bitmap 64, 64, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $clear = [System.Drawing.Color]::FromArgb(0, 0, 0, 0)

  for ($y = 0; $y -lt 64; $y++) {
    for ($x = 0; $x -lt 64; $x++) {
      $base = $shield.GetPixel($x, $y)
      if ($base.A -lt 200) { $out.SetPixel($x, $y, $clear) }
      else { $out.SetPixel($x, $y, [System.Drawing.Color]::FromArgb(255, $base.R, $base.G, $base.B)) }
    }
  }

  $dirs = @(@(-1,0),@(1,0),@(0,-1),@(0,1),@(-1,-1),@(-1,1),@(1,-1),@(1,1))
  for ($y = 1; $y -lt 63; $y++) {
    for ($x = 1; $x -lt 63; $x++) {
      if ($Mask[($y * 64 + $x)]) { continue }
      $near = $false
      foreach ($d in $dirs) {
        if ($Mask[(($y + $d[1]) * 64 + ($x + $d[0]))]) { $near = $true; break }
      }
      if (-not $near) { continue }
      if (Test-IsOnShield ($shield.GetPixel($x, $y))) {
        $out.SetPixel($x, $y, $OutlineColor)
      }
    }
  }

  $painted = 0
  for ($y = 0; $y -lt 64; $y++) {
    for ($x = 0; $x -lt 64; $x++) {
      if (-not $Mask[($y * 64 + $x)]) { continue }
      if (-not (Test-IsOnShield ($shield.GetPixel($x, $y)))) { continue }
      $out.SetPixel($x, $y, $IvoryColor)
      $painted++
    }
  }

  Save-Png $out $OutPath
  Write-Output ("  {0}: painted={1}" -f (Split-Path $OutPath -Leaf), $painted)
  $out.Dispose()
  $shield.Dispose()
}

if (-not $EnemyDir) {
  $repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")
  $EnemyDir = Join-Path $repoRoot "SquadsIcons\Enemy"
}
if (-not (Test-Path $EnemyDir)) {
  throw "EnemyDir not found: $EnemyDir"
}

$Role = $Role.ToUpperInvariant()
$factionList = @($Factions.Split(",") | ForEach-Object { $_.Trim().ToLowerInvariant() } | Where-Object { $_ })
$shieldMap = @{
  legion = "legion.png"
  army = "army.png"
  adonis = "adonis.png"
  rebels = "rebels.png"
  smugglers = "smugglers.png"
}

$paletteSrcPath = Join-Path $EnemyDir "legion_GARRISON_squad.png"
if (-not (Test-Path $paletteSrcPath)) {
  $paletteSrcPath = Join-Path $EnemyDir "legion.png"
}
$paletteBmp = [System.Drawing.Bitmap]::FromFile($paletteSrcPath)
$ivory = Find-IvoryColor $paletteBmp
$outline = Find-OutlineColor $paletteBmp
$paletteBmp.Dispose()
Write-Output ("Palette ivory=({0},{1},{2}) outline=({3},{4},{5})" -f $ivory.R,$ivory.G,$ivory.B,$outline.R,$outline.G,$outline.B)

$sourcePath = $null
if ($SourceLegion) {
  $sourcePath = Join-Path $EnemyDir ("legion_{0}_squad.png" -f $Role)
} elseif ($SourceDraft) {
  $sourcePath = $SourceDraft
} else {
  throw "Provide -SourceDraft <png> or -SourceLegion"
}
if (-not (Test-Path $sourcePath)) {
  throw "Source not found: $sourcePath"
}

$src = Ensure-64 ([System.Drawing.Bitmap]::FromFile($sourcePath))
$maskInfo = Get-IvoryMask $src
$src.Dispose()
if ($maskInfo.Count -lt 40) {
  throw "Ivory mask too small ($($maskInfo.Count) px). Check draft colors/alpha."
}
if ($maskInfo.Count -gt 1200) {
  Write-Warning "Ivory mask unusually large ($($maskInfo.Count) px) — possible background bleed."
}

foreach ($fid in $factionList) {
  if (-not $shieldMap.ContainsKey($fid)) {
    throw "Unknown faction: $fid"
  }
  $shieldPath = Join-Path $EnemyDir $shieldMap[$fid]
  if (-not (Test-Path $shieldPath)) {
    throw "Missing shield: $shieldPath"
  }
  $outPath = Join-Path $EnemyDir ("{0}_{1}_squad.png" -f $fid, $Role)
  Compose-OntoShield -Mask $maskInfo.Mask -ShieldPath $shieldPath -OutPath $outPath -IvoryColor $ivory -OutlineColor $outline
}

# Verify transparent corner on first faction
$first = $factionList[0]
$verifyPath = Join-Path $EnemyDir ("{0}_{1}_squad.png" -f $first, $Role)
$v = [System.Drawing.Bitmap]::FromFile($verifyPath)
$c0 = $v.GetPixel(0, 0)
Write-Output ("VERIFY {0} 0,0 A={1} (expect 0)" -f (Split-Path $verifyPath -Leaf), $c0.A)
$v.Dispose()
Write-Output "Done"
