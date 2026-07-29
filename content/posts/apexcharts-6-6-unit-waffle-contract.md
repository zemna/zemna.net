---
title: "ApexCharts 6.6 unit and waffle charts are a product decision, not a type swap"
date: 2026-07-29T07:00:00+07:00
draft: false
slug: "apexcharts-6-6-unit-waffle-contract"
description: "ApexCharts 6.6 adds premium unit and waffle charts with trial watermarks, tree-shakeable imports, and TypeScript options. Treat adoption as a license, fixture, accessibility, and rollback contract."
topics: ["developer-tools"]
tags: ["apexcharts", "unit-chart", "waffle-chart", "dashboard", "vue", "licensing", "frontend-maintenance"]
cover: /covers/apexcharts-6-6-unit-waffle-contract.png
seo:
  primaryQuery: "ApexCharts 6.6 unit waffle chart"
  secondaryQueries:
    - "ApexCharts premium unit chart license"
    - "ApexCharts waffle chart import"
    - "vue3-apexcharts unit chart compatibility"
---

A new chart type looks like a one-line config change. In a SaaS dashboard, it is rarely that small.

ApexCharts **6.6.0**, published on 2026-07-27, introduces the first premium chart type in the library: `unit`, with `waffle` as a thin alias. The release is explicit that the feature renders in trial mode with an `APEXCHARTS` watermark until a license key is set, that other chart types stay free and unwatermarked, and that existing configs render unchanged. Those three sentences already change the maintenance conversation. You are no longer choosing between `pie` and `donut`. You are choosing whether a paid, watermarked, opt-in visualization path belongs in a product surface that support, sales, and compliance will see.

The question is not whether the demo looks clever. The question is whether the change survives license review, handoff, SSR, accessibility checks, and a clean rollback when the new type is the wrong fit.

<!--more-->

![A new chart type is a product contract, not a one-line type swap](/img/apexcharts-6-6-unit-waffle-contract-1.png)

## What 6.6 actually shipped

Ground the work in the primary release, not a secondary summary. The [ApexCharts v6.6.0 release notes](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.6.0) describe:

| Claim from the release | Operational meaning |
|---|---|
| New premium chart type `unit` | Discrete mark per unit of value: dots, pictograms, waffles, beeswarms |
| `waffle` alias | Thin preset of `unit` that selects the grid layout with square cells |
| Trial mode watermark until a key is set | Customer-visible branding unless licensing is configured |
| Tree-shakeable `import 'apexcharts/unit'` | Bundle and entry-point decisions, not only options JSON |
| Six layouts via `plotOptions.unit.layout` | Geometry and interaction surface is larger than one sample |
| TypeScript coverage for `plotOptions.unit` and `chart.type` `'unit'\|'waffle'` | Types help, they do not replace visual fixtures |
| No breaking API changes for existing chart types | Core charts can stay put while you evaluate the premium path separately |
| License manager gains signature verification | License injection is part of the runtime surface |
| Zoom-out edge-case fix | Orthogonal fix; do not fold it into the unit adoption ticket |

npm currently lists `apexcharts` **latest** as **6.6.1**. There is **no** matching GitHub release tag or body for `v6.6.1` at collection time, so this article does not invent patch details for 6.6.1. Pin and test against the version you actually install, and treat the verified GitHub body of **6.6.0** as the feature contract for unit and waffle.

