"""JAZZ-COMBAT-009-AC-001: Overwatch cone angle anchors (static replica of Lua helper)."""

from __future__ import annotations


def muldivround(a: int, b: int, d: int) -> int:
    if d == 0:
        return 0
    return (a * b + d // 2) // d


def divround(a: int, b: int) -> int:
    return (a + b // 2) // b


def clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def class_strip(kind: str) -> int:
    if kind in ("SniperRifle", "AssaultRifle", "BattleRifle", "MachineGun", "LightMachineGun"):
        return 120
    if kind in ("SubmachineGun", "Shotgun"):
        return 480
    if kind in ("Pistol", "Revolver"):
        return 1200
    return 240


def cone_angle(
    authored: int,
    bdr: int,
    weapon_range: int,
    close_range: int,
    kind: str,
    dist_tiles: int,
) -> int:
    authored = max(authored, 1)
    bdr = max(bdr, 2)
    weapon_range = max(weapon_range, bdr)
    d_min = max(2, divround(bdr, 2))
    d = clamp(dist_tiles, d_min, weapon_range)
    if d <= bdr:
        angle = muldivround(authored, bdr, d)
        if kind in ("MachineGun", "LightMachineGun"):
            angle = muldivround(angle, bdr, d)
    else:
        strip = class_strip(kind)
        angle = authored + muldivround(strip - authored, d - bdr, max(weapon_range - bdr, 1))
    if d < bdr and kind == "Shotgun":
        angle = max(angle, muldivround(100 * 60, d_min, d))
    return clamp(angle, 120, 155 * 60)


def min_range(bdr: int, m2: bool = False, weapon_range: int = 0) -> int:
    del m2, weapon_range
    return max(2, divround(max(bdr, 2), 2))


def main() -> int:
    errors: list[str] = []

    def expect(name: str, got: int, want: int) -> None:
        if got != want:
            errors.append(f"{name}: got {got}, want {want}")

    expect(
        "Glock d_min=4",
        cone_angle(5400, 8, 19, 0, "Pistol", 4),
        9300,
    )
    expect(
        "Glock BDR=8",
        cone_angle(5400, 8, 19, 0, "Pistol", 8),
        5400,
    )
    expect(
        "Glock R=19",
        cone_angle(5400, 8, 19, 0, "Pistol", 19),
        1200,
    )
    expect("Glock MinRange", min_range(8), 4)
    expect(
        "Makarov d_min=3",
        cone_angle(5400, 6, 15, 0, "Pistol", 3),
        9300,
    )
    expect(
        "Colt1911 d_min=2",
        cone_angle(5400, 4, 14, 0, "Pistol", 2),
        9300,
    )
    expect(
        "CZ75 d_min=4 inverse cap",
        cone_angle(5400, 7, 20, 0, "Pistol", 4),
        9300,
    )
    expect(
        "CZ75 d=5 narrower than d_min",
        cone_angle(5400, 7, 20, 0, "Pistol", 5),
        7560,
    )
    expect(
        "MP5A4 d_min=5",
        cone_angle(4320, 10, 30, 3, "SubmachineGun", 5),
        8640,
    )
    expect(
        "AK-74 d_min=8 extra 0",
        cone_angle(1320, 16, 48, 8, "AssaultRifle", 8),
        2640,
    )
    expect(
        "AK shorter BDR narrower at same d",
        1 if cone_angle(1320, 11, 48, 5, "AssaultRifle", 8)
        < cone_angle(1320, 16, 48, 8, "AssaultRifle", 8)
        else 0,
        1,
    )
    m1897 = cone_angle(2160, 7, 21, 5, "Shotgun", 4)
    if m1897 < 6000:
        errors.append(f"M1897 d_min: got {m1897}, want >= 6000")
    expect(
        "Mosin R=66 strip",
        cone_angle(420, 16, 66, 16, "SniperRifle", 66),
        120,
    )
    expect(
        "PKM R=60 strip",
        cone_angle(600, 18, 60, 8, "MachineGun", 60),
        120,
    )
    expect(
        "PKM d_min square",
        cone_angle(600, 18, 60, 8, "MachineGun", 9),
        2400,
    )
    expect(
        "PKM BDR authored",
        cone_angle(600, 18, 60, 8, "MachineGun", 18),
        600,
    )
    expect("AK MinRange 50% BDR", min_range(16), 8)
    expect("M2 min 50% BDR", min_range(28, True, 80), 14)

    if errors:
        print("COMBAT-009 cone FAIL")
        for err in errors:
            print(" -", err)
        return 1
    print("COMBAT-009 cone PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
