---
title: "Treat Unreadable Managed Settings as Empty"
date: 2026-09-10T07:00:00+07:00
draft: false
slug: "treat-unreadable-managed-settings-as-empty"
description: "When a managed allow-list cannot be read, Claude Code now admits nothing. Classify the block, name who owns the file, then resume the coding agent."
topics: ["tutorials"]
tags: ["claude-code", "managed-settings", "http-hooks", "allow-list", "coding-agents", "change-control"]
cover: /covers/treat-unreadable-managed-settings-as-empty.png
seo:
  primaryQuery: "Claude Code unreadable managed settings empty allowlist"
  secondaryQueries:
    - "allowedHttpHookUrls fail closed unreadable"
    - "claude doctor managed settings dropped keys"
    - "named owner managed-settings.json HTTP hooks"
---

Standup hears “the org locked HTTP hooks.” Someone pasted a red agent log. The hook URL that worked yesterday is blocked. The junior opens the vendor status page. The coding agent offers to “relax the allow-list in the project file until chat works.”

I stop the run there. A sudden block on HTTP hooks is a readable-file problem until proven otherwise. It is not “Claude Code locked the company.”

On 9 September 2026 Claude Code published a patch that names three managed allow-list keys. Official notes say managed `allowedHttpHookUrls`, `httpHookAllowedEnvVars`, and `allowedChannelPlugins` now admit nothing, not everything, when those settings are unreadable. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.267] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat an Organization policy why-line as a loaded fleet file in [Read the Why-Line Before You Trust the Org Policy](/blog/org-policy-why-line/). I already refused to treat a failed Cloudflare login as a status outage in [Read the Requested Scopes Before You File an Outage](/blog/requested-scopes-before-outage/). This post is the same desk rule for the managed allow-list. Read the file. Parse the three keys. Name who owns that file. Do not let the agent rewrite policy as a drive-by lint.

The question is not whether the CLI printed a new block. The question is whether the managed file on this machine is readable, and who owns the pin when it is not.

<!--more-->

![Classify the red hook: not a lockdown, read the managed file, name the owner](/img/treat-unreadable-managed-settings-as-empty-1.png)

## The red hook that looks like a lockdown

Juniors read a blocked HTTP hook the way they read a 403 from the public API. Red text. The word “allow.” A URL that used to fire. They assume security shipped a new deny.

Allow-lists do not work that way. Unset means any URL is allowed. An empty array blocks every HTTP hook. A defined array runs a hook only when the URL matches. Official settings docs spell that default in one sentence: when `allowedHttpHookUrls` is unset, any URL is allowed; when you define the key, non-matching URLs are blocked without running; an empty array blocks every HTTP hook. [Source: https://code.claude.com/docs/en/settings-reference]

The 9 September patch changes what happens when the **managed** value cannot be read. The GitHub notes and the changelog use the same sentence: those three keys admit nothing, not everything, when unreadable. “Everything” is the old default for an unset allow-list: any URL, any hook env name, the default channel-plugin list. “Nothing” is the empty-array end of the same docs. Read that bullet as a parse ticket, not as a new deny that security shipped overnight. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.267] [Source: https://code.claude.com/docs/en/changelog]

Three sentences belong on the ticket, in this order:

1. Which managed file or source Claude Code selected (remote, plist, file, drop-ins, or a merged list).
2. Whether `allowedHttpHookUrls`, `httpHookAllowedEnvVars`, or `allowedChannelPlugins` is unreadable as a whole, or only one entry is bad.
3. Who owns that file, and whether the owner will repair it before anyone “unblocks” hooks in a user settings file.

If you skip sentence two, you will file a security incident for a JSON parse, or you will open the allow-list in the wrong file.

{{< note type="warning" title="Do not relax the project file" >}}
If HTTP hooks, hook headers, or channel plugins stop in the same hour the managed file went unreadable, stop the coding-agent session. Copy `claude doctor`. Do not paste a wider `allowedHttpHookUrls` into `~/.claude/settings.json` to “unblock.”
{{< /note >}}

I do not invent a fake lockdown on this desk. I use the public contract. The GitHub release is not a prerelease. Published 9 September 2026 at 19:58 UTC. The bullet is explicit: admit nothing, not everything, when unreadable. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.267]

## Three keys, three owners

Laravel and Vue work on this desk still runs coding agents next to HTTP hooks: a deploy bot that posts to an internal URL, a header that interpolates a token, a channel plugin that pushes a build note. Mixing those three into one “hooks are down” thread is how a junior turns a parse error into a two-hour security page.

