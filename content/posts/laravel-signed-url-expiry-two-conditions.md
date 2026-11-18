---
title: "A Laravel Signed Link Can Outlive Its Expiry Under Two Conditions: One Version Check, One Grep"
date: 2026-11-14T06:00:00+07:00
lastmod: 2026-11-18T08:00:00+07:00
draft: false
slug: "laravel-signed-url-expiry-two-conditions"
description: "Two Laravel advisories from Nov 11 say a temporary signed URL can be accepted after it expired, but only under two specific conditions. Updated Nov 18: what Laravel 12.73.0 adds past the advisory floor, plus the version check and the grep."
topics: ["laravel"]
tags: ["laravel", "signed-urls", "security-advisory", "composer", "php", "patch-management", "code-review"]
cover: /covers/laravel-signed-url-expiry-two-conditions.png
seo:
  primaryQuery: "laravel signed url expiry bypass"
  secondaryQueries:
    - "laravel temporarySignedRoute expired link still works"
    - "laravel 12.73.0 signed url array expires"
    - "check laravel framework version composer.lock"
---

Somewhere in your Laravel app there is a link that promises to work for 24 hours. A download link, an unsubscribe link, a "confirm this change" link in an email. When the 24 hours pass, the link is supposed to answer with a 403 and nothing else.

On Nov 11, 2026 the Laravel team published two advisories that say this promise can break. Both are rated Moderate. Both say the same thing in different words: under a specific condition, an expired temporary signed URL may be accepted anyway.

The word "specific" matters more than the word "Moderate". So the useful question for your team is not "are we on a bad Laravel?" It is "do we have either condition, and who owns the links?"

<!--more-->

The question is not whether the advisory sounds technical. It is whether you can list every place your app builds a link that is supposed to expire, and say who reads it.

{{< note type="note" title="Updated on 2026-11-18" >}}
Written on Nov 14. New today: the next section, and a rewritten section near the end about the 12.x query-string regression, which now has a release. The floor script and its output are also updated. Everything else is the original check, and it still holds. The two advisories did not change.
{{< /note >}}

## Update, Nov 18: 12.73.0 goes one step past the advisory floor

On Tuesday, Nov 17, Laravel released 12.73.0 and 13.43.0 (Packagist lists them at 14:54 and 14:58 UTC). I re-read the two advisory pages this morning, Nov 18, at about 08:00 Jakarta time. Nothing moved: both still say Moderate, still say "No known CVE", and still name 12.72.0 and 13.41.0 as the patched versions. The newest entry on the repository's advisory list is still the one from Nov 11.

So the floor in the rest of this post is still correct. What changed is that there is now something newer than the floor, and it touches the same part of the code.

**What 12.73.0 adds for signed links.** Its release notes list pull request #62411, "Prevent array `expires` parameters from bypassing signed URL expiration". The pull request text says that when the `expires` value of a signed URL is an array, the expiry check treats the URL as never expiring: a non-empty array counts as true, and comparing the current time with an array is always false. It also says the signature still has to match. Then it gives the reason the guard exists: #62401, the fix that is already in 12.72.0, "showed that a signed URL can be made to carry an unexpected `expires` value, so the expiry check should not rely on that never happening."

That is a second lock on the same door. It is not a new hole announced by the Laravel team. I found no advisory and no CVE for it, and I am not going to call it more than the pull request calls it.

**What this means for 13.x.** The same pull request says it "backports the `expires` guard" from #59860 on 13.x. #59860, "Prevent array query params from bypassing signed URL validation", was merged into 13.x on Apr 27, 2026. I did not check which 13.x release first shipped it, so I make no claim for 13.x beyond the advisory floor, 13.41.0. The 13.43.0 notes list #62411 too. I did not test any of this.

