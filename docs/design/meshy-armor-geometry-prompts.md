# Промпты объёмной брони для Meshy

Подготовлено 2026-10-02 после боковых рендеров первой партии. Владелец разрешил один text-to-3d preview кольчуги без текстур; остальные новые генерации не запускались.

`image-to-3d` принимает изображение и `texture_prompt`, но не документирует текстовый prompt для геометрии. Нельзя обещать исправление плоского жилета через `texture_prompt`. Промпты ниже предназначены для `text-to-3d`, `mode=preview`: сначала проверка геометрии без текстур. Это другой вход: точное совпадение с исходной иконкой не гарантируется. Если обязательно сохранить оригинальный дизайн, требуется подготовить по оригиналу согласованные объёмные ракурсы и передать их в `multi-image-to-3d`; такую подготовку согласовать отдельно.

Официальные контракты: [Image to 3D](https://docs.meshy.ai/en/api/image-to-3d), [Text to 3D](https://docs.meshy.ai/en/api/text-to-3d). API документирует 800 символов, но CLI 0.4.0 указывает 600; исполняемый промпт кольчуги укладывается в 600. Остальные черновики перед запуском сократить. Промпт повышает определённость задания, но не заменяет боковую и заднюю проверку.

## Chainmail

```text
Wearable chainmail armor for an adult male video game character, standalone equipment for later skeletal rigging. Full 3D hollow torso volume with distinct curved chest and back joined at shoulders and sides. Open neck, waist and armholes; short sleeves angled outward for arm movement. Two steel breast plates, shoulder guards, leather belt and one front groin plate. Plain mail back, no rear breast plates. Real material thickness, clearance over a shirt. No character, mannequin, pedestal, frame or background. Not a flat icon, plaque or relief.
```

## TireBrigantine

```text
A complete wearable improvised tire brigantine vest, modeled fully in the round around an EMPTY adult male torso cavity. Horizontal curved strips of truck tire rubber wrap the chest, flanks and back. Brown riveted leather vertical straps hold the strips; a central front buckle secures the harness. Small shoulder guards. Front and back are physically separated by realistic torso depth and joined at shoulders and sides. Open neck, open waist and two open armholes, clear interior cavity. The rear has its own simpler rubber strip construction rather than a copy of the front buckle. Thick rubber edges and attached rivets. Armor alone, no person, mannequin, display board, rectangle or background mesh. A volumetric wearable object, never a flat icon or relief.
```

## LeatherArmor

```text
A wearable improvised leather breastplate harness modeled fully in the round. Rounded convex chest panel with a double stitched rim and a closed plate pocket; two broad leather shoulder straps curve over the shoulders to a small separate back panel. Two buckled side straps on each flank connect the chest to the back at realistic male torso depth. All straps visibly meet their attachment points. EMPTY torso cavity, open sides between straps, open neck, open waist, open armholes. Thick dark leather, rough repair patch and metal rivets. The rear is a small leather panel, not a duplicate breastplate. Standalone armor only: no body, mannequin, pedestal, rectangular frame, display card or background geometry. Never flatten the harness into a plaque or bas-relief.
```

## Приёмка перед текстурированием

Рендеры спереди, сзади, сбоку и в три четверти. Проверить объём под грудную клетку, самостоятельную спину, отверстия для рук/шеи/талии, физическую толщину, контакты ремней и отсутствие фоновой рамки. При FAIL не запускать refine и не делать платный повтор автоматически. Точная посадка под JA3 проверяется уже на отдельном этапе импорта.

## Проверенный результат Chainmail

Text preview `01a0f98e-cf42-77e9-b51d-221a9ee684c3` завершён: 20 кредитов, 15330 треугольников, один меш без скелета. По четырём ракурсам объём появился, но генератор добавил человеческую голову, руки и части тела вопреки явному No character, mannequin. Художественная приёмка FAIL: это не отдельная надеваемая броня. Текстурирование и следующие платные попытки не запускались. Формулировка «для игрового персонажа» сама по себе не обеспечивает отделение снаряжения от тела. Результаты: `meshy_output/chainmail-game-armor-20261002/20261002_012142_chainmail-game-armor_01a0f98e/`.
