# Finalize HUD/action icon draft → Perks/SignatureAbilities/<ActionId>.png (108×54)
# Usage:
#   finalize-action-icon.ps1 -SourceDraft "draft.png" -ActionId Bullseye
#   finalize-action-icon.ps1 -SourceDraft "draft.png" -ActionId bandage -OutDir "Icons\Med"
#
# Keys near-black draft background to alpha, resizes to 108x54 RGBA.
# Requires: System.Drawing (Windows PowerShell).

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$SourceDraft,

  [Parameter(Mandatory = $true)]
  [Alias("IconId")]
  [string]$ActionId,

  [string]$OutDir = "",

  [string]$Recolor = "",

  [int]$BlackKeyMax = 28,

  [int]$Width = 108,

  [int]$Height = 54
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

function Resolve-RepoRoot {
  # .../jazz/.agents/skills/create-jazz-action-icons/scripts
  return (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
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
  $OutDir = Join-Path $repo "Perks\SignatureAbilities"
} elseif (-not [System.IO.Path]::IsPathRooted($OutDir)) {
  $OutDir = Join-Path $repo $OutDir
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$safeId = $ActionId.Trim()
if ($safeId -notmatch '^[A-Za-z0-9_]+$') {
  throw "ActionId must be alphanumeric/underscore: $ActionId"
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

  $out = New-Object System.Drawing.Bitmap $Width, $Height, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g = [System.Drawing.Graphics]::FromImage($out)
  try {
    $g.Clear([System.Drawing.Color]::FromArgb(0, 0, 0, 0))
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    # Letterbox-fit into 108x54 keeping aspect, centered
    $srcAspect = [double]$work.Width / [double]$work.Height
    $dstAspect = [double]$Width / [double]$Height
    if ($srcAspect -gt $dstAspect) {
      $drawW = $Width
      $drawH = [int][Math]::Round($Width / $srcAspect)
    } else {
      $drawH = $Height
      $drawW = [int][Math]::Round($Height * $srcAspect)
    }
    $ox = [int](($Width - $drawW) / 2)
    $oy = [int](($Height - $drawH) / 2)
    $g.DrawImage($work, $ox, $oy, $drawW, $drawH)
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

Write-Host "Wrote $outPath (${Width}x${Height})"
