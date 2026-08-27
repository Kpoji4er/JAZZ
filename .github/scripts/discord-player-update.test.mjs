import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  analyzeCommitMarkers,
  buildAiContext,
  buildDiscordPayload,
  buildFallbackSummary,
  collectPushChanges,
  combineDiffPieces,
  detectNewGameNeededMarker,
  duplicatePublishSkipReason,
  formatNewGameNeededLabel,
  formatSuitePackagesField,
  parseMetadataEngineVersion,
  parseSuiteVersions,
  getSummarySkipReason,
  isClearlyNoiseOnly,
  neutralizeDiscordMentions,
  parseAiOutput,
  redactSecrets,
  resolveNewGameNeeded,
  resolvePlayerSummary,
  resolveSuitePackages,
  safeErrorMessage,
} from "./discord-player-update.mjs";

test("duplicatePublishSkipReason skips when a peer already succeeded", () => {
  const sha = "abc123";
  assert.equal(
    duplicatePublishSkipReason(
      [
        { id: 10, head_sha: sha, status: "completed", conclusion: "success" },
        { id: 11, head_sha: sha, status: "in_progress", conclusion: null },
      ],
      sha,
      11,
    ),
    "another Discord run already completed successfully for this after SHA",
  );
});

test("duplicatePublishSkipReason defers to an older in-progress twin", () => {
  const sha = "def456";
  assert.equal(
    duplicatePublishSkipReason(
      [
        { id: 20, head_sha: sha, status: "in_progress", conclusion: null },
        { id: 21, head_sha: sha, status: "queued", conclusion: null },
      ],
      sha,
      21,
    ),
    "an older Discord run for this after SHA is already in progress",
  );
  assert.equal(
    duplicatePublishSkipReason(
      [{ id: 20, head_sha: sha, status: "in_progress", conclusion: null }],
      sha,
      20,
    ),
    null,
  );
});

test("system prompt treats merc Name/Nick as one person", async () => {
  const source = await readFile(
    fileURLToPath(new URL("./discord-player-update.mjs", import.meta.url)),
    "utf8",
  );
  assert.match(source, /Имена наёмников/);
  assert.match(source, /Trevor Colby/);
  assert.match(source, /не второй персонаж/);
  assert.match(source, /Колби и Тревор/);
  assert.match(source, /Вольф/);
  assert.match(source, /не «Волк»/);
});

function git(cwd, args) {
  const result = spawnSync("git", args, {
    cwd,
    encoding: "utf8",
    windowsHide: true,
  });
  assert.equal(
    result.status,
    0,
    `git ${args.join(" ")} failed: ${result.stderr}`,
  );
  return result.stdout.trim();
}

async function createTestRepository() {
  const cwd = await mkdtemp(join(tmpdir(), "jazz-discord-update-"));
  git(cwd, ["init", "-b", "main"]);
  git(cwd, ["config", "user.name", "JAZZ Test"]);
  git(cwd, ["config", "user.email", "jazz-test@example.invalid"]);

  await writeFile(join(cwd, "Code.lua"), "return 1\n", "utf8");
  git(cwd, ["add", "Code.lua"]);
  git(cwd, ["commit", "-m", "Начальное состояние"]);
  const before = git(cwd, ["rev-parse", "HEAD"]);

  await writeFile(join(cwd, "Code.lua"), "return 2\n", "utf8");
  git(cwd, ["add", "Code.lua"]);
  git(cwd, ["commit", "-m", "Изменена логика боя"]);

  await mkdir(join(cwd, "docs", "technical"), { recursive: true });
  await writeFile(join(cwd, "docs", "technical", "Notes.md"), "Описание изменения\n", "utf8");
  git(cwd, ["add", "docs/technical/Notes.md"]);
  git(cwd, ["commit", "-m", "Добавлено описание"]);
  const after = git(cwd, ["rev-parse", "HEAD"]);

  return { cwd, before, after };
}

