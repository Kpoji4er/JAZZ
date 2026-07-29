import { execFileSync } from "node:child_process";
import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync,
} from "node:fs";
import { basename, dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const rootDir = resolve(scriptDir, "..", "..");
const dataDir = join(rootDir, "docs", "technical", "weapons", "data");
const wikiDir = join(rootDir, "docs", "wiki", "weapons");
const wikiDirEn = join(wikiDir, "en");

const familyDefinitions = {
  Pistol: { id: "pistol", title_ru: "Пистолеты", title_en: "Pistols", order: 10 },
  Autopistol: {
    id: "autopistol",
    title_ru: "Автоматические пистолеты",
    title_en: "Autopistols",
    order: 20,
  },
  Revolver: { id: "revolver", title_ru: "Револьверы", title_en: "Revolvers", order: 30 },
  SubmachineGun: {
    id: "submachine-gun",
    title_ru: "Пистолеты-пулемёты",
    title_en: "Submachine guns",
    order: 40,
  },
  Carbine: { id: "carbine", title_ru: "Карабины", title_en: "Carbines", order: 50 },
  AssaultRifle: {
    id: "assault-rifle",
    title_ru: "Штурмовые винтовки",
    title_en: "Assault rifles",
    order: 60,
  },
  BattleRifle: {
    id: "battle-rifle",
    title_ru: "Боевые винтовки",
    title_en: "Battle rifles",
    order: 70,
  },
  SniperRifle: {
    id: "sniper-rifle",
    title_ru: "Снайперские винтовки",
    title_en: "Sniper rifles",
    order: 80,
  },
  LightMachineGun: {
    id: "light-machine-gun",
    title_ru: "Ручные пулемёты",
    title_en: "Light machine guns",
    order: 90,
  },
  MachineGun: { id: "machine-gun", title_ru: "Пулемёты", title_en: "Machine guns", order: 100 },
  Shotgun: { id: "shotgun", title_ru: "Дробовики", title_en: "Shotguns", order: 110 },
};

function familyTitle(family, lang) {
  return lang === "en" ? family.title_en : family.title_ru;
}

function hasCyrillic(text) {
  return /[\u0400-\u04FF]/.test(String(text ?? ""));
}

function localizedLabel(ruName, id, lang) {
  if (lang !== "en") return ruName || id;
  if (!ruName) return id;
  if (!hasCyrillic(ruName)) return ruName;
  return id;
}

const defaults = {
  AimAccuracy: 2,
  AutoShots: 10,
  BaseJamChance: 0,
  BurstShots: 3,
  Cost: 1000,
  CritChanceScaled: 10,
  Cumbersome: 0,
  DegradePerShot: 1,
  Damage: 0,
  Grouping: 0,
  HandSlot: "OneHanded",
  Handling: 0,
  LargeItem: 0,
  MagazineSize: 1,
  MaxAimActions: 3,
  Noise: 20,
  ObjDamageMod: 100,
  OverwatchAngle: 2400,
  PenetrationBonus: 0,
  PenetrationClass: 1,
  ReloadAP: 1000,
  Reliability: 40,
  RepairCost: 80,
  Recoil: 100,
  ShootAP: 1000,
  WeaponRange: 20,
  WeaponResource: 1000,
  WeaponResourceMax: -1,
};

const weaponColumns = [
  "id",
  "display_name",
  "family_id",
  "family_name_ru",
  "object_class",
  "catalog_status",
  "balance_tier",
  "balance_subtier",
  "tier_label",
  "tier_status",
  "tier_source",
  "code_tier_label",
  "engine_tier",
  "caliber",
  "damage",
  "obj_damage_mod",
  "penetration_class",
  "penetration_bonus",
  "crit_chance_scaled",
  "magazine_size",
  "shoot_ap",
  "reload_ap",
  "max_aim_actions",
  "aim_accuracy",
  "burst_shots",
  "auto_shots",
  "recoil",
  "weapon_range",
  "bullet_drop_range",
  "grouping",
  "handling",
  "overwatch_angle",
  "noise",
  "reliability",
  "base_jam_chance",
  "weapon_resource",
  "weapon_resource_max",
  "degrade_per_shot",
  "hand_slot",
  "holster_slot",
  "large_item",
  "cumbersome",
  "cost",
  "scrap_parts",
  "repair_cost",
  "available_attacks",
  "component_slot_count",
  "component_option_count",
  "defaulted_fields",
  "source_file",
  "snapshot_commit",
];

const optionColumns = [
  "weapon_id",
  "slot_index",
  "slot_type",
  "modifiable",
  "can_be_empty",
  "default_component",
  "default_in_options",
  "option_index",
  "component_id",
  "component_name",
  "component_source",
  "is_default",
  "source_file",
  "snapshot_commit",
];

const componentColumns = [
  "component_id",
  "display_name",
  "slot",
  "cost",
  "modification_difficulty",
  "effects",
  "parameters",
  "additional_costs",
  "group",
  "used_by_count",
  "source",
  "snapshot_commit",
];

const effectColumns = [
  "effect_id",
  "display_name",
  "description",
  "parameters",
  "source",
  "snapshot_commit",
];

function git(args) {
  return execFileSync("git", args, {
    cwd: rootDir,
    encoding: "utf8",
    maxBuffer: 128 * 1024 * 1024,
  }).replace(/\r\n/g, "\n");
}

function luaUnescape(value) {
  return value
    .replace(/\\\\/g, "\\")
    .replace(/\\"/g, '"')
    .replace(/\\n/g, "\n")
    .replace(/\\r/g, "\r")
    .replace(/\\t/g, "\t");
}

function quotedStrings(text) {
  const values = [];
  const pattern = /"((?:\\.|[^"\\])*)"/g;
  for (const match of text.matchAll(pattern)) {
    values.push(luaUnescape(match[1]));
  }
  return values;
}

