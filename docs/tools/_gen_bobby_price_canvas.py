# -*- coding: utf-8 -*-
"""Generate canvases/bobby-ray-weapon-prices.canvas.tsx from audit JSON."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / ".tmp/bobby_weapon_prices.json"
OUT = Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz"
    r"\canvases\bobby-ray-weapon-prices.canvas.tsx"
)


def main() -> None:
    rows = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    # tier, name, now, realism, proposed, family, id, delta, shop, why,
    # cas_action, cas_label, br_tier, br_tier_now, br_total, rarity, rw, rw_now
    compact = [
        [
            r["tier"],
            r["name"],
            r["now"],
            r["realism"],
            r["proposed"],
            r["family"],
            r["id"],
            r["delta"],
            r["shop"],
            r["why"],
            r.get("cas_action", "keep"),
            r.get("cas_label", ""),
            r.get("br_tier"),
            r.get("br_tier_now"),
            r.get("br_tier_total", 5),
            r.get("rarity") or "—",
            r.get("rw"),
            r.get("rw_now"),
        ]
        for r in rows
    ]
    families = sorted({r["family"] for r in rows})
    n = len(rows)
    bobby = [r for r in rows if r["shop"] == "bobby"]
    out_u = sum(1 for r in rows if r["shop"] == "out_unique")
    out_o = sum(1 for r in rows if r["shop"] == "out_old")
    set_false = sum(1 for r in rows if r.get("cas_action") == "SET_FALSE")
    down = sum(1 for r in bobby if r["delta"] < 0)
    up = sum(1 for r in bobby if r["delta"] > 0)
    br_total = rows[0].get("br_tier_total", 5) if rows else 5
    from collections import Counter

    br_dist = Counter(r.get("br_tier") for r in bobby if r.get("br_tier"))
    rarity_dist = Counter(r.get("rarity") for r in bobby if r.get("rarity"))
    median_now = sorted(r["now"] for r in rows)[len(rows) // 2] if rows else 0
    median_prop = sorted(r["proposed"] for r in rows)[len(rows) // 2] if rows else 0
    br_dist_txt = ", ".join(f"T{k}:{v}" for k, v in sorted(br_dist.items()))
    rarity_txt = ", ".join(f"{k}:{v}" for k, v in rarity_dist.most_common())

    data_js = json.dumps(compact, ensure_ascii=False)
    fam_js = json.dumps(["all"] + families, ensure_ascii=False)

    tsx = f'''import {{
  Callout,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Grid,
  H1,
  H2,
  Pill,
  Row,
  Select,
  Stack,
  Stat,
  Table,
  Text,
  TextInput,
  useCanvasState,
}} from "cursor/canvas";

type RowT = [
  string,
  string,
  number,
  number,
  number,
  string,
  string,
  number,
  string,
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

const DATA: RowT[] = {data_js};

const FAMILY_IDS: string[] = {fam_js};
const BR_TOTAL = {br_total};

const FAMILY_RU: Record<string, string> = {{
  pistol: "Пистолеты",
  autopistol: "Автопистолеты",
  revolver: "Револьверы",
  "submachine-gun": "ПП",
  shotgun: "Дробовики",
  carbine: "Карабины",
  "assault-rifle": "Штурмовые",
  "battle-rifle": "Боевые винтовки",
  "sniper-rifle": "Снайперские",
  "light-machine-gun": "Лёгкие пулемёты",
  "machine-gun": "Пулемёты",
  "grenade-launcher": "Гранатомёты",
  "rocket-launcher": "РПГ / LAW",
}};

function fmt(n: number) {{
  return n.toLocaleString("en-US");
}}

export default function BobbyRayWeaponPrices() {{
  const [family, setFamily] = useCanvasState("family", "all");
  const [q, setQ] = useCanvasState("q", "");
  const [shop, setShop] = useCanvasState("shop", "all");
  const [brFilter, setBrFilter] = useCanvasState("brFilter", "all");
  const [rarityFilter, setRarityFilter] = useCanvasState("rarityFilter", "all");
  const [onlyBig, setOnlyBig] = useCanvasState("onlyBig", "no");

  const filtered = DATA.filter((r) => {{
    if (shop === "bobby" && r[8] !== "bobby") return false;
    if (shop === "out" && r[8] === "bobby") return false;
    if (shop === "need_cas" && r[10] !== "SET_FALSE") return false;
    if (family !== "all" && r[5] !== family) return false;
    if (brFilter !== "all") {{
      const want = Number(brFilter);
      if (r[12] !== want) return false;
    }}
    if (rarityFilter !== "all" && r[15] !== rarityFilter) return false;
    if (onlyBig === "yes" && Math.abs(r[7]) < 10000) return false;
    if (q) {{
      const s = q.toLowerCase();
      if (
        !(`${{r[1]}} ${{r[6]}} ${{r[0]}} ${{r[9]}} ${{r[11]}} ${{r[15]}}`.toLowerCase().includes(s))
      )
        return false;
    }}
    return true;
  }});

  const tableRows = filtered.map((r) => {{
    const d = r[7];
    const dStr = d === 0 ? "=" : d > 0 ? `+${{fmt(d)}}` : fmt(d);
    const shopLabel =
      r[8] === "bobby" ? "Bobby" : r[8] === "out_unique" ? "out UNIQ" : "out ~2005";
    const propCell = r[8] === "bobby" ? fmt(r[4]) : "—";
    const brProp = r[12] == null ? "—" : String(r[12]);
    const brNow = r[13] == null ? "unset" : String(r[13]);
    const brCell = r[8] === "bobby" ? `${{brProp}} / ${{BR_TOTAL}} (now ${{brNow}})` : "—";
    const rwProp = r[16] == null ? "—" : String(r[16]);
    const rwNow = r[17] == null ? "unset→100" : String(r[17]);
    const rareCell =
      r[8] === "bobby" ? `${{r[15]}} · RW ${{rwProp}} (now ${{rwNow}})` : "—";
    return {{
      cells: [
        r[0],
        r[1],
        r[6],
        brCell,
        rareCell,
        fmt(r[2]),
        `$${{fmt(r[3])}}`,
        propCell,
        dStr,
        shopLabel,
        r[11] || "",
        r[9],
      ],
      tone:
        r[10] === "SET_FALSE"
          ? ("danger" as const)
          : r[8] !== "bobby"
            ? ("warning" as const)
            : r[16] != null && r[16] <= 20
              ? ("info" as const)
              : r[12] != null && r[13] != null && r[12] !== r[13]
                ? ("info" as const)
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
        <H1>Цены оружия — Bobby + мир</H1>
        <Text tone="secondary">
          Proposed = InventoryItem.Cost для всех стволов: Bobby buy и позже world
          buy/sell (порт/NPC). Вне магазина (unique / ~2005) — только не в витрине
          Bobby, цена всё равно нужна. BR unlock: 1-*→1; 2-1..2-2→2; 2-3..2-4→3;
          2-5→4; 3-1..3-2→4; 3-3+→5. Quest unlock сейчас 1–3.
        </Text>
        <Row gap={{8}} wrap>
          <Pill>всего {n}</Pill>
          <Pill tone="info">Bobby {len(bobby)}</Pill>
          <Pill>BR={br_total} ({br_dist_txt})</Pill>
          <Pill>RW: {rarity_txt}</Pill>
          <Pill tone="danger">SET false {set_false}</Pill>
          <Pill>out unique {out_u}</Pill>
          <Pill>out ~2005 {out_o}</Pill>
          <Pill tone="warning">{down} ↓</Pill>
          <Pill tone="success">{up} ↑</Pill>
        </Row>
      </Stack>

      <Grid columns={{4}} gap={{12}}>
        <Stat value={{{br_total}}} label="Unlock tiers всего" tone="info" />
        <Stat value={{{set_false}}} label="Нужен SET false" tone="danger" />
        <Stat value={{{len(bobby)}}} label="В каталоге Bobby" />
        <Stat value={{fmt({median_prop})}} label="Медиана Cost (все)" />
      </Grid>

      <Callout tone="info" title="Джекпот-хвост (T > U)">
        Без потолка по Δ: AN94 (BR5) может теоретически висеть уже при U=1 —
        вес ×0.1^4 (≈0.01% от RW; в пуле ~0.001%-класс), цена ×81 (~4.5M при
        Cost 55k). Нормальный ассортимент — T==U; хвост не ломает прогрессию.
      </Callout>

      <Callout tone="info" title="Редкость = RestockWeight">
        Выше RW — чаще выпадает при restock (vanilla default 100). Шкала: ≤8 очень
        редко · ≤20 редко · ≤45 нечасто · ≤90 обычно · ≤120 часто · выше очень часто.
        Welrod/DeLisle/Абакан вручную низкие; AK/Type56/Makarov — высокие.
      </Callout>

      <Callout tone="warning" title="CanAppearInShop / ~2005">
        В Bobby: P38, Thompson, M1897, BAR, Winchester1894, Stoeger; Welrod/DeLisle
        редко+дорого (BR4); Абакан BR5 конец. Вне: StG, Luger, MP40, MAT-49, Auto5,
        Garand, квест-уники, PB/RSH12… Пистолеты: band/overrides ↓.
      </Callout>

      <Card>
        <CardHeader trailing={{<Text tone="secondary">{{filtered.length}} шт.</Text>}}>
          Каталог
        </CardHeader>
        <CardBody>
          <Stack gap={{12}}>
            <Row gap={{12}} wrap>
              <Select
                value={{shop}}
                onChange={{setShop}}
                options={{[
                  {{ value: "bobby", label: "Только Bobby" }},
                  {{ value: "need_cas", label: "Нужен SET false" }},
                  {{ value: "out", label: "Все вне Bobby" }},
                  {{ value: "all", label: "Все стволы" }},
                ]}}
              />
              <Select
                value={{brFilter}}
                onChange={{setBrFilter}}
                options={{[
                  {{ value: "all", label: "Все BR tiers" }},
                  ...[1, 2, 3, 4, 5].map((t) => ({{
                    value: String(t),
                    label: `BR ${{t}}`,
                  }})),
                ]}}
              />
              <Select
                value={{rarityFilter}}
                onChange={{setRarityFilter}}
                options={{[
                  {{ value: "all", label: "Вся редкость" }},
                  {{ value: "очень часто", label: "очень часто" }},
                  {{ value: "часто", label: "часто" }},
                  {{ value: "обычно", label: "обычно" }},
                  {{ value: "нечасто", label: "нечасто" }},
                  {{ value: "редко", label: "редко" }},
                  {{ value: "очень редко", label: "очень редко" }},
                ]}}
              />
              <Select
                value={{family}}
                onChange={{setFamily}}
                options={{FAMILY_IDS.map((id) => ({{
                  value: id,
                  label: id === "all" ? "Все семейства" : FAMILY_RU[id] || id,
                }}))}}
              />
              <TextInput
                value={{q}}
                onChange={{setQ}}
                placeholder="имя / id / почему"
              />
              <Select
                value={{onlyBig}}
                onChange={{setOnlyBig}}
                options={{[
                  {{ value: "no", label: "Все дельты" }},
                  {{ value: "yes", label: "|delta| >= 10k" }},
                ]}}
              />
            </Row>
            <Table
              headers={{[
                "Weapon tier",
                "Оружие",
                "Id",
                "BR tier",
                "Редкость",
                "Сейчас $",
                "Реализм",
                "Proposed $",
                "Δ",
                "Shop",
                "CanAppearInShop",
                "Почему",
              ]}}
              columnAlign={{[
                "left",
                "left",
                "left",
                "left",
                "left",
                "right",
                "right",
                "right",
                "right",
                "left",
                "left",
                "left",
              ]}}
              rows={{tableRows.map((r) => r.cells)}}
              rowTone={{tableRows.map((r) => r.tone)}}
            />
          </Stack>
        </CardBody>
      </Card>

      <Divider />

      <Stack gap={{8}}>
        <H2>Медиана Cost (все стволы)</H2>
        <Text>
          now {median_now} · proposed {median_prop} · Bobby BR dist {br_dist_txt}
        </Text>
      </Stack>
    </Stack>
  );
}}
'''
    # Fix accidental double-brace issues in map template - the f-string above has
    # `...[1, 2, 3, 4, 5].map((t) => ({{` which is correct for JS object in f-string.
    OUT.write_text(tsx, encoding="utf-8")
    print("wrote", OUT, "bobby", len(bobby), "SET_FALSE", set_false, "BR", br_total, br_dist_txt, "|", rarity_txt)


if __name__ == "__main__":
    main()
