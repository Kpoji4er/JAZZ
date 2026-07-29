# Merc generation progress helper
# Updated by agent during JAZZ-UNITS-002 wave. Queue: _generation-queue.md

$ErrorActionPreference = 'Stop'
$jazz = Split-Path (Split-Path (Split-Path $PSScriptRoot))
if (-not (Test-Path (Join-Path $jazz 'docs\design\mercs-ja12'))) {
  $jazz = 'C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz'
}
$units = Join-Path (Split-Path $jazz) 'jazz-units'
$base = Join-Path $jazz 'docs\design\mercs-ja12'
$merc = Join-Path $units 'MercPortraits'
$queue = @(
  'colby','blade','ira','dimitri','madman','conrad','mike','grom',
  'rothman','quinten','vicious','biff','nervous','flo','cougar','miguel','gamos','dynamo','gaston','horg','manuel','monk','allik','henning',
  'static','highball','bull','cord','hobbit','ricochet','meat','carlos','devin','shank','vince','hitman','biggens','kulba','vilde','grace','steiger','lucky','laura','eskimo'
)

Write-Host "slug`texec`tunitdata`tperk`tportrait`tbig"
foreach ($slug in $queue) {
  $art = Join-Path $base "$slug.md"
  $exec = if (Test-Path $art) { [bool](Select-String -Path $art -Pattern '^executable: true' -Quiet) } else { $false }
  $unitId = if (Test-Path $art) { if ((Get-Content $art -Raw) -match '(?m)^unit_id:\s*(\S+)') { $Matches[1] } else { "Jazz_$slug" } } else { "Jazz_$slug" }
  $portraitId = if (Test-Path $art) { if ((Get-Content $art -Raw) -match '(?m)^portrait_id:\s*(\S+)') { $Matches[1] } else { (Get-Culture).TextInfo.ToTitleCase($slug) } } else { $slug }
  $ud = Test-Path (Join-Path $units "UnitData\$unitId.lua")
  $perk = Test-Path (Join-Path $jazz "CharacterEffect\Jazz_Perk_$portraitId.lua")
  if (-not $perk) { $perk = Test-Path (Join-Path $jazz "CharacterEffect\Jazz_Perk_$((Get-Culture).TextInfo.ToTitleCase($slug)).lua") }
  $p = Test-Path (Join-Path $merc "$portraitId.png")
  $b = Test-Path (Join-Path $merc "${portraitId}_Big.png")
  Write-Host "$slug`t$exec`t$ud`t$perk`t$p`t$b"
}
