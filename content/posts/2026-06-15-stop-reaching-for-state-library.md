---
title: "Stop reaching for a state library"
date: 2026-06-15
description: "Modern JavaScript runtimes have had structured state primitives for years. You probably don't need a 40KB dependency for what your app actually does."
topics: ["code"]
tags: ["javascript", "patterns", "state-management"]
draft: false
cover: "/covers/code-cover.png"
author: "Shinjae Kang"
authorRole: "Senior Software Developer"
authorLocation: "Jakarta, Indonesia"
seo:
  primaryQuery: "stop reaching for a state library"
  secondaryQueries:
    - "frontend state library overuse"
    - "Vue state management decision"
    - "when not to use state management library"
---

Every JavaScript codebase I've touched in the last two years has had a state-management library somewhere in `package.json`. Most of them didn't need one.

Here's the test: **does your state need to outlive a single function call?** If the answer is "no" for 80% of your state, you don't need a library. You need a function.

## The pattern that replaces 90% of state libraries

```javascript
// store.js — 12 lines, no dependencies
const stores = new Map();

export function createStore(name, initial) {
  if (stores.has(name)) return stores.get(name);

  let value = initial;
  const subscribers = new Set();

  const store = {
    get: () => value,
    set: (next) => {
      value = typeof next === "function" ? next(value) : next;
      subscribers.forEach((fn) => fn(value));
    },
    subscribe: (fn) => {
      subscribers.add(fn);
      return () => subscribers.delete(fn);
    },
  };

  stores.set(name, store);
  return store;
}
```

That's it. You get a shared, observable, type-safe-enough value holder. It works in any runtime. It works in tests. It works on the server.

## When you actually need a library

There are three signals:

1. **Computed state that needs caching.** A value that's expensive to derive and is read from many places.
2. **Time-travel debugging.** You need to be able to replay state changes.
3. **Cross-store transactions.** A change in store A must atomically update stores B, C, and D.

If you have one of those, look at a library. If you have two, look at a *small* library. If you have all three, look at Redux Toolkit. None of those? Don't add a dependency.

## The hidden cost

Every state library you add is a future migration. The JavaScript ecosystem's "state library of the year" has changed roughly every 18 months for the last decade. Code you write today in library X will need to be rewritten when library X loses maintenance.

The 12-line store above has no version, no maintainer, no breaking change. It'll work the same way in 2030.

---

_Try this on one screen of your app this week. You'll know within an hour whether the library was load-bearing or not._

{{< field-note title="Field note" >}}
Most frontend state problems I see are ownership problems first. Before adding a store, name who owns the data, when it expires, and which screen is allowed to mutate it. The library should come after that map, not before it.
{{< /field-note >}}

## What you should do Monday morning

1. Pick one shared state object in your app.
2. Write its owner, lifetime, and invalidation rule.
3. Remove one global state path that is only used by a single screen.

## Refresh note

This piece is now part of the site's operating archive. Read it as a decision pattern, not as a frozen news item: check whether the tool, model, or platform detail has changed, then keep the underlying verification habit if it still reduces operational risk.

## Deep refresh
## The decision tree I use now

Before adding a state library, I try to answer five questions.

1. Is the state shared across distant parts of the app?
2. Does the state outlive the current route?
3. Does more than one actor mutate it?
4. Does it need caching, invalidation, or optimistic updates?
5. Would a simpler URL, prop, form object, or server response be easier to reason about?

If the answer to most of these is no, a state library is probably not the next move.

The trap is that state libraries make early code look organized. They give names to things, centralize files, and make the architecture feel deliberate. But if the underlying ownership is unclear, the library only centralizes confusion.

## Common states that do not need a store

A lot of state can stay closer to where it is used.

| State type | Better first home |
|---|---|
| Form draft | Component or form helper. |
| Modal open state | Component local state. |
| Current tab | URL query or local component state. |
| Server list data | Server response or query cache. |
| One-page wizard state | Parent component or route-scoped object. |
| Auth user | Shared store or app-level provider, because it is truly global. |

