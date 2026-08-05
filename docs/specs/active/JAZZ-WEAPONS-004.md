---
id: JAZZ-WEAPONS-004
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
  - combat-cth-actions
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/System_Firearm_AddProperties.lua
  - jazz/Code/*Reload*.lua
  - jazz/InventoryItem/*.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz/docs/specs/active/JAZZ-WEAPONS-004.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/combat-actions.md
  - jazz/docs/technical/weapons/data/weapons.csv
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/wiki/combat-actions.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/showcase/ru/combat-actions.md
  - jazz/docs/showcase/en/combat-actions.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-002
  - JAZZ-WEAPONS-003
approved_by: project-owner
---

# JAZZ-WEAPONS-004: поэлементная перезарядка (tube / break / revolver)

## Проблема

1. Перезарядка в JA3/JAZZ — один полный `ReloadAP` на весь магазин, даже когда конструкция позволяет **добавить один патрон** (трубчатый магазин дробовика, внутренний магазин рычажника, ствол двустволки, камора револьвера).
2. Тактически невыгодно и нереалистично: нельзя «добить» один патрон в R870 за малую долю AP, когда полный reload = 7 AP на 6 мест.
3. Магазинные платформы (АК, M4, AA12/USAS) наоборот должны оставаться только полной сменой магазина — не путать с tube-fed.

## Цели

1. Ввести `ReloadStyle` на Firearm: какие стволы умеют поэлементную дозарядку.
2. **UI/действие по состоянию магазина** (для `Tube` / `Break` / `Revolver`):
   - магазин **пуст** → обычная **«Перезарядка»** (полный `ReloadAP`, как сейчас);
   - магазин **не пуст** и не полон → вместо перезарядки показывается **«Дозарядить»** (+1 патрон за unit AP);
   - магазин полон → reload/дозарядка недоступны.
3. Unit AP = доля полного `ReloadAP`:
   ```text
   ReloadUnitAP = max(1_AP, CeilDiv(ReloadAP_effective, MagazineSize))
   ```
4. Box-magazine / belt / drum **без** per-round (только полный reload всегда).
5. Docs + wiki + showcase RU/EN.

## Non-goals

- Две кнопки сразу («Перезарядка» + «Дозарядить») в v1 — только **замена** действия по состоянию магазина.
- Случайная длина / partial mag dump в середине хода без явного действия.
- Переписывать экономику `ReloadAP` всех стволов с нуля (только unit поверх текущего full).
- WEAPONS-002 removable mag containers (координировать порядок; 004 не блокирует 002, но не дублирует mag-as-item).
- WEAPONS-003 recoil/RPM (отдельный change set; оба exclusive `items.lua` — **не параллелить**).
- AI-идеальный «добей 1 и стреляй» как отдельный POL-spec — минимум: AI **может** вызвать unit reload; тонкая политика — follow-up.
- Stripper clip / en-bloc как отдельный мини-игры (M1 Garand) — later; в v1 Garand = Magazine full-only, если не tube.

## ReloadStyle (authored)

| Style | Поведение | Примеры |
| --- | --- | --- |
| `Magazine` | только полный reload (default) | AR, SMG, mag-fed shotgun (AA12, USAS12) |
| `Tube` | unit +1 в магазин до MagSize | R870, Ithaca, Auto5, Winchester1894, … |
| `Break` | unit +1 в пустой ствол до MagSize (обычно 2) | DoubleBarrelShotgun |
| `Revolver` | unit +1 в камору (v1); пустой барабан → полный reload | Colt/S&W revolvers |

Свойство: `ReloadStyle` (string/enum), default `Magazine`. Заполняется на активных стволах, где style ≠ Magazine.

Опционально позже: `ReloadUnitAPOverride` — не в v1 (формула от full достаточна).

## Стоимость AP

```text
full = weapon:GetReloadAP()   # уже с компонентами Reduce/Increase ReloadAP
cap  = weapon.MagazineSize
unit = Max(const.Scale.AP, DivCeil(full, Max(1, cap)))   # CeilDiv; floor 1 AP
```

- Каждое **«Дозарядить»**: −`unit` AP, +1 патрон (совместимый ammo), не выше MagSize; только если **уже есть ≥1** патрон в оружии.
- Можно повторять, пока есть AP, патроны и свободные места (каждый раз снова «Дозарядить»).
- **«Перезарядка»** (полный `full` AP): когда магазин **пуст** (0 патронов) — заливает по правилам vanilla до MagSize / доступному ammo.
- На `Magazine` style — всегда только «Перезарядка», без «Дозарядить».

UI (v1): одно слот-действие reload — либо «Перезарядка», либо «Дозарядить» по состоянию; не две кнопки рядом.

RU DisplayName unit: **«Дозарядить»** / EN: **«Top up»**.

## Требования

- `JAZZ-WEAPONS-004-REQ-001` — `ReloadStyle` на Firearm; default `Magazine`; Tube/Break/Revolver проставлены на целевых пресетах; CSV колонка.
- `JAZZ-WEAPONS-004-REQ-002` — unit reload AP = `CeilDiv(effective ReloadAP, MagazineSize)`, не меньше 1 AP; детерминировано.
- `JAZZ-WEAPONS-004-REQ-003` — при `ReloadStyle ∈ {Tube,Break,Revolver}`: ammo==0 → действие «Перезарядка» (full); 0 < ammo < MagSize → вместо него «Дозарядить» (unit); ammo==MagSize → недоступно. На `Magazine` — только «Перезарядка».
- `JAZZ-WEAPONS-004-REQ-004` — mag-fed shotguns (AA12, USAS12 и аналоги) остаются `Magazine` — без per-round.
- `JAZZ-WEAPONS-004-REQ-005` — `n × unit ≥ full` для n = MagSize (ceil-свойство); полный reload с пустого не удаляется.
- `JAZZ-WEAPONS-004-REQ-006` — RU **«Дозарядить»** / EN **«Top up»**; docs/wiki/showcase sync.
- `JAZZ-WEAPONS-004-REQ-007` — револьверы в **v1** (`ReloadStyle=Revolver`).

## Инварианты и ограничения

- Deterministic AP и расход патронов.
- Не ломать jam / unjam / WEAPONS-001 Reliability.
- Exclusive `items.lua` — не параллелить с WEAPONS-002/003.
- Network: тот же CombatAction path, seeded как reload.

## Acceptance criteria

- `JAZZ-WEAPONS-004-AC-001` — static: R870/Ithaca/Winchester = Tube; DoubleBarrel = Break; sample revolver = Revolver; AA12/USAS12 = Magazine; AR = Magazine.
- `JAZZ-WEAPONS-004-AC-002` — static/runtime: R870 ReloadAP=7000 Mag=6 → unit = 2000 (2 AP) или точный CeilDiv движка; шесть unit ≥ full.
- `JAZZ-WEAPONS-004-AC-003` — runtime: пустой R870 → «Перезарядка» full; при 5/6 → только «Дозарядить» unit, не full-кнопка рядом; +1 патрон.
- `JAZZ-WEAPONS-004-AC-004` — runtime: на M4/AK нет «Дозарядить».
- `JAZZ-WEAPONS-004-AC-005` — runtime: sample revolver — пустой барабан = Перезарядка; частично = Дозарядить.
- `JAZZ-WEAPONS-004-AC-006` — human: добить один при малом AP читается; с пустого — привычная перезарядка.
- `JAZZ-WEAPONS-004-AC-007` — docs/wiki/showcase RU/EN обновлены.

## Impact и совместимость

- Vanilla reload override / новый CombatAction.
- Saves: новый preset field; instance ammo count без schema break.
- Координация: порядок vs WEAPONS-003 **не важен**; **не** в одном commit с 003; 002 removable — не дублировать mag item.

## План и ownership

- Пакет: `jazz`
- Exclusive: `jazz/items.lua`
- Реализация — по отдельной команде владельца (как 002/003/005).

## Открытые решения для владельца (до approve)

*Нет открытых пунктов.* Spec **approved**.

**Закрыто направлением владельца (chat):**

- Unit AP = **CeilDiv(ReloadAP, MagSize)**, min 1 AP.
- Только где конструкция позволяет (не box mag).
- UI v1: **«Дозарядить» вместо перезарядки** когда маг не пуст; **пустой маг → «Перезарядка»**.
- Револьверы **в v1**.
- Порядок vs WEAPONS-003: **всё равно** (не один commit).
- EN DisplayName: **Top up**.

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner
- Дата: 2026-08-01
- Решение: approve WEAPONS-004; implement по команде.

## Evidence

- `JAZZ-WEAPONS-004-AC-001`: `PASS` (static) — `items.lua` tags Tube/Break/Revolver; AA12/USAS12 retain the `Magazine` default.
- `JAZZ-WEAPONS-004-AC-002`: `PASS` (static) — `Firearm:GetReloadUnitAP()` uses `Max(const.Scale.AP, DivCeil(ReloadAP, MagazineSize))`; R870 `7000/6` is `2000`.
- `JAZZ-WEAPONS-004-AC-003`: `PASS` (static) / `BLOCKED` (runtime) — Top up path now passes `max_add=1` into `Firearm:Reload` (vanilla filled MagSize per call; stack-loop break alone was insufficient). Runtime wave still pending.
- `JAZZ-WEAPONS-004-AC-004`: `BLOCKED` (runtime) — wave test pending.
- `JAZZ-WEAPONS-004-AC-005`: `BLOCKED` (runtime) — wave test pending.
- `JAZZ-WEAPONS-004-AC-006`: `BLOCKED` (human) — readability in combat HUD pending.
- `JAZZ-WEAPONS-004-AC-007`: `PASS` (static) — technical, wiki and RU/EN showcase pages updated.

## Documentation delta

При реализации:

- technical weapons-ammo + combat-actions;
- wiki + showcase RU/EN weapons/combat-actions;
- weapons.csv `reload_style`.
