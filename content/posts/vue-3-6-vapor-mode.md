---
title: "Vue 3.6 Vapor Mode — No Virtual DOM, No Rewrite"
date: 2026-06-21T10:00:00+07:00
draft: false
topics: ["frontend", "vue", "performance"]
cover: /covers/vue-3-6-vapor-mode.png
summary: "Vue 3.6 Vapor Mode compiles SFC templates directly to DOM operations, hitting Solid.js-speed renders without rewriting your codebase. Here's how it works, what it can't do yet, and why teams should start piloting it now."
---

100,000 components mounted in roughly 100 milliseconds. Render times slashed by up to 97% in extreme cases. A baseline bundle under 10KB. These aren't aspirational roadmap slides — they're the numbers Evan You's team delivered at Vue.js Nation 2025, and they're now running in production-adjacent code with v3.6.0-beta.16, released June 17, 2026.

The virtual DOM era is closing. Not gradually. Not hypothetically. Right now, every major JavaScript framework — React, Vue, Svelte — has either abandoned the VDOM or is actively building the off-ramp. Vue 3.6 Vapor Mode is the latest and most significant domino to fall: the largest framework by combined adoption to offer a non-breaking path away from virtual DOM rendering.

If you've spent years optimizing `shouldComponentUpdate`, fighting `key` props, or profiling VNode allocation in Chrome DevTools, Vapor Mode is the end of that particular brand of suffering.

## What Vapor Mode Actually Is

Vapor Mode is a new compilation target for Vue Single-File Components. Instead of building a JavaScript tree of VNodes, diffing it against the previous tree, and issuing patch operations to the real DOM — the three-step dance every Vue and React developer has internalized since 2014 — the compiler now emits imperative DOM operations at build time.

Think of it this way: classic Vue 3 takes your `<template>` and produces code that says "here's a tree of objects representing the UI, now let Vue's runtime reconcile it." Vapor Mode takes the same `<template>` and produces code that says "bind this `<span>` to `count.value`, update its `textContent` when `count` changes, and don't allocate anything else."

You opt in at the file level. One attribute:

