#Requires -Version 5.1
<#
.SYNOPSIS
  Dispatch GitHub Actions "Discord player updates" for a package after push.

.DESCRIPTION
  Cursor / agent git pushes often create only a Cursor check suite and do NOT
  start GitHub Actions, so Discord stays silent. After an approved push to main,
  run this to ensure the Discord workflow actually starts.

  Default mode waits briefly, then dispatches workflow_dispatch only if no
  push-triggered Discord run exists for AfterSha.

.EXAMPLE
  pwsh docs/tools/_dispatch_discord_player_update.ps1
  pwsh docs/tools/_dispatch_discord_player_update.ps1 -Repo jazz-units -Force
  pwsh docs/tools/_dispatch_discord_player_update.ps1 -Repo jazz -Before 971d5d4 -After 652675d -Force -AlwaysDispatch
#>
[CmdletBinding()]
param(
  [ValidateSet("jazz", "jazz-units", "jazz-maps", "jazz_assets", "jazz-nomaps")]
  [string] $Repo = "jazz",

  [string] $Before = "",
  [string] $After = "",
  [string] $RepoPath = "",

  [switch] $Force,
  [switch] $DryRun,
  [switch] $AlwaysDispatch,
  [int] $WaitSeconds = 20
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoMap = @{
  "jazz"        = "Kpoji4er/JAZZ"
  "jazz-units"  = "Kpoji4er/JAZZ-units"
  "jazz-maps"   = "Kpoji4er/JAZZ-maps"
  "jazz_assets" = "Kpoji4er/JAZZ-assets"
  "jazz-nomaps" = "Kpoji4er/JAZZ-nomaps"
}
$dirMap = @{
  "jazz"        = "jazz"
  "jazz-units"  = "jazz-units"
  "jazz-maps"   = "jazz-maps"
  "jazz_assets" = "jazz_assets"
  "jazz-nomaps" = "jazz-nomaps"
}

$slug = $repoMap[$Repo]
if (-not $slug) { throw "Unknown repo key: $Repo" }

if (-not $RepoPath) {
  # PSScriptRoot = jazz/docs/tools → ../../.. = Mods/
  $modsRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
  $RepoPath = Join-Path $modsRoot $dirMap[$Repo]
}
if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
  throw "RepoPath is not a git checkout: $RepoPath"
}

function Get-Sha([string]$rev) {
  return (git -C $RepoPath rev-parse $rev).Trim()
}

$afterSha = if ($After) { Get-Sha $After } else { Get-Sha "HEAD" }
$beforeSha = if ($Before) { Get-Sha $Before } else { Get-Sha "$afterSha^" }

Write-Host "Discord dispatch target: $slug"
Write-Host "Checkout: $RepoPath"
Write-Host "Range: $beforeSha..$afterSha  force=$Force dry_run=$DryRun"

if (-not $AlwaysDispatch -and -not $DryRun) {
  if ($WaitSeconds -gt 0) {
    Write-Host "Waiting ${WaitSeconds}s for a push-triggered Actions run..."
    Start-Sleep -Seconds $WaitSeconds
  }
  $existingJson = gh api "repos/$slug/actions/workflows/discord-player-updates.yml/runs?branch=main&per_page=15"
  $existing = $existingJson | ConvertFrom-Json
  $hit = @($existing.workflow_runs) | Where-Object {
    $_.head_sha -eq $afterSha -and $_.event -eq "push"
  } | Select-Object -First 1
  if ($hit) {
    Write-Host "Push-triggered Discord run already exists: $($hit.html_url) ($($hit.status)/$($hit.conclusion))"
    return
  }
  Write-Host "No push-triggered Discord run for $afterSha; dispatching workflow_dispatch."
}

$forceValue = if ($Force) { "true" } else { "false" }
$dryValue = if ($DryRun) { "true" } else { "false" }

gh workflow run discord-player-updates.yml `
  --repo $slug `
  --ref main `
  -f "dry_run=$dryValue" `
  -f "force_publish=$forceValue" `
  -f "before_sha=$beforeSha" `
  -f "after_sha=$afterSha"

Start-Sleep -Seconds 3
$runs = gh run list --repo $slug --workflow=discord-player-updates.yml --limit 1 --json databaseId,url,status,event,displayTitle |
  ConvertFrom-Json
if ($runs) {
  Write-Host "Started: $($runs[0].url) ($($runs[0].status), $($runs[0].event))"
}