async function createDocumentationRepository(commitMessage) {
  const cwd = await mkdtemp(join(tmpdir(), "jazz-discord-docs-"));
  git(cwd, ["init", "-b", "main"]);
  git(cwd, ["config", "user.name", "JAZZ Test"]);
  git(cwd, ["config", "user.email", "jazz-test@example.invalid"]);

  await mkdir(join(cwd, "docs", "technical"), { recursive: true });
  await writeFile(
    join(cwd, "docs", "technical", "system.md"),
    "Реализованная механика описана здесь.\n",
    "utf8",
  );
  git(cwd, ["add", "docs/technical/system.md"]);
  git(cwd, ["commit", "-m", commitMessage]);

  return {
    cwd,
    after: git(cwd, ["rev-parse", "HEAD"]),
  };
}

function documentationPushEvent(after) {
  return {
    before: "0000000000000000000000000000000000000000",
    after,
    ref: "refs/heads/main",
    forced: false,
    pusher: { name: "tester" },
    head_commit: { timestamp: "2026-07-26T10:00:00Z" },
  };
}

function testPushEnvironment(repository = "Kpoji4er/JAZZ") {
  return {
    GITHUB_EVENT_NAME: "push",
    GITHUB_REPOSITORY: repository,
    GITHUB_SERVER_URL: "https://github.com",
    GITHUB_REF_NAME: "main",
  };
}

test("skip marker has priority over force and implementation markers", () => {
  const result = analyzeCommitMarkers([
    { message: "Показать [discord implemented]" },
    { message: "Не публиковать [skip discord]" },
  ]);

  assert.deepEqual(result, {
    skip: true,
    force: false,
    documentationImplementationExplicit: false,
    newGameNeeded: null,
  });
  assert.deepEqual(analyzeCommitMarkers([{ message: "Показать [discord]" }]), {
    skip: false,
    force: true,
    documentationImplementationExplicit: false,
    newGameNeeded: null,
  });
  assert.deepEqual(
    analyzeCommitMarkers([{ message: "Подтверждено [discord implemented]" }]),
    {
      skip: false,
      force: true,
      documentationImplementationExplicit: true,
      newGameNeeded: null,
    },
  );
});

test("new game markers resolve with strongest value in the push range", () => {
  assert.equal(detectNewGameNeededMarker("fix [new game]"), "required");
  assert.equal(
    detectNewGameNeededMarker("loot [needs new game]"),
    "required",
  );
  assert.equal(
    detectNewGameNeededMarker("content [new game recommended]"),
    "recommended",
  );
  assert.equal(detectNewGameNeededMarker("ui [no new game]"), "not_needed");
  assert.equal(detectNewGameNeededMarker("combat [save ok]"), "not_needed");
  assert.equal(detectNewGameNeededMarker("обычный коммит"), null);

  assert.equal(
    analyzeCommitMarkers([
      { message: "UI [no new game]" },
      { message: "Кампания [new game recommended]" },
      { message: "Спавн [new game]" },
    ]).newGameNeeded,
    "required",
  );
  assert.equal(resolveNewGameNeeded("required", "not_needed"), "required");
  assert.equal(resolveNewGameNeeded(null, "recommended"), "recommended");
  assert.equal(resolveNewGameNeeded(null, "bogus"), "unknown");
  assert.match(formatNewGameNeededLabel("required"), /Нужна новая игра/);
});

test("service-only paths are recognized as noise", () => {
  assert.equal(
    isClearlyNoiseOnly([
      ".github/workflows/discord.yml",
      "docs/technical/testing.md",
      "docs/specs/active/JAZZ-DISCORD-999.md",
      "docs/wiki/player-guide.md",
      "tests/update.test.mjs",
    ]),
    true,
  );
  assert.equal(isClearlyNoiseOnly(["Code/CombatAI.lua"]), false);
});

