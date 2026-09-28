# Повторение съёмки

Требуется уже запущенная через Steam debug-игра, DAP на 8165, изолированная карта ModEditor и согласованное исключительное владение камерой. Не запускать одновременно с другой съёмкой, reload, игрой владельца или отладкой боя. Скрипт не вызывает initialize, pause, запуск или остановку игры. Python: Pillow, numpy; offline-проверка resolver дополнительно требует lupa.

Пути в командах — из корня jazz. Выход всегда в новый staging-каталог. Нельзя подставлять активный Mods каталог.

```powershell
python docs/tools/weapon_layer_icons/export_catalog.py
python docs/tools/weapon_layer_icons/dispatch_capture.py --output docs/design/weapon-layer-icons/live/production-capture --catalog docs/design/weapon-layer-icons/live/catalog.json --matte --variants all
```

Dispatch возвращается сразу. Дождаться `capture-report.json: phase=done` и `dispatch.result.txt: OK / capture complete`; `running` не является успехом. Отчёт обновляется после каждого кадра. Во время съёмки не запускать второй batch. При неожиданном сбое смотреть error/rows, не повторять вслепую большой batch и не убивать процесс игры: сначала выяснить, восстановилась ли сцена.

После завершения:

```powershell
python docs/tools/weapon_layer_icons/process_live.py --catalog docs/design/weapon-layer-icons/live/catalog.json --captures docs/design/weapon-layer-icons/live/production-capture --output docs/design/weapon-layer-icons/live/staged
python docs/tools/weapon_layer_icons/survey_names.py --catalog docs/design/weapon-layer-icons/live/catalog.json --manifest docs/design/weapon-layer-icons/live/staged/manifest.json --output docs/design/weapon-layer-icons/live/staged
python docs/tools/weapon_layer_icons/live_gallery.py --staged docs/design/weapon-layer-icons/live/staged
python docs/tools/weapon_layer_icons/verify_live.py --catalog docs/design/weapon-layer-icons/live/catalog.json --staged docs/design/weapon-layer-icons/live/staged --captures docs/design/weapon-layer-icons/live/production-capture
```

Для пересъёмки креплений использовать `--ids M4A1 AK74 ... --variants Scope Side Handguard`, новый output и текущий исправленный capture.lua (его receipt — `consistency-capture/capture-source.lua`). Не брать ранние pilot sources. У `process_live.py --profile-manifest <старый manifest>` сохраняет кадрирование исходного выпуска. При нескольких `--captures` более поздний источник заменяет совпадающий `(class,label)`; не смешивать разные light recipes в одном выпуске. Большие семейства переснимать целиком с `--distance 2100`; Side/Under M4/M16 требуют `--prerequisite Handguard=JAZZ_Handguard_RIS --label-prefix RIS__`.

Проверка файлов не заменяет просмотр: открыть `staged/sheets`, проверить дефекты посадки, максимальные габариты и видимость чёрных деталей на обоих фонах. `verify_live.py` проверяет полное single-slot покрытие; для заведомо частичного переснятого набора использовать объединённый manifest с предыдущим выпуском. Крепления provisional до отдельной приёмки геометрии.

`production-capture` здесь означает финальный проход съёмки, **не установку в production**. Никаких ModItem, metadata, игровых иконок или CSV локализации эти инструменты не изменяют.
