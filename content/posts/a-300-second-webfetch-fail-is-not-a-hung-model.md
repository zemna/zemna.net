---
title: "A 300-Second WebFetch Fail Is Not a Hung Model"
date: 2026-09-16T07:00:00+07:00
draft: false
slug: "a-300-second-webfetch-fail-is-not-a-hung-model"
description: "A red WebFetch at five minutes is a download deadline, not a stuck model. Print the named CLI pin, the deadline env, and the named owner before you page the model."
topics: ["tutorials"]
tags: ["claude-code", "webfetch", "coding-agents", "timeouts", "change-control"]
cover: /covers/a-300-second-webfetch-fail-is-not-a-hung-model.png
seo:
  primaryQuery: "Claude Code WebFetch 300 seconds not a hung model"
  secondaryQueries:
    - "WebFetch hang not a hung model"
    - "CLAUDE_CODE_WEBFETCH_DEADLINE_MS"
    - "Claude Code fetch timeout 300 seconds"
---

Standup hears “the model hung.” Someone pasted a terminal. The line sat on Fetching. Five minutes later it went red. The junior files a model-outage ticket. They ping the vendor channel. They tell chat to wait for a new brain.

I stop the run there. A red WebFetch at five minutes is not a hung model. Official notes from 10 September 2026 name the field: WebFetch used to hang indefinitely on a server that keeps the response open without finishing. A fetch now fails after 300 seconds. The env that overrides that deadline is `CLAUDE_CODE_WEBFETCH_DEADLINE_MS`. Zero turns the limit off. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.268] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a wait line as a finished background agent in [Waiting for Your Input Is Not a Finished Background Agent](/blog/waiting-for-input-is-not-finished/). I already refused to treat an every-turn HTTP 400 as a dead gateway in [Every-Turn HTTP 400 on ANTHROPIC_BASE_URL Is Not a Dead Gateway](/blog/every-turn-http-400-is-not-a-dead-gateway/). This post is the same desk rule for a fetch that never closed. Print the pin. Print the deadline. Name who owns both.

The question is not whether chat looks stuck. The question is whether the named owner can still tell a download deadline from a model that stopped producing tokens.

<!--more-->

![Three columns: spinner, red deadline, hung model — a 300s fail is not a hung model](/img/a-300-second-webfetch-fail-is-not-a-hung-model-1.png)

## The fetch that used to never end

Juniors read a long Fetching line the way they read a frozen IDE. The spinner is still moving. Chat is quiet. They assume the model is thinking.

WebFetch is not the model. Official tool notes and the public GitHub issue trail already said the old shape: a slow, open, or anti-bot host could hold the HTTP connection. The session sat on the tool. The model was waiting for the tool result, so it could not skip, retry, or move. The only exit was a human interrupt. [Source: https://github.com/anthropics/claude-code/issues/24684]

That is an open socket. It is not “Claude stopped thinking.”

The 10 September 2026 GitHub release, published 20:30 UTC, not a prerelease, names the fix in one bullet: WebFetch hanging indefinitely on a server that keeps the response open without finishing; a fetch now fails after 300 seconds. Set `CLAUDE_CODE_WEBFETCH_DEADLINE_MS` to override the deadline. Zero turns it off. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.268]

