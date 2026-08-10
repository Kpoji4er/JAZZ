# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("items.lua")
t = p.read_text(encoding="utf-8")
marker = 'unit:SetActionCommand("GrizzlyPerk", self.id, ap, ...)'
idx = t.find(marker)
if idx < 0:
    raise SystemExit("GrizzlyPerk Run not found")
# walk back to dmg_penalty Value -50 inside this CA
chunk_start = t.rfind("PlaceObj('ModItemCombatAction'", 0, idx)
chunk = t[chunk_start:idx]
if "'Name', \"dmg_penalty\",\n\t\t\t\t\t\t\t'Value', -50," not in chunk:
    # try alternate whitespace
    if "'Value', -50," not in chunk or "dmg_penalty" not in chunk:
        raise SystemExit("dmg_penalty -50 not in GrizzlyPerk CA chunk")
old = "'Name', \"dmg_penalty\",\n\t\t\t\t\t\t\t'Value', -50,"
new = "'Name', \"dmg_penalty\",\n\t\t\t\t\t\t\t'Value', 0,"
# replace only within GrizzlyPerk CA: find absolute position
rel = chunk.find(old)
if rel < 0:
    raise SystemExit("exact dmg_penalty pattern missing")
abs_i = chunk_start + rel
t = t[:abs_i] + new + t[abs_i + len(old) :]

# CE description in items (ModItemCharacterEffectCompositeDef GrizzlyPerk)
old_desc = (
    "<em>Сигнатурная пулемётная атака</em> игнорирует штрафы <em>без опоры</em> к точности и отдаче, "
    "даёт <em>вдвое больше пуль</em> и <em>вдвое сильнее подавление</em>, при пониженном уроне и жёстком контроле отдачи. "
    "Обычная очередь пулемёта эти бонусы не получает."
)
new_desc = (
    "<em>Сигнатурная пулемётная атака</em>: вдвое больше пуль, чем у длинной очереди, полный урон, "
    "игнор штрафов <em>без опоры</em> к точности и отдаче, <em>вдвое сильнее подавление</em>. "
    "Обычная очередь пулемёта эти бонусы не получает."
)
if old_desc in t:
    t = t.replace(old_desc, new_desc, 1)
elif new_desc in t:
    pass
else:
    print("WARN: CE description string not found in items.lua")

p.write_text(t, encoding="utf-8", newline="\n")
print("OK: GrizzlyPerk dmg_penalty=0")
