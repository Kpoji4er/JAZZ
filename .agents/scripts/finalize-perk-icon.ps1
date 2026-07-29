# Finalize a personal perk icon draft into Perks/Personal/<Name>.png (68x68).
# Usage:
#   .agents/scripts/finalize-perk-icon.ps1 -SourceDraft "path\to\draft.png" -Name Blade
#
# Keys near-black draft background to alpha and resizes to 68x68 RGBA PNG.

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$SourceDraft,

  [Parameter(Mandatory = $true)]
  [string]$Name,

  [string]$OutDir = "",

  [int]$BlackKeyMax = 28
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

function Resolve-RepoRoot {
  $here = $PSScriptRoot
  return (Resolve-Path (Join-Path $here "..\..")).Path
}

if (-not (Test-Path -LiteralPath $SourceDraft)) {
  throw "SourceDraft not found: $SourceDraft"
}

$repo = Resolve-RepoRoot
if (-not $OutDir) {
  $OutDir = Join-Path $repo "Perks\Personal"
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$safe = $Name.Trim()
if ($safe -notmatch '^[A-Za-z0-9_]+$') {
  throw "Name must be alphanumeric/underscore: $Name"
}
$outPath = Join-Path $OutDir "$safe.png"
$tempPath = Join-Path $OutDir "$safe.$([Guid]::NewGuid().ToString('N')).tmp.png"
$size = 68

$src = [System.Drawing.Bitmap]::FromFile((Resolve-Path -LiteralPath $SourceDraft).Path)
try {
  $keyed = New-Object System.Drawing.Bitmap $src.Width, $src.Height, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  try {
    for ($y = 0; $y -lt $src.Height; $y++) {
      for ($x = 0; $x -lt $src.Width; $x++) {
        $c = $src.GetPixel($x, $y)
        $max = [Math]::Max($c.R, [Math]::Max($c.G, $c.B))
        $min = [Math]::Min($c.R, [Math]::Min($c.G, $c.B))
        $isNearBlack = ($max -le $BlackKeyMax) -and (($max - $min) -le 12)
        if ($c.A -lt 8 -or $isNearBlack) {
          $keyed.SetPixel($x, $y, [System.Drawing.Color]::FromArgb(0, 0, 0, 0))
        }
        else {
          $keyed.SetPixel($x, $y, $c)
        }
      }
    }

    $work = New-Object System.Drawing.Bitmap $size, $size, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
      $g = [System.Drawing.Graphics]::FromImage($work)
      try {
        $g.Clear([System.Drawing.Color]::FromArgb(0, 0, 0, 0))
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $g.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
        $g.DrawImage($keyed, 0, 0, $size, $size)
      }
      finally {
        $g.Dispose()
      }
      $work.Save($tempPath, [System.Drawing.Imaging.ImageFormat]::Png)
    }
    finally {
      $work.Dispose()
    }
  }
  finally {
    $keyed.Dispose()
  }
}
finally {
  $src.Dispose()
}

try {
  if (Test-Path -LiteralPath $outPath) {
    Remove-Item -LiteralPath $outPath -Force
  }
  Move-Item -LiteralPath $tempPath -Destination $outPath
}
finally {
  if (Test-Path -LiteralPath $tempPath) {
    Remove-Item -LiteralPath $tempPath -Force
  }
}

Write-Output $outPath