The point is not to avoid state libraries forever. The point is to reserve them for state that has earned the right to be global.

## How this applies to Vue and Laravel

In a Laravel/Vue SaaS app, many state problems are actually boundary problems.

A controller returns data with one shape. A Vue page mutates it into another shape. A modal edits a nested part. A background job changes the underlying record. Then the UI needs to decide whether to trust local state, refetch, or show stale data.

A store does not solve that by itself. You still need a rule for freshness.

For small teams, I prefer explicit server boundaries:

1. The backend owns persisted truth.
2. The page owns temporary interaction state.
3. The URL owns navigation state.
4. A shared store owns only cross-page session state.
5. A query/cache layer owns server data freshness if the app is complex enough.

That split is boring, but boring is good. It makes code review easier because every state change has a home.

## A refactor pattern

When a store has grown too large, I do not delete it all at once. I use a three-pass cleanup:

1. Mark every state key with its actual reader count.
2. Move one-reader state back into the component or route.
3. Keep only state that has multiple readers and a clear invalidation rule.

This usually makes the remaining store smaller and more meaningful.

Related notes:

- [Code That Renders Is Not Code You Can Trust](/blog/code-that-renders-is-not-code-you-can-trust/)
- [Vue 3.6 Vapor Mode: No Virtual DOM, No Rewrite](/blog/vue-3.6-vapor-mode-no-virtual-dom-no-rewrite/)
- [Laravel and Vue SaaS Notes](/laravel-vue-saas/)

## The review smell

The smell is not "there is a store." The smell is when a reviewer cannot answer why a value is global.

When I see a store key, I want to know who writes it, who reads it, when it expires, and what happens when the server disagrees. If those answers are unclear, the state library has become a hiding place.

This is also a good AI-code review prompt. Ask the agent to list every state value it introduced and explain why each one is not local state, URL state, or server-owned state. If the explanation is weak, the code is probably too broad.

## How to verify this advice

Treat this as a small operating experiment around **frontend state ownership**.

The failure mode to watch is **global state hiding unclear responsibility**. It usually does not look dramatic at first. It looks like one convenient shortcut, one skipped check, or one tool decision that nobody writes down. A month later, the team has more output but less confidence in what actually changed.

A practical verification loop has four parts.

1. **Name the decision.** Write the decision in one sentence. If the team cannot name it, the team cannot improve it.
2. **Name the evidence.** Decide what would prove the decision helped. That might be a passing test, a smaller diff, a faster rollback, a lower bill, a clearer support path, or a page that earns impressions in Search Console.
3. **Name the counter-signal.** Decide what would prove the decision is not working. This prevents the team from defending a bad choice just because it was exciting at the start.
4. **Name the next review date.** A decision without a review date becomes architecture sediment.

For this topic, the metric I would watch is **smaller state surface and clearer invalidation**.

That metric does not need to be perfect. It only needs to be concrete enough that the next review is not based on memory. If the metric improves, keep the pattern and document it. If the metric stays flat, change the approach. If the metric gets worse, rollback or narrow the scope.

This is the operating habit I want the site to teach. A post should not end with a clever opinion. It should leave the reader with a way to test the opinion in their own repo, workflow, or team.

The same habit connects the rest of the site: [Start Here](/start-here/), [AI Agent Operations](/ai-agent-operations/), [Laravel and Vue SaaS Notes](/laravel-vue-saas/), and [Developer Tools and Model Choices](/developer-tools/). The topics are different, but the standard is the same: choose deliberately, leave proof, and keep the exit path visible.

## Final operating check

Before treating this idea as adopted, run one small review with another person. Ask them what changed, what evidence they would trust, and what would make them reverse the decision. If the answer depends on private context, improve the note. If the answer points to a file, command, metric, or dashboard, the idea is ready to become part of the operating system.

The point is not to make the process heavy. The point is to make the next decision easier than the first one. A useful technical note should reduce future debate, not create another ritual.
