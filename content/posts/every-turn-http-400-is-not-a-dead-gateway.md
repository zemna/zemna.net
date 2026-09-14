---
title: "Every-Turn HTTP 400 on ANTHROPIC_BASE_URL Is Not a Dead Gateway"
date: 2026-09-14T07:00:00+07:00
draft: false
slug: "every-turn-http-400-is-not-a-dead-gateway"
description: "A wall of HTTP 400s on a named Claude Code base URL is a schema reject, not a status outage. Print the 400 body, the named URL, and the named CLI pin before you page the gateway."
topics: ["devops"]
tags: ["claude-code", "anthropic-base-url", "llm-gateway", "http-400", "coding-agents", "change-control"]
cover: /covers/every-turn-http-400-is-not-a-dead-gateway.png
seo:
  primaryQuery: "Claude Code HTTP 400 ANTHROPIC_BASE_URL not a dead gateway"
  secondaryQueries:
    - "Claude Code every turn HTTP 400 third-party endpoint"
    - "ANTHROPIC_BASE_URL schema reject vs gateway down"
    - "who owns Claude Code base URL and CLI pin"
---

Standup hears “the gateway is down.” Someone pasted a terminal. Every turn is HTTP 400. The junior files a status ticket. They ping the network channel. They tell chat to wait for the vendor.

