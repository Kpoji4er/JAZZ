# -*- coding: utf-8 -*-
"""Jazz slug → ja2mercs folder map (confident / skip / ambiguous).

Generated for remesh from Downloads/ja2mercs/ja2mercs.
speech_source form: ja2mercs:<cat>/<merc>[|battle=<pid>]
Only rows with decision=remesh|need_pack are written into jazz_to_ja2_profile.csv.

Columns:
  slug, folder, profile_id, battle_pid, decision, reason
"""
from __future__ import annotations

# Canonical map used by ship tooling and docs. Keep in sync with jazz_to_ja2_profile.csv.
JA2MERCS_MAP: list[dict[str, str]] = [
    # --- remesh (shipped overwrite) ---
    {"slug": "colby", "folder": "аимовцы/trevor", "profile_id": "005", "battle_pid": "", "decision": "remesh", "reason": "Trevor; was done from trevor.rar"},
    {"slug": "blade", "folder": "мерки/razor", "profile_id": "043", "battle_pid": "", "decision": "remesh", "reason": "Razor"},
    {"slug": "ira", "folder": "локался/ira", "profile_id": "059", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "dimitri", "folder": "локался/dimitry", "profile_id": "060", "battle_pid": "", "decision": "remesh", "reason": "NOT цс/manuel (also 060)"},
    {"slug": "madman", "folder": "локался/maddog", "profile_id": "072", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "conrad", "folder": "локался/conrad", "profile_id": "070", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "rothman", "folder": "аимовцы/stephen", "profile_id": "030", "battle_pid": "", "decision": "remesh", "reason": "Stefan; filename Hitman lies"},
    {"slug": "quinten", "folder": "аимовцы/danny", "profile_id": "028", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "vicious", "folder": "аимовцы/lamalice", "profile_id": "032", "battle_pid": "", "decision": "remesh", "reason": "La Malice"},
    {"slug": "nervous", "folder": "мерки/haywire", "profile_id": "041", "battle_pid": "", "decision": "remesh", "reason": "Haywire; not Razor 043"},
    {"slug": "flo", "folder": "мерки/flo", "profile_id": "044", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "cougar", "folder": "мерки/cougar", "profile_id": "048", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "miguel", "folder": "локался/miguel", "profile_id": "057", "battle_pid": "", "decision": "remesh", "reason": "NOT импы/imp4"},
    {"slug": "gamos", "folder": "локался/Hamous", "profile_id": "063", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "dynamo", "folder": "локался/Dinamo", "profile_id": "066", "battle_pid": "", "decision": "remesh", "reason": "SLF Dynamo; NOT но-шж/simon"},
    {"slug": "benny", "folder": "но-шж/benni", "profile_id": "067", "battle_pid": "", "decision": "remesh", "reason": "SJ Benny; NOT локался/shank"},
    {"slug": "simon", "folder": "но-шж/simon", "profile_id": "066", "battle_pid": "", "decision": "remesh", "reason": "SJ Simon; NOT локался/Dinamo"},
    {"slug": "gaston", "folder": "цс/gaston", "profile_id": "U_58", "battle_pid": "165", "decision": "remesh", "reason": "UB Gaston; speech U_58 + battle 165; NOT локался/carlos"},
    {"slug": "horg", "folder": "цс/bychok", "profile_id": "U_59", "battle_pid": "166", "decision": "remesh", "reason": "UB Stogie; speech U_59 + battle 166"},
    {"slug": "static", "folder": "аимовцы/static", "profile_id": "026", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "highball", "folder": "аимовцы/kliff", "profile_id": "020", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "bull", "folder": "аимовцы/Bull", "profile_id": "021", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "cord", "folder": "мерки/gusket", "profile_id": "042", "battle_pid": "", "decision": "remesh", "reason": "Gasket"},
    {"slug": "hobbit", "folder": "мерки/gumpy", "profile_id": "045", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "ricochet", "folder": "мерки/numb", "profile_id": "049", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "meat", "folder": "мерки/bubba", "profile_id": "050", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "carlos", "folder": "локался/carlos", "profile_id": "058", "battle_pid": "", "decision": "remesh", "reason": "Carlos RPC; NOT цс/gaston"},
    {"slug": "devin", "folder": "локался/devin", "profile_id": "061", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "shank", "folder": "локался/shank", "profile_id": "067", "battle_pid": "", "decision": "remesh", "reason": "SLF Shank; NOT но-шж/benni"},
    {"slug": "vince", "folder": "локался/vince", "profile_id": "069", "battle_pid": "", "decision": "remesh", "reason": ""},
    {"slug": "hitman", "folder": "локался/slay", "profile_id": "064", "battle_pid": "", "decision": "remesh", "reason": "Slay; not Hennessey"},
    {"slug": "kulba", "folder": "цс/kulba", "profile_id": "062", "battle_pid": "", "decision": "remesh", "reason": "filter 062 only; ignore co-folder 118"},
    {"slug": "eskimo", "folder": "но-шж/escimo", "profile_id": "065", "battle_pid": "", "decision": "remesh", "reason": "filter 065 / D_065 / r_065; ignore stray 067"},
    # --- need_pack fill ---
    {"slug": "monk", "folder": "вилдфаер/monk", "profile_id": "170", "battle_pid": "", "decision": "need_pack", "reason": "WF Monk"},
    {"slug": "allik", "folder": "вилдфаер/brains", "profile_id": "171", "battle_pid": "", "decision": "need_pack", "reason": "WF Brains / Allik"},
    {"slug": "henning", "folder": "вилдфаер/henning", "profile_id": "173", "battle_pid": "", "decision": "need_pack", "reason": "WF Henning"},
    {"slug": "vilde", "folder": "вилдфаер/scream", "profile_id": "172", "battle_pid": "", "decision": "need_pack", "reason": "WF Scream / Vilde"},
    {"slug": "grace", "folder": "вилдфаер/grace", "profile_id": "176", "battle_pid": "", "decision": "need_pack", "reason": "WF Grace"},
    {"slug": "steiger", "folder": "вилдфаер/rudolf", "profile_id": "177", "battle_pid": "", "decision": "need_pack", "reason": "WF Rudolf / Steiger"},
    {"slug": "lucky", "folder": "вилдфаер/lucky", "profile_id": "174", "battle_pid": "", "decision": "need_pack", "reason": "WF Lucky"},
    {"slug": "laura", "folder": "вилдфаер/laura", "profile_id": "175", "battle_pid": "", "decision": "need_pack", "reason": "WF Laura"},
    {"slug": "biggens", "folder": "цс/biggens", "profile_id": "U_61", "battle_pid": "168", "decision": "need_pack", "reason": "UB Biggens; speech U_61 + battle 168"},
    # --- skip / ambiguous (owner) ---
    {"slug": "grom", "folder": "но-шж/гром", "profile_id": "076", "battle_pid": "047", "decision": "remesh", "reason": "user: both 076_*+047_* are Grom (replaced/reused IDs); battle from 047; speech merge_speech fullest; NOT Larry for this pack"},
    {"slug": "mike", "folder": "локался/mike", "profile_id": "074", "battle_pid": "", "decision": "skip_ambiguous", "reason": "Mike 074? identity unclear vs JA1/NO notes"},
    {"slug": "manuel", "folder": "цс/manuel", "profile_id": "060", "battle_pid": "", "decision": "skip_ambiguous", "reason": "folder pid 060 = Dimitri; profile Manuel is 071 — do not mix"},
    {"slug": "biff", "folder": "", "profile_id": "040", "battle_pid": "", "decision": "skip_no_folder", "reason": "no ja2mercs folder; keep data_slf"},
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
    # Same-merc dual file prefixes (Grom 076+047): battle + merge_speech.
    if row.get("slug") == "grom" and battle:
        return f"ja2mercs:{folder}|battle={battle}|merge_speech"
    if battle:
        return f"ja2mercs:{folder}|battle={battle}"
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
    # This module lives in docs/tools — parents[1]=docs/tools's parent = jazz? 
    # __file__ = jazz/docs/tools/_ja2mercs_folder_map.py → parents[2] = jazz
    write_csv(out)
    print(f"Wrote {out} rows={len(JA2MERCS_MAP)}")
