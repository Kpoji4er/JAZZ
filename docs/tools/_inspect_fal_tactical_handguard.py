# -*- coding: utf-8 -*-
"""Compare tactical RIS handguard donor vs vanilla FAL handguard bboxes."""
from __future__ import annotations

from pathlib import Path

import numpy as np

VANILLA = Path(r"E:\JaWeapons\Weapons\_vanilla_reference\OBJ\WeaponAttA_HandguardFNFal_01_mesh.obj")
DONOR = Path(r"E:\JaWeapons\Weapons\_fal_jazz_build\source\tactical\model_2.obj")


def load_obj(path: Path) -> np.ndarray:
    verts = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("v "):
            parts = line.split()
            verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
    return np.asarray(verts, dtype=np.float64)


def report(name: str, v: np.ndarray) -> None:
    mn = v.min(axis=0)
    mx = v.max(axis=0)
    span = mx - mn
    print(f"{name}: n={len(v)}")
    print(f"  min {mn}")
    print(f"  max {mx}")
    print(f"  span {span}  (axis order xyz)")
    print(f"  aspect x/y={span[0]/span[1]:.3f} x/z={span[0]/span[2]:.3f} y/z={span[1]/span[2]:.3f}")


def end_slice(v: np.ndarray, axis: int, which: str, depth: float) -> np.ndarray:
    lo, hi = v[:, axis].min(), v[:, axis].max()
    if which == "min":
        return v[v[:, axis] <= lo + depth]
    return v[v[:, axis] >= hi - depth]


def main() -> None:
    van = load_obj(VANILLA)
    don = load_obj(DONOR)
    report("vanilla HandguardFNFal_01 (m)", van)
    report("donor model_2 raw", don)
    don_m = don * 0.01
    report("donor model_2 *0.01 (m)", don_m)

    print("\nvanilla end slices 1.5cm:")
    for which in ("min", "max"):
        for axis, name in enumerate("xyz"):
            sl = end_slice(van, axis, which, 0.015)
            c = sl.mean(axis=0)
            print(f"  {name} {which}: n={len(sl)} centroid={c}")

    print("\ndonor*0.01 end slices 1.5cm:")
    for which in ("min", "max"):
        for axis, name in enumerate("xyz"):
            sl = end_slice(don_m, axis, which, 0.015)
            c = sl.mean(axis=0)
            print(f"  {name} {which}: n={len(sl)} centroid={c}")

    # After the export remaps, vanilla/donor long axis is Y and the
    # receiver collar is max-Y. Muzzle seating left ~2cm in the receiver.
    van_len = float(van.max(axis=0)[1] - van.min(axis=0)[1])
    don_len = float(don_m.max(axis=0)[2] - don_m.min(axis=0)[2])
    print(f"\nseat hint: vanilla_len_y={van_len:.4f} donor_len_z={don_len:.4f} extra={(don_len-van_len):.4f}")
    print("export seats TacHandguard on max-Y (receiver), not min-Y (muzzle)")


if __name__ == "__main__":
    main()
