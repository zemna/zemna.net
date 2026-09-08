---
title: "Read the Why-Line Before You Trust the Org Policy"
date: 2026-09-08T07:00:00+07:00
draft: false
slug: "org-policy-why-line"
description: "An Organization policy line on /status can explain a miss. It does not prove the fleet policy loaded. Read claude doctor, name the proxy owner, then resume coding."
topics: ["ai-agents"]
tags: ["claude-code", "managed-settings", "org-policy", "proxy", "coding-agents", "change-control"]
cover: /covers/org-policy-why-line.png
seo:
  primaryQuery: "Claude Code organization policy line not loaded"
  secondaryQueries:
    - "claude doctor organization policy proxy"
    - "Claude Code /status policy could not be loaded"
    - "named owner corporate proxy Claude Code managed settings"
---

Standup hears “org policy is on.” Someone pasted a screenshot of `/status`. There is a line that says Organization policy. The junior treats that line as a green light and keeps prompting.

I stop the run there. A line that explains a miss is not a loaded policy. A proxy that drops the settings endpoint will still print a reason. The reason is useful. The reason is not enforcement.

On 4 September 2026 Claude Code added an Organization policy line to `/status` and `claude doctor`. Official notes say the line reports **why** the organization’s policy could not be loaded, for example a proxy not passing the endpoint through. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.261] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a deferred group name as a PHP helper in [A Deferred Group Name Is Not a Helper](/blog/deferred-group-name-is-not-a-helper/). I already refused to treat a missing Issues tab as a missing ticket in [An Issues Tab Is Not a Laravel Package Ticket](/blog/issues-tab-is-not-a-package-ticket/). This post is the same desk rule for fleet policy. Read the why-line. Name who owns the proxy and the allow-list. Do not resume a coding agent until that owner answers.

The question is not whether the CLI printed a new label. The question is whether the machine you are about to trust actually loaded the policy your admin thinks is in force.

<!--more-->

![Read the why-line: status line, claude doctor, named proxy owner](/img/org-policy-why-line-1.png)

## The screenshot that looks like a green light

Juniors read `/status` the way they read a CI badge. A new heading appears. It contains the word policy. They assume the org rules landed.

