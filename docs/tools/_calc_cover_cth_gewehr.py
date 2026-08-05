#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static Gewehr 98 cover CTH check (JAZZ multiplicative pipeline).

Mirrors AccuracyRangeCTH.lua helpers + RangeAttackTargetStanceCover params
from items.lua (falls back to owner recalibration defaults if parse fails).
Run from jazz/: python docs/tools/_calc_cover_cth_gewehr.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def isqrt(n: int) -> int:
	n = max(0, n)
	lo, hi = 0, n
	while lo < hi:
		mid = (lo + hi + 1) // 2
		if mid <= 0:
			lo = mid
		elif mid > n // mid:
			hi = mid - 1
		elif mid * mid <= n:
			lo = mid
		else:
			hi = mid - 1
	return lo


def div_round(a: int, b: int) -> int:
	return (a + b // 2) // b if b > 0 else 0


def skill_curve(value: float) -> int:
	value = max(0, int(round(value)))
	if value == 0:
		return 20
	root2 = isqrt(value * 100_000_000)
	root4 = isqrt(root2)
	return 20 + div_round(value * root4, 400)


def aim_mastery(m: int) -> int:
	m = max(0, min(100, m))
	mastery = (
		div_round(min(m, 60) * 20, 60)
		+ div_round(max(0, min(m - 60, 20)) * 20, 20)
		+ div_round(max(0, min(m - 80, 10)) * 20, 10)
		+ div_round(max(0, min(m - 90, 6)) * 20, 6)
		+ div_round(max(0, min(m - 96, 4)) * 20, 4)
	)
	return min(100, mastery)


def pct_to_factor(v: int) -> float:
	# JAZZ_CTHPercentToFactor: 1000 + round(v * 10), then / 1000
	return (1000 + round(v * 10)) / 1000.0


def load_cover_params() -> tuple[int, int, int, int]:
	"""Read Cover/Exposed/Crouch/Prone from items.lua RangeAttackTargetStanceCover."""
	defaults = (-45, -12, -12, -23)
	items = ROOT / "items.lua"
	if not items.is_file():
		return defaults
	text = items.read_text(encoding="utf-8", errors="replace")
	i = text.find('id = "RangeAttackTargetStanceCover"')
	if i < 0:
		return defaults
	chunk = text[max(0, i - 900) : i + 80]
	got = dict(re.findall(r"'Name', \"(\w+)\"[^']*'Value', (-?\d+)", chunk))
	try:
		return (
			int(got["Cover"]),
			int(got["ExposedCover"]),
			int(got["CrouchPenalty"]),
			int(got["PronePenalty"]),
		)
	except (KeyError, ValueError):
		return defaults


COVER, EXPOSED, CROUCH, PRONE = load_cover_params()


def scenario(
	label: str,
	dex: int,
	marks: int,
	lvl: int,
	aim: int,
	max_aim: int,
	dist: int,
	cover_pp: int,
	*,
	aa: int = 12,
	bdr: int = 15,
	wr: int = 62,
	grouping: int = 45,
	close_range: int = 12,
	close_range_factor: int = 70,
) -> None:
	snap_raw = (dex * 4 + marks + lvl * 5) / 6
	prec_raw = (marks * 4 + dex + lvl * 5) / 6
	snap = skill_curve(snap_raw)
	prec = skill_curve(prec_raw)
	aim_prog = aim / max_aim if max_aim else 0.0
	shot_skill = snap + aim_prog * max(prec - snap, 0)
	am = aim_mastery(marks)
	aim_gain = aim * aa * am / 100
	core = min(100.0, shot_skill + aim_gain)

	# Irons: optic reach 0 → E ≈ BDR
	e = float(bdr)
	if dist <= e:
		rf = 1.0
	else:
		p = max(1.25, bdr * 0.05 + grouping / 100)
		t = (dist - e) / (wr - e)
		rf = 0.25 + (1 - 0.25) * (1 - t**p)

	if dist < close_range:
		close = (close_range_factor / 100) + (1 - close_range_factor / 100) * (dist / close_range)
	else:
		close = 1.0

	cover_f = pct_to_factor(cover_pp) if cover_pp else 1.0
	p = core * rf * close * cover_f
	final = max(2, min(100, round(p)))

	miss_graze = min(50, int(50 * ((100 - final) / 100) ** 2))
	if cover_pp and cover_pp < EXPOSED:
		cover_graze = max(0, min(100, round((-cover_pp) * 100 / (-COVER))))
	else:
		cover_graze = 0

	print(f"=== {label} ===")
	print(f"  core={core:.1f} rf={rf:.3f} close={close:.3f} cover_pp={cover_pp} cover_f={cover_f:.3f}")
	print(
		"  final CTH=%s%%  miss->graze~%s%%  cover->graze~%s%%"
		% (final, miss_graze, cover_graze)
	)


def main() -> None:
	print("Cover params (from items.lua): Cover=%s Exposed=%s Crouch=%s Prone=%s" % (COVER, EXPOSED, CROUCH, PRONE))
	print(
		"Factors: full=%.2f exposed=%.2f crouch=%.2f prone=%.2f"
		% (
			pct_to_factor(COVER),
			pct_to_factor(EXPOSED),
			pct_to_factor(CROUCH),
			pct_to_factor(PRONE),
		)
	)
	# Gewehr98 companion: AA12, BDR15, WR62, Grouping45, CloseRange12/70; MaxAimActions default 3
	scenario("mid merc full aim OPEN @12", 70, 80, 4, 3, 3, 12, 0)
	scenario("mid merc full aim FULL COVER @12", 70, 80, 4, 3, 3, 12, COVER)
	scenario("mid merc snap FULL COVER @12", 70, 80, 4, 0, 3, 12, COVER)
	scenario("mid merc full aim crouch (no cover) @12", 70, 80, 4, 3, 3, 12, CROUCH)
	scenario("mid merc full aim prone (no cover) @12", 70, 80, 4, 3, 3, 12, PRONE)
	half = round((EXPOSED + COVER) / 2)
	scenario(f"mid merc full aim HALF COVER (~{half}) @12", 70, 80, 4, 3, 3, 12, half)


if __name__ == "__main__":
	main()
