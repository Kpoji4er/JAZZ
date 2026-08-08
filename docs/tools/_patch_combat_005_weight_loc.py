# docs/tools/_patch_combat_005_weight_loc.py
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESC_RU = (
	"Каждый стак: −1 ОД свободного перемещения. "
	"Тяжёлый комплект может снизить стартовые ОД (до −2). "
	"При 6+ стаках: +1 боль при первом перемещении за ход."
)
DESC_EN = (
	"Each stack: -1 Free Move AP. "
	"A heavy kit may also cut start-of-turn AP (up to -2). "
	"At 6+ stacks: +1 Pain on the first move this turn."
)
IDS = {
	"197266793683",
	"538937825340",
	"549247357132",
	"806830590860",
	"997296420646",
}
OLD_SRC = "ОД и ОД свободного перемещения уменьшены. Чем больше уровень, тем больше дебафов"
OLD_EN = "Reduces AP and Free Move AP. Higher levels impose stronger penalties."
OLD_RU_TR = "Снижает ОД и ОД свободного перемещения. Чем выше уровень, тем сильнее штрафы."


def patch(path: Path, mode: str) -> None:
	lines = path.read_text(encoding="utf-8").splitlines(True)
	out = []
	n = 0
	for line in lines:
		if any(line.startswith(i + ",") for i in IDS):
			new = line.replace(OLD_SRC, DESC_RU)
			if mode == "en":
				new = new.replace(OLD_EN, DESC_EN)
			else:
				new = new.replace(OLD_RU_TR, DESC_RU)
			if new != line:
				n += 1
			out.append(new)
		else:
			out.append(line)
	path.write_text("".join(out), encoding="utf-8")
	print(path.name, n)


def main() -> None:
	patch(ROOT / "English.csv", "en")
	patch(ROOT / "Russian.csv", "ru")


if __name__ == "__main__":
	main()
