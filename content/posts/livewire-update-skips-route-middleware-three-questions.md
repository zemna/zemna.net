---
title: "A Livewire Update Can Skip Your Route Middleware Under Three Conditions: Three Questions to Ask Before You Bump"
date: 2026-11-23T07:00:00+07:00
draft: false
slug: "livewire-update-skips-route-middleware-three-questions"
description: "A Livewire advisory published Nov 21 says a component update sent through another hostname can run without the page's persistent middleware. Three yes/no questions, a read-only script, and the one line to move into your actions."
topics: ["laravel"]
tags: ["laravel", "livewire", "security-advisory", "middleware", "multi-tenant", "composer", "patch-management", "authorization"]
cover: /covers/livewire-update-skips-route-middleware-three-questions.png
seo:
  primaryQuery: "livewire persistent middleware bypass different host"
  secondaryQueries:
    - "livewire GHSA-vw9g-2c4c-g767"
    - "livewire addPersistentMiddleware domain route authorization"
    - "check livewire version composer.lock multi tenant subdomain"
---

Picture a small SaaS built on Laravel and Livewire. Every customer gets a subdomain, `acme.example.com`, `globex.example.com`. The route file says "this page only answers on a tenant domain, and only if the user is allowed to edit the post". The route carries a `can:update,post` rule, and everybody sleeps well because the rule sits right there on the route.

Then a Livewire advisory lands, and it says that in one specific setup the rule on the route is not applied to the buttons on the page. Not on the first page load. On the follow-up requests that Livewire sends when someone clicks, types, or saves.

That is the part worth a careful read, and it is also the part that needs three conditions to be true at once. Plenty of apps will answer "no" to at least one of them. The useful work today is finding out which way yours goes, in about ten minutes, without panic.

<!--more-->

The question is not whether the advisory sounds scary. It is whether your own repo has all three conditions, and whether the permission check lives only on the route or also inside the action that changes data.

## What the advisory says, in plain words

I read the advisory page on GitHub on Nov 23 at about 08:00 Jakarta time. It is titled "Changing the Host can bypass Livewire persistent middleware", published by the Livewire maintainer on Nov 21, 2026. I cross-checked the version numbers against the GitHub releases and the Composer package list.

| Fact | What the page says |
|---|---|
| Severity | Moderate, CVSS 3.1 base score 6.8 (network, high attack complexity, low privileges, no user interaction) |
| CVE | No known CVE |
| Affected versions | `>= 3.7.4, < 3.8.12` and `>= 4.0.0, < 4.4.9` |
| Patched versions | `3.8.12` and `4.4.9` |
| Impact in the advisory's words | "bypass persistent route middleware on component updates in specific scenarios", including "bypasses of route-level authorization and tenant isolation" |
| Release notes for both patches | "Includes security fixes and reliability improvements. Updating is recommended." and "Refresh already-open pages after deploying the update." |

The advisory then lists exactly when an app is affected. All three at once:

1. A component is rendered on a **domain-constrained route**.
2. Access control **relies on Livewire's persistent middleware**.
3. The Livewire update endpoint is **available through another host** served by the same application.

It adds one more sentence that matters for how seriously to take it: "Exploitation requires a valid signed component snapshot but does not require the snapshot to be modified." So this is not a forged-payload story. It is a normal page, loaded normally, followed by an update that arrives on a different hostname.

The advisory credits an automated scanner for the report. That is not a reason to rank the issue up or down. It is only a reminder that this class of bug, "a rule was applied on the way in and quietly not applied on the way back", is now cheap to find, so expect more of them across every framework.

## First, what "persistent middleware" actually is

If you have never typed `addPersistentMiddleware`, you are still using the feature. The Livewire docs explain it with a route like this:

```php
Route::livewire('/post/{post}', App\Livewire\UpdatePost::class)
    ->middleware('can:update,post');
```