test("ordinary documentation is excluded from implementation evidence", async () => {
  const repository = await createDocumentationRepository(
    "Обновить техническое описание",
  );
  try {
    const changeSet = collectPushChanges({
      cwd: repository.cwd,
      event: documentationPushEvent(repository.after),
      env: testPushEnvironment(),
    });
    const context = buildAiContext(changeSet);

    assert.equal(changeSet.text, "");
    assert.equal(changeSet.documentationImplementationExplicit, false);
    assert.ok(
      changeSet.excluded.some(
        (entry) =>
          entry.filePath === "docs/technical/system.md" &&
          entry.reason === "documentation",
      ),
    );
    assert.equal(context.documentation_only, true);
    assert.equal(context.documentation_implementation_explicit, false);
    assert.deepEqual(context.implementation_changed_files, []);
    assert.deepEqual(context.documentation_changed_files, [
      "docs/technical/system.md",
    ]);
  } finally {
    await rm(repository.cwd, { recursive: true, force: true });
  }
});

test("explicit implementation marker includes documentation as evidence", async () => {
  const repository = await createDocumentationRepository(
    "Подтвердить реализованное состояние [discord implemented]",
  );
  try {
    const changeSet = collectPushChanges({
      cwd: repository.cwd,
      event: documentationPushEvent(repository.after),
      env: testPushEnvironment(),
    });
    const context = buildAiContext(changeSet);

    assert.equal(changeSet.documentationImplementationExplicit, true);
    assert.match(changeSet.text, /Реализованная механика/);
    assert.equal(
      changeSet.excluded.some((entry) => entry.reason === "documentation"),
      false,
    );
    assert.equal(context.documentation_only, true);
    assert.equal(context.documentation_implementation_explicit, true);
    assert.deepEqual(context.implementation_changed_files, []);
  } finally {
    await rm(repository.cwd, { recursive: true, force: true });
  }
});

test("docs-only push without marker is skipped before OpenAI fallback", async () => {
  const repository = await createDocumentationRepository(
    "Обновить техническое описание",
  );
  try {
    const eventPath = join(repository.cwd, "event.json");
    await writeFile(
      eventPath,
      JSON.stringify(documentationPushEvent(repository.after)),
      "utf8",
    );
    const scriptPath = fileURLToPath(
      new URL("./discord-player-update.mjs", import.meta.url),
    );
    const result = spawnSync(process.execPath, [scriptPath], {
      cwd: repository.cwd,
      encoding: "utf8",
      windowsHide: true,
      env: {
        ...process.env,
        ...testPushEnvironment(),
        DISCORD_WEBHOOK_URL: "",
        DRY_RUN: "true",
        EXPECTED_BRANCH: "main",
        GITHUB_EVENT_PATH: eventPath,
        MANUAL_FORCE_PUBLISH: "false",
        OPENAI_API_KEY: "",
      },
    });

    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /only CI, tests, tooling, or documentation/);
    assert.doesNotMatch(result.stdout, /OpenAI fallback/);
  } finally {
    await rm(repository.cwd, { recursive: true, force: true });
  }
});

test("[discord] publishes docs-only fallback without implementation claims", async () => {
  const repository = await createDocumentationRepository(
    "Обновить руководство [discord]",
  );
  try {
    const eventPath = join(repository.cwd, "event.json");
    await writeFile(
      eventPath,
      JSON.stringify(documentationPushEvent(repository.after)),
      "utf8",
    );
    const scriptPath = fileURLToPath(
      new URL("./discord-player-update.mjs", import.meta.url),
    );
    const result = spawnSync(process.execPath, [scriptPath], {
      cwd: repository.cwd,
      encoding: "utf8",
      windowsHide: true,
      env: {
        ...process.env,
        ...testPushEnvironment(),
        DISCORD_WEBHOOK_URL: "",
        DRY_RUN: "true",
        EXPECTED_BRANCH: "main",
        GITHUB_EVENT_PATH: eventPath,
        MANUAL_FORCE_PUBLISH: "false",
        OPENAI_API_KEY: "",
      },
    });

    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /JAZZ — обновление документации/);
    assert.match(result.stdout, /без выводов о реализации/);
    assert.doesNotMatch(result.stdout, /в разработке/);
  } finally {
    await rm(repository.cwd, { recursive: true, force: true });
  }
});

