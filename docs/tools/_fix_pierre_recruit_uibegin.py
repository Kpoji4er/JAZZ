# -*- coding: utf-8 -*-
"""UNITS-006 Pierre GloryHog: fix Jazz_PierreRecruit UIBegin (Unit choices) + loc for combat log / Charge tooltip."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"

ROWS = {
    "890000000009942": (
        "<merc> перевербовал(а) <target> в союзники.",
        "<merc> recruited <target> as an ally.",
        "jazz:Code/CombatActions.lua:Jazz_PierreRecruit",
    ),
    "890000000009943": (
        "Спецатака мачете <em>Charge</em> без прямой линии пути; даёт <em><grit></em> <GameTerm('Grit')>.",
        "Machete <em>Charge</em> without a straight-line path; grants <em><grit></em> <GameTerm('Grit')>.",
        "jazz:Code/CombatActions.lua:GloryHog",
    ),
}

OLD_UIBEGIN = """\t\t\t\t\tUIBegin = function (self, units, args)
\t\t\t\t\t\tlocal mode_dlg = GetInGameInterfaceModeDlg()
\t\t\t\t\t\tlocal targets = self:GetTargets(units)
\t\t\t\t\t\tif IsKindOf(mode_dlg, "IModeCommonUnitControl") and targets and targets[1] then
\t\t\t\t\t\t\tlocal list = {}
\t\t\t\t\t\t\tfor _, t in ipairs(targets) do
\t\t\t\t\t\t\t\tlist[#list + 1] = {
\t\t\t\t\t\t\t\t\tDisplayName = t.GetLogName and t:GetLogName() or (t.Name or Untranslated("?")),
\t\t\t\t\t\t\t\t\ttarget = t,
\t\t\t\t\t\t\t\t\tuiCtx = t,
\t\t\t\t\t\t\t\t}
\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tmode_dlg:ShowCombatActionTargetChoice(self, units, list, function(u, entry)
\t\t\t\t\t\t\t\tself:Execute({ u }, { target = entry.target })
\t\t\t\t\t\t\tend)
\t\t\t\t\t\t\treturn
\t\t\t\t\t\tend
\t\t\t\t\t\tCombatActionAttackStart(self, units, args, "IModeCombatAttack")
\t\t\t\t\tend,"""

NEW_UIBEGIN = """\t\t\t\t\tUIBegin = function (self, units, args)
\t\t\t\t\t\t-- ShowCombatActionTargetChoice expects Unit[] and default Execute(unit, {target=unit}).
\t\t\t\t\t\tlocal mode_dlg = GetInGameInterfaceModeDlg()
\t\t\t\t\t\tif IsKindOf(mode_dlg, "IModeCommonUnitControl") then
\t\t\t\t\t\t\tlocal targets = self:GetTargets(units)
\t\t\t\t\t\t\tif targets and targets[1] then
\t\t\t\t\t\t\t\tmode_dlg:ShowCombatActionTargetChoice(self, units, targets)
\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\tend
\t\t\t\t\t\tend
\t\t\t\t\t\tif args and args.target then
\t\t\t\t\t\t\tself:Execute(units, args)
\t\t\t\t\t\tend
\t\t\t\t\tend,"""


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def patch_csv(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    found: set[str] = set()
    out: list[str] = []
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in ROWS:
            ru, en, src = ROWS[rid]
            nl = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "\n")
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}{nl}")
            found.add(rid)
        else:
            out.append(line)
    missing = [rid for rid in ROWS if rid not in found]
    if missing:
        if out and not out[-1].endswith("\n"):
            out[-1] += "\n"
        for rid in missing:
            ru, en, src = ROWS[rid]
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}\n")
    path.write_text("".join(out), encoding="utf-8-sig")
    print(f"{path.name}: upsert {sorted(ROWS)}; appended={missing}")


def patch_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    if "id = \"Jazz_PierreRecruit\"" not in text:
        raise SystemExit("Jazz_PierreRecruit missing from items.lua")
    if NEW_UIBEGIN.strip() in text.replace("\r\n", "\n"):
        print("items.lua UIBegin already fixed")
        return
    if OLD_UIBEGIN not in text:
        # try flexible match around Jazz_PierreRecruit only
        m = re.search(
            r"(PlaceObj\('ModItemCombatAction', \{.*?id = \"Jazz_PierreRecruit\",.*?\},)",
            text,
            re.S,
        )
        if not m:
            raise SystemExit("Jazz_PierreRecruit block not found")
        block = m.group(1)
        if "ShowCombatActionTargetChoice(self, units, list, function" not in block:
            print("UIBegin pattern not in block; leave items")
            return
        raise SystemExit("OLD_UIBEGIN exact text not found (whitespace drift)")
    text = text.replace(OLD_UIBEGIN, NEW_UIBEGIN, 1)
    ITEMS.write_text(text, encoding="utf-8")
    print("items.lua: Jazz_PierreRecruit UIBegin fixed")


def bump_meta() -> None:
    meta = META.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", meta)
    if not m:
        raise SystemExit("version missing")
    ver = int(m.group(1)) + 1
    meta = meta[: m.start(1)] + str(ver) + meta[m.end(1) :]
    bullet = (
        "- UNITS-006: Pierre Jazz_PierreRecruit — fix target-choice UIBegin "
        "(Unit args; Charge tooltip separate) [no new game]\\n"
    )
    marker = "'last_changes', \""
    i = meta.find(marker) + len(marker)
    if "Pierre Jazz_PierreRecruit — fix target-choice" not in meta[i : i + 220]:
        meta = meta[:i] + bullet + meta[i:]
    chunk = meta[i : meta.find('",', i)]
    if "\n" in chunk or "\r" in chunk:
        raise SystemExit("raw newline in last_changes")
    META.write_text(meta, encoding="utf-8", newline="\n")
    print(f"metadata version={ver}")


def main() -> None:
    patch_items()
    bump_meta()
    patch_csv(ROOT / "English.csv")
    patch_csv(ROOT / "Russian.csv")
    print("OK Pierre recruit UIBegin hotfix")


if __name__ == "__main__":
    main()
