# Чеклисты, Git и проверки

## До реализации: Definition of Ready

1. Для контрактного изменения создать spec в `docs/specs/active/`.
2. Зафиксировать owner, systems, repositories, requirements, invariants, acceptance criteria, write set и exclusive resources.
3. Получить `approved_by` владельца проекта.
4. Запустить `$specify-jazz-change` validator с `-Phase Ready`.
5. Проверить dirty state только в затронутых репозиториях и отсутствие пересекающегося agent claim.

## После реализации: Definition of Done

1. Сопоставить каждый `AC-*` с evidence.
2. Проверить пути и порядок `metadata.lua.code` в затронутых пакетах.
3. Для compatibility-sensitive изменения подтвердить свежий CommonLib snapshot; для dependency/release scope использовать strict dependency audit.
4. Выполнить `git diff --check` в каждом изменённом репозитории.
5. Выполнить профильные static/generated/editor/runtime проверки.
6. Синхронизировать technical current-state docs.
7. Запустить spec validator с `-Phase Done`.
8. Провести независимое conformance review и human acceptance для субъективного/runtime результата.

## Git-границы

- Не включать посторонний dirty state.
- Не смешивать логическую правку и mass regeneration.
- Один агент владеет declared write set; `items.lua`, `metadata.lua`, editor state и release manifest являются exclusive resources.
- Межрепозиторное изменение перечисляет связанные SHA или явно фиксирует незакоммиченное состояние.
- Коммит создавать только по запросу пользователя; заголовок и пояснение — на русском, технические IDs не переводить.
- Любой `git push`, force-push, публикацию тега, GitHub Release или PR выполнять только после отдельного явного одобрения пользователя на конкретную публикацию. Разрешение на commit, merge или перенос изменений между ветками не считается разрешением на push.

## Неполная проверка

Если runtime/editor недоступен, оставить соответствующий `AC-*` как `BLOCKED` и не переводить spec в `implemented`/`accepted`.
