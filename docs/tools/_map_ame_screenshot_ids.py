"""Map OCR text to AppearancePreset via 'x <Id> idle' only."""
from __future__ import annotations

import json
import re
from pathlib import Path

DST = Path(__file__).resolve().parents[2] / ".tmp" / "ame-crops"
CATALOG = Path(__file__).resolve().parents[1] / "design" / "mercs-ja12" / "_appearance-donor-visual-catalog.md"

REAL = (
    "Pierre,Pierre_Steroid,Poacher_01,Poacher_02,President,Prisoner_01,Prisoner_02,Prisoner_03,"
    "Prisoner_04,Prisoner_05,Prisoner_06,Prisoner_07,Prisoner_08,Quinten,Raider,Raider_01,"
    "Raider_DustStorm,Raven,Raven_DustStorm,Reaper,Reaper_DustStorm,Reaper_Jungle,Reaper_Snake,"
    "RebelFemaleSniper,RebelFemaleSniper_1,Rebels_NPC_Ghost,Recon_Rebels,Recon_Rebels_02,"
    "Recon_Rebels_03,Red,Red_DustStorm,Referee,Reporter,Ricochet,Rothman,Sample_Horatio,Scope,"
    "Scope_DustStorm,Scully,Scully_Forest,Scully_Savana,Sebastocrator,Shadow,Shadow_Savanna,Shaman,"
    "Shank,Sidney,Sidney_DustStorm,Skeleton,Skeleton_Burnt,Smiley,Soldier_Local_01,Soldier_Rebels,"
    "Soldier_Rebels_02,Soldier_Rebels_03,Soldier_Rebels_04,Spider,Steroid,Steroid_DustStorm,"
    "Stormer_Rebels,Stormer_Rebels_02,Stormer_Rebels_03,Tedd,TestSoldier_01,TestSoldier_2,TestSuit,"
    "TestSuit_01,Tex,TheBeast,TheBeast_Civilian,TheHogLady,TheMajor,Thor,ThugAssault,ThugElite,"
    "ThugMelee,ThugWeaponMaster,Thug_Artillery,Thug_Artillery_1,Thug_Artillery_2,Thug_Demolishion,"
    "Thug_Demolishion_1,Thug_Demolishion_2,Thug_Heavy,Thug_Heavy_1,Thug_Heavy_2,Thug_Marksman,"
    "Thug_Marksman_1,Thug_Marksman_2,Thug_Medic,Thug_Medic_1,Thug_Medic_2,Thug_Officer,"
    "Thug_Officer_1,Thug_Recon,Thug_Recon_1,Thug_Recon_2,Thug_Soldier,Thug_Soldier_1,Thug_Soldier_2,"
    "Thug_Stormer,Thug_Stormer_1,Thug_Stormer_2,TimTurtledove,TourGuide,Travis,UncleBaggz,Vicious,"
    "Vicki,Vilde,VillagerFemale_01,VillagerFemale_02,VillagerFemale_03,VillagerFemale_04,"
    "VillagerFemale_05,VillagerFemale_06,VillagerFemale_07,VillagerFemale_08,VillagerFemale_09,"
    "VillagerFemale_10,VillagerFemale_11,VillagerFemale_12,VillagerFemale_13,VillagerFemale_14,"
    "VillagerFemale_15,VillagerFemale_16,VillagerFemale_17,VillagerFemale_18,VillagerFemale_19,"
    "VillagerFemale_20,VillagerMale_01,VillagerMale_02,VillagerMale_03,VillagerMale_04,"
    "VillagerMale_05,VillagerMale_06,VillagerMale_07,VillagerMale_08,VillagerMale_09,"
    "VillagerMale_10,VillagerMale_11,VillagerMale_12,VillagerMale_13,VillagerMale_14,"
    "VillagerMale_15,VillagerMale_16,VillagerMale_17,VillagerMale_18,VillagerMale_19,"
    "VillagerMale_20,VillagerMale_Drowned,Vince,Wanda,Weirdo,Wlad,Wolf,Wolf_DustStorm,"
    "WorkingGirl01,WorkingGirl02,WorkingGirl03,WorkingGirl04,WorkingGuy01,WorkingGuy02,"
    "WorkingGuy03,WorkingGuy04,Xavier,civ_Antoine,civ_Claudette,civ_Karen,civ_Pepe,test_Militia"
).split(",")
# Intentionally omit UI-colliding id `Static`
REAL_SET = set(REAL)


def catalog_headers(text: str) -> set[str]:
    headers: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("## "):
            continue
        head = line[3:].split(" ·")[0].strip()
        for part in re.split(r"[/,]", head):
            part = re.sub(r"\s*\(.*$", "", part.strip()).strip()
            if part and part[0].isalnum():
                headers.add(part)
    return headers


def extract_id(ocr: str) -> str | None:
    if not ocr:
        return None
    t = ocr.replace("\n", " ")
    for m in re.finditer(r"\bx\s+([A-Za-z][A-Za-z0-9_]{1,60})\s+idle\b", t, re.I):
        cand = m.group(1)
        if cand in REAL_SET:
            return cand
        if f"civ_{cand}" in REAL_SET:
            return f"civ_{cand}"
        # OCR truncations: tTheBeast, IRaider_01, VillagerFemale_041
        for real in REAL:
            if real.endswith(cand) or cand.endswith(real) or real.replace("_", "") == cand.replace("_", ""):
                if abs(len(real) - len(cand)) <= 3:
                    return real
        # prefix match unique
        hits = [r for r in REAL if r.startswith(cand) or cand.startswith(r)]
        if len(hits) == 1:
            return hits[0]
    # fallback: any REAL token in OCR (word boundary), excluding short names
    for real in sorted(REAL, key=len, reverse=True):
        if len(real) < 4:
            continue
        if re.search(rf"\b{re.escape(real)}\b", t):
            return real
    return None


def main() -> None:
    data = json.loads((DST / "ids.json").read_text(encoding="utf-8"))
    headers = catalog_headers(CATALOG.read_text(encoding="utf-8"))
    rows = []
    for r in data["rows"]:
        mid = extract_id(r.get("ocr") or "")
        rows.append({"i": r["i"], "mapped": mid, "ocr": r.get("ocr"), "raw": r.get("id")})

    uniq = []
    seen = set()
    for r in rows:
        if r["mapped"] and r["mapped"] not in seen:
            seen.add(r["mapped"])
            uniq.append(r["mapped"])

    missing = [x for x in uniq if x not in headers]
    unmapped = [r["i"] for r in rows if not r["mapped"]]
    out = {"uniq": uniq, "missing": missing, "unmapped_idx": unmapped, "rows": rows}
    (DST / "mapped_ids.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"uniq={len(uniq)} missing={len(missing)} unmapped={len(unmapped)}")
    print("UNIQ=" + ",".join(uniq))
    print("UNMAPPED=" + ",".join(str(i) for i in unmapped[:80]))
    if len(unmapped) > 80:
        print(f"... +{len(unmapped)-80} more")


if __name__ == "__main__":
    main()