function parseLuaScalar(raw) {
  const value = raw.trim().replace(/,\s*$/, "");
  if (value === "true") return true;
  if (value === "false") return false;
  if (value === "nil") return "";
  if (/^-?\d+(?:\.\d+)?$/.test(value)) return Number(value);
  if (value.startsWith('"')) return quotedStrings(value)[0] ?? "";
  return "";
}

function scalarField(text, key, exactTopLevel = false) {
  const pattern = exactTopLevel
    ? new RegExp(`^\\t${key}\\s*=\\s*(.+),\\s*$`, "m")
    : new RegExp(`^(\\s+)${key}\\s*=\\s*(.+),\\s*$`, "gm");

  if (exactTopLevel) {
    const match = text.match(pattern);
    return match ? parseLuaScalar(match[1]) : undefined;
  }

  const matches = [...text.matchAll(pattern)];
  if (matches.length === 0) return undefined;
  matches.sort((a, b) => a[1].length - b[1].length);
  return parseLuaScalar(matches[0][2]);
}

function translatedField(text, key, exactTopLevel = false) {
  const pattern = exactTopLevel
    ? new RegExp(`^\\t${key}\\s*=\\s*(.+)$`, "m")
    : new RegExp(`^(\\s+)${key}\\s*=\\s*(.+)$`, "gm");

  const matches = exactTopLevel ? [text.match(pattern)].filter(Boolean) : [...text.matchAll(pattern)];
  if (matches.length === 0) return "";
  if (!exactTopLevel) matches.sort((a, b) => a[1].length - b[1].length);
  const line = matches[0][exactTopLevel ? 1 : 2];
  const values = quotedStrings(line);
  return values.at(-1) ?? "";
}

function findMatchingBrace(text, openIndex) {
  let depth = 0;
  let quote = "";
  let escaped = false;
  let lineComment = false;

  for (let index = openIndex; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (lineComment) {
      if (char === "\n") lineComment = false;
      continue;
    }
    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (char === "\\") {
        escaped = true;
      } else if (char === quote) {
        quote = "";
      }
      continue;
    }
    if (char === "-" && next === "-") {
      lineComment = true;
      index += 1;
      continue;
    }
    if (char === '"' || char === "'") {
      quote = char;
      continue;
    }
    if (char === "{") depth += 1;
    if (char === "}") {
      depth -= 1;
      if (depth === 0) return index;
    }
  }
  throw new Error(`Unmatched brace at offset ${openIndex}`);
}

function arrayField(text, key, exactTopLevel = false) {
  const pattern = exactTopLevel
    ? new RegExp(`^\\t${key}\\s*=\\s*\\{`, "m")
    : new RegExp(`^(\\s+)${key}\\s*=\\s*\\{`, "gm");
  const matches = exactTopLevel ? [pattern.exec(text)].filter(Boolean) : [...text.matchAll(pattern)];
  if (matches.length === 0) return [];
  if (!exactTopLevel) matches.sort((a, b) => a[1].length - b[1].length);
  const selected = matches[0];
  const openIndex = text.indexOf("{", selected.index);
  const closeIndex = findMatchingBrace(text, openIndex);
  return quotedStrings(text.slice(openIndex + 1, closeIndex));
}

function pairScalarField(text, key) {
  const pattern = new RegExp(
    `['"]${key}['"]\\s*,\\s*("(?:\\\\.|[^"\\\\])*"|-?\\d+(?:\\.\\d+)?|true|false|nil)\\s*,`,
  );
  const match = text.match(pattern);
  return match ? parseLuaScalar(match[1]) : undefined;
}

function pairArrayField(text, key) {
  const pattern = new RegExp(`['"]${key}['"]\\s*,\\s*\\{`);
  const match = pattern.exec(text);
  if (!match) return [];
  const openIndex = text.indexOf("{", match.index);
  const closeIndex = findMatchingBrace(text, openIndex);
  return quotedStrings(text.slice(openIndex + 1, closeIndex));
}

function blockField(text, key, exactTopLevel = false) {
  const pattern = exactTopLevel
    ? new RegExp(`^\\t${key}\\s*=\\s*\\{`, "m")
    : new RegExp(`^(\\s+)${key}\\s*=\\s*\\{`, "gm");
  const matches = exactTopLevel ? [pattern.exec(text)].filter(Boolean) : [...text.matchAll(pattern)];
  if (matches.length === 0) return "";
  if (!exactTopLevel) matches.sort((a, b) => a[1].length - b[1].length);
  const selected = matches[0];
  const openIndex = text.indexOf("{", selected.index);
  const closeIndex = findMatchingBrace(text, openIndex);
  return text.slice(openIndex + 1, closeIndex);
}

function placeObjectBlocks(text, className) {
  const blocks = [];
  const needles = [`PlaceObj('${className}', {`, `PlaceObj("${className}", {`];
  let cursor = 0;

  while (cursor < text.length) {
    const candidates = needles
      .map((needle) => ({ needle, index: text.indexOf(needle, cursor) }))
      .filter((candidate) => candidate.index >= 0)
      .sort((a, b) => a.index - b.index);
    if (candidates.length === 0) break;
    const found = candidates[0];
    const openIndex = text.indexOf("{", found.index);
    const closeIndex = findMatchingBrace(text, openIndex);
    blocks.push(text.slice(found.index, closeIndex + 1));
    cursor = closeIndex + 1;
  }
  return blocks;
}

