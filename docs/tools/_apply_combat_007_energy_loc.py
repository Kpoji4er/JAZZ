# docs/tools/_apply_combat_007_energy_loc.py
"""Upsert RU/EN localization rows for JAZZ-COMBAT-007 energy ladder."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ROWS = [
	(890000000013100, "Fit", "В форме"),
	(
		890000000013101,
		"Maximum AP <em>+<ap_gain></em>. Free Move <em>x<fm_mul>%</em>. First <em><opening_fm_turns></em> combat turn(s): extra <em>+<opening_fm_bonus></em> Free Move.",
		"Макс. ОД <em>+<ap_gain></em>. Свободное перемещение <em>x<fm_mul>%</em>. Первые <em><opening_fm_turns></em> ход(а) боя: дополнительно <em>+<opening_fm_bonus></em> к свободному перемещению.",
	),
	(890000000013102, "Winded", "Запыхался"),
	(
		890000000013103,
		"Slightly worn from travel. Free Move at baseline (<em><fm_mul>%</em>). No AP penalty. Rest in Sat View to recover.",
		"Слегка утомлён дорогой. Свободное перемещение на базовом уровне (<em><fm_mul>%</em>). Без штрафа ОД. Отдых в режиме спутника восстанавливает энергию.",
	),
	(890000000013104, "Fatigued", "Утомлён"),
	(
		890000000013105,
		"Free Move reduced to <em><fm_mul>%</em>. No AP penalty yet. Rest in Sat View to recover.",
		"Свободное перемещение снижено до <em><fm_mul>%</em>. Штрафа ОД пока нет. Отдых в режиме спутника восстанавливает энергию.",
	),
	(
		890000000013106,
		"Maximum AP <em><ap_loss></em>. Free Move <em><fm_mul>%</em>. Recover by resting in Sat View.",
		"Макс. ОД <em><ap_loss></em>. Свободное перемещение <em><fm_mul>%</em>. Восстанавливается отдыхом в режиме спутника.",
	),
	(
		890000000013107,
		"AP penalty <em><ap_loss></em> at turn start. No Free Move. Cannot travel until rested in Sat View.",
		"Штраф ОД <em><ap_loss></em> в начале хода. Нет свободного перемещения. Нельзя путешествовать, пока не отдохнёт в режиме спутника.",
	),
	(
		890000000013108,
		"Maximum AP <em>+<ap_gain></em>. Free Move <em>x<fm_mul>%</em>. First <em><opening_fm_turns></em> combat turns: extra <em>+<opening_fm_bonus></em> Free Move.",
		"Макс. ОД <em>+<ap_gain></em>. Свободное перемещение <em>x<fm_mul>%</em>. Первые <em><opening_fm_turns></em> хода боя: дополнительно <em>+<opening_fm_bonus></em> к свободному перемещению.",
	),
	(890000000013109, "<name> is getting winded.", "<name> начинает запыхаться."),
	(890000000013110, "<name> is getting fatigued.", "<name> начинает уставать."),
	(890000000013111, "<name> is getting tired.", "<name> сильно устаёт."),
	(890000000013112, "<name> is getting exhausted.", "<name> на грани изнеможения."),
	(890000000013113, "<name> is now Winded.", "<name> теперь запыхался."),
	(890000000013114, "<name> is now Fatigued.", "<name> теперь утомлён."),
	(890000000013115, "<name> is now Tired.", "<name> теперь устал."),
	(890000000013116, "<name> is now Exhausted.", "<name> теперь измотан."),
	(890000000013117, "<name> has recovered energy (<level>).", "<name> восстановил энергию (<level>)."),
	(890000000013118, "<em><DisplayName></em> feels fit", "<em><DisplayName></em> в хорошей форме"),
	(890000000013119, "<em><DisplayName></em> is winded", "<em><DisplayName></em> запыхался"),
	(890000000013120, "<em><DisplayName></em> is fatigued", "<em><DisplayName></em> утомлён"),
]


def upsert(path: Path, *, english_file: bool) -> None:
	with path.open("r", encoding="utf-8", newline="") as f:
		data = list(csv.reader(f))
	by_id = {}
	for i, row in enumerate(data):
		if row and row[0].isdigit():
			by_id[int(row[0])] = i
	for tid, en, ru in ROWS:
		note = "jazz:COMBAT-007-energy"
		if english_file:
			# id, Text(en), Translation(en), blank, note
			row = [str(tid), en, en, "", note]
		else:
			# id, Text(ru), Translation(en), blank, note — match existing RU table habit
			row = [str(tid), ru, en, "", note]
		if tid in by_id:
			data[by_id[tid]] = row
		else:
			data.append(row)
	with path.open("w", encoding="utf-8", newline="") as f:
		csv.writer(f, lineterminator="\n").writerows(data)
	print(f"OK {path.name} (+{len(ROWS)} energy ids)")


def main() -> None:
	upsert(ROOT / "English.csv", english_file=True)
	upsert(ROOT / "Russian.csv", english_file=False)


if __name__ == "__main__":
	main()
