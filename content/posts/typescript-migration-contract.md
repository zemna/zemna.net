---
title: "Strict TypeScript Is a Migration Contract, Not a Compiler Nuisance"
slug: "typescript-migration-contract"
date: 2026-07-13T07:00:00+07:00
draft: false
description: "An exactOptionalPropertyTypes error is often an ownership decision left undocumented. Use a narrow boundary, type tests, runtime tests, an exact lockfile, and a rollback path to turn strict TypeScript into a maintainable migration."
topics: ["tutorial"]
tags: ["typescript", "exact-optional-property-types", "vue", "migration-testing", "dependency-management"]
cover: /covers/typescript-migration-contract.png
seo:
  primaryQuery: "TypeScript exactOptionalPropertyTypes migration"
  secondaryQueries:
    - "exactOptionalPropertyTypes undefined optional property"
    - "Vue TypeScript boundary testing"
    - "TypeScript dependency upgrade rollback checklist"
---

A UI utility upgrade rejects `undefined`. The pull request looks harmless: replace a few object literals, widen a type, move on. Then the same error appears in a prop adapter, an API mapper, a saved-filter serializer, and a test fixture. The compiler is not being difficult. It found an ownership decision that the codebase never wrote down.

That is why strict TypeScript work deserves a migration plan. `exactOptionalPropertyTypes` draws a real line between a property that is absent and a property that is present with `undefined`. The question is not whether an editor can silence the error. The question is which layer owns the meaning of absence, default, and invalid input. The question is not whether this demos well; it is whether it survives maintenance, handoff, and local constraints.

<!--more-->

This is a practical playbook for a Laravel and Vue application, but the boundary pattern applies to any TypeScript service or UI. It makes no package-performance promise and does not prescribe a framework upgrade. It gives a team a small, reversible way to turn a strictness failure into an explicit contract.

![Optional property states: absent, valid value, or invalid explicit undefined](/img/typescript-migration-contract-1.png)

## The error is describing a semantic difference

TypeScript documents `exactOptionalPropertyTypes` as stricter handling for properties declared with `?`. With the option enabled, an optional property means it is absent or has a value in its declared union. Assigning `undefined` is rejected unless `undefined` is explicitly part of that union. The distinction matters because checking whether a key exists and checking whether its value is truthy are different JavaScript operations. [Source: https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html]

Consider an account preference. A missing `colorThemeOverride` can mean “use the system setting.” A key explicitly present with `undefined` says something else: a caller wrote a value but failed to provide one. If the application serializes the object, sends it through an API, or merges it with defaults, that difference becomes observable.

```ts
// preferences.ts
type Preferences = {
  colorThemeOverride?: "dark" | "light"
}

const systemDefault: Preferences = {}
const explicitTheme: Preferences = { colorThemeOverride: "dark" }

// With exactOptionalPropertyTypes: true this is rejected.
const ambiguous: Preferences = { colorThemeOverride: undefined }

function hasOverride(value: Preferences) {
  return "colorThemeOverride" in value
}

console.log(hasOverride(systemDefault)) // false
console.log(hasOverride(explicitTheme)) // true
```

The correct response is not automatically “add `| undefined` everywhere.” Add it only when the domain genuinely has three states: absent, a valid value, and explicitly undefined. Most migration noise comes from treating those meanings as interchangeable for years, then discovering that a stricter library boundary refuses to continue the ambiguity.

| Situation | Contract to model | Owner |
|---|---|---|
| Caller has no preference | Omit the property | caller |
| UI applies a known default | Normalize to a valid value | boundary adapter |
| API accepts an empty/reset instruction | Model it as a named value such as `null` or `"system"` | API contract |
| Input is malformed | Reject it with a validation error | boundary validator |

The table matters because it prevents a common bad fix: scattering non-null assertions or type casts through every caller. A cast silences the compiler at one location. It does not tell the next maintainer whether the key must be omitted, defaulted, or rejected.

{{< note type="warning" title="Do not make undefined a migration solvent" >}}
If a property is optional because absence carries meaning, widening it to `T | undefined` changes the contract. Make that change only when an explicitly present `undefined` is a supported state across the sender, serializer, API, and consumer.
{{< /note >}}

## Pick one normalization boundary

A boundary is the one place where external or loose data becomes application data. In a Vue screen it is often the function that maps Laravel JSON into view props, parses route query parameters, or converts a UI utility’s options into local state. The rule is simple: callers pass their real intent; the boundary converts that intent into the smallest stable shape the component needs.

Do not normalize in every component. Do not make the backend guess what a local popover option meant. Put the policy in one named adapter, then test it independently. The adapter below treats an absent placement as the application default and rejects a present but invalid value before it reaches the component.

