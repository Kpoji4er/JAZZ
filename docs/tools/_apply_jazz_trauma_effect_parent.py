# One-shot: Trauma* -> JazzTraumaEffect parent (companions + items.lua).
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IDS = [
	"TraumaArmsLight",
	"TraumaArmsMedium",
	"TraumaArmsHeavy",
	"TraumaLegsLight",
	"TraumaLegsMedium",
	"TraumaLegsHeavy",
	"TraumaRibsLight",
	"TraumaRibsMedium",
	"TraumaRibsHeavy",
	"TraumaHeadLight",
	"TraumaHeadMedium",
	"TraumaHeadHeavy",
	"TraumaBurnLight",
	"TraumaBurnMedium",
	"TraumaBurnHeavy",
]


def patch_companions() -> None:
	for effect_id in IDS:
		path = ROOT / "CharacterEffect" / f"{effect_id}.lua"
		text = path.read_text(encoding="utf-8")
		updated = text.replace(
			'__parents = { "StatusEffect" }',
			'__parents = { "JazzTraumaEffect" }',
		)
		updated = updated.replace(
			'object_class = "StatusEffect",',
			'object_class = "JazzTraumaEffect",',
		)
		if updated == text:
			raise SystemExit(f"no change in {path}")
		path.write_text(updated, encoding="utf-8", newline="\n")
		print("companion", path.name)


def patch_items() -> None:
	path = ROOT / "items.lua"
	text = path.read_text(encoding="utf-8")
	pattern = re.compile(
		r"(PlaceObj\('ModItemCharacterEffectCompositeDef', \{\s*"
		r"'Id', \"(Trauma(?:Arms|Legs|Ribs|Head|Burn)(?:Light|Medium|Heavy))\",\s*"
		r"(?:(?!PlaceObj\('ModItemCharacterEffectCompositeDef').)*?"
		r"'object_class', \")StatusEffect(\")",
		re.S,
	)

	def repl(match: re.Match[str]) -> str:
		return match.group(1) + "JazzTraumaEffect" + match.group(3)

	updated, count = pattern.subn(repl, text)
	print("items replacements", count)
	if count != 15:
		raise SystemExit(f"expected 15 trauma object_class replacements, got {count}")
	path.write_text(updated, encoding="utf-8", newline="\n")


def main() -> None:
	patch_companions()
	patch_items()
	print("OK")


if __name__ == "__main__":
	main()
