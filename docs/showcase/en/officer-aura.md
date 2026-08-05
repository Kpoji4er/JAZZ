# Command aura

[Overview](home.md) · [Legion units](legion-units.md) · [Perks](perks.md) · [Русский](../ru/officer-aura.md)

In combat, AI officers (Legion, rebels, and similar) show **Command aura**; nearby allies get **Under aura influence**. The tooltip lists the **current order**. You do not pick the order — the officer changes it from the situation.

## Radius

| Officer | Tiles |
| --- | ---: |
| Sergeant / Leader | **15** |
| Lieutenant | **25** |
| Captain / merc captain | **whole map** |

Outside the radius or after the commander dies, influence drops. With several officers, the larger radius wins.

## Orders

| Order | When | What you see |
| --- | --- | --- |
| **Hold the line** | ~13–23 tiles to the enemy | Default squad roles |
| **Push** | enemy ≤ **12** | Scouts press more often |
| **Envelop** | enemy ≥ **24** | Assaults flank more often |
| **Fall back** | heavy squad losses | Hug cover |
| **Focus fire** | visible enemy ≤40% HP | Prefer finishing that target |
| **Occupy buildings** | urban / indoors | Fight from buildings |
| **Take cover** | losing a long-range firefight, no stealth | Cover, no rush |
| **Go hidden** | night/fog **or** long-range fight + stealth | Try to enter **Hidden** |
| **Low visibility — hold** | night/fog without mass stealth | Cautious hold |

No player command button. The officer does not pathfind for everyone — only combat style. MGs/heavies usually keep their own roles.
