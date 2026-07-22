---
title: "Vue Query Cache Invalidation Is a Contract, Not a Refetch Button"
date: 2026-07-22T07:00:00+07:00
draft: false
slug: vue-query-cache-invalidation-contract
description: "A successful Laravel mutation does not prove a Vue admin screen is fresh. Define query-key ownership, invalidation, rollback, and hydration as one cache contract."
topics: ["frontend-engineering"]
tags: ["vue", "tanstack-query", "cache-invalidation", "laravel", "admin-screens"]
cover: /covers/vue-query-cache-invalidation-contract.png
seo:
  primaryQuery: "Vue Query cache invalidation"
  secondaryQueries:
    - "TanStack Vue Query mutation invalidation"
    - "Laravel Vue stale admin list"
    - "optimistic update rollback Vue Query"
---

A save can return `200 OK`, the detail view can show the new value, and the list that brought the operator there can still show yesterday’s row. That is not a cosmetic bug. In an admin screen, the list is often the operational truth: who is assigned, which invoice is overdue, whether an account is active, or which queue needs attention.

The usual response is to add a refetch button. That hides the decision that caused the stale screen: nobody owns the relationship between a mutation and the query keys it changes. The question is not whether this demos well; it is whether it survives maintenance, handoff, and local constraints.

TanStack Query already gives us the primitives: query keys, invalidation, mutation callbacks, optimistic updates, cancellation, snapshots, and hydration. Its documentation describes invalidation as marking matching queries stale and refetching active observers; mutation callbacks are where teams connect a completed write to that work. [Source: TanStack Query invalidation guide](https://tanstack.com/query/v5/docs/framework/react/guides/query-invalidation) [Source: mutations guide](https://tanstack.com/query/v5/docs/framework/react/guides/invalidations-from-mutations)

The hard part is not calling an API. It is writing a contract that says which cached facts a write invalidates, which screen owns the policy, what gets restored after failure, and how server-rendered state joins the browser cache. This is a practical companion to the maintenance boundaries in [Laravel + Vue SaaS](/laravel-vue-saas/) and the verification habits collected in [Developer Tools](/developer-tools/).

<!--more-->

![A Laravel mutation affects several cache claims](/img/vue-query-cache-invalidation-contract-1.png)

## A cache key is an ownership boundary

A query key is not a convenient array you type beside `useQuery`. It is the address of a server-state claim. A record key such as `['users', userId]` says “this browser has a cached representation of one user.” A filtered list key such as `['users', { status: 'active', teamId }]` says something different: “this browser has a cached result set for this exact filter.” A dashboard counter is a third claim.

When an operator changes a user’s status, all three claims may change. The record is different. The active list may gain or lose a row. A count may change. A mutation that invalidates only the record key is internally consistent but operationally incomplete.

Write a small key factory before writing mutation callbacks. The factory makes the available cache claims visible, prevents ad-hoc spelling differences, and gives review a concrete surface.

```typescript
// resources/js/features/users/userKeys.ts
export type UserFilters = {
  status?: "active" | "suspended";
  teamId?: string;
};

export const userKeys = {
  all: ["users"] as const,
  lists: () => [...userKeys.all, "list"] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  detail: (id: string) => [...userKeys.all, "detail", id] as const,
  summary: () => [...userKeys.all, "summary"] as const,
};
```

This is intentionally boring. It captures a useful rule: every query key must have a named owner and a documented scope. A feature module owns its key factory. A route does not quietly invent a competing key. An API client does not decide which UI filter is affected. That separation keeps transport details from becoming accidental presentation policy.

| Cached claim | Example key | A status change can affect it? | Expected action |
|---|---|---:|---|
| One record | `userKeys.detail(id)` | Yes | Replace or invalidate |
| Filtered list | `userKeys.list(filters)` | Yes | Invalidate the list family |
| Aggregate summary | `userKeys.summary()` | Yes | Invalidate or recompute |
| Unrelated audit feed | `['audit', id]` | Depends on product contract | Decide explicitly |

The table is the beginning of an invalidation map. Keep it near the mutation code or in the feature’s architecture note. If a reviewer cannot identify the affected claims, the mutation is not ready to merge.

## A Laravel write boundary must return a usable fact

The browser cannot invalidate responsibly when the server responds with an ambiguous success body. A `204 No Content` is valid HTTP, but it gives the mutation no canonical record to put into a detail cache. It also makes client-side validation of the final server state impossible.

For an edit endpoint, return the resource that Laravel actually persisted. Use a request object to keep authorization and validation at the boundary, and use a resource to keep the response shape intentional.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\UpdateUserRequest;
use App\Http\Resources\UserResource;
use App\Models\User;

final class UserController
{
    public function update(UpdateUserRequest $request, User $user): UserResource
    {
        $user->fill($request->validated());
        $user->save();

        return new UserResource($user->fresh());
    }
}
```

This code does not solve list membership by itself. It does establish a clean boundary: the client receives the saved representation, not the submitted form and not a guessed state. That matters when the server normalizes values, applies authorization, assigns defaults, updates timestamps, or fires domain logic.

{{< field-note title="Field note" >}}
In Laravel/Vue maintenance work, the expensive stale-data incident is rarely a failed request. It is a successful request that leaves two screens disagreeing. Treat the mutation response, invalidation map, and rollback behavior as one handoff artifact. On Modoo Laravel SaaS projects, that artifact gives the next maintainer a way to reason about list filters and counters without replaying the original bug in production.
{{< /field-note >}}

{{< note type="warning" title="Do not make the refetch button the contract" >}}
A manual refresh can remain a recovery control for operators. It must not be the only path by which a completed mutation makes affected server state fresh.
{{< /note >}}

## Invalidate the family, then update the detail deliberately

TanStack Query supports partial matching for invalidation. The official guide shows that a prefix can mark queries beginning with that key stale. That makes a list family a useful invalidation target when a mutation can change membership across filters. [Source: TanStack Query query invalidation](https://tanstack.com/query/v5/docs/framework/react/guides/query-invalidation)

Use the successful response to update the most specific record, then invalidate the list and summary families. This avoids pretending that one form knows every filter currently open in the application.

```typescript
import { useMutation, useQueryClient } from "@tanstack/vue-query";
import { api } from "@/lib/api";
import { userKeys, type UserFilters } from "./userKeys";

type User = { id: string; name: string; status: "active" | "suspended" };
type UpdateUser = { id: string; name: string; status: User["status"] };

export function useUpdateUser(filters: UserFilters) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (input: UpdateUser) => {
      const { data } = await api.patch<User>(`/users/${input.id}`, input);
      return data;
    },
    onSuccess: async (savedUser) => {
      queryClient.setQueryData(userKeys.detail(savedUser.id), savedUser);

      await Promise.all([
        queryClient.invalidateQueries({ queryKey: userKeys.lists() }),
        queryClient.invalidateQueries({ queryKey: userKeys.summary() }),
      ]);
    },
  });
}
```

The `filters` argument is useful only if the feature uses it for a targeted optimistic list update or for UI behavior. Do not pass it merely because the component had it. A broad list-family invalidation expresses the safer default: any active filtered user list is eligible to refetch. If that creates unacceptable load, measure the actual query traffic and design a narrower invalidation map with explicit product cases. Do not replace a contract with a guess about performance.

A recent `@tanstack/vue-query` 5.101.4 update was described in the local release research as an eslint-plugin-query change, not a cache or hydration migration. That is exactly why release numbers should not drive this design. Cache ownership is an application contract, not a reaction to a patch note.

![Detail record, filtered lists, and summary are separate cache claims](/img/vue-query-cache-invalidation-contract-2.png)

## Optimism requires a rollback owner

Optimistic updates improve responsiveness only when failure has an equally explicit path. TanStack Query’s optimistic-update guidance cancels outgoing fetches, snapshots previous data, changes cached data, and uses the saved result for rollback on error. [Source: TanStack Query Vue optimistic updates](https://tanstack.com/query/v5/docs/framework/vue/guides/optimistic-updates)

The important discipline is ownership. The same mutation that writes the optimistic state must own the snapshot and restoration. A global “refresh everything after an error” helper cannot restore a screen deterministically when the network is unavailable or when another mutation is in flight.

```typescript
import { useMutation, useQueryClient } from "@tanstack/vue-query";
import { api } from "@/lib/api";
import { userKeys } from "./userKeys";