```vue
<script setup vapor>
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

That's it. `ref()`, `reactive()`, `computed()`, `watch()` — the Composition API surface is unchanged. The rendering layer underneath is what transforms, and it transforms radically.

The reactivity engine driving Vapor has been rebuilt on top of [alien-signals](https://github.com/stackblitz/alien-signals), a standalone signals library engineered for minimal overhead in dependency tracking and subscriber notification. Even non-Vapor Vue 3.6 components benefit from this rewrite — Vapor components simply have more headroom to exploit it, because there's no VDOM machinery in the way.

As of April 2026, Vapor Mode hit feature-complete status: every stable VDOM feature works inside Vapor components except Suspense. That includes SSR hydration, async components, transitions, KeepAlive, Teleport — the load-bearing pieces any non-trivial application depends on. The alpha series (v3.6.0-alpha.1 onward) deliberately excluded most of these. The beta releases closed the gaps one by one. Only Suspense remains outside scope, and that's an architectural decision, not a temporary omission.

![Vapor Mode architecture — Virtual DOM eliminated, direct DOM operations via alien-signals](/images/posts/vue-3-6-vapor-mode/vapor-architecture.png)

## How It Achieves ~97% Faster Renders

The performance story has three layers. Understanding all three explains why "97% faster" isn't marketing — it's the natural outcome of eliminating waste the VDOM introduced.

### Layer One: Zero VNode Allocation

Every re-render in classic Vue 3 allocates a fresh tree of VNode objects. Render a list of 10,000 rows? That's 10,000 object allocations per pass, plus the diffing algorithm walking both old and new trees, plus garbage collection pressure from the discarded old tree. On a mid-tier Android device, this adds up to real main-thread jank.

Vapor skips all of it. The compiler knows — at build time — exactly which DOM nodes correspond to which reactive values. When `items[42].price` changes, the compiler-emitted code updates the text content of one `<td>` and stops. No tree walk. No allocation. No diff.

This is the same architectural insight that made Svelte fast and Solid.js competitive with hand-written vanilla JavaScript: treat the DOM as the source of truth, not a JavaScript object graph you have to reconcile against it.

### Layer Two: alien-signals Reactivity

Vue's original reactivity system was already fast — Proxy-based, lazy by default, with smart dependency tracking. The alien-signals rewrite takes it further by reducing subscriber notification latency and cleaning up stale dependencies with fewer allocations per update cycle.

The practical impact: in a component tree where 500 reactive values are changing but only 50 affect visible DOM, alien-signals ensures those 450 irrelevant changes never trigger DOM work. The old system was good at this. The new system is surgical.

### Layer Three: Bundle Size Reduction

The Vapor runtime discards the diff/patch machinery entirely. Early-adopter reports converge on 20-50% smaller shipped JavaScript for Vapor-only components compared to equivalent VDOM components. The baseline bundle drops under 10KB.

This isn't just a download-speed optimization. On mobile devices, every kilobyte of JavaScript costs parse and compile time on the main thread. A 50% reduction in framework code shipped per component compounds into measurable Time To Interactive improvements — particularly on the mid-tier Android phones your users outside North America and Western Europe are actually holding.

## The Numbers: Vue 3.6 Vapor vs. The Field

The byteiota framework comparison, published alongside the 2026 convergence analysis, provides the most current cross-framework data:

![Framework benchmark comparison — Vue Vapor, React 19, Svelte 5, Solid.js performance](/images/posts/vue-3-6-vapor-mode/benchmark-comparison.png)

| Metric | Vue 3.6 (Standard) | Vue 3.6 (Vapor) | React 19 | Svelte 5 | Solid.js |
|---|---|---|---|---|---|
| **Render speed** (ops/sec) | 31.2 | ~39 (estimated parity with Svelte) | 28.4 | 39.5 | ~40 (estimated) |
| **Baseline bundle** | ~58KB | <10KB | 72KB | 28KB | ~7KB |
| **Market share** | 17.6% | — | 44.7% | 7.2% | <2% |
| **Learning curve** | Easiest | Identical to Vue 3 | Moderate | Easy | Steep |
| **VDOM-free** | No (opt-in) | Yes | No | Yes | Yes |
| **Migration cost** | Baseline | Per-file opt-in | Compiler adoption | Runes rewrite | Full rewrite |

A few notes on this table. Render speed numbers for React 19, Vue 3.6 Standard, and Svelte 5 are from the js-framework-benchmark as cited by byteiota. Vapor and Solid.js figures are estimated based on documented performance parity claims — independent benchmarks will firm these up once Vapor exits beta. The Migration Cost row reflects the community consensus on upgrade paths and is editorial characterization, not sourced data.

The render speed numbers come from the js-framework-benchmark. Svelte 5 leads at 39.5 ops/sec, React 19 trails at 28.4 — a 39% gap. Vue 3.6 Vapor closes that gap entirely, landing in the same performance tier as Svelte and Solid. As Evan You demonstrated at Vue.js Nation 2025, Vapor mounts 100,000 components in approximately 100ms. That's the kind of throughput that makes virtual scrolling libraries optional for all but the most extreme datasets.

The bundle size story is even sharper. Vapor's <10KB baseline is smaller than Svelte's 28KB — though Svelte's compiler eliminates unused framework code at the component level, so real-world comparisons depend on component composition. React's 72KB baseline, meanwhile, is the price of backward compatibility with a decade of ecosystem assumptions.

Market share data reflects the ecosystem reality: React dominates hiring pools, Vue holds strong in Asian markets and among solo-to-small teams, Svelte and Solid punch above their weight on technical merit but can't match the library ecosystem or talent availability.

## The Framework Convergence Nobody's Talking About

Vue's Vapor Mode didn't happen in a vacuum. It's part of a larger, unmistakable pattern:

- **Solid.js** shipped without a VDOM from day one, proving fine-grained signals-driven rendering works at scale.
- **Svelte 5** rewrote its reactivity model around Runes (`$state`, `$derived`, `$effect`), also VDOM-free and compile-time-resolved.
- **React 19** didn't kill the VDOM, but introduced an automated Compiler that memoizes components and cuts unnecessary re-renders by 25-40%. It's a mitigation, not a removal — but the direction is the same.
- **Vue 3.6 Vapor** now joins the post-VDOM camp with the largest install base of any framework making the leap.

All four arrived at the same conclusion independently: fine-grained reactivity plus compile-time optimization eliminates the need for a virtual DOM. The VDOM solved a real problem in 2014 — declarative UIs over imperative DOM APIs — but at a runtime cost signals-based architectures can now erase.

What makes Vue's entry significant isn't technical novelty. Solid did it first. Svelte popularized it. Vue's contribution is **backward compatibility at scale**. Existing Vue 3 codebases don't need a rewrite. Components mix freely across VDOM and Vapor boundaries (with documented interop limits). The Composition API is the same. The toolchain is the same. The migration is per-file, one attribute, no flag day.

If you've been through the React class-to-hooks transition or the AngularJS-to-Angular rewrite, you understand how rare this is.

## Code: Before and After (It's the Same Code)

Here's a real example. This is a product list component that renders a filtered, sorted table — exactly the kind of hot-path view where Vapor earns its keep.

**Before (standard Vue 3 — VDOM path):**

```vue
<script setup>
import { ref, computed } from 'vue'

