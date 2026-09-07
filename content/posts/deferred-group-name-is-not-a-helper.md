---
title: "A Deferred Group Name Is Not a Helper"
date: 2026-09-07T07:00:00+07:00
draft: false
slug: "deferred-group-name-is-not-a-helper"
description: "A deferred Inertia group named auth is a request batch, not a PHP function. A red loadDeferredProps test is not a missing Vue prop. Name who owns the group strings."
topics: ["developer-tools"]
tags: ["inertia", "laravel", "deferred-props", "php", "feature-tests", "coding-agents", "vue"]
cover: /covers/deferred-group-name-is-not-a-helper.png
seo:
  primaryQuery: "Inertia deferred props group name PHP helper"
  secondaryQueries:
    - "loadDeferredProps auth TypeError Closure"
    - "Inertia::defer group name not a callback"
    - "inertia-laravel testing helper is_callable"
---

The dashboard is green in the browser. Users load. Roles load. The Vue `Deferred` fallback flips to the user card. The feature test is red. Standup hears “Inertia dropped the auth group.”

I stop the run there. A deferred group named `auth` is a request batch. It is not the Laravel `auth()` helper. A red `loadDeferredProps('auth')` line this week is not a missing Vue prop.

On 4 September 2026 the Laravel adapter for Inertia published a testing-helper fix: `loadDeferredProps()` crashed when the group string matched a global PHP function. The Vue npm client did not move. [Source: https://github.com/inertiajs/inertia-laravel/releases/tag/v3.3.3] [Source: https://github.com/inertiajs/inertia-laravel/pull/908]

I already refused to treat a missing Issues tab as a missing ticket in [An Issues Tab Is Not a Laravel Package Ticket](/blog/issues-tab-is-not-a-package-ticket/). I already refused to treat a green `apt` line as a trusted key in [A Green apt Update Is Not a Trusted Key After Saturday](/blog/green-apt-is-not-a-trusted-key/). This post is the deferred-props version of the same desk rule. Name the group. Name whether it collides with a PHP helper. Name who owns that string before a coding agent copies `auth` from the controller into the test.

The question is not whether the Vue client bumped. The question is whether your next feature test treats a batch name as a callback.

<!--more-->

![Browser green, test red, named owner of the deferred group list](/img/deferred-group-name-is-not-a-helper-1.png)

## The red test that looks like a missing prop

Juniors read a failing Inertia assertion the way they read a blank Vue slot. The test asked for the `auth` group. The assertion exploded. They open the Vue file and add another `<Deferred data="user">` wrapper.

The page was never the failure.

Official Inertia docs are plain: deferred props load after the first render, and group names are arbitrary strings. You pick a label so two or three slow queries ride the same follow-up request. [Source: https://inertiajs.com/docs/v2/data-props/deferred-props]

That string lives in two places:

1. The controller: `Inertia::defer(fn () => ..., 'auth')`
2. The feature test: `$inertia->loadDeferredProps('auth', function ...)`

The second call is a **testing** helper on `AssertableInertia`. It is not the browser. It is not `@inertiajs/vue3`. It is PHP asking the test response to resolve one deferred batch so you can `where()` the payload.

The crash from the public pull request is a type error, not an empty array:

```text
TypeError: reloadOnly(): Argument #2 ($callback) must be of type ?Closure, string given
```

[Source: https://github.com/inertiajs/inertia-laravel/pull/908]

Standup translation that I refuse: “the user prop never arrived.” The helper never reached the user prop. It treated the word `auth` as the callback and dropped the closure you actually passed.

{{< note type="warning" title="The page can be right while the test is wrong" >}}
If the browser shows the deferred card and PHPUnit dies inside `loadDeferredProps()`, do not rewrite the Vue tree first. Print the group string. Check whether PHP already has a function of that name. Fix the assertion contract before you “fix” the UI.
{{< /note >}}

## Why PHP thought your group was a function

The old helper did this:

```php
$callback = is_callable($groupsOrCallback) ? $groupsOrCallback : $callback;
$groups = is_callable($groupsOrCallback) ? array_keys($this->deferredProps) : Arr::wrap($groupsOrCallback);
```

[Source: https://github.com/inertiajs/inertia-laravel/pull/908]

`is_callable()` on a string does not mean “this is a Closure.” It means “a function with this name exists.” Laravel’s global helpers make that true for names you will type without thinking:

| Group string you typed | PHP already has | What the old helper did |
| --- | --- | --- |
| `auth` | `auth()` | Treated the string as the callback. Dropped your Closure. |
| `session` | `session()` | Same. |
| `collect` | `collect()` | Same. |
| `custom` | no global `custom()` | Group stayed a group. Test passed. |

The pull request says those first three are “totally normal group names.” They are. They are also function names. [Source: https://github.com/inertiajs/inertia-laravel/pull/908]

The method’s own signature already told the truth: `Closure|array|string $groupsOrCallback`. A string is a group list. A Closure is “load every deferred group, then run this.” The old `is_callable()` check flattened that distinction.

The fix is one type check:

```php
$callback = $groupsOrCallback instanceof \Closure ? $groupsOrCallback : $callback;
$groups = $groupsOrCallback instanceof \Closure ? array_keys($this->deferredProps) : \Illuminate\Support\Arr::wrap($groupsOrCallback);
```

[Source: https://github.com/inertiajs/inertia-laravel/pull/908]

That is not a Vue rewrite. That is not a new Inertia protocol. That is PHP stopping the habit of asking “does a function named like this string exist?”

I keep a tiny probe next to the test so a junior can see the trap without opening GitHub:

```bash {linenos=inline,hl_lines=[12,18]}
#!/usr/bin/env bash
set -euo pipefail
# Usage: ./probe-group-callable.sh auth
group="${1:?group string}"

php -r '
$g = $argv[1];
echo "group=" . $g . PHP_EOL;
echo "is_callable=" . (is_callable($g) ? "true" : "false") . PHP_EOL;
echo "instanceof_closure=" . (($g instanceof Closure) ? "true" : "false") . PHP_EOL;
' "$group"
```

Run it on `auth` inside a Laravel app bootstrap and you get `is_callable=true`. Run it on `sidebar` and you get `false` unless you defined `sidebar()`. The probe does not pin a package. It names the collision.

![String treated as a function versus Closure check so the group stays a batch name](/img/deferred-group-name-is-not-a-helper-2.png)

## How I prove the group before anyone copies `auth`

Do not argue from a stack trace screenshot. Reproduce the collision in a feature test you own.

The adapter’s own regression test is the contract I copy, then I change the names to match the app:

```php {linenos=inline,hl_lines=[6,16]}
public function test_deferred_auth_group_is_a_batch_not_a_helper(): void
{
    $response = $this->get('/dashboard');

    $response->assertInertia(function (\Inertia\Testing\AssertableInertia $page) {
        $page->component('Dashboard')
            ->has('users')
            ->loadDeferredProps('auth', function (\Inertia\Testing\AssertableInertia $page) {
                $page->where('currentUser.email', 'owner@example.test');
                $page->missing('auditRows');
            });
    });
}
```

If this dies with `reloadOnly(): Argument #2 ($callback) must be of type ?Closure, string given`, the group string is the bug in the **test helper**, not a missing email. [Source: https://github.com/inertiajs/inertia-laravel/pull/908]

The shipped regression used `'auth'` and `'custom'` on two deferred props, then asserted only the `auth` batch resolved. That is the screenshot I want on a junior screen: one group in, one prop present, the other group still missing. [Source: https://github.com/inertiajs/inertia-laravel/pull/908]

Controller side, I still write the group as a batch label, never as a helper name I do not intend:

```php
return Inertia::render('Dashboard', [
    'users' => User::query()->limit(20)->get(),
    'currentUser' => Inertia::defer(fn () => auth()->user(), 'current-user'),
    'auditRows' => Inertia::defer(fn () => AuditRow::query()->latest()->limit(10)->get(), 'audit'),
]);
```

`current-user` and `audit` are ugly on purpose. They do not match `auth()` or `collect()`. Official docs already say group names are arbitrary. Use that freedom. [Source: https://inertiajs.com/docs/v2/data-props/deferred-props]

{{< details summary="If a coding agent still names the group auth" >}}
I do not let the agent “fix” the test by deleting `loadDeferredProps` and asserting only the first-paint props. That hides the deferred payload. I also do not let it rename the Vue `data` prop to match a PHP helper. Vue `data="currentUser"` is a **prop key**. PHP `'current-user'` is a **group**. Mixing those two strings is a second class of bug. The agent must print both maps: prop keys vs group names.
{{< /details >}}

## Adapter pin is not a Vue bump

Sunday already had enough “the package moved” noise on this desk. This one is easy to misread as a frontend bump. It is not.

| Surface | What moved on 4 September 2026 | What did not |
| --- | --- | --- |
| Laravel adapter 3.x | Testing helper `loadDeferredProps()` uses `instanceof Closure` | Vue runtime |
| Laravel adapter 2.x | Same helper fix on the 2.x line | Vue runtime |
| npm `@inertiajs/vue3` | — | `latest` stayed `3.7.0` (18 August 2026) |

[Source: https://github.com/inertiajs/inertia-laravel/releases/tag/v3.3.3] [Source: https://github.com/inertiajs/inertia-laravel/releases/tag/v2.0.26] [Source: https://registry.npmjs.org/@inertiajs/vue3]

The 3.x pull request is [#908](https://github.com/inertiajs/inertia-laravel/pull/908) by mdalikadar, merged 4 September 2026. The 2.x twin is [#909](https://github.com/inertiajs/inertia-laravel/pull/909) by pascalbaljet, same day. Packagist lists the 3.x line as the current adapter series. [Source: https://repo.packagist.org/p2/inertiajs/inertia-laravel.json]

I do not bump `@inertiajs/vue3` to “pick up the auth group fix.” There is nothing to pick up on the client. The `<Deferred>` component still waits on **prop keys**, not PHP group strings.

I also do not paste the adapter tag into a changelog title and call the post done. The useful sentence is: **the test helper no longer treats a group string as a PHP function.** The tag is evidence after that sentence, once.

If your app is still on the 2.x adapter line, the same helper bug lived there. The 2.x release notes say so in one line. Do not invent a Vue 2 story from that. [Source: https://github.com/inertiajs/inertia-laravel/releases/tag/v2.0.26]

![Laravel testing helper versus unchanged Vue client, named lockfile owners](/img/deferred-group-name-is-not-a-helper-3.png)

## What I refuse to let a coding agent name

A coding agent loves short group names. `auth`. `user`. `cache`. `event`. Those strings are also the Laravel helper table.

Desk rules this week:

1. **Group strings are allow-listed.** The list lives next to the Inertia controllers, not in chat. `current-user`, `billing-summary`, `audit` — hyphenated, boring, not a PHP function.
2. **The agent does not invent a group to match a helper.** If the controller already says `'auth'`, a human decides whether to rename or to pin the testing helper. The agent does not “simplify” it back to `auth` for style.
3. **A red `loadDeferredProps` is a PHP type error until proven otherwise.** The agent’s first artifact is the exception class and argument types, not a Vue diff.
4. **Vue `data=` is not the group.** The agent must not copy the PHP group string into `<Deferred data="auth">` unless `auth` is actually the prop key.

I already refused to give a coding agent merge rights in [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/). The same human who owns the merge click owns the deferred-group list. An agent may open the PR that renames `'auth'` to `'current-user'`. A named reviewer still says the string is a batch, not a helper.

{{< field-note title="Field note" >}}
On the Laravel and Vue SaaS apps I keep under [/laravel-vue-saas/](/laravel-vue-saas/), deferred groups show up on billing dashboards and audit drawers — the slow queries you hide behind a skeleton. A group named `session` or `auth` looks tidy in a controller and is poison in `loadDeferredProps` on an unpatched testing helper. I keep a one-column list in the app notes: group name, props in that batch, owner. Copilot does not get to add a row. The person who already owns change control on [/developer-tools/](/developer-tools/) also owns “does this string match a PHP helper on this runtime.”
{{< /field-note >}}

## A named owner, not a silent composer bump

Composer can already have the testing-helper fix while the team still copies `auth` into new tests. A bump without an owner is a date on `composer.lock`. It is not a naming policy.

I want three artifacts in the PR, not a lockfile selfie:

1. **The group map** — markdown table: group string, prop keys, PHP helper collision (`yes`/`no` from the probe).
2. **One feature test** that calls `loadDeferredProps` with the real group and asserts the deferred prop, not only the first-paint props.
3. **The owner line** — GitHub handle in the PR body: who is allowed to add a new group name this week.

If the map says `auth` collides, we rename the group in the controller and the test in the same PR. We do not leave the Vue file as the “fix.” We do not wait for a later adapter tag to make a bad name safe. The adapter fix makes the **old** name testable. It does not make `auth` a good name.

Rollback is the same shape. If a lockfile bump is the only change and tests still use colliding names on an older helper, revert the bump and ship the rename first. A rename works on the old helper. A bump without a rename still leaves the next agent one `collect` group away from the same TypeError.

{{< note type="success" title="The Monday screenshot" >}}
A junior should be able to photograph three lines: the controller group string, `php -r` `is_callable` for that string, and the `loadDeferredProps` call. If those three disagree, stop. Do not open Vue DevTools yet.
{{< /note >}}

## What production did not break

I am not claiming the browser deferred fetch crashed. The public diff for the 3.x fix is `src/Testing/AssertableInertia.php` plus one PHPUnit method. Production `Inertia::defer()` already stored the group as a string on the deferred prop object. [Source: https://github.com/inertiajs/inertia-laravel/pull/908]

That distinction matters for triage:

- Browser skeleton stuck: look at prop keys, network tab, `deferredProps` JSON.
- PHPUnit TypeError on `reloadOnly`: look at `loadDeferredProps` and `is_callable($group)`.
- Empty deferred prop after a successful helper: look at the query inside the defer closure.

Mixing those three is how a one-line testing bug becomes a two-day Vue rewrite.

Official grouping example uses `'attributes'` for teams, projects, and tasks. That word is safer than `auth` because PHP does not ship `attributes()`. Safer is not the same as owned. Put `'attributes'` on the map too. [Source: https://inertiajs.com/docs/v2/data-props/deferred-props]

![Named owner checklist: group map, helper probe, feature test, merge owner](/img/deferred-group-name-is-not-a-helper-4.png)

## What you should do Monday morning

1. **List every `Inertia::defer(..., '…')` group in the app.** One table. Prop keys in the second column. Owner in the third.
2. **Run the `is_callable` probe** on each group inside `php artisan tinker` or the bash snippet above. Any `true` is a rename candidate, even if tests are green on a patched helper.
3. **Add or fix one feature test** that calls `loadDeferredProps` with a real group and asserts one deferred prop. If it TypeErrors, you are on the old testing helper — pin the Laravel adapter that contains the `instanceof Closure` check, then still rename the colliding group.
4. **Do not bump `@inertiajs/vue3` for this.** Confirm npm `latest` yourself if someone claims the client “fixed auth groups.”
5. **Write the owner in the PR template.** New deferred group names go through that person. Coding agents copy the allow-list. They do not invent `cache` at 01:00.

## Further reading

- {{< source href="https://github.com/inertiajs/inertia-laravel/pull/908" label="inertia-laravel pull request: group name vs helper in loadDeferredProps" >}}
- {{< source href="https://inertiajs.com/docs/v2/data-props/deferred-props" label="Inertia deferred props: groups are arbitrary strings" >}}
- {{< source href="https://github.com/inertiajs/inertia-laravel/releases/tag/v3.3.3" label="Laravel adapter 3.x testing-helper release notes" >}}

Related on this site: [An Issues Tab Is Not a Laravel Package Ticket](/blog/issues-tab-is-not-a-package-ticket/), [A Green apt Update Is Not a Trusted Key After Saturday](/blog/green-apt-is-not-a-trusted-key/), [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/), and the hubs at [/developer-tools/](/developer-tools/) and [/laravel-vue-saas/](/laravel-vue-saas/).
