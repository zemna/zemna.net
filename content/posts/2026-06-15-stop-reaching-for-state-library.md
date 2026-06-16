---
title: "Stop reaching for a state library"
date: 2026-06-15
description: "Modern JavaScript runtimes have had structured state primitives for years. You probably don't need a 40KB dependency for what your app actually does."
categories: ["Code"]
tags: ["javascript", "patterns", "state-management"]
draft: false
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
