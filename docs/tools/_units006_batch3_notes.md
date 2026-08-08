# UNITS-006 batch 3 notes (§C signatures / CD-kill)

## Done

| Id | Effect |
| --- | --- |
| `BulletHell` | Signature recharge **on kill** (`Unit:BulletHell` + `recharge_on_kill` param) |
| `MakeThemBleed` | +10% dmg per bleeding enemy in sight, cap +50% |
| `DedicatedCamper` | Stationary +25% dmg; ≥25 dmg → +15 Grit |
| `TagTeam` | +15 CTH vs ally Pin Down targets |
| `BunsPerk` | +10 CTH vs ally-damaged targets this turn |
| `HawksEye` | `pindownCostOverwrite=1`; sniper Will suppress ×2 |
| `Spotter` | Pin Down → Marked + next hit 100% crit pending |
| `HaveABlast` | Own grenade blast dmg ×50% |
| `KillingWind` | ≥2 hit units → +8 Grit (FM/armor path kept from COMBAT-005) |
| `BuildingConfidence` | Inspired turn 2 and every 3rd turn |
| `SidneyPerk` | +2 AP/turn until miss or damage taken |
| `OnMyTarget` | Text: 10 AP (vanilla ActionPoints already 10000) |

Loc IDs: `890000000009861–9884` (never 6300–6599 VR band). Upsert refuses VoiceResponse overwrite.

## Soft cuts

- GloryHog recruit / non-straight charge
- RecklessAssault 4-attack rewrite
- BuildingConfidence heal ±10%/level combat+sat
- MakeThemBleed groin/animal bleed apply (aura only)
- Ice five-limb shot list
- Buns tracking depends on `Unit.OnAttack` wrap (fallback if missing)

## Tools

- `docs/tools/_gen_units006_batch3.py`
- `docs/tools/_fix_units006_batch3_loc.py`