| Release | Date (UTC) | What it adds for signed links |
|---|---|---|
| 12.72.0 | Nov 10 | The advisory fixes: raw query string fallback for `expires`, and the numeric-key fix |
| 12.73.0 | Nov 17 | Array `expires` guard (#62411), and the `EncodedParameter` fix (#62417, covered below) |
| 13.41.0 | Nov 10 | The advisory floor for 13.x |
| 13.43.0 | Nov 17 | Newest 13.x on Nov 18; its notes list the same two pull requests |

**What else is in 12.73.0.** The same release lists other changes whose titles sound security-related: "Fix XSS in debug page's 'copy request URL'" (#62418), "Fix XSS in component attributes" (#62503), "Fix Eloquent mass-assignment guard bypass via mutator attribute-name normalization mismatch" (#62499), "Prevent DoS in `Illuminate\JsonSchema\Deserializer` by bounding `$ref` chain depth" (#62498), and "Fix file validation bypass with empty input field collisions" (#62504). I read titles only. A title is not an impact statement, and I did not find an advisory for any of them. It also lists validation changes with titles like "Compare fluent database rule `where()` values literally" and "Keep every where on the same column in exists and unique rules". Those can change what your validation accepts.

So my advice is small: move to 12.73.0 or 13.43.0 or newer, but do it on a branch and run the tests that cover validation, redirects and signed links before you ship. If you want the old floor-only answer, it is in the script below: a lock at 12.72.0 or 13.41.0 is "ok", with a note that a newer release exists.

## Two advisories, one fix floor

I re-read both advisory pages on Nov 14 at about 08:00 Jakarta time. This is what they say, shortened:

| | First advisory | Second advisory |
|---|---|---|
| Title | Temporary signed URL expiration bypass | Temporary signed URL expiration bypass via unencoded numeric-keyed route parameters |
| ID | GHSA-v5ch-g375-82r6 | GHSA-6rv8-qj5v-p8ch |
| Published | Nov 11, 2026 | Nov 11, 2026 |
| Rating | Moderate, CVSS v3 4.8 | Moderate, CVSS v3 4.8 |
| CVE | "No known CVE" | "No known CVE" |
| Affected | below 12.72.0, and 13.0.0 up to below 13.41.0 | the same ranges |
| Patched | 12.72.0 and 13.41.0 | 12.72.0 and 13.41.0 |
| The condition | PHP's `max_input_vars` limit drops the `expires` value; the request line must be very long | Your code passes request-derived, numeric-keyed parameters into signed URL generation |

Both pages score "attack complexity" as High, which is the scoring system's way of saying the bug needs special circumstances.

That does not make it ignorable. It makes it a bug with conditions, and conditions are something a team can check in an afternoon.

## What a signed link is, in one minute

A signed URL is a normal link with two extra query values: `expires` and `signature`. The signature is a keyed hash of the rest of the link. If anyone changes the path or the query, the hash no longer matches and Laravel refuses the request.

The Laravel docs use an `unsubscribe` link as the example. They also state two facts that this post depends on: a signature "only covers the URL's path and query string", and when the `signed` middleware sees an invalid or expired signature, it returns a 403.

![A link split into path, expires and signature, with the signed middleware returning 403 for a bad or expired signature.](/img/laravel-signed-url-expiry-two-conditions-1.png)

The expiry rule is the part to hold on to. When Laravel validates a temporary signed route, the docs say it "will ensure that the expiration timestamp that is encoded into the signed URL has not elapsed". Both advisories are about ways that sentence stops being true.

## Condition 1: the expiry value goes missing before the check

PHP turns the query string into an array for you. It also has a safety limit, `max_input_vars`, which the PHP manual lists with a default of 1000. The manual says the limit applies to `$_GET`, `$_POST` and `$_COOKIE` separately, and that when there are more input variables than the limit, PHP issues a warning and truncates the rest.

The first advisory says that when this limit causes `expires` to be dropped from the parsed query, Laravel can still verify the signature against the raw query string. Then the expiry check finds no `expires` and treats the link as one that never expires. The advisory also says that exploiting this needs a request line long enough to go over the limit, and that this depends on server and proxy limits.

Notice the size. More than 1000 pairs in one URL is at least two thousand characters even with one-letter keys and no values, and in practice several thousand. A normal link from your app is nowhere near that.

The advisory's workaround is to limit URL length at the web server, and it adds that default nginx and Apache settings already reject the long URL the attack needs. I did not test that sentence. I did read the two directives it points at:

- nginx: `large_client_header_buffers` has the default `4 8k`, and a request line larger than one buffer gets a 414 error.
- Apache: `LimitRequestLine` has the default `8190` bytes.

Those are defaults. Your real limit is whatever your stack sets, and a CDN, a load balancer or a platform in front of PHP can have its own. Ask your infrastructure owner for the number.

The fix changes where Laravel reads `expires` from: the pull request title says it falls back to the raw query string. The 12.72.0 notes also list a change that lets Vapor apps read it from their own raw-query variable.

## Condition 2: your code hands a visitor's input to the link builder

The second advisory is about your code, not your server. It describes an app that passes "attacker-influenced, numeric-keyed parameters (for example a request's query array)" to `temporarySignedRoute()` or `signedRoute()`, where those parameters do not fill a route placeholder. Laravel then appended their values to the query string without URL encoding.

The page says the result is that someone can add a second `expires` field to the signed URL. The signature covers that field, but the request parsing reads it as the real value, so the link is treated as never expiring. I am not going to describe how to build the request. You do not need it to decide, and the page has the wording.

The sentence that decides it is the last one in the page's Impact section: exploitation requires the application to forward such input into signed URL generation. So the picture to look for in your code is simple. The third argument is something the visitor controlled.

```php
// The shape to look for: whatever the visitor sent becomes link parameters.
return URL::temporarySignedRoute(
    'invoices.download',
    now()->addHours(24),
    $request->query()
);
```

The advisory's own workaround for this one is to pass only explicitly selected, string-keyed parameters. That is also what the code was probably meant to do:

```php
// Pick the values you mean to put in the link, by name.
$format = in_array($request->query('format'), ['pdf', 'csv'], true)
    ? $request->query('format')
    : 'pdf';

return URL::temporarySignedRoute(
    'invoices.download',
    now()->addHours(24),
    ['invoice' => $invoice->id, 'format' => $format]
);
```

I did not run this PHP on this machine; it has no PHP. It is the pattern the advisory recommends, written out so a junior can copy the shape.

![Two panels. Left: PHP can drop expires from the parsed query when a URL has more than max_input_vars pairs. Right: your code passes a request's query array to the signed URL builders.](/img/laravel-signed-url-expiry-two-conditions-2.png)

## Check 1: which Laravel does each app run

A version in `composer.json` is a range. The version you actually run is in `composer.lock`. This script reads each lock file and compares `laravel/framework` with the two floors on the advisory pages. It only judges exact `x.y.z` versions, and it reports lines the advisory gives no fix for instead of guessing. Since Nov 18 it also prints a note when a lock sits at the floor but a newer release exists. That note does not change the exit code.

```python
#!/usr/bin/env python3
"""Compare laravel/framework in composer.lock files with the two Nov 11 advisories.

Usage: signed_floor.py PATH [PATH ...]    PATH = a composer.lock file or a folder
Exit 0 = every lock is at or past the listed fix.
Exit 1 = at least one lock is behind, or cannot be judged.
Exit 2 = no composer.lock found.

Floors come from the advisory pages (GHSA-v5ch-g375-82r6 and GHSA-6rv8-qj5v-p8ch):
12.x -> 12.72.0, 13.x -> 13.41.0. Other lines are reported, not guessed.
Updated Nov 18: a lock at the floor but below the newest release gets a note,
not a failure. The advisories did not change; the newer releases add hardening.
"""
import json
import re
import sys
from pathlib import Path

FLOORS = {12: (12, 72, 0), 13: (13, 41, 0)}
# Newest releases seen on Nov 18, 2026, with what the release notes list for them.
NEWER = {
    12: ((12, 73, 0), "adds an array-expires guard and the EncodedParameter fix"),
    13: ((13, 43, 0), "newest 13.x on Nov 18"),
}


def find_locks(args):
    for a in args:
        p = Path(a)
        if p.is_dir():
            yield from sorted(p.glob("**/composer.lock"))
        elif p.is_file():
            yield p


def framework_version(lock):
    data = json.loads(lock.read_text())
    for pkg in data.get("packages", []):
        if pkg.get("name") == "laravel/framework":
            return pkg.get("version", "")
    return None


def judge(text):
    m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", text.strip())
    if not m:
        return "CHECK", "not an exact x.y.z (dev branch?): read the lock by hand"
    v = tuple(int(x) for x in m.groups())
    floor = FLOORS.get(v[0])
    if floor is None:
        return "CHECK", f"line {v[0]}.x has no patched release on the advisory pages"
    want = ".".join(map(str, floor))
    if v < floor:
        return "BEHIND", f"move to {want} or newer"
    why = f"at or past {want}"
    newer, what = NEWER[v[0]]
    if v < newer:
        why += f"; {'.'.join(map(str, newer))} {what}"
    return "ok", why


def main(argv):
    locks = list(find_locks(argv))
    if not locks:
        print("no composer.lock found")
        return 2
    bad = 0
    for lock in locks:
        ver = framework_version(lock)
        if ver is None:
            print(f"SKIP   {lock}: no laravel/framework package")
            continue
        status, why = judge(ver)
        bad += status != "ok"
        print(f"{status:6} {ver:10} {lock}  {why}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

I ran it on a fixture folder with eight lock files, one per case (the two newest releases are new today):

```bash
$ python3 signed_floor.py fixture/locks; echo "exit=$?"
ok     v13.41.0   fixture/locks/admin-13/composer.lock  at or past 13.41.0; 13.43.0 newest 13.x on Nov 18
ok     v12.72.0   fixture/locks/api-12/composer.lock  at or past 12.72.0; 12.73.0 adds an array-expires guard and the EncodedParameter fix
CHECK  dev-master fixture/locks/dev-13/composer.lock  not an exact x.y.z (dev branch?): read the lock by hand
ok     v12.73.0   fixture/locks/fresh-12/composer.lock  at or past 12.72.0
ok     v13.43.0   fixture/locks/fresh-13/composer.lock  at or past 13.41.0
SKIP   fixture/locks/no-fw/composer.lock: no laravel/framework package
CHECK  v11.57.1   fixture/locks/old-11/composer.lock  line 11.x has no patched release on the advisory pages
BEHIND v12.71.0   fixture/locks/shop-12/composer.lock  move to 12.72.0 or newer
exit=1
```

About the `CHECK` row for 11.x: the advisory range literally says "below 12.72.0", which on its face includes older lines. But the pages list patched releases only for 12 and 13. The tag list I read shows 11.57.1 from Oct 27, which is before the advisories. I have no evidence either way about 11.x, so the honest output is "read the page yourself, and ask".

![A three-row table: 13.x moves to 13.41.0, 12.x moves to 12.72.0, 11.x and older has no fix listed.](/img/laravel-signed-url-expiry-two-conditions-3.png)

## Check 2: the one grep

A version check says what you run. It does not say whether you have condition 2. For that, find every call that builds a signed URL and look at the argument that carries the parameters. The scanner below reads PHP files only and prints one line per call. It skips `vendor`, `node_modules` and `storage`.

It sorts calls into four groups: `LOOK` when request input goes into the link, `TRACE` when the parameters are a variable built somewhere else, `LITERAL` when an explicit array is passed, and `NOARGS` when there are none.

```python
#!/usr/bin/env python3
"""List every call that builds a signed URL, and say which ones to read first.

Usage: signed_scan.py [APP_DIR]
Exit 0 = no calls found, or every call passes an explicit array.
Exit 1 = at least one call hands over request input or a variable to trace.
Exit 3 = bad path.

It reads PHP files only. It does not run anything. Exit 0 is not a clearance:
a literal array can still copy a visitor's value into a numeric key.
"""
import re
import sys
from pathlib import Path

SKIP = {"vendor", "node_modules", ".git", "storage", "bootstrap/cache"}
CALL = re.compile(r"(temporarySignedRoute|signedRoute)\s*\(")
REQUESTY = re.compile(r"\$request\b|\brequest\s*\(|Request::|->query\s*\(|->all\s*\(|->input\s*\(|\$_GET|\$_REQUEST")
# index of the "parameters" argument in each method signature
PARAM_INDEX = {"temporarySignedRoute": 2, "signedRoute": 1}


def call_text(src, start):
    """Return the text from the opening paren to its match, capped at 1500 chars."""
    depth, i = 0, start
    while i < len(src) and i - start < 1500:
        ch = src[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return src[start + 1:i]
        i += 1
    return src[start + 1:i]


def split_args(text):
    args, depth, cur = [], 0, []
    for ch in text:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        args.append(tail)
    return args


def classify(method, args):
    idx = PARAM_INDEX[method]
    if len(args) <= idx:
        return "NOARGS", "no parameters argument"
    param = args[idx]
    if REQUESTY.search(param):
        return "LOOK", "request input goes into the link: " + param[:60]
    if re.fullmatch(r"\$\w+", param):
        return "TRACE", f"{param} is built elsewhere: find where"
    return "LITERAL", "explicit parameters"


def main(argv):
    root = Path(argv[0] if argv else ".")
    if not root.exists():
        print(f"no such path: {root}")
        return 3
    hits = 0
    flagged = 0
    for path in sorted(root.glob("**/*.php")):
        if any(part in SKIP for part in path.parts):
            continue
        src = path.read_text(errors="replace")
        for m in CALL.finditer(src):
            line = src.count("\n", 0, m.start()) + 1
            args = split_args(call_text(src, m.end() - 1))
            kind, why = classify(m.group(1), args)
            hits += 1
            flagged += kind in ("LOOK", "TRACE")
            print(f"{kind:7} {path}:{line}  {m.group(1)}  {why}")
    if hits == 0:
        print("no signed URL calls found in app code")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

On a fixture controller with five calls, one per case (the fixture also holds a call under `vendor/`, which it skipped):

```bash
$ python3 signed_scan.py fixture/app; echo "exit=$?"
LOOK    fixture/app/app/Http/Controllers/InvoiceController.php:7  temporarySignedRoute  request input goes into the link: $request->query()
LITERAL fixture/app/app/Http/Controllers/InvoiceController.php:10  temporarySignedRoute  explicit parameters
LITERAL fixture/app/app/Http/Controllers/InvoiceController.php:17  signedRoute  explicit parameters
TRACE   fixture/app/app/Http/Controllers/InvoiceController.php:21  temporarySignedRoute  $params is built elsewhere: find where
NOARGS  fixture/app/app/Http/Controllers/InvoiceController.php:24  signedRoute  no parameters argument
exit=1
```

I also ran it on this site's own repository: `no signed URL calls found in app code`, exit 0. A missing path exits 3.

Two honest limits. It is a text scan, not a PHP parser, so a call written through a wrapper class you made will not show up. And a `LITERAL` row can still be wrong: `['id' => $id, ...$extra]` hides input behind a variable, and the scanner calls it `LITERAL`. Read each row; the output is a reading list, not a verdict.

## What to do about each row

Write down, for every call, three things: what the link opens, how long it should live, and who owns it. An unsubscribe page and a private invoice are not the same risk, even if the code is the same.

Then decide by row:

1. **`LOOK`:** change it first. Pick the values you mean to put in the link, by name, as in the second PHP block above. This does not depend on any upgrade.
2. **`TRACE`:** find where the variable is built. If it comes from a request, treat it as `LOOK`.
3. **`LITERAL` and `NOARGS`:** these usually do not match the second advisory's condition as it is written, unless a variable hides request input inside the array. They still need the upgrade for the first one.
4. **Every app:** move to the fixed version. The advisories name 12.72.0 and 13.41.0, and as of Nov 18 12.73.0 and 13.43.0 are newer. Anything newer on the same line also counts.

## One thing to read before you upgrade 12.x

The 12.72.0 release includes the fix for condition 2, which makes Laravel URL-encode numeric-keyed query values. The next day, someone opened issue #62416 titled "v12.72.0 breaks query strings, again". The report is narrow: code that returns `redirect()->route('search', new EncodedParameter('q=000001'))` started producing `/search?q%3D000001` instead of `/search?q=000001`.

A pull request, #62417, "Fix EncodedParameter being encoded again in numeric query parameters", was merged into the 12.x branch on Nov 11, and the issue was closed as completed the same day. Its description says `EncodedParameter` values are meant to be used as they are, plain strings are still encoded, and callers who build an `EncodedParameter` are expected to be trusted code, not user input.

**Update, Nov 18:** this now has a release. The 12.73.0 notes list #62417, so on 12.x the answer to "which version avoids both problems" is 12.73.0 or newer, not 12.72.0. The 13.43.0 notes list the same pull request. I did not run either release against the `EncodedParameter` case, so I am not saying what 13.x did before.

What this means in practice: if you never construct an `EncodedParameter`, this is not about you. If you do, upgrade to 12.73.0 or newer on a branch and run the tests that check redirect and link output before you ship.

## A test that stays

The best check after an upgrade is a boring test that fails when an expired link works. Laravel's testing docs have `travel()` for moving the clock. Adjust the route name for your app:

```php
public function test_expired_download_link_is_rejected(): void
{
    $url = URL::temporarySignedRoute(
        'invoices.download',
        now()->addHours(24),
        ['invoice' => 1]
    );

    $this->get($url)->assertOk();   // still inside the 24 hours

    $this->travel(25)->hours();
    $this->get($url)->assertForbidden();
}
```

This test would not have caught condition 1, because it uses a short normal URL. It guards the basic promise of the link, so an upgrade or a middleware change never quietly breaks it. I did not run it here; there is no PHP on this machine.

{{< field-note title="Field note" >}}
On the Laravel and Vue projects I look after, and the Modoo SaaS projects are that shape, signed links are rarely "a feature". They are a few lines someone added for an unsubscribe page or an export download, years ago, and they are not on any list. The person who wrote the call is often not the person who sets the nginx limit or reads the lockfile. Each of them is reasonable alone. These advisories are a prompt to write the list down: where the links are, what they open, who owns them. The question is not whether the upgrade is one command. It is whether anyone owns the places where the command has to run.
{{< /field-note >}}

## What this does not say

- It does not say your app is exploitable. Both pages describe conditions, and I did not test either one.
- It does not give a CVE. Both pages say "No known CVE". If one appears later, quote the page, not this post.
- It does not say that default nginx or Apache settings make you safe. That is the advisory's sentence, I did not test it, and your stack may not use the defaults.
- It does not say anything about 11.x or older beyond "the pages list no fix there".
- It does not say what 13.x did about the `EncodedParameter` side effect before 13.43.0. The 13.43.0 notes list the fix; I did not run it.
- It does not say the Nov 17 array-`expires` guard fixes a vulnerability. The pull request calls it a guard that "should not rely on that never happening", and I found no advisory or CVE for it.
- It does not say anything about the other security-sounding titles in 12.73.0. I read titles only.

## What I did and did not verify

On Nov 14 at about 08:00 Jakarta time I read both advisory pages in full, the 12.72.0 release notes, the GitHub tags and releases pages for `laravel/framework`, pull requests #62349, #62401 and #62417, issue #62416, the Laravel 13.x docs on URL generation and on mocking time, `UrlGenerator.php` on the 13.x branch (for the argument order the scanner relies on), the PHP manual page for runtime configuration, and the nginx and Apache directive docs named above.

On Nov 18 at about 08:00 Jakarta time I re-read both advisory pages, the repository's advisory list, the 12.73.0 and 13.43.0 release notes in full, pull requests #62411 and #59860, issue #62416, and the Packagist version list for release times. I updated `signed_floor.py` and ran it again on eight fixture lock files, plus a missing path and an empty folder. I did not read the pull requests behind the other titles in 12.73.0, and I did not check which 13.x tag first carried #59860.

I ran both Python scripts on the inputs shown: the fixture folders, an empty folder, a missing path and this site's repository (that last run is from Nov 14; the scanner did not change). I did not run PHP, any exploit, or the fix. The Releases page lists v13.42.0 and v12.72.0 but no entry for v13.41.0, while the tags page shows a v13.41.0 tag; I did not check why. Re-read the advisories before you act: a later edit can add a CVE or move a floor.

## What you should do Monday morning

These fit in one sitting, whatever day you read this.

1. **Run `signed_floor.py` on every app's `composer.lock`.** Fix `BEHIND` rows first, then read the `CHECK` rows by hand.
2. **Run `signed_scan.py` on every app.** Read every `LOOK` and `TRACE` row. Put a name next to each link.
3. **Change `LOOK` rows today.** Pass named values only. This needs no upgrade.
4. **Upgrade to 12.73.0 or 13.43.0 or newer** on a branch, and run the validation, redirect and link tests before you ship. The advisory floors are 12.72.0 and 13.41.0; 12.73.0 also carries the `EncodedParameter` fix.
5. **Ask infrastructure for the real request-line limit** in front of PHP: nginx, Apache, CDN, load balancer. Write the number in the runbook.
6. **Add the expired-link test** for the one or two links that matter most.
7. **On 11.x or older, open a ticket** that says "advisory lists no fix for this line", with an owner and a date.

## What this connects to

Same habit as [a Vite dev server advisory](/blog/vite-dev-server-bug-check-host-flag/), [a Node patch day](/blog/node-patch-day-where-your-version-lives/) and [a model string with a deadline](/blog/claude-api-two-calls-stop-nov-30/): a list of places, a check against the fix, one name per row. [Two Agents, One Database](/blog/herd-workspaces-share-the-parent-database/) is another Laravel default that nobody wrote down. More notes are on [Laravel and Vue SaaS](/laravel-vue-saas/), [Developer Tools](/developer-tools/) and [AI Agent Operations](/ai-agent-operations/), and [Start Here](/start-here/) lists the reading order.

## Further reading

- {{< source href="https://github.com/laravel/framework/security/advisories/GHSA-v5ch-g375-82r6" label="Laravel advisory GHSA-v5ch-g375-82r6: Temporary signed URL expiration bypass" >}}
- {{< source href="https://github.com/laravel/framework/security/advisories/GHSA-6rv8-qj5v-p8ch" label="Laravel advisory GHSA-6rv8-qj5v-p8ch: via unencoded numeric-keyed route parameters" >}}
- {{< source href="https://laravel.com/docs/13.x/urls" label="Laravel docs: URL generation and signed URLs" >}}
- {{< source href="https://www.php.net/manual/en/info.configuration.php" label="PHP manual: runtime configuration, max_input_vars" >}}
- {{< source href="https://github.com/laravel/framework/issues/62416" label="Laravel issue #62416: v12.72.0 breaks query strings, again" >}}
- {{< source href="https://github.com/laravel/framework/releases/tag/v12.73.0" label="Laravel release v12.73.0 (Nov 17)" >}}
- {{< source href="https://github.com/laravel/framework/pull/62411" label="Laravel pull request #62411: array expires guard" >}}