const products = ref([])
const sortKey = ref('price')
const filterText = ref('')

const filtered = computed(() => {
  return products.value
    .filter(p => p.name.includes(filterText.value))
    .sort((a, b) => a[sortKey.value] - b[sortKey.value])
})
</script>

<template>
  <input v-model="filterText" placeholder="Filter..." />
  <table>
    <tr v-for="p in filtered" :key="p.id">
      <td>{{ p.name }}</td>
      <td>{{ p.price }}</td>
      <td>{{ p.stock }}</td>
    </tr>
  </table>
</template>
```

Every keystroke in the filter input triggers a full VNode re-render of the table. For 500 products, that's 500 VNode allocations and a 500-node diff per character typed.

**After (Vapor Mode — same code, one attribute):**

```vue
<script setup vapor>
import { ref, computed } from 'vue'

const products = ref([])
const sortKey = ref('price')
const filterText = ref('')

const filtered = computed(() => {
  return products.value
    .filter(p => p.name.includes(filterText.value))
    .sort((a, b) => a[sortKey.value] - b[sortKey.value])
})
</script>

<template>
  <input v-model="filterText" placeholder="Filter..." />
  <table>
    <tr v-for="p in filtered" :key="p.id">
      <td>{{ p.name }}</td>
      <td>{{ p.price }}</td>
      <td>{{ p.stock }}</td>
    </tr>
  </table>