```ts
// ui/normalize-floating-options.ts
export type Placement = "top" | "right" | "bottom" | "left"

type IncomingOptions = {
  placement?: Placement
  offset?: number
}

export type FloatingOptions = {
  placement: Placement
  offset: number
}

export function normalizeFloatingOptions(
  incoming: IncomingOptions,
): FloatingOptions {
  return {
    placement: incoming.placement ?? "bottom",
    offset: incoming.offset ?? 8,
  }
}
```

This code does not claim every product should default to `bottom` and `8`. Those values belong to the local contract. The useful part is that the component receives `FloatingOptions`, not a bag of optional values whose missing-state semantics change from caller to caller.

For Laravel and Vue maintenance, this keeps responsibilities visible. Laravel still validates request input and authorizes data access. Vue still owns presentation defaults. A mapping function at the request, query, or component boundary says how those two worlds meet. It becomes the review surface when a library tightens its types.

![One boundary normalizes loose input into stable component options](/img/typescript-migration-contract-2.png)

{{< field-note title="Field note" >}}
In a Laravel/Vue SaaS, a front-end dependency update rarely stays inside one component. Saved filters become query strings, query strings hit controllers, controllers return JSON, and an admin screen turns that JSON into props. I keep the normalizer beside the feature instead of hiding it inside a vendor wrapper. It gives the next person a place to change the contract, a unit test to read, and a rollback that does not require hunting through every caller.
{{< /field-note >}}

## Type tests prove the boundary; runtime tests prove behavior

A type check and a runtime test answer different questions. TypeScript verifies that source code respects the declared contract. It does not prove that a route query arrived as expected, that a Laravel response contains the expected field, or that a click shows the correct menu. A browser-oriented test can exercise behavior, but it cannot prove an unwanted widening of a public type will fail compilation.

