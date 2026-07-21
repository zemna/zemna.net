---
title: "ApexCharts 6.4 Is a Dashboard Contract Migration, Not a Package Bump"
date: 2026-07-21T07:00:00+07:00
draft: false
slug: apexcharts-6-4-dashboard-contract
description: "ApexCharts 6.4 changes heatmap geometry, rendering imports, and interaction defaults. Treat the upgrade as a dashboard contract migration with visual and behavioral tests."
topics: ["frontend-engineering"]
tags: ["apexcharts", "heatmaps", "vue", "dashboard-maintenance", "frontend-engineering"]
cover: /covers/apexcharts-6-4-dashboard-contract.png
seo:
  primaryQuery: "ApexCharts 6.4 migration"
  secondaryQueries:
    - "ApexCharts heatmap canvas renderer"
    - "ApexCharts irregular datetime heatmap"
    - "vue3-apexcharts compatibility"
---

A charting dependency can change a dashboard without changing a single API endpoint. That is the uncomfortable part of an ApexCharts 6.4 upgrade.

The release was published on 2026-07-20, and it changes the rules that turn a heatmap data point into pixels, interaction, and labels. It also introduces an opt-in Canvas renderer with its own import requirement and fallback behavior. Those are dashboard contracts: visible agreements between your data, your configuration, and the people who use the screen. [The v6.4.0 release notes](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0) are the source for those changes.

Calling this a package bump invites the wrong workflow: update the lockfile, click through a happy-path page, and merge. A dashboard has too many quiet dependencies for that. A support manager may rely on a tooltip staying near the pointer. An operations user may rely on zoom to inspect a dense time range. A weekly activity heatmap may rely on every row label remaining visible. None of those expectations appears in a TypeScript import statement.

This post treats 6.4 as a controlled migration for a Laravel/Vue SaaS dashboard: inspect the current contract, choose the new behavior deliberately, and prove both the preferred path and the rollback path. The same approach applies outside Laravel and Vue. If you are building or maintaining the stack described in [Laravel + Vue SaaS](/laravel-vue-saas/), use the chart as an owned interface, not as decorative output from a dependency.

![ApexCharts 6.4 dashboard contract migration overview](/img/apexcharts-6-4-dashboard-contract-1.png)

## The release changes a dashboard's observable contract

A contract is broader than a function signature. For a heatmap, it includes where a cell sits, what a hover reveals, whether a user can zoom, which labels survive density controls, and whether the renderer produces the expected output. Those behaviors are visible. Once users learn them, they become part of the product.

ApexCharts 6.4 contains three categories of change that deserve separate review:

| Area | What must be treated as a contract |
|---|---|
| Heatmap geometry | Numeric and datetime cells can follow their real x values rather than an even category grid. |
| Rendering path | Canvas is optional and requires an explicit feature import; unsupported fills use SVG instead. |
| Default behavior | Tooltip placement, zoom, and y-axis label density changed for heatmaps. |

The release states that irregular numeric and datetime heatmaps position cells at their actual x values. It also documents the Canvas import, SVG fallback for unsupported fills, and the changed heatmap defaults. Read those claims in the [v6.4.0 release notes](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0), then test them against the charts you ship.

This is why release notes should become test inputs. Do not translate “irregular data now uses real x positions” into “the chart is more correct” and move on. Translate it into a fixture with irregular values, a named expected behavior, and a screenshot or DOM-level assertion that someone can review during a future upgrade.

The same discipline matters when the release includes performance results. Any benchmark in the release belongs to the upstream harness that produced it. It is evidence about that harness, not a promise about your browser mix, dataset shape, page composition, or user-perceived dashboard speed. The release itself is the only appropriate source for those figures; do not turn them into a product SLA. [ApexCharts v6.4.0 release notes](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0)

A useful migration ticket therefore has a different title from “upgrade ApexCharts.” Name the affected screens and their behavior: “Preserve incident-heatmap tooltip and zoom behavior while adopting real-x positioning.” That wording forces a conversation about the user-facing contract before implementation details take over.

## Real x positions change the meaning of an irregular heatmap

Many dashboards receive telemetry or business events at uneven intervals. A numeric x value may be a batch number, queue depth, or elapsed minute. A datetime x value may represent an event that occurred after a gap. When a renderer treats those entries as evenly spaced categories, the eye reads equal distance where the underlying values are not equally spaced.

ApexCharts 6.4 changes this for irregular numeric and datetime heatmaps: cells are positioned at their real x values. That is an intentional release behavior, documented in the [v6.4.0 notes](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0). If your heatmap already uses evenly spaced categories, the visual result may remain familiar. If it contains gaps, the plot can visibly redistribute itself after the upgrade.

Use an explicit fixture that makes gaps impossible to miss. This is a plain ApexCharts configuration that uses datetime x values with an intentional two-hour break:

```typescript
import ApexCharts from "apexcharts";

const options: ApexCharts.ApexOptions = {
  chart: {
    type: "heatmap",
    height: 280,
  },
  series: [
    {
      name: "API errors",
      data: [
        { x: new Date("2026-07-20T08:00:00Z").getTime(), y: 1 },
        { x: new Date("2026-07-20T08:05:00Z").getTime(), y: 4 },
        { x: new Date("2026-07-20T10:10:00Z").getTime(), y: 2 },
      ],
    },
  ],
  xaxis: {
    type: "datetime",
  },
};

const chart = new ApexCharts(document.querySelector("#error-heatmap"), options);
chart.render();
```

Keep this fixture small. A chart with thousands of points is useful for load testing, but it is poor at explaining a geometry change in code review. Three values with an obvious gap answer the important question: does the horizontal distance represent the values we supplied?

There is a product decision hidden inside that question. Real positions may expose downtime, missing collection windows, sparse activity, or gaps caused by filters. That can be the correct visual story. It can also surprise a team whose existing dashboard used a heatmap as a compact categorical matrix. Do not “fix” the new spacing with CSS until you have agreed which story the chart should tell.

Capture a before-and-after image for each affected chart family, not just the first dashboard page. The same wrapper may feed different x-axis types in billing, monitoring, fulfillment, and admin reporting. Search your codebase for `type: "heatmap"`, then classify each chart by x data: categories, numbers, or dates. This belongs in the upgrade checklist alongside version changes.

![Irregular heatmap values preserve meaningful gaps](/img/apexcharts-6-4-dashboard-contract-2.png)

{{< note >}}
If a heatmap represents a category grid, make the x values categories and test the grid. If it represents elapsed or calendar time, preserve numeric or datetime values and accept that gaps should occupy space. The model and the visual contract should agree.
{{< /note >}}

## Canvas is an explicit renderer choice, not a silent acceleration switch

The 6.4 release adds a Canvas heatmap renderer, but it does not turn on merely because the package version changes. The documented requirement is an explicit side-effect import:

```typescript
import ApexCharts from "apexcharts";
import "apexcharts/features/renderer-canvas";
```

That import is required for the Canvas heatmap renderer according to [the v6.4.0 release](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0). Put it in a deliberate client-side entry point. Do not scatter it through leaf components, where route-level code splitting can make the renderer's availability hard to reason about.

The release also says Canvas falls back to SVG for unsupported fills. That matters because “the chart rendered” does not prove it used Canvas. A fallback can be the intended compatibility behavior, but your tests need to distinguish expected output from an assumption that every heatmap has the same renderer. [ApexCharts v6.4.0](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0)

For a Vue application, keep registration and client-only rendering separate. The following component setup is syntactically usable in a client-rendered Vue app. It shows the shape of the integration, not a claim that any wrapper supports ApexCharts 6.4:

```typescript
// src/charting/apexcharts-client.ts
import ApexCharts from "apexcharts";
import "apexcharts/features/renderer-canvas";

export function createHeatmap(
  element: Element,
  options: ApexCharts.ApexOptions,
): ApexCharts {
  const chart = new ApexCharts(element, options);
  void chart.render();
  return chart;
}
```

```vue
<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import type ApexCharts from "apexcharts";
import { createHeatmap } from "@/charting/apexcharts-client";

const root = ref<HTMLElement | null>(null);
let chart: ApexCharts | undefined;

onMounted(() => {
  if (!root.value) return;

  chart = createHeatmap(root.value, {
    chart: { type: "heatmap", height: 260 },
    series: [{ name: "Jobs", data: [{ x: 1, y: 8 }, { x: 5, y: 3 }] }],
  });
});

onBeforeUnmount(() => {
  chart?.destroy();
});
</script>

<template>
  <div ref="root" />
</template>
```

Whether you use direct ApexCharts or a wrapper, add an explicit renderer test matrix: supported fill, unsupported fill, a realistic sparse dataset, and the exact browser targets your application supports. Do not write a test that asserts implementation details you cannot observe. A visual regression image plus a successful interaction test is stronger than a test that merely checks that a module was imported.

{{< field-note title="Field note" >}}
Laravel/Vue SaaS maintenance is often decided by handoff clarity and local operating constraints, so a dashboard upgrade needs a written renderer decision, a reproducible fixture, and a rollback version before someone else has to diagnose a different chart on a busy day.
{{< /field-note >}}

## The new defaults can break muscle memory without throwing an error

ApexCharts 6.4 changes three heatmap defaults: the tooltip appears above the cell, zoom is disabled, and y-axis labels are thinned. All three are documented in [the release notes](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0). None necessarily produces an exception. That is what makes them migration work.

Tooltip placement affects the hand and eye. A user who hovers across a row expects the value to appear in a stable place relative to the cell or pointer. Disabling zoom changes a familiar escape hatch for reading dense screens. Label thinning can remove context from a chart whose row names are the whole point. A shipping dashboard, for example, may have a short visible chart but many meaningful lanes. A chart that hides labels may remain technically legible while becoming operationally weaker.

The release provides explicit ways to restore the earlier behavior: set `tooltip.followCursor` to `true`, set `chart.zoom.enabled` to `true`, and provide a custom `yaxis.labels.formatter`. Use those settings only after checking why the new defaults exist and whether the old interaction still fits the current chart. [ApexCharts v6.4.0](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0)

Here is a concrete preservation configuration:

