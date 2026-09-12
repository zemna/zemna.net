---
title: "Node.js APIs On Is Not the New Module Registry"
date: 2026-09-12T07:00:00+07:00
draft: false
slug: "nodejs-apis-on-is-not-the-new-module-registry"
description: "When import.meta.url fails on a Worker, Node.js APIs are already on. Name who owns the compat-flag list before the coding agent flips the wrong switch."
topics: ["developer-tools"]
tags: ["cloudflare-workers", "nodejs-compat", "module-registry", "wrangler", "coding-agents", "change-control"]
cover: /covers/nodejs-apis-on-is-not-the-new-module-registry.png
seo:
  primaryQuery: "Cloudflare Workers Node.js compatibility vs new module registry"
  secondaryQueries:
    - "import.meta.url Workers new_module_registry flag"
    - "nodejs_compat default 2026-08-04 Workers"
    - "who owns Workers compatibility_flags list"
---

Standup hears “Node compat is off.” Someone pasted a red agent log. `import.meta.url` is undefined. A package that worked on Node 22 throws in `wrangler dev`. The junior opens the Cloudflare status page. The coding agent offers to “turn Node.js compatibility back on” by rewriting `compatibility_flags` until chat works.

I stop the run there. A missing `import.meta.url` is a module-registry ticket until proven otherwise. It is not “Workers turned Node off.”

