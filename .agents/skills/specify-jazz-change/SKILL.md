---
name: specify-jazz-change
description: Создавать и проверять change specification, Definition of Ready, Definition of Done и evidence для изменений JAZZ. Использовать до реализации нового поведения, изменения архитектуры, публичных ID, формул, generated data, dependencies, load order, save/network contract или межпакетных связей; также использовать при изменении уже утверждённого scope. Не требуется для чистого read-only анализа и тривиальной правки документации, не меняющей контракт.
---

# Спецификация изменения JAZZ

Не начинать реализацию контрактного изменения без утверждённой спецификации из `docs/specs/active/`.

## Рабочий цикл

1. Скопировать `docs/specs/_template/change.md` в `docs/specs/active/<SPEC-ID>.md`.
2. Заполнить problem, goals, non-goals, requirements, invariants, acceptance criteria, impact, ownership и declared write set.
3. Назначить стабильные `REQ-*` и `AC-*`. Не кодировать номер строки или имя агента в ID.
4. Зафиксировать exclusive resources: `items.lua`, `metadata.lua`, editor state, localization ID range, map или release manifest.
5. Получить решение владельца проекта и установить `status: approved`.
6. Запустить:

   ```powershell
   .agents/skills/specify-jazz-change/scripts/test-change-spec.ps1 -Path docs/specs/active/<SPEC-ID>.md -Phase Ready
   ```

7. Реализовывать только утверждённый scope. Для нового требования сначала обновить spec и повторить DoR.
8. В разделе evidence сопоставить каждый `AC-*` с результатом `PASS`, `FAIL` или `BLOCKED` и указать уровень проверки: static, editor, runtime или human.
9. Перед завершением установить `status: implemented` и выполнить `-Phase Done`.
10. После независимого ревью и human acceptance установить `status: accepted` и перенести spec в `docs/specs/accepted/`.

## Границы

- `docs/specs/` описывает требуемое или утверждённое поведение.
- `docs/technical/` описывает фактически загруженное текущее состояние.
- `docs/decisions/` хранит долгоживущие архитектурные решения и причины.
- Не выдавать approved spec за реализованную механику.
- Не закрывать `AC-*` статическим анализом, если spec требует editor/runtime/human evidence.
- Не разрешать двум агентам пересекающийся write set или один exclusive resource.

Полный контракт полей и lifecycle читать в [change-spec-contract.md](references/change-spec-contract.md).