Official env docs say the same number in milliseconds. `CLAUDE_CODE_WEBFETCH_DEADLINE_MS` is the upper bound on how long WebFetch waits for a page to download, including redirects it follows. A download that has not completed by then fails with a deadline error. The default is `300000`, which is five minutes. Set to `0` to remove the limit. The value takes plain digits only. A decimal or any other spelling keeps the default. The docs require a CLI at or past the 10 September pin. [Source: https://code.claude.com/docs/en/env-vars]

If the line goes red at five minutes and the body names a deadline, you do not have a hung model. You have a download that did not finish.

{{< note type="warning" title="Do not page the model on a five-minute fetch fail" >}}
If WebFetch goes red at about 300 seconds, copy the error, print `claude --version`, and print `CLAUDE_CODE_WEBFETCH_DEADLINE_MS` before you open a model-outage ticket. A deadline is not a brain that stopped.
{{< /note >}}

I do not invent a fake overnight hang. I use the public contract. The old issue asked for a timeout parameter because Bash already had one and WebFetch did not. The later pin ships a default deadline. The host that never closed is still a host problem. The model is not the owner of that socket. [Source: https://github.com/anthropics/claude-code/issues/24684]

## Three tickets, one owner

Laravel and Vue work on this desk still runs coding agents next to cron: a CLI that fetches docs, a headless `-p` job that reads a changelog, a junior who sees Fetching for five minutes and pages the wrong channel. Mixing “download deadline,” “needs input,” and “model stream died” into one “AI is hung” thread is how a junior burns an hour of model people on a URL they do not own.

| Ticket | What it means | What you do | Owner |
| --- | --- | --- | --- |
| WebFetch red at ~300s, body names deadline | The download did not finish in the named bound | Copy the error. Print the pin and the env. Do not page the model | Named human who pinned the CLI and the deadline |
| Needs input / Waiting for your input | The child is blocked on a human | Answer it or name who will. Do not call it hung | Named human who owns the session |
| Stream quiet, no tool in flight | Then it is a model or network stream ticket | Use the stream-watchdog path, not the fetch path | Named human who owns the model route |

Do not paste one red screenshot and call the brain dead. If the body names a WebFetch deadline, you are on a fetch ticket. If the row is Needs input, you are on a human ticket. If no tool is running and the stream is quiet, you are on a stream ticket. See [Waiting for Your Input Is Not a Finished Background Agent](/blog/waiting-for-input-is-not-finished/) for the sibling habit: a wait line is not recovered, and a five-minute fetch fail is not a hung model.

{{< details summary="Pins are evidence, not the hook" >}}
The WebFetch deadline landed in the 10 September 2026 GitHub release, published 20:30 UTC, not a prerelease. This morning’s npm registry, 16 September 2026: `@anthropic-ai/claude-code` `latest` and `next` are 2.1.273. `stable` is 2.1.267. The fetch field still lands in the 10 September pin. Pin what you run. Do not treat `latest` as `stable`. Do not put those numbers in the title. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.268] [Source: https://code.claude.com/docs/en/changelog] [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous host is ordinary: a coding agent that fetches a vendor doc, a junior who has never printed `claude --version`, and a Slack thread titled “the model hung.” I treat `CLAUDE_CODE_WEBFETCH_DEADLINE_MS` as a named owner’s artifact, the same way I treat a `.env` key. The person who owns [/ai-agent-operations/](/ai-agent-operations/) on this desk also owns “which host loaded which deadline.” A coding agent does not get to hide an open socket so standup looks like a model outage. I already wrote the sibling rule for a wait line that is not a finished child, and for a 400 wall that is not a dead gateway. This is the sibling for a five-minute fetch fail that is not a hung model.
{{< /field-note >}}

![Three tickets: fetch deadline, needs input, stream quiet](/img/a-300-second-webfetch-fail-is-not-a-hung-model-2.png)

## What the deadline actually measures

I do not invent a fake dashboard. I use the public variables.

Official env docs split two WebFetch knobs. Do not mix them.

1. `CLAUDE_CODE_WEBFETCH_DEADLINE_MS` — how long the download is allowed to run, including redirects. Default `300000`. Zero removes the limit. Plain digits only. Read once per launch. A change in a settings `env` block applies on the next `claude` start. Requires the 10 September pin or later. [Source: https://code.claude.com/docs/en/env-vars]
2. `CLAUDE_CODE_WEBFETCH_CACHE_TTL_MS` — how long WebFetch keeps each fetched URL’s response cached. Default `900000`, which is 15 minutes. Zero, a decimal, or any other spelling keeps the default. Also read once per launch. Docs name this from an earlier 2.1 pin. [Source: https://code.claude.com/docs/en/env-vars]

A cache hit is not a deadline. A deadline is not a cache. If a junior “fixed” a hang by clearing cache, they did not name the socket.

Official network docs name a different family of timers for the **model stream**: first-byte, event-level, and byte-level watchdogs that abort a quiet streaming response so a dead connection fails instead of hanging. Those timers are not WebFetch. Do not file a stream-watchdog ticket from a Fetching line. [Source: https://code.claude.com/docs/en/network-config]

{{< note type="note" title="Five minutes is the download, not the model" >}}
Default WebFetch deadline is 300000 ms. Default stream watchdogs live on the model connection. Print which clock you are on before you name the owner.
{{< /note >}}

The old public issue already split the pipeline: domain check, HTTP fetch, HTML to Markdown, then a secondary summarizer. The hang that froze a session sat on the fetch that never closed, or on a later step with no total deadline. The 10 September bullet is the download bound. It is not permission to skip the named pin. [Source: https://github.com/anthropics/claude-code/issues/24684] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.268]

If the host you fetch is your own docs, own the host. If the host is a vendor that holds the connection open, skip it and use a source you control. Do not set the deadline to zero so the spinner can sit until lunch.

## Print the pin and the deadline on the ticket

A wiki card that says “we use Claude Code” is not an owner. Print the strings the host actually loaded.

```bash {linenos=inline,hl_lines=[6,"8-10"]}
#!/usr/bin/env bash
set -euo pipefail

: "${DEADLINE_OWNER:?set DEADLINE_OWNER to one person, not a role}"

echo "host=$(hostname)"
echo "owner=${DEADLINE_OWNER}"
echo "claude=$(claude --version)"
echo "deadline_ms=${CLAUDE_CODE_WEBFETCH_DEADLINE_MS:-300000}"
echo "cache_ttl_ms=${CLAUDE_CODE_WEBFETCH_CACHE_TTL_MS:-900000}"
```

Run that on the host the team actually uses, not on your laptop. A dock-launched editor does not inherit a shell export from a different tty. Official env docs already say a settings `env` block is the durable place, and that Claude Code reads these values once per launch. [Source: https://code.claude.com/docs/en/env-vars]

Paste the four lines under the red WebFetch body. If `deadline_ms` is `0`, the named owner turned the bound off. That is a policy ticket, not a model ticket. If `deadline_ms` is `300000` and the fail landed at five minutes, the default bound did its job.

Do not “fix” the ticket by exporting `CLAUDE_CODE_WEBFETCH_DEADLINE_MS=0` in the same shell so the next fetch can sit open. Official docs document zero as remove-the-limit. I treat that as a named exception with a named owner, not a hangover cure. [Source: https://code.claude.com/docs/en/env-vars]

## Classify the line before you page anyone

I keep a boring classifier next to the print script. The value is the ticket field.

```python {linenos=inline,hl_lines=[14,18,22]}
from dataclasses import dataclass

DEADLINE_MS_DEFAULT = 300_000


@dataclass(frozen=True)
class Ticket:
    kind: str
    owner: str


def classify(line: str) -> Ticket:
    text = line.lower()
    if "webfetch" in text and ("deadline" in text or "300" in text):
        return Ticket("fetch-deadline", "cli-pin-owner")
    if "needs input" in text or "waiting for your input" in text:
        return Ticket("needs-input", "session-owner")
    if "http 400" in text:
        return Ticket("schema-or-request", "cli-pin-owner")
    if "fetching" in text and ("indefinitely" in text or "hung" in text):
        return Ticket("open-socket-hang", "cli-pin-owner")
    return Ticket("unknown", "cli-pin-owner")


if __name__ == "__main__":
    sample = "WebFetch failed after deadline (300 seconds)"
    ticket = classify(sample)
    print(f"{ticket.kind}\t{ticket.owner}")
```

If `ticket=fetch-deadline`, you stay on the CLI-pin owner. If `ticket=needs-input`, you stay on the session owner. If `ticket=schema-or-request`, you are on yesterday’s 400 wall, not this post. If `ticket=open-socket-hang` on a pin from before 10 September, the owner bumps the pin. You still do not have a hung model.

Parse the env the same way the docs describe it: plain digits, or keep the default.

```python {linenos=inline,hl_lines=[8,11]}
DEFAULT_DEADLINE_MS = 300_000


def parse_deadline_ms(raw: str | None) -> int:
    if raw is None or raw == "":
        return DEFAULT_DEADLINE_MS
    if not raw.isdigit():
        return DEFAULT_DEADLINE_MS
    return int(raw)


assert parse_deadline_ms(None) == 300_000
assert parse_deadline_ms("") == 300_000
assert parse_deadline_ms("300000") == 300_000
assert parse_deadline_ms("0") == 0
assert parse_deadline_ms("300000.0") == 300_000
assert parse_deadline_ms("off") == 300_000
```

Official docs say a decimal or any other spelling keeps the default. The tests above lock that contract so a junior cannot “set five minutes” with `300000.0` and think they changed anything. [Source: https://code.claude.com/docs/en/env-vars]

I keep that script boring on purpose. The value is the ticket field, not a new platform.

![Fetching to 300s to red deadline is not a hung model](/img/a-300-second-webfetch-fail-is-not-a-hung-model-3.png)

## What you must not do

Forbidden:

1. File a model-outage ticket from a five-minute WebFetch fail without printing `claude --version` and the deadline env.
2. Treat npm `latest` as the pin the host is running. Print `claude --version` on the host.
3. Mix this field with an every-turn HTTP 400, or with a wait line, or with a stream watchdog. Those are other posts.
4. Set `CLAUDE_CODE_WEBFETCH_DEADLINE_MS=0` so the old open-socket hang comes back. Official notes name zero as off. I do not put that on a wiki card as a “keep fetching” trick. A lying spinner is worse than a noisy deadline.
5. Replace WebFetch with an undocumented curl wrapper in the daily agent path because a junior wanted “no red.” Curl is a debug probe. It is not the named fetch tool.

Allowed:

1. Print `claude --version` on the ticket.
2. Print `CLAUDE_CODE_WEBFETCH_DEADLINE_MS` or the default `300000`.
3. Copy the WebFetch error body.
4. Stop, and ping the named owner of the CLI pin and the deadline.
5. Skip the URL. Use a source you control. Name the skip on the ticket.

I already refused to leave an org-policy why-line unread. Same instinct: a status sentence is a ticket, not a pass. See [Read the Why-Line Before You Trust the Org Policy](/blog/org-policy-why-line/).

## This is not Monday’s 400 wall

Monday’s post is a schema reject on a named `ANTHROPIC_BASE_URL`. The host answered. The request was illegal for that endpoint. [Source: https://zemna.net/blog/every-turn-http-400-is-not-a-dead-gateway/]

This post is a download that did not finish. The tool waited. The bound fired. The model was not the thing that timed out.

Do not merge the two into “Claude is broken.” A 400 wall still answers curl. A 300-second WebFetch fail still proves the CLI is alive enough to enforce a deadline. Both need a named pin. They do not share a vendor-down channel.

GSC this week still has no striking-distance query on those URLs. I am not refreshing the 400 post, the wait-line post, or the long-running agents page. This is a new field, not a synonym of Monday’s slug.

## Merge is not a reason to skip the owner

Fetch tools are cheap to leave on. They are not cheap to own.

Juniors hear “the agent can read the web” and think the host can run without a name on the wiki card. Then Friday arrives and nobody knows which box still exports `DEADLINE_MS=0` from a debug session.

I write the owner as a person, not a role. “Platform” is how these hosts stay half-watched until a spinner ships as a hung model.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tool pins live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/) when the agent is touching that stack. A first-week map is at [/start-here/](/start-here/). Do not mix those hubs into the WebFetch row.

I already refused to treat a green package bump as ownership of the next repair. Same here. A changelog bullet about a 300-second fail is not permission to skip `claude --version`.

![Ticket checklist: version, deadline env, error body, named human](/img/a-300-second-webfetch-fail-is-not-a-hung-model-4.png)

## What you should do Monday morning

1. Open the host the team actually uses for Claude Code. Run `claude --version`. Write the string on the ticket next to one human name. That person owns the CLI pin.
2. Print `CLAUDE_CODE_WEBFETCH_DEADLINE_MS`. If it is unset, write `300000` as the default. If it is `0`, name who turned the bound off and why. Do not leave zero as a tribal secret.
3. Trigger one WebFetch against a URL you control that answers in under a second. Confirm the happy path still works on this pin.
4. If a real fetch goes red at about five minutes, paste the error under the version and the env. Classify it: fetch-deadline, needs-input, schema-or-request, or open-socket-hang. Do not file a model-outage ticket for fetch-deadline.
5. Confirm background agents read the same `env` block. A shell export in one terminal does not own the supervisor. Official docs say these values are read once per launch. Write that on the ticket.
6. If the named pin is older than the 10 September deadline, the owner bumps the pin. If the named pin is already past that fix and WebFetch still never returns, you have a new ticket: this body, this URL, this pin. You still do not have a hung model until a tool-free stream is also quiet.

The question is not whether this demos well in chat. The question is whether the five-minute fail survives maintenance, handoff, and a junior who wants to page the brain.

## Further reading

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.268" label="GitHub release — WebFetch fails after 300 seconds (10 September 2026)" >}}

{{< source href="https://code.claude.com/docs/en/env-vars" label="Claude Code docs — CLAUDE_CODE_WEBFETCH_DEADLINE_MS default 300000" >}}

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code docs — changelog, 10 September 2026 WebFetch deadline" >}}
