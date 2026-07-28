# Global AI — вопросы на утро (28→29 июля 2026)

Overnight реализованы STRATEGY-008…011 (011 частично). Ниже locked defaults — подтверди или поправь.

## Баланс / числа

1. **Soft caps генератора** (MG ≤ min(4, 35%), sniper ≤ min(3, 25%), specialist ≤ min(3, 20%)) — ок?
2. **Tax**: только city/farm через tax; mine остаётся в diamond_stock/shipment — ок, или mine тоже через tax?
3. **Recruits**: farm **+1/сутки**, city **+2/сутки**; caps 8/20 — ок? (roadmap говорил city 2–3)
4. **Outpost manpower** start **20** / cap **60**; Major **80** / **600** — ок?
5. **RecruiterThreshold=8**, cargo manpower convoy **16**, trigger **40%** — ок?
6. **Militia training** жрёт **4** рекрута за сессию — ок?

## Militia Operation (STRATEGY-011)

7. Точный vanilla/preset id операции обучения ополчения: `MilitiaTraining`? `TrainMilitia`? другой?
8. На каких методах вешать consume: `CanPerform` + `Complete` / `OnComplete` / progress tick?
9. Если рекрутов 0 — блокировать старт операции или только показывать warning?

## Runtime smoke (приоритет)

10. После Reload модов с диска: schema diagnostics = **3**; tax/recruiter/manpower иконки; combat spawn списывает money+manpower; city/farm не капают outpost.money напрямую.

## Commits overnight

- `4e268cf` STRATEGY-007
- `1bc41f8` / `c4398d5` STRATEGY-008
- `f7548fd` / `2e15240` STRATEGY-009
- `c46a105` / `77b00cb` STRATEGY-010
- (+ STRATEGY-011 commit после этого файла)
