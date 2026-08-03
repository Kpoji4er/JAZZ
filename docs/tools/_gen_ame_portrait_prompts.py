#!/usr/bin/env python3
"""Generate AME merc portrait prompt bank (JAZZ-UNITS-005).

Loads ROSTER from docs/tools/_gen_ame_roster_60.py via importlib.
Writes jazz-units/MercPortraits/_ame_face_refs/prompts.jsonl — identity cues
for GenerateImage; style refs remain MercPortraits/References/.
Does not generate images.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JAZZ_UNITS = ROOT.parent / "jazz-units"
ROSTER_SCRIPT = Path(__file__).resolve().parent / "_gen_ame_roster_60.py"
OUT_DIR = JAZZ_UNITS / "MercPortraits" / "_ame_face_refs"
OUT_JSONL = OUT_DIR / "prompts.jsonl"
OUT_README = OUT_DIR / "README.md"

# 60 unique hair styles (uniqueness anchor for hair+age+scar triples).
HAIR_MALE = [
    "tight high-top fade with crisp line-up",
    "low buzz cut, even stubble on scalp",
    "short cropped coils, natural texture on top",
    "close-shaved head with faint razor shadow",
    "medium height short afro, picked out lightly",
    "single-row cornrows pulled back tight",
    "six thin cornrows to the crown",
    "short two-strand twists, neat ends",
    "low fade with short locs on top",
    "temple fade with short sponge twists",
    "classic short afro fade, sides skin-tight",
    "short dreadlocks tied back in a small tail",
    "widow's peak with short curly top",
    "flat-top fade, squared at the front",
    "short twists with tapered sides",
    "natural short coils, slightly uneven fringe",
    "high fade with short box braids",
    "crew cut with tight curl pattern visible",
    "short locs free at shoulder length (tucked for kit)",
    "shaved sides with longer coiled crown",
    "short afro with greying temples",
    "three cornrows with zigzag part",
    "short cropped hair with receding hairline",
    "low skin fade with short 360 waves",
    "short freeform locs, medium length",
    "taper fade with short curly fringe forward",
    "short braids in a low bun at nape",
    "bald head, polished scalp sheen",
    "short afro puff, compact and round",
    "side-part short natural hair, combed flat",
    "short twists with faded temples",
    "high and tight military-style fade (civilian, no insignia)",
    "short locs with gold bead at temple (single bead only)",
    "cropped hair with salt-and-pepper stubble on scalp",
    "short box braids ending at jawline",
    "natural short hair with tight curl clumps",
    "fade with short twisted top knot",
    "short hair with pronounced widow's peak",
    "low fade, short hair brushed forward",
    "short afro with flattened top from cap wear",
    "close crop with faint scar-visible scalp patch",
    "short dreads, half tied, half loose",
    "taper with short curls and sharp lineup",
    "short hair, sun-bleached tips on crown",
    "buzz cut with deliberate razor line part",
    "short coiled hair, slightly longer at front",
    "fade with short micro-locs at crown",
    "short natural hair, wind-swept forward",
    "low fade with short twisted rows",
    "short hair, dense tight curls, neat edges",
]

HAIR_FEMALE = [
    "short tapered natural cut, soft coils framing face",
    "tight bun at crown, edges laid with gel",
    "shoulder-length box braids, ends tied back for field work",
    "short pixie fade with curly top",
    "long single braid over one shoulder",
    "short locs to jawline, neat parts",
    "cornrow crown with loose coiled ends",
    "short natural afro, compact and professional",
    "braided updo, low at nape",
    "short twisted bob, asymmetric part",
]

SKIN_TONES = [
    "deep ebony",
    "rich ebony with warm undertone",
    "dark mahogany brown",
    "warm mahogany brown",
    "golden brown",
    "copper brown",
    "chestnut brown",
    "deep umber",
    "warm bronze brown",
    "dark caramel brown",
]

AGES = [
    "early 20s",
    "mid 20s",
    "late 20s",
    "early 30s",
    "mid 30s",
    "late 30s",
    "early 40s",
    "mid 40s",
    "late 40s",
    "early 50s",
]

SCARS = [
    "no visible facial scars",
    "thin faded scar through left eyebrow",
    "small nick scar on chin",
    "short horizontal scar on right cheekbone",
    "split left eyebrow scar, healed clean",
    "tiny keloid dot near right ear",
    "faint burn patch on left neck (visible at collar)",
    "old stitch line at hairline, left temple",
    "small scar at bridge of nose",
    "crescent scar on right jaw",
    "thin scar crossing lower lip (closed, subtle)",
    "faded shrapnel fleck scar on forehead",
    "short vertical scar on left cheek",
    "knuckle-scrape scar on brow ridge, right side",
    "small scar below left eye, cheek",
    "old cut line on right temple under hair",
    "faint acne-pitted texture on cheeks (light, natural)",
    "small scar at corner of mouth, left",
    "thin scar on Adam's apple area",
    "weathered crease scar on right brow (not deep)",
    "tiny notch on earlobe, left",
    "faded tribal-cut childhood scar on scalp edge (partially hidden)",
    "short scar on nose side, left nostril",
    "old burn line on back of neck (glimpse at collar)",
    "small scar on upper lip, philtrum",
    "thin scar parallel to jaw, left",
    "faint scar on chin center",
    "small scar on forehead center, hair-covered mostly",
    "healed cut on right cheek, horizontal",
    "tiny scar on left eyelid crease",
    "short scar on collarbone (visible at neckline)",
    "faint scar on right eyebrow tail",
    "small scar on left jaw hinge",
    "thin line scar on right cheek near ear",
    "old stitch scar on scalp, visible at part",
    "small scar on bridge of nose, off-center",
    "faint scar on lower right cheek",
    "tiny scar on upper left forehead",
    "short scar on left nostril edge",
    "healed scar on chin, off to right",
    "thin scar on left temple",
    "small scar on right brow center",
    "faint scar on left cheekbone",
    "tiny scar on right jawline",
    "short scar on left ear cartilage (old piercing tear)",
    "faint scar on forehead, right side",
    "small scar on right cheek, vertical",
    "thin scar on left cheek near nose",
    "healed cut scar on right temple",
    "tiny scar on chin left side",
    "faint scar on left brow, outer third",
    "small scar on right upper cheek",
    "thin scar on jaw, right side",
    "healed scar on left cheek, crescent",
    "tiny scar on forehead left",
    "short scar on right chin",
    "faint scar on left jaw",
    "small scar on right brow outer edge",
    "thin scar on left cheek lower",
]

FACIAL_HAIR_MALE = [
    "clean-shaven jaw",
    "light stubble, even",
    "neat short boxed beard",
    "thin mustache, trimmed",
    "full short beard, maintained",
    "goatee with connected mustache",
    "heavy stubble, uneven from field work",
    "clean-shaven with strong jaw shadow",
    "short chin strap beard",
    "trimmed mustache only",
]

BUILD_MALE = [
    "lean wiry frame",
    "stocky compact build",
    "broad-shouldered athletic build",
    "tall lanky frame",
    "solid muscular build",
    "medium build, work-hardened",
    "slim runner's build",
    "heavyset powerful build",
    "average height, dense muscle",
    "rangy long-limbed build",
]

BUILD_FEMALE = [
    "slim athletic build",
    "thin wiry frame",
    "compact lean build",
    "slender field-medic build",
    "light agile build",
    "thin sharp-featured build",
    "slim toned build",
    "petite lean build",
    "slender instructor's posture",
    "thin sniper-patient build",
]

def load_roster_module():
    spec = importlib.util.spec_from_file_location("gen_ame_roster_60", ROSTER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load roster module: {ROSTER_SCRIPT}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    roster = mod.ROSTER
    if len(roster) != 60:
        raise RuntimeError(f"ROSTER must have 60 entries, got {len(roster)}")
    return mod


def trait_bank(roster: list[dict]) -> list[dict[str, str]]:
    """Build 60 unique face trait records; hair is unique per slot."""
    bank: list[dict[str, str]] = []
    male_hair_i = 0
    female_hair_i = 0
    for slot, merc in enumerate(roster, start=1):
        female = bool(merc.get("female"))
        if female:
            hair = HAIR_FEMALE[female_hair_i % len(HAIR_FEMALE)]
            female_hair_i += 1
            facial_hair = "clean jawline, no facial hair"
            build = BUILD_FEMALE[(slot - 1) % len(BUILD_FEMALE)]
        else:
            hair = HAIR_MALE[male_hair_i % len(HAIR_MALE)]
            male_hair_i += 1
            facial_hair = FACIAL_HAIR_MALE[(slot - 1) % len(FACIAL_HAIR_MALE)]
            build = BUILD_MALE[(slot - 1) % len(BUILD_MALE)]
        age = AGES[(slot - 1) % len(AGES)]
        skin = SKIN_TONES[(slot * 3 - 1) % len(SKIN_TONES)]
        scar = SCARS[(slot - 1) % len(SCARS)]
        bank.append(
            {
                "age": age,
                "skin": skin,
                "hair": hair,
                "facial_hair": facial_hair,
                "scar": scar,
                "build": build,
            }
        )
    validate_trait_uniqueness(bank)
    return bank


def validate_trait_uniqueness(bank: list[dict[str, str]]) -> None:
    hairs = [t["hair"] for t in bank]
    if len(hairs) != len(set(hairs)):
        raise RuntimeError("duplicate hair styles in trait bank")
    triples = {(t["age"], t["hair"], t["scar"]) for t in bank}
    if len(triples) != len(bank):
        raise RuntimeError("duplicate hair+age+scar combo in trait bank")


FACE_SHAPE = [
    "wide cheekbones, broad nose bridge",
    "narrow oval face, high forehead",
    "square jaw, thick neck",
    "round soft cheeks, short chin",
    "long angular face, deep-set eyes",
    "heart-shaped face, pointed chin",
    "broad flat nose, full lips",
    "narrow nose, close-set eyes",
    "heavy brow ridge, wide-set eyes",
    "soft rounded jaw, wide smile lines",
    "sharp cheekbones, hollow cheeks",
    "short wide face, thick eyebrows",
]


def format_face_traits(traits: dict[str, str], nat: str, slot: int) -> str:
    region = {
        "Ghana": "West African",
        "Nigeria": "West African",
        "Senegal": "West African",
        "Mali": "West African",
        "GrandChien": "Central African",
        "Congo": "Central African",
        "Angola": "Central African",
        "Kenya": "East African",
        "Ethiopia": "East African",
        "SouthAfrica": "Southern African",
    }.get(nat, "Sub-Saharan African")
    shape = FACE_SHAPE[(slot - 1) % len(FACE_SHAPE)]
    return (
        f"{region} mercenary face; {traits['age']}; {traits['skin']} skin; "
        f"bone structure: {shape}; "
        f"hair: {traits['hair']}; {traits['facial_hair']}; {traits['scar']}; "
        f"{traits['build']}"
    )


def kit_line(merc: dict) -> str:
    cat = merc["cat"]
    role = merc["role"]
    female = merc.get("female", False)
    gender_kit = "feminine fitted hot-climate merc kit, thin build" if female else "male merc kit"

    if cat == "Irregulars":
        base = (
            f"scrappy irregular PMC clothing — worn tee or loose shirt, "
            f"patched cargo trousers or simple work pants, scuffed boots; "
            f"{gender_kit}; no uniform insignia"
        )
    elif cat == "Fighters":
        base = (
            f"field fighter kit — light tactical vest or chest rig (empty), "
            f"rolled sleeves, cargo pants, combat boots; {gender_kit}; "
            f"mercenary patches OK, no army rank stripes"
        )
    elif cat == "Hardened":
        base = (
            f"professional hardened merc kit — clean tactical shirt, "
            f"structured vest or plate carrier (no plates visible), "
            f"neat cargo pants, quality boots; {gender_kit}; "
            f"PMC look, no army rank stripes"
        )
    else:
        role_kits = {
            "Medic": (
                "specialist medic kit — light field shirt, cargo pants, "
                "small IFAK pouch on belt, subtle red cross patch (small, not hospital gown), "
                "medical shears on vest, no stethoscope"
            ),
            "Instructor": (
                "instructor kit — neat field shirt, cargo pants, "
                "optional clipboard or folded map in hand (no weapon), "
                "pen in chest pocket, professional merc instructor look"
            ),
            "Sniper": (
                "light sniper field kit — muted shirt, ghillie scrim scarf loose at neck "
                "(not full ghillie suit), slim cargo pants, soft boots"
            ),
            "Sapper": (
                "sapper kit — work shirt, cargo pants with tool loops, "
                "small toolkit pouch on belt, work gloves tucked in pocket"
            ),
            "Mechanic": (
                "mechanic kit — grease-stained work shirt, cargo pants, "
                "tool roll or wrench visible on belt, practical boots"
            ),
        }
        base = role_kits.get(
            role,
            f"specialist merc kit — light field clothing; {gender_kit}",
        )
        if female:
            base += "; feminine fitted cut, thin build"
    return base


def pose_hint(merc: dict, slot: int) -> str:
    role = merc.get("role", "")
    hints = [
        "weight on left leg, right hand on hip, left arm relaxed asymmetric",
        "weight on right leg, left hand adjusting vest strap, right arm loose",
        "slight turn to camera-left, one knee soft, arms asymmetric",
        "confident lean back on right leg, left hand in pocket",
        "forward step on left foot, right hand holding belt, left arm down",
        "standing tall, right hand on thigh, left elbow bent outward",
        "subtle contrapposto, arms at different heights",
        "right foot forward, left hand on chest rig, right arm relaxed",
    ]
    if role == "Medic":
        return "calm stance, one hand resting on IFAK pouch, other arm relaxed"
    if role == "Instructor":
        return "authoritative stance, optional clipboard in left hand, right hand on hip"
    if role == "Sniper":
        return "patient still stance, slight head tilt, arms loose and asymmetric"
    if role in ("Sapper", "Mechanic"):
        return "practical worker stance, one hand near tool pouch, asymmetric shoulders"
    if merc.get("cat") == "Irregulars":
        return "relaxed irregular stance, slightly slouched shoulders, asymmetric arms"
    return hints[(slot - 1) % len(hints)]


def specialty_look(merc: dict) -> str:
    """Visual cues from CombatRole / Specialization — kit props, body language, not firearms."""
    role = merc.get("role") or ""
    spec = merc.get("spec") or ""
    female = bool(merc.get("female"))
    bits: list[str] = []

    role_map = {
        "Rifle": "rifleman bearing — alert eyes, field-ready posture; no rifle in hands",
        "Autorifleman": "autorifleman presence — solid stance, chest rig for magazines visible; empty hands",
        "Machinegunner": "heavy-weapons build cues — broader shoulders / stronger frame emphasis, ammo belt pouches; empty hands",
        "Grenadier": "grenadier kit cues — frag pouch or bandolier on vest; empty hands, no thrown weapon posed",
        "Medic": (
            "field medic: IFAK / med pouch / small red cross patch on arm or chest, shears or gauze cues; "
            "calm caregiver presence — NOT a hospital doctor with stethoscope; empty hands"
        ),
        "Instructor": (
            "instructor / teacher presence — confident posture, optional clipboard or training whistle on cord; "
            "experienced NCO vibe without army rank stripes; empty hands"
        ),
        "Sniper": "marksman patience — still focused eyes, light field kit, rangefinder pouch OK; NO scoped rifle in hands",
        "Sapper": "sapper / demo tech — tool loops, detonator pouch or wire cutters on belt; practical grease marks OK; empty hands",
        "Mechanic": "field mechanic — toolkit pouch, wrench loop, lightly soiled hands/cuffs; empty hands",
    }
    if role in role_map:
        bits.append(role_map[role])
    elif spec:
        bits.append(f"specialization {spec} should read in kit and bearing")

    if spec == "Doctor" and role == "Medic":
        bits.append("medical specialization dominant over combat look")
    if spec == "Leader" or role == "Instructor":
        bits.append("leadership bearing — others would listen to this person")
    if "Teacher" in (merc.get("traits") or []):
        bits.append("Teacher perk: instructional, patient-but-firm expression")
    if female and role in ("Autorifleman", "Machinegunner", "Grenadier"):
        bits.append("feminine fighter kit still role-correct, not fashion")

    return "; ".join(bits) if bits else "general mercenary bearing"


def veteran_look(merc: dict) -> str:
    """Veteran / green cues from AME category, level, background."""
    cat = merc.get("cat") or "Irregulars"
    lvl = int(merc.get("lvl") or 1)
    bg = merc.get("bg") or ""
    age_hint = ""

    if cat == "Irregulars":
        age_hint = (
            "GREEN / low veteran: younger or less weathered face, cheaper scrappy kit, "
            "nervous-or-eager expression OK, less scar tissue, boots scuffed not broken-in by years"
        )
        if lvl <= 2:
            age_hint += "; very green — looks new to paid contracts"
    elif cat == "Fighters":
        age_hint = (
            "TRAINED fighter: competent field presence, some wear on kit, steady eyes, "
            "militia or early army seasoning — not a raw recruit, not yet a hard veteran"
        )
        if lvl >= 4:
            age_hint += "; upper Fighter — more confidence and kit care"
    elif cat == "Hardened":
        age_hint = (
            "HARDENED veteran: weathered skin, deeper lines, calm dangerous eyes, "
            "professional PMC/ex-army kit quality, scars that look earned, "
            "posture of someone who survived many contracts"
        )
        if lvl >= 7:
            age_hint += "; senior Hardened — older face, grey in hair OK if traits allow"
        if bg == "ex-army":
            age_hint += "; ex-army seasoning without army rank insignia"
    elif cat == "Specialists":
        age_hint = (
            "SPECIALIST veteran of their craft: competent professional, kit matches role "
            "(medic/instructor/sniper/sapper/mechanic), confident niche expertise in expression"
        )
        if lvl >= 6:
            age_hint += "; senior specialist — seasoned face, trusted expert vibe"
        if role_is_medic_instructor(merc):
            age_hint += "; craft seniority over frontline toughness"
    else:
        age_hint = f"category {cat}, level {lvl}"

    return f"VETERANCY: category {cat}, starting level {lvl}. {age_hint}"


def role_is_medic_instructor(merc: dict) -> bool:
    return merc.get("role") in ("Medic", "Instructor")


def big_prompt(merc: dict, slot: int, face_traits: str) -> str:
    female = merc.get("female", False)
    build_note = "thin feminine mercenary proportions" if female else "natural mercenary proportions"
    return (
        "Jagged Alliance 3 mercenary BigPortrait style reference match. "
        "Full body standing three-quarter pose on solid opaque #504633 background "
        "(no transparency, no gradient). "
        f"IDENTITY/KIT LOCK: {face_traits}. "
        "CRITICAL ANTI-BLEED: do NOT copy Ice (vanilla JA3) face, hairline, jaw, "
        "skin undertone, or likeness — Ice is banned identity. Do NOT copy Magic, "
        "Blood, Shadow, Buns, or any named AIM merc face/hair/clothes. Style refs "
        "are for color grade / lighting / proportions LEVEL only. "
        "Each AME merc must look like a different African person — unique bone "
        "structure, nose width, eye shape, and age from IDENTITY. "
        f"SPECIALTY: role={merc.get('role')}, specialization={merc.get('spec')}. "
        f"{specialty_look(merc)}. "
        f"{veteran_look(merc)}. "
        f"OUTFIT: {kit_line(merc)}. "
        f"POSE: {pose_hint(merc, slot)}; interesting asymmetric pose; tall long legs like JA3 merc portraits; "
        f"head and boots fully in frame with #504633 margin above hair and below boots. "
        f"{build_note}. "
        "Hot-climate PMC/mercenary — no winter gear. "
        "NO firearm in hands, no rifle on table, no weapon held; holstered pistol in belt holster OK only. "
        "No army rank stripes or sergeant chevrons; merc/PMC patches OK. "
        "Clean fabric surfaces, minimal wrinkle noise — no muddy fold clutter on pants. "
        "Realistic JA3-adjacent merc illustration, not photoreal studio photo."
    )


def bust_prompt(face_traits: str, merc: dict) -> str:
    female = bool(merc.get("female"))
    gender = "feminine" if female else "masculine"
    return (
        "Jagged Alliance 3 mercenary Portrait style. "
        "Tight headshot — face almost fills entire frame (JA3 UI portrait crop). "
        f"Same IDENTITY/KIT LOCK: {face_traits}. "
        "ANTI-BLEED: not Ice, not Magic, not any vanilla AIM merc likeness. "
        f"SPECIALTY face read: {merc.get('role')} / {merc.get('spec')} — "
        f"{specialty_look(merc)}. "
        f"{veteran_look(merc)}. "
        f"{gender.capitalize()} African mercenary face, consistent with BigPortrait identity. "
        "Solid opaque #504633 background, no transparency. "
        "Expression matches specialty and veteran level (green vs hardened vs specialist calm). "
        "No helmet, no weapon, no hands in frame. "
        "Match JA3 portrait lighting and painterly realism level."
    )


README_TEXT = """# AME face identity prompts (`_ame_face_refs`)