When the page loads, Laravel runs `can:update,post`. If you may not edit the post, you never see the page. But a Livewire page keeps talking to the server after it loads: every `wire:click`, every `wire:model.live` round trip is a new request to Livewire's update endpoint. That request does not go to your route. So Livewire remembers which middleware ran on the first load and re-applies it to the follow-ups. That is "persistent middleware", and the docs say it protects you when "the authorization rules or user permissions have changed after the initial page-load".

By default Livewire re-applies a fixed list: the Sanctum and Jetstream session middleware, `AuthenticateWithBasicAuth`, `SubstituteBindings`, `RedirectIfAuthenticated`, `Authenticate`, and `Authorize`. If your own middleware is not on that list, you register it yourself in a service provider:

```php
// app/Providers/AppServiceProvider.php
use Livewire\Livewire;

public function boot(): void
{
    Livewire::addPersistentMiddleware([
        \App\Http\Middleware\EnsureUserHasRole::class,
    ]);
}
```

Two practical notes from the docs. Persistent middleware does not take arguments in that list, so `AuthorizeResource::class.':admin'` is the wrong shape. And because `auth` and `can:` map to `Authenticate` and `Authorize`, a plain `->middleware('auth')` or `->middleware('can:update,post')` on a Livewire route already counts as persistent middleware. You do not need to have written a line of Livewire-specific code to be in condition 2.

## Where it went wrong, in one picture

{{< note type="note" title="How to read this section" >}}
This is the advisory's own explanation, not a test I ran. I did not reproduce the bypass, and this post does not contain steps to do so.
{{< /note >}}

![Request flow before and after the Livewire patch: before, an update through a second host runs the action with no route middleware; after, Livewire checks origin and route context and answers 404.](/img/livewire-update-skips-route-middleware-three-questions-1.png)

The advisory's "Details" paragraph says this, and I have kept it close to the original:

- When a component is rendered, Livewire stores the original request **path and method** in the component snapshot, so persistent middleware can be re-applied later.
- It did **not** store the original **host** or the **resolved route**.
- On an update, Livewire rebuilds the original request from the stored path and method, but keeps the **host from the update request**.
- If that update came in through a different host, the original domain-constrained route may not match. Livewire treats "no route matched" as "no route", so the action runs **without the persistent middleware** the original page had.

Read that last line twice. The failure is not "middleware ran and said yes". It is "middleware never ran". Nothing logs a denied request, because nothing was denied.

## What the patch changes, read straight from the source

I do not trust a changelog that says "security fixes and reliability improvements", so I looked at the code. The GitHub compare view between `v3.8.11` and `v3.8.12` shows the interesting change in one file, `src/Mechanisms/PersistentMiddleware/PersistentMiddleware.php`. The commit message for the core change is "Reject Livewire updates with mismatched route context". I also fetched the same file at tag `v4.4.9` and found the same logic, and at `v4.4.8`, where the new route-context function is absent.

In plain words, after the patch:

- Every snapshot now also records the request's **origin** (scheme plus host) and a small **route context** (the route's URI and its domain).
- On an update, if the snapshot is missing those fields or they are the wrong type, Livewire answers **404**.
- If the origin of the update request is not the origin the page was rendered on, Livewire answers **404**.
- If the route that matches now is not the route the page was rendered on, Livewire answers **404**.
- A page rendered without any route (an error page, for example) is still allowed to update, as long as it also matches no route now. That is a second small commit, "Keep updates working for components rendered without a route".

Two things follow from that reading. They are my inference from the code, not something I ran.

First, the release note "Refresh already-open pages after deploying the update" makes sense. A page opened before your deploy carries an old snapshot without the new fields, and the new code answers 404 to that. So a deploy in the middle of the working day will make some users see a failed click until they reload. Plan the deploy accordingly.

Second, the patch makes the page and its updates share one origin. If your setup renders a page on one hostname and sends updates to another on purpose, expect a 404 after the bump. That is also why one of the Monday steps below is "open the app on every hostname you serve".

## Three questions, then the script

Here are the three questions in the order that rules most apps out the fastest.

