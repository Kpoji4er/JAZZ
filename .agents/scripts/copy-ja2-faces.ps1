[Console]::OutputEncoding = [Text.UTF8Encoding]::new()
$ErrorActionPreference = 'Stop'
$extractRoot = Join-Path $env:TEMP 'jazz-ja2-faces'
$root = Get-ChildItem -LiteralPath $extractRoot -Directory | Select-Object -First 1
$dest = 'C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\docs\design\mercs-ja12'

# Match by unique substrings in source filenames (UTF-8 script file)
$rules = @(
  @{ needle = 'Рысь'; slug = 'lynx' },
  @{ needle = 'Тоска'; slug = 'tosca' },
  @{ needle = 'Паук'; slug = 'spider' },
  @{ needle = 'Колби'; slug = 'colby' },
  @{ needle = 'Бритва'; slug = 'blade' },
  @{ needle = 'Айра'; slug = 'ira' },
  @{ needle = 'Димитрий'; slug = 'dimitri' },
  @{ needle = 'бешеный'; slug = 'madman' },
  @{ needle = 'Гром'; slug = 'grom' },
  @{ needle = 'Майк.gif'; slug = 'mike' },
  @{ needle = 'Знаток'; slug = 'allik' },
  @{ needle = 'Конрад'; slug = 'conrad' },
  @{ needle = 'Ротман'; slug = 'rothman' },
  @{ needle = 'Квинтен'; slug = 'quinten' },
  @{ needle = 'Злобный'; slug = 'vicious' },
  @{ needle = 'Нервный'; slug = 'nervous' },
  @{ needle = 'Габриель'; slug = 'flo' },
  @{ needle = 'Пума'; slug = 'cougar' },
  @{ needle = 'Мигель'; slug = 'miguel' },
  @{ needle = 'Гамос'; slug = 'gamos' },
  @{ needle = 'Динамо'; slug = 'dynamo' },
  @{ needle = 'Гастон'; slug = 'gaston' },
  @{ needle = 'Сигара'; slug = 'horg' },
  @{ needle = 'Мануэль'; slug = 'manuel' },
  @{ needle = 'Монк'; slug = 'monk' },
  @{ needle = 'Хеннинг'; slug = 'henning' },
  @{ needle = 'Статик'; slug = 'static' },
  @{ needle = 'Скала'; slug = 'highball' },
  @{ needle = 'Бык'; slug = 'bull' },
  @{ needle = 'Кардан'; slug = 'cord' },
  @{ needle = 'Хоббит'; slug = 'hobbit' },
  @{ needle = 'Рикошет'; slug = 'ricochet' },
  @{ needle = 'Мясо'; slug = 'meat' },
  @{ needle = 'Карлос'; slug = 'carlos' },
  @{ needle = 'Девин'; slug = 'devin' },
  @{ needle = 'Шенк'; slug = 'shank' },
  @{ needle = 'Воймонт'; slug = 'vince' },
  @{ needle = 'Убийца'; slug = 'hitman' },
  @{ needle = 'Биггенс'; slug = 'biggens' },
  @{ needle = 'Кульба'; slug = 'kulba' },
  @{ needle = 'Зануда'; slug = 'vilde' },
  @{ needle = 'Грейс'; slug = 'grace' },
  @{ needle = 'Штайгер'; slug = 'steiger' },
  @{ needle = 'Лаки'; slug = 'lucky' },
  @{ needle = 'Лора Колин'; slug = 'laura' },
  @{ needle = 'Эскимо'; slug = 'eskimo' }
)

$copied = New-Object System.Collections.Generic.List[object]
$unmatched = New-Object System.Collections.Generic.List[string]

Get-ChildItem -LiteralPath $root.FullName -Recurse -File |
  Where-Object { $_.Extension -match '\.(gif|jpg|jpeg|png)$' -and $_.Name -notmatch '^ГГ ' } |
  ForEach-Object {
    $name = $_.Name
    $slug = $null
    foreach ($r in $rules) {
      if ($name.IndexOf($r.needle, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
        $slug = $r.slug
        break
      }
    }
    if (-not $slug) {
      [void]$unmatched.Add($name)
      return
    }
    $ext = $_.Extension.ToLowerInvariant()
    $targetName = "$slug.ja2-face$ext"
    $target = Join-Path $dest $targetName
    Copy-Item -LiteralPath $_.FullName -Destination $target -Force
    [void]$copied.Add([pscustomobject]@{ slug = $slug; file = $targetName; src = $name })
  }

$report = Join-Path $dest '_ja2-faces-map.txt'
$lines = @('slug`tfile`tsource') + ($copied | Sort-Object slug | ForEach-Object { "$($_.slug)`t$($_.file)`t$($_.src)" })
[IO.File]::WriteAllLines($report, $lines, [Text.UTF8Encoding]::new($true))

Write-Output "copied=$($copied.Count)"
Write-Output 'unmatched:'
$unmatched
Write-Output "faces_on_disk=$((Get-ChildItem -LiteralPath $dest -Filter '*.ja2-face*').Count)"

$xlsx = Get-ChildItem -LiteralPath $root.FullName -Recurse -Filter '*.xlsx' | Select-Object -First 1
if ($xlsx) {
  Copy-Item -LiteralPath $xlsx.FullName -Destination (Join-Path $dest '_ja2-faces-notes.xlsx') -Force
  Write-Output 'xlsx_ok'
}
