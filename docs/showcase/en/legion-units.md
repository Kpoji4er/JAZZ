# Legion units

[Overview](home.md) · [Legion strategy](legion-strategy.md) · [Ernie campaign](ernie-campaign.md) · [Русский](../ru/legion-units.md)

## Two difficulty axes

Legion difficulty in JAZZ has **two independent** scales:

1. **Unit class T1–T4** — who is in the squad (stats, role, AI, root preset). A living fighter does **not** morph into the next class mid-fight; spawns simply use a higher UnitData ID.
2. **Campaign gear tier** (`JAZZ_Legion_Tier`) — which weapon/armor/ammo pool generation may roll. It rises with **your** sector count; when the tier changes, Legion gear can regenerate.

Satellite squad roles (garrison, patrol, QRF…) are separate: [Legion strategy](legion-strategy.md).

## Families (38 classes)

Six lines plus a Recruit for the recruiter flow:

| Family | From → to (example names) | Role |
| --- | --- | --- |
| Assault | Roughneck → … → Headsman | Stormer / demolitions |
| Front | Rifleman → … → Mercenary / Mercenary Sniper | Marksman / soldier / medic |
| Flanker | Warden → … → Ranger | Recon |
| Gunner | Gunner → … → Merc Gunner | Heavy MG |
| Leader | Sergeant → … → Mercenary Captain | Commander (officer density in squads) |
| Heavy | Rocketeer → Grenadier → Mortarman | Artillery |

### Assault names (RU display)

T1 Головорез / Гренадёр / Громила → T2 Грабитель / Штурмовик / Пироман → T3 Каратель / Череполом → T4 Палач.

### Front

T1 Стрелок / Костоправ / Мародёр → T2 Засадник / Налётчик / Охотник → T3 Снайпер / Ветеран → T4 Наемник / Наемник снайпер.

### Flanker

T1 Дозорный → T2 Скаут / Застрельщик → T3 Разведчик / Следопыт → T4 Рейнджер.

### Gunner

T1 Пуляло → T2 Пулемётчик / Коммандо → T3 Подавитель → T4 Наемник Пулеметчик.

### Leaders

Бригадир → Командир → Советник → Мастер. Strategic T4 squads need a **MercenaryCaptain**; officers land by density (about Sergeant/8, Lieutenant/15–20, Captain/30 troops).

### Artillery

Ракетчик → Гранатомётчик → Миномётчик.

## Gear tier by sectors

Equipment tier starts at **11**, then by sectors you control:

| Your sectors | Tier |
| ---: | ---: |
| 0–1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4–8 | 21…25 |
| 9+ | 31…33 |

Higher tier → nastier allowed loot on newly rolled / regenerated Legionnaires. A T1 class with a high gear tier is still a “Roughneck” — with meaner kit.

## Strategic $ scale

Generator ballpark per head: line **500 / 1000 / 2000 / 3500**, specialist **800 / 1500 / 2800 / 4500**, leader **800 / 1500 / 2500 / 4000** across T1–T4.
