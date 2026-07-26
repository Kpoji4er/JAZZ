# Спецификации изменений JAZZ

Этот раздел является источником истины для утверждённых требований до реализации.

- `active/` — draft, approved и implemented specs;
- `accepted/` — принятые и подтверждённые изменения;
- `superseded/` — заменённые контракты;
- `_template/change.md` — обязательный шаблон.

Текущее состояние реализации описывается в `docs/technical/`. Архитектурные причины, которые должны пережить конкретное изменение, выносятся в `docs/decisions/`.

До начала реализации изменения поведения, архитектуры, generated data, dependencies, load order, публичных ID или save/network contract выполнить:

```powershell
.agents/skills/specify-jazz-change/scripts/test-change-spec.ps1 -Path docs/specs/active/<SPEC-ID>.md -Phase Ready
```

Перед приёмкой:

```powershell
.agents/skills/specify-jazz-change/scripts/test-change-spec.ps1 -Path docs/specs/active/<SPEC-ID>.md -Phase Done
```

Существующие `docs/technical/weapons/accuracy-model.md` и `class-roles.md` являются качественными legacy-прототипами спецификаций. Их не дублировать автоматически; перенос выполнить отдельным change set после стабилизации текущей оружейной работы.
