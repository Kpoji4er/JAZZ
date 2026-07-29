# Finalize attachment icon draft into Icons/Upgrades/<IconId>.png
# Usage:
#   finalize-attachment-icon.ps1 -SourceDraft "C:\path\draft.png" -IconId slot_scope
#
# Keys near-black draft background to alpha, resizes to 64x64 RGBA.

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$SourceDraft,

  [Parameter(Mandatory = $true)]
  [string]$IconId,

  [string]$OutDir = "",

  [string]$Recolor = "",

  [int]$BlackKeyMax = 28,

  [int]$Size = 64
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

function Resolve-RepoRoot {
  $here = $PSScriptRoot
  return (Resolve-Path (Join-Path $here "..\..\..\..")).Path
}

function Parse-HexColor([string]$hex) {
  $h = $hex.Trim()
  if ($h.StartsWith("#")) { $h = $h.Substring(1) }
  if ($h.Length -ne 6) { throw "Recolor must be #RRGGBB, got: $hex" }
  $r = [Convert]::ToInt32($h.Substring(0, 2), 16)
  $g = [Convert]::ToInt32($h.Substring(2, 2), 16)
  $b = [Convert]::ToInt32($h.Substring(4, 2), 16)
  return [System.Drawing.Color]::FromArgb(255, $r, $g, $b)
}

if (-not (Test-Path -LiteralPath $SourceDraft)) {
  throw "SourceDraft not found: $SourceDraft"
}

$repo = Resolve-RepoRoot
if (-not $OutDir) {
  $OutDir = Join-Path $repo "Icons\Upgrades"
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$safeId = $IconId.Trim()
if ($safeId -notmatch '^[A-Za-z0-9_]+$') {
  throw "IconId must be alphanumeric/underscore: $IconId"
}
$outPath = Join-Path $OutDir "$safeId.png"

$src = [System.Drawing.Bitmap]::FromFile((Resolve-Path -LiteralPath $SourceDraft).Path)
try {
  $work = New-Object System.Drawing.Bitmap $src.Width, $src.Height, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $recolorColor = $null
  if ($Recolor) { $recolorColor = Parse-HexColor $Recolor }

  for ($y = 0; $y -lt $src.Height; $y++) {
    for ($x = 0; $x -lt $src.Width; $x++) {
      $c = $src.GetPixel($x, $y)
      if ($c.A -lt 8) {
        $work.SetPixel($x, $y, [System.Drawing.Color]::FromArgb(0, 0, 0, 0))
        continue
      }
      $max = [Math]::Max($c.R, [Math]::Max($c.G, $c.B))
      $min = [Math]::Min($c.R, [Math]::Min($c.G, $c.B))
      $isNearBlack = ($max -le $BlackKeyMax) -and (($max - $min) -le 12)
      if ($isNearBlack) {
        $work.SetPixel($x, $y, [System.Drawing.Color]::FromArgb(0, 0, 0, 0))
        continue
      }
      if ($recolorColor -ne $null) {
        $work.SetPixel($x, $y, [System.Drawing.Color]::FromArgb([int]$c.A, $recolorColor.R, $recolorColor.G, $recolorColor.B))
      } else {
        $work.SetPixel($x, $y, $c)
      }
    }
  }

  $out = New-Object System.Drawing.Bitmap $Size, $Size, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g = [System.Drawing.Graphics]::FromImage($out)
  try {
    $g.Clear([System.Drawing.Color]::FromArgb(0, 0, 0, 0))
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.DrawImage($work, 0, 0, $Size, $Size)
  } finally {
    $g.Dispose()
    $work.Dispose()
  }

  $corner = $out.GetPixel(0, 0)
  if ($corner.A -gt 0 -and $corner.R -le $BlackKeyMax -and $corner.G -le $BlackKeyMax -and $corner.B -le $BlackKeyMax) {
    $out.SetPixel(0, 0, [System.Drawing.Color]::FromArgb(0, 0, 0, 0))
  }

  $out.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
  $out.Dispose()
} finally {
  $src.Dispose()
}

Write-Host "Wrote $outPath ($Size x $Size)"
