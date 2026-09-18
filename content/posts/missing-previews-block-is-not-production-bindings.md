---
title: "A Missing Previews Block Is Not a License to Reuse Production Bindings"
date: 2026-09-18T07:00:00+07:00
draft: false
slug: "missing-previews-block-is-not-production-bindings"
description: "A Wrangler onboarding write for a missing previews block is a warning, not permission to point preview at production KV, D1, or secrets. Print the block, the placeholder, and the named config owner before you ship."
topics: ["developer-tools"]
tags: ["wrangler", "cloudflare-workers", "previews", "bindings", "coding-agents", "change-control"]
cover: /covers/missing-previews-block-is-not-production-bindings.png
seo:
  primaryQuery: "Wrangler missing previews block production bindings"
  secondaryQueries:
    - "wrangler preview previews block not production KV"
    - "REPLACE_ME preview bindings Wrangler onboarding"
    - "who owns wrangler.jsonc previews block"
---

Standup hears “preview is using production.” Someone pasted a Wrangler log. There is no `previews` block in the local config. The CLI wrote a Preview Base into the file. When no Preview Base existed, it printed a placeholder derived from production bindings and warned against reusing that configuration. The junior treats the placeholder as a filled-in answer. They tell the coding agent to copy the production KV id, the production D1 id, and the production secret names into the new block so the preview “just works.”

I stop the run there. A missing `previews` block is not a license to reuse production bindings. Official Wrangler notes for the 16 September 2026 GitHub tag, not a prerelease, name the field: when a local `previews` block is absent, Wrangler writes the Preview Base configuration to the local config file. When no Preview Base configuration exists, Wrangler prints a placeholder configuration derived from production bindings and warns against reusing production binding configuration. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.133.0]

The pull request behind that note is public. When you run `npx wrangler preview` with no local `previews` block, Wrangler recommends a snippet. The expected snippet uses `REPLACE_ME` placeholders. Two origins, same rule: dashboard Preview Base, or first-time preview from production settings. Both paths are supposed to land on placeholders, not on live production ids. [Source: https://github.com/cloudflare/workers-sdk/pull/15600]

I already refused to treat an old MCP handshake as a dead Laravel server in [A Client That Still Sends Initialize Is Not a Broken Laravel MCP Server](/blog/initialize-is-not-a-broken-laravel-mcp-server/). I already refused to treat a five-minute WebFetch fail as a hung model in [A 300-Second WebFetch Fail Is Not a Hung Model](/blog/a-300-second-webfetch-fail-is-not-a-hung-model/). This post is the same desk rule for a config write. Print the block. Print the placeholder. Name who owns `wrangler.jsonc`.

The question is not whether `wrangler preview` demos well on a personal account. The question is whether the named owner can still tell an onboarding warning from permission to point preview at production data.

<!--more-->

![Four stations: missing block, CLI write, warning, named owner](/img/missing-previews-block-is-not-production-bindings-1.png)

## The warning is the ticket

Juniors read a generated config the way they read a green deploy. The file grew a `previews` block. The command returned. They assume the Worker is now safe to share.

A write is not an approval. Official notes split two cases. Do not mix them.

1. Local `previews` block absent, Preview Base already exists — Wrangler writes that Preview Base into the local file. That is onboarding. It is not “copy production.” [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.133.0]
2. Local `previews` block absent, no Preview Base — Wrangler prints a placeholder derived from production bindings and warns against reusing production binding configuration. The warning is the ticket. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.133.0]

