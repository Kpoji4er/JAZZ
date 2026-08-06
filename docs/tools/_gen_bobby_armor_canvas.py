# -*- coding: utf-8 -*-
"""Generate canvases/bobby-ray-armor-prices.canvas.tsx from armor audit JSON.

Mirrors _gen_bobby_price_canvas.py structure (known-working weapon canvas).
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / ".tmp/bobby_armor_prices.json"
OUT = Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz"
    r"\canvases\bobby-ray-armor-prices.canvas.tsx"
)


def main() -> None:
    rows = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    # Keep why short — long Cyrillic why-strings bloated the previous canvas.
    compact = []
    for r in rows:
        why = r.get("why") or ""
        if len(why) > 120:
            why = why[:117] + "..."
        compact.append(
            [
                r.get("tier") or "—",
                r["name"],
                r["now"],
                r["proposed"],
                r["slot"],
                r["id"],
                r["delta"],
                r["shop"],
                why,
                r.get("cas_action", "KEEP"),
                r.get("br_tier"),
                r.get("br_tier_now"),
                r.get("br_tier_total", 5),
                r.get("rarity") or "—",
                r.get("rw"),
                r.get("rw_now"),
            ]
        )

    slots = sorted({r["slot"] for r in rows})
    n = len(rows)
    bobby = [r for r in rows if r["shop"] == "bobby"]
    out_l = sum(1 for r in rows if r["shop"] == "out_legion")
    out_s = sum(1 for r in rows if r["shop"] == "out_special")
    set_false = sum(1 for r in rows if r.get("cas_action") == "SET_FALSE")
    down = sum(1 for r in bobby if r["delta"] < 0)
    up = sum(1 for r in bobby if r["delta"] > 0)
    br_total = rows[0].get("br_tier_total", 5) if rows else 5
    br_dist = Counter(r.get("br_tier") for r in bobby if r.get("br_tier"))
    rarity_dist = Counter(r.get("rarity") for r in bobby if r.get("rarity"))
    median_prop = sorted(r["proposed"] for r in rows)[len(rows) // 2] if rows else 0
    br_dist_txt = ", ".join(f"T{k}:{v}" for k, v in sorted(br_dist.items()))
    rarity_txt = ", ".join(f"{k}:{v}" for k, v in rarity_dist.most_common())

    data_js = json.dumps(compact, ensure_ascii=False)
    slot_js = json.dumps(["all"] + slots, ensure_ascii=False)
    br_opts = ",\n                  ".join(
        ['{ value: "all", label: "All BR" }']
        + [f'{{ value: "{i}", label: "BR{i}" }}' for i in range(1, br_total + 1)]
    )

    # Build TSX without nested f-string brace hell for JSX expressions.
    parts = []
    parts.append(
        '''import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  Grid,
  H1,
  Pill,
  Row,
  Select,
  Stack,
  Stat,
  Table,
  Text,
  TextInput,
  useCanvasState,
} from "cursor/canvas";

type RowT = [
  string,
  string,
  number,
  number,
  string,
  string,
  number,
  string,
  string,
  string,
  number | null,
  number | null,
  number,
  string,
  number | null,
  number | null,
];

const DATA: RowT[] = '''
    )
    parts.append(data_js)
    parts.append(
        f""";

const SLOT_IDS: string[] = {slot_js};
const BR_TOTAL = {br_total};

const SLOT_RU: Record<string, string> = {{
  torso: "Жилеты",
  soft: "Софт / форма",
  helm: "Шлемы",
  legs: "Ноги",
  plates: "Плиты",
  nvg: "ПНВ",
  face: "Лицо / маски",
  upgrade: "Апгрейды",
}};

function fmt(n: number) {{
  return n.toLocaleString("en-US");
}}

