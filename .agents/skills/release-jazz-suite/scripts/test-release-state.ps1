[CmdletBinding()]
param(
    [string]$ExpectedTag,
    [string]$SuiteRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path,
    [switch]$AllowDirty,
    [switch]$SkipOriginCheck,
    [switch]$SkipRemoteRefCheck,
    [switch]$ReportOnly
)

$ErrorActionPreference = 'Stop'
$tagPattern = '^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$'

if ($ExpectedTag -and -not [regex]::IsMatch($ExpectedTag, $tagPattern)) {
    Write-Error "Invalid expected tag '$ExpectedTag'. Use vMAJOR.MINOR.REVISION." -ErrorAction Continue
    exit 2
}

$suite = (Resolve-Path $SuiteRoot).Path
$parent = Split-Path $suite -Parent
$specs = @(
    [pscustomobject]@{ Name = 'JAZZ'; Candidates = @($suite); GitHub = 'Kpoji4er/JAZZ'; ModId = 'e6L4ECj' },
    [pscustomobject]@{ Name = 'JAZZ-assets'; Candidates = @((Join-Path $parent 'jazz_assets'), (Join-Path $parent 'jazz-assets')); GitHub = 'Kpoji4er/JAZZ-assets'; ModId = 'pDGDhr' },
    [pscustomobject]@{ Name = 'JAZZ-maps'; Candidates = @((Join-Path $parent 'jazz-maps')); GitHub = 'Kpoji4er/JAZZ-maps'; ModId = 'FhNNYd' },
    [pscustomobject]@{ Name = 'JAZZ-units'; Candidates = @((Join-Path $parent 'jazz-units')); GitHub = 'Kpoji4er/JAZZ-units'; ModId = 'Dv3mFVN' }
)

$findings = [System.Collections.Generic.List[object]]::new()
$states = [System.Collections.Generic.List[object]]::new()
$suiteDisplay = $null
$suiteTag = $null

function Add-Finding {
    param([string]$Level, [string]$Repository, [string]$Check, [string]$Detail)
    $script:findings.Add([pscustomobject]@{
        Level = $Level
        Repository = $Repository
        Check = $Check
        Detail = $Detail
    }) | Out-Null
}

function Invoke-GitRead {
    param(
        [string]$RepositoryPath,
        [string[]]$GitArguments,
        [switch]$AllowFailure
    )

    $lines = @(& git -C $RepositoryPath @GitArguments 2>&1)
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0 -and -not $AllowFailure) {
        throw "git $($GitArguments -join ' ') failed with exit code $exitCode."
    }

    return [pscustomobject]@{
        ExitCode = $exitCode
        Lines = @($lines | ForEach-Object { [string]$_ })
    }
}

function ConvertTo-GitHubSlug {
    param([string]$RemoteUrl)
    if (-not $RemoteUrl) { return $null }
    $match = [regex]::Match($RemoteUrl.Trim(), 'github\.com[:/](?<slug>[^/]+/[^/]+?)(?:\.git)?/?$', 'IgnoreCase')
    if (-not $match.Success) { return $null }
    return ($match.Groups['slug'].Value -replace '\.git$', '')
}

function Read-MetadataNumber {
    param([string]$Content, [string]$Field, [int]$DefaultValue = 0)
    $fieldPattern = "(?m)^\t'${Field}',\s*(\d+)"
    $match = [regex]::Match($Content, $fieldPattern)
    if (-not $match.Success) { return $DefaultValue }
    return [int]$match.Groups[1].Value
}

