---
title: "I Do Not Add a Second Chart Stack Mid-Sprint"
date: 2026-08-27T07:00:00+07:00
draft: false
slug: "second-chart-stack-mid-sprint"
description: "A green chart lockfile is not permission to add ECharts beside ApexCharts. Name a rollback owner and one failing chart fixture before anyone ships a second visualization stack."
topics: ["frontend-engineering"]
tags: ["apexcharts", "vue", "dashboard", "echarts", "change-control", "vue3-apexcharts", "laravel", "frontend-maintenance"]
cover: /covers/second-chart-stack-mid-sprint.png
seo:
  primaryQuery: "do not add a second chart library mid sprint"
  secondaryQueries:
    - "ApexCharts Vue dashboard rollback owner"
    - "vue3-apexcharts lockfile not a second stack"
    - "ECharts plus ApexCharts dual chart stack cost"
---

The chart PR is green. The screenshot on the happy path looks fine. Then someone adds a second chart library "just for one widget."

That is not a visualization improvement. That is two tooltips, two dark-mode contracts, two SSR hydrate paths, and two rollback stories living in the same admin shell. I refuse that merge until two names exist on the ticket: the person who owns revert, and the fixture that fails when the chart lies.

This week's ApexCharts default-bundle shrink is evidence that the stack you already have still moves. It is not a reason to install Apache ECharts beside it before Friday.

The question is not whether the extra widget demos well. The question is whether it survives maintenance, handoff, and the three dashboard screens your operators open every Monday.

<!--more-->

![One stack until rollback has a name](/img/second-chart-stack-mid-sprint-1.png)

## The second library is the incident

Laravel + Vue SaaS culture still treats charts as decoration. Backend migrations get owners. Chart PRs get "looks fine in Storybook." That split is false the moment two renderers share a route.

A second stack does not arrive as architecture. It arrives as a sentence:

> Apex cannot do this small-multiples panel. I will drop in ECharts for this one card.

The card ships. The next card copies the import. Six weeks later the operations dashboard has Apex for KPI sparklines and ECharts for the "special" grid, and nobody remembers which package owns tooltip delay, export PNG, or the Inertia visit that destroys the canvas.

I have watched this on admin work that looks nothing like a charting conference talk. Support opens the same sales mix screen every morning. Finance exports the same PNG into a WhatsApp thread. The "one widget" becomes the screen the business actually uses.

{{< note type="warning" title="Do not treat a dual stack as a pilot unless it is time-boxed" >}}
A pilot without a kill date is production. If the second library is a genuine evaluation, put the expire date, the owner, and the delete PR on the same ticket. Otherwise you are collecting a permanent dependency.
{{< /note >}}

This is the same change-control instinct as [a UI kit lockfile bump](/blog/ui-kit-bump-is-change-control/): generated surface area is a release, not cosmetics. Charts are worse, because users learn pixel behavior. Once a hover target moves, the product changed.

## What this week actually changed (once, as evidence)