type User = { id: string; name: string; status: "active" | "suspended" };

export function useSuspendUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => api.patch<User>(`/users/${id}`, { status: "suspended" }),
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: userKeys.lists() });
      const previousLists = queryClient.getQueriesData<User[]>({ queryKey: userKeys.lists() });

      queryClient.setQueriesData<User[]>({ queryKey: userKeys.lists() }, (users) =>
        users?.filter((user) => user.id !== id),
      );

      return { previousLists };
    },
    onError: (_error, _id, context) => {
      for (const [key, value] of context?.previousLists ?? []) {
        queryClient.setQueryData(key, value);
      }
    },
    onSettled: async () => {
      await queryClient.invalidateQueries({ queryKey: userKeys.lists() });
      await queryClient.invalidateQueries({ queryKey: userKeys.summary() });
    },
  });
}
```

This example removes a suspended user from cached active lists. It does not assert that every product should do that. Some products keep suspended users visible with a badge. The contract is the point: name the expected list membership, implement it once, restore the prior snapshot on failure, and reconcile with the server after settlement.

## SSR hydration is part of the same agreement

A server-rendered application has another cache producer before the browser runs: the server. TanStack Query’s Vue SSR material explains that a query client is dehydrated on the server and hydrated on the client; by default, successful queries are included in dehydration. [Source: TanStack Query Vue SSR](https://tanstack.com/query/v5/docs/framework/vue/guides/ssr) [Source: hydration reference](https://tanstack.com/query/v5/docs/framework/vue/reference/hydration)

That means a stale bug can be created before an operator clicks Save. If the server prefetched `['users', 'list', { status: 'active' }]` but the browser component asks for `['user-list', { status: 'active' }]`, hydration does not join them. The page may render server data and then fetch a separate browser cache entry. A mutation can invalidate one key while the other remains visible.

Make the key factory importable from both the SSR prefetch code and browser feature module. Test the first client render, not only the API response. For an Inertia application without full server rendering, the equivalent boundary may be initial page props rather than dehydration, but the rule remains: name the producer and the cache address used after navigation.

{{< details summary="A short hydration review checklist" >}}
1. Confirm the server and browser import the same key factory.
2. Confirm serialized filters have stable shapes and names.
3. Confirm the first browser render uses the hydrated key rather than a parallel key.
4. Confirm a mutation invalidates the same list family that the hydrated screen observes.
5. Confirm an error path restores optimistic state before the next successful refetch.
{{< /details >}}

![A shared key factory connects server prefetch, browser hydration, and invalidation](/img/vue-query-cache-invalidation-contract-3.png)

## Test the disagreement, not only the request

A feature test that asserts “PATCH returned 200” proves the controller accepted a request. It does not prove cache correctness. Add a client test for the stale-admin-list scenario: seed a list and a detail record, perform the mutation, assert that the list family was invalidated, and assert that a failed mutation restores the snapshot.

```typescript
import { describe, expect, it, vi } from "vitest";
import { QueryClient } from "@tanstack/vue-query";
import { userKeys } from "./userKeys";