</template>
```

The only difference is `vapor` on line one. The compiler now emits code that binds each `<td>` directly to the corresponding reactive value. When `filterText` changes and `filtered` recomputes, only the DOM nodes whose content actually changed get updated — no tree diff, no allocation storm.

This isn't hypothetical. This is how the v3.6.0-beta.16 compiler works today.

<!-- IMAGE: code-example -->

## Gradual Migration: Start Surgical, Not Sweeping

The pragmatic pattern emerging from early adopters is clear: don't migrate your entire app. Pick the views where rendering throughput is the user-visible bottleneck and Vaporize those first.

**Start here:**
- List views with large datasets (tables, data grids, infinite scroll feeds)
- Real-time dashboards where multiple reactive streams converge
- Search-as-you-type interfaces where every keystroke triggers re-renders
- Any view where you've already written `v-memo` or `shallowRef` workarounds

**Leave on VDOM for now:**
- Auth flows, settings pages, static landing content — places where render performance isn't the constraint
- Any component tree wrapped in `<Suspense>` (Vapor excludes it)
- Components relying on custom directives or third-party libraries that haven't confirmed Vapor compatibility

**The interop model works both ways:**
- A Vapor component can render a VDOM child
- A VDOM component can render a Vapor child
- Props, slots, and events cross the boundary — with some edge cases around reactive prop patterns that the team is still hardening

The operational playbook: ship Vapor components behind a feature flag, instrument them against production traffic, and roll back if the beta label bites. Let the VDOM handle everything else. This isn't an all-or-nothing decision — it's a dial you turn per component, guided by real metrics.

## The Catch: What Vapor Cannot Do (June 2026)

Vapor Mode is beta-quality feature-complete. That's a real milestone, but it's not the same as "shipping to production tomorrow." The honest constraints:

**Suspense is excluded.** If your application relies on `<Suspense>` for async data orchestration, those component trees stay on the VDOM path. This is a deliberate architectural limitation — Suspense coordinates with the virtual DOM's ability to pause and resume rendering subtrees, and Vapor's direct-DOM model doesn't expose the same hooks. The Vue team has not committed to a timeline for Suspense support.

**Ecosystem catch-up is incomplete.** Nuxt, Pinia, and VueUse work with Vapor components. But library authors across the broader ecosystem are still validating their code against the new compilation target. Some custom directives assume VDOM internals. Some third-party component libraries ship code that only works correctly under the VDOM reconciliation model. Laravel + Inertia.js users flagged specific compatibility friction with Vapor page components in community deep-dives as recently as April 2026.

**Interop edge cases exist.** A Vapor parent rendering a VDOM child (or vice versa) works for the common patterns. But reactive prop propagation across the boundary behaves differently in certain scenarios, and slot edge cases are still being documented. The Vue team's own messaging is that the interop story is functional but not seamless — expect to test boundary components thoroughly.

**The label says beta.** Vue's official stance is that beta means production-evaluation ready, not production-default. Estimates for a stable release range from mid-2026 to Q4 2026 — the Vue team hasn't committed to a specific date, and the timeline depends on how the beta feedback cycle plays out.

**Vue 2 codebases face a double-hop.** If you're still on Vue 2 (EOL since late 2023), your path is Vue 2 → Vue 3 Composition API → Vue 3 Vapor. The good news: time spent migrating to the Composition API today is not wasted — that code runs unchanged in Vapor when you're ready to flip the attribute. But there's no shortcut. You can't jump from Vue 2 Options API directly to Vapor Mode.

## What Teams Should Do in Q2/Q3 2026

Vue 3.6 Vapor Mode is a strategic signal, not just a release note. Three practical implications for engineering teams evaluating their stack:

**First, the architectural debate is over.** When Vue, Solid, and Svelte all converge on signals-driven, compile-time-resolved rendering — and when even React ships a compiler to mitigate VDOM cost — the direction is settled. Teams making framework choices in 2026 should weigh signals-native designs as the default, not the experimental fringe. If you're evaluating a new project right now, pick a framework where VDOM-free rendering is either the default or a first-class opt-in. That's Solid, Svelte 5, or Vue 3.6 with Vapor.

**Second, performance budgets are achievable without rewrites.** The 97% headline is the extreme case. But 30-50% improvements in render time and bundle size are realistic for component-heavy applications that Vaporize their hot paths. That's the difference between a dashboard that stutters on a mid-tier Android device and one that feels native — achieved by adding one attribute to a handful of files.

**Third, the migration cost is the lowest in framework history for a transition of this magnitude.** Composition API code is portable. The opt-in is per-file. The interop story, while imperfect, is real. You don't need a rewrite — you need a pilot on two or three high-traffic routes, a feature flag, and instrumentation.

The concrete next step: identify one rendering-bound view in your production application. Add `vapor` to its `<script setup>`. Test it. Deploy it behind a flag. Instrument it. Real benchmarks on real hardware with real users will tell you more than any synthetic 100K-component demo ever could. By the time Vue 3.6 exits beta, you'll already know whether Vapor delivers in your specific context — and which three files to flip next.