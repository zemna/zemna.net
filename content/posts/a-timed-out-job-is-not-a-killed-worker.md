---
title: "A Timed-Out Job Is Not a Killed Worker"
date: 2026-09-24T07:00:00+07:00
draft: false
slug: "a-timed-out-job-is-not-a-killed-worker"
description: "A job that hits its timeout is not a dead worker pool. Print the job timeout, the worker kill, and the named queue:work owner before you file an outage."
topics: ["devops"]
tags: ["laravel", "queues", "queue-workers", "timeouts", "coding-agents", "change-control"]
cover: /covers/a-timed-out-job-is-not-a-killed-worker.png
seo:
  primaryQuery: "Laravel job timeout is not a killed worker"
  secondaryQueries:
    - "queue:work timeout vs worker process kill"
    - "JobTimedOut vs supervisor pool outage"
    - "named owner for Laravel queue workers"
---

The junior pastes a Supervisor screenshot. One `queue:work` line vanished. The failed_jobs table is empty. Horizon still shows a running supervisor. They file a pool outage: “the workers are dead.”

I stop the run there. A timed-out job is not a killed worker. Official Laravel queue docs are blunt: the default timeout is 60 seconds, and if a job runs longer than that number, the worker processing that job exits with an error. A process manager on the server then starts another worker. That is one job hitting a clock, not a pool that died. [Source: https://laravel.com/docs/13.x/queues]

I already refused to treat one matching glob as a sandbox exemption for the rest of the line in [One Matching Glob Is Not a Sandbox Exemption for the Rest of the Line](/blog/one-matching-glob-is-not-a-whole-line-exemption/). I already refused to treat a hostname handed to a forward proxy as a missing host in [Handing the Hostname to the Forward Proxy Is Not a Missing Host](/blog/hostname-handed-to-proxy-is-not-a-missing-host/). I already refused to treat `ubuntu-latest` as a runner image I already tested in [Ubuntu-latest Is Not a Runner Image You Already Tested](/blog/ubuntu-latest-is-not-a-tested-runner-image/). This post is the same desk rule for queues. Print the timeout. Print the kill. Name who owns `queue:work`.

The question is not whether a long job demos on your laptop. The question is whether the named owner can tell a job clock from a worker death before paging the pool.

<!--more-->

![Three columns: job timeout, worker kill, named queue:work owner](/img/a-timed-out-job-is-not-a-killed-worker-1.png)

## The ticket that looks like a dead pool

Juniors treat a vanished `queue:work` process the way they treat a crashed PHP-FPM pool. The process is gone. The job is still on the queue or already reserved. They page infra.

Two jobs collide on that line.

1. **Stop a job that ran past its clock.** Laravel’s timeout exists so a frozen `handle()` does not sit forever. Official docs: the worker processing that job exits with an error. [Source: https://laravel.com/docs/13.x/queues]
2. **Keep the rest of the pool on the same supervisor.** One worker exiting is the designed path. A process manager starts another worker. That is not “all workers died.” [Source: https://laravel.com/docs/13.x/queues]

If you only screenshot “process missing,” you will file a pool outage. You will not file the clock.

{{< note type="warning" title="Do not file a pool outage on a job timeout" >}}
If a coding agent or a junior says the worker pool is dead, print the job timeout, the worker `--timeout`, the supervisor restart line, and one human name on `queue:work` before you page infra. A missing process is not a dead pool.
{{< /note >}}

I do not invent a fake overnight outage. I use the public contract. The timeout page is the ticket, not a version pin in the title.

## What the timeout field actually is

Official docs, Timeout section: you specify how long a queued job is allowed to run. Default is 60 seconds. If the job runs longer, the worker processing it exits with an error. Typically a process manager restarts that worker. [Source: https://laravel.com/docs/13.x/queues]

You set the clock in two places. Do not mix them.

1. **Worker flag.** `php artisan queue:work --timeout=30` sets the worker’s maximum seconds. [Source: https://laravel.com/docs/13.x/queues]
2. **Job attribute.** `#[Timeout(120)]` on the job class wins over the command line. [Source: https://laravel.com/docs/13.x/queues]

Copy the docs example as a probe, not as a bypass recipe.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\FailOnTimeout;
use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
#[FailOnTimeout]
class ProcessPodcast implements ShouldQueue
{
    public function handle(): void
    {
        // work that must finish inside 120 seconds
    }
}
```

[Source: https://laravel.com/docs/13.x/queues]

`FailOnTimeout` is a separate field. Official docs: by default a timed-out job consumes one attempt and is released back to the queue if retries remain. If you put `FailOnTimeout` on the class, the job is marked failed and is not retried, regardless of `tries`. [Source: https://laravel.com/docs/13.x/queues]

Three more sentences from the same page that belong on the ticket:

- The PCNTL PHP extension must be installed or you cannot specify job timeouts. [Source: https://laravel.com/docs/13.x/queues]
- A job’s timeout must be less than its `retry_after` value. Otherwise the job is re-attempted before it finished or timed out. Default Redis `retry_after` in the docs sample is 90 seconds. [Source: https://laravel.com/docs/13.x/queues]
- `--timeout` has no effect when `queue:work` is invoked with `--once`. [Source: https://laravel.com/docs/13.x/queues]
- IO that blocks in sockets or HTTP clients does not always respect PHP’s timeout. Guzzle needs its own connection and request timeouts. [Source: https://laravel.com/docs/13.x/queues]

That last line is why a junior files “the worker hung.” The PHP alarm fired. The HTTP client did not. The process still looks busy until the worker exits.

{{< details summary="Pins are evidence, not the hook" >}}
The opt-out of killing the worker on job timeout, and the reachable timed-out exit code, shipped in Laravel framework v13.33.0 on 22 September 2026. The GitHub release lists “[13.x] Ability to opt out of killing the worker on job timeout” as pull request 61591 and “[13.x] Make the worker timed out exit code reachable” as pull request 61622. Default still kills the worker. Do not put those numbers in the title. This post is the timeout field, not a patch table. [Source: https://github.com/laravel/framework/releases/tag/v13.33.0] [Source: https://github.com/laravel/framework/pull/61591] [Source: https://github.com/laravel/framework/pull/61622]
{{< /details >}}

![Default 60s clock, job Timeout attribute wins, FailOnTimeout is separate](/img/a-timed-out-job-is-not-a-killed-worker-2.png)

## Three columns on the ticket

I keep one table on the ticket.

| What you saw | What it is | What it is not |
| --- | --- | --- |
| Job ran past `Timeout` / `--timeout` | That job hit its clock | The pool is dead |
| Worker process gone after timeout | Designed worker exit, then supervisor restart | All workers died |
| `JobTimedOut` in logs | Timeout handler ran | A PHP fatal or an OOM |
| Empty `failed_jobs` after a timeout | Default: one attempt consumed, job released if retries remain | The job succeeded |
| Supervisor restarted one program | Process manager did its job | You need a new cluster |

The junior screenshot is the first row. They want the third column. Print the second column first.

Name the owner. I use `QUEUE_WORK_OWNER` the same way I use a migration owner. The person who owns `php artisan queue:work` on this desk also owns “did this job hit its clock, or did the worker die for another reason.” A coding agent does not get to file a pool outage because one process vanished.

```bash
php artisan queue:work redis --timeout=60
php artisan queue:work --queue=high,default
```

[Source: https://laravel.com/docs/13.x/queues]

If Horizon is in play, remember Horizon manages Redis queues. Official docs: if your failover list includes `database`, run a regular `php artisan queue:work database` process alongside Horizon. Mixing those two screenshots is a second ticket. [Source: https://laravel.com/docs/13.x/queues]

Do not heading-clone the ubuntu-latest post. That post is a moving CI label. This post is a queue clock.

## Opting out of the kill is not the default

Public pull request 61591, merged 15 September 2026 into `13.x`, says the quiet part out loud. Today, if a job times out, it takes the whole worker down with it. Infra has to ask why the process stopped. The framework re-bootstraps. Connections are grabbed again. The author wanted an opt-out. [Source: https://github.com/laravel/framework/pull/61591]

The flag they shipped:

```php
<?php

namespace App\Providers;

use Illuminate\Queue\Worker;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        // Evidence of the opt-out. Default remains true.
        // Do not flip this in production from a screenshot.
        // Worker::$killOnTimeout = false;
    }
}
```

[Source: https://github.com/laravel/framework/pull/61591]

Read the PR twice.

- `Worker::$killOnTimeout` defaults to **true**. Nothing changes unless you opt in. [Source: https://github.com/laravel/framework/pull/61591]
- With it off, the timeout path throws `TimeoutExceededException` rather than killing the worker. [Source: https://github.com/laravel/framework/pull/61591]
- One benefit: a timing-out job can tidy up, and can catch `TimeoutExceededException`. [Source: https://github.com/laravel/framework/pull/61591]
- The named risk: if `handle()` wraps work in a try/catch, that catch swallows the exception. That is why the flag is opt-in. [Source: https://github.com/laravel/framework/pull/61591]

This is not a recipe to keep a frozen job alive. This is a field: **kill on timeout is still the default.** If your screenshot is “the worker vanished,” you are looking at the default path, not a broken supervisor.

{{< note type="danger" title="Do not flip killOnTimeout from a ticket" >}}
A coding agent that pastes `Worker::$killOnTimeout = false` into `AppServiceProvider` because one job timed out is writing a bypass, not a fix. Print the clock first. Name the owner. Leave the default kill in place until that owner can state what a swallowed `TimeoutExceededException` does to the next job on the same process.
{{< /note >}}

I already wrote the sibling rule for a matching glob that is not a whole-line exemption. This is the sibling for a missing process that is not a dead pool.

![Default kill on timeout versus opt-in throw](/img/a-timed-out-job-is-not-a-killed-worker-3.png)

## An exit code you can actually read

Public pull request 61622, merged 17 September 2026, is the other half of the same desk. `Worker::$timedOutExitCode` existed from an earlier change and had no effect. `Worker::kill()` sends `SIGKILL` to itself, then calls `exit($status)`. `SIGKILL` is immediate. The `exit()` line never runs. A parent waiting on the worker sees a signal death, which carries no exit status. Measured in that PR on PHP 8.5.8 with ext-posix: the process reports `137` (`128+9`) and never prints the line before `exit()`. [Source: https://github.com/laravel/framework/pull/61622] [Source: https://github.com/laravel/framework/pull/60072]

That is why a junior files “OOM” or “PHP fatal.” The supervisor saw a signal death. It did not see a timeout code.

The PR is careful about why `SIGKILL` stays. `exit()` would run shutdown functions and destructors on a frozen, mid-timeout job. A destructor that hangs would hang the worker. A destructor that flushes or commits would now do work the kill existed to prevent. [Source: https://github.com/laravel/framework/pull/61622]

The change: `Worker::killUsing()` registers a callback before the `SIGKILL`. A worker can `pcntl_exec` and replace its process image. `execve` runs no shutdown functions and no destructors, so the kill semantics stay, while a real exit status reaches the parent. Off by default. If exec fails, it falls through to `posix_kill`. [Source: https://github.com/laravel/framework/pull/61622]

Laravel Cloud registers that callback and sets `Worker::$timedOutExitCode = 124` so a managed timeout is a restartable exit, not container exit 255 mixed with fatals and OOM. That is their supervisor contract, not a VPS default. [Source: https://github.com/laravel/framework/pull/61622]

`$killOnTimeout = false` short-circuits before `kill()`. Throwing keeps the worker alive only if PHP can reach a VM instruction boundary. A job wedged in a blocking call never gets there. An exec callback still dies, and only changes how the death is reported. [Source: https://github.com/laravel/framework/pull/61622]

Print that distinction on the ticket:

1. **Job timeout** — the clock.
2. **Worker kill** — default: process dies; opt-out: throw; Cloud path: reachable exit 124.
3. **Named owner** — who is allowed to change either flag.

Do not paste 124 into Supervisor because a blog mentioned Cloud. Signal death and timeout exit are different fields.

## Probe before you page the pool

I keep a probe in the app root the coding agent uses, not in a docs folder on a laptop. It does not dispatch jobs. It does not disable timeouts. It classifies the last supervisor event.

```python
#!/usr/bin/env python3
"""Classify a vanished queue:work line. Not a timeout bypass."""

from __future__ import annotations

import os
import re
from pathlib import Path


def main() -> int:
    owner = os.environ.get("QUEUE_WORK_OWNER", "").strip()
    log = Path(os.environ.get("SUPERVISOR_LOG", "storage/logs/worker.out.log"))
    job_timeout = os.environ.get("JOB_TIMEOUT", "60")
    worker_timeout = os.environ.get("WORKER_TIMEOUT", "60")
    text = log.read_text(encoding="utf-8", errors="replace") if log.exists() else ""

    print(f"QUEUE_WORK_OWNER={owner or 'MISSING'}")
    print(f"JOB_TIMEOUT={job_timeout}")
    print(f"WORKER_TIMEOUT={worker_timeout}")
    print(f"LOG={log}")

    if not owner:
        print("VERDICT=NO_OWNER")
        return 2

    timed_out = bool(re.search(r"JobTimedOut|has timed out", text))
    signal_kill = bool(re.search(r"\b(SIGKILL|signal 9|exit status 137)\b", text))
    exit_124 = bool(re.search(r"\b(exit status 124|exited with 124)\b", text))
    pool_down = bool(re.search(r"FATAL|gave up: .*queue:work", text, re.I))

    if pool_down and not timed_out:
        print("VERDICT=SUPERVISOR_GAVE_UP")
        return 1
    if timed_out and signal_kill:
        print("VERDICT=JOB_TIMEOUT_THEN_DEFAULT_KILL")
        return 0
    if timed_out and exit_124:
        print("VERDICT=JOB_TIMEOUT_REACHABLE_EXIT")
        return 0
    if timed_out:
        print("VERDICT=JOB_TIMEOUT_SEEN")
        return 0
    if signal_kill:
        print("VERDICT=SIGNAL_DEATH_NOT_YET_A_TIMEOUT")
        return 2
    print("VERDICT=INSUFFICIENT_LOG")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it in the app that actually ships.

```bash
export QUEUE_WORK_OWNER="shinjae"
export SUPERVISOR_LOG="storage/logs/worker.out.log"
export JOB_TIMEOUT="120"
export WORKER_TIMEOUT="60"
python3 scripts/probe_queue_timeout.py
php artisan --version
```

The script does not talk to Redis. It does not start Horizon. `VERDICT=JOB_TIMEOUT_THEN_DEFAULT_KILL` means you do not have a pool outage. Then open Supervisor. Copy the program name. Copy the last exit. Put those four lines on the ticket: owner, job timeout, worker timeout, verdict.

A second probe is the job class itself. Print `#[Timeout]`, `#[FailOnTimeout]`, `$timeout` if the class still uses the property, `--timeout` on the artisan line, and `retry_after` in `config/queue.php`. If the job clock is 120 and `retry_after` is 90, you are looking at the docs warning, not a dead pool. [Source: https://laravel.com/docs/13.x/queues]

![Probe checklist: owner, job clock, worker clock, last exit](/img/a-timed-out-job-is-not-a-killed-worker-4.png)

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: Horizon on Redis for the UI, a leftover `queue:work database` for a failover connection, and a coding agent that pastes “workers died” because Supervisor restarted one program after a 60-second clock. I treat `QUEUE_WORK_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “did this job hit its clock.” A coding agent does not get to restart the whole supervisor group because `ProcessPodcast` ran past 60 seconds while Guzzle had no request timeout. I already wrote the sibling rule for a present `AGENTS.md` that is not the brief, and for a matching glob that is not a whole-line exemption. This is the sibling for a timed-out job that is not a killed worker.
{{< /field-note >}}

## What you must not do

Forbidden:

1. File a “worker pool is dead” ticket without printing the job timeout, the worker `--timeout`, `retry_after`, the supervisor last exit, and one human name on `queue:work`.
2. Put a Laravel version in the title or the first line. The pin is evidence after the decision.
3. Mix this field with an `ubuntu-latest` runner label, a hostname-to-proxy DNS ticket, or a compound-glob sandbox ticket. Those are other posts.
4. Flip `Worker::$killOnTimeout = false` from a screenshot. Default still kills. The PR says a try/catch in `handle()` swallows `TimeoutExceededException`. [Source: https://github.com/laravel/framework/pull/61591]
5. Paste `Worker::$timedOutExitCode = 124` because Cloud uses 124. That number is their supervisor contract. Off by default. [Source: https://github.com/laravel/framework/pull/61622]
6. Raise `--timeout` until the long job “succeeds,” then call that a fix. Raise the clock only when the named owner can state why the work needs that many seconds, and keep timeout less than `retry_after`. [Source: https://laravel.com/docs/13.x/queues]
7. Dispatch a live job that `sleep()`s past the clock to “demo” the kill. Print logs. Do not freeze production.
8. Recommend buying Horizon, Cloud, a plan, or a seat because one worker exited on timeout.
9. Treat an empty `failed_jobs` table as success. Default timeout consumes an attempt and releases the job if retries remain. [Source: https://laravel.com/docs/13.x/queues]
10. Ignore Guzzle or socket timeouts because PHP’s alarm exists. Official docs: blocking IO does not always respect the job timeout. [Source: https://laravel.com/docs/13.x/queues]

Allowed:

1. Print `#[Timeout]`, `#[FailOnTimeout]`, `queue:work --timeout`, and `retry_after`.
2. Read Supervisor’s last exit for that one program, not the whole group.
3. Listen for `JobTimedOut` and write the seconds on the ticket. An earlier change put the timeout value on that event so you can tell a job clock from a worker `--timeout`. [Source: https://github.com/laravel/framework/pull/61060]
4. Keep `FailOnTimeout` on jobs that must not retry after a clock.
5. Name one human as `QUEUE_WORK_OWNER`.
6. Print `php artisan --version` after the decision, in a details block, not in the title.

GSC this week still has no striking-distance query on the compound-glob post, the hostname-to-proxy post, or the ubuntu-latest post. I am not refreshing those URLs. This is a new field, not a synonym of Wednesday’s glob or Saturday’s runner label.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about a worker kill is not permission to skip the clock.

## What you should do Monday morning

1. Open the repo that actually ships. Export `QUEUE_WORK_OWNER` to a human name. Run `probe_queue_timeout.py` against last week’s supervisor log. Write the verdict on the ticket next to that name.
2. Open the job class from the incident. Copy `#[Timeout]` or `$timeout`. Copy `#[FailOnTimeout]` if present. Copy the `queue:work` line from Supervisor, including `--timeout`. Copy `retry_after` from `config/queue.php`. If the job clock is not less than `retry_after`, file that mismatch, not a pool outage. [Source: https://laravel.com/docs/13.x/queues]
3. If the log shows `JobTimedOut` and Supervisor restarted one program, do not page the pool. File “that job hit its clock.” Decide whether the work is too slow, the clock is too low, or Guzzle has no request timeout.
4. If someone pasted `Worker::$killOnTimeout = false` in a review, reject it until the named owner can state what a swallowed `TimeoutExceededException` does to the next job on the same process. Default remains kill. [Source: https://github.com/laravel/framework/pull/61591]
5. Print `php artisan --version`. If the laptop is behind the 22 September 2026 framework release that named the opt-out and the reachable exit code, do not treat the local pin as those fields. Compare, then decide an upgrade as change control, not as a social post. [Source: https://github.com/laravel/framework/releases/tag/v13.33.0]
6. Confirm coding-agent instructions on this desk name the same owner and forbid “the worker pool is dead” without the four lines: owner, job timeout, worker timeout, supervisor last exit.

The question is not whether a timeout demos well in a gist. The question is whether the named owner can still tell a job clock from a worker death after handoff.

## Further reading

{{< source href="https://laravel.com/docs/13.x/queues" label="Laravel Docs — queues (timeout, FailOnTimeout, queue:work)" >}}

{{< source href="https://github.com/laravel/framework/pull/61591" label="GitHub — opt out of killing the worker on job timeout" >}}

{{< source href="https://github.com/laravel/framework/pull/61622" label="GitHub — make the worker timed-out exit code reachable" >}}