test("prompt treats documentation as non-implementation evidence", async () => {
  const source = await readFile(
    fileURLToPath(new URL("./discord-player-update.mjs", import.meta.url)),
    "utf8",
  );

  assert.match(source, /documentation_only=true/);
  assert.match(source, /сами по себе не\s+доказывают/);
  assert.match(source, /видимый игроку эффект/);
  assert.match(source, /оружие с обвесом/);
  assert.match(source, /Всегда заполняй new_game_needed/);
  assert.doesNotMatch(
    source,
    /Изменения в основной ветке называй работой в разработке/,
  );
});

test("valid AI JSON is parsed and invalid JSON is rejected", () => {
  const valid = JSON.stringify({
    should_publish: false,
    title: "JAZZ — изменения",
    summary: "",
    sections: [],
    new_game_needed: "not_needed",
    confidence: "high",
  });

  assert.equal(parseAiOutput(valid).should_publish, false);
  assert.equal(parseAiOutput(valid).new_game_needed, "not_needed");
  assert.throws(() => parseAiOutput("{broken"), /valid JSON/);
  assert.throws(
    () =>
      parseAiOutput(
        JSON.stringify({
          should_publish: false,
          title: "JAZZ — изменения",
          summary: "",
          sections: [],
          confidence: "high",
        }),
      ),
    /new_game_needed/,
  );

  const truncated = parseAiOutput(
    JSON.stringify({
      should_publish: true,
      title: "Title",
      summary: "Summary",
      sections: [
        {
          name: "Too many",
          items: Array.from({ length: 9 }, (_, index) => `Item ${index}`),
        },
      ],
      new_game_needed: "recommended",
      confidence: "high",
    }),
  );
  assert.equal(truncated.sections.length, 1);
  assert.equal(truncated.sections[0].items.length, 8);
  assert.deepEqual(truncated.sections[0].items, [
    "Item 0",
    "Item 1",
    "Item 2",
    "Item 3",
    "Item 4",
    "Item 5",
    "Item 6",
    "Item 7",
  ]);
  assert.equal(truncated.new_game_needed, "recommended");

  assert.throws(
    () =>
      parseAiOutput(
        JSON.stringify({
          should_publish: false,
          title: "Title",
          summary: "",
          sections: [],
          development_note: null,
          new_game_needed: "unknown",
          confidence: "high",
        }),
      ),
    /unsupported development_note/,
  );
});

test("diff is truncated without dropping the truncation signal", () => {
  const result = combineDiffPieces(
    [
      { filePath: "Code/One.lua", diff: "a".repeat(80) },
      { filePath: "Code/Two.lua", diff: "b".repeat(80) },
    ],
    { totalLimit: 110, perFileLimit: 70 },
  );

  assert.equal(result.truncated, true);
  assert.match(result.text, /diff/);
});

test("AI context limits commit text and redacts suspicious file names", () => {
  const commits = Array.from({ length: 50 }, (_, index) => ({
    sha: String(index).padStart(40, "0"),
    author: "tester",
    message: `Изменение ${index} ${"x".repeat(500)}`,
  }));
  const fakeToken = ["sk", "proj", "abcdefghijklmnopqrstuvwxyz"].join("-");
  const context = buildAiContext({
    repository: "Kpoji4er/JAZZ",
    branch: "main",
    pusher: "tester",
    beforeSha: "1".repeat(40),
    afterSha: "2".repeat(40),
    forcePush: false,
    degraded: false,
    compareUrl: "https://github.com/Kpoji4er/JAZZ/compare/a...b",
    commitCount: commits.length,
    commitsTruncated: false,
    commits,
    changedFiles: [`Code/${fakeToken}.lua`],
    additions: 1,
    deletions: 0,
    excluded: [],
    truncated: false,
    omittedFiles: [`Code/${fakeToken}.lua`],
    text: "",
  });

  assert.equal(context.commits_truncated, true);
  assert.ok(JSON.stringify(context.commits).length < 9_000);
  assert.doesNotMatch(
    JSON.stringify([context.changed_files, context.omitted_diff_files]),
    /abcdefghijklmnopqrstuvwxyz/,
  );
});

