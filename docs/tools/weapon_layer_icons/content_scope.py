"""Share the canonical disabled-weapon filter across capture, gallery and install."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def disabled_ids():
    with (ROOT/'docs/technical/weapons/data/weapons.csv').open(encoding='utf-8-sig',newline='') as f:
        return {r['id'] for r in csv.DictReader(f) if r['catalog_status']=='excluded_disabled'}
