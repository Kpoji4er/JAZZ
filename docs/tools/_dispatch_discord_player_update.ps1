#Requires -Version 5.1
<#
.SYNOPSIS
  Dispatch GitHub Actions "Discord player updates" for a package after push.

.DESCRIPTION
  Cursor / agent git pushes often create only a Cursor check suite and do NOT
  start GitHub Actions, so Discord stays silent. After an approved push to main,
  run this to ensure the Discord workflow actually starts.

  Default mode polls for up to WaitSeconds. If ANY Discord run already exists
  for AfterSha (push or workflow_dispatch, queued/in_progress/success), it exits
  without dispatching. That prevents double posts when push Actions starts late.

  Suite rule (one logical feature across jazz / jazz-units / jazz-maps / nomaps):
  call this script ONCE for the primary player-facing package. Sibling packages
  should use commit marker [skip discord]. Do NOT -Force -AlwaysDispatch on every
  repo of the same change set — that creates 3 near-duplicate Discord posts.

.EXAMPLE
  powershell -File docs/tools/_dispatch_discord_player_update.ps1
  powershell -File docs/tools/_dispatch_discord_player_update.ps1 -Repo jazz-units
  powershell -File docs/tools/_dispatch_discord_player_update.ps1 -Repo jazz -Before 971d5d4 -After 652675d -Force -AlwaysDispatch
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

  # Comma-separated suite packages for Discord "Пакеты" field, e.g. jazz,jazz-units,jazz-nomaps
  [string] $SuitePackages = "",

  [int] $WaitSeconds = 90,
  [int] $PollSeconds = 8
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

function Find-DiscordRunForSha([string]$repoSlug, [string]$sha) {
  $existingJson = gh api "repos/$repoSlug/actions/workflows/discord-player-updates.yml/runs?branch=main&per_page=20"
  $existing = $existingJson | ConvertFrom-Json
  $shaLower = $sha.ToLowerInvariant()
  return @($existing.workflow_runs) | Where-Object {
    $_.head_sha -and ($_.head_sha.ToLowerInvariant() -eq $shaLower) -and (
      $_.status -in @("queued", "in_progress", "waiting", "pending", "requested") -or
      ($_.status -eq "completed" -and $_.conclusion -in @("success", "neutral"))
    )
  } | Select-Object -First 1
}

$afterSha = if ($After) { Get-Sha $After } else { Get-Sha "HEAD" }
$beforeSha = if ($Before) { Get-Sha $Before } else { Get-Sha "$afterSha^" }

Write-Host "Discord dispatch target: $slug"
Write-Host "Checkout: $RepoPath"
Write-Host "Range: $beforeSha..$afterSha  force=$Force dry_run=$DryRun always=$AlwaysDispatch"
if ($SuitePackages) {
  Write-Host "Suite packages: $SuitePackages"
}
if ($Force -or $AlwaysDispatch) {
  Write-Host "NOTE: suite = one Discord post per logical feature. Do not Force/AlwaysDispatch sibling repos for the same change."
}

if (-not $AlwaysDispatch -and -not $DryRun) {
  $deadline = [DateTime]::UtcNow.AddSeconds([Math]::Max(0, $WaitSeconds))
  $poll = [Math]::Max(3, $PollSeconds)
  Write-Host "Polling up to ${WaitSeconds}s for an existing Discord run for $afterSha..."
  do {
    $hit = Find-DiscordRunForSha -repoSlug $slug -sha $afterSha
    if ($hit) {
      Write-Host "Discord run already covers this SHA: $($hit.html_url) ($($hit.event) $($hit.status)/$($hit.conclusion))"
      Write-Host "Skipping workflow_dispatch to avoid a duplicate Discord post."
      return
    }
    if ([DateTime]::UtcNow -ge $deadline) { break }
    Start-Sleep -Seconds $poll
  } while ([DateTime]::UtcNow -lt $deadline)

  Write-Host "No Discord run for $afterSha after wait; dispatching workflow_dispatch."
}

$forceValue = if ($Force) { "true" } else { "false" }
$dryValue = if ($DryRun) { "true" } else { "false" }
$suiteValue = if ($SuitePackages) { $SuitePackages.Trim() } else { $Repo }

gh workflow run discord-player-updates.yml `
  --repo $slug `
  --ref main `
  -f "dry_run=$dryValue" `
  -f "force_publish=$forceValue" `
  -f "before_sha=$beforeSha" `
  -f "after_sha=$afterSha" `
  -f "suite_packages=$suiteValue"

Start-Sleep -Seconds 3
$runs = gh run list --repo $slug --workflow=discord-player-updates.yml --limit 1 --json databaseId,url,status,event,displayTitle |
  ConvertFrom-Json
if ($runs) {
  Write-Host "Started: $($runs[0].url) ($($runs[0].status), $($runs[0].event))"
}