test("should_publish=false and low confidence produce safe skips", () => {
  assert.match(
    getSummarySkipReason({ should_publish: false, confidence: "high" }, false),
    /should_publish=false/,
  );
  assert.match(
    getSummarySkipReason({ should_publish: true, confidence: "low" }, false),
    /confidence is low/,
  );
  assert.equal(
    getSummarySkipReason({ should_publish: true, confidence: "low" }, true),
    null,
  );
});

test("secrets and mass mentions are neutralized", () => {
  const secret = ["sk", "proj", "abcdefghijklmnopqrstuvwxyz"].join("-");
  assert.doesNotMatch(redactSecrets(`key=${secret}`), /abcdefghijklmnopqrstuvwxyz/);
  assert.equal(
    neutralizeDiscordMentions("@everyone и @here"),
    "@\u200beveryone и @\u200bhere",
  );
  assert.doesNotMatch(
    safeErrorMessage(new Error(`failed with ${secret}`)),
    /abcdefghijklmnopqrstuvwxyz/,
  );
});

test("fallback uses commit subjects and removes control markers", () => {
  const fallback = buildFallbackSummary([
    { message: "Исправлена ошибка [discord implemented]\n\nПодробности" },
  ]);

  assert.equal(fallback.should_publish, true);
  assert.deepEqual(fallback.sections[0].items, ["Исправлена ошибка"]);
  assert.doesNotMatch(fallback.title, /в разработке/);
  assert.equal(fallback.new_game_needed, "unknown");

  const markedFallback = buildFallbackSummary([
    { message: "Спавн [new game]" },
  ]);
  assert.equal(markedFallback.new_game_needed, "required");
  assert.deepEqual(markedFallback.sections[0].items, ["Спавн"]);

  const docsFallback = buildFallbackSummary(
    [{ message: "Обновлено руководство [discord]" }],
    { documentationOnly: true },
  );
  assert.equal(docsFallback.title, "JAZZ — обновление документации");
  assert.match(docsFallback.summary, /без выводов о реализации/);
  assert.equal(docsFallback.new_game_needed, "not_needed");
});

test("missing OpenAI key automatically uses fallback without override", async () => {
  let requestCalled = false;
  const result = await resolvePlayerSummary({
    apiKey: "",
    model: "test-model",
    aiContext: {},
    commits: [{ message: "Updated combat rules" }],
    forcePublish: false,
    requestSummary: async () => {
      requestCalled = true;
      return null;
    },
    log: () => {},
  });

  assert.equal(requestCalled, false);
  assert.equal(result.usedFallback, true);
  assert.equal(result.summary.should_publish, true);
  assert.deepEqual(result.summary.sections[0].items, [
    "Updated combat rules",
  ]);
});

test("OpenAI failure automatically uses fallback without override", async () => {
  const logs = [];
  const result = await resolvePlayerSummary({
    apiKey: "test-api-key",
    model: "test-model",
    aiContext: {},
    commits: [{ message: "Improved enemy behavior" }],
    forcePublish: false,
    requestSummary: async () => {
      throw new Error("insufficient_quota");
    },
    log: (message) => logs.push(message),
  });

  assert.equal(result.usedFallback, true);
  assert.equal(result.summary.should_publish, true);
  assert.deepEqual(result.summary.sections[0].items, [
    "Improved enemy behavior",
  ]);
  assert.match(logs.join("\n"), /insufficient_quota/);
});

test("dry run publishes automatic fallback without OpenAI key or override", async () => {
  const repository = await createTestRepository();
  try {
    const eventPath = join(repository.cwd, "event.json");
    await writeFile(
      eventPath,
      JSON.stringify({
        before: repository.before,
        after: repository.after,
        ref: "refs/heads/main",
        forced: false,
        pusher: { name: "tester" },
        head_commit: { timestamp: "2026-07-26T10:00:00Z" },
      }),
      "utf8",
    );

    const scriptPath = fileURLToPath(
      new URL("./discord-player-update.mjs", import.meta.url),
    );
    const result = spawnSync(process.execPath, [scriptPath], {
      cwd: repository.cwd,
      encoding: "utf8",
      windowsHide: true,
      env: {
        ...process.env,
        DISCORD_WEBHOOK_URL: "",
        DRY_RUN: "true",
        EXPECTED_BRANCH: "main",
        GITHUB_EVENT_NAME: "push",
        GITHUB_EVENT_PATH: eventPath,
        GITHUB_REF_NAME: "main",
        GITHUB_REPOSITORY: "Kpoji4er/JAZZ",
        GITHUB_SERVER_URL: "https://github.com",
        MANUAL_FORCE_PUBLISH: "false",
        OPENAI_API_KEY: "",
      },
    });

    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /OPENAI_API_KEY is not configured/);
    assert.match(result.stdout, /Dry run: Discord publication skipped/);
    assert.match(result.stdout, /Updated combat rules|Improved enemy behavior|Изменена логика боя/);
  } finally {
    await rm(repository.cwd, { recursive: true, force: true });
  }
});

