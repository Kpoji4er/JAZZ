# Agent tooling: сохранять скрипты и знания для следующих агентов

Агенты JAZZ часто пишут одноразовые Python/PowerShell-скрипты под миграцию `items.lua`, CSV, audit и cleanup. Эти артефакты — часть операционной памяти проекта, не «мусор сессии».

## Обязательно

1. **Не удалять** рабочие скрипты из `docs/tools/` (и профильных `scripts/`), которые:
   - меняли generated data / CSV / companions;
   - делали audit/acceptance checks для SPEC;
   - чинили массовые баги rename/strip (SlotType, Handling, Mount, …).
2. После появления нового полезного скрипта **в том же change set**:
   - добавить строку в `docs/tools/README.md` (назначение, вход, выход, idempotent?);
   - при системной/повторяемой процедуре — ссылку в профильный playbook (например `.agents/docs/playbooks/weapons-balance.md`) и/или `.agents/docs/index.md`.
3. Временные `_tmp_*.py` / scratch-файлы можно удалять **только если** их логика уже перенесена в постоянный скрипт или README. Иначе переименовать в каноническое имя без `_tmp_`.
4. В summary для пользователя / handoff другому агенту кратко указать: какие скрипты добавлены и где они описаны.
5. Правило «сохранять tooling и описывать его» само по себе тоже живёт здесь и в `.cursor/rules/jazz-agent-tooling.mdc` — не считать это одноразовой просьбой чата.

## Не делать

- Молча `Remove-Item` / `rm` на `_apply_*`, `_export_*`, `_audit_*`, `_remove_*`, `_promote_*` после «успешного» прогона.
- Оставлять знание только в agent transcript: следующий агент может не видеть тот чат.
- Дублировать огромные one-off без README-строки «зачем».

## Где смотреть

| Что | Где |
| --- | --- |
| Каталог скриптов | `docs/tools/README.md` |
| DAP / live Lua | `scripts/dap/`, playbook `.agents/docs/playbooks/dap-runtime-debug.md` |
| ATTACH / weapons generated | `.agents/docs/playbooks/weapons-balance.md` |
| Cursor rule | `.cursor/rules/jazz-agent-tooling.mdc` |
| Spec ATTACH-001 | `docs/specs/active/JAZZ-ATTACH-001.md` |
