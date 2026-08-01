"""Prep clean salary-only staging: revert unrelated AUG line in jazz-units/items.lua;
build salary-only Russian.csv; bump metadata versions."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")


def git_show(repo: Path, path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"HEAD:{path}"],
        cwd=repo,
        encoding="utf-8",
    )


def revert_aug_in_units_items() -> None:
    path = UNITS / "items.lua"
    text = path.read_text(encoding="utf-8")
    # Revert the single accidental rename shown in git diff (~line 75017).
    # Prefer a unique nearby context if possible; fall back to first JAZZ_ that HEAD has as AUG.
    head = git_show(UNITS, "items.lua")
    # Find first position where work has JAZZ_AUGCompensator_03 and head has AUGCompensator_03
    # by scanning work for lines that differ.
    if '"JAZZ_AUGCompensator_03"' not in text:
        print("AUG: nothing to revert")
        return
    # Only revert if head still uses plain AUGCompensator_03 more than work
    if text.count('"JAZZ_AUGCompensator_03"') == head.count('"JAZZ_AUGCompensator_03"') + 1:
        # Find a context unique to the diff hunk: look for sequence with Compensator in AvailableComponents
        # Replace first occurrence where surrounding 200 chars match head with AUG not JAZZ_
        replaced = False
        for m in re.finditer(r'"JAZZ_AUGCompensator_03"', text):
            start = max(0, m.start() - 120)
            end = min(len(text), m.end() + 120)
            window = text[start:end]
            head_window = window.replace('"JAZZ_AUGCompensator_03"', '"AUGCompensator_03"', 1)
            if head_window in head or '"AUGCompensator_03"' in head[start : end + 50]:
                text = text[: m.start()] + '"AUGCompensator_03"' + text[m.end() :]
                replaced = True
                break
        if not replaced:
            # last resort: replace first only
            text = text.replace('"JAZZ_AUGCompensator_03"', '"AUGCompensator_03"', 1)
            print("AUG: reverted first occurrence (fallback)")
        else:
            print("AUG: reverted contextual occurrence")
        path.write_text(text, encoding="utf-8")
    else:
        print("AUG: count mismatch; leave alone", text.count('"JAZZ_AUGCompensator_03"'), head.count('"JAZZ_AUGCompensator_03"'))


def salary_only_russian_csv() -> Path:
    """Write a temp Russian.csv = HEAD + salary string replacements. Backup WIP beside it."""
    wip = JAZZ / "Russian.csv"
    backup = JAZZ / "Russian.csv.wip_salary_commit"
    backup.write_text(wip.read_text(encoding="utf-8"), encoding="utf-8")
    head = git_show(JAZZ, "Russian.csv")
    reps = [
        (
            '890000000002115,"Ха! Поехали крушить. Бесплатно, лишь бы весело было.","Ха! Поехали крушить. Бесплатно, лишь бы весело было."',
            '890000000002115,"Ха! Поехали крушить. Дёшево и сердито — лишь бы весело было.","Ха! Поехали крушить. Дёшево и сердито — лишь бы весело было."',
        ),
        (
            '890000000002116,"Контракт заканчивается, но я всё равно бесплатный — продлеваем?","Контракт заканчивается, но я всё равно бесплатный — продлеваем?"',
            '890000000002116,"Контракт заканчивается — продлеваем, или сам пойду кого-нибудь чинить?","Контракт заканчивается — продлеваем, или сам пойду кого-нибудь чинить?"',
        ),
        (
            "890000000002417,Контракт заканчивается. Я всё равно бесплатный — продолжаем службу?,Контракт заканчивается. Я всё равно бесплатный — продолжаем службу?",
            "890000000002417,Контракт заканчивается. Продлеваем службу, или мне искать другой аэродром?,Контракт заканчивается. Продлеваем службу, или мне искать другой аэродром?",
        ),
    ]
    out = head
    for old, new in reps:
        if old not in out:
            raise SystemExit(f"HEAD Russian.csv missing expected old string:\n{old[:80]}...")
        out = out.replace(old, new)
    wip.write_text(out, encoding="utf-8")
    print("Russian.csv: salary-only overlay ready; WIP backed up to Russian.csv.wip_salary_commit")
    return backup


def bump_metadata(repo: Path, bullet: str) -> None:
    path = repo / "metadata.lua"
    text = path.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", text)
    if not m:
        raise SystemExit(f"no version in {path}")
    ver = int(m.group(1)) + 1
    text2 = re.sub(r"'version',\s*\d+", f"'version', {ver}", text, count=1)
    lm = re.search(r"'last_changes',\s*\"((?:\\.|[^\"])*)\"", text2)
    if not lm:
        # try single-quoted multiline style used in files
        lm = re.search(r"'last_changes',\s*'((?:\\.|[^'])*)'", text2)
        if not lm:
            raise SystemExit("last_changes not found")
        old = lm.group(0)
        inner = lm.group(1)
        new_inner = f"- {bullet}\\n" + inner
        text2 = text2.replace(old, f"'last_changes', '{new_inner}'", 1)
    else:
        old = lm.group(0)
        inner = lm.group(1)
        new_inner = f"- {bullet}\\n" + inner
        text2 = text2.replace(old, f"'last_changes', \"{new_inner}\"", 1)
    path.write_text(text2, encoding="utf-8")
    print(f"{repo.name} metadata version -> {ver}")


def salary_only_readme() -> Path:
    """HEAD README + salary script rows; backup WIP."""
    wip = JAZZ / "docs" / "tools" / "README.md"
    backup = JAZZ / "docs" / "tools" / "README.md.wip_salary_commit"
    backup.write_text(wip.read_text(encoding="utf-8"), encoding="utf-8")
    head = git_show(JAZZ, "docs/tools/README.md")
    insert = (
        "| `_fix_madman_salary.py` | Jazz_Madman: `StartingSalary`/`SalaryLv1`/`SalaryMaxLv` в `jazz-units/items.lua` (companion править отдельно). |\n"
        "| `_fix_free_merc_salaries.py` | Jazz_Grom / Jazz_Hitman: paid hire salaries в companion + `jazz-units/items.lua`. |\n"
        "| `_sync_grom_rehire_chat.py` | Гром RehireIntro: убрать «бесплатный» из `items.lua` + `Russian.csv`. |\n"
        "| `_sync_madman_chat_salary_strings.py` | Синк AIM-фраз Бешеного (не «бесплатный») в `items.lua` + `Russian.csv`/`English.csv`. |\n"
    )
    marker = "| `_audit_recoil_dist.py`"
    if marker in head:
        # insert after audit_recoil line
        lines = head.splitlines(keepends=True)
        out = []
        done = False
        for line in lines:
            out.append(line)
            if (not done) and line.startswith(marker):
                out.append(insert)
                done = True
        if not done:
            out.append("\n" + insert)
        head = "".join(out)
    else:
        head = head.rstrip() + "\n\n" + insert
    wip.write_text(head, encoding="utf-8")
    print("README.md: salary-only overlay ready")
    return backup


def bump_units_from_head() -> None:
    """Bump jazz-units metadata from HEAD content (avoid unrelated WIP)."""
    path = UNITS / "metadata.lua"
    backup = UNITS / "metadata.lua.wip_salary_commit"
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    head = git_show(UNITS, "metadata.lua")
    path.write_text(head, encoding="utf-8")
    bump_metadata(UNITS, "Paid hire for Madman/Grom/Hitman (fix StartingSalary=0 div0 on AIM)")
    print("units metadata prepared from HEAD + bump")


def bump_jazz_from_head() -> None:
    path = JAZZ / "metadata.lua"
    backup = JAZZ / "metadata.lua.wip_salary_commit"
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    head = git_show(JAZZ, "metadata.lua")
    path.write_text(head, encoding="utf-8")
    bump_metadata(JAZZ, "Docs/loc: Madman/Grom/Hitman paid hire; AIM chat no longer claims free")
    print("jazz metadata prepared from HEAD + bump")


if __name__ == "__main__":
    revert_aug_in_units_items()
    salary_only_russian_csv()
    salary_only_readme()
    bump_units_from_head()
    bump_jazz_from_head()
    print("PREP DONE")