I stop the run there. A wall of 400s on a named `ANTHROPIC_BASE_URL` is not a dead gateway. Official notes from 10 September 2026 name the field: every turn failed with HTTP 400 on third-party Anthropic-compatible endpoints since a mid-week CLI pin, because those endpoints rejected a regex in the Artifact tool’s input schema. The later pin fixes the schema. The host was answering. The request was illegal for that endpoint. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.268] [Source: https://code.claude.com/docs/en/changelog]

I already refused to treat a wait line as a finished background agent in [Waiting for Your Input Is Not a Finished Background Agent](/blog/waiting-for-input-is-not-finished/). I already refused to treat a Node API miss as a new module registry in [Node.js APIs On Is Not the New Module Registry](/blog/nodejs-apis-on-is-not-the-new-module-registry/). This post is the same desk rule for a 400 wall. Print the body. Print the named base URL. Name who owns the CLI pin.

The question is not whether chat looks red. The question is whether the named owner can still tell a schema reject from a host that does not answer.

<!--more-->

![Schema reject, not an outage: HTTP 400 tickets beside a host that still answers](/img/every-turn-http-400-is-not-a-dead-gateway-1.png)

## The wall of 400s that looks like an outage

Juniors read HTTP 400 the way they read a red CI badge. The number is angry. Every turn fails. The session cannot move. They assume the pipe is dead.

HTTP 400 is a client error. The server received the request and refused it. That is the opposite of “nothing is listening.”

Official gateway docs already split the tickets. A one-token `curl` to `$ANTHROPIC_BASE_URL/v1/messages` that returns JSON starting with `{"id":"msg_` proves the URL and credential work. An error that names an unknown model still proves the same thing: the gateway authenticated the request before it rejected the model name. A `401` means the credential was rejected. Connection refused or `ENOTFOUND` means nothing answered at the address. [Source: https://code.claude.com/docs/en/llm-gateway-connect]

If every Claude Code turn is 400, and the same host still answers that one-token request, you do not have an outage. You have a request the endpoint will not accept.

{{< note type="warning" title="Do not page the gateway on a 400 wall" >}}
If every turn is HTTP 400 on a named `ANTHROPIC_BASE_URL`, copy the 400 body, print the named URL from `/status`, and print `claude --version` before you open a status ticket. A host that answers curl is not down.
{{< /note >}}

I do not invent a fake overnight outage. I use the public contract. The 10 September 2026 GitHub release names the old lie in one bullet: every turn failing with HTTP 400 on third-party Anthropic-compatible endpoints (`ANTHROPIC_BASE_URL`) since 2.1.265, from a regex in the Artifact tool’s input schema that those endpoints reject. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.268]

That is a schema fight. It is not “the gateway went dark.”

## Three tickets, one owner

Laravel and Vue work on this desk still runs coding agents next to cron: a CLI pointed at an organization gateway, a headless `-p` job in CI, a junior who sees a wall of 400s and pages the wrong channel. Mixing “schema reject,” “wrong credential,” and “host unreachable” into one “the gateway is down” thread is how a junior burns an hour of network people on a pin they do not own.

| Ticket | What it means | What you do | Owner |
| --- | --- | --- | --- |
| Every-turn HTTP 400, host still answers curl | The endpoint refused the request body or tool schema | Copy the 400 body. Name the CLI pin. Do not page down | Named human who pinned the CLI |
| HTTP 401 | The credential header is wrong or rejected | Switch the documented header variable. Re-run the one-token curl | Named human who owns the gateway credential |
| Connection refused / ENOTFOUND | Nothing answers at the address | Then it is a status path | Named human who owns the host and DNS |

Do not paste one red screenshot and call the vendor dead. If the body names an invalid request, you are on a schema ticket. If the body is 401, you are on a credential ticket. If nothing answers, you are on a status ticket. See [Treat Unreadable Managed Settings as Empty](/blog/treat-unreadable-managed-settings-as-empty/) for the sibling habit: an unread setting is not a company lockdown, and a 400 wall is not a downed host.

{{< details summary="Pins are evidence, not the hook" >}}
The HTTP 400 schema fix landed in the 10 September 2026 GitHub release, published 20:30 UTC, not a prerelease. This morning’s npm registry, 14 September 2026: `@anthropic-ai/claude-code` `latest` and `next` are 2.1.270 (published 12 September 2026). `stable` is still 2.1.236. The 400 field still lands in the 10 September pin. Pin what you run. Do not treat `latest` as `stable`. Do not put those numbers in the title. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.268] [Source: https://code.claude.com/docs/en/changelog] [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous host is ordinary: a coding agent pointed at the company LLM gateway, a junior who has never opened `/status`, and a Slack thread titled “AI is down.” I treat `ANTHROPIC_BASE_URL` as a named owner’s artifact, the same way I treat a `.env` key. The person who owns [/ai-agent-operations/](/ai-agent-operations/) on this desk also owns “which host loaded which base URL.” A coding agent does not get to hide a schema reject so standup looks like a vendor outage. I already wrote the sibling rule for a wait line that is not a finished child. This is the sibling for a 400 wall that is not a dead gateway.
{{< /field-note >}}

![Three tickets: 400 schema, 401 credential, no answer — named human owns the base URL](/img/every-turn-http-400-is-not-a-dead-gateway-2.png)

## What /status and a one-token curl actually prove

I do not invent a fake dashboard. I use the public commands.

Official env docs say `ANTHROPIC_BASE_URL` overrides the API endpoint to route requests through a proxy or gateway. When it points at a non-first-party host, MCP tool search is disabled by default. Remote Control is disabled when this points at a host other than `api.anthropic.com`, matching Bedrock, Google Cloud’s Agent Platform, and Microsoft Foundry. [Source: https://code.claude.com/docs/en/env-vars]

Official gateway docs say you check two lines on `/status`:

1. `Anthropic base URL`. This line only appears when a gateway address is set. If it is missing, the session is not pointed at the gateway.
2. `Auth token` or `API key`. A line naming `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`, or an `apiKeyHelper` confirms a gateway credential is active. A login-method line naming a claude.ai account means the credential was not distributed. [Source: https://code.claude.com/docs/en/llm-gateway-connect]

Print the version on the same ticket:

```bash
claude --version
```

Then print the named URL the process actually has. Do not quote a wiki card from last month.

```bash
echo "$ANTHROPIC_BASE_URL"
```

A shell export only reaches that terminal and programs started from it. An editor launched from the dock will not see it. Official docs also say a shell-only gateway does not reliably reach background agents hosted by the supervisor. Use a settings file `env` block for any gateway that background agents must always route through. When both a shell export and a settings-file `env` block set the same variable, the settings-file value applies. [Source: https://code.claude.com/docs/en/llm-gateway-connect] [Source: https://code.claude.com/docs/en/env-vars]

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://llm-gateway.example.com",
    "ANTHROPIC_AUTH_TOKEN": "sk-gateway-key"
  }
}
```

Do not put the credential in a project’s `.claude/settings.json`. That file is committed. Use `~/.claude/settings.json` or `.claude/settings.local.json` after you gitignore it. [Source: https://code.claude.com/docs/en/llm-gateway-connect]

Then prove the host still answers. Official docs use a one-token request. Replace the example host and the credential with the values your gateway team gave you. Do not paste a real token into a ticket screenshot that leaves the company.

```bash
curl -X POST "$ANTHROPIC_BASE_URL/v1/messages" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model": "claude-sonnet-4-6", "max_tokens": 1, "messages": [{"role": "user", "content": "."}]}'
```

If your gateway expects keys in `x-api-key`, swap the Authorization header for `x-api-key: $ANTHROPIC_API_KEY`. A JSON response that starts with `{"id":"msg_` and includes a `"content"` field means the gateway is reachable and the credential works. A 401 means the credential was rejected: if you guessed the variable, switch to the other one and try again. [Source: https://code.claude.com/docs/en/llm-gateway-connect]

Write three sentences on the ticket, in this order:

1. What Claude Code printed: every-turn 400, 401, or no answer.
2. What the one-token curl returned: JSON message id, 401, or connection error.
3. Who owns the named base URL and the CLI pin, and whether that owner will change the pin without a status page.

If you skip sentence two, you will file a down ticket for a host that still signed a one-token reply.

## Every-turn 400 is a schema reject

The 10 September changelog and the GitHub tag say the same thing in one sentence. Third-party Anthropic-compatible endpoints rejected a regex in the Artifact tool’s input schema. That regex shipped in the 8 September pin. Every turn 400’d until the 10 September pin fixed the schema. [Source: https://code.claude.com/docs/en/changelog] [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.268]

Read that slowly.

The endpoint was up. The credential was accepted far enough for the server to parse the body. The body contained a tool schema those endpoints do not accept. The CLI then failed every turn, because every turn sent that schema.

That is why a junior’s “I can curl the host” and a teammate’s “Claude is 400 forever” can both be true in the same minute.

A one-token curl does not send the Artifact tool schema. Claude Code does. The short request is a reachability check. It is not a replay of the session.

I do not write a bypass. I do not tell you to strip the Artifact tool, to hide a header, or to teach the gateway to swallow a regex it rejected. The public fix is a CLI pin that no longer ships that schema. The public check is: named URL, named pin, 400 body, one-token curl.

Older 400s on custom base URLs exist in public issues from earlier in 2026: unexpected `anthropic-beta` header values, plugin-loaded request bodies a proxy does not accept. Those are different tickets. Do not glue them onto this field. This post is the every-turn Artifact-schema 400 named on 10 September. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.268]

{{< note type="note" title="400 is not 401, and 401 is not down" >}}
Official gateway docs map 401 to the wrong credential header. `ANTHROPIC_AUTH_TOKEN` goes in `Authorization`. `ANTHROPIC_API_KEY` goes in `x-api-key`. A credential in the wrong variable reaches the gateway in a header it does not read. That is a 401. It is still not a dead host. [Source: https://code.claude.com/docs/en/llm-gateway-connect]
{{< /note >}}

![A one-token curl and a Claude Code session are different requests](/img/every-turn-http-400-is-not-a-dead-gateway-3.png)

## Classify the body before you open a channel

Paste the 400 body into the ticket. Do not summarize from memory. Then classify it with a small script so the next junior does not invent a new severity.

```python
#!/usr/bin/env python3
"""Classify a saved Claude Code / gateway HTTP body for the ticket."""
from pathlib import Path
import json
import sys

def load(path: Path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw": raw[:800], "_kind": "non-json"}

def classify(status: int, body: dict) -> str:
    if status in (0, None):
        return "no-answer"
    if status == 401:
        return "credential"
    if status == 400:
        return "schema-or-request"
    if status == 403 and "_raw" in body:
        return "front-door-html"
    if status >= 500:
        return "server"
    return "other"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: classify_gateway_body.py STATUS_CODE BODY.json")
    status = int(sys.argv[1])
    body = load(Path(sys.argv[2]))
    kind = classify(status, body)
    print(f"status={status}")
    print(f"ticket={kind}")
    if "_raw" in body:
        print("body_preview=" + body["_raw"][:240])
    else:
        err = body.get("error") or body
        print("body_preview=" + json.dumps(err)[:240])
```

Run it on a file the junior already saved:

```bash
python3 classify_gateway_body.py 400 /opt/data/tmp/gateway-400.json
```

If `ticket=schema-or-request`, you stay on the CLI-pin owner. If `ticket=credential`, you stay on the credential owner. If `ticket=no-answer`, then you open the status path. Official docs also name a 403 with an HTML body when a WAF in front of the gateway blocked the request body; a short curl can pass while a real session does not. That is still not “Claude’s API is down.” It is the front door. [Source: https://code.claude.com/docs/en/llm-gateway-connect]

I keep that script boring on purpose. The value is the ticket field, not a new platform.

## What you must not do

Forbidden:

1. File a vendor-down ticket from a 400 wall without a one-token curl on the same named URL.
2. Treat npm `latest` as the pin the host is running. Print `claude --version` on the host.
3. Mix this field with a 401 from a dropped base URL, or with a wait line, or with an empty MCP install. Those are other posts.
4. Write a hide-schema recipe so the old regex comes back. Official notes name the fix as a schema change in the CLI. I do not put a workaround on a wiki card as a “keep shipping” trick. A lying 400 is worse than a noisy pin bump.
5. Commit `ANTHROPIC_AUTH_TOKEN` to the repo because a junior wanted the agent to “just work” on every laptop.

Allowed:

1. Print `claude --version` on the ticket.
2. Run `/status` and copy the `Anthropic base URL` line.
3. Run the official one-token curl on that same URL.
4. Stop, and ping the named owner of the base URL and the CLI pin.

I already refused to leave an org-policy why-line unread. Same instinct: a status sentence is a ticket, not a pass. See [Read the Why-Line Before You Trust the Org Policy](/blog/org-policy-why-line/).

## Merge is not a reason to skip the owner

Gateways are cheap to point at. They are not cheap to own.

Juniors hear “we use a company URL” and think the host can run without a name on the wiki card. Then Friday arrives and nobody knows which box still exports last week’s pin.

I write the owner as a person, not a role. “Platform” is how these hosts stay half-watched until a 400 wall ships as down.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tool pins live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/) when the agent is touching that stack. A first-week map is at [/start-here/](/start-here/). Do not mix those hubs into the 400-body row.

I already refused to treat a green package bump as ownership of the next repair. Same here. A changelog bullet about HTTP 400 is not permission to skip `/status`.

![Not done until version, base URL, curl result, and a named human are on the ticket](/img/every-turn-http-400-is-not-a-dead-gateway-4.png)

## What you should do Monday morning

1. Open the host the team actually uses for Claude Code. Run `claude --version`. Write the string on the ticket next to one human name. That person owns the CLI pin.
2. Run `/status`. Copy the `Anthropic base URL` line. If the line is missing, the session is not on the gateway you think it is. Name who will set `ANTHROPIC_BASE_URL` in a settings `env` block rather than a dock-launched editor.
3. Run the official one-token curl against that same URL. Save the status code and the first line of the body. If curl returns a message id, the host is not down.
4. If Claude Code is still 400 on every turn, paste the 400 body under the curl result. Classify it: schema-or-request, credential, no-answer, or front-door HTML. Do not file a down ticket for schema-or-request.
5. Confirm background agents read the same `env` block. A shell export in one terminal does not own the supervisor. Official docs say so. Write that on the ticket.
6. If the named pin is older than the 10 September schema fix, the owner bumps the pin. If the named pin is already past that fix and every turn is still 400, you have a new ticket: this body, this URL, this pin. You still do not have a dead gateway until curl also fails to connect.

The question is not whether this demos well in chat. The question is whether the 400 wall survives maintenance, handoff, and a host that still answers a one-token request.

## Further reading

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.268" label="GitHub release — every-turn HTTP 400 on third-party ANTHROPIC_BASE_URL (10 September 2026)" >}}

{{< source href="https://code.claude.com/docs/en/changelog" label="Claude Code docs — changelog, 10 September 2026 schema fix" >}}

{{< source href="https://code.claude.com/docs/en/llm-gateway-connect" label="Claude Code docs — gateway /status lines and one-token curl" >}}