test("Discord payload disables mentions and respects explicit role opt-in", () => {
  const summary = {
    should_publish: true,
    title: "Новости @everyone",
    summary: "Проверка @here",
    sections: [{ name: "Что изменилось", items: ["Первый пункт"] }],
    new_game_needed: "not_needed",
    confidence: "high",
  };
  const changeSet = {
    repository: "Kpoji4er/JAZZ-maps",
    compareUrl: "https://github.com/Kpoji4er/JAZZ-maps/compare/a...b",
    commitCount: 2,
    changedFiles: ["Code/A.lua"],
    additions: 10,
    deletions: 3,
    afterSha: "1234567890abcdef",
    timestamp: "2026-07-26T10:00:00.000Z",
  };

  const safePayload = buildDiscordPayload({ summary, changeSet });
  assert.deepEqual(safePayload.allowed_mentions.parse, []);
  assert.equal("content" in safePayload, false);
  assert.doesNotMatch(safePayload.embeds[0].title, /@everyone/);
  assert.match(safePayload.embeds[0].description, /\*\*Новая игра:\*\*/);
  assert.match(
    safePayload.embeds[0].description,
    /можно продолжить текущий сейв/,
  );
  assert.equal(safePayload.embeds[0].fields[0].name, "Новая игра");
  assert.match(
    safePayload.embeds[0].fields[0].value,
    /можно продолжить текущий сейв/,
  );
  assert.equal(safePayload.embeds[0].fields[1].name, "Пакеты");
  assert.match(safePayload.embeds[0].fields[1].value, /jazz-maps/);
  assert.match(safePayload.embeds[0].description, /\*\*Пакеты:\*\*/);
  assert.match(
    safePayload.embeds[0].footer.text,
    /JAZZ-maps · 2 коммита · 1 файл/,
  );

  const multiPayload = buildDiscordPayload({
    summary,
    changeSet,
    suitePackages: ["jazz", "jazz-units", "jazz-nomaps"],
  });
  assert.equal(multiPayload.embeds[0].fields[1].name, "Пакеты");
  assert.match(
    multiPayload.embeds[0].fields[1].value,
    /jazz[\s\S]*jazz-units[\s\S]*jazz-nomaps/,
  );
  assert.match(
    multiPayload.embeds[0].footer.text,
    /jazz, jazz-units, jazz-nomaps · /,
  );

  const rolePayload = buildDiscordPayload({
    summary,
    changeSet,
    mentionRole: true,
    roleId: "123456789012345678",
  });
  assert.equal(rolePayload.content, "<@&123456789012345678>");
  assert.deepEqual(rolePayload.allowed_mentions.roles, [
    "123456789012345678",
  ]);
});