```typescript
const options: ApexCharts.ApexOptions = {
  chart: {
    type: "heatmap",
    zoom: {
      enabled: true,
    },
  },
  tooltip: {
    followCursor: true,
  },
  yaxis: {
    labels: {
      formatter: (value: string) => value,
    },
  },
  series: [
    { name: "Payments", data: [{ x: "Mon", y: 12 }, { x: "Tue", y: 7 }] },
  ],
};
```

Treat that snippet as a compatibility choice, not ceremonial configuration. Add an interaction test that drags or uses the zoom control according to your application flow. Add a visual test at the narrowest supported dashboard width to prove the y labels are still useful. Hover a cell and inspect the tooltip position. When your team later decides to accept the 6.4 defaults, remove these settings with the same test coverage instead of letting them linger as cargo-cult options.

![Dashboard default behavior and rollback checklist](/img/apexcharts-6-4-dashboard-contract-3.png)

## Vue wrapper status is a separate compatibility question

A core-library release and a wrapper release are separate facts. The npm page for [`vue3-apexcharts`](https://www.npmjs.com/package/vue3-apexcharts) lists version 1.11.1. That version number does not establish compatibility with ApexCharts 6.4, and it does not establish Nuxt SSR compatibility. The official sources named here do not provide that guarantee, so do not claim one in an upgrade plan.

This boundary changes the order of work. First, test the direct ApexCharts package and the charts you own. Then test the wrapper where it is actually used. Finally, test the server-rendered build and hydration path if your app uses Nuxt or another SSR setup. A page that works after client navigation may still fail in a server render or hydrate into a different DOM shape.

A practical repository check can surface where the wrapper enters the app:

```javascript
// scripts/find-apexcharts-usage.mjs
import { glob } from "glob";
import { readFile } from "node:fs/promises";

const files = await glob(["src/**/*.{ts,tsx,vue}", "pages/**/*.vue", "components/**/*.vue"]);
const pattern = /vue3-apexcharts|apexcharts\/features\/renderer-canvas|type:\s*["']heatmap["']/;

for (const file of files) {
  const source = await readFile(file, "utf8");
  if (pattern.test(source)) console.log(file);
}
```

Run a tool like this before changing imports. It tells you whether you have direct usage, wrapper usage, or both. Then build a small test page for each path. For SSR, render the route in the same mode your deployment uses, then load it in a browser and check hydration, resize behavior, hover, and teardown after navigation.

Do not solve uncertainty by upgrading the wrapper and core together, then declaring victory after one local page. Keep the dependency boundary visible in the pull request. State what the sources confirm: ApexCharts 6.4 behavior comes from [its release](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0), while the npm listing shows `vue3-apexcharts` 1.11.1. Everything else requires your own compatibility test.

![Test ApexCharts core and Vue wrapper separately](/img/apexcharts-6-4-dashboard-contract-4.png)

## What you should do Monday morning

1. Create a branch that changes only the ApexCharts dependency and its lockfile. Record the current package version and the rollback command in the pull request before testing begins.
2. Search for every heatmap and classify its x data as category, numeric, or datetime. Add one irregular numeric or datetime fixture wherever real spacing matters, because 6.4 places those cells at real x values. [Release source](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0)
3. Take baseline screenshots at desktop and narrow dashboard widths. Include a hovered cell, the complete y-axis label set, and any zoomed state users rely on.
4. Decide chart by chart whether to adopt the new defaults or preserve the old behavior. If preservation is required, add `tooltip.followCursor: true`, `chart.zoom.enabled: true`, and a `yaxis.labels.formatter`, then test each behavior. Those restoration options are documented in the [v6.4.0 release](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0).
5. If you want Canvas heatmaps, add `import "apexcharts/features/renderer-canvas";` in a controlled client entry point. Test a fill you expect to render with Canvas and a fill that may use the documented SVG fallback. [Release source](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0)
6. Test direct ApexCharts and `vue3-apexcharts` separately. The npm listing identifies the wrapper as 1.11.1; it does not certify 6.4 or Nuxt SSR compatibility. [npm source](https://www.npmjs.com/package/vue3-apexcharts)
7. Run the real production build, open the affected routes, navigate away and back, resize, hover, zoom where applicable, and compare screenshots. Keep the old dependency version ready until those checks pass.
8. Write the decisions into the maintenance record. Link the chart fixtures, screenshots, chosen renderer path, accepted default changes, and rollback point from your [developer tools](/developer-tools/) notes so the next maintainer does not have to reconstruct the reasoning from a lockfile.

The goal is not to preserve every old pixel. The goal is to make intentional changes, expose them in review, and keep evidence for the next package update. That is ordinary engineering work, but dashboards punish teams that skip it.

## Further reading

- {{< source title="ApexCharts v6.4.0 release notes" url="https://github.com/apexcharts/apexcharts.js/releases/tag/v6.4.0" >}}
- {{< source title="vue3-apexcharts on npm" url="https://www.npmjs.com/package/vue3-apexcharts" >}}
- Start with the site's [orientation page](/start-here/) if you are new to the maintenance notes and frontend writing on zemna.net.
