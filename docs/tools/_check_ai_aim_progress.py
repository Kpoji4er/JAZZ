"""Bounded Lua 5.3 regression of the actual AICalcAttacksAndAim source.

Requires lupa.lua53. JA3 integer division is reproduced for the two AP divisions.
The Lua instruction hook makes the captured old loop fail instead of hanging.
"""
from pathlib import Path
from lupa.lua53 import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / 'Code/AiActions.lua').read_text(encoding='utf-8')
source = source.split('function AICalcAttacksAndAim(context, ap, target)', 1)[1]
source = 'function AICalcAttacksAndAim(context, ap, target)' + source.split('-- JAZZ-AI-002: Commit', 1)[0]
source = source.replace('ap / ', 'ap // ')
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
Min=math.min; const={Scale={AP=1000}}; NetUpdateHash=function() end
IsKindOfClasses=function() return false end
JazzAI_ContextUsesJazzCombatAI=function(c) return not c.vanilla end
JazzAI_VanillaCalcAttacksAndAim=function() return 7, {3} end
function run_case(maxaim, weaponmax, cth, ap, cost, maxattacks, force, vanilla)
 local unit={GetBaseAimLevelRange=function() return 0,maxaim end,
  CalcChanceToHit=function() return cth end}
 local ctx={unit=unit,weapon={MaxAimActions=weaponmax},default_attack={},
  default_attack_cost=cost,max_attacks=maxattacks,force_max_aim=force,vanilla=vanilla}
 debug.sethook(function() error('instruction budget exhausted') end,'',20000)
 local ok,n,aims=pcall(AICalcAttacksAndAim,ctx,ap,{})
 debug.sethook()
 return ok,n,aims
end
''')
lua.execute(source)
cases = [
    ('captured M1 zero aim', (0, 3, 50, 17480, 10000, 1, False, False), 1, None),
    ('aim cap leaves AP', (2, 3, 50, 17480, 10000, 1, False, False), 1, 2),
    ('CTH already 100', (3, 3, 100, 17480, 10000, 1, False, False), 1, None),
    ('ordinary AP allocation', (3, 3, 50, 14000, 10000, 1, False, False), 1, 3),
    ('multiple attacks capped', (2, 3, 50, 27000, 10000, 2, False, False), 2, 2),
    ('no spare aim AP', (3, 3, 50, 12000, 10000, 1, False, False), 1, None),
    ('zero attack cost guard', (3, 3, 50, 17000, 0, 1, False, False), 1, None),
    ('vanilla delegation', (0, 3, 50, 17480, 10000, 1, False, True), 7, 3),
]
for name, args, expected_n, expected_aim in cases:
    ok, n, aims = lua.globals().run_case(*args)
    assert ok, (name, n)
    assert n == expected_n, (name, n)
    assert (aims[1] or 0) == (expected_aim or 0), (name, aims[1])
    if not args[-1]:
        assert all(0 <= value <= args[0] for _, value in aims.items()), name
    print('PASS', name)

# Demonstrate the test catches the previous implementation's actual failure.
old = source.replace('aim < max_aim', 'aim <= (max_aim)').replace(
    'remaining >= remaining_before', 'remaining >= ap - num_attacks * cost')
lua.execute(old)
ok, error, _ = lua.globals().run_case(*cases[0][1])
assert not ok and 'instruction budget exhausted' in error, error
print('PASS old M1 implementation exceeds instruction budget')
