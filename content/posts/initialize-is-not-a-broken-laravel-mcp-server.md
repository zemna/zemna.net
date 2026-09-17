---
title: "A Client That Still Sends Initialize Is Not a Broken Laravel MCP Server"
date: 2026-09-17T07:00:00+07:00
draft: false
slug: "initialize-is-not-a-broken-laravel-mcp-server"
description: "An old MCP client that still opens with initialize is a handshake the new Laravel server still answers, not a dead 1.0 package. Print the method, the pin, and the named owner before you file the server."
topics: ["software-engineering"]
tags: ["laravel-mcp", "mcp", "initialize", "coding-agents", "change-control"]
cover: /covers/initialize-is-not-a-broken-laravel-mcp-server.png
seo:
  primaryQuery: "Laravel MCP initialize still works"
  secondaryQueries:
    - "Laravel MCP server/discover handshake"
    - "initialize handshake not a broken MCP server"
    - "laravel/mcp legacy initialize clients"
---

Standup hears “Laravel MCP is broken.” Someone pasted a JSON-RPC log. The first method is `initialize`. The package pin on the host is the new stable line. The junior files a server-outage ticket. They ping the person who shipped the bump. They tell the coding agent to wait for a rollback.

I stop the run there. A client that still opens with `initialize` is not a broken Laravel MCP server. Official upgrade notes for the 14 September 2026 GitHub tag, published 14:39 UTC, not a prerelease, name the field: the server now speaks protocol revision `2026-07-28` by default, and `server/discover` replaces the old handshake for modern clients. The same notes say clients that still open with `initialize` continue to work. The server answers that handshake with `2025-11-25` or `2025-06-18`, whichever the client requested. [Source: https://github.com/laravel/mcp/releases/tag/v1.0.0] [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

Laravel News, 15 September 2026, repeats the same desk rule in one sentence: clients that still connect with `initialize` continue to work. [Source: https://laravel-news.com/laravel-mcp-1-0]

I already refused to treat an every-turn HTTP 400 as a dead gateway in [Every-Turn HTTP 400 on ANTHROPIC_BASE_URL Is Not a Dead Gateway](/blog/every-turn-http-400-is-not-a-dead-gateway/). I already refused to treat a five-minute WebFetch fail as a hung model in [A 300-Second WebFetch Fail Is Not a Hung Model](/blog/a-300-second-webfetch-fail-is-not-a-hung-model/). This post is the same desk rule for an old handshake on a new MCP server. Print the method. Print the pin. Name who owns both.

The question is not whether the new handshake demos well in Inspector. The question is whether the named owner can still tell an old client from a dead server.

<!--more-->

![Three columns: initialize, discover, dead server — an old handshake is not a dead server](/img/initialize-is-not-a-broken-laravel-mcp-server-1.png)

## The handshake that still answers

Juniors read `initialize` the way they read a 404. The method name is old. The package is new. They assume the bump killed the client.

MCP is not a Laravel-only toy. It is a protocol with a handshake. The old shape is `initialize`, then `tools/list`. The new shape for protocol `2026-07-28` is `server/discover`, then every later request carries protocol version and client capabilities in `params._meta`. Official upgrade notes print both payloads. [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

That is a client dialect. It is not “the server died in composer.”

The GitHub release for tag `v1.0.0` lists pull request 341 in the same body: serve legacy `initialize` clients alongside the modern protocol. That line is the ticket. A log that still says `initialize` is evidence the old path is in use. It is not evidence the new path is missing. [Source: https://github.com/laravel/mcp/releases/tag/v1.0.0] [Source: https://github.com/laravel/mcp/pull/341]

If the first method is `initialize` and the server answers with `2025-11-25` or `2025-06-18`, you do not have a broken server. You have an old client on a server that still speaks the old handshake.

{{< note type="warning" title="Do not file the server on an initialize log" >}}
If the JSON-RPC method is `initialize`, copy the method, print `composer show laravel/mcp`, and name the human who owns that pin before you open a “1.0 is broken” ticket. An old handshake is not a dead package.
{{< /note >}}

I do not invent a fake overnight outage. I use the public contract. Official notes also say clients requesting `2025-03-26` or `2024-11-05` are offered `2025-11-25` instead. A request that already carries `io.modelcontextprotocol/protocolVersion` or `io.modelcontextprotocol/clientCapabilities` in `_meta` is treated as a `2026-07-28` request and validated as such. Those are routing rules. They are not a license to delete the old client from the wiki card. [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

## Three tickets, one owner

Laravel plus Vue work on this desk still runs coding agents next to HTTP MCP: a `Mcp::web()` route, a client that still opens with `initialize`, a junior who sees the old method after a composer bump and pages the wrong channel. Mixing “old handshake,” “header mismatch,” and “server process down” into one “MCP is broken” thread burns an hour of backend people on a client they do not own.

| Ticket | What it means | What you do | Owner |
| --- | --- | --- | --- |
| First method is `initialize`, server answers `2025-11-25` or `2025-06-18` | Old client on a server that still serves the legacy handshake | Copy the method. Print the pin. Do not file the server | Named human who pinned `laravel/mcp` and the client |
| HTTP 400, JSON-RPC `-32020` | Header mismatch on a modern request | Fix `MCP-Protocol-Version`, `Mcp-Method`, and `Mcp-Name` to match the body | Named human who owns the HTTP client and the tests |
| No process, no route, composer pin missing | Then it is a server install ticket | Use the install path, not the handshake path | Named human who owns `composer.lock` |

Do not paste one `initialize` screenshot and call the package dead. If the body names `initialize` and the server answered a protocol the client asked for, you are on a client ticket. If the body is a modern `tools/call` with a 400 and `-32020`, you are on a header ticket. If the route 404s and `composer show laravel/mcp` is empty, you are on an install ticket. See [Every-Turn HTTP 400 on ANTHROPIC_BASE_URL Is Not a Dead Gateway](/blog/every-turn-http-400-is-not-a-dead-gateway/) for the sibling habit: a 400 that still answers is not a dead host, and an old handshake that still answers is not a dead MCP server.

{{< details summary="Pins are evidence, not the hook" >}}
The GitHub tag `v1.0.0` for `laravel/mcp` published at 2026-09-14T14:39:00Z, prerelease false. Packagist recorded the same version at 2026-09-14T14:35:19+00:00. Laravel News covered the stable line on 15 September 2026. Print `composer show laravel/mcp` on the host. Do not treat Packagist time as GitHub `published_at`. Do not put those numbers in the title. [Source: https://github.com/laravel/mcp/releases/tag/v1.0.0] [Source: https://packagist.org/packages/laravel/mcp] [Source: https://laravel-news.com/laravel-mcp-1-0]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous host is ordinary: a `Mcp::web()` route next to the same app that serves the admin, a coding agent that still opens with `initialize`, and a Slack thread titled “MCP 1.0 is broken.” I treat `laravel/mcp` as a named owner’s artifact, the same way I treat a `.env` key. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “which client still sends initialize.” A coding agent does not get to hide an old handshake so standup looks like a dead server. I already wrote the sibling rule for a 400 wall that is not a dead gateway, and for a five-minute fetch fail that is not a hung model. This is the sibling for an old handshake that is not a broken MCP package.
{{< /field-note >}}

![Three tickets: initialize handshake, header 400, missing pin](/img/initialize-is-not-a-broken-laravel-mcp-server-2.png)

## What initialize actually buys you

I do not invent a fake dashboard. I use the public payloads.

Official upgrade notes split two dialects. Do not mix them.

1. Legacy client — first method `initialize`, protocol `2025-11-25` or `2025-06-18` in the handshake params. No `_meta`. No MCP HTTP headers required for the rest of that client’s requests. The server still serves it. [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]
2. Modern client — first method `server/discover`, protocol `2026-07-28` in `params._meta`, and every later request repeats that `_meta`. HTTP clients also send `MCP-Protocol-Version` and `Mcp-Method`. Tool, prompt, and resource calls also send `Mcp-Name`. [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

If your application only defines `Tool`, `Resource`, `Prompt`, and `Server` classes, official notes say no application-class changes are required as long as the MCP client supports `2026-07-28`. Both `Laravel\Mcp\Client` and the MCP Inspector support that revision. That sentence is for app code. It is not a claim that every third-party client already speaks discover. [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

Here is the official before and after, copied as a working JSON-RPC trace, not as a bypass:

```json
{
  "legacy": {
    "initialize": {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "initialize",
      "params": {
        "protocolVersion": "2025-11-25",
        "capabilities": {},
        "clientInfo": {"name": "my-client", "version": "desk"}
      }
    },
    "tools_list": {
      "jsonrpc": "2.0",
      "id": 2,
      "method": "tools/list",
      "params": {}
    }
  },
  "modern": {
    "discover": {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "server/discover",
      "params": {
        "_meta": {
          "io.modelcontextprotocol/protocolVersion": "2026-07-28",
          "io.modelcontextprotocol/clientCapabilities": {}
        }
      }
    }
  }
}
```

[Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

A junior who only greps for `initialize` after the bump will always get a hit on the old client. That grep is not a health check. The health check is: did the server answer, and which dialect did it answer in.

{{< note type="note" title="Discover is the new default, not a delete switch" >}}
Protocol `2026-07-28` uses `server/discover` in place of the initial `initialize` exchange. The upgrade notes still keep the old clients on a documented path. Do not delete `initialize` from the runbook because the default changed. [Source: https://laravel-news.com/laravel-mcp-1-0]
{{< /note >}}

Stateless is a separate field. Official notes removed `Request::sessionId()`, `Request::setSessionId()`, the `MCP-Session-Id` header, and the `SessionInitialized` event. Every HTTP request and stdio message is processed independently. If you need to correlate calls, pass your own identifier through arguments or `_meta`. That is not this ticket. Do not file “initialize is broken” because a listener on `SessionInitialized` went quiet. The event is gone. The handshake is not. [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md] [Source: https://laravel-news.com/laravel-mcp-1-0]

## The header 400 that is not this ticket

Modern HTTP clients live under `ValidateMcpHeaders`. Official notes apply that middleware to every route registered via `Mcp::web(...)`. Each POST must include `MCP-Protocol-Version` and `Mcp-Method` whose values match the request body. Requests for `tools/call`, `prompts/get`, and `resources/read` must also include `Mcp-Name` matching `params.name` or, for `resources/read`, `params.uri`. [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

A mismatch returns HTTP 400 with JSON-RPC error code `-32020`. Laravel News states the same code. Older clients that use `initialize` and send no protocol metadata in `_meta` are exempt from header validation. [Source: https://laravel-news.com/laravel-mcp-1-0] [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

That 400 is a schema reject. It is the sibling of [Every-Turn HTTP 400 on ANTHROPIC_BASE_URL Is Not a Dead Gateway](/blog/every-turn-http-400-is-not-a-dead-gateway/). The host answered. The request was illegal for that dialect. It is not proof `initialize` is dead, and it is not proof the package failed to install.

Tests that still `postJson()` a modern `tools/call` without headers will fail after the bump. Official notes show the repair. Use it in the test suite the named owner actually runs:

```php
public function test_modern_tools_call_sends_matching_mcp_headers(): void
{
    $message = [
        'jsonrpc' => '2.0',
        'id' => 1,
        'method' => 'tools/call',
        'params' => [
            'name' => 'say-hi',
            'arguments' => [],
            '_meta' => [
                'io.modelcontextprotocol/protocolVersion' => '2026-07-28',
                'io.modelcontextprotocol/clientCapabilities' => [],
            ],
        ],
    ];

    $this->postJson('mcp-endpoint', $message, [
        'MCP-Protocol-Version' => '2026-07-28',
        'Mcp-Method' => 'tools/call',
        'Mcp-Name' => 'say-hi',
    ])->assertOk();
}
```

[Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

Replace `mcp-endpoint` with the path you registered in `Mcp::web()`. Do not copy `say-hi` into production. The point is the three headers matching the body. A 400 with `-32020` after this test still fails is a header ticket. A log that only shows `initialize` never entered this test.

I already refused to treat a wait line as a finished background agent in [Waiting for Your Input Is Not a Finished Background Agent](/blog/waiting-for-input-is-not-finished/). Same instinct: a red test is a ticket, not a pass, and an old handshake in production is a client ticket, not a rollback.

![Modern request headers to HTTP 400 — header mismatch is not a dead handshake](/img/initialize-is-not-a-broken-laravel-mcp-server-3.png)

## Print the method before you file the server

I write the owner as a person, not a role. “Platform” is how these hosts stay half-watched until an old method ships as a dead package.

Print three artifacts on the ticket:

1. The JSON-RPC `method` on the first request.
2. The installed `laravel/mcp` version from the lockfile the host actually runs.
3. The human who owns that lockfile.

This script reads `composer.lock` in the app root and prints the pinned version. It is the check I want on the ticket, not a Packagist screenshot:

```php
<?php
declare(strict_types=1);

$lockPath = $argv[1] ?? 'composer.lock';
$raw = file_get_contents($lockPath);
if ($raw === false) {
    fwrite(STDERR, "cannot read {$lockPath}\n");
    exit(1);
}

$lock = json_decode($raw, true);
if (! is_array($lock)) {
    fwrite(STDERR, "invalid composer.lock\n");
    exit(1);
}

foreach ($lock['packages'] ?? [] as $package) {
    if (($package['name'] ?? '') === 'laravel/mcp') {
        fwrite(STDOUT, ($package['version'] ?? 'unknown') . PHP_EOL);
        exit(0);
    }
}

fwrite(STDERR, "laravel/mcp not in composer.lock\n");
exit(1);
```

Run it on the host that serves `Mcp::web()`, not on a laptop that last ran `composer update` in January.

Then log the method the route actually received. Keep it as a probe, not as a new public API:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

public function beforeMcpDispatch(Request $request): void
{
    Log::info('mcp.jsonrpc.first_look', [
        'method' => $request->input('method'),
        'has_meta' => $request->input('params._meta') !== null,
        'protocol_header' => $request->header('MCP-Protocol-Version'),
    ]);
}
```

If `method` is `initialize` and `has_meta` is false, you are on the legacy path the upgrade notes still serve. If `method` is `server/discover`, you are on the new path. If `method` is `tools/call` and the response is 400 with `-32020`, you are on the header path. Those three lines are the screenshot a junior can paste. [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]

Do not wrap this probe in a “compatibility shim” that rewrites `initialize` into `server/discover` on the wire. Official notes already keep the old clients. A homemade rewrite is a protocol-bypass. I will not put one in this post.

GSC this week still has no striking-distance query on the HTTP 400 post, the wait-line post, or the WebFetch post. I am not refreshing those URLs. This is a new field, not a synonym of Monday’s slug or yesterday’s fetch fail.

## What you must not do

Forbidden:

1. File a “Laravel MCP is broken” ticket from an `initialize` log without printing `composer show laravel/mcp` and the JSON-RPC method.
2. Put the package version in the title or the first line. The version is evidence after the decision.
3. Mix this field with a reconnect-gave-up `/mcp` notice, a whitespace MCP stall, or an idle MCP screenshot. Those are other tickets.
4. Treat a 400 with `-32020` as proof the legacy handshake is dead. Official notes exempt `initialize` clients from header validation.
5. Rewrite `initialize` into `server/discover` in a proxy so the log looks modern. That is a bypass. The server already answers the old method.
6. Delete listeners and then claim the handshake is gone because `SessionInitialized` is gone. The event was removed. The legacy handshake was not. [Source: https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md]
7. Recommend buying a new client, a new model, or a new host because the method name looks old.

Allowed:

1. Print the JSON-RPC `method` on the ticket.
2. Print `composer show laravel/mcp` or the lockfile script above.
3. Copy the protocol the server answered: `2025-11-25`, `2025-06-18`, or `2026-07-28`.
4. Stop, and ping the named owner of the package pin and the MCP client.
5. Keep the old client on a written exception until that owner moves it. Name the exception on the wiki card.

![Ticket checklist: method, composer pin, protocol answer, named human](/img/initialize-is-not-a-broken-laravel-mcp-server-4.png)

## This is not yesterday's fetch fail

Yesterday’s post is a download deadline. WebFetch goes red at about 300 seconds. The model was waiting on a socket. [Source: https://zemna.net/blog/a-300-second-webfetch-fail-is-not-a-hung-model/]

Monday’s post is a schema reject on a named `ANTHROPIC_BASE_URL`. The host answered. The request was illegal for that endpoint. [Source: https://zemna.net/blog/every-turn-http-400-is-not-a-dead-gateway/]

This post is a handshake dialect. The client still says `initialize`. The server still answers. The package is not the thing that failed.

Do not merge the three into “the agent stack is down.” A 400 wall still answers curl. A five-minute fetch fail still proves the CLI enforced a deadline. An `initialize` log on a current `laravel/mcp` pin still proves the server served the legacy path. All three need a named pin. They do not share a vendor-down channel.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tool pins live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/) when the agent is touching that stack. A first-week map is at [/start-here/](/start-here/). Do not mix those hubs into the handshake row.

I already refused to treat a green package bump as ownership of the next repair. Same here. A changelog bullet about `server/discover` is not permission to skip `composer show laravel/mcp`.

## What you should do Monday morning

1. Open the host that actually serves `Mcp::web()`. Run `composer show laravel/mcp`. Write the string on the ticket next to one human name. That person owns the package pin.
2. Capture one live JSON-RPC first request. Write the `method`. If it is `initialize`, write the protocol the server answered. If it is `server/discover`, write that instead. Do not leave the method as a tribal screenshot in Slack.
3. Run the lockfile script in the app root the supervisor uses. Confirm it matches `composer show`. A laptop lockfile is not the host.
4. If a modern HTTP test returns 400 with `-32020`, add the three headers from the upgrade notes and re-run. Classify it: legacy-handshake, header-mismatch, or missing-package. Do not file a server-outage ticket for legacy-handshake.
5. Confirm coding-agent MCP configs on this desk still name the same URL the Laravel route serves. A client pointed at `/mcp` on another box is a different ticket. Print the URL on the same card as the pin.
6. If the named pin is older than the 14 September 2026 GitHub tag and you needed the documented legacy path, the owner bumps the pin on purpose, with a written exception for every client that still sends `initialize`. If the named pin is already on that tag and `initialize` still answers, you have the expected path. You still do not have a broken server until the route is down and the lockfile is empty.

The question is not whether Inspector demos `server/discover`. The question is whether the old handshake survives maintenance, handoff, and a junior who wants to roll back the package.

## Further reading

{{< source href="https://github.com/laravel/mcp/blob/v1.0.0/UPGRADE.md" label="laravel/mcp upgrade guide — initialize clients continue to work" >}}

{{< source href="https://github.com/laravel/mcp/releases/tag/v1.0.0" label="GitHub release v1.0.0 — PR 341 legacy initialize clients (14 September 2026)" >}}

{{< source href="https://laravel-news.com/laravel-mcp-1-0" label="Laravel News — Laravel MCP 1.0, 15 September 2026" >}}