export default function BobbyRayArmorPrices() {{
  const [slot, setSlot] = useCanvasState("slot", "all");
  const [q, setQ] = useCanvasState("q", "");
  const [shop, setShop] = useCanvasState("shop", "bobby");
  const [brFilter, setBrFilter] = useCanvasState("brFilter", "all");
  const [onlyBig, setOnlyBig] = useCanvasState("onlyBig", "no");

  const filtered = DATA.filter((r) => {{
    if (shop === "bobby" && r[7] !== "bobby") return false;
    if (shop === "out" && r[7] === "bobby") return false;
    if (shop === "legion" && r[7] !== "out_legion") return false;
    if (shop === "need_cas" && r[9] !== "SET_FALSE") return false;
    if (slot !== "all" && r[4] !== slot) return false;
    if (brFilter !== "all") {{
      const want = Number(brFilter);
      if (r[7] !== "bobby" || r[10] !== want) return false;
    }}
    if (onlyBig === "yes" && Math.abs(r[6]) < 5000) return false;
    if (q) {{
      const s = q.toLowerCase();
      if (!(`${{r[1]}} ${{r[5]}} ${{r[0]}} ${{r[8]}}`).toLowerCase().includes(s)) return false;
    }}
    return true;
  }});

  const tableRows = filtered.map((r) => {{
    const d = r[6];
    const dStr = d === 0 ? "=" : d > 0 ? `+${{fmt(d)}}` : fmt(d);
    const shopLabel =
      r[7] === "bobby"
        ? "Bobby"
        : r[7] === "out_legion"
          ? "out legion"
          : "out special";
    const br =
      r[10] == null
        ? "—"
        : `${{r[10]}} / ${{BR_TOTAL}}` +
          (r[11] != null && r[11] !== r[10] ? ` (now ${{r[11]}})` : "");
    const rw =
      r[14] == null
        ? "—"
        : `${{r[13]}} · RW ${{r[14]}}` +
          (r[15] != null && r[15] !== r[14] ? ` (was ${{r[15]}})` : "");
    return {{
      cells: [
        br,
        SLOT_RU[r[4]] || r[4],
        r[1],
        r[5],
        fmt(r[2]),
        r[7] === "bobby" ? fmt(r[3]) : fmt(r[3]),
        dStr,
        shopLabel,
        rw,
        r[8],
      ],
      tone:
        r[9] === "SET_FALSE"
          ? ("danger" as const)
          : r[7] !== "bobby"
            ? ("warning" as const)
            : Math.abs(d) >= 20000
              ? ("warning" as const)
              : d > 0
                ? ("success" as const)
                : ("neutral" as const),
    }};
  }});

  return (
    <Stack gap={{24}}>
      <Stack gap={{8}}>
        <H1>Цены брони — Bobby + мир</H1>
        <Text tone="secondary">
          Proposed = InventoryItem.Cost. Legion-style (шины/кольчуга/рейдер) вне
          витрины, цена для лута/продажи. BR1 flak/софт → BR2 PASGT/Twaron → BR3
          Guardian → BR4 IBA/UHMWPE → BR5 Spectra. Soft-tail как у оружия.
        </Text>
        <Row gap={{8}} wrap>
          <Pill>всего {n}</Pill>
          <Pill tone="info">Bobby {len(bobby)}</Pill>
          <Pill>BR={br_total} ({br_dist_txt})</Pill>
          <Pill>RW: {rarity_txt}</Pill>
          <Pill tone="danger">SET false {set_false}</Pill>
          <Pill>out legion {out_l}</Pill>
          <Pill>out special {out_s}</Pill>
          <Pill tone="warning">{down} down</Pill>
          <Pill tone="success">{up} up</Pill>
        </Row>
      </Stack>

      <Grid columns={{4}} gap={{12}}>
        <Stat value={{{br_total}}} label="Unlock tiers" tone="info" />
        <Stat value={{{set_false}}} label="Нужен SET false" tone="danger" />
        <Stat value={{{len(bobby)}}} label="В каталоге Bobby" />
        <Stat value={{fmt({median_prop})}} label="Медиана Cost" />
      </Grid>

      <Callout tone="info" title="Прогрессия">
        BR1 flak/soft/plates C2 → BR2 PASGT/Twaron/plates C3 → BR3 Guardian/NVG1/plates
        C4 → BR4 IBA/MICH/NVG2/plates C5 → BR5 Spectra/UHMWPE/NVG3.
      </Callout>

      <Card>
        <CardHeader trailing={{<Text tone="secondary">{{filtered.length}} pcs</Text>}}>
          Armor catalog
        </CardHeader>
        <CardBody>
          <Stack gap={{12}}>
            <Row gap={{12}} wrap>
              <Select
                value={{shop}}
                onChange={{setShop}}
                options={{[
                  {{ value: "all", label: "Все" }},
                  {{ value: "bobby", label: "Только Bobby" }},
                  {{ value: "out", label: "Вне Bobby" }},
                  {{ value: "legion", label: "Legion-style" }},
                  {{ value: "need_cas", label: "Нужен SET false" }},
                ]}}
              />
              <Select
                value={{brFilter}}
                onChange={{setBrFilter}}
                options={{[
                  {br_opts}
                ]}}
              />
              <Select
                value={{slot}}
                onChange={{setSlot}}
                options={{SLOT_IDS.map((id) => ({{
                  value: id,
                  label: id === "all" ? "Все слоты" : SLOT_RU[id] || id,
                }}))}}
              />
              <Select
                value={{onlyBig}}
                onChange={{setOnlyBig}}
                options={{[
                  {{ value: "no", label: "Любой delta" }},
                  {{ value: "yes", label: "|delta| >= 5k" }},
                ]}}
              />
              <TextInput value={{q}} onChange={{setQ}} placeholder="поиск" />
            </Row>
            <Table
              headers={{[
                "BR",
                "Слот",
                "Название",
                "Id",
                "now $",
                "proposed $",
                "delta",
                "Shop",
                "Редкость",
                "Почему",
              ]}}
              rows={{tableRows.map((r) => r.cells)}}
              rowTone={{tableRows.map((r) => r.tone)}}
            />
          </Stack>
        </CardBody>
      </Card>
    </Stack>
  );
}}
"""
    )

    tsx = "".join(parts)
    OUT.write_text(tsx, encoding="utf-8")
    print(f"wrote {OUT} bobby={len(bobby)} set_false={set_false} bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