On 9 September 2026 Cloudflare published the field note that names the split. Node.js APIs that you want in a serverless Worker are already on by default. The new URL-based module registry is a **separate** compatibility flag named `new_module_registry`. Official post: that flag does not have a default-on date. It will not turn on from `compatibility_date` alone. You add it on purpose. [Source: https://blog.cloudflare.com/workers-module-registry-nodejs/]

I already refused to treat a failed Cloudflare login as a status outage in [Read the Requested Scopes Before You File an Outage](/blog/requested-scopes-before-outage/). I already refused to treat an unreadable managed allow-list as a company lockdown in [Treat Unreadable Managed Settings as Empty](/blog/treat-unreadable-managed-settings-as-empty/). This post is the same desk rule for Workers flags. Read the list. Split the two switches. Name who owns that list. Do not let the agent flip `no_nodejs_compat` because a URL API is missing.

The question is not whether Node “works” in chat. The question is which flag the named owner pinned, and whether the coding agent is allowed to touch it.

<!--more-->

![Two switches: Node APIs on, registry flag off, named owner](/img/nodejs-apis-on-is-not-the-new-module-registry-1.png)

## The red import.meta that looks like Node is off

Juniors read a missing `import.meta.url` the way they read a missing `node:fs`. Red text. The word “Node.” A package that used to resolve. They assume the runtime dropped Node.js compatibility overnight.

Those are two different machines.

Node.js **API** compatibility is the set of built-ins: `node:crypto`, `node:buffer`, `node:stream`, `node:fs`, `node:http`, and the rest of the supported table. For compatibility dates of `2026-08-04` or later, Workers enables that behavior by default. You do not add `nodejs_compat` on a new project with that date. [Source: https://developers.cloudflare.com/changelog/post/2026-08-04-nodejs-compat-default/] [Source: https://developers.cloudflare.com/workers/runtime-apis/nodejs/]

The **module registry** is how the runtime turns a specifier into a compiled module: ESM, CommonJS, Wasm, `node:` as a protocol, `import.meta`, query strings on module URLs, `require()` of ESM. Cloudflare rewrote that registry in `workerd`. You opt in with `new_module_registry`. The official blog is explicit: it does not have a default-on date, so it will not turn on automatically for a Worker, old or new, no matter what compatibility date it uses. [Source: https://blog.cloudflare.com/workers-module-registry-nodejs/]

Three sentences belong on the ticket, in this order:

1. What failed: a Node built-in call, or `import.meta` / specifier resolution / `require(esm)`.
2. What the wrangler file actually pins: `compatibility_date`, `nodejs_compat` / `no_nodejs_compat`, and whether `new_module_registry` is present.
3. Who owns that flag list, and whether the owner will add the registry flag before anyone “fixes Node” by toggling the API switch.

If you skip sentence two, you will file a Node outage for a URL API, or you will disable Node APIs on a date that already turned them on.

{{< note type="warning" title="Do not flip the API switch to fix import.meta" >}}
If `import.meta.url`, `import.meta.main`, or `import.meta.resolve()` fails on a Worker whose `compatibility_date` is 2026-08-04 or later, stop the coding-agent session. Copy the wrangler file. Do not paste `nodejs_compat` as a lucky charm. Do not paste `no_nodejs_compat` to “reset.” The registry flag is a different row.
{{< /note >}}

I do not invent a fake Node outage on this desk. I use the public contract. The 9 September blog names both facts in the same article: APIs on by default, registry behind an explicit flag with no default-on date. [Source: https://blog.cloudflare.com/workers-module-registry-nodejs/]

## Two switches, three owners

Laravel and Vue work on this desk still deploys Workers next to coding agents: a preview Worker for a SaaS webhook, a Pages-adjacent function, a cron that posts a deploy note. Mixing “Node is on,” “the registry is on,” and “the bundle is under 64 MiB” into one “Workers is broken” thread is how a junior turns a missing URL API into a two-hour platform page.

| Switch | What it gates | Default on a date of 2026-08-04 or later | How you opt in / out | Owner |
| --- | --- | --- | --- | --- |
| Node.js APIs | Built-ins such as `node:fs`, `node:crypto`, `node:http` | On | Date does it. To turn **off**, add `no_nodejs_compat` **and** `no_nodejs_compat_v2` | Named human who pins `compatibility_date` |
| New module registry | `import.meta.*`, URL specifiers, `require(esm)`, lazy compile | Off. No default-on date | Add `new_module_registry` on purpose | Named human who owns `compatibility_flags` |
| Uncompressed size | How large the uploaded Worker is | 64 MiB on all plans. Compressed size is no longer the limit | Measure with `wrangler deploy --dry-run` | Named human who owns the bundle budget |

Do not copy the size ticket onto the registry ticket. Cloudflare’s 4 September changelog removed the compressed 3 MB / 10 MB check. The runtime now checks uncompressed size only, 64 MiB on free and paid. `Total Upload` is the number that counts. The gzip line is reference. [Source: https://developers.cloudflare.com/changelog/post/2026-09-04-increased-worker-size-limit/]

Do not paste one screenshot and call every row done. If the red line names `import.meta.url`, you are on the registry row. If it names `node:fs` or `[unenv] … is not implemented yet!`, you are on the API / polyfill row. If Wrangler prints a size reject, you are on the bundle row. Write the row name first.

{{< details summary="Dates are evidence, not the hook" >}}
Node.js API default-on date: 2026-08-04. Registry blog date: 9 September 2026. Size changelog date: 4 September 2026. Pin what you run. Do not put those dates in the title. Do not treat “Node is on by default” as permission to assume `import.meta.url` exists. [Source: https://developers.cloudflare.com/changelog/post/2026-08-04-nodejs-compat-default/] [Source: https://blog.cloudflare.com/workers-module-registry-nodejs/] [Source: https://developers.cloudflare.com/changelog/post/2026-09-04-increased-worker-size-limit/]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous Worker is ordinary: a coding agent that “helps” when a preview function cannot read `import.meta.url`, and a junior who pastes `nodejs_compat` or, worse, `no_nodejs_compat` into wrangler because chat said Node is off. I treat `compatibility_flags` as a named owner’s artifact, the same way I treat a migration. The person who owns [/developer-tools/](/developer-tools/) on this desk also owns “which Worker loaded which flag list.” Copilot does not get to rewrite the registry flag as a drive-by lint. I already wrote the sibling rule for a requested-scope list that is not a status page. This is the sibling for a URL API that is not an API kill-switch.
{{< /field-note >}}

![Read the flag list: Node APIs by date, registry explicit flag, 64 MiB uncompressed](/img/nodejs-apis-on-is-not-the-new-module-registry-2.png)

## What Node-on-by-default actually means

Read the changelog before you let the agent “enable Node.”

For compatibility dates of `2026-08-04` or later, Workers enables both `nodejs_compat` and `nodejs_compat_v2` by default. Built-in Node.js APIs and polyfills are available without extra flags. Those two flag names are **not used** for those dates because the date already enables the same behavior. Wrangler, Miniflare, the Cloudflare Vite plugin, and the Workers Vitest plugin ignore the redundant positive flags when starting the runtime. Existing projects do not need to remove them when updating the date. New projects omit them. [Source: https://developers.cloudflare.com/workers/runtime-apis/nodejs/] [Source: https://developers.cloudflare.com/changelog/post/2026-08-04-nodejs-compat-default/]

To turn Node.js compatibility **off** on a date of 2026-08-04 or later, you remove the positive flags if present, then add **both** `no_nodejs_compat` and `no_nodejs_compat_v2`. One disable flag is not the contract. [Source: https://developers.cloudflare.com/workers/configuration/compatibility-flags/]

A coding agent that “helps” by adding `nodejs_compat` on a 2026-09-12 date is writing a no-op. A coding agent that “helps” by adding only `no_nodejs_compat` is writing a half-disable that does not match the docs. A coding agent that adds both disable flags because `import.meta.url` failed has now turned off Node APIs to treat a registry miss. That is the incident.

For dates from `2024-09-23` through `2026-08-03`, you still add `nodejs_compat` to opt in. Those Workers are not on the default-on contract. Write the date on the ticket before anyone debates flags. [Source: https://developers.cloudflare.com/workers/runtime-apis/nodejs/]

Polyfills are a third smell. Wrangler injects unenv shims for APIs the runtime does not implement. Calling a mocked method no-ops or throws `[unenv] <method> is not implemented yet!`. That error is not “Node compat is off.” It is “this method is a stub.” Do not disable Node to silence it. Do not enable the registry flag to silence it. File the package against the supported API table. [Source: https://developers.cloudflare.com/workers/runtime-apis/nodejs/]

## What the new registry actually turns on

The official blog lists the behavior behind `new_module_registry`. Copy this list onto the ticket. Do not summarize it as “Node modules work now.”

When the flag is on:

- `import.meta.url`, `import.meta.main`, and `import.meta.resolve()` work.
- Module specifiers parse as real URLs, including query strings and fragments.
- `node:` built-ins resolve to the same module instance no matter how you reach them.
- Import attributes (`with { type: 'json' }`) are validated.
- `require()` on an ES module follows Node.js `require(esm)` rules.
- Errors use consistent classes and messages across static import, dynamic `import()`, and `require()`.
- Modules compile lazily on first import.
- WebAssembly supports source-phase imports.

[Source: https://blog.cloudflare.com/workers-module-registry-nodejs/]

The old registry resolves specifiers as filesystem-style paths, not URLs. That is why `import.meta.url` had no clean implementation, why relative imports did not match `new URL()`, and why `node:` and `cloudflare:` were string prefixes instead of protocols. The old registry also compiles the whole bundle up front and keeps a private copy per V8 isolate. The new one starts from URLs and treats laziness and cache sharing as design, not a later patch. Deployed Workers on the old registry keep working. Cloudflare is not flipping the world on a date. [Source: https://blog.cloudflare.com/workers-module-registry-nodejs/]

Python Workers do not use the new registry. When `python_workers` is enabled, `new_module_registry` is ignored. Do not diagnose a Python Worker `import.meta` miss as a missing Node flag. [Source: https://github.com/cloudflare/workerd/blob/main/docs/reference/detail/new-module-registry.md]

Wrangler still bundles most npm graphs into one module with esbuild. Vite 8 plus the Cloudflare Vite plugin emits an entry plus chunks via Rolldown. `--no-bundle` uploads the graph you wrote. In every case, **something** has to resolve a specifier. That something is the registry. Bundling does not give you `import.meta.url` on the old path. [Source: https://blog.cloudflare.com/workers-module-registry-nodejs/]

{{< note type="note" title="The flag name is evidence" >}}
The flag string is `new_module_registry`. Put it in the wrangler file, not in the title of the incident. A junior who googles the flag after the ticket is classified is doing the job. A junior who pastes the flag name into Slack as the headline is writing a version-pin.
{{< /note >}}

![import.meta.url failure is a registry ticket; do not disable Node](/img/nodejs-apis-on-is-not-the-new-module-registry-3.png)

## Pin the list the agent is not allowed to rewrite

Here is the wrangler shape I want on the ticket. Dates in this block are examples. Replace them with the date the named owner pinned. Do not copy a future date from chat.

```json {linenos=inline,hl_lines=[3,"5-6"]}
{
  "name": "preview-hooks",
  "compatibility_date": "2026-09-12",
  "compatibility_flags": [
    "new_module_registry"
  ],
  "main": "src/index.js"
}
```

On this date, Node APIs are already on. The only extra flag is the registry. There is no `nodejs_compat` line. There is no `no_nodejs_compat` line.

The disable contract, for a Worker that must not load Node built-ins, is both flags together:

```json
{
  "name": "preview-hooks",
  "compatibility_date": "2026-09-12",
  "compatibility_flags": [
    "no_nodejs_compat",
    "no_nodejs_compat_v2"
  ],
  "main": "src/index.js"
}
```

That second file is a product decision. It is not a repair for `import.meta.url`. If the coding agent produces the second file because the first file’s registry line was missing, reject the PR.

Classify with a script. Do not ask the agent to “clean wrangler.”

```python {linenos=inline,hl_lines=[16,"24-31"]}
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
date = data.get("compatibility_date") or ""
flags = data.get("compatibility_flags") or []
if not isinstance(flags, list):
    print("invalid_flags: compatibility_flags is not a list")
    sys.exit(3)

node_off = "no_nodejs_compat" in flags and "no_nodejs_compat_v2" in flags
node_half = ("no_nodejs_compat" in flags) != ("no_nodejs_compat_v2" in flags)
registry = "new_module_registry" in flags
default_node_date = date >= "2026-08-04"

print(f"date={date or 'MISSING'}")
print(f"node_apis={'off' if node_off else 'on_by_date' if default_node_date else 'opt_in_needed'}")
print(f"registry={'on' if registry else 'off'}")
if node_half:
    print("half_disable: both no_nodejs_compat and no_nodejs_compat_v2 are required")
    sys.exit(4)
if not registry:
    print("registry_off: import.meta.url is not a Node-API outage")
    sys.exit(2)
print("ok: registry flag present; Node APIs not half-disabled")
```

This script does not claim Wrangler uses Python. It gives the named owner three labels a human can compare to the official pages: date versus 2026-08-04, both disable flags, registry present or absent. [Source: https://developers.cloudflare.com/workers/runtime-apis/nodejs/] [Source: https://blog.cloudflare.com/workers-module-registry-nodejs/]

If the owner needs the registry, that is a flag ticket. It is not a coding-agent ticket to invent `nodejs_compat`. I do not publish a recipe that disables Node to “reset.”

## A fixture the PR has to fail first

I do not merge a registry flag because chat said the package needs it. I merge it when a fixture names the miss.

```js {linenos=inline,hl_lines=[6,"12-16"]}
export default {
  async fetch() {
    const url = import.meta.url;
    const main = import.meta.main;
    if (typeof url !== "string" || !url) {
      return new Response("registry_miss: import.meta.url", { status: 500 });
    }
    if (main !== true) {
      return new Response("entrypoint_miss: import.meta.main", { status: 500 });
    }
    const resolved = import.meta.resolve("./index.js");
    return new Response(
      JSON.stringify({ url, main, resolved }),
      { headers: { "content-type": "application/json" } }
    );
  },
};
```

Run it twice. Once without `new_module_registry`. Once with it. Save both responses on the ticket. The first run is the proof the miss is the registry. The second run is the proof the flag does what the blog says. Do not accept a PR that only adds the flag and deletes the fixture.

A second fixture belongs on the API row, not this one:

```js
import { Buffer } from "node:buffer";

export default {
  async fetch() {
    const buf = Buffer.from("ok");
    return new Response(buf.toString());
  },
};
```

If this fails on a date of 2026-08-04 or later, you have a Node-API ticket: wrong date, both disable flags, or a stub. If this passes and the `import.meta` fixture fails, you already have the split. Stop mixing them. [Source: https://developers.cloudflare.com/changelog/post/2026-08-04-nodejs-compat-default/]

{{< note type="danger" title="Do not disable Node to make the fixture green" >}}
A red `import.meta.url` plus a green `node:buffer` is the registry row. Adding `no_nodejs_compat` will not invent `import.meta`. It will take down the green row.
{{< /note >}}

## Size is a third ticket, not a fourth flag

The same 9 September blog mentions larger Node apps, up to 64 MiB, and the removed compressed-bundle limit. Juniors glue that sentence to the registry flag and ship a “we need the new registry because the Worker is too big” PR.

Size is measured. It is not a flag.

Cloudflare now checks uncompressed size only. The limit is 64 MiB on all plans. Dry-run:

```bash
wrangler deploy --outdir bundled/ --dry-run
```

`Total Upload` is uncompressed. That number counts. `gzip:` is shown for reference and is no longer a limit. [Source: https://developers.cloudflare.com/changelog/post/2026-09-04-increased-worker-size-limit/]

If `Total Upload` is over 64 MiB, you have a bundle ticket: drop a dependency, split a Worker, stop inlining a dataset. The registry flag does not raise the limit. The Node default-on date does not raise the limit. Do not let the agent “enable Node” to fix a size reject.

I already refused to treat a green package bump as ownership of Postgres post-update repairs. Same instinct: a changelog sentence about 64 MiB is not permission to skip the dry-run number.

![Before the agent edits wrangler: date, import.meta vs buffer, registry flag, dry-run size](/img/nodejs-apis-on-is-not-the-new-module-registry-4.png)

## What the coding agent is allowed to do

The agent’s first idea is always the same: edit the nearest wrangler file until `import.meta.url` prints. That is how you launder a registry miss into an API kill-switch.

Allowed:

1. Print `compatibility_date` and `compatibility_flags` from the wrangler file the Worker actually deploys.
2. Run the two fixtures above. Save both status codes.
3. Run `wrangler deploy --dry-run` and copy `Total Upload`.
4. Stop, and ping the named owner of the flag list.

Forbidden:

1. Add `nodejs_compat` on a date of 2026-08-04 or later “to turn Node back on.”
2. Add `no_nodejs_compat` without `no_nodejs_compat_v2`, or add both because `import.meta` failed.
3. Add `new_module_registry` and delete the fixture in the same PR.
4. Retry deploy ten times and call the API dead. A different desk rule already covers a generic request-failed storm. Keep them on separate cards. See [Read the Requested Scopes Before You File an Outage](/blog/requested-scopes-before-outage/).

I already refused to leave Copilot Approve on as a required check. The same instinct applies here. The model that wrote the PR does not own the Workers flag list. See [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/) if your team still treats agent review as a merge gate. For the broader agent-ops habit, start at [/ai-agent-operations/](/ai-agent-operations/).

## Merge is not a reason to skip the owner

Flags are a list. Juniors hear “list” and think a preview wrangler can punch a hole in production’s date.

Read the Node docs with the 9 September blog together. The date turns Node APIs on. The registry flag is opt-in with no default-on date. Production and preview are two pins. A preview file that adds `new_module_registry` is not a production pin. Name who promotes the flag. [Source: https://developers.cloudflare.com/workers/runtime-apis/nodejs/] [Source: https://blog.cloudflare.com/workers-module-registry-nodejs/]

I write the owner on the ticket as a person, not a role. “Platform” is how these lists stay half-disabled until Friday.

If you need a deeper map of how this desk treats tools, start at [/start-here/](/start-here/) and keep Workers flags next to the other pins on [/developer-tools/](/developer-tools/). Laravel plus Vue SaaS notes live under [/laravel-vue-saas/](/laravel-vue-saas/) when the Worker is in front of that stack. Do not mix those hubs into the registry row.

## What you should do Monday morning

1. Open the wrangler file the preview Worker actually deploys. Write `compatibility_date` on the ticket. If it is before 2026-08-04, Node APIs are still opt-in. If it is on or after, Node APIs are already on unless both disable flags are present.
2. Search the file for `new_module_registry`, `no_nodejs_compat`, and `no_nodejs_compat_v2`. One disable flag without the other is a half-disable. Registry absent is the default for `import.meta`.
3. Run the `import.meta.url` fixture and the `node:buffer` fixture. If buffer is green and import.meta is red, classify registry. Stop the coding agent.
4. If the owner wants the registry, add only `new_module_registry`. Keep the fixture. Do not add `nodejs_compat` as a lucky charm on a default-on date.
5. Run `wrangler deploy --outdir bundled/ --dry-run`. Copy `Total Upload`. If it is over 64 MiB, that is a bundle ticket, not a flag ticket.
6. Name one human who owns the Workers `compatibility_flags` list. Put that name on the wiki card next to the CLI pin. The agent does not get that seat.

The question is not whether this demos well in chat. The question is whether the flag list survives maintenance, handoff, and a missing URL API.

## Further reading

{{< source href="https://blog.cloudflare.com/workers-module-registry-nodejs/" label="Cloudflare blog — rebuilt Workers module registry (9 September 2026)" >}}

{{< source href="https://developers.cloudflare.com/workers/runtime-apis/nodejs/" label="Workers Node.js compatibility — default-on date and disable flags" >}}

{{< source href="https://developers.cloudflare.com/changelog/post/2026-09-04-increased-worker-size-limit/" label="Changelog — 64 MiB uncompressed Worker size, compressed limit removed" >}}
