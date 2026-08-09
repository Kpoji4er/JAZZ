# -*- coding: utf-8 -*-
from pathlib import Path
import json

data = Path(
    r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\Ammopics\_gen\ammo_stats_compact.json"
).read_text(encoding="utf-8")
rows = json.loads(data)
cals = sorted({r["cal"] for r in rows})

tsx = f'''import {{
  Callout,
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
  useCanvasState,
}} from "cursor/canvas";

type AmmoRow = {{
  id: string;
  name: string;
  cal: string;
  style: string;
  pen: string;
  penClassAdd: number | null;
  dmg: string;
  grp: string;
  rel: number | null;
  jam: number | null;
  crit: number | null;
  rec: number | null;
  noise: string;
  rng: number | null;
  drop: number | null;
  buck: string;
  eff: string;
  cost: number | null;
  tier: number | null;
  rw: number | null;
  shop: boolean;
}};

const ROWS: AmmoRow[] = {data};

const CALIBERS = {json.dumps(["Все"] + cals, ensure_ascii=False)} as const;

function dash(v: string | number | null | undefined): string {{
  if (v === null || v === undefined || v === "") return "—";
  return String(v);
}}

function jamTone(jam: number | null): "danger" | "warning" | undefined {{
  if (jam == null) return undefined;
  if (jam >= 14) return "danger";
  if (jam >= 6) return "warning";
  return undefined;
}}

export default function AmmoStatsCanvas() {{
  const [cal, setCal] = useCanvasState<string>("cal", "Все");
  const [q, setQ] = useCanvasState<string>("q", " ");

  const filtered = ROWS.filter((r) => {{
    if (cal !== "Все" && r.cal !== cal) return false;
    const needle = q.trim();
    if (needle) {{
      const hay = `${{r.id}} ${{r.name}} ${{r.style}} ${{r.eff}}`.toLowerCase();
      if (!hay.includes(needle.toLowerCase())) return false;
    }}
    return true;
  }});

  const pens = filtered.map((r) => parseFloat(r.pen)).filter((n) => !Number.isNaN(n));
  const jams = filtered.map((r) => r.jam).filter((n): n is number => n != null);
  const shopN = filtered.filter((r) => r.shop).length;
  const anom = filtered.filter((r) => r.penClassAdd != null);

  const headers = [
    "Id",
    "Имя",
    "Калибр",
    "Тип",
    "Pen",
    "Dmg",
    "Grp",
    "Jam%",
    "Crit",
    "Recoil",
    "Rel",
    "Noise",
    "Rng",
    "Drop",
    "Effects",
    "Cost",
    "T",
    "RW",
  ];

  const tableRows = filtered.map((r) => [
    r.id,
    r.name,
    r.cal,
    r.style || "—",
    r.penClassAdd != null ? `${{r.pen}}*` : r.pen,
    dash(r.dmg),
    dash(r.grp),
    r.jam == null ? "—" : String(r.jam),
    r.crit == null ? "—" : `+${{r.crit}}`,
    dash(r.rec),
    dash(r.rel),
    dash(r.noise),
    dash(r.rng),
    dash(r.drop),
    dash(r.eff),
    dash(r.cost),
    dash(r.tier),
    dash(r.rw),
  ]);

  const tones = filtered.map((r) => jamTone(r.jam));

  return (
    <Stack gap={{16}} style={{{{ padding: 16 }}}}>
      <Stack gap={{6}}>
        <H1>JAZZ ammo — статы</H1>
        <Text tone="secondary" size="small">
          Source: InventoryItem/JAZZ_AMMO_*.lua · export docs/tools/_export_ammo_stats.py · Pen =
          FormatAmmoPenetrationDisplay · Jam% = BaseJamChance/10 · Dmg/Grouping = mod_mul÷10 as % or
          mod_add
        </Text>
      </Stack>

      <Grid columns={{4}} gap={{12}}>
        <Stat value={{String(filtered.length)}} label="Строк в фильтре" />
        <Stat
          value={{pens.length ? (pens.reduce((a, b) => a + b, 0) / pens.length).toFixed(2) : "—"}}
          label="Средний Pen"
        />
        <Stat
          value={{jams.length ? Math.max(...jams).toFixed(1) + "%" : "—"}}
          label="Макс Jam%"
          tone={{jams.length && Math.max(...jams) >= 14 ? "danger" : undefined}}
        />
        <Stat value={{`${{shopN}}/${{filtered.length}}`}} label="В Bobby Ray" />
      </Grid>

      <Row gap={{12}} align="center" wrap>
        <Select
          value={{cal}}
          onChange={{setCal}}
          options={{CALIBERS.map((c) => ({{ value: c, label: c }}))}}
        />
        <Select
          value={{q}}
          onChange={{setQ}}
          options={{[
            {{ value: " ", label: "Поиск: все" }},
            {{ value: "Crafted", label: "Crafted" }},
            {{ value: "Poor", label: "Poor / Substandard" }},
            {{ value: "AP", label: "AP в id/имени" }},
            {{ value: "Bleeding", label: "Effect: Bleeding" }},
            {{ value: "MarkedTraccers", label: "Effect: Tracer" }},
          ]}}
        />
        <Pill tone="neutral">{{cal === "Все" ? "все калибры" : cal}}</Pill>
      </Row>

      {{anom.length > 0 ? (
        <Callout tone="warning" title="Аномалия PenetrationClass">
          У {{anom.map((a) => a.id).join(", ")}} задан mod_add на PenetrationClass. UI pen берёт только
          mod_mul (+ PenetrationBonus). Звёздочка у Pen в таблице.
        </Callout>
      ) : null}}

      <H2>Таблица модификаторов</H2>
      <Table
        headers={{headers}}
        rows={{tableRows}}
        rowTone={{tones}}
        striped
        stickyHeader
        framed
        columnAlign={{[
          "left",
          "left",
          "left",
          "left",
          "right",
          "right",
          "right",
          "right",
          "right",
          "right",
          "right",
          "right",
          "right",
          "right",
          "left",
          "right",
          "right",
          "right",
        ]}}
        style={{{{ maxHeight: 560 }}}}
      />

      <Divider />
      <Text tone="tertiary" size="small">
        Пустые ячейки = модификатор не задан (для mul часто ≡ ×1 / 100%). colorStyle сокращён. Не
        включает vanilla _9mm_* stubs. CSV/JSON: Ammopics/_gen/ammo_stats.*
      </Text>
      <Text tone="tertiary" size="small">
        Пересобери экспорт: python docs/tools/_export_ammo_stats.py
      </Text>
    </Stack>
  );
}}
'''

out = Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz\canvases\ammo-stats.canvas.tsx"
)
out.write_text(tsx, encoding="utf-8")
print("wrote", out, "chars", len(tsx))

helper = Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz\canvases\_ammo_stats_data.json"
)
if helper.exists():
    helper.unlink()