test("resolveSuitePackages merges env list with posting repo", () => {
  assert.deepEqual(
    resolveSuitePackages({
      repository: "Kpoji4er/JAZZ",
      suitePackagesEnv: "jazz,jazz-units,jazz-nomaps",
    }),
    ["jazz", "jazz-units", "jazz-nomaps"],
  );
  assert.deepEqual(
    resolveSuitePackages({
      repository: "Kpoji4er/JAZZ-units",
      suitePackagesEnv: "",
    }),
    ["jazz-units"],
  );
  assert.equal(
    formatSuitePackagesField(["jazz", "jazz-units"]),
    "• jazz\n• jazz-units",
  );
  assert.equal(
    formatSuitePackagesField(["jazz", "jazz-units"], {
      jazz: "0.20-6206",
      "jazz-units": "0.19-2326",
    }),
    "• jazz 0.20-6206\n• jazz-units 0.19-2326",
  );
  assert.deepEqual(
    parseSuiteVersions("jazz:0.20-6206, jazz-units=0.19-2326"),
    { jazz: "0.20-6206", "jazz-units": "0.19-2326" },
  );
  assert.equal(
    parseMetadataEngineVersion(
      "return PlaceObj('ModDef', {\n\t'dependencies', {\n\t\tPlaceObj('ModDependency', {\n\t\t\t'version_major', 1,\n\t\t\t'version_minor', 11,\n\t\t}),\n\t},\n\t'author', \"Kpoji4er\",\n\t'version_minor', 20,\n\t'version', 6206,\n})",
    ),
    "0.20-6206",
  );
});

test("Discord packages field shows full engine versions", () => {
  const summary = {
    should_publish: true,
    title: "Title",
    summary: "Summary",
    sections: [],
    new_game_needed: "not_needed",
    confidence: "high",
  };
  const changeSet = {
    repository: "Kpoji4er/JAZZ",
    compareUrl: "https://github.com/Kpoji4er/JAZZ/compare/a...b",
    commitCount: 1,
    changedFiles: ["Code/A.lua"],
    additions: 1,
    deletions: 1,
    afterSha: "1234567890abcdef",
    timestamp: "2026-07-26T10:00:00.000Z",
  };
  const payload = buildDiscordPayload({
    summary,
    changeSet,
    suitePackages: ["jazz", "jazz-units"],
    suiteVersions: { jazz: "0.20-6206", "jazz-units": "0.19-2326" },
  });
  assert.match(
    payload.embeds[0].fields[1].value,
    /jazz 0\.20-6206[\s\S]*jazz-units 0\.19-2326/,
  );
});

test("Discord embed remains inside field and total size limits", () => {
  const summary = {
    should_publish: true,
    title: "T".repeat(500),
    summary: "S".repeat(10_000),
    sections: [
      {
        name: "N".repeat(500),
        items: Array.from({ length: 8 }, () => "I".repeat(2_000)),
      },
    ],
    development_note: "D".repeat(2_000),
    new_game_needed: "unknown",
    confidence: "high",
  };
  const changeSet = {
    repository: "Kpoji4er/JAZZ",
    compareUrl: "https://github.com/Kpoji4er/JAZZ/compare/a...b",
    commitCount: 1,
    changedFiles: ["Code/A.lua"],
    additions: 1,
    deletions: 1,
    afterSha: "1234567890abcdef",
    timestamp: "2026-07-26T10:00:00.000Z",
  };

  const payload = buildDiscordPayload({ summary, changeSet });
  const embed = payload.embeds[0];
  const total =
    embed.title.length +
    embed.description.length +
    embed.footer.text.length +
    embed.fields.reduce(
      (sum, field) => sum + field.name.length + field.value.length,
      0,
    );

  assert.ok(embed.title.length <= 256);
  assert.ok(embed.description.length <= 4_096);
  assert.ok(embed.fields.every((field) => field.value.length <= 1_024));
  assert.ok(total <= 6_000);
  assert.equal(
    embed.fields.some((field) => field.name === "За кулисами"),
    false,
  );
  assert.equal(embed.fields[0].name, "Новая игра");
});

test("commit new-game marker overrides AI value in resolvePlayerSummary", async () => {
  const result = await resolvePlayerSummary({
    apiKey: "test-api-key",
    model: "test-model",
    aiContext: {},
    commits: [{ message: "Спавн [new game]" }],
    newGameNeeded: "required",
    requestSummary: async () => ({
      should_publish: true,
      title: "Title",
      summary: "Summary",
      sections: [{ name: "Что изменилось", items: ["Спавн"] }],
      new_game_needed: "not_needed",
      confidence: "high",
    }),
    log: () => {},
  });

  assert.equal(result.usedFallback, false);
  assert.equal(result.summary.new_game_needed, "required");
});

