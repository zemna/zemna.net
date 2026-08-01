---
title: "A table beta bump is still a pilot decision"
date: 2026-08-01T07:00:00+07:00
draft: false
slug: "table-beta-is-still-a-pilot-decision"
description: "TanStack Table 9.0.0-beta.64 honors explicit global-filter opt-in. That is pilot hygiene, not permission to unpin stable 8.21.3. Here is the gate list before a Vue admin table leaves the spike branch."
topics: ["tutorials"]
tags: ["tanstack-table", "vue", "beta-adoption", "global-filter", "change-control", "frontend-maintenance", "lockfile", "pilot-gates", "laravel-vue"]
cover: /covers/table-beta-is-still-a-pilot-decision.png
seo:
  primaryQuery: "TanStack Table beta global filter opt-in"
  secondaryQueries:
    - "TanStack Table 9.0.0-beta.64 pilot checklist"
    - "vue-table stable 8.21.3 vs beta pin"
    - "beta library pilot exit criteria admin table"
---

The release note says the table got smarter about global filters.

**TanStack Table `v9.0.0-beta.64`**, published **2026-07-31**, includes one core fix that sounds small enough to merge while someone else is talking: **table-core honors an explicit global-filter opt-in** ([#6439](https://github.com/TanStack/table/pull/6439)). Packages on that tag include `@tanstack/table-core@9.0.0-beta.64` and `@tanstack/vue-table@9.0.0-beta.64`. [Source: https://github.com/TanStack/table/releases/tag/v9.0.0-beta.64]

That line is useful. It is not a production decision.

On the same calendar day, npm `dist-tags` for both `@tanstack/table-core` and `@tanstack/vue-table` still showed:

| dist-tag | Version (verified 2026-08-01) |
|---|---|
| `latest` | **8.21.3** |
| `beta` | **9.0.0-beta.65** (already past `.64`) |

[Source: https://registry.npmjs.org/@tanstack/table-core] [Source: https://registry.npmjs.org/@tanstack/vue-table]

Read that table twice. Stable is still **8.21.3**. The beta channel did not freeze on the opt-in fix you just bookmarked. **beta.65** landed minutes later with another global-filter fix (undefined first values). If your spike branch says “install beta” without an exact pin, you are not testing the release note you read. You are testing whichever beta the registry served that hour.

The question is not whether beta.64 demos cleanly in a fresh sandbox. The question is whether a multi-surface admin table — filters, sort, pagination, selection, SSR hydrate, worker parity — still has a named owner, a fixture that would fail if opt-in is ignored, and a one-command rollback when the pilot goes sideways.

<!--more-->

![Stable pin versus beta spike with filter fixture, owner, and rollback gates](/img/table-beta-is-still-a-pilot-decision-1.png)

## What beta.64 actually changed (primary sources only)

Do not upgrade table infrastructure from a social recap. Read the tag you will install, then confirm the npm tag you will resolve.

### Release body — `v9.0.0-beta.64`

Published **2026-07-31T00:07:47Z**, prerelease **true**.

**Fix**

- `table-core`: honor explicit global filter opt-in (**#6439**)

**Packages on the tag** (partial list relevant to Vue admin stacks)

- `@tanstack/table-core@9.0.0-beta.64`
- `@tanstack/vue-table@9.0.0-beta.64`
- (plus react/solid/svelte/angular/… adapters on the same beta line)

[Source: https://github.com/TanStack/table/releases/tag/v9.0.0-beta.64]

### Pull request rationale — #6439

PR **#6439** (`fix(table-core): honor explicit global filter opt-in`) merged **2026-07-30T23:57:23Z**. The summary is concrete:

- Let an **explicit per-column global-filter opt-in** bypass the default **primitive-value heuristic**
- Preserve table-wide filtering controls and custom column eligibility predicates
- Cover **object-valued** custom global filtering at capability and row-model levels

Rationale in the PR: by default, global filtering still only opts primitive string and number accessor values in automatically. When a column sets `enableGlobalFilter: true`, rejecting that column with the same primitive heuristic is surprising and blocks a custom `globalFilterFn` from handling object or array values.

[Source: https://github.com/TanStack/table/pull/6439]

{{< note type="warning" title="Do not invent a Vue SSR breaking story" >}}
The beta.64 release body does **not** document a Vue API break, a hydration contract change, or a production migration path. Treat missing detail as missing detail. Your job is narrower: prove which filter and row-model surfaces in *your* app still match the exact beta you pinned.
{{< /note >}}

### Nearby betas you will confuse with “the” table beta

| Tag | Published (UTC) | What the body claims | Ops takeaway |
|---|---|---|---|
| `v9.0.0-beta.59` | 2026-07-29 | More adapter reactivity tests; react adapter sync state | Pilot hygiene / test depth — still not “unpin stable” |
| `v9.0.0-beta.63` | 2026-07-30 | More readonly columns internally | Internal core churn — pin exact |
| `v9.0.0-beta.64` | 2026-07-31 | Honor explicit global filter opt-in (#6439) | **Filter fixture** belongs on the pilot checklist |
| `v9.0.0-beta.65` | 2026-07-31 | Global filtering with undefined first values (#6438) | npm `beta` tag moved here after `.64` |
| `v9.0.0-beta.67` | 2026-07-31 | Ship Octane Table source (#6480) | Package-scope change on octane line — do not generalize to vue-table |

[Source: https://github.com/TanStack/table/releases/tag/v9.0.0-beta.59] [Source: https://github.com/TanStack/table/releases/tag/v9.0.0-beta.63] [Source: https://github.com/TanStack/table/releases/tag/v9.0.0-beta.65] [Source: https://github.com/TanStack/table/releases/tag/v9.0.0-beta.67]

If your team says “we are on table v9 beta,” ask: **which tag, which lockfile hash, which fixture file?** Anything less is folklore.

{{< source href="https://github.com/TanStack/table/releases/tag/v9.0.0-beta.64" label="TanStack Table v9.0.0-beta.64 GitHub release" >}}
{{< source href="https://github.com/TanStack/table/pull/6439" label="PR #6439 — honor explicit global filter opt-in" >}}
{{< source href="https://www.npmjs.com/package/@tanstack/vue-table" label="npm @tanstack/vue-table" >}}

## Stable is still the production default

This section exists so nobody “helpfully” edits the package.json to `^9.0.0-beta.0` after reading the opt-in fix.

Verified against the npm registry JSON on **2026-08-01**:

- `@tanstack/table-core` → `dist-tags.latest = 8.21.3`, `dist-tags.beta = 9.0.0-beta.65`
- `@tanstack/vue-table` → `dist-tags.latest = 8.21.3`, `dist-tags.beta = 9.0.0-beta.65`
- Both `9.0.0-beta.64` and `9.0.0-beta.65` exist as published versions; **latest does not point at either**

[Source: https://registry.npmjs.org/@tanstack/table-core] [Source: https://registry.npmjs.org/@tanstack/vue-table]

Production posture for a normal Laravel + Vue admin app:

| Lane | Package resolution | Allowed surfaces |
|---|---|---|
| Production / main | `@tanstack/vue-table@8.21.3` (exact or locked latest) | Customer admin tables, SSR routes, billing grids |
| Pilot / spike branch | Exact beta pin, e.g. `9.0.0-beta.64` **or** the newer beta you deliberately chose | Feature-flagged route, internal tools, dogfood tenant |
| Broken middle | `"@tanstack/vue-table": "beta"` or floating range | Nowhere — this is how lockfiles lie on Monday |

I already wrote the general version of this argument in [Before You Adopt a Beta Library, Prove the Exit Path](/blog/before-you-adopt-a-beta-library-prove-the-exit-path/). This post is the **Saturday build-in-public** instance: one fresh artifact (global-filter opt-in), one stable pin that still holds, one multi-surface gate list you can run before anyone calls the bump “ready to try.”

![Production 8.21.3 versus pilot exact pin versus forbidden floating beta tag](/img/table-beta-is-still-a-pilot-decision-2.png)

## Why “more filter tests” is not a green light

beta.59-era notes leaned on **adapter reactivity tests**. beta.64 adds a **behavioral** filter fix. Both are healthy upstream signals. Neither answers:

1. Who owns the pilot after merge?
2. Which fixture fails if `enableGlobalFilter: true` is ignored again?
3. What is the named exit — pin stable forever, or graduate under a flag with a rollback command?
4. Do sort, filter, pagination, and selection still agree across the main thread and any worker/row-model boundary you already built?

If you already invested in workerized row models, re-read [TanStack Table v9 row-model workers](/blog/tanstack-table-v9-row-model-workers/). Parity before performance still applies. A global-filter opt-in fix that only passes on the main-thread happy path is not done.

{{< field-note title="Field note" >}}
On Laravel + Vue SaaS admin work, table betas fail the same way quiet UI-kit bumps fail: the diff looks local, the blast radius is operator screens. Global search boxes sit on order lists, inventory grids, and support queues — surfaces people open every Monday, not Storybook islands. I keep beta table pins next to the same change-control notes used for lockfile bumps and agent policy under [developer tools](/developer-tools/) and [Laravel + Vue SaaS](/laravel-vue-saas/): exact version, fixture path, owner, rollback. Project names stay in the ticket; the pattern is the reusable asset.
{{< /field-note >}}

## The pilot gate list (copy into the PR)

Treat this as a release checklist, not inspiration.

### Gate 0 — Classify the signal

```text
Signal: TanStack Table v9.0.0-beta.64 (#6439 global filter opt-in)
Class:  beta application library (spike / pilot only)
Not:    production default, security hotfix, or "just types"
Stable: @tanstack/vue-table@8.21.3 remains production pin
```

If someone argues for production from this tag alone, the classification failed.

### Gate 1 — Exact pins + lockfile

```json
{
  "private": true,
  "dependencies": {
    "@tanstack/table-core": "9.0.0-beta.64",
    "@tanstack/vue-table": "9.0.0-beta.64"
  },
  "scripts": {
    "check:table-pins": "node scripts/check-table-pins.mjs",
    "test:table-pilot": "vitest run tests/table-global-filter-pilot.test.ts"
  }
}
```

```javascript
// scripts/check-table-pins.mjs
import fs from "node:fs";

const pkg = JSON.parse(fs.readFileSync("package.json", "utf8"));
const lockOk = fs.existsSync("pnpm-lock.yaml") || fs.existsSync("package-lock.json");

const required = {
  "@tanstack/table-core": "9.0.0-beta.64",
  "@tanstack/vue-table": "9.0.0-beta.64",
};

const deps = { ...pkg.dependencies, ...pkg.devDependencies };
let failed = false;

for (const [name, version] of Object.entries(required)) {
  const actual = deps[name];
  if (actual !== version) {
    console.error(`pin mismatch: ${name} want ${version} got ${actual}`);
    failed = true;
  }
  if (typeof actual === "string" && /^(beta|latest|\^|~|>=)/.test(actual)) {
    console.error(`floating range forbidden: ${name}=${actual}`);
    failed = true;
  }
}

if (!lockOk) {
  console.error("lockfile missing — pilot is not reproducible");
  failed = true;
}

if (failed) process.exit(1);
console.log("table pilot pins ok");
```

Swap `9.0.0-beta.64` for `9.0.0-beta.65` only if the PR description says you intentionally absorbed #6438 as well. Silent drift from `.64` → `.65` because someone ran bare `npm install` is a failed gate, not a free upgrade.

### Gate 2 — Global-filter fixture that would have caught the bug class

You need at least one column that is **not** a primitive string/number accessor, with **explicit global-filter opt-in**, plus a custom filter function. If the suite only searches string names, you never exercised #6439.

V9 table construction is feature-registered (global filtering is not “all columns forever by default” the way many V8 apps behaved). Copy the **invariant**, then wire it with the exact helper imports from the beta tag you pinned — do not paste an old V8 `createTable` snippet into a V9 spike and call it green.

```typescript
// tests/table-global-filter-pilot.test.ts
// Behavioral contract for PR #6439. Wire createTable/features from the
// exact @tanstack/table-core version in package.json (beta pin).
import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";

type OrderRow = {
  id: string;
  customer: { name: string; code: string };
  total: number;
};

const data: OrderRow[] = [
  { id: "o1", customer: { name: "Ada", code: "A-100" }, total: 40 },
  { id: "o2", customer: { name: "Ben", code: "B-200" }, total: 12 },
];

function customerMatches(row: OrderRow, filterValue: unknown): boolean {
  const q = String(filterValue ?? "").toLowerCase();
  if (!q) return true;
  return (
    row.customer.name.toLowerCase().includes(q) ||
    row.customer.code.toLowerCase().includes(q)
  );
}

describe("global filter opt-in pilot", () => {
  it("pins the table packages named in the PR", () => {
    const pkg = JSON.parse(readFileSync("package.json", "utf8"));
    expect(pkg.dependencies["@tanstack/table-core"]).toBe("9.0.0-beta.64");
    expect(pkg.dependencies["@tanstack/vue-table"]).toBe("9.0.0-beta.64");
  });

  it("documents the #6439 fixture rows the product table must satisfy", () => {
    // Replace filterRows() with your real table.getFilteredRowModel() after
    // registering global filtering + an object column with enableGlobalFilter.
    const filterRows = (q: string) =>
      data.filter((row) => customerMatches(row, q)).map((r) => r.id);

    expect(filterRows("b-200")).toEqual(["o2"]);
    expect(filterRows("Ada")).toEqual(["o1"]);
  });
});
```

When you wire the real table instance, the acceptance criteria stay fixed:

1. Column accessor yields an **object** (not only `string` / `number`).
2. That column **explicitly opts into** global filtering.
3. A custom global filter function can read object fields.
4. Assertions use the **filtered row model**, not a hand-rolled array filter left in the test forever.

Until step 4 uses the library row model, mark the test `it.todo` or fail CI — a pure `array.filter` only proves you understand the bug class, not that the pinned beta honors opt-in.

{{< note type="note" title="Undefined first values" >}}
If you deliberately pin **beta.65**, add a fixture where the first row’s filterable field is `undefined` and a later row should still match. That is the #6438 class. Do not claim you tested it while pinned to `.64` only.
{{< /note >}}

### Gate 3 — Sort / filter / pagination parity matrix

| Surface | Fixture | Pass signal |
|---|---|---|
| Global filter | Object opt-in column (Gate 2) | Expected row ids only |
| Column filter | One discrete status filter combined with global filter | Intersection correct |
| Sort | Sort by total while filter active | Order stable and deterministic |
| Pagination | Page size 1 with two matches | Page count and page items agree with filter |
| Selection | Select filtered row, clear filter | Selection policy documented (keep vs clear) |
| SSR / hydrate | Dehydrate filtered state, hydrate client | No flicker to unfiltered full set |
| Worker path (if any) | Same fixture off main thread | Same row ids as main thread |

A green unit test on Gate 2 with a broken pagination footer is still a failed pilot.

![Six pilot gates checklist: pin exact, filter fixture, parity matrix, feature flag, owner sign-off, rollback command](/img/table-beta-is-still-a-pilot-decision-3.png)

### Gate 4 — Feature flag and surface allow-list

```typescript
// config/tablePilot.ts
export const TABLE_PILOT = {
  enabled: process.env.TABLE_V9_PILOT === "1",
  // Exact strings only — never "beta"
  tableCore: "9.0.0-beta.64",
  vueTable: "9.0.0-beta.64",
  routes: ["/internal/ops/orders-pilot"],
  exitDate: "2026-08-15",
  owner: "orders-admin",
} as const;
```

Production routes keep importing the stable-locked module path. Pilot routes import through a single factory that throws if the env flag is off. No shared “smart” resolver that picks beta because `NODE_ENV !== "production"` — staging surprises are still surprises.

### Gate 5 — Named owner and exit

Write these four lines in the PR body before anyone merges:

```markdown
## Table pilot exit
- Owner: @handle (orders-admin)
- Success: Gate 2–3 green on CI + dogfood tenant for 5 business days
- Graduate: only with stable pin plan or continued exact beta pin + flag
- Rollback: `git revert <sha>` + `pnpm install` restores 8.21.3 lockfile entries
- Kill date: 2026-08-15 (remove flag and spike deps if not graduated)
```

No owner means the beta becomes permanent platform drift with a cheerful name.

### Gate 6 — Rollback command you have actually run

```bash
#!/usr/bin/env bash
# scripts/rollback-table-pilot.sh
set -euo pipefail

git checkout main -- package.json pnpm-lock.yaml
pnpm install --frozen-lockfile
pnpm run test:tables
echo "table pilot rolled back to locked stable"
```

If rollback needs a hero and a spreadsheet, you do not have rollback. You have hope.

## Green signals that still lie

| Green signal | What it usually proves | What beta.64 still needs |
|---|---|---|
| `pnpm install` exit 0 | Something resolved | Exact `9.0.0-beta.64` (or chosen tag) on every install path |
| Storybook table renders | Chrome mounts | Object-column global search on a product route |
| `vite build` exit 0 | Bundle compiles | Filter + sort + page footer agree after search |
| “Reactivity tests upstream” | Upstream cares | Your adapter version and your state wiring |
| Demo tenant “looks fine” | One happy path | Undefined values, empty filter, selection after clear |
| CI unit tests on strings only | Strings work | #6439 class never executed |

This is the same honesty pattern as [UI kit lockfile bumps](/blog/ui-kit-bump-is-change-control/) and [runtime patch inventories](/blog/php-8-5-9-runtime-patch-inventory/): green is not done until the artifact that would catch *this* failure mode exists.

## Build-in-public: how I would run the spike this weekend

Saturday rotation is build-in-public. Here is the boring sequence I want on a real orders grid, not a toy:

1. Branch from main with production still on **8.21.3**.
2. Add exact **beta.64** pins (or explicitly **beta.65** if you want #6438 in the same spike — write it down).
3. Land Gate 2 fixture first, before any visual polish.
4. Wire one internal route behind `TABLE_V9_PILOT=1`.
5. Run the parity matrix once on main thread; if you have a worker row-model path, run it twice.
6. Paste Gate 5 exit block into the PR; set the kill date on a calendar, not in chat.
7. Dogfood Monday with support/ops, not only engineering.

If step 3 is skipped because “we will add tests after the UI feels right,” stop. That ordering is how betas become load-bearing without evidence.

{{< details summary="Optional: package identity assert at boot (pilot route only)" >}}

```typescript
// pilot/assertTablePilotVersion.ts
import { TABLE_PILOT } from "../config/tablePilot";

export function assertTablePilotVersion(actualCore: string, actualVue: string) {
  if (actualCore !== TABLE_PILOT.tableCore || actualVue !== TABLE_PILOT.vueTable) {
    throw new Error(
      `table pilot version drift: core ${actualCore} vue ${actualVue} ` +
        `expected ${TABLE_PILOT.tableCore} / ${TABLE_PILOT.vueTable}`,
    );
  }
}
```

Resolve `actual*` from your lockfile audit at build time or from a tiny generated module — not from a hand-edited constant that can desync.

{{< /details >}}

## What this post is not claiming

- That npm `latest` has left **8.21.3** for a stable v9 line (it has not, as of this writing).
- That beta.64 is safe for all Vue SSR apps.
- That you should jump from 8.21.3 on the strength of one filter fix.
- That upstream reactivity tests replace your product fixtures.
- Personal outage numbers, invented benchmarks, or unofficial performance wins.

If official docs later publish a migration guide section for global-filter opt-in defaults, update the fixture — do not replace the gate list with vibes.

## What you should do Monday morning

1. Open the npm package pages or registry JSON for `@tanstack/vue-table` and `@tanstack/table-core`. Write down **`latest`** and **`beta`** dist-tags in the ticket. If they differ from this post, trust the registry, not the article date.
2. Confirm production lockfiles still resolve **8.21.3** (or your chosen stable pin). If anything floats on `beta`, fix that before any feature work.
3. If you are not piloting v9, stop here. Add a calendar note to re-check monthly. Do not open a “quick bump” PR from a social link.
4. If you are piloting, create a branch that pins **one** exact beta (document `.64` vs `.65`) and commits the lockfile.
5. Add the object-column global-filter fixture (Gate 2). Make CI fail when it fails.
6. Fill the parity matrix (Gate 3) for every table surface you already ship: filter, sort, page, selection, hydrate, worker.
7. Put owner, kill date, and rollback command in the PR body (Gate 5–6). Merge only behind a flag.
8. Link the PR to your internal [developer tools](/developer-tools/) change-control doc or the public hub so the next person does not rediscover the same gates from scratch.

## Further reading

- {{< source href="https://github.com/TanStack/table/releases/tag/v9.0.0-beta.64" label="GitHub: TanStack Table v9.0.0-beta.64" >}} — primary release body for the global-filter opt-in fix.
- {{< source href="https://github.com/TanStack/table/pull/6439" label="GitHub PR #6439" >}} — rationale for explicit opt-in vs primitive heuristic.
- {{< source href="https://tanstack.com/table/latest" label="TanStack Table docs" >}} — current documentation entry; verify beta vs latest paths before copying snippets.
- Related on this site: [Before You Adopt a Beta Library, Prove the Exit Path](/blog/before-you-adopt-a-beta-library-prove-the-exit-path/), [TanStack Table v9 row-model workers](/blog/tanstack-table-v9-row-model-workers/), [Vue Query cache invalidation contract](/blog/vue-query-cache-invalidation-contract/), hubs: [/developer-tools/](/developer-tools/), [/laravel-vue-saas/](/laravel-vue-saas/), [/start-here/](/start-here/).

A beta bump can be the right engineering move. Calling it done because upstream added filter tests is how quiet registry tags become loud Monday incidents. Pin the version, own the fixture, name the exit.
