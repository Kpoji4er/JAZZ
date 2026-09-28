"""Export actual loaded weapon definitions without creating objects or pausing."""
from pathlib import Path
from live import evaluate,quote
root=Path(__file__).resolve().parents[3]
out=root/'docs/design/weapon-layer-icons/live'
body='return assert(load('+quote((Path(__file__).parent/'catalog.lua').read_text())+'))()('+quote((out/'catalog.json').as_posix())+')'
evaluate(body,out/'catalog-dispatch.json')
