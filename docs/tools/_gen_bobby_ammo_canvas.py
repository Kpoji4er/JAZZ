# -*- coding: utf-8 -*-
"""Generate canvases/bobby-ray-ammo-prices.canvas.tsx from ammo audit JSON."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / ".tmp/bobby_ammo_prices.json"
OUT = Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz"
    r"\canvases\bobby-ray-ammo-prices.canvas.tsx"
)


def main() -> None:
    rows = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    compact = []
    for r in rows:
        why = r.get("why") or ""
        if len(why) > 100:
            why = why[:97] + "..."
        compact.append(
            [
                r.get("tier") or "—",
                r["name"],
                r["now"],
                r["proposed"],
                r["family"],
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
                r.get("sss") or 0,
                r.get("per_prop") or 0,
                r.get("grade") or "",
            ]
        )

    families = sorted({r["family"] for r in rows})
    n = len(rows)
    bobby = [r for r in rows if r["shop"] == "bobby"]
    out_c = sum(1 for r in rows if r["shop"] == "out_craft")
    out_o = sum(1 for r in rows if r["shop"] == "out_old")
    out_m = sum(1 for r in rows if r["shop"] == "out_mortar")
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
    fam_js = json.dumps(["all"] + families, ensure_ascii=False)
    br_opts = ",\n                  ".join(
        ['{ value: "all", label: "All BR" }']
        + [f'{{ value: "{i}", label: "BR{i}" }}' for i in range(1, br_total + 1)]
    )

    head = '''import {
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
  number,
  number,
  string,
];

const DATA: RowT[] = '''

    body = f""";

const FAMILY_IDS: string[] = {fam_js};
const BR_TOTAL = {br_total};

function fmt(n: number) {{
  return n.toLocaleString("en-US");
}}

export default function BobbyRayAmmoPrices() {{
  const [family, setFamily] = useCanvasState("family", "all");
  const [q, setQ] = useCanvasState("q", "");
  const [shop, setShop] = useCanvasState("shop", "bobby");
  const [brFilter, setBrFilter] = useCanvasState("brFilter", "all");
  const [onlyBig, setOnlyBig] = useCanvasState("onlyBig", "no");

  const filtered = DATA.filter((r) => {{
    if (shop === "bobby" && r[7] !== "bobby") return false;
    if (shop === "out" && r[7] === "bobby") return false;
    if (shop === "need_cas" && r[9] !== "SET_FALSE") return false;
    if (family !== "all" && r[4] !== family) return false;
    if (brFilter !== "all") {{
      const want = Number(brFilter);
      if (r[7] !== "bobby" || r[10] !== want) return false;
    }}
    if (onlyBig === "yes" && Math.abs(r[6]) < 2000) return false;
    if (q) {{
      const s = q.toLowerCase();
      if (!(`${{r[1]}} ${{r[5]}} ${{r[4]}} ${{r[18]}} ${{r[8]}}`).toLowerCase().includes(s))
        return false;
    }}
    return true;
  }});

  const tableRows = filtered.map((r) => {{
    const d = r[6];
    const dStr = d === 0 ? "=" : d > 0 ? `+${{fmt(d)}}` : fmt(d);
    const shopLabel =
      r[7] === "bobby"
        ? "Bobby"
        : r[7] === "out_craft"
          ? "craft"
          : r[7] === "out_old"
            ? "antique"
            : r[7] === "out_mortar"
              ? "mortar"
              : r[7];
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
        r[4],
        r[18] || "—",
        r[1],
        r[5],
        `x${{r[16]}}`,
        fmt(r[2]),
        fmt(r[3]),
        `~${{r[17]}}`,
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
            : Math.abs(d) >= 5000
              ? ("warning" as const)
              : d > 0
                ? ("success" as const)
                : ("neutral" as const),
    }};
  }});

  return (
    <Stack gap={{24}}>
      <Stack gap={{8}}>
        <H1>Ammo prices — Bobby + world</H1>
        <Text tone="secondary">
          Proposed = stack Cost (ShopStackSize pack). Grades: Poor→FMJ→Army→Match/EPR→AP.
          Crafted/mortar/antique 7.92/7.5 French out of Bobby (Cost kept). Soft-tail same as guns.
        </Text>
        <Row gap={{8}} wrap>
          <Pill>total {n}</Pill>
          <Pill tone="info">Bobby {len(bobby)}</Pill>
          <Pill>BR={br_total} ({br_dist_txt})</Pill>
          <Pill>RW: {rarity_txt}</Pill>
          <Pill tone="danger">SET false {set_false}</Pill>
          <Pill>craft {out_c}</Pill>
          <Pill>antique {out_o}</Pill>
          <Pill>mortar {out_m}</Pill>
          <Pill tone="warning">{down} down</Pill>
          <Pill tone="success">{up} up</Pill>
        </Row>
      </Stack>

      <Grid columns={{4}} gap={{12}}>
        <Stat value={{{br_total}}} label="Unlock tiers" tone="info" />
        <Stat value={{{set_false}}} label="Need SET false" tone="danger" />
        <Stat value={{{len(bobby)}}} label="Bobby catalog" />
        <Stat value={{fmt({median_prop})}} label="Median stack $" />
      </Grid>

      <Callout tone="info" title="Ammo restock vs guns">
        Below unlock: weight ×2^(U−T) (cap ×8) + MaxStock boost — more FMJ/JHP packs
        as Bobby tiers up. Above unlock: soft-tail ×0.1^Δ. Poor: ×1 / ×0.35 / ×0.08 /
        then gone at U≥4. Handgun ammo stays T1–T3 when guns exist there.
      </Callout>

      <Card>
        <CardHeader trailing={{<Text tone="secondary">{{filtered.length}} pcs</Text>}}>
          Ammo catalog
        </CardHeader>
        <CardBody>
          <Stack gap={{12}}>
            <Row gap={{12}} wrap>
              <Select
                value={{shop}}
                onChange={{setShop}}
                options={{[
                  {{ value: "all", label: "All" }},
                  {{ value: "bobby", label: "Bobby only" }},
                  {{ value: "out", label: "Out of Bobby" }},
                  {{ value: "need_cas", label: "Need SET false" }},
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
                value={{family}}
                onChange={{setFamily}}
                options={{FAMILY_IDS.map((id) => ({{
                  value: id,
                  label: id === "all" ? "All calibers" : id,
                }}))}}
              />
              <Select
                value={{onlyBig}}
                onChange={{setOnlyBig}}
                options={{[
                  {{ value: "no", label: "Any delta" }},
                  {{ value: "yes", label: "|delta| >= 2k" }},
                ]}}
              />
              <TextInput value={{q}} onChange={{setQ}} placeholder="search" />
            </Row>
            <Table
              headers={{[
                "BR",
                "Cal",
                "Grade",
                "Name",
                "Id",
                "SSS",
                "now $",
                "prop $",
                "$/rd",
                "delta",
                "Shop",
                "Rarity",
                "Why",
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

    OUT.write_text(head + data_js + body, encoding="utf-8")
    print(f"wrote {OUT} bobby={len(bobby)} set_false={set_false} bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
