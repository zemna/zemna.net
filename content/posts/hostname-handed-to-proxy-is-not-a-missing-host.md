---
title: "Handing the Hostname to the Forward Proxy Is Not a Missing Host"
date: 2026-09-21T07:00:00+07:00
draft: false
slug: "hostname-handed-to-proxy-is-not-a-missing-host"
description: "A failed local DNS lookup on a Claude apps gateway pod is not a missing host when the pod only talks through a forward proxy. Print the env, read the boot network line, and name who owns proxy-only egress."
topics: ["software-engineering"]
tags: ["claude-code", "claude-apps-gateway", "forward-proxy", "dns", "egress", "coding-agents", "change-control"]
cover: /covers/hostname-handed-to-proxy-is-not-a-missing-host.png
seo:
  primaryQuery: "Claude apps gateway proxy-only egress hostname not local DNS"
  secondaryQueries:
    - "CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY forward proxy"
    - "gateway pod cannot resolve public DNS HTTPS_PROXY"
    - "Claude Code gateway CONNECT hostname vs IP"
---

The junior SSHs into the gateway box. `nslookup api.anthropic.com` times out. `getent hosts` is empty. They paste that into the incident channel and call DNS down. Standup treats it as a missing host.

I stop the run there. Handing the hostname to the forward proxy is not a missing host. On a Claude apps gateway whose only egress is that proxy, the field is whether the gateway hands the proxy the name. Local resolve on the pod is the wrong screenshot.