**Question 1: which Livewire do you run?** Read it from `composer.lock`, not from `composer.json`, because `^3.5` in the manifest says nothing about what is installed.

```bash
composer show livewire/livewire | head -n 4
# or, without running PHP:
grep -A3 '"name": "livewire/livewire"' composer.lock
```

Below 3.7.4 is outside the advisory's range. From 3.7.4 up to 3.8.11, or from 4.0.0 up to 4.4.8, is inside it. 3.8.12 and 4.4.9 or later are patched.

**Question 2: does any route have a domain constraint?** Search `routes/`, and also your providers and `bootstrap/`, because route groups sometimes live there. You are looking for `->domain(` and `Route::domain(`.

**Question 3: do you rely on route middleware for access?** That means `auth`, `can:...`, your own `EnsureUserHasRole`, anything you would call "the permission check". If a Livewire page sits behind it, you are leaning on persistent middleware whether or not you know the name.

A "yes" on all three still does not prove you are affected. The advisory has a fourth part, "available through another host", and that part is server configuration, not code. In a wildcard-subdomain SaaS, a lot of hostnames can reach the same app. Whether one of them reaches the Livewire update endpoint is a question for your web server and DNS, and no grep over PHP answers it.

So I wrote a read-only script that answers the first three and prints the fourth as a reminder. It reads files, changes nothing, and needs only Python 3:

```python
#!/usr/bin/env python3
"""Three-question Livewire check. Reads files only; changes nothing.
Usage: python3 livewire-host-check.py /path/to/laravel-app
Advisory: GHSA-vw9g-2c4c-g767 (affected >=3.7.4,<3.8.12 and >=4.0.0,<4.4.9)."""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")


def ver(s):
    return tuple(int(x) for x in re.findall(r"\d+", s)[:3])


def lock_version():
    lock = root / "composer.lock"
    if not lock.exists():
        return None
    data = json.loads(lock.read_text())
    for pkg in data.get("packages", []) + data.get("packages-dev", []):
        if pkg["name"] == "livewire/livewire":
            return pkg["version"].lstrip("v")
    return None


def grep(pattern, folders):
    rx = re.compile(pattern)
    hits = []
    for folder in folders:
        base = root / folder
        if not base.exists():
            continue
        for f in base.rglob("*.php"):
            for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
                if rx.search(line):
                    hits.append(f"{f.relative_to(root)}:{n}: {line.strip()}")
    return hits


v = lock_version()
print(f"app: {root}")
if v is None:
    print("Q1 version : livewire/livewire not found in composer.lock -> stop, nothing to check")
    sys.exit(0)
t = ver(v)
if t < (3, 7, 4):
    q1 = "below 3.7.4: outside the advisory's affected range"
elif t < (3, 8, 12):
    q1 = "INSIDE the affected range (3.7.4 up to 3.8.11): update to 3.8.12 or later 3.x"
elif t[0] == 3:
    q1 = "patched (3.8.12 or later)"
elif t < (4, 4, 9):
    q1 = "INSIDE the affected range (4.0.0 up to 4.4.8): update to 4.4.9 or later"
else:
    q1 = "patched (4.4.9 or later)"
print(f"Q1 version : {v} -> {q1}")

dom = grep(r"->domain\(|Route::domain\(", ["routes", "app", "bootstrap"])
print(f"Q2 domain routes : {len(dom)} line(s)")
for h in dom[:5]:
    print("   " + h)

pm = grep(r"addPersistentMiddleware|setUpdateRoute", ["app", "bootstrap", "config", "routes"])
# Livewire persists auth-style route middleware by default (docs list Authenticate, Authorize, ...)
mw = grep(r"middleware\(.*(auth|can:|Authenticate|Authorize)", ["routes"])
print(f"Q3 persisted middleware : {len(pm)} custom line(s), {len(mw)} default-persisted route line(s)")
for h in (pm + mw)[:5]:
    print("   " + h)

th = grep(r"trustHosts|TrustHosts", ["app", "bootstrap"])
print(f"info trusted hosts : {'configured' if th else 'not configured (Laravel answers any Host)'}")

inside = "INSIDE" in q1
print("verdict :", end=" ")
if inside and dom and (pm or mw):
    print("all three answers are yes -> read the advisory conditions, then update and move the check into the action")
elif inside:
    print("in range, but not every condition shows up in code -> still update; keep the action-level authorize() anyway")
else:
    print("not in the affected range")
print("not checked by this script: whether a second hostname reaches the same app (that is server config)")
```

