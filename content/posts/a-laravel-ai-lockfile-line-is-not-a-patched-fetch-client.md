---
title: "A Laravel/AI Lockfile Line Is Not a Patched Fetch Client"
date: 2026-10-02T07:00:00+07:00
draft: false
slug: "a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client"
description: "Seeing laravel/ai in composer.lock is not proof the chat fetch client is patched. Print the lockfile line, the fetch-client field, and the named Laravel owner before you file an all-patched ticket."
topics: ["devops"]
tags: ["laravel", "composer", "lockfile", "laravel-ai", "advisory", "change-control"]
cover: /covers/a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client.png
seo:
  primaryQuery: "laravel/ai lockfile is not a patched fetch client"
  secondaryQueries:
    - "composer.lock laravel/ai fetch client advisory"
    - "laravel/ai vs laravel/mcp security advisory"
    - "named owner for laravel/ai lockfile"
---

The junior pastes `composer.lock`. The file contains `laravel/ai`. Dependabot is green. The ticket says “AI package is patched.”

I stop the run there. A laravel/ai lockfile line is not a patched fetch client. The public advisory that named this field is blunt: the Vercel adapter and the AG-UI adapter in laravel/ai 1.0.0 accepted a client-supplied file URL and fetched it on the server without a guard. That is one package, one pair of adapters, one fetch client. It is not laravel/mcp. It is not framework 13.34. It is not “Composer found a line, so the chat endpoint is safe.” [Source: https://github.com/laravel/ai/security/advisories/GHSA-6qhr-3g93-pxhw] [Source: https://laravel-news.com/laravel-ai-mcp-security-advisories]

I already refused to treat a 2,500+ Actions count as an exact run inventory in [A 2,500+ Actions Count Is Not an Exact Run Inventory](/blog/a-2500-plus-actions-count-is-not-an-exact-run-inventory/). I already refused to treat a NUL byte in a permission rule as a wildcard allow in [A NUL Byte in a Permission Rule Is Not a Wildcard Allow](/blog/a-nul-byte-in-a-permission-rule-is-not-a-wildcard/). I already refused to treat Copilot’s ready-to-approve line as a required merge vote in [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/). This post is the same desk rule for a Composer lock line. Print the package. Print the locked version. Name who owns the Laravel answers.

The question is not whether the lockfile looks patched. The question is whether the named owner can tell this fetch client from a different advisory and from a framework bump.

<!--more-->

![Three columns: lockfile line, patched fetch client, named Laravel owner](/img/a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client-1.png)

## The ticket that looks like all-patched

Juniors treat a lockfile the way they treat a green CI badge. The name is in the file. The bot did not scream. They page the desk: “laravel/ai is in the lockfile, we are patched.”

Two jobs collide on that line.

1. **Keep Composer honest.** `composer.lock` records the exact package and version this deploy installs. That is inventory. [Source: https://packagist.org/packages/laravel/ai]
2. **Keep the fetch client honest.** The advisory that shipped on 30 September 2026 names a fetch of client-supplied file URLs inside two adapters. A lockfile line does not print those adapters. [Source: https://github.com/laravel/ai/security/advisories/GHSA-6qhr-3g93-pxhw]

If you only screenshot “laravel/ai is present,” you will file all-patched. You will not file the fetch client.

{{< note type="warning" title="Do not file all-patched on a lockfile name" >}}
If a coding agent or a junior says the AI package is patched, print the exact `composer.lock` package name, the locked version, whether this app exposes the Vercel or AG-UI adapter to untrusted clients, and one human name on the Laravel answers before you page the desk. A name in a lockfile is not a patched fetch client.
{{< /note >}}

I do not invent a fake overnight policy flip. I use the public contract. The fetch-client field is the ticket, not a version pin in the title.

## What the lockfile line actually is

Composer’s lockfile is a list of packages this install resolved. Packagist currently lists laravel/ai with latest `v1.0.1` (29 September 2026, 18:50 UTC) and still lists `v1.0.0` (23 September 2026). A lockfile that contains the name `laravel/ai` tells you the package is a dependency. It does not tell you which of those two lines you ship. [Source: https://packagist.org/packages/laravel/ai]

The GitHub release that moved the fetch client is `v1.0.1`. The notes name “Improve remote file fetching” as pull request 1082. That sentence is evidence after you print the lockfile. It is not a heading. [Source: https://github.com/laravel/ai/releases/tag/v1.0.1]

The repo advisory is more specific than the release list:

- Package: laravel/ai (Composer).
- Affected: `>= 1.0.0, < 1.0.1`.
- Patched: 1.0.1.
- Severity: Moderate. Laravel News restates CVSS 5.3. No CVE ID in the public notes.
- Adapters: `Laravel\Ai\Vercel\Vercel` and `Laravel\Ai\AgentUserInteraction\AgentUserInteraction`.
- Field: file parts with a URL from the client, fetched on the server without a guard.
- Scope: only apps that expose one of those adapters to untrusted clients.
- 0.x: both adapters first shipped in 1.0.0. No 0.x release contains them. [Source: https://github.com/laravel/ai/security/advisories/GHSA-6qhr-3g93-pxhw] [Source: https://laravel-news.com/laravel-ai-mcp-security-advisories]

A lockfile line of `laravel/ai` at 0.11.2 is a different field. That line is not this fetch client. Do not file 1.0.0-only work as a 0.x emergency.

A lockfile line of `laravel/framework` at 13.34.0 is a different field again. Framework weekly is not this advisory. Do not merge them. [Source: https://laravel-news.com/laravel-ai-mcp-security-advisories]

{{< details summary="Where the public notes sit (not the title)" >}}
The fetch-client sentence lives in the laravel/ai repo advisory GHSA-6qhr-3g93-pxhw (published 30 September 2026) and in the v1.0.1 release notes that name pull request 1082. Packagist latest on the morning of this post is v1.0.1. GitHub’s global `/advisories/GHSA-6qhr-3g93-pxhw` URL 404s; the live page is the repo advisory. Later npm-style scanners that wait for a CVE will miss this line. Compare the locked version after you name the owner. Do not put a version in the heading. [Source: https://github.com/laravel/ai/security/advisories/GHSA-6qhr-3g93-pxhw] [Source: https://github.com/laravel/ai/releases/tag/v1.0.1] [Source: https://packagist.org/packages/laravel/ai]
{{< /details >}}

## Two advisories, two owners

The same week Laravel published a second advisory: laravel/mcp, GHSA-mx2h-h55v-pm44, insecure OAuth redirect. Severity Low. Needs user interaction. Fixed in 0.9.6 or 1.0.1. That is a redirect field, not a fetch client. [Source: https://github.com/laravel/mcp/security/advisories/GHSA-mx2h-h55v-pm44] [Source: https://x.com/pushpak1300/status/2105336372471234860]

A junior who sees both packages in one `composer update laravel/ai laravel/mcp` paste will screenshot “both AI packages are patched.” Print two tickets:

| Ticket | Package | Field | Untrusted-client question |
| --- | --- | --- | --- |
| Fetch client | laravel/ai | Client file URL fetched on the server by Vercel or AG-UI adapters | Does this app expose those adapters to callers you do not trust? |
| OAuth redirect | laravel/mcp | Redirect URL validation in the OAuth flow | Does this app run MCP OAuth, and did a human follow a crafted link? |

Same Composer command. Two fields. Two named owners if the teams split. One human is enough if one person owns Laravel on this desk. Do not let a coding agent collapse them into “AI is patched.”

Pushpak’s public note is the same split: laravel/ai 1.0.0 fetch of client-supplied file URLs in Vercel + AG-UI adapters, fix 1.0.1; laravel/mcp insecure OAuth redirect, fix 0.9.6 or 1.0.1. Do not wait for a CVE. Do not treat a missing CVE as a missing advisory. [Source: https://x.com/pushpak1300/status/2105336372471234860]

![Two fields: laravel/ai fetch client versus laravel/mcp OAuth redirect](/img/a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client-2.png)

## Probe: print the package, not the framework

Copy this probe. Run it against the lockfile the deploy actually uses. Do not run it against a gist. Do not turn it into a live fetch of an internal URL. This script only reads JSON.

```python {linenos=inline,hl_lines=[12,"24-28"]}
#!/usr/bin/env python3
"""Print laravel/ai and laravel/mcp from composer.lock. Inventory only."""
from __future__ import annotations

import json
import sys
from pathlib import Path

WANTED = ("laravel/ai", "laravel/mcp")


def packages(lock: Path) -> dict[str, str]:
    data = json.loads(lock.read_text())
    found: dict[str, str] = {}
    for row in data.get("packages", []) + data.get("packages-dev", []):
        name = row.get("name")
        if name in WANTED:
            found[name] = str(row.get("version"))
    return found


def main() -> int:
    lock = Path(sys.argv[1] if len(sys.argv) > 1 else "composer.lock")
    if not lock.is_file():
        print(f"missing lockfile: {lock}")
        return 2
    found = packages(lock)
    print(f"lockfile={lock.resolve()}")
    for name in WANTED:
        version = found.get(name, "ABSENT")
        print(f"{name} locked={version}")
    ai = found.get("laravel/ai")
    if ai in {"1.0.0", "v1.0.0"}:
        print("fetch_client_field=THIS_PACKAGE_AT_AFFECTED_LINE")
    elif ai in {"1.0.1", "v1.0.1"}:
        print("fetch_client_field=THIS_PACKAGE_AT_PATCH_LINE")
    elif ai is None:
        print("fetch_client_field=PACKAGE_NOT_LOCKED")
    else:
        print("fetch_client_field=OTHER_LINE_PRINT_ADAPTERS")
    print("owner_required=LARAVEL_AI_LOCKFILE_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Save it as `probe_laravel_ai_lockfile.py`. Point it at the lockfile on the branch that ships.

PHP on the same desk, if you refuse a Python helper in a Laravel repo:

```php
<?php
// Inventory only. Reads composer.lock. Does not fetch URLs.
$lockFile = $argv[1] ?? 'composer.lock';
$raw = file_get_contents($lockFile);
if ($raw === false) {
    fwrite(STDERR, "missing lockfile: {$lockFile}\n");
    exit(2);
}
$data = json_decode($raw, true);
$wanted = ['laravel/ai' => 'ABSENT', 'laravel/mcp' => 'ABSENT'];
foreach (array_merge($data['packages'] ?? [], $data['packages-dev'] ?? []) as $row) {
    $name = $row['name'] ?? '';
    if (array_key_exists($name, $wanted)) {
        $wanted[$name] = (string) ($row['version'] ?? '');
    }
}
echo "lockfile={$lockFile}\n";
foreach ($wanted as $name => $version) {
    echo "{$name} locked={$version}\n";
}
```

Composer itself, from the app root, after you already trust the lockfile path:

```bash
composer show laravel/ai --locked --format=json
composer show laravel/mcp --locked --format=json
```

Those three blocks print inventory. They do not open a chat endpoint. They do not fetch a file URL. They do not demonstrate the old adapter. The public advisory already states the old fetch. You do not need a live poison request. [Source: https://github.com/laravel/ai/security/advisories/GHSA-6qhr-3g93-pxhw]

If `composer show` says the package is not locked, the ticket is “this app does not install laravel/ai,” not “the fetch client is patched.” Absence is a field. Do not upgrade a package you do not ship because a social post named it.

![Probe checklist: lockfile path, locked package, adapter exposure, named owner](/img/a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client-3.png)

## Who is affected (adapters, not every Laravel app)

The advisory is explicit: only applications that expose one of the two adapters to untrusted clients are affected. Both adapters first shipped in 1.0.0. [Source: https://github.com/laravel/ai/security/advisories/GHSA-6qhr-3g93-pxhw]

That sentence kills three lazy tickets.

1. **Every Laravel 13 app is on fire.** False. Framework 13.34 is a weekly. This field is laravel/ai adapters. Print the package.
2. **Every laravel/ai install is on fire.** False if the locked line is 0.x, or if the app never exposes Vercel or AG-UI chat to untrusted callers. Print the adapters.
3. **Packagist latest means this deploy is patched.** False. Packagist latest is the registry. The deploy is the lockfile. Print the lockfile.

Laravel News restates the same boundary: you are only affected if the app exposes one of these adapters to untrusted clients. [Source: https://laravel-news.com/laravel-ai-mcp-security-advisories]

The v1.0 product post is useful background and a trap. Laravel shipped AI SDK v1.0 on 23 September 2026 with classification, frontend chat protocols, and storage changes. That post is not the advisory. Do not file an upgrade-guide ticket as this fetch client. [Source: https://laravel.com/blog/introducing-laravel-ai-sdk-v1]

On this desk the named owner answers four lines before any `composer update`:

1. Lockfile path (the file CI installs, not a laptop copy).
2. `laravel/ai` locked version.
3. Yes or no: this app exposes Vercel or AG-UI to callers we do not trust.
4. `LARAVEL_AI_LOCKFILE_OWNER` = a human name.

If line 3 is no, the ticket is “adapters not exposed.” Keep the lockfile current as change control. Do not pretend a private artisan command is a public chat endpoint.

If line 2 is the affected line and line 3 is yes, the ticket is “this fetch client.” The named owner schedules the patch as a normal Laravel change: lockfile, tests, rollback tag. The advisory’s own workaround is upgrade, or reject URL-based file parts before they reach the adapter, or block outbound traffic to internal and metadata addresses. I am not going to write a fetch recipe. Print those three options as owner choices. Do not paste an internal URL into a chat form to “prove” it. [Source: https://github.com/laravel/ai/security/advisories/GHSA-6qhr-3g93-pxhw]

## What still is not this ticket

Print these so a junior does not collapse every AI headline into this lockfile.

1. **laravel/mcp OAuth redirect.** Different GHSA. Different package. Different field. [Source: https://github.com/laravel/mcp/security/advisories/GHSA-mx2h-h55v-pm44]
2. **Framework weekly.** laravel/framework 13.34.0 is not this advisory.
3. **0.x laravel/ai.** Adapters not present. Do not file 1.0.0-only work on 0.11.2.
4. **A Dependabot green check.** A bot that waits for a CVE will miss a GHSA with no CVE. Pushpak said that out loud. [Source: https://x.com/pushpak1300/status/2105336372471234860]
5. **A 2,500+ Actions count.** Inventory of workflow runs is a different post. Do not clone it. [Source: https://zemna.net/blog/a-2500-plus-actions-count-is-not-an-exact-run-inventory/]
6. **Sandbox auto-allow.** An equals matcher on `python3 -c` is a different post. Do not merge. [Source: https://zemna.net/blog/sandbox-auto-allow-is-not-a-retry-tax-on-equals/]
7. **A moved runner deadline.** Actions runner images are a different post. Do not merge. [Source: https://zemna.net/blog/a-moved-runner-deadline-is-not-an-all-clear/]

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: `composer.lock` committed, `laravel/ai` pulled because a coding agent added a chat route last month, and a junior who pastes “AI package is patched” because the name is in the lockfile. I treat `LARAVEL_AI_LOCKFILE_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “which adapter does this route expose.” A coding agent does not get to run `composer update` on both laravel/ai and laravel/mcp, or to open a chat form against an internal URL, because a lockfile contains a name. I already wrote the sibling rule for a 2,500+ Actions count that is not an exact run inventory, and for Copilot’s ready-to-approve line that is not a merge vote. This is the sibling for a lockfile line that is not a patched fetch client.
{{< /field-note >}}

## What you must not do

Forbidden:

1. File an “AI package is patched” ticket without printing the lockfile path, `laravel/ai` locked version, adapter exposure yes/no, and one human name on the Laravel answers.
2. Put `1.0.1` or `13.34.0` in the title or the first line. The pin is evidence after the decision.
3. Mix this field with laravel/mcp OAuth, a framework weekly, a 2,500+ inventory ticket, a runner-deadline ticket, or a sandbox-equals ticket. Those are other posts.
4. Write a live chat request with a file URL to “demo” the old fetch. The public advisory already states the old fetch. You do not need a live poison request. [Source: https://github.com/laravel/ai/security/advisories/GHSA-6qhr-3g93-pxhw]
5. Treat Packagist latest as this deploy. The deploy is the lockfile.
6. Treat GitHub global advisory 404 as “no advisory.” The live page is the repo advisory.
7. Treat a missing CVE as a missing field. Laravel News and the maintainer both said scanners that wait for a CVE will miss this. [Source: https://laravel-news.com/laravel-ai-mcp-security-advisories]
8. Recommend buying a plan, a seat, or a scanner because one lockfile line is old.
9. Run `composer update` on laravel/mcp to close a laravel/ai fetch-client ticket, or the reverse.
10. Paste internal, metadata, or loopback URLs into a chat form. That is a fetch recipe. This post does not write one.
11. Clone the auto-start post, the green-deploy post, the /readyz post, the runner-deadline post, or the sandbox-equals post as a synonym. Those URLs already shipped. GSC this week has no striking-distance query that asks for another copy.
12. File “every Laravel app” or “every laravel/ai 0.x app” as this field. The advisory names 1.0.0 adapters and untrusted clients.

Allowed:

1. Print `laravel/ai` and `laravel/mcp` from the lockfile CI installs.
2. Classify the locked laravel/ai line with `probe_laravel_ai_lockfile.py`. Do not fetch a file URL as a demo.
3. Answer adapter exposure in one yes/no owned by a human.
4. Name one human as `LARAVEL_AI_LOCKFILE_OWNER`.
5. Print `composer show laravel/ai --locked` after the decision, in a details block, not in the title.
6. Schedule the patch as Laravel change control when the locked line is affected and adapters are exposed.
7. Keep 0.x and “adapters not exposed” as separate tickets, not as fake all-clears.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about remote file fetching is not permission to skip the four lines.

![A lockfile line is not a patched fetch client](/img/a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client-4.png)

## What you should do Monday morning

1. Open the repo that actually ships. Export `LARAVEL_AI_LOCKFILE_OWNER` to a human name. Run `probe_laravel_ai_lockfile.py` against the `composer.lock` CI installs. Write the locked `laravel/ai` line and the locked `laravel/mcp` line on the ticket next to that name.
2. Answer adapter exposure in one sentence: this app does or does not expose the Vercel or AG-UI adapter to callers we do not trust. If you cannot answer, the ticket is “owner missing,” not “patched.”
3. If laravel/ai is locked on the affected line and adapters are exposed, file “this fetch client,” not “AI is patched.” If the package is absent, file absent. If the line is 0.x, file 0.x. If adapters are not exposed, file that.
4. If someone pastes a single `composer update laravel/ai laravel/mcp` as the close of both fields, split the ticket. Print two packages. Close each field on its own evidence. [Source: https://github.com/laravel/mcp/security/advisories/GHSA-mx2h-h55v-pm44]
5. Print `composer show laravel/ai --locked`. If the laptop lockfile is not the CI lockfile, do not treat the laptop as production. Compare, then decide an upgrade as change control, not as a social post. [Source: https://github.com/laravel/ai/releases/tag/v1.0.1] [Source: https://packagist.org/packages/laravel/ai]
6. Confirm coding-agent instructions on this desk name the same owner and forbid “AI package is patched” without the four lines. Forbid any live fetch of a file URL as a demo.

The question is not whether the advisory demos well in a gist. The question is whether the named owner can still tell a lockfile line from a patched fetch client after handoff.

## Further reading

{{< source href="https://github.com/laravel/ai/security/advisories/GHSA-6qhr-3g93-pxhw" label="GitHub — laravel/ai advisory on client-supplied file URLs" >}}

{{< source href="https://github.com/laravel/ai/releases/tag/v1.0.1" label="GitHub — laravel/ai v1.0.1 release notes" >}}

{{< source href="https://laravel-news.com/laravel-ai-mcp-security-advisories" label="Laravel News — AI SDK and MCP security advisories" >}}