Official config docs put the switch in one environment variable: `CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY=1`, next to `HTTPS_PROXY`, when the pod reaches other hosts only through that forward proxy and cannot resolve public DNS names itself, or when the proxy refuses `CONNECT` to an IP address. [Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

I already refused to treat a present `AGENTS.md` as the project instructions while `CLAUDE.md` exists in [A Present AGENTS.md Is Not the Project Instructions While CLAUDE.md Exists](/blog/agents-md-is-not-the-project-instructions/). I already refused to treat `ubuntu-latest` as a runner image I already tested in [Ubuntu-latest Is Not a Runner Image You Already Tested](/blog/ubuntu-latest-is-not-a-tested-runner-image/). I already refused to treat a missing Wrangler `previews` block as production bindings in [A Missing Previews Block Is Not a License to Reuse Production Bindings](/blog/missing-previews-block-is-not-production-bindings/). This post is the same desk rule for gateway egress. Print the env. Read the boot `network:` line. Name who owns the boundary.

The question is not whether the pod can resolve the provider. The question is whether the named owner can prove the hostname left the box through the proxy.

<!--more-->

![Two columns: local DNS fail is not a missing host when the hostname is handed to the proxy](/img/hostname-handed-to-proxy-is-not-a-missing-host-1.png)

## The ticket that looks like DNS

Juniors treat a gateway pod the way they treat a laptop. If `dig` fails, the host is missing. That habit is correct on a box that talks to the public internet. It is wrong on a box that is only allowed to talk to a forward proxy.

Two jobs collide on that pod.

1. **Reach the provider.** Inference, token exchange, telemetry export, and some identity calls have to leave the cluster.
2. **Do not resolve those names on the pod.** The cluster DNS has no public records. The proxy refuses `CONNECT` to a raw IP. The gateway’s own address check wants a hostname the proxy already allowlists.

Default Claude apps gateway behavior with `HTTPS_PROXY` set still resolves and checks many destinations locally, then opens `CONNECT` to the checked IP through the proxy. That path needs public DNS on the pod. Proxy-only egress turns that path off for the classes the docs name. [Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

If you only run `nslookup` inside the pod, you will file DNS. You will not file the boundary.

{{< note type="warning" title="Do not file DNS on a proxy-only gateway pod" >}}
If the gateway cannot reach a provider and the pod has no public DNS, print `HTTPS_PROXY`, both `NO_PROXY` spellings, `CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY`, and the boot `network:` line before you page the resolver team. A failed local lookup is not a missing host.
{{< /note >}}

I do not invent a fake overnight outage. I use the public contract. The GitHub release that added the switch says: for Claude apps gateways whose only egress is a forward proxy, every outbound request hands the proxy the hostname instead of resolving it locally. The official changelog repeats that sentence. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277] [Source: https://code.claude.com/docs/en/changelog]

## What the gateway actually does with a name

Official docs give one table. I keep it as the ticket, not as a version pin.

| Outbound request | Default with `HTTPS_PROXY` | Proxy-only egress active |
| --- | --- | --- |
| `provider: anthropic` upstreams, Workload Identity Federation token exchange, `telemetry.forward_to` exports | Resolved and checked locally, then `CONNECT` to the checked IP through the proxy. A telemetry collector listed in `NO_PROXY` is reached directly | Hostname handed to the proxy |
| IdP discovery, JWKS, token, and userinfo | Direct unless `oidc.use_proxy: true`, then `CONNECT` to the checked IP | Hostname handed to the proxy, unless `oidc.use_proxy: false` keeps an internal IdP direct |
| Amazon Bedrock, Claude Platform on AWS, Google Cloud’s Agent Platform, and Microsoft Foundry upstreams; Google group lookups | Hostname handed to the proxy | Unchanged |

[Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

Read the last row twice. Cloud-provider upstreams already hand the hostname to the proxy. Turning the env on does not “fix Bedrock DNS.” It changes the Anthropic-provider row, the WIF row, the telemetry-export row, and the IdP row. File the wrong row and you will “fix” a path that never resolved locally.

A gateway is not the developer laptop. Official overview: Claude Code talks to the gateway with a developer credential; the gateway forwards with the organization credential. Laptop `HTTPS_PROXY` is a different ticket. This post is the gateway pod. [Source: https://code.claude.com/docs/en/gateways]

{{< details summary="Pins are evidence, not the hook" >}}
Proxy-only egress needs Claude Code at or after the 18 September 2026 GitHub release that named `CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY`. This morning’s npm registry, 21 September 2026: `@anthropic-ai/claude-code` `latest` and `next` are 2.1.278 (published 19 September 2026). `stable` is still 2.1.267 (published 9 September 2026). Do not treat `stable` as the field. Do not put those numbers in the title. Changelog notes for 2.1.278 are an auto-mode classifier change. That is a different ticket. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277] [Source: https://code.claude.com/docs/en/changelog] [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]
{{< /details >}}

## Three conditions, or the switch stays off

The env name looks like a boolean. Official docs say it stays off unless the gateway environment meets all three conditions.

1. `HTTPS_PROXY` or `HTTP_PROXY` is set.
2. `NO_PROXY` and `no_proxy` are empty. If the platform injects either into pods, set both to an empty value on the gateway container. Listing a telemetry collector in `NO_PROXY` keeps proxy-only egress off.
3. `CLAUDE_GATEWAY_ALLOW_LOOPBACK` is not turned on. A collector or IdP on the pod’s own loopback cannot combine with proxy-only egress, because a loopback address handed to the proxy would be the proxy host’s own. The gateway refuses `localhost`-style names outright while proxy-only egress is active.

[Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

When one condition is missing, the gateway logs a warning at boot naming the variable that stopped it and keeps the default behavior. That warning is the artifact. A missing warning plus a failed `dig` is not “the flag is on.”

Official docs also say why the flag is an environment variable rather than a `gateway.yaml` key: nothing in the config file can relax the gateway’s address check. Put the flag in YAML and you will ship a key the binary does not read. [Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

The example the docs publish is this shape. Copy it as a probe, not as a bypass recipe.

```bash
export HTTPS_PROXY=http://proxy.corp.example.com:3128
export NO_PROXY=
export no_proxy=
export CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY=1
```

[Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

`NO_PROXY=` is not “unset.” A platform list such as `localhost,127.0.0.1,.svc.cluster.local` is enough to keep the switch off. Empty both spellings on the gateway container, not on the laptop.

![Three conditions or the switch stays off: proxy set, NO_PROXY empty, loopback allow off](/img/hostname-handed-to-proxy-is-not-a-missing-host-2.png)

## The boot line is the screenshot

I do not guess the mode from the Deployment YAML. Official docs say the gateway logs one `network:` line at boot while proxy-only egress is active. If that line is absent, the switch did not take. [Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

Once it is active, the docs require every destination in the proxy allowlist, including an internal collector and any host configured by IP address. You can still keep an internal IdP direct with `oidc.use_proxy: false`. That is the one documented exception, not a general bypass. [Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

Turn this on only when the proxy’s allowlist is at least as strict as the gateway’s own check. Official docs are blunt: the proxy must refuse cloud metadata endpoints such as `169.254.169.254` and `metadata.google.internal`, link-local addresses, and the proxy host’s own loopback, and it must refuse them by the address a name resolves to, not only by name, because the gateway no longer catches a hostname that resolves to one of them. A proxy that connects anywhere it is asked removes the gateway’s SSRF guard for these requests. [Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

That paragraph is why I name a human owner. The env does not make the network safer by itself. It moves the check to the proxy. If nobody owns the proxy allowlist, you traded a local DNS ticket for an open CONNECT ticket.

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous mix is ordinary: a Claude apps gateway in Kubernetes, a corporate forward proxy, and a platform `NO_PROXY` that lists cluster DNS plus a telemetry collector. The coding agent on the laptop is fine. The gateway pod is not. I treat `PROXY_EGRESS_OWNER` the same way I treat a migration owner. The person who owns [/ai-agent-operations/](/ai-agent-operations/) on this desk also owns “did this session hand the hostname to the proxy.” A coding agent does not get to skip `php artisan test --parallel` because the gateway looked “down” on a local `dig`. I already wrote the sibling rule for a present `AGENTS.md` that is not the brief. This is the sibling for a failed local lookup that is not a missing host.
{{< /field-note >}}

## Probe the env, not the public resolver

I do not curl the provider from the pod to “prove DNS.” That curl is the wrong tool on a proxy-only box. I print the four names, require a human owner, and fail closed when the owner is unset.

```python {linenos=inline,hl_lines=[12,"28-32"]}
#!/usr/bin/env python3
"""Probe Claude apps gateway proxy-only egress. Does not open sockets."""

from __future__ import annotations

import os
import sys

REQUIRED_OWNER = "PROXY_EGRESS_OWNER"


def main() -> int:
    owner = os.environ.get(REQUIRED_OWNER, "UNSET")
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or ""
    no_proxy = os.environ.get("NO_PROXY")
    no_proxy_lc = os.environ.get("no_proxy")
    boundary = os.environ.get("CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY", "")
    loopback = os.environ.get("CLAUDE_GATEWAY_ALLOW_LOOPBACK", "")

    print(f"OWNER={owner}")
    print(f"HTTPS_PROXY_OR_HTTP_PROXY_SET={bool(https_proxy)}")
    print(f"NO_PROXY={no_proxy!r}")
    print(f"no_proxy={no_proxy_lc!r}")
    print(f"CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY={boundary!r}")
    print(f"CLAUDE_GATEWAY_ALLOW_LOOPBACK={loopback!r}")

    empty_no_proxy = no_proxy == "" and no_proxy_lc == ""
    boundary_on = boundary == "1"
    loopback_off = loopback not in {"1", "true", "TRUE", "yes"}

    if not https_proxy:
        print("VERDICT=SWITCH_OFF_NO_PROXY_URL")
    elif not empty_no_proxy:
        print("VERDICT=SWITCH_OFF_NO_PROXY_INJECTED")
    elif not loopback_off:
        print("VERDICT=SWITCH_OFF_LOOPBACK_ALLOW")
    elif not boundary_on:
        print("VERDICT=SWITCH_OFF_FLAG_NOT_ONE")
    else:
        print("VERDICT=ENV_MATCHES_PROXY_ONLY_CONTRACT")

    if owner == "UNSET":
        print("FAIL=name PROXY_EGRESS_OWNER before you file DNS")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it in the gateway container, not on your laptop.

```bash
export PROXY_EGRESS_OWNER="shinjae"
python3 scripts/probe_proxy_egress.py
printenv HTTPS_PROXY HTTP_PROXY NO_PROXY no_proxy \
  CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY \
  CLAUDE_GATEWAY_ALLOW_LOOPBACK
claude --version
```

The script does not talk to Anthropic. It reads the environment. `VERDICT=SWITCH_OFF_NO_PROXY_INJECTED` means the platform still wrote a bypass list. Then read the boot log. Copy the `network:` line, or copy the warning that named the variable that stopped the switch. Put those four lines on the ticket: owner, verdict, boot line, `claude --version`.

`nslookup api.anthropic.com` on the pod is evidence of local DNS. It is not evidence of proxy-only egress.

![Probe the env, not public DNS: owner, verdict, boot line, version](/img/hostname-handed-to-proxy-is-not-a-missing-host-3.png)

## Adjacent tickets you must not mix in

The same release added more than this switch. Mixing them on one ticket is how a junior upgrades the binary and still files DNS.

**Static upstream headers.** Official release notes add an optional `headers:` map on Claude apps gateway upstreams, to send static headers to a proxy you run in front of a provider. That is a header contract. It is not proxy-only egress. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277]

**Telemetry collector listed in `NO_PROXY`.** The same release fixed the Claude apps gateway’s telemetry relay ignoring a collector hostname or domain listed in `NO_PROXY` when a proxy is set. That fix is the default path: a collector in `NO_PROXY` is reached directly. Proxy-only egress docs say listing a collector in `NO_PROXY` keeps the switch off. You do not get both “collector bypasses the proxy” and “every outbound request hands the hostname to the proxy.” Pick one. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277] [Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

**Loopback allow.** Official docs improved loopback error messages to name `CLAUDE_GATEWAY_ALLOW_LOOPBACK`. That flag is incompatible with proxy-only egress. Do not turn it on to “make localhost telemetry work” on the same pod. Give those services an address the proxy can reach. [Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277] [Source: https://code.claude.com/docs/en/claude-apps-gateway-config]

**Developer nonessential traffic.** Official overview: version checks and downloads leave Claude Code toward Anthropic, not through the gateway path. `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is a client flag. It does not turn on proxy-only egress on the pod. [Source: https://code.claude.com/docs/en/gateways]

**HTTP 400 on `ANTHROPIC_BASE_URL`.** I already wrote [Every-Turn HTTP 400 on ANTHROPIC_BASE_URL Is Not a Dead Gateway](/blog/every-turn-http-400-is-not-a-dead-gateway/). A 400 from a bad base URL is not this field. Do not refresh that URL as a synonym.

![Same release, different tickets: headers map, collector NO_PROXY, loopback allow, client traffic](/img/hostname-handed-to-proxy-is-not-a-missing-host-4.png)

## What you must not do

Forbidden:

1. File a “DNS is down” ticket on a Claude apps gateway without printing `HTTPS_PROXY` or `HTTP_PROXY`, both `NO_PROXY` spellings, `CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY`, `CLAUDE_GATEWAY_ALLOW_LOOPBACK`, the boot `network:` line or the boot warning, and one human name as `PROXY_EGRESS_OWNER`.
2. Put a Claude Code version in the title or the first line. The pin is evidence after the decision.
3. Mix this field with a present `AGENTS.md`, an `ubuntu-latest` runner label, a missing Wrangler `previews` block, billed auto-mode, or a Copilot picker name. Those are other tickets.
4. Treat `stable` on npm as the field. This morning `stable` is still behind the release that named the switch. [Source: https://www.npmjs.com/package/@anthropic-ai/claude-code]
5. Put `CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY` in `gateway.yaml` and expect the binary to honor it. Official docs keep it as an environment variable so the config file cannot relax the address check. [Source: https://code.claude.com/docs/en/claude-apps-gateway-config]
6. List a telemetry collector in `NO_PROXY` and also claim proxy-only egress is active. Official docs say that listing keeps the switch off.
7. Turn on `CLAUDE_GATEWAY_ALLOW_LOOPBACK` on the same pod to keep a localhost collector. Official docs say those two modes do not combine.
8. Write a proxy-bypass recipe, a CONNECT-to-IP workaround, or a “set NO_PROXY to the provider” cheat. That is the opposite of this field.
9. Recommend buying a plan, a model, or a seat because the pod cannot resolve public DNS.
10. Trust a laptop `dig` as proof the gateway handed the hostname to the proxy.

Allowed:

1. Print the four environment names from the gateway container.
2. Copy the boot `network:` line, or the warning that named the variable that stopped the switch.
3. Keep an internal IdP direct with `oidc.use_proxy: false` when official docs say that exception applies.
4. Put every destination the gateway still needs, including collectors and IP-configured hosts, on the proxy allowlist once the switch is on.
5. Name one human as `PROXY_EGRESS_OWNER`.
6. Confirm the proxy refuses metadata, link-local, and its own loopback by resolved address, not only by name.

GSC this week still has no striking-distance query on the AGENTS.md post, the ubuntu-latest post, or the previews-block post. I am not refreshing those URLs. This is a new field, not a synonym of yesterday’s instruction-file load or Saturday’s runner label.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/) when the agent is touching that stack. A first-week map is at [/start-here/](/start-here/).

A changelog bullet about handing the hostname to the proxy is not permission to skip the boot line.

## What you should do Monday morning

1. Open the gateway container that actually forwards traffic. Export `PROXY_EGRESS_OWNER` to a human name. Run `probe_proxy_egress.py` there. Write the verdict on the ticket next to that name.
2. Print `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`, `no_proxy`, `CLAUDE_GATEWAY_PROXY_IS_EGRESS_BOUNDARY`, and `CLAUDE_GATEWAY_ALLOW_LOOPBACK`. If the platform injected a `NO_PROXY` list, set both spellings to empty on that container. Do not “fix” DNS on cluster CoreDNS for this ticket.
3. Read the gateway boot log. Copy the `network:` line if proxy-only egress is active. If you see a warning naming the variable that stopped it, that warning is the field. Do not argue with a failed `nslookup`.
4. If the switch is on, confirm the proxy allowlist includes every remaining destination, including internal collectors and hosts configured by IP. Confirm the proxy refuses metadata, link-local, and its own loopback by resolved address. Name the proxy-allowlist owner if that is a different human.
5. Print `claude --version` on the gateway image. If `stable` is still behind the release that named the switch, do not treat npm `stable` as the field.
6. Confirm coding-agent instructions on this desk name the same owner and forbid a “DNS is down” ticket without the env dump and the boot line. A prompt that says “check DNS” on a proxy-only pod is a different ticket.

The question is not whether public DNS demos on a laptop. The question is whether the hostname-to-proxy path survives maintenance, handoff, and a junior who already ran `nslookup` inside the pod.

## Further reading

{{< source href="https://code.claude.com/docs/en/claude-apps-gateway-config" label="Claude Code Docs — Claude apps gateway configuration (proxy-only egress)" >}}

{{< source href="https://github.com/anthropics/claude-code/releases/tag/v2.1.277" label="GitHub — Claude Code release that added hostname-to-proxy egress" >}}

{{< source href="https://code.claude.com/docs/en/gateways" label="Claude Code Docs — Run Claude Code through a gateway" >}}
