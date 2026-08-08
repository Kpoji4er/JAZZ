# UNITS-006 batch 4 notes (§B JA12 stubs)

## Priority (wired)

| Id | Before | After |
| --- | --- | --- |
| `Jazz_Perk_Flo` | «Барахольщица» WIP stub | «Теоретически подкована»: −12% Bobby Ray buy / +12% CashIn; Flo in player squad; additive with Negotiator (ops/boat stay Negotiator) |
| `Jazz_Perk_Static` | «Экономия запчастей» WIP stub | «Собрал на коленке»: Parts −5%×Level repair/craft estimate + ModifyWeaponDlg, cap −25% |
| `Jazz_Perk_Cougar` | «Мягкая лапа» WIP stub | Shots −33% noise (`PushUnitAlert`); Stealth Kill → Inspired 1×/turn (not AP) |

## Text + cheap hooks

| Id | Hook |
| --- | --- |
| `Jazz_Perk_Grace` | First `KnifeThrow`/turn CTH=100 if ≤12 |
| `Jazz_Perk_Kulba` | US autos −50% via `JAZZ_CTHGetRecoilProfile` wrap |
| `Jazz_Perk_Grom` | GL/mortar/AT suppress ×2 (`Jazz_ApplyGromSuppression`) |
| `Jazz_Perk_Ricochet` | Melee splash ~35% to enemy ≤1 from target |
| `Jazz_Perk_Highball` | `OnCalcHealAmount` ±50% if ally Med≥80 within 5 |
| `Jazz_Perk_Meat` | `OnCalcPersonalMorale` floors negative morale |
| `Jazz_Perk_Carlos` | Text only (detection / failed-SK stay Hidden deferred) |
| `Jazz_Perk_Iggy` | Text + helper `Jazz_ApplyIggyMortarScatter` (bombard call-site soft) |
| `Jazz_Perk_Monk` / `Horg` / `Manuel` / `Hitman` | Text only — active signatures TBD |
| `Jazz_Perk_Bull` | Text only — fist trauma / +2 slots TBD |

## Soft cuts → batch5 / later

- Rothman mine op, Biff paid troopers, Ira militia train, Miguel aura, Livewire money, Barry craft, Thor joints
- Carlos detection −33% + failed SK stay Hidden
- Iggy mortar scatter wired into bombard path
- Meat Will→Grit + unsuppressible
- Highball satellite-in-squad path
- Bull inventory slots + body-part fist trauma
- Monk / Horg / Manuel / Hitman JA12 CombatAction signatures (CD on kill)
- Local sector-merchant buy/sell (JA3 has no Negotiator shop pipeline; Flo = Bobby Ray + CashIn)

## Tools

- `docs/tools/_gen_units006_batch4.py`
- Loc: reuse existing CE IDs (3000/4100/3100/…); upsert refuses VoiceResponse overwrite
