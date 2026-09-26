---
title: "A /readyz 200 Through a Postgres Blip Is Not a Healthy Store"
date: 2026-09-26T07:00:00+07:00
draft: false
slug: "a-readyz-200-is-not-a-healthy-store"
description: "A green /readyz is not proof Postgres is healthy. Print the ready status, the store probe, and the named gateway owner before you file an all-clear."
topics: ["software-engineering"]
tags: ["claude-code", "postgres", "health-checks", "readyz", "coding-agents", "change-control"]
cover: /covers/a-readyz-200-is-not-a-healthy-store.png
seo:
  primaryQuery: "readyz 200 is not a healthy Postgres store"
  secondaryQueries:
    - "Claude apps gateway /readyz through Postgres failover"
    - "Laravel /up vs database health check"
    - "named owner for gateway readiness vs store probe"
---

The junior pastes a curl. `/readyz` returns 200. Chat is quiet. They file an all-clear: “Postgres is healthy.”

I stop the run there. A `/readyz` 200 through a Postgres blip is not a healthy store. The public Claude Code notes that named this field are blunt: the Claude apps gateway gained `store.readiness_grace_seconds` so `/readyz` can stay ready through a short Postgres outage such as a database failover. That is a ready bit that held. It is not a store that answered `SELECT 1`. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.282] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a NUL byte in a permission rule as a wildcard allow in [A NUL Byte in a Permission Rule Is Not a Wildcard Allow](/blog/a-nul-byte-in-a-permission-rule-is-not-a-wildcard/). I already refused to treat a timed-out job as a killed worker in [A Timed-Out Job Is Not a Killed Worker](/blog/a-timed-out-job-is-not-a-killed-worker/). I already refused to treat every-turn HTTP 400 as a dead gateway in [Every-Turn HTTP 400 on ANTHROPIC_BASE_URL Is Not a Dead Gateway](/blog/every-turn-http-400-is-not-a-dead-gateway/). This post is the same desk rule for a green ready check. Print ready. Print the store. Name who owns the gateway check.

The question is not whether curl looks green. The question is whether the named owner can still tell “ready to take traffic” from “the store answered.”

<!--more-->

![Three columns: ready 200, store probe, named owner](/img/a-readyz-200-is-not-a-healthy-store-1.png)

## The ticket that looks like all-clear

Juniors treat `/readyz` the way they treat a green LED on a rack. The path is the one Kubernetes taught them. The HTTP code is 200. They page nobody. They tell chat the database is fine.

Two jobs collide on that path.

