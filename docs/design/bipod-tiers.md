# Сошки (Bipod) — prone only

Канон. Apply: `docs/tools/_rebalance_bipod_tiers.py` (+ `_fix_dup_bipod.py` если remap оставил дубли).  
Связано: `attachments-rebalance.md`, `JAZZ-ATTACH-001`.

**Статус:** applied 2026-08-01.

## Роли

| ID | Slot | Эффект |
| --- | --- | --- |
| `JAZZ_Bipod` | **Bipod** (единственный) | prone CTH **+10** + ShotsBeforeRecoilProne **+1** |
| `JAZZ_Bipod_Under` | Under | то же |
| `JAZZ_Bipod_Galil` | Under | то же |

**Вырезаны** (remap → `JAZZ_Bipod`): `Bipod_MG42`, `KSP_BIPOD`, `FoldBipod`, `UnfoldBipod`.

Cost **50**, Diff **10**.

## Инварианты

1. Нет always-on flat CTH вне prone/half-cover path.
2. Один ID на слот Bipod; Under-варианты остаются.
3. Fold/Unfold pair не поддерживаем.