function parameterPairs(text) {
  const parameters = [];
  for (const block of [
    ...placeObjectBlocks(text, "PresetParamNumber"),
    ...placeObjectBlocks(text, "PresetParamPercent"),
    ...placeObjectBlocks(text, "PresetParamText"),
  ]) {
    const nameMatch = block.match(/['"]Name['"]\s*,\s*"((?:\\.|[^"\\])*)"/);
    const valueMatch = block.match(/['"]Value['"]\s*,\s*([^,\n}]+)/);
    if (!nameMatch) continue;
    const rawValue = valueMatch ? parseLuaScalar(valueMatch[1]) : "";
    parameters.push(`${luaUnescape(nameMatch[1])}=${rawValue}`);
  }
  return parameters;
}

function additionalCosts(text) {
  return placeObjectBlocks(text, "WeaponComponentCost").map((block) => {
    const typeMatch = block.match(/['"]Type['"]\s*,\s*"((?:\\.|[^"\\])*)"/);
    const amountMatch = block.match(/['"]Amount['"]\s*,\s*(-?\d+(?:\.\d+)?)/);
    const type = typeMatch ? luaUnescape(typeMatch[1]) : "unknown";
    const amount = amountMatch ? amountMatch[1] : "1";
    return `${type}=${amount}`;
  });
}

function fieldWithDefault(text, key, defaulted) {
  const explicit = scalarField(text, key, true);
  if (explicit !== undefined) return explicit;
  if (Object.hasOwn(defaults, key)) {
    defaulted.push(key);
    return defaults[key];
  }
  return "";
}

function parseTier(text) {
  const comment = scalarField(text, "comment", true);
  const match = typeof comment === "string" ? comment.match(/^Tier\s+(\d+)-(.+)$/) : null;
  if (!match) {
    return {
      balanceTier: "",
      balanceSubtier: "",
      tierLabel: "",
      tierStatus: "unassigned",
    };
  }
  return {
    balanceTier: Number(match[1]),
    balanceSubtier: match[2],
    tierLabel: `${match[1]}-${match[2]}`,
    tierStatus: match[2] === "UNIQ" ? "unique" : "assigned",
  };
}

function parseSlots(text) {
  const componentSlots = blockField(text, "ComponentSlots", true);
  if (!componentSlots) return [];
  return placeObjectBlocks(componentSlots, "WeaponComponentSlot").map((block, slotIndex) => {
    const options = pairArrayField(block, "AvailableComponents");
    const defaultComponent = pairScalarField(block, "DefaultComponent") ?? "";
    return {
      slotIndex: slotIndex + 1,
      slotType: pairScalarField(block, "SlotType") ?? "",
      modifiable: pairScalarField(block, "Modifiable") ?? true,
      canBeEmpty: pairScalarField(block, "CanBeEmpty") ?? false,
      defaultComponent,
      defaultInOptions: defaultComponent === "" || options.includes(defaultComponent),
      options,
    };
  });
}

function parseComponents(itemsText, commit, className = "ModItemWeaponComponent", source = "jazz") {
  const components = new Map();
  for (const block of placeObjectBlocks(itemsText, className)) {
    const id = scalarField(block, "id");
    if (!id) continue;
    components.set(id, {
      component_id: id,
      display_name: translatedField(block, "DisplayName") || id,
      slot: scalarField(block, "Slot") ?? "",
      cost: scalarField(block, "Cost") ?? 0,
      modification_difficulty: scalarField(block, "ModificationDifficulty") ?? 0,
      effects: arrayField(block, "ModificationEffects").join(";"),
      parameters: parameterPairs(blockField(block, "Parameters")).join(";"),
      additional_costs: additionalCosts(blockField(block, "AdditionalCosts")).join(";"),
      group: scalarField(block, "group") ?? "",
      used_by_count: 0,
      source,
      snapshot_commit: commit,
    });
  }
  return components;
}

function parseEffects(itemsText, commit) {
  const effects = [];
  for (const block of placeObjectBlocks(itemsText, "ModItemWeaponComponentEffect")) {
    const id = scalarField(block, "id");
    if (!id) continue;
    effects.push({
      effect_id: id,
      display_name: translatedField(block, "DisplayName") || id,
      description: translatedField(block, "Description"),
      parameters: parameterPairs(blockField(block, "Parameters")).join(";"),
      source: "jazz",
      snapshot_commit: commit,
    });
  }
  return effects.sort((a, b) => a.effect_id.localeCompare(b.effect_id, "en"));
}

function csvCell(value) {
  const text = value === null || value === undefined ? "" : String(value);
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

function serializeCsv(columns, rows) {
  return [
    columns.join(","),
    ...rows.map((row) => columns.map((column) => csvCell(row[column])).join(",")),
    "",
  ].join("\n");
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') {
        value += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        value += char;
      }
    } else if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(value);
      value = "";
    } else if (char === "\n") {
      row.push(value.replace(/\r$/, ""));
      if (row.some((cell) => cell !== "")) rows.push(row);
      row = [];
      value = "";
    } else {
      value += char;
    }
  }
  if (value !== "" || row.length > 0) {
    row.push(value);
    rows.push(row);
  }
  if (rows.length === 0) return [];
  const headers = rows[0];
  return rows.slice(1).map((values) =>
    Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ""])),
  );
}

function ensureParent(path) {
  mkdirSync(dirname(path), { recursive: true });
}

function writeUtf8(path, content) {
  ensureParent(path);
  writeFileSync(path, content.replace(/\r\n/g, "\n"), "utf8");
}

function tierSort(a, b) {
  const tierA = a.balance_tier === "" ? Number.POSITIVE_INFINITY : Number(a.balance_tier);
  const tierB = b.balance_tier === "" ? Number.POSITIVE_INFINITY : Number(b.balance_tier);
  if (tierA !== tierB) return tierA - tierB;
  const subA = /^\d+$/.test(a.balance_subtier) ? Number(a.balance_subtier) : Number.POSITIVE_INFINITY;
  const subB = /^\d+$/.test(b.balance_subtier) ? Number(b.balance_subtier) : Number.POSITIVE_INFINITY;
  if (subA !== subB) return subA - subB;
  return a.display_name.localeCompare(b.display_name, "ru");
}

function applyTierMigration(weapons) {
  const migrationPath = join(dataDir, "tier-migration.csv");
  if (!existsSync(migrationPath)) return { mapped: 0, planned: [] };
  const rows = parseCsv(readFileSync(migrationPath, "utf8"));
  const byId = new Map(rows.filter((row) => row.weapon_id).map((row) => [row.weapon_id, row]));
  const planned = rows.filter((row) => row.migration_status === "not_in_runtime");
  let mapped = 0;

  for (const weapon of weapons) {
    if (weapon.catalog_status !== "active") {
      weapon.balance_tier = "";
      weapon.balance_subtier = "";
      weapon.tier_label = "";
      weapon.tier_status = "excluded";
      weapon.tier_source = "excluded_disabled";
      continue;
    }
    const row = byId.get(weapon.id);
    if (!row) {
      weapon.balance_tier = "";
      weapon.balance_subtier = "";
      weapon.tier_label = "";
      weapon.tier_status = "unassigned";
      weapon.tier_source = "";
      continue;
    }
    const match = row.tier_label.match(/^(\d+)-(.+)$/);
    if (match) {
      weapon.balance_tier = Number(match[1]);
      weapon.balance_subtier = match[2];
      weapon.tier_label = row.tier_label;
      weapon.tier_status = match[2] === "UNIQ" ? "unique" : "assigned";
    } else {
      weapon.balance_tier = "";
      weapon.balance_subtier = "";
      weapon.tier_label = "";
      weapon.tier_status = "unassigned";
    }
    weapon.tier_source = `google_sheet:${row.sheet_tab}`;
    mapped += 1;
  }

  return { mapped, planned };
}
function importFromGit() {
  const force = process.argv.includes("--force");
  const commitArg = process.argv.find((argument) => argument.startsWith("--commit="));
  const commit = git(["rev-parse", commitArg ? commitArg.slice("--commit=".length) : "HEAD"]).trim();
  const target = join(dataDir, "weapons.csv");
  if (existsSync(target) && !force) {
    throw new Error(
      `${relative(rootDir, target)} already exists. The docs are authoritative; use --force only for an intentional full re-bootstrap.`,
    );
  }

  const itemsText = git(["show", `${commit}:items.lua`]);
  const components = parseComponents(itemsText, commit);
  const vanillaComponentPath =
    process.env.JA3_WEAPON_COMPONENTS_PATH ??
    (process.env.JA3_ROOT
      ? join(
          process.env.JA3_ROOT,
          "ModTools",
          "Src",
          "Data",
          "WeaponComponentSharedClass.lua",
        )
      : undefined);
  if (!vanillaComponentPath || !existsSync(vanillaComponentPath)) {
    throw new Error(
      "Set JA3_ROOT or JA3_WEAPON_COMPONENTS_PATH to the installed WeaponComponentSharedClass.lua before import.",
    );
  }
  const vanillaComponents = parseComponents(
    readFileSync(vanillaComponentPath, "utf8"),
    commit,
    "WeaponComponent",
    "vanilla_233360",
  );
  const effects = parseEffects(itemsText, commit);
  const files = git(["ls-tree", "-r", "--name-only", commit, "InventoryItem"])
    .split("\n")
    .filter((path) => path.endsWith(".lua"));

  const weapons = [];
  const optionRows = [];
  const componentUsers = new Map();

  for (const sourceFile of files) {
    const text = git(["show", `${commit}:${sourceFile}`]);
    const objectClass = scalarField(text, "object_class", true);
    const family = familyDefinitions[objectClass];
    if (!family) continue;

    const id = basename(sourceFile, ".lua");
    const tier = parseTier(text);
    const slots = parseSlots(text);
    const defaulted = [];
    const attacks = arrayField(text, "AvailableAttacks", true);
    const optionCount = slots.reduce((sum, slot) => sum + slot.options.length, 0);

    const weapon = {
      id,
      display_name: translatedField(text, "DisplayName", true) || id,
      family_id: family.id,
      family_name_ru: family.title_ru,
      object_class: objectClass,
      catalog_status: (translatedField(text, "DisplayName", true) || id).trim() === "\u041e\u0422\u041a\u041b\u042e\u0427\u0415\u041d\u041e" ? "excluded_disabled" : "active",
      balance_tier: tier.balanceTier,
      balance_subtier: tier.balanceSubtier,
      tier_label: tier.tierLabel,
      tier_status: tier.tierStatus,
      tier_source: tier.tierLabel ? "code_comment" : "",
      code_tier_label: tier.tierLabel,
      engine_tier: scalarField(text, "Tier", true) ?? "",
      caliber: scalarField(text, "Caliber", true) ?? "",
      damage: fieldWithDefault(text, "Damage", defaulted),
      obj_damage_mod: fieldWithDefault(text, "ObjDamageMod", defaulted),
      penetration_class: fieldWithDefault(text, "PenetrationClass", defaulted),
      penetration_bonus: fieldWithDefault(text, "PenetrationBonus", defaulted),
      crit_chance_scaled: fieldWithDefault(text, "CritChanceScaled", defaulted),
      magazine_size: fieldWithDefault(text, "MagazineSize", defaulted),
      shoot_ap: fieldWithDefault(text, "ShootAP", defaulted),
      reload_ap: fieldWithDefault(text, "ReloadAP", defaulted),
      max_aim_actions: fieldWithDefault(text, "MaxAimActions", defaulted),
      aim_accuracy: fieldWithDefault(text, "AimAccuracy", defaulted),
      burst_shots: fieldWithDefault(text, "BurstShots", defaulted),
      auto_shots: fieldWithDefault(text, "AutoShots", defaulted),
      recoil: fieldWithDefault(text, "Recoil", defaulted),
      weapon_range: fieldWithDefault(text, "WeaponRange", defaulted),
      bullet_drop_range: fieldWithDefault(text, "BulletDropRange", defaulted),
      grouping: fieldWithDefault(text, "Grouping", defaulted),
      handling: fieldWithDefault(text, "Handling", defaulted),
      overwatch_angle: fieldWithDefault(text, "OverwatchAngle", defaulted),
      noise: fieldWithDefault(text, "Noise", defaulted),
      reliability: fieldWithDefault(text, "Reliability", defaulted),
      base_jam_chance: fieldWithDefault(text, "BaseJamChance", defaulted),
      weapon_resource: fieldWithDefault(text, "WeaponResource", defaulted),
      weapon_resource_max: fieldWithDefault(text, "WeaponResourceMax", defaulted),
      degrade_per_shot: fieldWithDefault(text, "DegradePerShot", defaulted),
      hand_slot: fieldWithDefault(text, "HandSlot", defaulted),
      holster_slot: scalarField(text, "HolsterSlot", true) ?? "",
      large_item: fieldWithDefault(text, "LargeItem", defaulted),
      cumbersome: fieldWithDefault(text, "Cumbersome", defaulted),
      cost: fieldWithDefault(text, "Cost", defaulted),
      scrap_parts: scalarField(text, "ScrapParts", true) ?? "",
      repair_cost: fieldWithDefault(text, "RepairCost", defaulted),
      available_attacks: attacks.join(";"),
      component_slot_count: slots.length,
      component_option_count: optionCount,
      defaulted_fields: defaulted.sort().join(";"),
      source_file: sourceFile,
      snapshot_commit: commit,
    };
    weapons.push(weapon);

    for (const slot of slots) {
      const options = slot.options.length > 0 ? slot.options : [""];
      options.forEach((componentId, optionIndex) => {
        let component = components.get(componentId);
        if (!component && componentId && vanillaComponents.has(componentId)) {
          component = vanillaComponents.get(componentId);
          components.set(componentId, component);
        }
        optionRows.push({
          weapon_id: id,
          slot_index: slot.slotIndex,
          slot_type: slot.slotType,
          modifiable: slot.modifiable,
          can_be_empty: slot.canBeEmpty,
          default_component: slot.defaultComponent,
          default_in_options: slot.defaultInOptions,
          option_index: optionIndex + 1,
          component_id: componentId,
          component_name: component?.display_name ?? componentId,
          component_source: component?.source ?? (componentId ? "unresolved" : ""),
          is_default: componentId !== "" && componentId === slot.defaultComponent,
          source_file: sourceFile,
          snapshot_commit: commit,
        });
        if (componentId) {
          if (!componentUsers.has(componentId)) componentUsers.set(componentId, new Set());
          componentUsers.get(componentId).add(id);
        }
      });
    }
  }

  const tierMigration = applyTierMigration(weapons);

  weapons.sort((a, b) => {
    const familyDelta =
      familyDefinitions[a.object_class].order - familyDefinitions[b.object_class].order;
    return familyDelta || tierSort(a, b);
  });
  optionRows.sort(
    (a, b) =>
      a.weapon_id.localeCompare(b.weapon_id, "en") ||
      Number(a.slot_index) - Number(b.slot_index) ||
      Number(a.option_index) - Number(b.option_index),
  );

  const componentRows = [...components.values()]
    .map((component) => ({
      ...component,
      used_by_count: componentUsers.get(component.component_id)?.size ?? 0,
    }))
    .sort((a, b) => a.component_id.localeCompare(b.component_id, "en"));

  mkdirSync(dataDir, { recursive: true });
  writeUtf8(join(dataDir, "weapons.csv"), serializeCsv(weaponColumns, weapons));
  writeUtf8(
    join(dataDir, "weapon-component-options.csv"),
    serializeCsv(optionColumns, optionRows),
  );
  writeUtf8(
    join(dataDir, "weapon-components.csv"),
    serializeCsv(componentColumns, componentRows),
  );
  writeUtf8(
    join(dataDir, "weapon-component-effects.csv"),
    serializeCsv(effectColumns, effects),
  );

  console.log(
    `Imported ${weapons.length} weapons, ${optionRows.length} component options, ${componentRows.length} components and ${effects.length} effects from ${commit}; overlaid ${tierMigration.mapped} sheet tier rows and retained ${tierMigration.planned.length} planned rows.`,
  );
}

function readCanonicalData() {
  const paths = {
    weapons: join(dataDir, "weapons.csv"),
    options: join(dataDir, "weapon-component-options.csv"),
    components: join(dataDir, "weapon-components.csv"),
    effects: join(dataDir, "weapon-component-effects.csv"),
  };
  for (const path of Object.values(paths)) {
    if (!existsSync(path)) throw new Error(`Missing canonical data file: ${relative(rootDir, path)}`);
  }
  return {
    weapons: parseCsv(readFileSync(paths.weapons, "utf8")),
    options: parseCsv(readFileSync(paths.options, "utf8")),
    components: parseCsv(readFileSync(paths.components, "utf8")),
    effects: parseCsv(readFileSync(paths.effects, "utf8")),
  };
}

function validateCanonicalData(data) {
  const errors = [];
  const ids = new Set();
  for (const weapon of data.weapons) {
    if (!weapon.id) errors.push("Weapon row without id");
    if (ids.has(weapon.id)) errors.push(`Duplicate weapon id: ${weapon.id}`);
    ids.add(weapon.id);
    if (!familyDefinitions[weapon.object_class]) {
      errors.push(`${weapon.id}: unknown object_class ${weapon.object_class}`);
    }
    if (!weapon.display_name) errors.push(`${weapon.id}: missing display_name`);
    if (!["unassigned", "excluded"].includes(weapon.tier_status) && !weapon.balance_tier) {
      errors.push(`${weapon.id}: assigned tier without balance_tier`);
    }
  }

  const componentIds = new Set(data.components.map((component) => component.component_id));
  for (const option of data.options) {
    if (!ids.has(option.weapon_id)) {
      errors.push(`Component option references unknown weapon: ${option.weapon_id}`);
    }
    if (option.component_source === "jazz" && !componentIds.has(option.component_id)) {
      errors.push(`${option.weapon_id}: missing JAZZ component ${option.component_id}`);
    }
  }

  const invalidDefaults = new Set(
    data.options
      .filter(
        (option) =>
          option.default_component &&
          option.default_in_options !== "true" &&
          option.default_in_options !== "1",
      )
      .map(
        (option) =>
          `${option.weapon_id}/${option.slot_type}: ${option.default_component}`,
      ),
  );

  if (errors.length > 0) {
    throw new Error(`Canonical weapon data is invalid:\n- ${errors.join("\n- ")}`);
  }
  return { invalidDefaults: [...invalidDefaults].sort() };
}

function mdCell(value) {
  const text = value === "" || value === undefined ? "—" : String(value);
  return text.replace(/\|/g, "\\|").replace(/\r?\n/g, "<br>");
}

function ap(value) {
  if (value === "") return "—";
  const number = Number(value) / 1000;
  return Number.isInteger(number) ? String(number) : number.toFixed(1).replace(/\.0$/, "");
}

function angle(value) {
  if (value === "") return "—";
  const number = Number(value) / 60;
  return Number.isInteger(number) ? `${number}°` : `${number.toFixed(1)}°`;
}

function attackModes(weapon, lang = "ru") {
  const attacks = weapon.available_attacks.split(";").filter(Boolean);
  const modes = [];
  if (lang === "en") {
    if (attacks.includes("SingleShot")) modes.push("single");
    if (attacks.includes("BurstFire")) modes.push(`burst ${weapon.burst_shots}`);
    if (attacks.includes("AutoFire")) modes.push(`auto ${weapon.auto_shots}`);
    if (attacks.includes("MGBurstFire")) modes.push(`MG burst ${weapon.burst_shots}`);
    if (attacks.includes("Buckshot")) modes.push("buckshot");
  } else {
    if (attacks.includes("SingleShot")) modes.push("одиночный");
    if (attacks.includes("BurstFire")) modes.push(`очередь ${weapon.burst_shots}`);
    if (attacks.includes("AutoFire")) modes.push(`авто ${weapon.auto_shots}`);
    if (attacks.includes("MGBurstFire")) modes.push(`пулемёт ${weapon.burst_shots}`);
    if (attacks.includes("Buckshot")) modes.push("картечь");
  }
  return modes.length > 0 ? modes.join(", ") : attacks.join(", ");
}

function slotSummary(weaponId, optionsByWeapon, lang = "ru") {
  const options = optionsByWeapon.get(weaponId) ?? [];
  const slots = new Map();
  for (const option of options) {
    const key = `${option.slot_index}:${option.slot_type}`;
    if (!slots.has(key)) {
      slots.set(key, {
        name:
          option.slot_type ||
          (lang === "en" ? `Slot ${option.slot_index}` : `Слот ${option.slot_index}`),
        canBeEmpty: option.can_be_empty === "true",
        modifiable: option.modifiable !== "false",
        options: [],
      });
    }
    if (option.component_id) {
      const label = localizedLabel(option.component_name, option.component_id, lang);
      slots.get(key).options.push(`${label}${option.is_default === "true" ? " ★" : ""}`);
    }
  }
  if (slots.size === 0) {
    return lang === "en" ? "No component slots" : "Нет компонентных слотов";
  }
  return [...slots.values()]
    .map((slot) => {
      const flags = [];
      if (!slot.modifiable) flags.push(lang === "en" ? "fixed" : "фикс.");
      if (slot.canBeEmpty) flags.push(lang === "en" ? "removable" : "можно снять");
      const suffix = flags.length > 0 ? ` (${flags.join(", ")})` : "";
      const empty = lang === "en" ? "no options" : "без вариантов";
      return `${slot.name}${suffix}: ${slot.options.join(" / ") || empty}`;
    })
    .join("<br>");
}

function familyPage(family, weapons, optionsByWeapon, snapshotCommit, lang = "ru") {
  const combatHeader =
    lang === "en"
      ? [
          "Tier",
          "Weapon",
          "Caliber",
          "Damage",
          "Pen.",
          "Mag",
          "AP shot/reload",
          "Aim",
          "BDR / range",
          "Hold",
          "Recoil",
          "Modes",
        ]
      : [
          "Тир",
          "Оружие",
          "Калибр",
          "Урон",
          "Пробитие",
          "Маг.",
          "ОД выстрел/перезарядка",
          "Прицел",
          "BDR / дальность",
          "Кучность",
          "Отдача",
          "Режимы",
        ];
  const serviceHeader =
    lang === "en"
      ? ["Weapon", "Reliability", "Jam base", "Resource / wear", "Noise", "Overwatch", "Cost", "Components"]
      : ["Оружие", "Надёжность", "База клина", "Ресурс / износ", "Шум", "Overwatch", "Цена", "Компоненты"];

  const noTier = lang === "en" ? "no tier" : "без тира";
  const combatRows = weapons.map((weapon) => [
    weapon.tier_label || noTier,
    `${localizedLabel(weapon.display_name, weapon.id, lang)} (\`${weapon.id}\`)`,
    weapon.caliber,
    weapon.damage,
    `${weapon.penetration_class}${weapon.penetration_bonus && weapon.penetration_bonus !== "0" ? ` (${Number(weapon.penetration_bonus) > 0 ? "+" : ""}${weapon.penetration_bonus})` : ""}`,
    weapon.magazine_size,
    `${ap(weapon.shoot_ap)} / ${ap(weapon.reload_ap)}`,
    `${weapon.max_aim_actions} × ${weapon.aim_accuracy}`,
    `${weapon.bullet_drop_range} / ${weapon.weapon_range}`,
    weapon.grouping,
    weapon.recoil,
    attackModes(weapon, lang),
  ]);

  const serviceRows = weapons.map((weapon) => [
    `${localizedLabel(weapon.display_name, weapon.id, lang)} (\`${weapon.id}\`)`,
    weapon.reliability,
    weapon.base_jam_chance,
    `${weapon.weapon_resource} / ${weapon.degrade_per_shot}`,
    weapon.noise,
    angle(weapon.overwatch_angle),
    weapon.cost,
    slotSummary(weapon.id, optionsByWeapon, lang),
  ]);

  const table = (headers, rows) => [
    `| ${headers.join(" | ")} |`,
    `|${headers.map(() => "---").join("|")}|`,
    ...rows.map((row) => `| ${row.map(mdCell).join(" | ")} |`),
  ].join("\n");

  const title = familyTitle(family, lang);
  const nav =
    lang === "en"
      ? `[Weapon catalog](README.md) · [How to read stats](../../../showcase/en/weapons-and-ammo.md) · [All components](components.md)`
      : `[К каталогу оружия](README.md) · [Как читать характеристики](../weapons-and-ammo.md) · [Все компоненты](components.md)`;
  const intro =
    lang === "en"
      ? `This family has ${weapons.length} weapons. Tier is the power band; sub-tier only orders or separates close variants. \`UNIQ\` is a unique variant inside that tier; “no tier” means quest, technical, or not yet classified.`
      : `В семействе — ${weapons.length} единиц оружия. Тир задаёт силовой диапазон; под-тир только упорядочивает или различает близкие варианты. \`UNIQ\` означает уникальный вариант внутри указанного тира, а «без тира» — технический, квестовый или ещё не классифицированный предмет.`;
  const combatH = lang === "en" ? "## Combat stats" : "## Боевые характеристики";
  const serviceH = lang === "en" ? "## Service and components" : "## Эксплуатация и компоненты";
  const serviceNote =
    lang === "en"
      ? `Star \`★\` marks the default component. “fixed” means a non-modifiable slot. AP values are in game units, not internal thousandths.`
      : `Звезда \`★\` отмечает компонент по умолчанию. «Фикс.» означает немодифицируемый слот. ОД показаны в игровых единицах, а не во внутренних тысячных.`;
  const footer =
    lang === "en"
      ? `Numbers come from canonical CSV snapshot \`${snapshotCommit}\`. Field meanings and sync rules: [technical contract](../../../technical/weapons/README.md).`
      : `Источник чисел: канонический CSV-снимок \`${snapshotCommit}\`. Описание полей и правила синхронизации находятся в [техническом контракте](../../technical/weapons/README.md).`;

  return `<!-- Generated by scripts/docs/weapons-docs.mjs from docs/technical/weapons/data. Do not edit this file directly. -->
# ${title}

${nav}

${intro}

${combatH}

${table(combatHeader, combatRows)}

${serviceH}

${serviceNote}

${table(serviceHeader, serviceRows)}

${footer}
`;
}

function componentsPage(data) {
  const effects = new Map(data.effects.map((effect) => [effect.effect_id, effect]));
  const useCounts = new Map();
  for (const option of data.options) {
    if (!option.component_id) continue;
    if (!useCounts.has(option.component_id)) useCounts.set(option.component_id, new Set());
    useCounts.get(option.component_id).add(option.weapon_id);
  }
  const usedComponents = data.components
    .filter(
      (component) =>
        useCounts.has(component.component_id) &&
        component.component_id !== "DefaultIronsight_AR15",
    )
    .sort(
      (a, b) =>
        a.slot.localeCompare(b.slot, "ru") ||
        a.display_name.localeCompare(b.display_name, "ru"),
    );
  const rows = usedComponents.map((component) => {
    const effectText = component.effects
      .split(";")
      .filter(Boolean)
      .map((id) => {
        const effect = effects.get(id);
        return effect?.display_name && effect.display_name !== id
          ? `${effect.display_name} (\`${id}\`)`
          : `\`${id}\``;
      })
      .join("<br>");
    return `| ${[
      component.slot,
      `${component.display_name} (\`${component.component_id}\`)`,
      component.cost,
      component.modification_difficulty,
      effectText,
      component.parameters,
      component.additional_costs,
      useCounts.get(component.component_id).size,
    ].map(mdCell).join(" | ")} |`;
  });

  return `<!-- Generated by scripts/docs/weapons-docs.mjs from docs/technical/weapons/data. Do not edit this file directly. -->
# Компоненты оружия

[К каталогу оружия](README.md)

Здесь перечислены компоненты, доступные хотя бы у одного оружия в каталоге. Стабильные ID оставлены рядом с человекочитаемыми названиями, поэтому таблицу можно использовать и как справочник игрока, и как точку поиска по коду.

| Слот | Компонент | Цена | Сложность | Эффекты | Параметры | Доп. материалы | Оружий |
|---|---|---:|---:|---|---|---|---:|
${rows.join("\n")}

Полный нормализованный список, включая неиспользуемые определения и отдельный словарь эффектов, находится в [технических CSV](../../technical/weapons/README.md).
`;
}

function indexPage(data, invalidDefaults) {
  const byFamily = new Map();
  for (const weapon of data.weapons) {
    if (!byFamily.has(weapon.object_class)) byFamily.set(weapon.object_class, []);
    byFamily.get(weapon.object_class).push(weapon);
  }
  const families = Object.entries(familyDefinitions)
    .filter(([objectClass]) => byFamily.has(objectClass))
    .sort(([, a], [, b]) => a.order - b.order);
  const snapshotCommit = data.weapons[0]?.snapshot_commit ?? "unknown";
  const assigned = data.weapons.filter((weapon) => weapon.tier_status === "assigned").length;
  const unique = data.weapons.filter((weapon) => weapon.tier_status === "unique").length;
  const unassigned = data.weapons.filter((weapon) => weapon.tier_status === "unassigned");

  const familyRows = families.map(([objectClass, family]) => {
    const weapons = byFamily.get(objectClass);
    const tiers = [...new Set(weapons.map((weapon) => weapon.balance_tier).filter(Boolean))]
      .sort((a, b) => Number(a) - Number(b))
      .join(", ");
    return `| [${family.title}](${family.id}.md) | \`${objectClass}\` | ${weapons.length} | ${tiers || "—"} |`;
  });

  return `<!-- Generated by scripts/docs/weapons-docs.mjs from docs/technical/weapons/data. Do not edit this file directly. -->
# Энциклопедия оружия JAZZ

Это полный справочник основных классов стрелкового оружия: ${data.weapons.length} предметов, ${assigned} обычных tiered-вариантов, ${unique} уникальных и ${unassigned.length} пока без balance-tier. Числа берутся из канонических таблиц документации, а не из Google Sheets.

## Как устроены тиры

- **Тир** — заметный силовой диапазон внутри семейства. Переход между тирами должен ощущаться в суммарной боевой ценности.
- **Под-тир** — порядок и вариативность внутри одного тира. Он не должен превращаться в скрытый дополнительный тир.
- **\`UNIQ\`** — уникальное оружие с особым профилем; первая цифра всё равно задаёт его силовой диапазон.
- Сравнивать нужно не один урон: магазин, ОД, прицеливание, дальность, кучность, отдача, ресурс, надёжность и доступные компоненты образуют общий бюджет оружия.
- Поле \`engine_tier\` магазина/лут-системы не является balance-tier и хранится отдельно.

## Семейства

| Семейство | Класс данных | Оружий | Тиры |
|---|---|---:|---|
${familyRows.join("\n")}

- [Все компоненты](components.md)
- [Как читать характеристики оружия](../weapons-and-ammo.md)
- [Бой и точность](../combat-and-accuracy.md)

## Оружие без balance-tier

${unassigned.length > 0
    ? unassigned
        .sort((a, b) => a.object_class.localeCompare(b.object_class) || a.id.localeCompare(b.id))
        .map((weapon) => `- \`${weapon.id}\` — ${weapon.display_name} (${weapon.family_name_ru}); источник: \`${weapon.source_file}\`.`)
        .join("\n")
    : "Нет."}

## Известные аномалии данных

${invalidDefaults.length > 0
    ? invalidDefaults.map((value) => `- Компонент по умолчанию отсутствует среди вариантов слота: \`${value}\`.`).join("\n")
    : "Проверка не нашла default-компонентов вне списка вариантов."}

Снимок первичного импорта: \`${snapshotCommit}\`. После импорта источник истины — [CSV-каталог и его схема](../../technical/weapons/README.md); эти wiki-страницы генерируются из него.
`;
}

function buildWiki(checkOnly = false) {
  const data = readCanonicalData();
  const publicWeaponIds = new Set(
    data.weapons.filter((weapon) => weapon.catalog_status === "active").map((weapon) => weapon.id),
  );
  const publicData = { ...data,
    weapons: data.weapons.filter((weapon) => publicWeaponIds.has(weapon.id)),
    options: data.options.filter((option) => publicWeaponIds.has(option.weapon_id)) };
  const { invalidDefaults } = validateCanonicalData(data);
  const optionsByWeapon = new Map();
  for (const option of publicData.options) {
    if (!optionsByWeapon.has(option.weapon_id)) optionsByWeapon.set(option.weapon_id, []);
    optionsByWeapon.get(option.weapon_id).push(option);
  }
  const snapshotCommit = publicData.weapons[0]?.snapshot_commit ?? "unknown";
  const expected = new Map();
  expected.set(join(wikiDir, "README.md"), indexPage(publicData, invalidDefaults));
  expected.set(join(wikiDir, "components.md"), componentsPage(publicData));

  for (const [objectClass, family] of Object.entries(familyDefinitions)) {
    const weapons = publicData.weapons
      .filter((weapon) => weapon.object_class === objectClass)
      .sort(tierSort);
    if (weapons.length === 0) continue;
    expected.set(
      join(wikiDir, `${family.id}.md`),
      familyPage(family, weapons, optionsByWeapon, snapshotCommit),
    );
  }

  if (checkOnly) {
    const mismatches = [];
    for (const [path, content] of expected) {
      if (!existsSync(path) || readFileSync(path, "utf8").replace(/\r\n/g, "\n") !== content) {
        mismatches.push(relative(rootDir, path));
      }
    }
    if (mismatches.length > 0) {
      throw new Error(`Generated wiki is stale:\n- ${mismatches.join("\n- ")}\nRun: node scripts/docs/weapons-docs.mjs build`);
    }
    console.log(
      `Validated ${data.weapons.length} weapons. Generated wiki is current. ${invalidDefaults.length} known default-component anomalies.`,
    );
    return;
  }

  mkdirSync(wikiDir, { recursive: true });
  for (const [path, content] of expected) writeUtf8(path, content);
  console.log(
    `Built ${expected.size} wiki pages from ${data.weapons.length} canonical weapon rows. ${invalidDefaults.length} default-component anomalies retained.`,
  );
}

function usage() {
  console.log(`Usage:
  node scripts/docs/weapons-docs.mjs import [--commit=<git-ref>] [--force]
  node scripts/docs/weapons-docs.mjs build
  node scripts/docs/weapons-docs.mjs check

The import command is only for the initial bootstrap or an intentional full re-bootstrap.
After bootstrap, docs/technical/weapons/data/*.csv is authoritative and build never reads weapon Lua.`);
}

const command = process.argv[2];
if (command === "import") {
  importFromGit();
} else if (command === "build") {
  buildWiki(false);
} else if (command === "check") {
  buildWiki(true);
} else {
  usage();
  process.exitCode = command ? 1 : 0;
}