I tested it against four fake app skeletons that I built for this post (a `composer.lock` with only the Livewire entry, one `routes/web.php`, one service provider). They are fixtures, not real apps, so they prove the script's logic and nothing about your code. The second one is a patched version with the same routes:

```text
app: lw-fixtures/app-a-3.8.11-domain-persistent
Q1 version : 3.8.11 -> INSIDE the affected range (3.7.4 up to 3.8.11): update to 3.8.12 or later 3.x
Q2 domain routes : 1 line(s)
   routes/web.php:3: Route::domain('{tenant}.example.test')->middleware('can:update,post')->group(function () {
Q3 persisted middleware : 1 custom line(s), 1 default-persisted route line(s)
   app/Providers/AppServiceProvider.php:4: Livewire::addPersistentMiddleware([\App\Http\Middleware\EnsureUserHasRole::class]);
   routes/web.php:3: Route::domain('{tenant}.example.test')->middleware('can:update,post')->group(function () {
info trusted hosts : not configured (Laravel answers any Host)
verdict : all three answers are yes -> read the advisory conditions, then update and move the check into the action
not checked by this script: whether a second hostname reaches the same app (that is server config)
```

```text
app: lw-fixtures/app-b-4.4.9-domain-persistent
Q1 version : 4.4.9 -> patched (4.4.9 or later)
Q2 domain routes : 1 line(s)
   routes/web.php:3: Route::domain('{tenant}.example.test')->middleware('can:update,post')->group(function () {
Q3 persisted middleware : 1 custom line(s), 1 default-persisted route line(s)
   app/Providers/AppServiceProvider.php:4: Livewire::addPersistentMiddleware([\App\Http\Middleware\EnsureUserHasRole::class]);
   routes/web.php:3: Route::domain('{tenant}.example.test')->middleware('can:update,post')->group(function () {
info trusted hosts : not configured (Laravel answers any Host)
verdict : not in the affected range
not checked by this script: whether a second hostname reaches the same app (that is server config)
```

The third, a 4.4.8 app with a domain route and a `can:` rule but no `addPersistentMiddleware` call, is the one I changed the script for. My first version only counted `addPersistentMiddleware` and called that app "not every condition". The Livewire docs say `Authorize` is persisted by default, so a bare `can:update,post` counts. The fixed script reports it correctly:

```text
app: lw-fixtures/app-d-4.4.8-domain-only
Q1 version : 4.4.8 -> INSIDE the affected range (4.0.0 up to 4.4.8): update to 4.4.9 or later
Q2 domain routes : 1 line(s)
   routes/web.php:3: Route::domain('{tenant}.example.test')->middleware('can:update,post')->group(function () {
Q3 persisted middleware : 0 custom line(s), 1 default-persisted route line(s)
   routes/web.php:3: Route::domain('{tenant}.example.test')->middleware('can:update,post')->group(function () {
info trusted hosts : not configured (Laravel answers any Host)
verdict : all three answers are yes -> read the advisory conditions, then update and move the check into the action
not checked by this script: whether a second hostname reaches the same app (that is server config)
```

The fourth fixture, a 3.7.3 single-host app with `->middleware('auth')`, ends in "not in the affected range". Reading its output was the quickest sanity check of the lot.

![Four questions: composer.lock version, a domain route, route middleware for access, and whether a second host reaches the app. The script reads the first three; the fourth is checked by hand.](/img/livewire-update-skips-route-middleware-three-questions-2.png)