Prompt bank for **GenerateImage** identity passes on the AME mercenary pool (`JAZZ_AME_01` … `JAZZ_AME_60`).

## What lives here

- `prompts.jsonl` — one JSON object per roster slot: `slot`, `id`, `name`, `female`, `cat`, `role`, `spec`, `lvl`, `nat`, `face_traits`, `specialty_look`, `veteran_look`, `big_prompt`, `bust_prompt`.
- `face_traits` — unique visual identity cues (age, skin tone, hair, facial hair, scars, build, bone structure). **Not** copied bio prose.
- `specialty_look` / `veteran_look` — role/spec kit+bearing and Irregulars→Hardened/Specialists seniority baked into prompts.
- Generated by `docs/tools/_gen_ame_portrait_prompts.py` from `docs/tools/_gen_ame_roster_60.py`.

## Style references (do not replace)

**Composition, color grade, proportions, and JA3 merc look** still come from:

`jazz-units/MercPortraits/References/` (+ `_quality_bar/Highball_ideal_Big.png` for proportions)

**AME batch ban:** never put `References/Ice.png` (or ship Ice) in `reference_image_paths` —
Ice bleed made the whole pool look like one vanilla merc. Prefer Highball proportions +
rotating non-Ice refs (Magic/Blood/Fauda/Meltdown) with strong ANTI-BLEED in the prompt.

