param(
    [string]$Path = "Russian.csv",
    [long]$Lo = 890000000002400,
    [long]$Hi = 890000000003500
)
$matches = Select-String -Path $Path -Pattern '890000000\d{6}' -AllMatches
$ids = @()
foreach ($m in $matches) {
    foreach ($mm in $m.Matches) {
        $ids += [int64]$mm.Value
    }
}
$ids = $ids | Sort-Object -Unique
Write-Host "Total unique ids: $($ids.Count)"
Write-Host "Max id: $($ids | Measure-Object -Maximum | Select-Object -ExpandProperty Maximum)"
Write-Host "In range ${Lo}-${Hi}:"
$ids | Where-Object { $_ -ge $Lo -and $_ -le $Hi } | ForEach-Object { Write-Host $_ }