Vitest documents type testing through `expectTypeOf` or `assertType`, and its type-checking mode invokes `tsc` or `vue-tsc` according to configuration. Vue Test Utils is the official utility library for Vue component tests. Use both layers where the boundary is important. [Source: https://vitest.dev/guide/testing-types] [Source: https://test-utils.vuejs.org/guide/]

```ts
// ui/normalize-floating-options.test-d.ts
import { expectTypeOf } from "vitest"
import { normalizeFloatingOptions } from "./normalize-floating-options"

const result = normalizeFloatingOptions({ placement: "top" })

expectTypeOf(result.placement).toEqualTypeOf<"top" | "right" | "bottom" | "left">()
expectTypeOf(result.offset).toEqualTypeOf<number>()

// This belongs in a compile-failing fixture in a real repository:
// normalizeFloatingOptions({ placement: undefined })
```

Then test the behavior with ordinary test inputs. The important assertion is not that a utility library renders a pixel in a particular location. It is that your adapter returns the defined, application-owned value for absence and preserves an explicit valid value.

```ts
// ui/normalize-floating-options.spec.ts
import { describe, expect, it } from "vitest"
import { normalizeFloatingOptions } from "./normalize-floating-options"

describe("normalizeFloatingOptions", () => {
  it("uses local defaults when options are absent", () => {
    expect(normalizeFloatingOptions({})).toEqual({
      placement: "bottom",
      offset: 8,
    })
  })

  it("preserves supported explicit values", () => {
    expect(normalizeFloatingOptions({ placement: "left", offset: 12 })).toEqual({
      placement: "left",
      offset: 12,
    })
  })
})
```

A third check belongs in the integration layer: mount the component or exercise the endpoint that supplies the options. That test should use the real boundary—route parsing, a Laravel resource, or a component prop adapter—not a duplicate object literal. If the integration test needs a giant setup, that is evidence the boundary is in the wrong place.

| Check | Failure it should catch | Keep it small by |
|---|---|---|
| Type test | accidental widening or invalid option shape | testing exported adapter types |
| Unit test | defaulting and explicit-value behavior | using plain objects |
| Component/integration test | wrong route/API/prop wiring | exercising one real entry point |
| Manual smoke test | focus, overlay, browser-specific interaction | defining one repeatable scenario |

## Make the dependency change reversible

A migration contract needs an artifact trail. Pin the exact package version under review, commit the lockfile, keep the test command in CI, and name the rollback. `npm ci` installs from the lockfile and errors when `package.json` and the lockfile are out of sync, which makes it useful for repeatable CI installs. [Source: https://docs.npmjs.com/cli/v11/commands/npm-ci]

```json
{
  "scripts": {
    "check:types": "vue-tsc --noEmit",
    "test:unit": "vitest run",
    "test:types": "vitest --typecheck",
    "check:migration": "npm run check:types && npm run test:types && npm run test:unit"
  }
}
```

```sh
# Record the exact dependency change and validate the same install in CI.
npm install --save-exact @floating-ui/vue@2.0.1
npm ci
npm run check:migration
npm run build

git diff -- package.json package-lock.json
```

The version in that example is only a command shape; use the version your repository has actually approved. Never turn a blog snippet into a production install instruction. What belongs in the pull request is the exact diff, the command output, the component boundary changed, and the rollback commit or previous lockfile revision.

![Migration evidence trail: lockfile, type test, runtime test, and rollback](/img/typescript-migration-contract-3.png)

A rollback should be boring. If the normalizer caused the issue, revert the adapter and lockfile in one change. If a feature flag guarded the new utility path, disable it first, then investigate. Do not make a component-by-component cleanup the emergency path. The shortest rollback is usually the best evidence that the migration slice was small enough.

{{< details summary="A useful pull-request checklist" >}}
- State whether absence means default, inherit, reset, or invalid input.
- Name the one adapter that normalizes the value.
- Include a type test and a runtime test for that adapter.
- Commit the exact dependency and lockfile diff.
- Write the rollback command or revert target before review.
- Add a follow-up date for removing a temporary compatibility branch.
{{< /details >}}

## Review the options before fixing the error

When strictness reports a failure, there are three honest choices. The right choice depends on the domain, not on which one produces the shortest diff.

1. **Fix the caller.** Choose this when the caller has enough information to omit a key rather than write `undefined`. This is often right for props assembled by one component.
2. **Normalize at a boundary.** Choose this when several inputs meet at a mapper, serializer, route parser, or component adapter. It centralizes policy and limits the migration surface.
3. **Widen the type deliberately.** Choose this when explicit `undefined` is a supported, documented state. Update producers, consumers, serialization, and tests together.

The risky fourth choice is a broad cast. It makes the compiler quiet while leaving the ownership question open. The next library upgrade will find the same ambiguity again, usually in a less convenient place.

A practical review asks for artifacts rather than opinions: a before-and-after input example, the normalizer, one type-test fixture, one runtime test, the lockfile diff, and a rollback note. That is enough for a reviewer to challenge the semantics without needing to reconstruct the entire UI state in their head.

### Keep transport shapes and view shapes separate

The cleanest boundary work starts by refusing to reuse one type for every layer. A Laravel JSON resource is a transport shape. A route query is an input shape. A Vue component prop is a view shape. They sometimes look identical at the beginning of a feature, which is exactly why they get accidentally coupled. When an optional field changes meaning, that coupling turns a local package upgrade into a cross-application repair job.

Name the conversion deliberately. A `toInvoiceListProps` function can decide that a missing `status` query means “show all,” while an `InvoiceFilterInput` can reject a present but malformed status. Neither rule needs to leak into a presentational table component. The component receives a stable list and an explicit filter state. The controller receives validated input. The query parser owns the translation in between.

This separation pays for itself during handoff. A developer who did not write the original screen can locate the adapter, read the tests, and see where a new optional field becomes a domain decision. It also limits AI-assisted edits. Give an assistant the adapter file, its test, and the permitted downstream type. Do not give it a repository-wide instruction to “make strict mode pass.” The former produces a reviewable patch; the latter encourages casts, unrelated formatting, and changes that have no shared owner.

For a team, add two lightweight review questions: “Where does this value first become trustworthy?” and “Can a caller express an invalid state that the next layer has to guess about?” If the answer to either question is unclear, the migration is not ready. Keep the pull request small enough to revert, and keep the decision close to the code that enforces it.

![Three decision paths: fix caller, normalize boundary, or widen deliberately](/img/typescript-migration-contract-4.png)

The same discipline helps an AI coding assistant. Give it the contract, the adapter path, a failing type test, and the allowed files. Do not ask it to “fix all TypeScript errors.” That instruction invites scattered casts and unrelated cleanup. A bounded task makes the generated diff easier to verify and revert. The broader workflow belongs with [developer tools](/developer-tools/) and the migration habits in [Laravel + Vue SaaS](/laravel-vue-saas/); start new contributors with the operating assumptions on [Start Here](/start-here/).

## What you should do Monday morning

1. Turn on `exactOptionalPropertyTypes` in a branch or select one existing strictness error. Do not start by changing every package and every screen.
2. Pick one failing object and write down whether the optional key means absent, default, reset, or invalid. Put that sentence in the pull request.
3. Move conversion into one named boundary function. Make downstream components receive a stable, non-optional shape where that is the real contract.
4. Add one compile-time test and one runtime test. Then exercise one component, route, or Laravel resource that supplies the input.
5. Pin the dependency under review, commit the lockfile, and run the same install and test commands CI will run.
6. Record the rollback before merge: revert the lockfile and adapter, or disable the guarded code path. Schedule removal of any temporary compatibility layer.

A strict compiler setting does not create the ownership problem. It exposes it while the change is still small enough to review. Treat that moment as an opportunity to leave a contract behind. The durable output is not a green local build alone; it is a boundary that another developer can inspect, test, explain, and reverse without rediscovering the decision.

## Further reading

- {{< source href="https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html" label="TypeScript: exactOptionalPropertyTypes" >}}
- {{< source href="https://vitest.dev/guide/testing-types" label="Vitest: Testing Types" >}}
- {{< source href="https://docs.npmjs.com/cli/v11/commands/npm-ci" label="npm ci documentation" >}}
