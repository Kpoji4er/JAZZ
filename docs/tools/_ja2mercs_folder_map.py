# -*- coding: utf-8 -*-
"""Jazz slug → ja2mercs folder map (confident / skip / ambiguous).

Preferred pack: Downloads/ja2mercs (1)/ja2mercs (pid-prefixed folders +
схема реплик *.xlsx). Falls back to Downloads/ja2mercs/ja2mercs via ship root
discovery / fuzzy folder resolve.

speech_source form: ja2mercs:<cat>/<merc>[|battle=<pid>][|merge_speech]
Only rows with decision=remesh|need_pack are written into jazz_to_ja2_profile.csv.

Columns:
  slug, folder, profile_id, battle_pid, decision, reason
"""
from __future__ import annotations

# Canonical map used by ship tooling and docs. Keep in sync with jazz_to_ja2_profile.csv.
JA2MERCS_MAP: list[dict[str, str]] = [
    # --- remesh (shipped overwrite) ---
    {"slug": "colby", "folder": "аимовцы/005 trevor", "profile_id": "005", "battle_pid": "", "decision": "remesh", "reason": "Trevor; pid-prefixed pack"},
    {"slug": "blade", "folder": "мерки/043 razor", "profile_id": "043", "battle_pid": "", "decision": "remesh", "reason": "Razor; MERK no hire 081–120"},
    {"slug": "ira", "folder": "локался/059 ira", "profile_id": "059", "battle_pid": "", "decision": "remesh", "reason": "RPC; hire bank usually absent"},
    {"slug": "dimitri", "folder": "локался/060 dimitry", "profile_id": "060", "battle_pid": "", "decision": "remesh", "reason": "NOT цс/167 manuel"},
    {"slug": "madman", "folder": "локался/072 maddog", "profile_id": "072", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "conrad", "folder": "локался/070 conrad", "profile_id": "070", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "rothman", "folder": "аимовцы/030 stephen", "profile_id": "030", "battle_pid": "", "decision": "remesh", "reason": "Stefan; filename Hitman lies"},
    {"slug": "quinten", "folder": "аимовцы/028 danny", "profile_id": "028", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "vicious", "folder": "аимовцы/032 lamalice", "profile_id": "032", "battle_pid": "", "decision": "remesh", "reason": "La Malice"},
    {"slug": "nervous", "folder": "мерки/041 haywire", "profile_id": "041", "battle_pid": "", "decision": "remesh", "reason": "Haywire; MERK no hire"},
    {"slug": "flo", "folder": "мерки/044 flo", "profile_id": "044", "battle_pid": "", "decision": "remesh", "reason": "MERK no hire"},
    {"slug": "cougar", "folder": "мерки/048 cougar", "profile_id": "048", "battle_pid": "", "decision": "remesh", "reason": "MERK no hire"},
    {"slug": "miguel", "folder": "локался/057 miguel", "profile_id": "057", "battle_pid": "", "decision": "remesh", "reason": "NOT импы/imp4"},
    {"slug": "gamos", "folder": "локался/063 Hamous", "profile_id": "063", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "dynamo", "folder": "локался/066 Dynamo", "profile_id": "066", "battle_pid": "", "decision": "remesh", "reason": "SLF Dynamo; NOT но-шж/062 simon"},
    # SJ banks remapped in ja2mercs (1): Benny 067→040, Simon 066→062 (Kulba moved to 164).
    {"slug": "benny", "folder": "но-шж/040 benni", "profile_id": "040", "battle_pid": "", "decision": "remesh", "reason": "SJ Benny files remapped 067→040; NOT Biff data_slf 040; NOT локался/shank"},
    {"slug": "simon", "folder": "но-шж/062 simon", "profile_id": "062", "battle_pid": "", "decision": "remesh", "reason": "SJ Simon remapped 066→062; NOT Dynamo; NOT old Kulba 062"},
    # ЦС consolidated under battle pid (U_58→165, U_59→166, U_61→168).
    {"slug": "gaston", "folder": "цс/165 gaston", "profile_id": "165", "battle_pid": "", "decision": "remesh", "reason": "UB Gaston; pack consolidated on 165 (was U_58+165); NOT локался/carlos"},
    {"slug": "horg", "folder": "цс/166 stogie", "profile_id": "166", "battle_pid": "", "decision": "remesh", "reason": "UB Stogie; consolidated on 166 (was U_59+166); prefer not 166 stogie UB"},
    {"slug": "static", "folder": "аимовцы/026 static", "profile_id": "026", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "highball", "folder": "аимовцы/020 kliff", "profile_id": "020", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "bull", "folder": "аимовцы/021 Bull", "profile_id": "021", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "cord", "folder": "мерки/042 gusket", "profile_id": "042", "battle_pid": "", "decision": "remesh", "reason": "Gasket; MERK no hire"},
    {"slug": "hobbit", "folder": "мерки/045 gumpy", "profile_id": "045", "battle_pid": "", "decision": "remesh", "reason": "MERK no hire"},
    {"slug": "ricochet", "folder": "мерки/049 numb", "profile_id": "049", "battle_pid": "", "decision": "remesh", "reason": "MERK no hire"},
    {"slug": "meat", "folder": "мерки/050 bubba", "profile_id": "050", "battle_pid": "", "decision": "remesh", "reason": "MERK no hire"},
    {"slug": "carlos", "folder": "локался/058 carlos", "profile_id": "058", "battle_pid": "", "decision": "remesh", "reason": "Carlos RPC; NOT цс/165 gaston"},
    {"slug": "devin", "folder": "локался/061 devin", "profile_id": "061", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "shank", "folder": "локался/067 shank", "profile_id": "067", "battle_pid": "", "decision": "remesh", "reason": "SLF Shank; NOT но-шж/040 benni"},
    {"slug": "vince", "folder": "локался/069 vince", "profile_id": "069", "battle_pid": "R_069", "decision": "remesh", "reason": "NEW pack often stubs on 069_*; full lines on R_069 — merge_speech longest"},
    {"slug": "hitman", "folder": "локался/064 slay", "profile_id": "064", "battle_pid": "", "decision": "remesh", "reason": "Slay; not Hennessey"},
    {"slug": "kulba", "folder": "цс/164 kulba", "profile_id": "164", "battle_pid": "R_164", "decision": "remesh", "reason": "UB Kulba 062→164; full lines often R_164; IGNORE co-folder 118"},
    {"slug": "eskimo", "folder": "но-шж/065 escimo", "profile_id": "065", "battle_pid": "", "decision": "remesh", "reason": "filter 065 / D_065 / R_065"},
    # --- need_pack / WF AIM (hire 081–120 present) ---
    {"slug": "monk", "folder": "вилдфаер/170 monk", "profile_id": "170", "battle_pid": "", "decision": "remesh", "reason": "WF Monk"},
    {"slug": "allik", "folder": "вилдфаер/171 brains", "profile_id": "171", "battle_pid": "", "decision": "remesh", "reason": "WF Brains / Allik"},
    {"slug": "henning", "folder": "вилдфаер/173 henning", "profile_id": "173", "battle_pid": "", "decision": "remesh", "reason": "WF Henning"},
    {"slug": "vilde", "folder": "вилдфаер/172 scream", "profile_id": "172", "battle_pid": "", "decision": "remesh", "reason": "WF Scream / Vilde"},
    {"slug": "grace", "folder": "вилдфаер/176 grace", "profile_id": "176", "battle_pid": "", "decision": "remesh", "reason": "WF Grace"},
    {"slug": "steiger", "folder": "вилдфаер/177 rudolf", "profile_id": "177", "battle_pid": "", "decision": "remesh", "reason": "WF Rudolf / Steiger"},
    {"slug": "lucky", "folder": "вилдфаер/174 lucky", "profile_id": "174", "battle_pid": "", "decision": "remesh", "reason": "WF Lucky"},
    {"slug": "laura", "folder": "вилдфаер/175 laura", "profile_id": "175", "battle_pid": "", "decision": "remesh", "reason": "WF Laura"},
    {"slug": "biggens", "folder": "цс/168 biggens", "profile_id": "168", "battle_pid": "R_168", "decision": "remesh", "reason": "UB Biggens 168 (=old U_61 speech); full lines often R_168 — merge_speech"},
    {"slug": "manuel", "folder": "цс/167 manuel", "profile_id": "167", "battle_pid": "R_167", "decision": "remesh", "reason": "UB Manuel pack pid 167; merge R_167 when longer"},
    # Grom: old 076_* → R_047_*; battle/speech both under 047 with merge against R_047.
    {"slug": "grom", "folder": "но-шж/047 gromov", "profile_id": "047", "battle_pid": "R_047", "decision": "remesh", "reason": "both 047_* + R_047_* (ex-076) are Grom; merge_speech fullest; NOT Larry"},
    # Mike: pack present; owner wants VO — ship 074 + R_074 fullest.
    {"slug": "mike", "folder": "локался/074 mike", "profile_id": "074", "battle_pid": "R_074", "decision": "remesh", "reason": "combat 074+R_074 NEW; hire 081–120 from OLD локался/mike R_074 (HIRE_ALT_BANKS)"},
    {"slug": "biff", "folder": "", "profile_id": "040", "battle_pid": "", "decision": "skip_no_folder", "reason": "no ja2mercs Biff folder; data_slf combat-proxy hire (no archive 081–120; do not use но-шж/040 benni)"},
    {"slug": "lynx", "folder": "", "profile_id": "002", "battle_pid": "", "decision": "skip_no_folder", "reason": "no ja2mercs folder; keep data_slf"},
    {"slug": "tosca", "folder": "", "profile_id": "016", "battle_pid": "", "decision": "skip_no_folder", "reason": "Buzz 016 absent; keep data_slf"},
    {"slug": "spider", "folder": "", "profile_id": "019", "battle_pid": "", "decision": "skip_no_folder", "reason": "Houston 019 absent; keep data_slf"},
    {"slug": "spouke", "folder": "", "profile_id": "", "battle_pid": "", "decision": "skip_manual", "reason": "done_manual — never overwrite"},
]


def speech_source_for(row: dict[str, str]) -> str:
    folder = row.get("folder") or ""
    if not folder:
        return ""
    battle = (row.get("battle_pid") or "").strip()
    # Same-merc dual prefixes (bare + R_*): always merge_speech when battle set.
    if battle:
        return f"ja2mercs:{folder}|battle={battle}|merge_speech"
    return f"ja2mercs:{folder}"


def write_csv(path) -> None:
    import csv
    from pathlib import Path

    p = Path(path)
    fields = ["slug", "folder", "profile_id", "battle_pid", "decision", "reason", "speech_source"]
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in JA2MERCS_MAP:
            out = dict(row)
            out["speech_source"] = speech_source_for(row) if row["decision"] in (
                "remesh",
                "need_pack",
            ) else ""
            w.writerow(out)


if __name__ == "__main__":
    from pathlib import Path

    out = Path(__file__).resolve().parents[2] / (
        "docs/design/mercs-ja12/_voice-source/jazz_to_ja2mercs_folders.csv"
    )
    write_csv(out)
    print(f"Wrote {out} rows={len(JA2MERCS_MAP)}")