Official admin docs split the screenshot into two jobs. `/status` has a Setting sources line that names the managed source Claude Code selected: remote, plist, file, drop-ins, or a merged list. `claude doctor` lists what it dropped. To check whether organization settings reached a given machine, read the Organization policy line on `claude doctor`. That line says **where** Claude Code loaded the policy from, or **why** it did not load. The same Organization policy line shows up in a running session on `/status` when the policy did not load. The docs pin that behavior to Claude Code 2.1.261 or later. [Source: https://code.claude.com/docs/en/managed-settings]

Two different sentences live in one label:

1. Loaded from X. The fleet file, the admin console, or the gateway actually arrived.
2. Did not load, because Y. The machine never received the policy. Y is a diagnosis, not a pass.

If you only read the heading, you will ship under the second sentence while standup still quotes the first.

{{< note type="warning" title="A why-line is a ticket, not a pass" >}}
If `/status` or `claude doctor` explains a miss, stop the coding-agent session. File the network path. Do not “try one more prompt” on a machine that never received the fleet rules.
{{< /note >}}

Managed settings sit above user, project, local, and `--settings` values, with a short list of security-sensitive exceptions. That precedence only matters after the file or the server fetch actually arrives. [Source: https://code.claude.com/docs/en/managed-settings]

## What loaded looks like, and what a miss looks like

I do not invent a fake incident. I use the public contract.

The GitHub release for 2.1.261, published 4 September 2026 at 19:58 UTC, is not a prerelease. The first bullet is the why-line. Example given in that bullet: a proxy not passing the endpoint through. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.261]

The docs page that administrators actually use adds the positive case. The line can also say where the policy loaded from. Remote Control and web-session org settings are the same check: `claude doctor` on that machine. [Source: https://code.claude.com/docs/en/managed-settings]

Server-managed settings are a sibling check, not the same sentence. `claude doctor` has a Managed settings (remote) line from 2.1.248 onward. That line reports one of four outcomes: the delivered settings loaded; the organization has no server-managed settings; the fetch failed, with the cause and whether a cached policy still applies; or Claude Code skipped the fetch, with the reason. While the fetch is still in progress, the line reports that instead. [Source: https://code.claude.com/docs/en/server-managed-settings]

Keep the two lines separate in the ticket:

| What you opened | Line to read | Pass | Miss |
| --- | --- | --- | --- |
| `/status` | Setting sources | Lists Enterprise managed settings and the source in parentheses | Line missing: no managed source delivered a policy key |
| `claude doctor` | Organization policy | Says where it loaded from | Says why it did not load |
| `/status` in a live session | Organization policy | Loaded, or absent when the policy loaded | Shows the same why-line when the policy did not load |
| `claude doctor` | Managed settings (remote) | Delivered settings loaded | Fetch failed, skipped, in progress, or none configured |

Do not paste one screenshot and call the row done. Read the words after the label.

{{< details summary="npm tags are evidence, not the hook" >}}
This morning’s registry, 8 September 2026: `@anthropic-ai/claude-code` `latest` and `next` are 2.1.263 (published 6 September 2026). `stable` is still 2.1.236. Changelog for 2.1.263 is bug fixes and reliability. The why-line itself landed in 2.1.261. Pin what you run. Do not treat `latest` as `stable`. Do not put those numbers in the title. [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code] [Source: https://code.claude.com/docs/en/changelog]
{{< /details >}}

## The proxy miss that looks like a settings debate

Corporate desks lose hours here. Security says the proxy is “transparent.” The developer says Claude Code “has a policy bug.” Both are guessing.

Claude Code respects standard proxy environment variables: `HTTPS_PROXY` (recommended), `HTTP_PROXY`, and `NO_PROXY`. Lowercase variants also work. The first one set wins in this order: `https_proxy`, `HTTPS_PROXY`, `http_proxy`, `HTTP_PROXY`. Variables exported in the shell are read once at startup. A running session does not pick up a later export. [Source: https://code.claude.com/docs/en/network-config]

Claude Code does not support SOCKS proxies. If the desk “proxy” is SOCKS-only, the why-line will keep firing until someone puts an HTTP/HTTPS proxy in front or allowlists the hosts the CLI actually needs. Official network docs start that list with `api.anthropic.com`. Put that host on the ticket, not a vibe. [Source: https://code.claude.com/docs/en/network-config]

If the settings endpoint never leaves the building, `/status` can still print a why-line. That is the point of the 2.1.261 change. The CLI stopped failing silently. It started naming the miss.

The named owner is not “the intern who runs Claude.” The named owner is the person who can change the proxy allow-list or the PAC file. Until that person says the Anthropic settings endpoint is passed through, you do not have a loaded policy. You have a diagnosis.

I already treat repository instruction files as change control in [A Coding-Agent Policy Is Change Control, Not a Settings File](/blog/coding-agent-policy-change-control/). Fleet managed settings are the same class of object, delivered by a different pipe. A local `CLAUDE.md` cannot paper over a proxy that drops the admin fetch.

![Proxy miss: laptop, proxy wall, settings endpoint, why-line is a ticket](/img/org-policy-why-line-2.png)

## How I read the machine before I let the agent touch Laravel

On a Modoo Laravel SaaS checkout I will not let a coding agent rewrite billing or a Vue form until I know which rules the machine is under. The check is boring. That is why it works.

```bash
claude --version
claude doctor
```

I copy the Organization policy line into the ticket. If the line explains a miss, I copy the Managed settings (remote) line as well. Then I print the proxy the process will actually see:

```bash
printf 'https_proxy=%s\nHTTPS_PROXY=%s\nhttp_proxy=%s\nHTTP_PROXY=%s\nNO_PROXY=%s\n' \
  "${https_proxy-}" "${HTTPS_PROXY-}" "${http_proxy-}" "${HTTP_PROXY-}" "${NO_PROXY-}"
```

A desktop app session does not always share your shell. Official network docs say that in Claude Desktop sessions where the app manages the provider connection, Claude Code reads proxy values from managed settings and `~/.claude/settings.json`. If the miss is on Desktop, the shell export you just printed is not the evidence. [Source: https://code.claude.com/docs/en/network-config]

Then I write three names, not three theories:

1. Who owns the proxy allow-list.
2. Who owns the managed-settings file or the admin-console policy.
3. Who is allowed to resume the coding-agent session after those two say yes.

If any name is empty, the agent stays parked.

Background agents do not inherit “the shell I have open now.” Official network docs say a per-user supervisor starts on demand, outlives the terminal, and hosts `claude agents`, `--bg`, and `/background`. That supervisor keeps the environment of whichever shell started it first. A proxy export in a later window never reaches it. Put `HTTPS_PROXY` in `~/.claude/settings.json` or managed settings if background sessions must see the same path. After you change that, run `claude daemon stop --any` so the next background job starts a supervisor that honors it. [Source: https://code.claude.com/docs/en/network-config]

{{< field-note title="Field note" >}}
On a Laravel and Vue maintenance desk the blast radius is a form that looks done while org deny-rules never arrived. A Modoo Laravel SaaS pull request that “passes locally” under a missed fetch is not a local win. It is an ungoverned edit. I already refuse Copilot’s ready-to-approve line as a merge vote in [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/). I refuse a why-line as a loaded policy for the same reason: fluency is not enforcement.
{{< /field-note >}}

## The ticket I file instead of another prompt

Do not paste a novel. Paste a contract.

```md
# Org policy miss

- Machine: (hostname)
- CLI: (output of `claude --version`)
- Organization policy line: (verbatim)
- Managed settings (remote) line: (verbatim, if present)
- Proxy vars at process start: (verbatim)
- Desktop or terminal: (one word)
- Endpoint the proxy must pass: (from the admin who owns the policy)
- Owner of the allow-list: (name)
- Owner of the fleet policy: (name)
- Resume coding-agent?: no until both owners reply
```

That ticket is the artifact. Chat saying “should be fine now” is not the artifact. I already wrote that a green cron exit is not a finished job. Same shape. Different pipe. See the operating notes on [AI agent operations](/ai-agent-operations/).

Server-managed settings fetch at startup and refresh hourly during the session. A miss at 08:05 can still be a miss at 08:40. Do not “wait for the next prompt” as a retry policy. Re-run `claude doctor` after the network owner changes the allow-list, then paste the new line. [Source: https://code.claude.com/docs/en/admin-setup]

{{< note type="note" title="Cached policy is a separate sentence" >}}
The remote-settings line can say the fetch failed **and** a cached policy still applies. That is not “ignore the miss.” It is “you are running yesterday’s file.” Name the cache age in the ticket. Decide whether yesterday’s file is still the policy you think you shipped.
{{< /note >}}

## What I refuse on this desk

I refuse four cheap moves.

**Bump the CLI and call it done.** Installing 2.1.263 does not open a proxy hole. 2.1.263 is bug fixes. The why-line already exists from 2.1.261. A bump can make the diagnosis readable. It cannot load a policy the network still blocks. [Source: https://code.claude.com/docs/en/changelog]

**Treat `latest` as `stable`.** This morning `stable` is 2.1.236. `latest` is 2.1.263. If the fleet pins `stable`, a developer on `latest` is not on the fleet pin. Say that in the ticket. Do not hide it in a version table in the title. [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]

**Let the coding agent “fix” the proxy.** An agent that can edit your shell rc is not the allow-list owner. A local `NO_PROXY=*` that “makes Claude work” is a bypass, not a load. Network docs even document `NO_PROXY="*"` as bypass-all. That is a decision for the named owner, not a silent export in a pull request. [Source: https://code.claude.com/docs/en/network-config]

**Buy a new plan because the line looks empty.** A miss can be a proxy. A miss can be “your organization has no server-managed settings configured.” Neither sentence is a checkout page. I do not recommend a purchase from a status line.

![Four refusals: bump CLI, latest as stable, agent edits NO_PROXY, buy a plan](/img/org-policy-why-line-3.png)

## A small gate you can run in CI without pretending CI is the fleet

CI cannot prove a developer laptop loaded org policy. CI can refuse to merge a “I exported NO_PROXY=*” “fix.”

```yaml
name: refuse-proxy-bypass-in-dotfiles
on:
  pull_request:
    paths:
      - ".bashrc"
      - ".zshrc"
      - ".profile"
      - "**/.env"
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Reject NO_PROXY star in tracked shells
        run: |
          if git grep -n 'NO_PROXY="\\*"' -- .bashrc .zshrc .profile ':*.env' ; then
            echo "NO_PROXY=* is a fleet decision, not a PR."
            exit 1
          fi
```

That gate is narrow on purpose. It does not claim GitHub Actions loaded your org policy. It claims the repository will not absorb a bypass disguised as a developer convenience.

For the laptop itself, keep the check human and short:

```bash
line=$(claude doctor 2>/dev/null | sed -n '/Organization policy/p')
printf '%s\n' "$line"
case "$line" in
  *"could not be loaded"*|*"not load"*|*"proxy"*)
    echo "STOP: why-line is a miss. File the network ticket."
    exit 2
    ;;
esac
```

Tune the `case` to the verbatim words on your build. Do not invent a regex for a sentence you have not seen on that machine. The public example is “proxy not passing the endpoint through.” Copy the real line first. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.261]

## How this fits the rest of the desk

A coding agent that never received deny-rules will still write fluent PHP. Fluent PHP is how we get a Vue form that posts to a route the org meant to block, or a Composer script the fleet meant to deny.

I keep the same sequence I use for other agent work. Map the repo. Name the owner. Require an artifact. Then type. The map post is still [Your Coding Agent Needs a Map, Not a Bigger Context Window — Part 2](/blog/your-coding-agent-needs-a-map-not-a-bigger-context-window-part-2/). The merge refusal is still [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/). The start path for new readers is [/start-here/](/start-here/).

If the Organization policy line says where the policy loaded from, resume. If it says why it did not load, you are not in a prompt problem. You are in a network ticket. The agent waits.

![Resume or wait: loaded from X resume agent, or why it missed file ticket](/img/org-policy-why-line-4.png)

## What you should do Monday morning

1. Run `claude --version` and `claude doctor` on the machine you actually use for Laravel work, not on a spare VM.
2. Copy the Organization policy line verbatim into a note. If a Managed settings (remote) line exists, copy that too.
3. If either line explains a miss, stop the coding-agent session. Do not start a “quick” refactor while you wait.
4. Print `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY` from the same process family (terminal vs Desktop).
5. Name two humans: allow-list owner, fleet-policy owner. Put both names in the ticket.
6. After the allow-list changes, re-run `claude doctor`. Paste the new line. Only then resume the agent.
7. Pin the CLI the fleet agreed to. Do not silently ride `latest` if the fleet is on `stable`.
8. Refuse a pull request that “fixes Claude” by setting `NO_PROXY=*`.

## Further reading

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.261" label="Claude Code 2.1.261: Organization policy why-line on /status and claude doctor" >}}

{{< source href="https://code.claude.com/docs/en/managed-settings" label="Official managed settings: how to check that a policy is in force" >}}

{{< source href="https://code.claude.com/docs/en/network-config" label="Official network config: HTTPS_PROXY, HTTP_PROXY, NO_PROXY" >}}
