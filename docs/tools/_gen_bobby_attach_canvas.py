# -*- coding: utf-8 -*-
"""Generate bobby-ray-attach-prices.canvas.tsx from .tmp/bobby_attach_prices.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON = ROOT / ".tmp" / "bobby_attach_prices.json"
OUT = (
    Path.home()
    / ".cursor"
    / "projects"
    / "c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz"
    / "canvases"
    / "bobby-ray-attach-prices.canvas.tsx"
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

/** id, display, category, family, shop, Cost_cur, Cost, Tier_cur, Tier, RW, Parts, note */
type RowT = [
  string,
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

const CATS = __CATS__;
const FAMS = __FAMS__;
const GENERATED = __GENERATED__;

function fmt(n: number | null) {
  if (n == null) return "—";
  return n.toLocaleString("en-US");
}

export default function BobbyRayAttachPrices() {
  const [shop, setShop] = useCanvasState("shop", "bobby");
  const [cat, setCat] = useCanvasState("cat", "Optics");
  const [fam, setFam] = useCanvasState("fam", "all");
  const [br, setBr] = useCanvasState("br", "all");
  const [q, setQ] = useCanvasState("q", "");

  const filtered = DATA.filter((r) => {
    if (shop === "bobby" && r[4] !== "bobby") return false;
    if (shop === "out" && !r[4].startsWith("out_")) return false;
    if (shop === "optics" && r[2] !== "Optics") return false;
    if (cat !== "all" && r[2] !== cat) return false;
    if (fam !== "all" && r[3] !== fam) return false;
    if (br !== "all") {
      const want = Number(br);
      if (r[8] !== want) return false;
    }
    if (q) {
      const s = q.toLowerCase();
      if (!(`${r[0]} ${r[1]} ${r[11]}`).toLowerCase().includes(s)) return false;
    }
    return true;
  });

  const bobby = DATA.filter((r) => r[4] === "bobby").length;
  const optics = DATA.filter((r) => r[2] === "Optics" && r[4] === "bobby").length;
  const outN = DATA.filter((r) => r[4].startsWith("out_")).length;

  return (
    <Stack gap={16}>
      <H1>Bobby Ray — weapon attachments (optics+)</H1>
      <Callout tone="info">
        Soft-tail. BR = max(design, earliest Bobby host gun). Cold War optics out.
        12× BR4; Eotech BR4. Cost=Parts×100. Default filter: Optics. Source:
        _audit_bobby_attach_prices.py · {GENERATED}
      </Callout>
      <Grid columns={4} gap={12}>
        <Stat value={String(bobby)} label="In Bobby" />
        <Stat value={String(optics)} label="Optics in Bobby" />
        <Stat value={String(outN)} label="Out / skip" />
        <Stat value={String(filtered.length)} label="Filtered rows" />
      </Grid>
      <Row gap={8} align="center">
        <Select
          value={shop}
          onChange={setShop}
          options={[
            { value: "bobby", label: "Bobby only" },
            { value: "optics", label: "All Optics (incl out)" },
            { value: "out", label: "Out only" },
            { value: "all", label: "All" },
          ]}
        />
        <Select
          value={cat}
          onChange={setCat}
          options={CATS.map((c) => ({ value: c, label: c === "all" ? "All categories" : c }))}
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
            { value: "5", label: "BR5" },
          ]}
        />
        <TextInput value={q} onChange={setQ} placeholder="Filter id/name…" />
      </Row>
      <Card>
        <CardHeader>Catalog ({filtered.length})</CardHeader>
        <CardBody>
          <Table
            headers={["Id", "Name", "Cat", "Fam", "Shop", "Cost", "BR", "RW", "Parts", "Note"]}
            rows={filtered.map((r) => {
              const dlt = (r[6] ?? 0) - (r[5] ?? 0);
              const costStr =
                r[5] != null && r[6] != null && r[5] !== r[6]
                  ? `${fmt(r[5])}→${fmt(r[6])}`
                  : fmt(r[6] ?? r[5]);
              const tierStr =
                r[7] != null && r[8] != null && r[7] !== r[8]
                  ? `${r[7]}→${r[8]}`
                  : r[8] != null
                    ? String(r[8])
                    : "—";
              return [
                r[0],
                r[1],
                r[2],
                r[3],
                <Pill
                  tone={
                    r[4] === "bobby"
                      ? "success"
                      : r[4].startsWith("out_")
                        ? "warning"
                        : "neutral"
                  }
                >
                  {r[4] === "bobby" ? "Bobby" : r[4].replace("out_", "")}
                </Pill>,
                costStr + (dlt ? ` (${dlt > 0 ? "+" : ""}${dlt})` : ""),
                tierStr,
                fmt(r[9]),
                fmt(r[10]),
                r[11],
              ];
            })}
          />
        </CardBody>
      </Card>
      <Text tone="secondary" size="small">
        Heuristic BR for non-optics by Parts band. Underslung GL / irons / G36 integral → out.
        New BobbyRayShopSubCategory ids should match CategoryPair (like Ammo calibers).
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
            r.get("category") or "",
            r.get("family") or "",
            r.get("shop") or "",
            r.get("Cost_cur"),
            r.get("Cost"),
            r.get("Tier_cur"),
            r.get("Tier"),
            r.get("RestockWeight"),
            r.get("Parts"),
            (r.get("note") or "")[:80],
        ]
        data_lines.append("  " + json.dumps(vals, ensure_ascii=False) + ",")

    cats = sorted({r.get("category") or "" for r in rows if r.get("category")})
    fams = sorted({r.get("family") or "" for r in rows if r.get("family")})
    footer = (
        FOOTER.replace("__CATS__", json.dumps(["all"] + cats, ensure_ascii=False))
        .replace("__FAMS__", json.dumps(["all"] + fams, ensure_ascii=False))
        .replace("__GENERATED__", json.dumps(d.get("generated", ""), ensure_ascii=False))
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(HEADER + "\n".join(data_lines) + footer, encoding="utf-8", newline="\n")
    print(f"wrote {OUT} rows={len(rows)}")


if __name__ == "__main__":
    main()