1. **Keep the process in the pool.** Official Kubernetes docs: a readiness probe decides when a container is ready to accept traffic. A 200 on `/readyz` means ready, not “every dependency you care about just ran a query.” [Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/] [Source: https://kubernetes.io/docs/reference/using-api/health-checks/]
2. **Keep the store honest.** A gateway that stays ready through a short Postgres outage is doing the first job on purpose. The public Claude apps gateway note says `/readyz` can stay ready through a short Postgres outage such as a database failover. That sentence is the field. It is not a store health report. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.282] [Source: https://code.claude.com/docs/en/changelog]

If you only screenshot “200 OK,” you will file all-clear. You will not file the store.

{{< note type="warning" title="Do not file all-clear on a green /readyz" >}}
If a coding agent or a junior says Postgres is healthy because `/readyz` returned 200, print the ready status, a store probe that is not that path, and one human name on the gateway check before you close the ticket. A ready bit is not a store bit.
{{< /note >}}

I do not invent a fake overnight failover. I use the public contract. The ready field is the ticket, not a version pin in the title.

## What /readyz actually is

Kubernetes API health docs: the API server exposes `livez` and `readyz` (and a deprecated `healthz`). Machines that check those paths rely on the HTTP status code. A status code 200 indicates the API server is live or ready, depending on the called endpoint. `readyz` is for “ready to accept traffic.” If `/readyz` fails, traffic should be routed away. That is a pool decision. [Source: https://kubernetes.io/docs/reference/using-api/health-checks/]

Official probe docs split the jobs:

| Probe | Job | Failure means |
| --- | --- | --- |
| Liveness | Restart the container | The process is stuck |
| Readiness | Keep or drop traffic | The process is not ready to serve |
| Startup | Wait before the other two | The process is still booting |

[Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/]

Readiness and liveness do not depend on each other. A process can be live and not ready. A process can be ready on HTTP and still have a store that is mid-failover. The probe you wired is the probe you get.

Laravel’s built-in health route is the same split on a PHP desk. Official Laravel 12 deployment docs: the health check route is served at `/up` by default and returns a 200 HTTP response if the application has booted without exceptions. Otherwise it returns 500. You change the URI in `bootstrap/app.php`. When that route runs, Laravel dispatches `Illuminate\Foundation\Events\DiagnosingHealth`, and a listener can check database or cache and throw. The default `/up` without that listener is a boot check. It is not `SELECT 1`. [Source: https://laravel.com/docs/12.x/deployment]

Copy the docs example as a probe of the route, not as a hide-the-blip recipe.

```php
<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware): void {
        //
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        //
    })
    ->create();
```

[Source: https://laravel.com/docs/12.x/deployment]

That file names the boot path. It does not name a store probe. If the junior curls `/up` and files “Postgres is healthy,” they mixed the two jobs the same way they mix `/readyz` with the store.

{{< details summary="Pins are evidence, not the hook" >}}
The Claude apps gateway field shipped in Claude Code v2.1.282 on 24 September 2026 (`published_at` 2026-09-24T18:38:05Z, prerelease false). The GitHub release and the official changelog use the same sentence: added `store.readiness_grace_seconds` to the Claude apps gateway so `/readyz` can stay ready through a short Postgres outage such as a database failover. Do not put those numbers in the title. This post is the ready field versus the store field, not a patch table. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.282] [Source: https://code.claude.com/docs/en/changelog]
{{< /details >}}

![Ready path HTTP 200 is not the same ticket as a store SELECT 1](/img/a-readyz-200-is-not-a-healthy-store-2.png)

## Three columns on the ticket

I keep one table on the ticket.

| What you saw | What it is | What it is not |
| --- | --- | --- |
| `/readyz` HTTP 200 | Ready to take traffic, for the probe that is wired | Proof the store answered |
| Short Postgres outage while ready stays 200 | The public grace field on the Claude apps gateway | A healthy primary |
| Laravel `/up` 200 | The app booted without exceptions | `SELECT 1` on `pgsql` |
| `SELECT 1` on the named connection | A store probe | A ready probe |
| Empty chat while ready is green | Clients still have a path | The replica caught up |

The junior screenshot is the first row. They want the third column. Print the second column first.

Name the owner. I use `GATEWAY_READY_OWNER` the same way I use a migration owner. The person who owns the Claude apps gateway config on this desk also owns “did `/readyz` stay 200 while Postgres blipped.” A coding agent does not get to file all-clear because curl was green.

Do not heading-clone the HTTP 400 post. That post is a schema reject on a named base URL. This post is a ready bit that can hold through a store blip. Do not heading-clone the timed-out-job post. That post is one queue clock versus a worker kill. This post is one HTTP path versus one store path.

## Probe the two paths, do not write a grace recipe

I keep a probe in the repo the coding agent uses, not in a gist on a laptop. It does not set `store.readiness_grace_seconds`. It does not teach a hide-the-blip flag. It classifies two existing endpoints.

```python
#!/usr/bin/env python3
"""Classify ready HTTP vs store probe. Not a grace-seconds recipe."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def http_status(url: str, timeout: float = 2.0) -> int | None:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return int(resp.status)
    except urllib.error.HTTPError as exc:
        return int(exc.code)
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None


def store_select_1(dsn: str) -> str:
    # Optional. Empty DSN is a missing store probe, not a pass.
    if not dsn:
        return "MISSING_DSN"
    try:
        import psycopg

        with psycopg.connect(dsn, connect_timeout=2) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                row = cur.fetchone()
        return "OK" if row and row[0] == 1 else "BAD_ROW"
    except Exception as exc:  # noqa: BLE001 — probe must never raise into chat
        return type(exc).__name__


def main() -> int:
    owner = os.environ.get("GATEWAY_READY_OWNER", "").strip()
    ready_url = os.environ.get("READYZ_URL", "").strip()
    dsn = os.environ.get("STORE_DSN", "").strip()
    if not owner or not ready_url:
        print("NEED_OWNER_AND_READYZ_URL", file=sys.stderr)
        return 2
    ready = http_status(ready_url)
    store = store_select_1(dsn)
    if ready == 200 and store == "OK":
        verdict = "READY_AND_STORE"
    elif ready == 200 and store != "OK":
        verdict = "READY_200_IS_NOT_A_HEALTHY_STORE"
    elif ready != 200:
        verdict = "READY_NOT_200"
    else:
        verdict = "UNCLASSIFIED"
    payload = {
        "owner": owner,
        "ready_url": ready_url,
        "ready_status": ready,
        "store": store,
        "verdict": verdict,
    }
    Path("readyz-ticket.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload))
    return 0 if verdict == "READY_AND_STORE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it from the repo that actually ships.

```bash
export GATEWAY_READY_OWNER="shinjae"
export READYZ_URL="http://127.0.0.1:8080/readyz"
export STORE_DSN="${STORE_DSN:-}"
python3 scripts/probe_readyz_vs_store.py
python3 -c "import json,pathlib; print(json.loads(pathlib.Path('readyz-ticket.json').read_text())['verdict'])"
```

The script does not call the model. It does not edit gateway YAML. `VERDICT=READY_200_IS_NOT_A_HEALTHY_STORE` means you do not have an all-clear. You have a ready bit that held while the store probe did not. Then open the gateway ticket. Put those four lines on it: owner, ready URL, ready status, store result.

A second probe is Laravel’s own split. Official docs: `/up` returns 200 if the application has booted without exceptions. A listener on `DiagnosingHealth` is how you add a database check. Print both. Do not treat `/up` as the store. [Source: https://laravel.com/docs/12.x/deployment]

```php
<?php

namespace App\Listeners;

use Illuminate\Foundation\Events\DiagnosingHealth;
use Illuminate\Support\Facades\DB;
use RuntimeException;

class ProbeStoreOnHealth
{
    public function handle(DiagnosingHealth $event): void
    {
        $row = DB::connection('pgsql')->select('select 1 as ok');
        if ($row === [] || (int) $row[0]->ok !== 1) {
            throw new RuntimeException('store probe failed');
        }
    }
}
```

That listener is a store probe attached to the boot path. It is still not permission to hide a failover. If the named owner wants `/up` to stay 200 while Postgres fails over, that is a written decision on the ticket, with a name. It is not a coding-agent default.

{{< note type="danger" title="Do not ship a grace-seconds how-to" >}}
This post names `store.readiness_grace_seconds` once, as evidence that `/readyz` can stay ready through a short Postgres outage. It does not tell you which number to set. A number on that key is change control for the named gateway owner. A coding agent does not pick it in chat.
{{< /note >}}

![Four-line ticket: owner, ready URL, ready status, store result](/img/a-readyz-200-is-not-a-healthy-store-3.png)

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a load balancer hitting `/up`, a coding agent curling a gateway `/readyz`, and a junior filing “Postgres is healthy” because both paths were 200 during a replica promotion. I treat `GATEWAY_READY_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “did the store answer, or did only ready stay green.” A coding agent does not get to close a database ticket because curl was 200. I already wrote the sibling rule for a timed-out job that is not a killed worker, and for an HTTP 400 wall that is not a dead gateway. This is the sibling for a ready bit that is not a healthy store.
{{< /field-note >}}

## The load balancer is not the ticket

A load balancer reads three digits. Kubernetes probe docs treat HTTP 200–399 as success for that probe. The balancer then keeps the instance in the pool. That is the right machine job. [Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/]

A human ticket is a different job. The human names the store. The human names the owner. The human writes whether `SELECT 1` passed on the named connection while `/readyz` stayed 200. Mixing those jobs is how a failover becomes an all-clear in chat.

On this desk I keep the balancer on the ready path and the ticket on both paths. If the named owner later decides the balancer should also wait on the store, that is a written change to the probe, with a name, not a coding-agent edit in a gist.

## What you must not do

Forbidden:

1. File an “Postgres is healthy” ticket without printing the ready URL, the HTTP status, a store probe that is not that URL, and one human name on the gateway check.
2. Put a Claude Code version in the title or the first line. The pin is evidence after the decision.
3. Mix this field with an HTTP 400 schema ticket, a timed-out job ticket, or a NUL-in-rule ticket. Those are other posts.
4. Write a `store.readiness_grace_seconds` how-to, a recommended number, or a “set this during failover” runbook. The public notes already state that `/readyz` can stay ready through a short Postgres outage. You do not need a live hide-the-blip recipe. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.282]
5. Treat Laravel `/up` 200 as `SELECT 1`. Official docs: 200 means the application has booted without exceptions unless you added a listener that throws. [Source: https://laravel.com/docs/12.x/deployment]
6. Recommend buying a plan, a seat, or a managed gateway because one ready check stayed green.
7. Treat Kubernetes `/readyz` 200 as proof etcd or Postgres is independently healthy. Official docs: 200 means ready to accept traffic for that server’s wired checks. [Source: https://kubernetes.io/docs/reference/using-api/health-checks/]
8. Treat “ready stayed 200” as “the store never failed.” The public sentence is the opposite: ready can stay through a short outage.
9. Confuse liveness with readiness. Official probe docs: they do not depend on each other. Restarting a container is not the same job as dropping traffic. [Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/]
10. Paste a telemetry, permission-NUL, or queue-timeout fix because those families shipped this week. Those are different fields.

Allowed:

1. Print `/readyz` status from the URL the load balancer actually hits.
2. Print a store probe on the named connection. Empty DSN is `MISSING_DSN`, not a pass.
3. Keep Laravel `/up` as a boot path, and add a `DiagnosingHealth` listener only when the named owner wants the boot path to include the store. [Source: https://laravel.com/docs/12.x/deployment]
4. Name one human as `GATEWAY_READY_OWNER`.
5. Print `claude --version` after the decision, in a details block, not in the title.
6. File “ready held, store missed” as the ticket title when those two columns disagree.

GSC this week still has no striking-distance query on the HTTP 400 post, the timed-out-job post, or the NUL-in-rule post. I am not refreshing those URLs. This is a new field, not a synonym of Friday’s matcher bytes or Thursday’s queue clock.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about a ready grace window is not permission to skip the store.

## What you should do Monday morning

1. Open the repo that actually ships. Export `GATEWAY_READY_OWNER` to a human name. Run `probe_readyz_vs_store.py` against the `/readyz` URL the load balancer hits and, if it exists, the store DSN. Write the verdict on the ticket next to that name.
2. Open the Laravel app that sits in front of the same Postgres. Curl `/up`. If you have a `DiagnosingHealth` listener, say so on the ticket. If you do not, write “boot check only.” Do not write “database healthy.” [Source: https://laravel.com/docs/12.x/deployment]
3. If chat was quiet while `/readyz` stayed 200, file “ready held.” Decide whether the store probe passed, failed, or was missing. Official Kubernetes language: 200 on `/readyz` is ready to accept traffic. [Source: https://kubernetes.io/docs/reference/using-api/health-checks/]
4. If someone pastes only a green curl, reject the review until the named owner can show four lines: owner, ready URL, ready status, store result.
5. Print `claude --version`. If the laptop is behind the 24 September 2026 release that named the gateway ready field, do not treat the local pin as those fields. Compare, then decide an upgrade as change control, not as a social post. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.282] [Source: https://code.claude.com/docs/en/changelog]
6. Confirm coding-agent instructions on this desk name the same owner and forbid “Postgres is healthy” without the four lines: owner, ready URL, ready status, store probe.

The question is not whether a green curl demos well in a gist. The question is whether the named owner can still tell a ready bit from a store that answered after handoff.

## Further reading

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code Docs — changelog" >}}

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.282" label="GitHub — Claude Code v2.1.282 release notes" >}}

{{< source href="https://laravel.com/docs/12.x/deployment" label="Laravel 12.x docs — the health route" >}}
