[CmdletBinding()]
param(
    [string]$SuiteRoot = '.',
    [string]$AssetsRoot = '',
    [switch]$Strict,
    [switch]$SelfTest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-RegisteredEntityNames {
    param([Parameter(Mandatory)][string]$MetadataPath)

    $text = [IO.File]::ReadAllText($MetadataPath, [Text.Encoding]::UTF8)
    $entities = [regex]::Match(
        $text,
        "(?s)['""]entities['""]\s*,\s*\{(?<body>.*?)\}\s*,"
    )
    if (-not $entities.Success) {
        throw "Cannot parse metadata.entities: $MetadataPath"
    }

    $names = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($match in [regex]::Matches($entities.Groups['body'].Value, '["''](?<name>[^"'']+)["'']')) {
        [void]$names.Add($match.Groups['name'].Value)
    }
    return ,$names
}

function Get-RelativeAssetPath {
    param(
        [Parameter(Mandatory)][string]$Root,
        [Parameter(Mandatory)][string]$Path
    )

    return $Path.Substring($Root.Length + 1).Replace('\', '/')
}

function Test-CollisionTriangle {
    param([Parameter(Mandatory)][string]$Points)

    $rawPoints = @($Points.Split(';', [StringSplitOptions]::RemoveEmptyEntries) |
        ForEach-Object { $_.Trim() })
    if ($rawPoints.Count -ne 3) {
        return [pscustomobject]@{
            Valid = $false
            Reason = "expected 3 vertices, found $($rawPoints.Count)"
        }
    }

    $unique = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($point in $rawPoints) {
        [void]$unique.Add($point)
    }
    if ($unique.Count -ne 3) {
        return [pscustomobject]@{
            Valid = $false
            Reason = 'duplicate vertices'
        }
    }

    $vectors = @()
    foreach ($point in $rawPoints) {
        $rawCoordinates = @($point.Split(','))
        if ($rawCoordinates.Count -ne 3) {
            return [pscustomobject]@{
                Valid = $false
                Reason = "expected 3 coordinates, found $($rawCoordinates.Count)"
            }
        }

        $parts = @()
        foreach ($rawCoordinate in $rawCoordinates) {
            $value = 0.0
            if (-not [double]::TryParse(
                $rawCoordinate,
                [Globalization.NumberStyles]::Float,
                [Globalization.CultureInfo]::InvariantCulture,
                [ref]$value
            )) {
                return [pscustomobject]@{
                    Valid = $false
                    Reason = "non-numeric coordinate '$rawCoordinate'"
                }
            }
            $parts += $value
        }
        $vectors += ,$parts
    }

    $abX = [double]($vectors[1][0]) - [double]($vectors[0][0])
    $abY = [double]($vectors[1][1]) - [double]($vectors[0][1])
    $abZ = [double]($vectors[1][2]) - [double]($vectors[0][2])
    $acX = [double]($vectors[2][0]) - [double]($vectors[0][0])
    $acY = [double]($vectors[2][1]) - [double]($vectors[0][1])
    $acZ = [double]($vectors[2][2]) - [double]($vectors[0][2])
    $crossX = $abY * $acZ - $abZ * $acY
    $crossY = $abZ * $acX - $abX * $acZ
    $crossZ = $abX * $acY - $abY * $acX
    $areaSquared = $crossX * $crossX + $crossY * $crossY + $crossZ * $crossZ
    if ($areaSquared -le 1.0e-12) {
        return [pscustomobject]@{
            Valid = $false
            Reason = 'collinear vertices'
        }
    }

    return [pscustomobject]@{
        Valid = $true
        Reason = ''
    }
}

function Invoke-AssetIntegrityAudit {
    param([Parameter(Mandatory)][string]$PackageRoot)

    $resolvedPackage = (Resolve-Path -LiteralPath $PackageRoot).Path
    $entitiesRoot = Join-Path $resolvedPackage 'Entities'
    $metadataPath = Join-Path $resolvedPackage 'metadata.lua'
    $itemsPath = Join-Path $resolvedPackage 'items.lua'
    foreach ($required in @($entitiesRoot, $metadataPath, $itemsPath)) {
        if (-not (Test-Path -LiteralPath $required)) {
            throw "Missing required assets path: $required"
        }
    }

    $registered = Get-RegisteredEntityNames -MetadataPath $metadataPath
    $allPaths = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($file in Get-ChildItem -LiteralPath $entitiesRoot -Recurse -File) {
        [void]$allPaths.Add((Get-RelativeAssetPath -Root $entitiesRoot -Path $file.FullName))
    }

    $entFiles = @(Get-ChildItem -LiteralPath $entitiesRoot -File -Filter '*.ent')
    $entNames = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($file in $entFiles) {
        [void]$entNames.Add($file.BaseName)
    }

    $errors = [System.Collections.Generic.List[string]]::new()
    $warnings = [System.Collections.Generic.List[string]]::new()
    $absoluteSourceCount = 0

    function Add-EntityIssue {
        param(
            [Parameter(Mandatory)][string]$EntityName,
            [Parameter(Mandatory)][string]$Message
        )

        $formatted = "Entities/$EntityName.ent: $Message"
        if ($registered.Contains($EntityName)) {
            $errors.Add($formatted) | Out-Null
        } else {
            $warnings.Add("$formatted [dormant/unlisted]") | Out-Null
        }
    }

    foreach ($entityName in $registered) {
        if (-not $entNames.Contains($entityName)) {
            $errors.Add("metadata.entities: registered '$entityName', but Entities/$entityName.ent is missing or has different casing.") | Out-Null
        }
    }

    foreach ($file in $entFiles) {
        $entityName = $file.BaseName
        try {
            [xml]$xml = [IO.File]::ReadAllText($file.FullName, [Text.Encoding]::UTF8)
        } catch {
            Add-EntityIssue -EntityName $entityName -Message "XML parse error: $($_.Exception.Message)"
            continue
        }

        if (-not $xml.entity) {
            Add-EntityIssue -EntityName $entityName -Message 'root <entity> element is missing.'
            continue
        }

        $declaredName = [string]$xml.entity.name
        if ($declaredName -and $declaredName -cne $entityName) {
            Add-EntityIssue -EntityName $entityName -Message "entity.name='$declaredName' does not match the file name."
        }

        $seenStates = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        foreach ($state in @($xml.entity.state)) {
            $stateId = [string]$state.id
            if ($stateId -and -not $seenStates.Add($stateId)) {
                Add-EntityIssue -EntityName $entityName -Message "duplicate state id '$stateId'."
            }
        }

        $meshIds = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        foreach ($description in @($xml.entity.mesh_description)) {
            $meshId = [string]$description.id
            if ($meshId) {
                [void]$meshIds.Add($meshId)
            }
        }
        foreach ($meshRef in @($xml.SelectNodes('//mesh_ref'))) {
            $ref = [string]$meshRef.ref
            if ($ref -and -not $meshIds.Contains($ref)) {
                Add-EntityIssue -EntityName $entityName -Message "mesh_ref '$ref' has no local mesh_description."
            }
        }

        foreach ($resource in @($xml.SelectNodes('//mesh|//material'))) {
            $relative = ([string]$resource.file).Replace('\', '/')
            if (-not $relative) {
                continue
            }
            if ($allPaths.Contains($relative)) {
                continue
            }

            $caseInsensitivePath = Join-Path $entitiesRoot $relative.Replace('/', '\')
            if (Test-Path -LiteralPath $caseInsensitivePath) {
                Add-EntityIssue -EntityName $entityName -Message "resource path has incorrect casing: '$relative'."
            } else {
                Add-EntityIssue -EntityName $entityName -Message "resource is missing: '$relative'."
            }
        }

        foreach ($source in @($xml.SelectNodes('//src'))) {
            if ([string]$source.file -match '^[A-Za-z]:[/\\]') {
                $absoluteSourceCount++
            }
        }

        foreach ($surface in @($xml.SelectNodes('//surf[@type="collision"]'))) {
            $points = [string]$surface.points
            $triangle = Test-CollisionTriangle -Points $points
            if (-not $triangle.Valid) {
                Add-EntityIssue -EntityName $entityName -Message "degenerate collision triangle ($($triangle.Reason)): '$points'."
            }
        }
    }

    return [pscustomobject]@{
        PackageRoot = $resolvedPackage
        Registered = $registered.Count
        EntityFiles = $entFiles.Count
        Errors = @($errors | Sort-Object -Unique)
        Warnings = @($warnings | Sort-Object -Unique)
        AbsoluteSourcePaths = $absoluteSourceCount
    }
}

function Invoke-AssetIntegritySelfTest {
    $fixtureRoot = Join-Path ([IO.Path]::GetTempPath()) ("jazz-asset-integrity-" + [guid]::NewGuid().ToString('N'))
    try {
        $entities = New-Item -ItemType Directory -Path (Join-Path $fixtureRoot 'Entities') -Force
        [IO.File]::WriteAllText(
            (Join-Path $fixtureRoot 'metadata.lua'),
            "return PlaceObj('ModDef', {`n  'entities', {`n    `"Broken`",`n  },`n})`n",
            [Text.UTF8Encoding]::new($false)
        )
        [IO.File]::WriteAllText(
            (Join-Path $fixtureRoot 'items.lua'),
            "return {}`n",
            [Text.UTF8Encoding]::new($false)
        )
        [IO.File]::WriteAllText(
            (Join-Path $entities.FullName 'Broken.ent'),
            @'
<?xml version="1.0" encoding="UTF-8"?>
<entity path="" name="Broken">
  <state id="idle"><mesh_ref ref="Broken"/></state>
  <mesh_description id="Broken">
    <lod idx="0" distance="0">
      <mesh file="Meshes/missing.hgm"/>
      <material file="Materials/missing.mtl"/>
    </lod>
    <surf type="collision" name="PVS" points="0,0,0;1,0,0;0,0,0"/>
  </mesh_description>
</entity>
'@,
            [Text.UTF8Encoding]::new($false)
        )

        $result = Invoke-AssetIntegrityAudit -PackageRoot $fixtureRoot
        if ($result.Errors.Count -lt 3) {
            throw "Self-test expected at least 3 blocking errors, found $($result.Errors.Count)."
        }
        if (-not ($result.Errors -match 'resource is missing')) {
            throw 'Self-test did not detect a missing resource.'
        }
        if (-not ($result.Errors -match 'duplicate vertices')) {
            throw 'Self-test did not detect duplicate collision vertices.'
        }
        Write-Host "Asset integrity self-test passed: errors=$($result.Errors.Count)."
    } finally {
        if (Test-Path -LiteralPath $fixtureRoot) {
            Remove-Item -LiteralPath $fixtureRoot -Recurse -Force
        }
    }
}

if ($SelfTest) {
    Invoke-AssetIntegritySelfTest
    exit 0
}

if (-not $AssetsRoot) {
    $resolvedSuite = (Resolve-Path -LiteralPath $SuiteRoot).Path
    $AssetsRoot = Join-Path (Split-Path -Parent $resolvedSuite) 'jazz_assets'
}

try {
    $audit = Invoke-AssetIntegrityAudit -PackageRoot $AssetsRoot
} catch {
    Write-Error $_
    exit 1
}

Write-Host 'JAZZ asset integrity audit (read-only)'
Write-Host ("[jazz_assets] registered={0}; ent_files={1}; errors={2}; warnings={3}; absolute_src={4}" -f
    $audit.Registered,
    $audit.EntityFiles,
    $audit.Errors.Count,
    $audit.Warnings.Count,
    $audit.AbsoluteSourcePaths)

foreach ($message in $audit.Errors) {
    Write-Host "ERROR [jazz_assets] $message"
}
foreach ($message in $audit.Warnings) {
    Write-Host "WARNING [jazz_assets] $message"
}
if ($audit.AbsoluteSourcePaths -gt 0) {
    Write-Host "INFO [jazz_assets] legacy absolute <src file> paths: $($audit.AbsoluteSourcePaths); non-blocking technical debt."
}

if ($audit.Errors.Count -gt 0) {
    Write-Host "RESULT: FAILED ($($audit.Errors.Count) error(s))"
    exit 1
}
if ($Strict -and $audit.Warnings.Count -gt 0) {
    Write-Host "RESULT: FAILED STRICT ($($audit.Warnings.Count) warning(s))"
    exit 2
}

Write-Host 'RESULT: PASSED'
exit 0