## The fix, in the order I would do it

**1. Update.** Composer constraints decide how far a plain `composer update` moves you, so say the target out loud:

```bash
composer require livewire/livewire:^3.8.12   # if you are on 3.x
composer require livewire/livewire:^4.4.9    # if you are on 4.x
```

Run your test suite and open the app before you ship it. This is a patch release on both lines, but it touches request handling, and the first thing I look at after any request-handling patch is the happy path.

**2. Tell people, or time it.** The release note says to refresh already-open pages. For an internal tool, a message in the team chat is enough. For a customer-facing app, deploy at a quiet hour and expect a few "my click did nothing" reports from people who had a tab open overnight.

**3. Put the permission check inside the action.** The advisory's own second workaround is to "perform authorization within sensitive component actions instead of relying solely on persistent route middleware". The Livewire security docs already recommend this for another reason: action parameters and public properties are input from the browser. Here is the shape from the docs, applied to the `UpdatePost` component from earlier:

```php
public function update(): void
{
    // Runs on every update request, whatever route or host it arrived on.
    $this->authorize('update', $this->post);

    $this->post->update([
        'title' => $this->title,
        'content' => $this->content,
    ]);
}
```

One line, in the one place that cannot be skipped. The route rule can stay. It is still the right place to keep strangers away from the page. It just stops being the only thing standing between a click and your database.

**4. Pin the test, so it stays true.** Livewire's testing docs have an authorization pattern. The version for this component is:

```php
use App\Livewire\UpdatePost;
use App\Models\Post;
use App\Models\User;
use Livewire\Livewire;

it('refuses to update a post the user cannot edit', function () {
    $user = User::factory()->create();
    $stranger = User::factory()->create();
    $post = Post::factory()->for($stranger)->create();

    Livewire::actingAs($user)
        ->test(UpdatePost::class, ['post' => $post])
        ->set('title', 'not mine')
        ->call('update')
        ->assertForbidden();
});
```

A test like this does not reproduce the advisory. Livewire's test harness fakes the request, and the code comment in Livewire itself says persistent middleware is skipped for fake requests such as tests. What it does is guarantee the check exists inside the action, which is exactly the protection that does not depend on which route or host the update used.

**5. Decide which hostnames your app should answer on.** This one is optional and it is my suggestion, not the advisory's. Laravel answers any `Host` header by default unless you enable trusted hosts. Laravel's docs show the switch in `bootstrap/app.php`:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^example\.com$'], subdomains: true);
})
```

That refuses hostnames you never meant to serve, such as a forgotten staging alias or a raw server name. It does not help if the "other host" is one of your legitimate tenant domains, so treat it as hygiene, not as the fix.

## Test after you bump: every hostname you serve

Because the patched code ties an update to the origin of the page, the first test I would run after the bump is boring on purpose: open one Livewire page on each hostname you serve, click a button that calls an action, and watch the network tab.

- A tenant subdomain, the main app domain, and your custom domains, if you have them.
- The `www` form and the bare domain, if one redirects to the other.
- Local and staging hostnames.
- Anything behind a proxy or a load balancer that rewrites the host or the scheme. The new check compares scheme plus host, so a page rendered as `https://...` and an update that arrives as `http://...` inside the app is a mismatch.

I have not run those cases against 3.8.12 or 4.4.9. They come from reading the new comparison, which is why they are on the list. If everything passes, you have also learned which hostnames actually reach your update endpoint, which is the fourth question the grep could not answer.

{{< field-note title="Field note" >}}
In a Laravel SaaS, where a rule lives matters more than whether it exists. A permission check on a route is easy to read and easy to review, so it feels like the rule. A permission check inside the method that writes to the database is harder to miss in review and cannot be skipped by a request that never touched the route. When I review a multi-tenant Laravel SaaS (the Modoo projects are the ones I know best), the first thing I ask is which layer is the last one standing before data changes. Framework glue (persisted middleware, route groups, tenant resolvers) is where the surprises tend to hide, because it works by remembering decisions across requests. A patch like this one is the right moment to move one check down a layer, whatever your answers to the three questions turn out to be.
{{< /field-note >}}