The official waffle guide states the same product boundary: waffle shares the unit engine, is a Premium chart type, renders with an `APEXCHARTS` watermark without a license key, and is enabled with `import 'apexcharts/unit'`. [Source: https://apexcharts.com/docs/chart-types/waffle-chart/]

{{< note type="warning" title="Do not invent 6.6.1 behavior" >}}
If lockfiles resolve to `6.6.1` while GitHub only documents `v6.6.0`, record both facts in the PR. Feature claims in this post come from the 6.6.0 release body and the waffle documentation. Patch-level differences for 6.6.1 remain unverified without primary notes.
{{< /note >}}

## Why a premium chart type is a product decision

Most dashboard teams treat chart libraries as presentation glue. Bar, line, area, and pie already sit behind KPI cards. A designer asks for a “friendlier pie,” a developer finds `type: 'waffle'`, and the PR title becomes “improve energy mix visualization.”

That framing hides the real decisions:

1. **Commercial path** — premium feature, trial watermark, license key placement, and who pays.
2. **Default chart inventory** — which screens are allowed to depend on premium types.
3. **Accessibility and density** — discrete marks behave differently from continuous geometry for keyboard users and dense data.
4. **Wrapper and SSR lag** — core package movement does not move `vue3-apexcharts` automatically.
5. **Rollback** — can you return to a free chart type without a product incident?

The release itself frames unit as the first premium chart type and states that every other chart type stays free and is never watermarked. That asymmetry is the point. You can keep shipping ordinary charts under the existing license conversation and still refuse a watermarked or paid path on customer-facing admin screens until legal and product agree.

{{< field-note title="Field note" >}}
On Laravel + Vue SaaS admin work, chart upgrades fail in review for the same reason agent-driven migrations fail: the diff looks local, the blast radius is not. When a premium type shows a vendor watermark in a client demo, the incident is not “CSS.” It is an unowned commercial boundary. I keep chart-type allow-lists next to the same kind of change-control notes used for coding-agent policy and dependency upgrades under [developer tools](/developer-tools/) and [Laravel + Vue SaaS](/laravel-vue-saas/). The rule is boring on purpose: no new premium chart type reaches a shared environment until license mode, screenshot fixtures, and a free fallback type are named in the PR.
{{< /field-note >}}

![Five gates before adopting unit or waffle charts](/img/apexcharts-6-6-unit-waffle-contract-2.png)

## Gate 1 — License and watermark before aesthetics

Official npm documentation for ApexCharts describes premium features and licensing: without a valid key, premium features still work in trial mode but show an `APEXCHARTS` watermark; a valid key removes it. The unit chart type, aliased by waffle, is the premium chart type called out there. License can be set globally with `ApexCharts.setLicense(...)`, via `window.Apex = { license: '...' }`, or per chart with `chart.license`. [Source: https://www.npmjs.com/package/apexcharts]

That means a staging environment that “looks fine” without a key is not proof of production readiness. It is proof that trial mode is easy to forget.

Use an explicit startup path and fail closed in environments that must not show vendor chrome:

```typescript
// resources/js/charts/apex-license.ts
import ApexCharts from "apexcharts";

/**
 * Call once on the client before any chart render.
 * Keep the raw key out of the SPA bundle when your threat model requires it:
 * inject from a server-rendered meta tag or a short-lived config endpoint.
 */
export function configureApexLicense(): void {
  const key = import.meta.env.VITE_APEXCHARTS_LICENSE_KEY as string | undefined;

  if (!key) {
    if (import.meta.env.PROD) {
      throw new Error(
        "Missing VITE_APEXCHARTS_LICENSE_KEY. Refusing premium chart boot in production."
      );
    }
    // Local dev may intentionally exercise trial watermark screenshots.
    return;
  }

  ApexCharts.setLicense(key);
}
```

Pair that with a product rule, not only an env var:

| Environment | Allowed unit/waffle mode | Evidence |
|---|---|---|
| Local developer machine | Trial watermark OK for exploration | Screenshot labeled `trial` |
| Shared staging / client demo | Licensed only | Screenshot without watermark + key injection path documented |
| Production | Licensed only, or free chart type fallback | Same as staging, plus rollback type named |

Pricing and plan packaging change over time. The public pricing and license pages describe Community, Commercial, Pro, Premium, and OEM options; waffle documentation currently points premium waffle availability at Premium and OEM plans. Do not hard-code prices into architecture docs as eternal facts. Link the current [pricing](https://apexcharts.com/pricing/) and [license](https://apexcharts.com/license/) pages in the PR and re-check them when finance renews.

{{< note type="note" title="Core dual-license is separate from premium chart gating" >}}
ApexCharts also documents a revenue-based dual-license model for the library itself (Community under a revenue threshold, Commercial above it). That conversation is related but not identical to “this chart type watermarks until a key is set.” Keep both checks on the adoption ticket: org eligibility for the core library, and premium-feature key handling for unit/waffle.
{{< /note >}}

## Gate 2 — Import path and TypeScript surface

The release and waffle docs agree on the opt-in import. With a tree-shakeable core, waffle and unit are not free just because the package is installed:

```typescript
// resources/js/charts/unit-chart.ts
import ApexCharts from "apexcharts/core";
import "apexcharts/unit"; // serves both chart.type 'unit' and 'waffle'

import { configureApexLicense } from "./apex-license";

configureApexLicense();

export type MixSlice = {
  label: string;
  value: number;
};

export function renderEnergyWaffle(
  el: HTMLElement,
  slices: MixSlice[]
): ApexCharts {
  const chart = new ApexCharts(el, {
    chart: {
      type: "waffle",
      height: 320,
      animations: { enabled: true },
    },
    series: slices.map((s) => s.value),
    labels: slices.map((s) => s.label),
    plotOptions: {
      unit: {
        // waffle alias presets grid + square; options still live under plotOptions.unit
        grid: {
          total: 100,
          columns: 10,
          fillFrom: "bottom",
        },
      },
    },
    legend: {
      show: true,
      position: "bottom",
    },
  });

  chart.render();
  return chart;
}
```

The same release documents a direct unit example with layouts such as `grouped`:

```javascript
// Minimal unit example adapted from the v6.6.0 release body.
// Prefer fixture data that matches a real KPI, not marketing sample counts.
new ApexCharts(document.querySelector("#vote-units"), {
  chart: { type: "unit" },
  series: [276, 266, 3],
  labels: ["For", "Against", "Abstain"],
  plotOptions: {
    unit: {
      layout: "grouped",
    },
  },
});
```

Layouts listed in the release body: `grouped` (default), `packed`, `columns`, `grid`, `grid` with `split: true`, and `scatter` (including beeswarm and bubble variants). Shapes include `circle`, `square`, and `image` pictograms. Transitions include `group`, `flow`, and `identity`. That is a large combinatorial surface. Do not approve “we turned on waffle” without naming the layout, shape, and update behavior you will support.

TypeScript accepting `'unit' | 'waffle'` is helpful. It is not a visual test. A green `tsc` run does not prove the watermark is gone, that legend toggles reflow marks correctly, or that a 10×10 percentage waffle still reads at mobile width.

![Free chart path versus premium unit and waffle path](/img/apexcharts-6-6-unit-waffle-contract-3.png)

## Gate 3 — Fixtures beat demo pages

Release notes ship demos. Products ship contracts. Build fixtures that encode the decisions you refuse to rediscover later.

```typescript
// tests/fixtures/apex-unit-contract.ts
export const energyMixFixture = {
  id: "energy-mix-waffle-100",
  chartType: "waffle" as const,
  layout: "grid",
  grid: { total: 100, columns: 10, fillFrom: "bottom" as const },
  series: [35, 23, 15, 9, 8, 6, 4],
  labels: ["Coal", "Gas", "Hydro", "Nuclear", "Wind", "Solar", "Other"],
  // Expected after largest-remainder allocation to 100 cells — assert in visual or unit harness
  expectedCellSum: 100,
  fallbackType: "donut" as const,
  requiresLicense: true,
};

export const adoptionChecklist = [
  "license mode screenshot (trial vs licensed)",
  "import path uses apexcharts/unit",
  "layout and shape pinned in fixture",
  "legend hide/show reflow checked",
  "narrow width readability checked",
  "keyboard/ARIA smoke checked",
  "wrapper path tested if vue3-apexcharts is used",
  "SSR/hydration path tested if Nuxt or equivalent is used",
  "fallback free chart type renders with same labels/series",
  "rollback PR description names the free type and version pin",
] as const;
```

For percentage waffles, the docs state that `grid.total: 100` uses a largest-remainder rule so cells sum exactly to the budget. That is a perfect automated assertion target. For `grid.split: true`, each tile is a mini-waffle with its own track — assert tile count and labels, not only total series length.

```bash
# scripts/check-apex-unit-usage.sh
# Fail CI if premium types appear without the unit import in the same package graph area.
set -euo pipefail

if rg -n "type:\\s*['\"]waffle['\"]|type:\\s*['\"]unit['\"]" resources/js apps --glob '!**/node_modules/**'; then
  if ! rg -n "apexcharts/unit" resources/js apps --glob '!**/node_modules/**'; then
    echo "unit/waffle usage found without apexcharts/unit import" >&2
    exit 1
  fi
fi
```

Keep the fallback cheap. If unit or waffle is rejected for license, density, or accessibility reasons, the same labels and series should render as a donut or bar without a second product design cycle.

## Gate 4 — Accessibility and density are first-class

Discrete marks sell “countability.” They also change the failure modes:

- A 100-cell waffle is readable when categories are few and proportions are coarse.
- The same waffle becomes noise when you push ten near-equal categories or update every second.
- Pictogram/`image` marks can fail contrast and meaning when icons are decorative rather than encoded.
- Legend click reflow and animated transitions can be motion-heavy; respect reduced-motion settings in your app shell even if the chart demo celebrates tweening.

ApexCharts documents keyboard navigation and ARIA support at the library level on npm marketing copy. That is not a certificate for your specific unit layout. Run a short manual harness:

1. Tab to the chart region and any focusable controls your wrapper exposes.
2. Toggle a legend item if the chart uses one; confirm the remaining marks still make sense.
3. Capture the chart at the narrowest supported admin width.
4. Compare against the free fallback type with the same data.

If the chart only works as a large decorative panel, it does not belong in a dense operations table view. Put it on an analytics page with room, or keep the free chart.

{{< details summary="Layout shortlist for first production use" >}}
Start with one layout, not six.

- **waffle / grid + total 100** — part-to-whole percentages; easiest story for stakeholders.
- **unit + grouped** — category comparison with countable dots; good for small integer KPIs.
- Defer **scatter / beeswarm / image pictograms** until you have fixtures for axes, packing determinism, and icon contrast.

The release lists all six layouts; your product does not need to support all six on day one.
{{< /details >}}

## Gate 5 — Wrapper and SSR are separate version facts

`vue3-apexcharts` remains **1.11.1** on npm at collection time (last publish timestamp in 2026-03). Core moving to 6.6.x does not prove the Vue wrapper, Nuxt plugins, or your client-only boundaries understand premium chart types.

Test in this order:

1. Direct `apexcharts` + `import 'apexcharts/unit'` on a plain page.
2. The same config through `vue3-apexcharts` if that is how production mounts charts.
3. SSR route render + client hydration if you use Nuxt or another meta-framework.
4. Navigation away/back, resize, and teardown.

```vue
<!-- resources/js/components/EnergyMixWaffle.vue -->
<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import type ApexCharts from "apexcharts";
import { renderEnergyWaffle, type MixSlice } from "../charts/unit-chart";

const props = defineProps<{ slices: MixSlice[] }>();
const host = ref<HTMLElement | null>(null);
let chart: ApexCharts | null = null;

onMounted(() => {
  if (!host.value) return;
  chart = renderEnergyWaffle(host.value, props.slices);
});

onBeforeUnmount(() => {
  chart?.destroy();
  chart = null;
});
</script>

<template>
  <div
    ref="host"
    class="energy-mix-waffle"
    role="img"
    :aria-label="`Energy mix waffle for ${slices.length} categories`"
  />
</template>
```

If the wrapper lags or hydration flickers, keep the free chart on SSR routes and load unit/waffle only after client mount with a skeleton that does not claim false precision.

This is the same separation used when ApexCharts 6.4 changed heatmap contracts: core release notes define core behavior; wrapper compatibility is an independent check. See the earlier maintenance write-up on the [ApexCharts 6.4 dashboard contract](/blog/apexcharts-6-4-dashboard-contract/).

![Version facts for core, npm, wrapper, and SSR](/img/apexcharts-6-6-unit-waffle-contract-4.png)

## How this differs from the 6.4 dashboard contract

The 6.4 work was about heatmap geometry, Canvas imports, and default interaction drift on charts many teams already shipped. The 6.6 work is about **introducing a paid visualization path**.

| Dimension | 6.4 theme | 6.6 unit/waffle theme |
|---|---|---|
| Primary risk | Silent visual/behavior drift on existing heatmaps | Watermark, license, and product approval on a new type |
| Import concern | Optional Canvas renderer feature import | Required `apexcharts/unit` for tree-shakeable builds |
| Default posture | Preserve or accept new heatmap defaults | Default remain on free types until gates pass |
| Rollback | Restore options / previous renderer path | Swap back to pie/donut/bar with same series |
| Success signal | Screenshots and interaction tests match the chosen contract | Licensed screenshot + fixture + free fallback both green |

Keep both posts in the maintenance index. They are related and not duplicates.

## What good rejection looks like

Not every shiny chart type should merge. A successful evaluation can end with “no.”

Reject unit/waffle when:

- Finance will not approve premium packaging for the surfaces that need it.
- The watermark appears in any shared environment under the current key injection design.
- The data updates too fast for discrete mark transitions to stay readable.
- Accessibility review fails contrast, motion, or keyboard checks.
- The free fallback already answers the user question with less operational risk.

Write the rejection into the same doc as an approval would use. Future you will thank present you when someone pastes a Dribbble waffle and asks why the app still uses a donut.

## What you should do Monday morning

1. Read the primary [v6.6.0 release notes](https://github.com/apexcharts/apexcharts.js/releases/tag/v6.6.0) and the [waffle chart guide](https://apexcharts.com/docs/chart-types/waffle-chart/). Copy the claims you care about into the PR description with links.
2. Record the installed versions: `apexcharts` (likely 6.6.0 or 6.6.1 from npm) and `vue3-apexcharts` (currently 1.11.1 if unchanged). Note that 6.6.1 has no GitHub release body at the time of writing.
3. Decide the product rule: premium chart types allowed only on named routes, or frozen until license review completes.
4. Implement license configuration once, client-side, before render. Capture trial vs licensed screenshots for the same fixture.
5. Add `import 'apexcharts/unit'` only in the entry path that mounts unit/waffle. Add a CI grep so premium types cannot ship without that import.
6. Create one fixture with real labels from a production KPI. Pin layout, grid totals, and the free fallback type.
7. Run direct ApexCharts tests, then wrapper tests, then SSR/hydration if applicable.
8. Perform a 15-minute accessibility and density pass at the narrowest supported width.
9. Only then open the design/product review with screenshots of licensed mode and the free fallback side by side.
10. File the decision under your [developer tools](/developer-tools/) notes and link related dashboard maintenance from [start here](/start-here/) so the next upgrade does not restart from a lockfile diff.

## Further reading

- {{< source title="ApexCharts v6.6.0 release notes" url="https://github.com/apexcharts/apexcharts.js/releases/tag/v6.6.0" >}}
- {{< source title="ApexCharts waffle chart documentation" url="https://apexcharts.com/docs/chart-types/waffle-chart/" >}}
- {{< source title="apexcharts on npm (premium features and setLicense)" url="https://www.npmjs.com/package/apexcharts" >}}
- {{< source title="vue3-apexcharts on npm" url="https://www.npmjs.com/package/vue3-apexcharts" >}}

Related on this site: [ApexCharts 6.4 dashboard contract](/blog/apexcharts-6-4-dashboard-contract/), [Laravel + Vue SaaS](/laravel-vue-saas/), [developer tools](/developer-tools/), and [AI agent operations](/ai-agent-operations/) for the same change-control instinct applied to agents rather than chart types.
