# Пять кустарных броней: проверка 3 октября 2026

После обновления ресурсов запустить игру заново через Steam. В тестовом списке юнитов искать ID, группа **JAZZ Tests**; отображаемое имя — «Новобранец».

| Броня | UnitData ID | Модель |
| --- | --- | --- |
| Кираса | `JAZZ_Legion_ArmorTest` | Сохранённая игровая кираса |
| Кольчуга | `JAZZ_Legion_ArmorTest_Chainmail` | Body v5, 22 272 tri с телом |
| Бригантина | `JAZZ_Legion_ArmorTest_TireBrigantine` | Meshy, 18 000 tri |
| Шинная броня | `JAZZ_Legion_ArmorTest_TireArmor` | Meshy, 18 000 tri |
| Кожаный жилет | `JAZZ_Legion_ArmorTest_LeatherArmor` | Meshy, 18 000 tri |

Все пять: LegionGoon, MP40 и 120 FMJ, броня в Torso; вне боевых пулов кампании. Иконка кольчуги восстановлена из ae4e775a, характеристики прежние. Три новых Armor надеваются поверх штатного верха; кольчуга заменяет root Body и включает торс/руки/шею.

Проверить спереди/сзади/сбоку, idle, бег, прицеливание стоя/сидя/лёжа. У кольчуги — горловину, рукава, неподвижность верхних наплечников относительно торса, возврат прежней одежды при снятии и после save/load. У остальных — лямки, плечи, пояс и спинку на Shirt08. Синтетические позы и compiled geometry/skin PASS не заменяют игровые анимации.

Исходники в sibling jazz_assets/Sources/Character/JAZZ_<item>_Male/meshy-20261003; кольчуга — JAZZ_Chainmail_Male/meshy-body-v5-20261003. Сохранены source blends, pose/compiled reports, рендеры и installation.json с backup. Материалы 2K Base/Norm/RM, у кольчуги также C1 Color. RM: R=G roughness, B metallic.

Прежняя майка оставалась из-за ошибочного parts.Body, который не заменял root entity и отсутствует в animated_parts JA3. Live DAP подтвердил это на unit 2000000084. После исправления root стал JAZZ_Chainmail_Male, Body/Armor attachments отсутствовали, idle сохранился. Финальная версия после изменения плеч и торса ещё требует игровой приёмки.