Use `_ame_face_refs` only for **who** the face/body belongs to. Regenerate with:

1. Big on opaque `#504633` using `big_prompt` + non-Ice References style.
2. Portrait bust using `bust_prompt` (or tight crop from Big per portrait skill).
3. Background removal in a separate pass (BiRefNet / rembg); do not prompt transparent BG here.

## Regenerate prompts

```text
python docs/tools/_gen_ame_portrait_prompts.py
```

Spec: `docs/specs/active/JAZZ-UNITS-005.md`.
"""


def main() -> None:
    mod = load_roster_module()
    roster = mod.ROSTER
    traits_list = trait_bank(roster)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for slot, (merc, traits) in enumerate(zip(roster, traits_list, strict=True), start=1):
        face = format_face_traits(traits, merc["nat"], slot)
        rows.append(
            {
                "slot": slot,
                "id": f"JAZZ_AME_{slot:02d}",
                "name": merc["name"],
                "female": bool(merc.get("female")),
                "cat": merc["cat"],
                "role": merc["role"],
                "spec": merc.get("spec"),
                "lvl": merc.get("lvl"),
                "nat": merc["nat"],
                "face_traits": face,
                "specialty_look": specialty_look(merc),
                "veteran_look": veteran_look(merc),
                "big_prompt": big_prompt(merc, slot, face),
                "bust_prompt": bust_prompt(face, merc),
            }
        )

    with OUT_JSONL.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    OUT_README.write_text(README_TEXT, encoding="utf-8")
    line_count = len(rows)
    print(f"wrote {OUT_JSONL} lines={line_count}")
    print(f"wrote {OUT_README}")


if __name__ == "__main__":
    main()