## What this does not say

- It does not say your app is exposed. It says that when three conditions hold, the route-level rule can be skipped. Plenty of apps have two of them.
- It does not say "critical". The vendor rates it Moderate, 6.8, and that is the label I use.
- It does not say anybody exploited this. The advisory does not mention exploitation and I found nothing that does.
- It does not say Livewire is unsafe. The security change sits in one source file, with tests, and the patched releases appeared minutes before the advisory on Nov 21.
- It does not say route-level middleware is wrong. It says it should not be the only layer on a path that changes data.

## What I did and did not verify

I did: read the advisory and the Livewire security docs with a fresh fetch on Nov 23; read both GitHub release bodies and confirmed the affected and patched ranges against the package list; read the source diff between `v3.8.11` and `v3.8.12` and the file at `v4.4.8` and `v4.4.9`; wrote the script and ran it on four fixtures, with the real output above.

I did not: run any PHP. This host has no PHP or Composer, so the PHP snippets above are copied from the Livewire and Laravel docs and adapted by hand, not executed. I did not install Livewire, did not build a two-host app, and did not reproduce the bypass. I did not check how many apps meet all three conditions, and I did not test how a default Forge or Octane setup answers on a second hostname. The advisory gives the conditions. I give you a way to check them in your repo.

## What you should do Monday morning

1. Run `grep -A3 '"name": "livewire/livewire"' composer.lock` in each Laravel app. Write down the version next to the app name.
2. Run the script above on each one that is inside the range. Read the three answers, then read the line about the second hostname and ask whoever owns DNS and the web server.
3. Update to 3.8.12 or 4.4.9 in a branch. Run your tests and open one Livewire page.
4. Open that page on every hostname you serve, click an action, and keep the network tab open. A 404 on an update is a finding, not a bug in this post.
5. Add `$this->authorize(...)` to every action that writes data, starting with the ones behind a domain route. Add one test per component that proves a stranger gets a 403.
6. Deploy at a quiet hour, and tell people with long-lived tabs to refresh.

![Monday morning in five steps: write down versions, run the check script, update in a branch, open every hostname, authorize inside the action.](/img/livewire-update-skips-route-middleware-three-questions-3.png)

## What this connects to

Same shape, different framework piece: [a Laravel signed link that outlives its expiry](/blog/laravel-signed-url-expiry-two-conditions/) was also "one version check, one grep". If you run Vue on the front end, [the Vue patch that touches Teleport and SSR variables](/blog/vue-patch-teleport-transition-ssr-retest/) uses the same method: list the files that use the feature, then test one. For a patch where the first question is "is this server even exposed", see [the PHP security release checklist](/blog/php-critical-release-tonight-four-checks/). The wider Laravel and Vue notes live on the [Laravel and Vue SaaS hub](/laravel-vue-saas/), and the [start here page](/start-here/) lists the rest.

## Further reading

- {{< source href="https://github.com/livewire/livewire/security/advisories/GHSA-vw9g-2c4c-g767" label="Livewire advisory: Changing the Host can bypass Livewire persistent middleware (GHSA-vw9g-2c4c-g767)" >}}
- {{< source href="https://github.com/livewire/livewire/releases/tag/v4.4.9" label="Livewire v4.4.9 release (and v3.8.12 for the 3.x line)" >}}
- {{< source href="https://livewire.laravel.com/docs/4.x/security" label="Livewire docs: Security (action parameters, persistent middleware)" >}}
- {{< source href="https://livewire.laravel.com/docs/4.x/testing" label="Livewire docs: Testing (authorization tests)" >}}
- {{< source href="https://laravel.com/framework/docs/requests" label="Laravel docs: HTTP requests, configuring trusted hosts" >}}