On **25 August 2026**, ApexCharts published **7.0.0**. npm `dist-tags.latest` and `dist-tags.next` both point at **7.0.0** (`2026-08-25T08:13:16Z`). The official story is a subtraction, not a feature parade. [Source: https://github.com/apexcharts/apexcharts.js/releases/tag/v7.0.0] [Source: https://www.npmjs.com/package/apexcharts]

The v7.0.0 body and the [migration guide](https://apexcharts.com/docs/migration-v7/) agree on the headline:

| Claim from primary notes | What a Vue admin actually does |
|---|---|
| Default bundle no longer ships every feature | An `npm update` can drop optional features you never imported explicitly |
| Nine features moved behind `import 'apexcharts/features/...'` | Trellis, canvas renderer, context menu, and six more need a one-line restore |
| gzip 291,654 B (6.10.0) → 252,005 B (7.0.0), −13.6% | Smaller default is real; it is not a license to add a second vendor |
| 24% of the 6.10.0 default was licence-gated Premium code | Unlicensed apps were downloading watermarked code they did not ask to run |
| Console warning names both restore routes | Silence is not the failure mode; a single-chart fallback is |
| Wrappers including `vue3-apexcharts` already accept 7.x | Wrapper package version does not have to move for the core pin to move |
| `plotOptions.bar.borderRadiusWhenStacked` is gone | Stacked-bar corner ownership follows the outer edge; leftover option is ignored |
| `dataLabels.animate.enabled` defaults to `true` | Bar/column labels ride the update clock unless you turn animation off |

The nine opt-in features, as named by the migration table: Trellis, Storyboard, Perspectives, Ink, Canvas renderer (Strata), Linked views, Measure ruler, Rewind, Context menu. Chart types, axes, tooltips, legend, toolbar, exports, annotations, keyboard navigation, morph, drilldown, themes, plugins (Weave), custom series (Marks), and design tokens (Facet) stay in the default bundle. [Source: https://apexcharts.com/docs/migration-v7/]

{{< source href="https://apexcharts.com/docs/migration-v7/" label="ApexCharts v7 migration guide" >}}
{{< source href="https://github.com/apexcharts/apexcharts.js/releases/tag/v7.0.0" label="ApexCharts v7.0.0 GitHub release" >}}

Trellis is new **and** Premium. Canvas is now an explicit import; a chart that still asks for `renderer: 'canvas'` draws SVG and tells you in the console. That is the behavior I want in a dashboard: degrade loudly, do not invent a second library because one import line was missing.

I already wrote the sibling decisions for this stack: [ApexCharts 6.4 as a dashboard contract](/blog/apexcharts-6-4-dashboard-contract/) (heatmap geometry and the Canvas import), and [unit/waffle as a product decision](/blog/apexcharts-6-6-unit-waffle-contract/) (premium type, watermark, rollback to a free chart). Today's refusal sits on top of those posts. Do not reread them as permission to dual-run ECharts.

{{< note type="note" title="Versions appear here once" >}}
The rest of this article does not tour Apex 7 features. The lockfile moved. The wrapper did not. That pair is enough evidence. The decision is ownership, not a changelog.
{{< /note >}}

## Wrapper lag is not a second-library permit

`vue3-apexcharts` **latest** is still **1.11.1**, published **2026-03-03T19:29:31Z**. Peer range: `apexcharts >= 5.10.0`, `vue >= 3.0.0`. [Source: https://registry.npmjs.org/vue3-apexcharts] [Source: https://www.npmjs.com/package/vue3-apexcharts]

That peer range accepts 7.x. The official migration guide says the Vue 3 wrapper already accepts 7.x and does not need a new wrapper version for the core upgrade. GitHub `package.json` on `main` matches: `"apexcharts": ">=5.10.0"`. [Source: https://github.com/apexcharts/vue3-apexcharts/blob/main/package.json]

So this week's failure mode is not "the Vue package is stuck, switch vendors." The failure mode is:

1. Core moves to 7.0.0 through `npm update`.
2. CI stays green because types still parse and Vite still bundles.
3. A trellis or canvas config silently falls back (single chart / SVG).
4. Someone "fixes" the missing panel by adding ECharts.

Step 4 is the merge I reject.

If you need a second engine, you need a product reason that survives a rollback meeting: licensing, a chart type the current stack cannot express even with an explicit feature import, or a proven performance ceiling on the screens you actually ship. "The wrapper did not bump" is not that reason.

Apache ECharts **latest** is **6.1.0**. `vue-echarts` **latest** is **8.1.0** (`2026-08-07T09:38:06Z`), peer `echarts ^6.0.0`. Those numbers are inventory, not a recommendation. [Source: https://www.npmjs.com/package/echarts] [Source: https://www.npmjs.com/package/vue-echarts]

![Wrapper lag is not a vendor switch](/img/second-chart-stack-mid-sprint-2.png)

## Two names before merge

I will not argue chart aesthetics in review. I will ask for two strings.

**Rollback owner.** A person, not a team alias. They revert the lockfile and the feature import in one PR if staging lies. If they are on leave, the ticket waits.

**One failing fixture.** A test that is red when the chart is wrong. Green unit tests on option JSON are not a fixture. The fixture has to see pixels or a documented fallback.

That pair is enough. Without it, the PR is a demo.

{{< field-note title="Field note" >}}
On Laravel + Vue SaaS admin work (the same class of surfaces I keep under [Laravel + Vue SaaS](/laravel-vue-saas/) and [developer tools](/developer-tools/)), chart incidents do not show up as 500s. They show up as a support lead saying the export looks different from yesterday, or a finance user asking why the small-multiples grid collapsed into one line. I keep the chart allow-list next to the same change-control notes used for UI-kit bumps and agent-edited frontends. The rule is boring on purpose: one visualization stack per product surface until revert has a name and a failing screenshot. Modoo-style Laravel admin dashboards do not get a second engine because a coding agent found an ECharts snippet.
{{< /field-note >}}

Here is the merge desk I actually paste into a PR template.

```markdown
## Chart change
- [ ] Stack stays ApexCharts + vue3-apexcharts (no new chart package)
- [ ] Rollback owner: @username
- [ ] Fixture path: tests/e2e/dashboard-revenue-chart.spec.ts
- [ ] Explicit feature imports listed (or "none — default bundle only")
- [ ] Screenshot of the failing state attached (fallback / missing series / wrong renderer)
- [ ] Kill date if this is a time-boxed evaluation: YYYY-MM-DD
```

If the author cannot fill the owner and the fixture path, the chart does not ship. I do not negotiate that on Friday afternoon.

## Prove the pin, then prove the lie

Do not trust `package.json` ranges in a Vite app. Prove what the lockfile resolved, and prove the chart still tells the truth after that resolve.

```javascript {linenos=inline,hl_lines=[12,"18-24"]}
import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import assert from 'node:assert/strict'

const require = createRequire(import.meta.url)
const lock = JSON.parse(readFileSync('package-lock.json', 'utf8'))

function resolved(name) {
  const key = `node_modules/${name}`
  const pkg = lock.packages?.[key]
  assert.ok(pkg, `${name} missing from lockfile`)
  return pkg.version
}

const apex = resolved('apexcharts')
const vueApex = resolved('vue3-apexcharts')

assert.match(apex, /^7\./, `apexcharts pin drifted: ${apex}`)
assert.equal(vueApex, '1.11.1', `vue3-apexcharts unexpected: ${vueApex}`)

const vueMeta = require('vue3-apexcharts/package.json')
assert.match(
  vueMeta.peerDependencies.apexcharts,
  />=5\.10\.0/,
  'peer range no longer accepts the core pin you think you shipped',
)

console.log(`ok apexcharts@${apex} vue3-apexcharts@${vueApex}`)
```

Run that in CI before Vite. It does not prove pixels. It proves you are not arguing about two different trees.

Then restore optional features in the **same module that mounts the chart**, not in a random `main.ts` someone will delete during an Inertia cleanup.

```vue
<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'
import ApexCharts from 'apexcharts'
import 'apexcharts/features/trellis'
import 'apexcharts/features/renderer-canvas'

const el = ref<HTMLDivElement | null>(null)
let chart: ApexCharts | undefined

onMounted(() => {
  if (!el.value) {
    throw new Error('chart mount node missing')
  }
  chart = new ApexCharts(el.value, {
    chart: { type: 'line', renderer: 'canvas', height: 320 },
    series: [
      { name: 'Revenue', region: 'North', data: [12, 18, 15, 22] },
      { name: 'Revenue', region: 'South', data: [9, 11, 14, 13] },
    ],
    xaxis: { categories: ['W1', 'W2', 'W3', 'W4'] },
    trellis: { by: 'region', minPanelWidth: 260 },
  })
  chart.render()
})

onBeforeUnmount(() => {
  chart?.destroy()
  chart = undefined
})
</script>

<template>
  <div ref="el" data-testid="revenue-trellis" />
</template>
```

If Trellis is Premium in your environment, this module is already a license decision. Do not hide that inside a "UI tweak" PR. The [unit/waffle contract](/blog/apexcharts-6-6-unit-waffle-contract/) already covers watermarked types. Same rule: commercial path first, aesthetics second.

The fixture that earns the merge is the one that fails when the feature import is missing.

```typescript {linenos=inline,hl_lines=[14,"18-24"]}
import { test, expect } from '@playwright/test'

test('revenue trellis refuses a silent single-chart fallback', async ({ page }) => {
  const warnings: string[] = []
  page.on('console', (msg) => {
    if (msg.type() === 'warning' || msg.type() === 'error') {
      warnings.push(msg.text())
    }
  })

  await page.goto('/admin/revenue')
  const root = page.getByTestId('revenue-trellis')
  await expect(root).toBeVisible()
  await expect(root).not.toBeEmpty()

  const fallback = warnings.find((w) =>
    w.includes('requires the trellis feature') && w.includes('Rendering as a single chart'),
  )
  expect(
    fallback,
    'official fallback warning means the feature import never loaded',
  ).toBeUndefined()
})
```

That test is supposed to go red if someone removes the feature import or if a lockfile bump drops Trellis from the default bundle and nobody restored it. A red test is cheaper than a second vendor.

{{< details summary="If you do not use Trellis or Canvas, the fixture is still required" >}}
Pick the chart that finance actually screenshots. Assert series count, category labels, and that a known gap (null point, empty stack) does not invent a neighbor bar. The 7.0.0 notes fixed stacked baselines resolving by array position instead of x — a 92px displace on ragged data. Your fixture should include a missing point on purpose. [Source: https://github.com/apexcharts/apexcharts.js/releases/tag/v7.0.0]
{{< /details >}}

![Two strings on the ticket](/img/second-chart-stack-mid-sprint-3.png)

## The tax of "just add ECharts"

A second stack is not `npm install echarts vue-echarts`. It is a permanent fork of every dashboard rule you already paid for.

| Surface | One stack (Apex + vue3-apexcharts) | Two stacks (plus ECharts) |
|---|---|---|
| Tooltip delay / overflow | One CSS + one z-index story | Two portals fighting Inertia overlays |
| Dark mode tokens | One theme object | Two palettes, two "almost navy" greys |
| SSR / first paint | One hydrate path | `vue-echarts` + Apex each want a client-only fence |
| PNG export | One toolbar contract | Two export buttons, two DPI lies |
| Coding-agent PRs | One allow-list | Agents paste the other library because the README ranked higher |
| Rollback | Revert one lockfile subtree | Half the route still imports the abandoned engine |

Coding agents make this worse. They do not share your allow-list. They share GitHub snippets. If both libraries exist in `package.json`, the next agent-authored widget will pick whichever sample ranked. That is how a "pilot card" becomes the default.

I treat visualization the same way I treat [agent operations](/ai-agent-operations/): the process is not the product. The product is a named side effect plus a proof artifact. A new chart package without a fixture is an unowned side effect.

If ECharts is the right long-term engine, schedule a migration. Freeze new Apex charts. Name the cut date. Do not run both as a lifestyle.

## A dashboard allow-list you can enforce in CI

Keep the allow-list in repo, not in Slack.

```json
{
  "chartStack": {
    "engine": "apexcharts",
    "wrapper": "vue3-apexcharts",
    "forbidden": ["echarts", "vue-echarts", "chart.js", "highcharts"]
  }
}
```

```javascript
import { readFileSync } from 'node:fs'
import assert from 'node:assert/strict'

const pkg = JSON.parse(readFileSync('package.json', 'utf8'))
const policy = JSON.parse(readFileSync('policy/chart-stack.json', 'utf8'))
const deps = { ...pkg.dependencies, ...pkg.devDependencies }

for (const name of policy.chartStack.forbidden) {
  assert.equal(
    deps[name],
    undefined,
    `${name} is a second chart stack; remove it or open a migration ticket with a kill date`,
  )
}

assert.ok(deps[policy.chartStack.engine], 'engine missing')
assert.ok(deps[policy.chartStack.wrapper], 'wrapper missing')
```

This is dumb on purpose. Dumb gates survive handoff. Clever exceptions die when the original author changes jobs.

Put the same forbidden list in your coding-agent instructions. A local CI check that agents cannot see is a lecture, not a control.

## What a mid-sprint chart change is allowed to be

Allowed, with owner + fixture:

- Restore a v7 feature import that a lockfile bump dropped.
- Pin `dataLabels.animate.enabled` when bar labels now ride the update clock and your screenshot diff is noise.
- Remove `borderRadiusWhenStacked` from leftover config.
- Fix a ragged stacked series after the x-alignment repair.
- Swap `type: 'pie'` to `type: 'donut'` on an existing Apex instance.

Not allowed mid-sprint:

- Add `echarts` because Trellis looked empty (import the feature, or drop the panel).
- Add a premium type to a customer-facing screen without license review.
- Let a coding agent introduce `vue-echarts` in a "quick dashboard polish" PR.
- Keep both engines "until we decide." Decision is the ticket. Dual running is the absence of one.

The [start here](/start-here/) hub on this site is the same idea at a higher level: pick the boring path you can maintain. Chart libraries are not where you collect souvenirs.

![Mid-sprint allow versus refuse](/img/second-chart-stack-mid-sprint-4.png)

## What you should do Monday morning

1. **Inventory one product surface.** List every chart on the admin home and the finance export screen. One engine or you already have an incident.
2. **Read the lockfile, not Twitter.** Confirm `apexcharts` and `vue3-apexcharts` resolved versions. If core is on 7.x, grep for the nine feature names and for `borderRadiusWhenStacked`.
3. **Name the rollback owner** in the next chart PR template before anyone types `npm install`.
4. **Add one failing fixture** for the chart finance actually screenshots. Include a missing data point.
5. **Commit a forbidden-package assert** for `echarts` / `vue-echarts` unless a dated migration ticket exists.
6. **Tell coding agents the allow-list.** If the agent cannot see the policy, it will paste the other library.
7. **If you truly need ECharts**, open a migration with a freeze on new Apex charts and a kill date. Do not "just add it for one widget."

## Further reading

{{< source href="https://apexcharts.com/docs/migration-v7/" label="Migrating to ApexCharts v7" >}}
{{< source href="https://github.com/apexcharts/apexcharts.js/releases/tag/v7.0.0" label="ApexCharts 7.0.0 release notes" >}}
{{< source href="https://www.npmjs.com/package/vue3-apexcharts" label="vue3-apexcharts on npm" >}}

Related on this site: [ApexCharts 6.6 unit/waffle contract](/blog/apexcharts-6-6-unit-waffle-contract/), [UI kit bump as change control](/blog/ui-kit-bump-is-change-control/), and the [Laravel + Vue SaaS](/laravel-vue-saas/) hub.
