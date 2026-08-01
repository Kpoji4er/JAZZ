# Физическая шкала отдачи (JAZZ-WEAPONS-003)

`Recoil` — авторское число тяжести потери точности следующих пуль, а не
runtime-симуляция массы. Все active firearms получают `WeaponMass` (десятые кг),
`CyclicRPM`, `WeaponSizeClass` (`Compact` / `Carbine` / `Rifle` / `Long`) и
`BurstLimiter` (0 = нет механической отсечки).

```text
mass_f = clamp(35 / WeaponMass, 0.70, 1.45)
size_f = Compact 1.15 / Carbine 1.00 / Rifle 0.92 / Long 0.85
rpm_f  = 1 + clamp((CyclicRPM - 700) / 2000, -0.08, 0.18)
Recoil = clamp(round(impulse * mass_f * size_f * rpm_f * family_f), familyMin, 70)
```

Impulse bands: pistol soft 8–10; pistol/SMG 11–14; light intermediate 16–18;
heavy intermediate 22–26; battle/full 36–42; heavy MG/.50 48–55. Explicit
anchors win: AK74 **15**, AKM **25**, FN FAL **43**.

`BurstShots = clamp(round(RPM / 200), 2..8)` and
`AutoShots = clamp(round(RPM / 100), 3..14)` only when the corresponding fire
mode exists. `BurstLimiter` caps burst only; belt/MG auto is capped at 10.
There is no random burst-length variance.

The 9×19 validation set deliberately differentiates platforms: Micro UZI
(27 / 1200 / Compact) has Recoil 21, versus Sterling (33 / 550 / Carbine) 18.
Mass/RPM/size never multiply recoil again at runtime.
