# docs/tools/_apply_combat_005_weight_items.py
# Sync Weight_*Class descriptions + OnCalcMoveModifier in items.lua (JAZZ-COMBAT-005).
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

DESC_RU = (
	"Каждый стак: −1 ОД свободного перемещения. "
	"Тяжёлый комплект может снизить стартовые ОД (до −2). "
	"При 6+ стаках: +1 боль при первом перемещении за ход."
)

DESC_IDS = {
	"Weight_1Class": "538937825340",
	"Weight_2Class": "997296420646",
	"Weight_3Class": "806830590860",
	"Weight_4Class": "197266793683",
	"Weight_5Class": "549247357132",
}

NEW_REACTIONS = """\
			'unit_reactions', {
				PlaceObj('UnitReaction', {
					Event = "OnCalcMoveModifier",
					Handler = function(self, target, value, action)
						JazzArmorWeightPainOnMove(target)
						return value
					end,
				}),
			},"""


def main() -> None:
	text = ITEMS.read_text(encoding="utf-8")
	for name, tid in DESC_IDS.items():
		pat = (
			rf"(T\({tid}, --\[\[ModItemCharacterEffectCompositeDef {name} Description\]\] \")"
			rf"([^\"]*)"
			rf"(\")"
		)
		text, n = re.subn(pat, rf"\g<1>{DESC_RU}\g<3>", text, count=1)
		print(f"{name} description replace: {n}")
		if n != 1:
			raise SystemExit(f"failed description for {name}")

	for name in DESC_IDS:
		marker = f"'Id', \"{name}\","
		idx = text.find(marker)
		if idx < 0:
			raise SystemExit(f"missing {name}")
		# Limit search to this PlaceObj (until next Weight_ or closing of this def ~800 chars)
		chunk_end = idx + 900
		chunk = text[idx:chunk_end]
		old = "\t\t\t'unit_reactions', {},"
		if old not in chunk:
			# already patched?
			if "JazzArmorWeightPainOnMove" in chunk:
				print(f"{name} unit_reactions already patched")
				continue
			raise SystemExit(f"no empty unit_reactions in {name}: {chunk!r}")
		chunk2 = chunk.replace(old, NEW_REACTIONS, 1)
		text = text[:idx] + chunk2 + text[chunk_end:]
		print(f"{name} unit_reactions OK")

	ITEMS.write_text(text, encoding="utf-8")
	print("OK", ITEMS)


if __name__ == "__main__":
	main()
