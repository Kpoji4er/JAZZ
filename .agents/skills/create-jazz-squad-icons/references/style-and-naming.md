# Style bible и naming

## Canvas и щит

| Свойство | Значение |
| --- | --- |
| Размер | `64×64` |
| Фон вне щита | прозрачный (`A=0`), как у `legion.png` |
| Щит | плоский верх, вертикальные бока, остриё снизу |
| Символ | ivory/cream ≈ `RGB(230,222,202)`, толстый силуэт |
| Outline символа | тёмный ≈ `RGB(48,28,28)`, 1px |
| Стиль | flat 2D UI badge, без текста/цифр/градиентов/фотореализма |

Фракционные щиты (подложки):

| faction | файл | вид |
| --- | --- | --- |
| `legion` | `legion.png` | madder-red |
| `army` | `army.png` | красно-коричневый camo |
| `adonis` | `adonis.png` | purple |
| `rebels` | `rebels.png` | green camo |
| `smugglers` | `smugglers.png` | money/orange |

## Naming

```text
<faction>_<ROLE>_squad.png
Mod/e6L4ECj/SquadsIcons/Enemy/<faction>_<ROLE>_squad.png
```

`ROLE` — `SCREAMING_SNAKE` без пробелов (`TAX`, `REINFORCE`, `QRF`).

## Занятые символы (не повторять без причины)

| ROLE | Символ |
| --- | --- |
| BASE / major | череп |
| GARRISON | башня / rook |
| PATROL | скрещённые стрелы |
| RECON | бинокль |
| QRF | тесак / cutlass |
| SUPPLY | грузовик |
| SHIPMENT | грузовик + ромб |
| REINFORCE | плюс |
| RETRIBUTION | кулак |
| RECRUITER | мегафон |
| MANPOWER | колонна солдат с флагом |
| TAX | мешок с монетами |

## Промпт GenerateImage (шаблон)

Подставить `SYMBOL_DESCRIPTION` и приложить `reference_image_paths` на `legion.png` + 2–3 существующих role PNG.

```text
Create ONE Jagged Alliance 3 64x64 satellite squad icon matching references EXACTLY.

Canvas: square. Background outside the shield must be easy to key out (solid black is OK in draft).
Center: muted madder-red/burgundy pentagonal shield identical to references
(flat top, vertical sides, pointed bottom), thin dark outline, same size/margins.
Style: flat 2D minimalist UI badge, no gradients, no textures, no drop shadows,
no bevels, no frames, no text, no numbers.

SCALE: ivory symbol about half to 60% of shield height with clear red margins.
Thick chunky shapes for tiny-size readability.

SYMBOL: SYMBOL_DESCRIPTION

MUST NOT collide with: skull, single garrison tower, crossed arrows, binoculars,
cutlass, supply truck, diamond truck, plus sign, fist, megaphone, marching soldiers,
money bag — unless replacing that exact role.

Colors ONLY: black draft bg, muted red shield, ivory/cream symbol.
```

После генерации всегда прогонять композит на настоящий щит фракции — draft с чёрным фоном в репозиторий не класть.

## Композит: критичные баги

1. **Прозрачный canvas исходника** хранит `RGBA(255,255,255,0)`. Без проверки `A >= 200` маска ivory заливает весь фон бежевым.
2. **Непрозрачный чёрный фон** ломает контракт с базовыми щитами; в игре нужен прозрачный canvas.
3. **Rim-линия по верху щита** — ivory/outline на первых рядах щита; чистить по маске щита.

## Референс каталога

Актуальная галерея и статусы wired/asset only: `docs/technical/systems/squad-role-icons.md`.