The pull request that shipped the onboarding is explicit about the snippet: `REPLACE_ME` placeholders, not live ids. If the file still says `REPLACE_ME`, you do not have a preview environment. You have a stub. [Source: https://github.com/cloudflare/workers-sdk/pull/15600]

{{< note type="warning" title="Do not paste production ids into the stub" >}}
If Wrangler just wrote a `previews` block, copy the warning, leave `REPLACE_ME` in place, and name the human who owns `wrangler.jsonc` before anyone “fixes” the preview by copying production KV, D1, R2, or secret bindings.
{{< /note >}}

This is not the same field as `preview_urls`. Official Workers docs still document `preview_urls` as a boolean that toggles versioned and aliased `workers.dev` preview URLs. Default follows `workers_dev`. That flag is routing. It does not name which D1 preview is allowed to read. [Source: https://developers.cloudflare.com/workers/versions-and-deployments/preview-urls/] [Source: https://developers.cloudflare.com/workers/wrangler/configuration/]

A custom-domain preview that 404s after you add the domain is a different ticket. That family already shipped on this desk as social copy. Do not merge “missing `previews` block” into “preview URL 404.” One is bindings. One is DNS and domain attach.

## Three tickets, one owner

Laravel plus Vue work on this desk still sits next to a Worker or Pages Function: a `wrangler.jsonc` in the repo, a coding agent that “helpfully” fills ids, a junior who sees a warning and pastes production because the preview must hit real data. Mixing “missing block,” “placeholder warning,” and “preview URL 404” into one “Wrangler is broken” thread burns an hour of backend people on a config they do not own.

| Ticket | What it means | What you do | Owner |
| --- | --- | --- | --- |
| No local `previews` block; CLI writes Preview Base or a `REPLACE_ME` stub | Onboarding, not a filled environment | Leave placeholders. Do not copy production ids | Named human who owns `wrangler.jsonc` |
| Warning against reusing production binding configuration | The CLI already refused the shortcut | Keep the warning on the ticket. Create a separate preview KV/D1 | Same named human |
| Custom-domain preview 404 after the domain is attached | Routing / DNS, not bindings | Check the domain attach, not the D1 id | Named human who owns the Pages/Workers domain |

Do not paste one warning screenshot and call the Worker ready. If the body still names `REPLACE_ME`, you are on an onboarding ticket. If the body names the production KV id inside `previews`, you are on a data-risk ticket. If the preview hostname 404s and the bindings are already split, you are on a domain ticket.

{{< details summary="Pins are evidence, not the hook" >}}
The GitHub tag that named the missing-block onboarding is `wrangler@4.133.0`, published 16 September 2026, 20:30 UTC, prerelease false. npm recorded `4.133.0` at 2026-09-16T20:23:15.485Z. The next morning, npm `latest` moved to `4.134.0` at 2026-09-17T15:39:50.975Z. That later GitHub tag, also not a version-hook, marks `wrangler preview` commands as open beta in help output and command warnings. Print `npx wrangler --version` on the host. Do not put those numbers in the title. Do not treat open beta as a production cutover. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.133.0] [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.134.0] [Source: https://registry.npmjs.org/-/package/wrangler/dist-tags]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous host is ordinary: a Worker in front of the same app that serves the admin, a `wrangler.jsonc` next to `composer.lock`, and a coding agent that treats a generated `previews` block as a completed PR. I treat that file as a named owner’s artifact, the same way I treat a `.env` key. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “which D1 preview is allowed to read.” A coding agent does not get to hide a production id inside `previews` so standup looks green. I already wrote the sibling rule for an old MCP handshake that is not a dead server, and for a five-minute fetch fail that is not a hung model. This is the sibling for an onboarding write that is not permission to reuse production bindings.
{{< /field-note >}}

![Three tickets: missing block, production-reuse warning, preview URL 404](/img/missing-previews-block-is-not-production-bindings-2.png)

## What a missing previews block actually buys you

I do not invent a fake dashboard. I use the public contract.

Official notes add one more field in the same tag: you can configure `placement` in the `previews` block. Preview-specific placement overrides the top-level placement for Preview Defaults and deployments. That is a placement override. It is not a license to inherit production data. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.133.0]

The onboarding pull request names `npx wrangler preview` as the command that triggers the snippet when the local block is missing. A later tag, the current npm `latest` on the morning of 18 September 2026, labels those Preview commands as open beta in help output and command warnings. Open beta is a label. It is not “flip this on production traffic.” [Source: https://github.com/cloudflare/workers-sdk/pull/15600] [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.134.0]

Official Wrangler configuration docs still treat the config file as the source of truth. Sample files show `kv_namespaces` with a binding name and an `id`. They also document `preview_id` on KV for `wrangler dev --remote`. That older `preview_id` field exists because preview was never supposed to silently share the production namespace. The new `previews` block is the same idea, written as a block instead of a sibling key. [Source: https://developers.cloudflare.com/workers/wrangler/configuration/]

If the coding agent copies the production `id` into the preview side “so tests pass,” you did not finish onboarding. You wired the preview to production.

## Probe without a bypass

Do not wrap this in a “compatibility shim” that copies production ids into `previews` so CI goes green. Official notes already warn against reusing production binding configuration. A homemade copy is a config-bypass. I will not put one in this post.

Print the CLI pin on the host that actually runs Wrangler:

```bash {linenos=inline,hl_lines=[3,6]}
#!/usr/bin/env bash
set -euo pipefail
npx wrangler --version
test -f wrangler.jsonc || test -f wrangler.toml
echo "OWNER=${WRANGLER_CONFIG_OWNER:?set WRANGLER_CONFIG_OWNER to a human name}"
rg -n "previews|REPLACE_ME|preview_urls" wrangler.jsonc wrangler.toml 2>/dev/null || true
```

That script does not deploy. It prints the pin, forces a human name, and shows whether the block and the placeholder exist. Empty `OWNER` fails on purpose.

Then fail the PR if the preview side still carries production ids or leftover placeholders after someone claimed the preview was ready:

```python
# check_previews_not_production.py
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PLACEHOLDER = "REPLACE_ME"
OWNER = "WRANGLER_CONFIG_OWNER"


def load_config(root: Path) -> tuple[dict, Path]:
    jsonc = root / "wrangler.jsonc"
    json_file = root / "wrangler.json"
    path = jsonc if jsonc.exists() else json_file
    if not path.exists():
        raise SystemExit("no wrangler.jsonc or wrangler.json in this directory")
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    raw = re.sub(r"^\s*//.*$", "", raw, flags=re.M)
    return json.loads(raw), path


def ids_from(block: object) -> set[str]:
    found: set[str] = set()
    if isinstance(block, dict):
        for key, value in block.items():
            if key in {"id", "preview_id", "database_id", "bucket_name"} and isinstance(
                value, str
            ):
                found.add(value)
            else:
                found |= ids_from(value)
    elif isinstance(block, list):
        for item in block:
            found |= ids_from(item)
    return found


def main() -> int:
    owner = Path(".wrangler-owner").read_text(encoding="utf-8").strip() if Path(".wrangler-owner").exists() else ""
    if not owner:
        print(f"FAIL: write one human name to .wrangler-owner ({OWNER})")
        return 2
    cfg, path = load_config(Path("."))
    text = path.read_text(encoding="utf-8")
    if "previews" not in cfg and "previews" not in text:
        print("FAIL: no previews block — onboarding is not done")
        print(f"owner={owner} file={path}")
        return 2
    if PLACEHOLDER in text:
        print("FAIL: REPLACE_ME still in config — stub is not an environment")
        print(f"owner={owner} file={path}")
        return 2
    production_ids = ids_from({k: v for k, v in cfg.items() if k != "previews"})
    preview_ids = ids_from(cfg.get("previews", {}))
    overlap = production_ids & preview_ids
    overlap.discard("")
    if overlap:
        print("FAIL: preview reuses production binding ids")
        print("overlap=" + ",".join(sorted(overlap)))
        print(f"owner={owner} file={path}")
        return 2
    print(f"PASS owner={owner} file={path} preview_ids={len(preview_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Run it from the app root the supervisor uses, not from a laptop clone that never ships:

```bash
echo "Shinjae Kang" > .wrangler-owner
python3 check_previews_not_production.py
```

`FAIL: no previews block` means onboarding did not finish. `FAIL: REPLACE_ME still in config` means the snippet is still a stub. `FAIL: preview reuses production binding ids` means someone copied production. All three are named-owner tickets. None of them is “Wrangler is down.”

I do not claim this script talks to Cloudflare. It reads the file you are about to commit. That is the artifact.

![Probe the file: pin, owner, stub, overlap](/img/missing-previews-block-is-not-production-bindings-3.png)

## What you must not do

Forbidden:

1. File a “preview is production” ticket without printing `npx wrangler --version`, the presence of a `previews` block, and one human name on `wrangler.jsonc`.
2. Put the Wrangler version in the title or the first line. The version is evidence after the decision.
3. Mix this field with a custom-domain preview 404, a Hyperdrive `SELECT 1` fail, or a Node.js compat flag. Those are other tickets.
4. Treat a generated placeholder as a filled preview. Official notes warn against reusing production binding configuration. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.133.0]
5. Copy production KV, D1, R2, or secret ids into `previews` so the coding agent’s tests pass. That is a bypass.
6. Treat open beta `wrangler preview` as a production cutover because npm `latest` moved the next day. The later tag labels the commands as open beta. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.134.0]
7. Recommend buying a new host, a new plan, or a new model because the preview warning looks scary.

Allowed:

1. Print whether `previews` exists in the local file.
2. Print whether `REPLACE_ME` is still in the file.
3. Print `npx wrangler --version` on the host.
4. Stop, and ping the named owner of `wrangler.jsonc`.
5. Create a separate preview KV/D1, then replace placeholders on purpose, with a written exception if any binding must stay shared.

GSC this week still has no striking-distance query on the initialize post, the WebFetch post, or the HTTP 400 post. I am not refreshing those URLs. This is a new field, not a synonym of yesterday’s handshake or Wednesday’s fetch fail.

## This is not a preview 404

A custom-domain preview 404 after you add the domain is a routing miss. Official Preview URL docs still say versioned and aliased previews live on `workers.dev`, Preview URLs follow `workers_dev` when `preview_urls` is omitted, and you cannot currently put Preview URLs on a subdomain other than `workers.dev`. [Source: https://developers.cloudflare.com/workers/versions-and-deployments/preview-urls/]

This post is a bindings miss. The CLI wrote a stub. The warning told you not to reuse production. The junior still pasted production ids.

Do not merge the two into “Wrangler preview is broken.” A 404 on a new custom domain still needs DNS. A `REPLACE_ME` stub still needs a named owner and a separate database. They do not share a vendor-down channel.

If you need the broader habit, start at [/developer-tools/](/developer-tools/). Agent verification lives under [/ai-agent-operations/](/ai-agent-operations/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/) when the agent is touching that stack. A first-week map is at [/start-here/](/start-here/). Do not mix those hubs into the bindings row.

I already refused to treat a green package bump as ownership of the next repair. Same here. A changelog bullet about a `previews` block is not permission to skip the warning.

![Two tickets: routing 404 versus bindings](/img/missing-previews-block-is-not-production-bindings-4.png)

## What you should do Monday morning

1. Open the repo that actually deploys the Worker. Run `npx wrangler --version`. Write the string on the ticket next to one human name. That person owns `wrangler.jsonc`.
2. Search the file for `previews` and `REPLACE_ME`. If the block is missing, you are still in onboarding. If `REPLACE_ME` is present, the stub is not an environment. Do not leave that as a tribal screenshot in Slack.
3. Run `check_previews_not_production.py` in the app root the supervisor uses. Confirm it matches the file CI will ship. A laptop config is not the host.
4. If the overlap check fails, create a separate preview KV and D1. Replace placeholders on purpose. Do not copy production ids to silence the warning.
5. Confirm coding-agent instructions on this desk name the same owner and forbid “reuse production so preview works.” A prompt that says “make wrangler preview pass” without naming the owner is a different ticket.
6. If the named pin is older than the 16 September 2026 GitHub tag that described the missing-block write, the owner bumps Wrangler on purpose, then re-runs the file probe. If the named pin is already on that line or the next day’s open-beta label, you still do not have a production-safe preview until placeholders are gone and production ids do not overlap.

The question is not whether `wrangler preview` demos on a personal account. The question is whether the onboarding warning survives maintenance, handoff, and a junior who wants the preview to share production data.

## Further reading

{{< source href="https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.133.0" label="GitHub wrangler@4.133.0 — missing previews block onboarding and production-binding warning" >}}

{{< source href="https://github.com/cloudflare/workers-sdk/pull/15600" label="PR 15600 — REPLACE_ME snippet when wrangler preview has no local previews block" >}}

{{< source href="https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.134.0" label="GitHub wrangler@4.134.0 — wrangler preview commands labeled open beta" >}}
