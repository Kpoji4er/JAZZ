# Ownership и эксклюзивные ресурсы

Канонический список ресурсов, которые нельзя одновременно изменять нескольким агентам, находится в `exclusive-resources.yaml`.

Каждая approved spec объявляет:

- затронутые systems и repositories;
- declared write set;
- exclusive resources либо `none`;
- implementer, reviewer и coordinator при необходимости.

File ownership не дублируется вручную здесь: current load-state файлов остаётся в `docs/technical/systems/file-coverage.md`, а package ownership — в `docs/technical/architecture.md`.