| Key | What it gates | Unset | Empty array | Unreadable managed value after 9 September |
| --- | --- | --- | --- | --- |
| `allowedHttpHookUrls` | Which URLs HTTP hooks may call | Any URL | Block every HTTP hook | Empty allow-list until fixed |
| `httpHookAllowedEnvVars` | Which env names may land in hook headers | Each hook’s own list | No header interpolation from env | Empty allow-list until fixed |
| `allowedChannelPlugins` | Which channel plugins may push inbound messages | Default Anthropic list | Block all channel plugins | Empty allow-list until fixed |

Do not copy the version-pin fallback onto these three keys. Official managed-settings docs still say `requiredMinimumVersion` and `requiredMaximumVersion` fail **open** on purpose: an invalid value is dropped rather than enforced. A different row on the same page, `allowedMcpServers`, already enforces an empty allow-list when the value is present but invalid. The 9 September bullet is the HTTP-hook and channel-plugin cousin of that instinct, sourced from the release notes, not from that table. [Source: https://code.claude.com/docs/en/managed-settings] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.267]

`allowedChannelPlugins` is managed-only. `allowedHttpHookUrls` and `httpHookAllowedEnvVars` can live in any settings file and merge across sources. The HTTP hook allow-lists apply to hooks from every source, including managed policy. [Source: https://code.claude.com/docs/en/hooks] [Source: https://code.claude.com/docs/en/settings-reference]

Do not paste one screenshot and call every row done. If the red line names a URL, you are on the HTTP hook row. If it names a header env var, you are on the interpolation row. If it names a channel plugin id, you are on the channel row. Write the key name first.

{{< details summary="npm tags are evidence, not the hook" >}}
This morning’s registry, 10 September 2026: `@anthropic-ai/claude-code` `latest` is 2.1.267, published 9 September 2026 at 18:25 UTC. GitHub `v2.1.267` published 9 September 2026 at 19:58 UTC, prerelease false. The `stable` dist-tag is still 2.1.236, published 19 August 2026. Pin what you run. Do not put those numbers in the title. Do not treat `stable` as the field pin. [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.267]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous hook is ordinary: a coding agent that “helps” when a deploy webhook fails, and a junior who pastes a wider URL pattern into the project settings because chat said the org locked down. I treat the managed-settings file as a named owner’s artifact, the same way I treat a migration. The person who owns [/developer-tools/](/developer-tools/) on this desk also owns “which machine loaded which allow-list.” Copilot does not get to rewrite `allowedHttpHookUrls` as a drive-by lint. I already wrote the sibling rule for a why-line that is not a loaded policy. This is the sibling for a file that will not parse.
{{< /field-note >}}

## Fail closed is a ticket type

Juniors hear “invalid JSON” and think “ignore that key and keep going.” For these three managed keys, the 9 September notes say the opposite when the value is unreadable: admit nothing.

Official admin docs still split other invalid managed values into two jobs. Most managed keys drop the bad item, log a warning, and keep the rest of the policy. A short list of enforcement keys is not dropped when invalid. Claude Code enforces a stricter fallback until the value is fixed. `allowedMcpServers` is on that list. The three hook and channel keys are named in the release notes for the unreadable case. Put the GitHub bullet on the ticket next to doctor, not a reconstructed table. [Source: https://code.claude.com/docs/en/managed-settings] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.267]

User, project, and local settings files stay strict. A file whose JSON or top-level shape fails validation is rejected as a whole and reported. An individual bad permission rule is skipped with a warning while the rest of that file applies. That tolerance sentence on the docs page applies **only** to managed settings. Do not diagnose a broken `~/.claude/settings.json` with the managed fail-closed table. [Source: https://code.claude.com/docs/en/managed-settings]

I keep a short table on the wiki card. I do not let the agent expand it into a bypass novel.

| What you saw | What it is | Next action |
| --- | --- | --- |
| HTTP hooks blocked after a managed-file deploy | Fail-closed empty allow-list, or a real empty array | Run `claude doctor`. Repair the managed file. Do not widen the user file. |
| File parses, one URL pattern looks garbage | Unknown until doctor names the field | Copy doctor. Do not delete the whole key to “unblock.” |
| `/status` Organization policy why-line, hooks still fire | Load miss, not this patch | Read the why-line post. Name the proxy owner. |
| `requiredMinimumVersion` ignored | Fail-open by design | File against the version-pin owner, not against hooks. |

![Three allow-list ends: unset allows, empty blocks, unreadable admits nothing](/img/treat-unreadable-managed-settings-as-empty-2.png)

## Copy doctor, then classify it

Do not screenshot a cropped window. Copy the command, the binary version, and the doctor lines that name dropped keys. Then classify.

```bash {linenos=inline,hl_lines=[3,"18-24"]}
#!/usr/bin/env bash
set -euo pipefail

out=${1:-/tmp/claude-doctor.txt}
bin=$(command -v claude || true)

{
  echo "host=$(hostname)"
  echo "user=$(id -un)"
  echo "claude_bin=${bin:-missing}"
  command -v claude >/dev/null && claude --version || true
} | tee /tmp/cli-pin.txt

claude doctor >"$out" 2>&1 || true

if grep -Ei 'allowedHttpHookUrls|httpHookAllowedEnvVars|allowedChannelPlugins' "$out"; then
  echo "STOP: managed allow-list keys named. File the settings owner, not a lockdown."
  exit 2
fi

if grep -Ei 'unreadable|could not be (read|parsed)|invalid' "$out"; then
  echo "STOP: unreadable or invalid managed value. Empty allow-list until fixed."
  exit 2
fi

echo "doctor did not name the fail-closed keys. Keep the URL, the header, and the plugin id on the ticket."
```

Run that script on the machine that blocked the hook. Do not run it on a laptop that never loaded the fleet file and then declare the fleet healthy.

`claude doctor` is the documented place that lists removed items, their source file, and the field. Official managed-settings docs say to run it when managed settings contain entries that fail the schema. [Source: https://code.claude.com/docs/en/managed-settings]

If doctor names a proxy miss, you are back on the why-line ticket. That is a load problem. This post is a parse problem. I already wrote how to read that why-line. Do not merge the two threads.

## Prove the file before you touch the allow-list

A named owner needs a file path, a parse result, and the three keys. Guessing the path from chat is how you “fix” a file the CLI never read.

Linux and WSL file source: `/etc/claude-code/managed-settings.json`. macOS file source: `/Library/Application Support/ClaudeCode/managed-settings.json`. Pass another path as argv when MDM or a drop-in directory is the source. [Source: https://code.claude.com/docs/en/managed-settings]

```python {linenos=inline,hl_lines=[8,"22-28"]}
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

FAIL_CLOSED = (
    "allowedHttpHookUrls",
    "httpHookAllowedEnvVars",
    "allowedChannelPlugins",
)
candidates = [
    Path("/etc/claude-code/managed-settings.json"),
    Path("/Library/Application Support/ClaudeCode/managed-settings.json"),
]
path = Path(sys.argv[1]) if len(sys.argv) > 1 else next((p for p in candidates if p.exists()), None)
if path is None:
    print("NO_FILE")
    sys.exit(2)

raw = path.read_bytes()
print(f"path={path}")
print(f"bytes={len(raw)}")
try:
    data = json.loads(raw.decode("utf-8"))
except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
    print(f"UNREADABLE:{type(exc).__name__}:{exc}")
    print("CLASS=fail_closed_empty_allowlist")
    sys.exit(3)

if not isinstance(data, dict):
    print("UNREADABLE:top_level_not_object")
    print("CLASS=fail_closed_empty_allowlist")
    sys.exit(3)

for key in FAIL_CLOSED:
    if key not in data:
        print(f"{key}=unset")
        continue
    val = data[key]
    if not isinstance(val, list):
        print(f"{key}=invalid_type:{type(val).__name__}")
        print("CLASS=fail_closed_empty_allowlist")
        continue
    print(f"{key}=list_len_{len(val)}")
```

The script exits 2 when none of the official file paths exist, 3 when the bytes will not parse. Unreadable bytes are the new “admit nothing.” They are not “key missing, so allow all.”

I keep this next to the Laravel deploy notes on purpose. A PHP `config` cache that will not parse does not mean “no config, so public.” The 9 September bullet puts the same instinct on three managed keys. User settings files already rejected a broken file as a whole. Do not treat a managed parse miss as an unset key.

![Copy doctor, then the official file path, then the named owner](/img/treat-unreadable-managed-settings-as-empty-3.png)

## Do not delete the key to unblock

The other trap is the opposite of unreadable. The file parses. One URL pattern looks wrong. The junior deletes the whole `allowedHttpHookUrls` array “to unblock.”

The 9 September bullet names the **unreadable** case. It does not give you a license to unset a readable key. Unset is the “any URL” default in the settings reference. Deleting the key is how you open the list. Leave the readable list in place until the named owner edits the managed source. [Source: https://code.claude.com/docs/en/settings-reference] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.267]

Classify with a second script. Do not ask the agent to “clean the file.”

```python {linenos=inline,hl_lines=[14,"20-27"]}
#!/usr/bin/env python3
import json
import sys
from urllib.parse import urlparse

path = sys.argv[1]
data = json.loads(open(path, encoding="utf-8").read())
urls = data.get("allowedHttpHookUrls")
if urls is None:
    print("unset: any URL allowed at this file (other sources still merge)")
    sys.exit(0)
if urls == []:
    print("empty_array: every HTTP hook blocked by this file")
    sys.exit(2)
if not isinstance(urls, list):
    print("invalid_type: fail closed on managed source")
    sys.exit(3)

bad = []
for item in urls:
    if not isinstance(item, str) or not item:
        bad.append(repr(item))
        continue
    parsed = urlparse(item.replace("*", "x"))
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        bad.append(item)

print(f"count={len(urls)} bad={len(bad)}")
for item in bad:
    print(f"STRIP_CANDIDATE:{item}")
if bad:
    sys.exit(4)
```

This script does not claim Claude Code uses `urlparse`. It gives the named owner a list of strings a human can compare to the official pattern examples: `https://hooks.example.com/*` and `http://localhost:*`. Hostname matching is case-insensitive and treats a trailing DNS dot as the same host. [Source: https://code.claude.com/docs/en/settings-reference]

If the owner needs a bypass, that is a policy ticket. It is not a coding-agent ticket. I do not publish a recipe that widens the list.

{{< note type="danger" title="Empty array is a decision" >}}
An empty `allowedHttpHookUrls` array is a deliberate block of every HTTP hook. Unreadable managed bytes now land in the same place. Do not “fix” either case by deleting the key so the default (any URL) returns.
{{< /note >}}

## What the coding agent is allowed to do

The agent’s first idea is always the same: edit the nearest settings file until the hook fires. That is how you launder a managed fail-closed into a user fail-open.

Allowed:

1. Run `claude --version` and `claude doctor`.
2. Copy the three key names and the source file doctor printed.
3. Stop, and ping the named owner of the managed file.

Forbidden:

1. Write `allowedHttpHookUrls` in the project or user file to “match production.”
2. Unset the key because “empty is too strict.”
3. Retry the hook ten times and call the API dead. A different 9 September bullet fixed expired AWS or Google Cloud credentials under a host app that retried ten times with a generic “request failed.” That is a re-auth ticket, not this allow-list ticket. Keep them on separate cards. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.267]

I already refused to leave Copilot Approve on as a required check. The same instinct applies here. The model that wrote the PR does not own the fleet allow-list. See [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/) if your team still treats agent review as a merge gate. For the broader agent-ops habit, start at [/ai-agent-operations/](/ai-agent-operations/).

![Coding agent may copy doctor and must not widen the allow-list](/img/treat-unreadable-managed-settings-as-empty-4.png)

## Merge is not a reason to skip the owner

Arrays merge across settings files. That sentence is in the official `allowedHttpHookUrls` reference. Juniors hear “merge” and think a user file can punch a hole in a managed empty list.

Read the managed page with the settings-reference page together. HTTP hook allow-lists apply to hooks from every source. When the managed value is unreadable, the release notes say admit nothing. Repair the managed source doctor named. A user file that lists `https://hooks.example.com/*` is not the repair. [Source: https://code.claude.com/docs/en/settings-reference] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.267]

`allowManagedHooksOnly` is a different switch. When true, only managed hooks (plus SDK hooks and hooks from plugins force-enabled in managed `enabledPlugins`) run. User, project, and local hooks are blocked. That switch is managed-only. Do not diagnose a fail-closed allow-list as `allowManagedHooksOnly` unless doctor named that key. [Source: https://code.claude.com/docs/en/settings-reference]

I write the owner on the ticket as a person, not a role. “Platform” is how these files stay unreadable until Friday.

## What you should do Monday morning

1. Print `claude --version` on the machine that runs HTTP hooks. If it is older than the 9 September fail-closed patch, write the pin owner on the ticket. Do not treat npm `stable` 2.1.236 as the field.
2. Run `claude doctor`. Save the Organization policy line **and** any line that names `allowedHttpHookUrls`, `httpHookAllowedEnvVars`, or `allowedChannelPlugins`.
3. If doctor says the managed value is unreadable or invalid, classify the ticket as fail-closed empty allow-list. Stop the coding agent. Do not widen a user or project allow-list.
4. If the file parses, leave the list in the managed source. Do not delete the key. File the odd pattern with the owner.
5. Name one human who owns the managed-settings file (or the MDM/plist/remote source). Put that name on the wiki card next to the CLI pin.
6. Keep the why-line post and this post on separate cards. A proxy that drops the settings endpoint is a load miss. Unreadable bytes are a parse miss. Both can print the word “policy.” They are not the same repair.

The question is not whether this demos well in chat. The question is whether the allow-list survives maintenance, handoff, and a file that will not parse.

## Further reading

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.267" label="Claude Code v2.1.267 release notes (fail-closed allow-list bullet)" >}}

{{< source href="https://code.claude.com/docs/en/managed-settings" label="Deploy managed settings — keys that fail closed" >}}

{{< source href="https://code.claude.com/docs/en/settings-reference" label="allowedHttpHookUrls and httpHookAllowedEnvVars reference" >}}