describe("user cache contract", () => {
  it("marks every user list stale after a successful edit", async () => {
    const queryClient = new QueryClient();
    const invalidateQueries = vi.spyOn(queryClient, "invalidateQueries");

    await queryClient.invalidateQueries({ queryKey: userKeys.lists() });

    expect(invalidateQueries).toHaveBeenCalledWith({
      queryKey: userKeys.lists(),
    });
  });
});
```

The example is deliberately small. Your integration test should exercise the mutation hook with a mocked API response and a realistic active-list key. The test name should describe the user-visible disagreement it prevents: “suspending a user refreshes active user lists,” not “calls invalidateQueries.” The latter tests an implementation detail; the former preserves a contract.

### Put the contract where a future change can find it

A cache contract needs a home outside the current developer’s memory. A short `CACHE_CONTRACT.md` in the feature directory is enough. It should name the key factory, mutation endpoints, affected list families, aggregate keys, optimistic behavior, server-rendering producer, and test fixture. The document should not repeat framework documentation. It should answer local questions that the framework cannot answer: does a suspended user disappear from this team’s active list, does the assignment counter include pending work, and should a failed edit return the user to the exact prior filter position?

Use pull-request review to keep the artifact honest. When a change adds a new filter, ask whether it belongs under the existing `userKeys.lists()` family. When a mutation adds a new state transition, ask which summary keys change. When a route gains SSR prefetching, ask whether it imports the same key factory. These are cheap questions before merge and expensive investigations after a support report. The same note should identify the safe fallback: invalidate the relevant family, preserve the failed form input for the operator, and avoid presenting a locally optimistic state as a confirmed server result. That gives support, product, and engineering one language for discussing freshness.

A useful failure drill is to disable the mutation endpoint in a local environment, edit a row from a filtered list, and watch the screen. The expected behavior should be explicit: an optimistic row returns to its previous state, the detail view does not claim the edit succeeded, and the list is reconciled when connectivity returns. Capture that behavior in a test or a repeatable browser check. The value is not a dramatic demo; it is a reliable diagnosis when the next feature changes the same data from a different screen.

## What you should do Monday morning

1. Pick one Laravel/Vue admin mutation that changes list membership or a dashboard count.
2. List every cached claim it affects: record, filtered lists, summaries, and any server-rendered initial state.
3. Create or clean up a feature-owned key factory. Delete competing ad-hoc key arrays.
4. Make the Laravel endpoint return the persisted resource shape used by the detail view.
5. Add an `onSuccess` policy that updates the detail and invalidates affected list and summary families.
6. If the screen uses optimism, add cancellation, a snapshot, an error restore, and an `onSettled` reconciliation.
7. Write one test for the successful-save/stale-list scenario and one for rollback after a failed write.
8. Add the invalidation map to the feature handoff notes so the next filter or counter has an owner.

The refetch button may stay. It becomes an operator tool rather than the only proof that an application knows which facts changed. That distinction keeps recovery visible without making user patience responsible for an unfinished data contract. It also gives an incident responder a clear first question: which cached claim was not updated, invalidated, restored, or hydrated after the write?

## Further reading

- {{< source href="https://tanstack.com/query/v5/docs/framework/react/guides/query-invalidation" label="TanStack Query: Query Invalidation" >}}
- {{< source href="https://tanstack.com/query/v5/docs/framework/react/guides/invalidations-from-mutations" label="TanStack Query: Invalidations from Mutations" >}}
- {{< source href="https://tanstack.com/query/v5/docs/framework/vue/guides/optimistic-updates" label="TanStack Query Vue: Optimistic Updates" >}}
- {{< source href="https://tanstack.com/query/v5/docs/framework/vue/guides/ssr" label="TanStack Query Vue: SSR" >}}

For broader operational checks, see [AI agent operations](/ai-agent-operations/) and the [site start page](/start-here/). The same pattern applies: name the state, name the owner, retain an artifact, and verify the readback.
