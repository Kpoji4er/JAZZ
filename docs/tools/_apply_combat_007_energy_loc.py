# docs/tools/_apply_combat_007_energy_loc.py
"""Upsert RU/EN localization rows for JAZZ-COMBAT-007 energy ladder.

Runtime CSV contract (same as audit-localization.ps1 export):
  Text        = T() source (English for these IDs)
  Translation = language column (RU in Russian.csv, EN in English.csv)

Do not put Russian in Text and English in Translation: JA3 displays Translation.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ROWS = [
	(890000000013100, "Fit", "В форме", "jazz:COMBAT-007-energy"),
	(
		890000000013101,
		"Maximum AP <em>+<ap_gain></em>. Free Move <em>x<fm_mul>%</em>. First <em><opening_fm_turns></em> combat turn(s): extra <em>+<opening_fm_bonus></em> Free Move.",
		"Макс. ОД <em>+<ap_gain></em>. Свободное перемещение <em>x<fm_mul>%</em>. Первые <em><opening_fm_turns></em> ход(а) боя: дополнительно <em>+<opening_fm_bonus></em> к свободному перемещению.",
		"jazz:COMBAT-007-energy",
	),
	(890000000013102, "Winded", "Запыхался", "jazz:COMBAT-007-energy"),
	(
		890000000013103,
		"Slightly worn from travel. Free Move at baseline (<em><fm_mul>%</em>). No AP penalty. Rest in Sat View to recover.",
		"Слегка утомлён дорогой. Свободное перемещение на базовом уровне (<em><fm_mul>%</em>). Без штрафа ОД. Отдых в режиме спутника восстанавливает энергию.",
		"jazz:COMBAT-007-energy",
	),
	(890000000013104, "Fatigued", "Утомлён", "jazz:COMBAT-007-energy"),
	(
		890000000013105,
		"Free Move reduced to <em><fm_mul>%</em>. No AP penalty yet. Rest in Sat View to recover.",
		"Свободное перемещение снижено до <em><fm_mul>%</em>. Штрафа ОД пока нет. Отдых в режиме спутника восстанавливает энергию.",
		"jazz:COMBAT-007-energy",
	),
	(
		890000000013106,
		"Maximum AP <em><ap_loss></em>. Free Move <em><fm_mul>%</em>. Recover by resting in Sat View.",
		"Макс. ОД <em><ap_loss></em>. Свободное перемещение <em><fm_mul>%</em>. Восстанавливается отдыхом в режиме спутника.",
		"jazz:COMBAT-007-energy",
	),
	(
		890000000013107,
		"AP penalty <em><ap_loss></em> at turn start. No Free Move. Cannot travel until rested in Sat View.",
		"Штраф ОД <em><ap_loss></em> в начале хода. Нет свободного перемещения. Нельзя путешествовать, пока не отдохнёт в режиме спутника.",
		"jazz:COMBAT-007-energy",
	),
	(
		890000000013108,
		"Maximum AP <em>+<ap_gain></em>. Free Move <em>x<fm_mul>%</em>. First <em><opening_fm_turns></em> combat turns: extra <em>+<opening_fm_bonus></em> Free Move.",
		"Макс. ОД <em>+<ap_gain></em>. Свободное перемещение <em>x<fm_mul>%</em>. Первые <em><opening_fm_turns></em> хода боя: дополнительно <em>+<opening_fm_bonus></em> к свободному перемещению.",
		"jazz:COMBAT-007-energy",
	),
	(890000000013109, "<name> is getting winded.", "<name> начинает запыхаться.", "jazz:COMBAT-007-energy"),
	(890000000013110, "<name> is getting fatigued.", "<name> начинает уставать.", "jazz:COMBAT-007-energy"),
	(890000000013111, "<name> is getting tired.", "<name> сильно устаёт.", "jazz:COMBAT-007-energy"),
	(890000000013112, "<name> is getting exhausted.", "<name> на грани изнеможения.", "jazz:COMBAT-007-energy"),
	(890000000013113, "<name> is now Winded.", "<name> теперь запыхался.", "jazz:COMBAT-007-energy"),
	(890000000013114, "<name> is now Fatigued.", "<name> теперь утомлён.", "jazz:COMBAT-007-energy"),
	(890000000013115, "<name> is now Tired.", "<name> теперь устал.", "jazz:COMBAT-007-energy"),
	(890000000013116, "<name> is now Exhausted.", "<name> теперь измотан.", "jazz:COMBAT-007-energy"),
	(890000000013117, "<name> has recovered energy (<level>).", "<name> восстановил энергию (<level>).", "jazz:COMBAT-007-energy"),
	(890000000013118, "<em><DisplayName></em> feels fit", "<em><DisplayName></em> в хорошей форме", "jazz:COMBAT-007-energy"),
	(890000000013119, "<em><DisplayName></em> is winded", "<em><DisplayName></em> запыхался", "jazz:COMBAT-007-energy"),
	(890000000013120, "<em><DisplayName></em> is fatigued", "<em><DisplayName></em> утомлён", "jazz:COMBAT-007-energy"),
	(
		890000000013121,
		"<em>(Injured legs)</em>",
		"<em>(Раненые ноги)</em>",
		"jazz:COMBAT-008-trauma-travel",
	),
	(
		890000000013122,
		"Move without spending AP. Remaining: <em><apn(remain)> AP</em>. Removed after attacking or after using up the allowance (based on Agility).",
		"Перемещение без траты ОД. Осталось: <em><apn(remain)> ОД</em>. Снимается после атаки или когда запас исчерпан (зависит от Ловкости).",
		"jazz:COMBAT-007-freemove-ui",
	),
	(
		890000000013123,
		" <em>(<apn(fm)> FM)</em>",
		" <em>(<apn(fm)> FM)</em>",
		"jazz:COMBAT-007-freemove-ui",
	),
]


def format_csv_row(fields: list[str]) -> str:
	buf = io.StringIO()
	csv.writer(buf, lineterminator="\n").writerow(fields)
	return buf.getvalue()


def upsert(path: Path, *, english_file: bool) -> tuple[int, int]:
	wanted: dict[str, str] = {}
	for tid, en, ru, note in ROWS:
		text = en
		translation = en if english_file else ru
		wanted[str(tid)] = format_csv_row([str(tid), text, translation, "", note])

	lines = path.read_text(encoding="utf-8").splitlines(True)
	seen: set[str] = set()
	out: list[str] = []
	updated = 0
	for line in lines:
		hit = None
		for tid in wanted:
			if line.startswith(tid + ","):
				hit = tid
				break
		if hit:
			if line != wanted[hit]:
				updated += 1
			out.append(wanted[hit])
			seen.add(hit)
		else:
			out.append(line)
	appended = 0
	for tid, row in wanted.items():
		if tid not in seen:
			if out and not out[-1].endswith("\n"):
				out[-1] += "\n"
			out.append(row)
			appended += 1
	path.write_text("".join(out), encoding="utf-8")
	print(f"OK {path.name}: updated={updated} appended={appended}")
	return updated, appended


def main() -> None:
	upsert(ROOT / "English.csv", english_file=True)
	upsert(ROOT / "Russian.csv", english_file=False)


if __name__ == "__main__":
	main()