test("full before..after range includes every commit in a multi-commit push", async () => {
  const repository = await createTestRepository();
  try {
    const event = {
      before: repository.before,
      after: repository.after,
      ref: "refs/heads/main",
      forced: false,
      pusher: { name: "tester" },
      head_commit: { timestamp: "2026-07-26T10:00:00Z" },
    };
    const changeSet = collectPushChanges({
      cwd: repository.cwd,
      event,
      env: {
        GITHUB_EVENT_NAME: "push",
        GITHUB_REPOSITORY: "Kpoji4er/JAZZ-units",
        GITHUB_SERVER_URL: "https://github.com",
        GITHUB_REF_NAME: "main",
      },
    });

    assert.equal(changeSet.commitCount, 2);
    assert.equal(changeSet.commits.length, 2);
    assert.deepEqual(changeSet.changedFiles.sort(), ["Code.lua", "docs/technical/Notes.md"]);
    assert.match(changeSet.text, /return 2/);
    assert.equal(changeSet.repository, "Kpoji4er/JAZZ-units");
    assert.match(changeSet.compareUrl, /Kpoji4er\/JAZZ-units\/compare\//);

    const context = buildAiContext(changeSet, false);
    assert.equal(context.commit_count, 2);
    assert.equal(context.diff_truncated, false);
    assert.equal(context.repository, "Kpoji4er/JAZZ-units");
    assert.equal(context.documentation_only, false);
    assert.deepEqual(context.implementation_changed_files, ["Code.lua"]);
    assert.deepEqual(context.documentation_changed_files, [
      "docs/technical/Notes.md",
    ]);
    assert.equal(context.excluded_diff_file_counts.documentation, 1);
  } finally {
    await rm(repository.cwd, { recursive: true, force: true });
  }
});

test("zero before SHA uses the empty tree for an initial push", async () => {
  const repository = await createTestRepository();
  try {
    const changeSet = collectPushChanges({
      cwd: repository.cwd,
      event: {
        before: "0000000000000000000000000000000000000000",
        after: repository.after,
        ref: "refs/heads/main",
        pusher: { name: "tester" },
      },
      env: {
        GITHUB_EVENT_NAME: "push",
        GITHUB_REPOSITORY: "Kpoji4er/JAZZ",
        GITHUB_SERVER_URL: "https://github.com",
        GITHUB_REF_NAME: "main",
      },
    });

    assert.equal(
      changeSet.beforeSha,
      "4b825dc642cb6eb9a060e54bf8d69288fbee4904",
    );
    assert.equal(changeSet.commitCount, 3);
    assert.match(changeSet.compareUrl, /\/commit\//);
  } finally {
    await rm(repository.cwd, { recursive: true, force: true });
  }
});


test("force push compares the exact before and after snapshots", async () => {
  const repository = await createTestRepository();
  try {
    const oldAfter = repository.after;
    git(repository.cwd, ["checkout", "-b", "rewritten", repository.before]);
    await writeFile(join(repository.cwd, "Code.lua"), "return 99\n", "utf8");
    git(repository.cwd, ["add", "Code.lua"]);
    git(repository.cwd, ["commit", "-m", "Переписана логика"]);
    const newAfter = git(repository.cwd, ["rev-parse", "HEAD"]);

    const changeSet = collectPushChanges({
      cwd: repository.cwd,
      event: {
        before: oldAfter,
        after: newAfter,
        ref: "refs/heads/main",
        forced: true,
        pusher: { name: "tester" },
      },
      env: {
        GITHUB_EVENT_NAME: "push",
        GITHUB_REPOSITORY: "Kpoji4er/JAZZ",
        GITHUB_SERVER_URL: "https://github.com",
        GITHUB_REF_NAME: "main",
      },
    });

    assert.equal(changeSet.forcePush, true);
    assert.equal(changeSet.commitCount, 1);
    assert.match(changeSet.text, /return 99/);
  } finally {
    await rm(repository.cwd, { recursive: true, force: true });
  }
});