function Read-MetadataString {
    param([string]$Content, [string]$Field)
    $fieldPattern = "(?m)^\t'${Field}',\s*`"([^`"]*)`""
    $match = [regex]::Match($Content, $fieldPattern)
    if (-not $match.Success) { return '' }
    return $match.Groups[1].Value
}

foreach ($spec in $specs) {
    $repositoryPath = $spec.Candidates |
        Where-Object { Test-Path -LiteralPath $_ -PathType Container } |
        Select-Object -First 1

    if (-not $repositoryPath) {
        Add-Finding 'FAIL' $spec.Name 'repository' 'Local directory was not found.'
        continue
    }

    $gitProbe = Invoke-GitRead $repositoryPath @('rev-parse', '--git-dir') -AllowFailure
    if ($gitProbe.ExitCode -ne 0) {
        Add-Finding 'FAIL' $spec.Name 'repository' 'Directory is not a Git working tree.'
        continue
    }

    $branch = (Invoke-GitRead $repositoryPath @('branch', '--show-current')).Lines | Select-Object -First 1
    $head = (Invoke-GitRead $repositoryPath @('rev-parse', 'HEAD')).Lines | Select-Object -First 1
    $status = @((Invoke-GitRead $repositoryPath @('status', '--porcelain=v1', '--untracked-files=all')).Lines | Where-Object { $_ })
    $metadataStatus = @((Invoke-GitRead $repositoryPath @('status', '--porcelain=v1', '--', 'metadata.lua')).Lines | Where-Object { $_ })
    $remotes = @((Invoke-GitRead $repositoryPath @('remote')).Lines | Where-Object { $_ })
    $originResult = Invoke-GitRead $repositoryPath @('remote', 'get-url', 'origin') -AllowFailure
    $originUrl = if ($originResult.ExitCode -eq 0) { $originResult.Lines | Select-Object -First 1 } else { $null }
    $originSlug = ConvertTo-GitHubSlug $originUrl

    $metadataResult = Invoke-GitRead $repositoryPath @('show', 'HEAD:metadata.lua') -AllowFailure
    if ($metadataResult.ExitCode -ne 0) {
        Add-Finding 'FAIL' $spec.Name 'metadata' 'Committed HEAD:metadata.lua was not found.'
        continue
    }

    $metadata = $metadataResult.Lines -join "`n"
    $major = Read-MetadataNumber $metadata 'version_major'
    $minor = Read-MetadataNumber $metadata 'version_minor'
    $revision = Read-MetadataNumber $metadata 'version'
    $modId = Read-MetadataString $metadata 'id'
    $title = Read-MetadataString $metadata 'title'
    $engineVersion = ('{0}.{1:00}-{2:000}' -f $major, $minor, $revision)
    $normalizedVersion = ('{0}.{1}.{2}' -f $major, $minor, $revision)

    if ($spec.Name -eq 'JAZZ') {
        $suiteDisplay = $engineVersion
        $suiteTag = "v$normalizedVersion"
    }

    if ($branch -eq 'main') {
        Add-Finding 'PASS' $spec.Name 'branch' 'main'
    } else {
        Add-Finding 'FAIL' $spec.Name 'branch' "Expected main, found '$branch'."
    }

    if ($status.Count -eq 0) {
        Add-Finding 'PASS' $spec.Name 'working tree' 'Clean.'
    } elseif ($AllowDirty) {
        Add-Finding 'WARN' $spec.Name 'working tree' "Found $($status.Count) changes; allowed for diagnostics only."
    } else {
        Add-Finding 'FAIL' $spec.Name 'working tree' "Found $($status.Count) changes."
    }

    if ($metadataStatus.Count -gt 0) {
        Add-Finding 'WARN' $spec.Name 'metadata source' 'Working-tree metadata differs and is ignored; version comes from HEAD.'
    } else {
        Add-Finding 'PASS' $spec.Name 'metadata source' 'Version comes from committed HEAD.'
    }

    if ($remotes.Count -eq 1 -and $remotes[0] -eq 'origin') {
        Add-Finding 'PASS' $spec.Name 'remotes' 'origin only.'
    } else {
        Add-Finding 'FAIL' $spec.Name 'remotes' "Expected origin only; found: $($remotes -join ', ')."
    }

    if ($SkipOriginCheck) {
        Add-Finding 'WARN' $spec.Name 'origin URL' 'Check skipped.'
    } elseif ($originSlug -and $originSlug.Equals($spec.GitHub, [System.StringComparison]::OrdinalIgnoreCase)) {
        Add-Finding 'PASS' $spec.Name 'origin URL' $spec.GitHub
    } else {
        Add-Finding 'FAIL' $spec.Name 'origin URL' "Expected $($spec.GitHub)."
    }

    if ($SkipRemoteRefCheck) {
        Add-Finding 'WARN' $spec.Name 'origin/main' 'Check skipped.'
    } else {
        $remoteHead = Invoke-GitRead $repositoryPath @('rev-parse', '--verify', 'refs/remotes/origin/main') -AllowFailure
        if ($remoteHead.ExitCode -ne 0) {
            Add-Finding 'FAIL' $spec.Name 'origin/main' 'Remote-tracking ref is missing; run git fetch origin.'
        } elseif (($remoteHead.Lines | Select-Object -First 1) -ne $head) {
            Add-Finding 'FAIL' $spec.Name 'origin/main' 'HEAD does not match the recorded origin/main.'
        } else {
            Add-Finding 'PASS' $spec.Name 'origin/main' 'HEAD matches.'
        }
    }

    if ($spec.Name -eq 'JAZZ') {
        if ($ExpectedTag) {
            if ($ExpectedTag -eq $suiteTag) {
                Add-Finding 'PASS' $spec.Name 'expected tag' $suiteTag
            } else {
                Add-Finding 'FAIL' $spec.Name 'expected tag' "Metadata requires $suiteTag, received $ExpectedTag."
            }
        }

        $tag = @((Invoke-GitRead $repositoryPath @('tag', '--list', $suiteTag)).Lines | Where-Object { $_ })
        if ($tag.Count -eq 0) {
            Add-Finding 'PASS' $spec.Name 'tag' "$suiteTag is locally unused."
        } else {
            Add-Finding 'FAIL' $spec.Name 'tag' "Tag $suiteTag already exists locally."
        }

        if ($title -match '(?i)(?:^|[\s_-])v?\d+\.\d+(?:[.-]\d+)?') {
            Add-Finding 'FAIL' $spec.Name 'metadata title' 'Remove the hard-coded version; JA3 displays the metadata version.'
        } else {
            Add-Finding 'PASS' $spec.Name 'metadata title' 'No hard-coded version.'
        }
    }

    $largeBlobs = @()
    foreach ($line in (Invoke-GitRead $repositoryPath @('ls-tree', '-r', '-l', 'HEAD')).Lines) {
        $match = [regex]::Match($line, '^\d{6}\s+\w+\s+[0-9a-f]{40}\s+(\d+)\t(.+)$')
        if ($match.Success -and [int64]$match.Groups[1].Value -gt 100MB) {
            $largeBlobs += $match.Groups[2].Value
        }
    }
    if ($largeBlobs.Count -eq 0) {
        Add-Finding 'PASS' $spec.Name 'GitHub blob limit' 'No tracked blob exceeds 100 MiB.'
    } else {
        Add-Finding 'FAIL' $spec.Name 'GitHub blob limit' "Git LFS is required for: $($largeBlobs -join ', ')."
    }

    if ($modId -eq $spec.ModId) {
        Add-Finding 'PASS' $spec.Name 'mod id' $modId
    } else {
        Add-Finding 'FAIL' $spec.Name 'mod id' "Expected $($spec.ModId), found '$modId'."
    }

    Add-Finding 'PASS' $spec.Name 'metadata version' "$engineVersion from committed HEAD."

    $states.Add([pscustomobject]@{
        Repository = $spec.Name
        Branch = $branch
        Head = $head
        Dirty = $status.Count
        MetadataVersion = $engineVersion
    }) | Out-Null
}

if ($suiteDisplay -and $suiteTag) {
    Write-Host "Suite release version: $suiteDisplay"
    Write-Host "GitHub tag: $suiteTag"
}

$states | Format-Table Repository, Branch, Head, Dirty, MetadataVersion -AutoSize
$findings | Format-Table Level, Repository, Check, Detail -AutoSize -Wrap

$failures = @($findings | Where-Object { $_.Level -eq 'FAIL' })
if ($failures.Count -gt 0) {
    if ($ReportOnly) {
        Write-Warning "Found $($failures.Count) blockers. ReportOnly did not change repository state."
        exit 0
    }
    Write-Error "Release preflight failed with $($failures.Count) blockers." -ErrorAction Continue
    exit 1
}

Write-Host "Release preflight passed for $suiteTag."
exit 0
