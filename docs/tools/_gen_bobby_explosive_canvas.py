# -*- coding: utf-8 -*-
"""Generate bobby-ray-explosive-prices.canvas.tsx from .tmp/bobby_explosive_prices.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON = ROOT / ".tmp" / "bobby_explosive_prices.json"
OUT = (
    Path.home()
    / ".cursor"
    / "projects"
    / "c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz"
    / "canvases"
    / "bobby-ray-explosive-prices.canvas.tsx"
)

HEADER = r'''import {
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

/** id, display, family, shop, Cost_cur, Cost, Tier_cur, Tier, RW, MaxStock, note */
type RowT = [
  string,
  string,
  string,
  string,
  number | null,
  number | null,
  number | null,
  number | null,
  number | null,
  number | null,
  string,
];

const DATA: RowT[] = [
'''

FOOTER = r'''
];

const FAMS = __FAMS__;
const GENERATED = __GENERATED__;

function fmt(n: number | null) {
  if (n == null) return "—";
  return n.toLocaleString("en-US");
}

export default function BobbyRayExplosivePrices() {
  const [shop, setShop] = useCanvasState("shop", "bobby");
  const [fam, setFam] = useCanvasState("fam", "all");
  const [br, setBr] = useCanvasState("br", "all");
  const [q, setQ] = useCanvasState("q", "");

  const filtered = DATA.filter((r) => {
    if (shop === "bobby" && r[3] !== "bobby") return false;
    if (shop === "cross" && !r[3].startsWith("cross_")) return false;
    if (shop === "out" && !r[3].startsWith("out_")) return false;
    if (fam !== "all" && r[2] !== fam) return false;
    if (br !== "all") {
      const want = Number(br);
      if (r[7] !== want) return false;
    }
    if (q) {
      const s = q.toLowerCase();
      if (!(`${r[0]} ${r[1]} ${r[10]}`).toLowerCase().includes(s)) return false;
    }
    return true;
  });

  const bobby = DATA.filter((r) => r[3] === "bobby").length;
  const cross = DATA.filter((r) => r[3].startsWith("cross_")).length;
  const outN = DATA.filter((r) => r[3].startsWith("out_")).length;

  return (
    <Stack gap={16}>
      <H1>Bobby Ray — explosives / grenades / demo</H1>
      <Callout tone="info">
        Soft-tail like guns. TNT BR1 · C4 BR2 · PETN BR3 · fused MaxStock1 · grenades BR1–2.
        BlackPowder = consumables flat. 40mm/mortar = ammo audit. Source:
        _audit_bobby_explosive_prices.py · {GENERATED}
      </Callout>
      <Grid columns={4} gap={12}>
        <Stat value={String(bobby)} label="In Bobby" />
        <Stat value={String(cross)} label="Cross-ref" />
        <Stat value={String(outN)} label="Out" />
        <Stat value={String(filtered.length)} label="Filtered" />
      </Grid>
      <Row gap={8} align="center">
        <Select
          value={shop}
          onChange={setShop}
          options={[
            { value: "bobby", label: "Bobby only" },
            { value: "cross", label: "Cross-ref" },
            { value: "out", label: "Out" },
            { value: "all", label: "All" },
          ]}
        />
        <Select
          value={fam}
          onChange={setFam}
          options={FAMS.map((f) => ({ value: f, label: f === "all" ? "All families" : f }))}
        />
        <Select
          value={br}
          onChange={setBr}
          options={[
            { value: "all", label: "All BR" },
            { value: "1", label: "BR1" },
            { value: "2", label: "BR2" },
            { value: "3", label: "BR3" },
            { value: "4", label: "BR4" },
          ]}
        />
        <TextInput value={q} onChange={setQ} placeholder="Filter…" />
      </Row>
      <Card>
        <CardHeader>Catalog ({filtered.length})</CardHeader>
        <CardBody>
          <Table
            headers={["Id", "Name", "Fam", "Shop", "Cost", "BR", "RW", "Max", "Note"]}
            rows={filtered.map((r) => {
              const costStr =
                r[4] != null && r[5] != null && r[4] !== r[5]
                  ? `${fmt(r[4])}→${fmt(r[5])}`
                  : fmt(r[5] ?? r[4]);
              const tierStr =
                r[6] != null && r[7] != null && r[6] !== r[7]
                  ? `${r[6]}→${r[7]}`
                  : r[7] != null
                    ? String(r[7])
                    : "—";
              const tone =
                r[3] === "bobby"
                  ? "success"
                  : r[3].startsWith("cross_")
                    ? "info"
                    : "warning";
              return [
                r[0],
                r[1],
                r[2],
                <Pill tone={tone}>
                  {r[3] === "bobby" ? "Bobby" : r[3].replace(/^(out_|cross_)/, "")}
                </Pill>,
                costStr,
                tierStr,
                fmt(r[8]),
                fmt(r[9]),
                r[10],
              ];
            })}
          />
        </CardBody>
      </Card>
      <Text tone="secondary" size="small">
        Proposed only — no mass apply yet. Owner OK 2026-08-07 (PipeBomb/ShapedCharge out; Smoke BR1; rest kept).
      </Text>
    </Stack>
  );
}
'''


def main() -> None:
    d = json.loads(JSON.read_text(encoding="utf-8"))
    rows = d["rows"]
    data_lines = []
    for r in rows:
        vals = [
            r["id"],
            r.get("display") or r["id"],
            r.get("family") or "",
            r.get("shop") or "",
            r.get("Cost_cur"),
            r.get("Cost"),
            r.get("Tier_cur"),
            r.get("Tier"),
            r.get("RestockWeight"),
            r.get("MaxStock"),
            (r.get("note") or "")[:90],
        ]
        data_lines.append("  " + json.dumps(vals, ensure_ascii=False) + ",")
    fams = sorted({r.get("family") or "" for r in rows if r.get("family")})
    footer = (
        FOOTER.replace("__FAMS__", json.dumps(["all"] + fams, ensure_ascii=False))
        .replace("__GENERATED__", json.dumps(d.get("generated", ""), ensure_ascii=False))
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(HEADER + "\n".join(data_lines) + footer, encoding="utf-8", newline="\n")
    print(f"wrote {OUT} rows={len(rows)}")


if __name__ == "__main__":
    main()
