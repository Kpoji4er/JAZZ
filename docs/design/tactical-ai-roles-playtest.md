# Playtest: tactical AI (batch smokes → full playtest)

Ветка: `feature/tactical-ai-roles` в `jazz` и `jazz-units`.

Сначала **смоки** по чеклисту ниже, потом обычный playtest на кампании/секторах.

| Spec | Код | Smoke |
| --- | --- | --- |
| [ROLE-001](../specs/active/JAZZ-AI-ROLE-001.md) | done | OK 29.07 |
| [POL-001](../specs/active/JAZZ-AI-POL-001.md) | done | P1–P5 |
| [ROLE-002](../specs/active/JAZZ-AI-ROLE-002.md) (+ Rebel = ROLE-003) | done | R1–R5 |
| [MED-001](../specs/active/JAZZ-AI-MED-001.md) | done | M1–M3 |
| [POL-002](../specs/active/JAZZ-AI-POL-002.md) | done | A1–A3 |
| [CTX-001](../specs/active/JAZZ-AI-CTX-001.md) | done | C1–C2 |
| [CMD-001](../specs/active/JAZZ-AI-CMD-001.md) | done | O1 |
| [ACT-001](../specs/active/JAZZ-AI-ACT-001.md) | done | S1–S3 |
| [ACT-002](../specs/active/JAZZ-AI-ACT-002.md) | code | S1–S3 (curtain) |

## Перед тестом

1. Закрыть игру / Mod Editor.
2. Reload модов с диска.
3. После правок `items.lua` — желателен SaveWholeMod `jazz-units`.

---

## POL-001 — cover / proximity

- **P1** Frontliner чаще в cover vs visible shooter.
- **P2** Assaulter всё ещё давит.
- **P3** Flanker не «укрыватель» (OptLoc TakeCover ~15).
- **P4** Союзники не разбегаются из‑за Proximity.
- **P5** Нет краша StartAI; MG/Medic ок.

---

## ROLE-002 / ROLE-003 — stance helper

- **R1** Scout default `Legion_Flanker`; в упор/push → `Legion_Assaulter` (F2). Debug archetype id.
- **R2** Roughneck / knife secondary: при AP-reach реально Melee (не фикс. 10 тайлов).
- **R3** T1–T2 при ранах/низком Will иногда `Deserter`; T4 / Merc почти никогда.
- **R4** RebelFlanker без мгновенного Melee с 10 тайлов; panic спокойнее Legion.
- **R5** Нет спама Hide в начале хода фланкера; нет краша PickCustom.

---

## MED-001 — medic (когда ready)

- **M1** Bonemaker рано уходит в Medic при bleed / низком HP союзника.
- **M2** Нет freeze на Bandage (ход завершается / fail-safe).
- **M3** Bleed-цель приоритетнее «чуть поцарапанного».

---

## POL-002 — anchors / peek

- **A1** Солдат рядом со снайпером чаще «экран», не в чистом поле один.
- **A2** Свита лидера не уходит далеко.
- **A3** Повторный peek → dest с last_attack_pos штрафуется.

---

## CTX-001 — Urban / LowVis

- **C1** Night: снайпер Hold, не-снайперы flare; Fog: без «ждать свет».
- **C2** Город/indoor: выше cover/OW bias.

---

## CMD-001 — aura

- **O1** Sgt ~15 / Lt ~25 / Capt карта — заметный Hold/Push bias у союзников в радиусе.
- **O2** На командире perk badge **Командная аура**; на союзниках в радиусе **Под влиянием ауры**; вне радиуса / после смерти командира — снят.

---

## ACT-001 — smoke / OW / flare

- **S1** Smoke на перебежку / LOS-break, не рандом в толпу.
- **S2** После 2+ peek — чаще OW.
- **S3** После flare — короткий Press bias.

## ACT-002 — smoke curtain / post-turn self-cover

- **S1** Дым на угол / отрезок OW→exit, куда свой ещё выбегает (закрыть вражеский OW).
- **S2** Прямо на своих — только после их хода в этом combat turn.
- **S3** Не ослепляет ещё не ходивших своих без curtain-причины; не кидает «в пустоту».

---

## REG-001 — isolated regroup

- **R1** 1–2 Legion далеко от основной группы (≥3 @ ≥18) → archetype `Legion_Regroup`, движение к своим, не Deserter exit.
- **R2** В плотном отряде (≥3 в 8 тайлах) Regroup не срабатывает.

---

## POL-003 — anti-stack

- **P1** Два AI не занимают одну XYZ-клетку (stance не обходит dibs).
- **P2** Реже стоят впритык на одном выгодном cover (soft spacing).

## POL-004 — casualty-aware anti-stack

- **P1** Одна dead/downed/incapacitated casualty снижает привлекательность той же и соседней destination относительно безопасной альтернативы.
- **P2** Две casualties в радиусе 3 сильнее выталкивают ranged AI из fatal funnel; при единственном маршруте casualty tile остаётся soft и проходимой.
- **P3** Melee и medic сохраняют обязательный подход благодаря floor 55%; replay/seed не меняет modifier.
- **P4** В debug destination details modifier появляется один раз как `CROWD/DANGER MOD (%)` после BiasMarker.

## Регрессия всегда

Нет краша; MG setup; Front/Assault/Flanker читаются разными; replay/seed стабилен на глаз.
