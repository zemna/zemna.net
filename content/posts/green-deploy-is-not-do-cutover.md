---
title: "A Green Wrangler Deploy Is Not an Immediate Durable Object Code Cutover"
date: 2026-09-27T07:00:00+07:00
draft: false
slug: "green-deploy-is-not-do-cutover"
description: "A green wrangler deploy is not proof Durable Object code is live. Print the deploy, the code-update strategy, and the named Workers owner before you file an all-cutover."
topics: ["developer-tools"]
tags: ["wrangler", "durable-objects", "cloudflare-workers", "coding-agents", "change-control"]
cover: /covers/green-deploy-is-not-do-cutover.png
seo:
  primaryQuery: "wrangler Durable Objects code update strategy deferred"
  secondaryQueries:
    - "green wrangler deploy is not immediate Durable Object cutover"
    - "durable_objects.code_update_strategy default deferred"
    - "named owner for Workers Durable Object code update"
---

The junior pastes a terminal. `npx wrangler deploy` exits 0. Chat is quiet. They file an all-cutover: “Durable Object code is live.”

I stop the run there. A green wrangler deploy is not an immediate Durable Object code cutover. The public Workers SDK notes that named this field are blunt: Durable Objects now have code update strategies on `wrangler deploy`, `wrangler versions deploy`, and `wrangler rollback`. When the strategy is unset, it defaults to deferred with a 5-minute maximum delay. Delays cannot exceed 24 hours. That is a Worker bundle that uploaded. It is not every live object already running the new class. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.141.0] [Source: https://releasebot.io/updates/cloudflare/workers-sdk]

I already refused to treat a `/readyz` 200 through a Postgres blip as a healthy store in [A /readyz 200 Through a Postgres Blip Is Not a Healthy Store](/blog/a-readyz-200-is-not-a-healthy-store/). I already refused to treat a timed-out job as a killed worker in [A Timed-Out Job Is Not a Killed Worker](/blog/a-timed-out-job-is-not-a-killed-worker/). I already refused to treat every-turn HTTP 400 as a dead gateway in [Every-Turn HTTP 400 on ANTHROPIC_BASE_URL Is Not a Dead Gateway](/blog/every-turn-http-400-is-not-a-dead-gateway/). This post is the same desk rule for a green deploy. Print deploy. Print the strategy. Name who owns the Workers cutover.

The question is not whether the CLI looks green. The question is whether the named owner can still tell “Worker version uploaded” from “Durable Object instances left the old class.”

<!--more-->

![Three columns: green deploy, deferred DO code, named owner](/img/green-deploy-is-not-do-cutover-1.png)

## The ticket that looks like all-cutover

Juniors treat `wrangler deploy` the way they treat a green LED on a rack. The command returned. The dashboard shows a new version. They page nobody. They tell chat every Durable Object is on the new code.

Two jobs collide on that command.

1. **Upload the Worker.** Official Cloudflare docs: you deploy a Worker version with Wrangler. A successful deploy means the new Worker version exists. It does not mean every globally unique Durable Object already restarted onto that version. [Source: https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/]
2. **Move Durable Object code.** Official Durable Objects known-issues docs: only one version of each Durable Object can run at a time. Code changes for Workers and Durable Objects are released globally in an eventually consistent manner. A request can arrive at the latest Worker and still call a unique Durable Object running the previous class for a short period, typically seconds to minutes. [Source: https://developers.cloudflare.com/durable-objects/platform/known-issues/]

If you only screenshot “Uploaded” you will file all-cutover. You will not file the objects that are still awake on the old class.

{{< note type="warning" title="Do not file all-cutover on a green wrangler deploy" >}}
If a coding agent or a junior says Durable Object code is live because `wrangler deploy` exited 0, print the deploy result, the code-update strategy (or that it is unset), and one human name on the Workers cutover before you close the ticket. A green CLI is not an instance cutover.
{{< /note >}}

I do not invent a fake overnight outage. I use the public contract. The update-strategy field is the ticket, not a version pin in the title.

## What wrangler deploy actually is

Official gradual-deployment docs: you upload a version, then you create a deployment that may split traffic. `wrangler versions upload` creates a version that is not automatically deployed. `wrangler versions deploy` creates a deployment. `wrangler deploy` is the older one-shot path many desks still run in CI. All three are Worker version jobs. [Source: https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/]

Durable Objects sit on a different clock. Official known-issues page, under Global uniqueness: uniqueness is enforced when a new event starts and when storage is accessed. A Durable Object may be replaced on a software update, including an update of the Durable Object class code. Official Code updates section: because each Durable Object is globally unique, the latest Worker can call a previous-class object for seconds to minutes. Best practice is forward and backward compatible APIs across that window. [Source: https://developers.cloudflare.com/durable-objects/platform/known-issues/]

The 25 September 2026 Workers SDK release named the missing knob. GitHub tag `wrangler@4.141.0` (`published_at` 2026-09-25T19:33:53Z, prerelease false) adds Durable Objects code update strategies to Worker deployments. Use `--durable-objects-code-update-mode immediate` on `wrangler deploy`, `wrangler versions deploy`, and `wrangler rollback` to update code without waiting for active instances to hibernate. Use `--durable-objects-code-update-mode deferred 30s` to set a maximum delay, or configure `durable_objects.code_update_strategy` with `mode` and `max_delay`. When unset, the strategy defaults to deferred with a 5-minute maximum delay. Delays cannot exceed 24 hours and must use millisecond precision. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.141.0] [Source: https://releasebot.io/updates/cloudflare/workers-sdk]

That paragraph is evidence. It is not a how-to. This post does not tell you to pass `immediate`. This post tells you to print which mode you actually ran.

{{< details summary="Pins are evidence, not the hook" >}}
GitHub published `wrangler@4.141.0` on 25 September 2026. The npm tarball `wrangler@4.141.0` exists at https://registry.npmjs.org/wrangler/4.141.0. This morning’s `https://registry.npmjs.org/wrangler/latest` still answered `version: 4.140.0`. Print GitHub tag, npm tarball, and `dist-tags.latest` as three columns. Do not treat `npx wrangler@latest` as the GitHub tag. Do not put those numbers in the title. This post is the deploy field versus the Durable Object field, not a patch table. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.141.0] [Source: https://registry.npmjs.org/wrangler/latest] [Source: https://registry.npmjs.org/wrangler/4.141.0]
{{< /details >}}

![Worker version uploaded is not the same ticket as Durable Object still on the previous class](/img/green-deploy-is-not-do-cutover-2.png)

## Three columns on the ticket

I keep one table on the ticket.

| What you saw | What it is | What it is not |
| --- | --- | --- |
| `wrangler deploy` exit 0 | Worker version uploaded | Proof every Durable Object left the old class |
| Unset `code_update_strategy` | Public default: deferred, 5-minute maximum delay | Immediate cutover |
| `--durable-objects-code-update-mode deferred 30s` | A named maximum delay | Proof instances already restarted |
| `--durable-objects-code-update-mode immediate` | A named owner decision to skip the wait for hibernation | A coding-agent default |
| Latest Worker calling an old-class object | The documented seconds-to-minutes window | A broken binding |
| Gradual 20 / 80 split | Each object pinned to one version for that deployment | Permission to mix class APIs |

[Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.141.0] [Source: https://developers.cloudflare.com/durable-objects/platform/known-issues/] [Source: https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/with-durable-objects/]

The junior screenshot is the first row. They want the third column. Print the second column first.

Name the owner. I use `WORKERS_CUTOVER_OWNER` the same way I use a migration owner. The person who owns Wrangler on this desk also owns “did we deploy deferred, immediate, or unset.” A coding agent does not get to file all-cutover because the CLI was green.

Do not heading-clone the compound-glob post. That post is one matching glob versus the rest of the line. This post is one deploy versus one object clock. Do not heading-clone a wrangler-never-returns post. That post is a hung CLI. This post is a finished CLI that still left objects on a delay.

## Probe the two clocks, do not write a force-immediate recipe

I keep a probe in the repo the coding agent uses, not in a gist on a laptop. It does not pass `--durable-objects-code-update-mode immediate`. It does not edit `wrangler.jsonc` for you. It classifies the config that already exists.

```python
#!/usr/bin/env python3
"""Classify wrangler Durable Object code-update strategy. Do not flip the mode."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

OWNER = os.environ.get("WORKERS_CUTOVER_OWNER", "").strip()
CONFIG = Path(os.environ.get("WRANGLER_CONFIG", "wrangler.jsonc"))
OUT = Path("do-cutover-ticket.json")

DEFAULT_MODE = "deferred"
DEFAULT_MAX_DELAY = "5m"
MAX_ALLOWED = "24h"


def strip_jsonc(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    return text


def load_config(path: Path) -> dict:
    if not path.is_file():
        return {}
    raw = strip_jsonc(path.read_text(encoding="utf-8"))
    return json.loads(raw)


def classify(cfg: dict) -> dict:
    do = cfg.get("durable_objects") or {}
    strategy = do.get("code_update_strategy")
    if not isinstance(strategy, dict) or not strategy:
        return {
            "mode": DEFAULT_MODE,
            "max_delay": DEFAULT_MAX_DELAY,
            "source": "unset_default",
            "verdict": "GREEN_DEPLOY_IS_NOT_IMMEDIATE_DO_CUTOVER",
        }
    mode = str(strategy.get("mode") or DEFAULT_MODE)
    max_delay = str(strategy.get("max_delay") or DEFAULT_MAX_DELAY)
    if mode == "immediate":
        verdict = "IMMEDIATE_NAMED_ON_TICKET"
    else:
        verdict = "GREEN_DEPLOY_IS_NOT_IMMEDIATE_DO_CUTOVER"
    return {
        "mode": mode,
        "max_delay": max_delay,
        "source": "config",
        "verdict": verdict,
        "max_delay_cannot_exceed": MAX_ALLOWED,
    }


def main() -> int:
    if not OWNER:
        print("MISSING_WORKERS_CUTOVER_OWNER", file=sys.stderr)
        return 2
    result = classify(load_config(CONFIG))
    result["owner"] = OWNER
    result["config"] = str(CONFIG)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The script does not call Wrangler. It does not call the Cloudflare API. `VERDICT=GREEN_DEPLOY_IS_NOT_IMMEDIATE_DO_CUTOVER` means you do not have an all-cutover. You have a Worker upload whose Durable Object code still sits on the public deferred default, or on an explicit delay. Then open the Workers ticket. Put those four lines on it: owner, deploy result, mode, max delay.

A second probe is the config field the release named. Official release text: configure `durable_objects.code_update_strategy` with `mode` and `max_delay`. Copy the shape as evidence of the field, not as a hide-the-wait recipe.

```jsonc
{
  "name": "session-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-09-25",
  "durable_objects": {
    "bindings": [
      {
        "name": "SESSION",
        "class_name": "Session"
      }
    ],
    "code_update_strategy": {
      "mode": "deferred",
      "max_delay": "5m"
    }
  }
}
```

[Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.141.0]

That file names the delay. It does not name an instance that already restarted. If the junior pastes it and files “Durable Object code is live,” they mixed the two jobs the same way they mix `/readyz` with the store.

{{< note type="danger" title="Do not ship a force-immediate how-to" >}}
This post names `--durable-objects-code-update-mode immediate` once, as evidence that Wrangler can skip the wait for hibernation. It does not tell you to pass that flag. A flag on that key is change control for the named Workers owner. A coding agent does not pick it in chat.
{{< /note >}}

Print the ticket from the probe file. Empty owner is a fail, not a skip.

```bash
export WORKERS_CUTOVER_OWNER="${WORKERS_CUTOVER_OWNER:-}"
export WRANGLER_CONFIG="${WRANGLER_CONFIG:-wrangler.jsonc}"
python3 scripts/probe_do_cutover.py
python3 -c "import json,pathlib; print(json.loads(pathlib.Path('do-cutover-ticket.json').read_text())['verdict'])"
```

![Four-line ticket: owner, deploy result, mode, max delay](/img/green-deploy-is-not-do-cutover-3.png)

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a coding agent runs `npx wrangler deploy` for a session Durable Object, CI prints green, and a junior files “cutover done” while objects that were mid-request still sit on the previous class for the documented seconds-to-minutes window. I treat `WORKERS_CUTOVER_OWNER` the same way I treat a migration owner. The person who owns [/developer-tools/](/developer-tools/) on this desk also owns “did we upload a Worker, or did Durable Object instances leave the old class.” A coding agent does not get to close a Workers ticket because the CLI was 0. I already wrote the sibling rule for a ready bit that is not a healthy store, and for a timed-out job that is not a killed worker. This is the sibling for a green deploy that is not an immediate Durable Object cutover.
{{< /field-note >}}

## Gradual deployments are not this ticket either

Official docs: gradual deployments work differently for Durable Objects because only one version of each Durable Object can run at a time. When you create a new gradual deployment, each Durable Object is assigned a Worker version based on the percentages you configured. That version does not change until you create a new deployment. For a given deployment, requests to each Durable Object always use the same Worker version. The object is reset when it is assigned a different version. [Source: https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/with-durable-objects/]

A 20 percent / 80 percent split is not “all objects on new code.” It is “some objects pinned to B, some still pinned to A, until you create another deployment.” Official docs also: Durable Object class lifecycle changes (create, delete, rename, transfer) cannot be uploaded as gradual versions. Those changes are atomic and go through `npx wrangler deploy`. Lifecycle is a third ticket. Do not mix it with a code-update delay. [Source: https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/with-durable-objects/]

If chat was quiet while 20 percent of objects sat on B, file “partial assignment.” Do not file all-cutover.

## Compatibility across the window is the real work

Official known-issues, Code updates: it is best practice to ensure that API changes between your Workers and Durable Objects are forward and backward compatible across code updates. The reason is the window itself. The latest Worker can call a previous-class object for seconds to minutes even without a gradual split. [Source: https://developers.cloudflare.com/durable-objects/platform/known-issues/]

That is the Monday job. Keep the old RPC method until the named owner prints that objects left the old class. Add the new method beside it. Do not delete the old argument shape in the same deploy that also changes storage layout. Lifecycle migrations stay on their own `wrangler deploy` because official docs say they are atomic and cannot roll back to a version before the migration. [Source: https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/with-durable-objects/]

A coding agent that “just bumps the class” in the same PR as a deleted method is writing the outage. The green CLI will still be green.

## What you must not do

Forbidden:

1. File a “Durable Object code is live” ticket without printing the deploy result, the code-update mode or unset default, the max delay, and one human name on the Workers cutover.
2. Put a Wrangler version in the title or the first line. The pin is evidence after the decision.
3. Mix this field with a `/readyz` store ticket, a timed-out job ticket, a compound-glob ticket, or a wrangler-never-returns ticket. Those are other posts.
4. Write a force-immediate how-to, a recommended `max_delay`, or a “pass this flag in CI” runbook. The public notes already state the default is deferred with a 5-minute maximum. You do not need a live skip-the-wait recipe. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.141.0]
5. Treat `npx wrangler@latest` as GitHub tag `wrangler@4.141.0`. This morning `registry.npmjs.org/wrangler/latest` still answered 4.140.0 while the 4.141.0 tarball existed. Print both. [Source: https://registry.npmjs.org/wrangler/latest] [Source: https://registry.npmjs.org/wrangler/4.141.0]
6. Recommend buying Workers, a plan, or a seat because one deploy stayed green.
7. Treat a gradual 20 percent assignment as all objects on the new class. Official docs: each object is assigned one version for that deployment. [Source: https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/with-durable-objects/]
8. Treat “Worker latest” as “Durable Object latest.” Official docs: the latest Worker can call a previous-class object for seconds to minutes. [Source: https://developers.cloudflare.com/durable-objects/platform/known-issues/]
9. Mix class lifecycle (create, delete, rename, transfer) with a code-update delay. Official docs: lifecycle changes are atomic and are not gradual. [Source: https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/with-durable-objects/]
10. Paste a ready-check, permission-NUL, or queue-timeout fix because those families shipped this week. Those are different fields.

Allowed:

1. Print `wrangler deploy` (or `versions deploy`) exit code from the job that actually ran.
2. Print `durable_objects.code_update_strategy` or write `unset_default` with the public 5-minute deferred maximum.
3. Name one human as `WORKERS_CUTOVER_OWNER`.
4. Keep Worker and Durable Object APIs compatible across the documented window.
5. Print `npx wrangler --version` and `npm view wrangler dist-tags.latest` after the decision, in a details block, not in the title.
6. File “Worker uploaded, Durable Object still deferred” as the ticket title when those two columns disagree.

GSC this week still has no striking-distance query on the `/readyz` post, the timed-out-job post, or the HTTP 400 post. I am not refreshing those URLs. This is a new field, not a synonym of Saturday’s ready bit or Thursday’s queue clock.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about a deferred Durable Object delay is not permission to skip the instance clock.

## What you should do Monday morning

1. Open the repo that actually ships. Export `WORKERS_CUTOVER_OWNER` to a human name. Run `probe_do_cutover.py` against the Wrangler config CI uses. Write the verdict on the ticket next to that name.
2. Print the last CI deploy log. Write exit code, command (`deploy` vs `versions deploy` vs `rollback`), and whether anyone passed `--durable-objects-code-update-mode`. If the flag is absent, write `unset_default`. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.141.0]
3. If chat was quiet after a green deploy, file “Worker uploaded.” Decide whether Durable Object instances were still inside the deferred window. Official language: the latest Worker can call a previous-class object for seconds to minutes. [Source: https://developers.cloudflare.com/durable-objects/platform/known-issues/]
4. If someone pastes only a green CLI, reject the review until the named owner can show four lines: owner, deploy result, mode, max delay.
5. Print `npx wrangler --version` and `npm view wrangler version dist-tags --json`. If the laptop is behind the 25 September 2026 GitHub tag that named the strategy field, do not treat the local pin as those fields. Compare GitHub tag, npm tarball, and `latest`, then decide an upgrade as change control, not as a social post. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.141.0] [Source: https://registry.npmjs.org/wrangler/latest]
6. Confirm coding-agent instructions on this desk name the same owner and forbid “Durable Object code is live” without the four lines: owner, deploy result, mode, max delay.

The question is not whether a green CLI demos well in a gist. The question is whether the named owner can still tell a Worker upload from Durable Object instances that left the old class after handoff.

## Further reading

{{< source href="https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.141.0" label="GitHub — wrangler@4.141.0 release notes" >}}

{{< source href="https://developers.cloudflare.com/durable-objects/platform/known-issues/" label="Cloudflare docs — Durable Objects known issues (global uniqueness and code updates)" >}}

{{< source href="https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/with-durable-objects/" label="Cloudflare docs — gradual deployments with Durable Objects" >}}
