---
title: "Read the Requested Scopes Before You File an Outage"
date: 2026-09-09T07:00:00+07:00
draft: false
slug: "requested-scopes-before-outage"
description: "A failed Cloudflare CLI login is a requested-scope list, not a status page. Copy the unknown scope, name who owns the CLI pin, then resume the coding agent."
topics: ["devops"]
tags: ["cloudflare", "oauth", "wrangler", "cf-cli", "workers-auth", "change-control", "coding-agents"]
cover: /covers/requested-scopes-before-outage.png
seo:
  primaryQuery: "cf auth login unknown OAuth scope"
  secondaryQueries:
    - "Cloudflare CLI login failed not an outage"
    - "email_routing:read OAuth scope not registered"
    - "named owner Wrangler OAuth scope list"
---

Standup hears “Cloudflare OAuth is down.” Someone pasted a red terminal. `cf auth login` died. The junior opens the status page. The coding agent offers to “switch providers until login works.”

I stop the run there. A failed login is a requested-scope list. It is not a status incident.

On 7 September 2026 Cloudflare published a patch for `@cloudflare/workers-auth`. The notes are blunt: `cf auth login` asked for `email_routing:read` and `email_sending:read`. The Cloudflare OAuth server does not define those names. Login failed with an unknown OAuth scope error. The CLI now requests only the registered write scopes for those products. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/%40cloudflare/workers-auth%400.6.9]

I already refused to treat an Organization policy why-line as a loaded fleet file in [Read the Why-Line Before You Trust the Org Policy](/blog/org-policy-why-line/). I already refused to treat a green `apt update` as a trusted key in [A Green apt Update Is Not a Trusted Key After Saturday](/blog/green-apt-is-not-a-trusted-key/). This post is the login version of the same desk rule. Read the scope the client asked for. Check whether the server registered it. Name who owns the CLI pin. Do not page an outage for a catalog mismatch.

The question is not whether Cloudflare’s dashboard loaded this morning. The question is whether the binary on this laptop asked the OAuth server for a name that server has never heard.

<!--more-->

![Classify the red line: red login, status page closed, named CLI owner](/img/requested-scopes-before-outage-1.png)

## The red line that looks like an outage

Juniors read a failed OAuth login the way they read a 500 from the public API. Red text. The word “OAuth.” A browser that never finished. They assume the identity plane is down.

OAuth does not work that way. The client sends a list of scope strings. The authorization server accepts only the strings it registered. If the client invents a name, the server rejects the request before any human clicks Authorize. That rejection is local to the client catalog. It is not “Cloudflare is down.”

The public patch names the two strings. `email_routing:read`. `email_sending:read`. The pull request that landed the fix says both products expose only their write scopes on Cloudflare’s OAuth registry. The change removes the two read names from the `cf` scope catalog. It does not change documented Email Routing or Email Sending API behavior. [Source: https://github.com/cloudflare/workers-sdk/pull/15547]

Three sentences belong on the ticket, in this order:

1. Which binary asked for login (`cf`, `wrangler`, a wrapper script, a coding-agent skill).
2. Which scope string the error named.
3. Whether that string is in the server catalog, or only in the client’s wish list.

If you skip sentence two, you will file an incident for a string the server never shipped.

{{< note type="warning" title="Unknown scope is a client ticket" >}}
If login fails because a scope is unknown, stop the coding-agent session. Copy the scope string. Do not “retry with a different model.” Do not paste `CLOUDFLARE_API_TOKEN` into chat to “unblock.”
{{< /note >}}

I do not invent a fake outage on this desk. I use the public contract. The release is not a prerelease. Published 7 September 2026 at 15:20 UTC. The first bullet is the unsupported email read scopes. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/%40cloudflare/workers-auth%400.6.9]

## Three login paths, three owners

Laravel and Vue work on this desk still deploys through Cloudflare Workers on some properties. That means three different auth paths sit on the same laptop. Mixing them is how a junior turns a scope bug into a two-hour “platform is down” thread.

| Path | What it is | Who owns it | Outage or catalog |
| --- | --- | --- | --- |
| `cf auth login` | Interactive OAuth for the `cf` CLI | Named human who pins the `cf` / `@cloudflare/workers-auth` binary | Catalog. The 7 September patch lives here. |
| `wrangler login` | Interactive OAuth for Wrangler | Named human who pins Wrangler in the repo | Catalog. Use `--scopes-list` and `--scopes`. |
| `CLOUDFLARE_API_TOKEN` | Non-interactive token | Named human who creates the token in the dashboard | Token permissions. Not an OAuth scope string. |

Official Wrangler docs split the last two on purpose. `wrangler login` opens a browser. Headless CI uses an API token. [Source: https://developers.cloudflare.com/workers/wrangler/commands/general/] [Source: https://developers.cloudflare.com/workers/ci-cd/]

Do not paste one screenshot and call every row done. `cf` and Wrangler share a monorepo. They do not share a failure mode. The 7 September notes fix `cf auth login`. They do not claim Wrangler asked for `email_routing:read`. If your red line came from `npx wrangler login`, you are on the Wrangler row. If it came from `cf auth login`, you are on the `cf` row. Write the binary name first.

{{< details summary="npm tags are evidence, not the hook" >}}
This morning’s registry, 9 September 2026: `@cloudflare/workers-auth` `latest` is 0.6.10, published 8 September 2026 at 17:05 UTC. That tag is a dependency bump onto `@cloudflare/workers-utils`. The unsupported-scope fix itself landed in 0.6.9. `wrangler` `latest` is 4.130.0, published 8 September 2026 at 17:07 UTC. Pin what you run. Do not put those numbers in the title. Do not treat `latest` as the fleet pin. [Source: https://www.npmjs.com/package/@cloudflare/workers-auth] [Source: https://www.npmjs.com/package/wrangler]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the dangerous login is ordinary: a deploy user on a laptop, `wrangler deploy` for a Worker that fronts the PHP API, and a coding agent that “helps” when the browser OAuth window fails. The agent’s first idea is always the same: paste a token into `.dev.vars`, or tell standup the dashboard is down. I treat the CLI pin as a named owner’s file, the same way I treat a migration. The person who owns [/developer-tools/](/developer-tools/) on this desk also owns “which binary asked for which scope.” Copilot does not get to rewrite the login command as a drive-by lint.
{{< /field-note >}}

## What “registered” means on the ticket

Juniors hear “scope” and think “permission I forgot to tick.” That is the dashboard token story. OAuth login is a different list.

Cloudflare’s own authorize-an-application docs say the consent screen shows the scopes the application is requesting after you pick accounts. You can decline optional permissions. You cannot invent a string the server never registered. [Source: https://developers.cloudflare.com/fundamentals/oauth/authorizing-an-application/]

Wrangler’s login command is explicit about the client list. `--scopes-list` prints the scopes the CLI knows. `--scopes` lets you pass a whitespace-separated subset, for example `account:read user:read`. If you pass nothing, Wrangler uses all available scopes by default. [Source: https://developers.cloudflare.com/workers/wrangler/commands/general/]

That default is a product choice. It is not a reason to file an outage. If a default list contains a name the server dropped or never shipped, login fails for everyone on that binary. The fix is a client patch, or a narrower `--scopes` list that only names registered strings. The 7 September `cf` patch is the first kind: delete the two read names, keep the write names the server actually has.

I keep a short table on the wiki card. I do not let the agent expand it into a permission novel.

| String you saw | What it is | Next action |
| --- | --- | --- |
| `email_routing:read` or `email_sending:read` on `cf auth login` | Client asked for a name the OAuth registry does not define | Upgrade the `cf` / workers-auth pin past the 7 September patch, or stop using that binary until the owner pins it |
| Unknown scope, other name | Still a client catalog problem until proven otherwise | Copy the string. Check `--scopes-list`. File against the CLI owner, not against “Cloudflare down” |
| Consent screen missing a box you expected | Optional-scope UI, not an outage | Re-authorize and grant the scope the command needs [Source: https://developers.cloudflare.com/changelog/post/2026-08-22-wrangler-mcp-optional-oauth-scopes/] |
| CI cannot open a browser | Expected | Use `CLOUDFLARE_API_TOKEN`, not `wrangler login` [Source: https://developers.cloudflare.com/workers/ci-cd/] |

![Four tickets, one owner each: requested string, registered catalog, optional consent, CI token](/img/requested-scopes-before-outage-2.png)

## Copy the error, then classify it

Do not screenshot a cropped window. Copy the command, the binary version, and the scope string. Then classify.

```bash {linenos=inline,hl_lines=[3,"12-16"]}
#!/usr/bin/env bash
set -euo pipefail

err=${1:-/tmp/cf-login.err}
bin=$(command -v cf || true)
wbin=$(command -v wrangler || true)

{
  echo "host=$(hostname)"
  echo "user=$(id -un)"
  echo "cf_bin=${bin:-missing}"
  echo "wrangler_bin=${wbin:-missing}"
  command -v cf >/dev/null && cf --version || true
  command -v wrangler >/dev/null && wrangler --version || true
} | tee /tmp/cli-pin.txt

if grep -E 'email_routing:read|email_sending:read|unknown OAuth scope|unsupported' "$err"; then
  echo "STOP: client scope catalog. File the CLI pin, not an outage."
  exit 2
fi

echo "No known catalog mismatch in $err. Paste the full log before paging."
```

Tune the `grep` to the verbatim words on your build. Do not invent a regex for a sentence you have not seen on that machine. The public example is “unknown OAuth scope error” plus the two email read names. Copy the real line first. [Source: https://github.com/cloudflare/workers-sdk/releases/tag/%40cloudflare/workers-auth%400.6.9]

For Wrangler, print the catalog the binary thinks it has. Official flag: `--scopes-list`.

```bash
npx wrangler login --scopes-list
```

I do not grep that table for `email_routing:read` and then claim Wrangler has the same bug. The 7 September notes are about `cf auth login`. If the Wrangler table contains a string you do not need, pass `--scopes` with the subset you actually use. Official example: `npx wrangler login --scopes account:read user:read`. [Source: https://developers.cloudflare.com/workers/wrangler/commands/general/]

If you are on SSH, a container, or Codespaces, the default login still wants a browser callback on `localhost:8976`. Wrangler’s device flow (`--device`) exists so you do not invent a “OAuth is down” story for a missing localhost. That path shipped in Wrangler 4.119.0. Use it, or use a token. Do not page. [Source: https://developers.cloudflare.com/changelog/post/2026-08-04-wrangler-login-device-flow/]

## CI never needed this login

The coding agent loves interactive login because that is what the README shows first. CI does not have a human in a browser. Official docs already said so: prefer API tokens in headless environments. [Source: https://developers.cloudflare.com/workers/wrangler/commands/general/]

Create the token in the dashboard, copy it once, store it in the platform secret store. Verify it with the documented endpoint. Do not paste the secret into the PR, into chat, or into `wrangler.jsonc`.

```bash
curl "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  --header "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}"
```

A valid token returns `"status": "active"` and the message that the token is valid and active. [Source: https://developers.cloudflare.com/fundamentals/api/get-started/create-token/]

GitHub Actions then looks like this. The login command is absent on purpose.

```yaml {linenos=inline,hl_lines=["11-13"]}
name: workers-deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - run: npm ci
      - name: Deploy Worker
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
        run: npx wrangler deploy --dry-run
      - name: Reject login in CI scripts
        run: |
          if git grep -nE 'wrangler login|cf auth login' -- .github ':*.yml' ':*.yaml'; then
            echo "Interactive OAuth login is not a CI step."
            exit 1
          fi
```

That gate is narrow on purpose. It does not claim the token has the right Workers permissions. It claims the repository will not absorb a browser login disguised as a deploy fix.

If the token is missing Email Sending or Email Routing on purpose, that is a dashboard permission choice. It is still not `email_routing:read` on an OAuth client. Keep the two lists apart in the ticket. Cloudflare’s API token permission catalog is a different page from the CLI OAuth catalog. [Source: https://developers.cloudflare.com/fundamentals/api/reference/permissions/]

![Browser login stays off CI: laptop OAuth versus CI API token](/img/requested-scopes-before-outage-3.png)

## What the coding agent will try, and what you refuse

A coding agent that sees a red login will still write fluent PHP. Fluent PHP is how we get a Worker deploy from a token pasted into the repo, or a “temporary” `wrangler login` inside GitHub Actions.

I keep the same sequence I use for other agent work. Map the repo. Name the owner. Require an artifact. Then type. The start path for new readers is [/start-here/](/start-here/). The operating hub is [/ai-agent-operations/](/ai-agent-operations/). The merge refusal is still [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/).

Refuse these “fixes” in review:

1. “Cloudflare is down, skip deploy.” You have not copied the scope string yet.
2. “Paste the API token in chat so I can retry.” That is a secret leak, not a diagnosis.
3. “Add `wrangler login` to CI.” CI has no browser. Use the token path.
4. “Request every scope so login works.” The 7 September bug existed because the client requested names the server does not define. More strings is not safer.
5. “Switch the model and try login again.” Login is not a model problem.

August 22 already gave Wrangler and the Cloudflare API MCP server optional scopes on the consent screen. Required scopes stay selected. If a later command needs a scope you declined, re-authorize and grant that one. That is a human consent edit. It is not an outage, and it is not a reason to approve Full access because the agent is impatient. [Source: https://developers.cloudflare.com/changelog/post/2026-08-22-wrangler-mcp-optional-oauth-scopes/]

I also refuse a PR that stores `CLOUDFLARE_API_TOKEN` in `wrangler.jsonc`, `.dev.vars`, or a committed `.env`. Official token docs tell you to copy the secret to a secure place once. CI uses the platform encrypted store. [Source: https://developers.cloudflare.com/fundamentals/api/get-started/create-token/]

```bash
# Tracked files only. Do not scan the secret store.
if git grep -nE 'CLOUDFLARE_API_TOKEN\\s*=' -- ':!*.md' ':!docs' ; then
  echo "Token assignment in git is a leak, not a login fix."
  exit 1
fi
```

If the line is a GitHub Actions `env:` mapping to `${{ secrets.CLOUDFLARE_API_TOKEN }}`, that is the allowed form. If the line is a literal token, reject the PR.

## Who owns the CLI pin

Someone has to own the binary that asked for the bad names. If nobody owns it, every laptop stays on last month’s `npx` cache and the next unknown-scope string becomes another “outage.”

Put two names in the ticket:

1. **CLI pin owner.** Pins `cf` and/or Wrangler for the fleet. Decides when `latest` is allowed.
2. **Token owner.** Creates and rotates `CLOUDFLARE_API_TOKEN` for CI. Never the coding agent.

The pin owner’s Monday check is short. Print versions. Confirm the workers-auth line you actually run is past the 7 September patch if this laptop uses `cf auth login`. Confirm Wrangler is the repo pin, not a global surprise.

```bash
printf 'pwd=%s\n' "$PWD"
git rev-parse --show-toplevel
npx wrangler --version
npm ls wrangler --depth=0 2>/dev/null || true
npm ls @cloudflare/workers-auth --depth=0 2>/dev/null || true
```

If `npx` and `npm ls` disagree, you are not on the repo pin. Stop. That mismatch is how a patched catalog on CI and an old catalog on the laptop tell two different outage stories.

Wrangler auth profiles are a sibling check, not this bug. A profile is a named OAuth login bound to a directory. `CLOUDFLARE_API_TOKEN` still wins in CI. Do not “fix” an unknown-scope error by creating a second profile. [Source: https://developers.cloudflare.com/workers/wrangler/profiles/]

![Two names before the agent types: CLI pin owner and token owner](/img/requested-scopes-before-outage-4.png)

## How this fits the rest of the desk

A login that asked for a name the server never registered will still look like a blocked deploy. A blocked deploy will still look like “stop shipping.” That is how a catalog bug becomes a freeze.

I already treated a why-line as a network ticket, not a green policy, in [Read the Why-Line Before You Trust the Org Policy](/blog/org-policy-why-line/). I already treated a green apt line as a clock, not a key, in [A Green apt Update Is Not a Trusted Key After Saturday](/blog/green-apt-is-not-a-trusted-key/). Login is the same shape. Red text is a classification job. It is not a status-page job.

If the error names `email_routing:read` or `email_sending:read` on `cf auth login`, you are on the 7 September client patch. Upgrade the pin. Resume the agent after `cf --version` (or the package you actually run) shows you are past that patch. If the error names a different unknown scope, copy it. File against the CLI owner. If the error is “cannot open browser,” use `--device` or a token. If CI is the red job, there should be no login command at all.

The question is not whether this demos well in a browser OAuth window. The question is whether the next operator can tell a catalog mismatch from an outage without asking the agent to guess.

## What you should do Monday morning

1. Print `cf --version` and `npx wrangler --version` on the machine you actually deploy from, not on a spare VM.
2. Copy the last login error verbatim into a note. Keep the binary name on the first line.
3. If the error names `email_routing:read` or `email_sending:read`, treat it as a client catalog miss. Pin past the 7 September workers-auth patch. Do not open the status page as the first move.
4. If you use Wrangler interactive login, run `npx wrangler login --scopes-list` once and save the table. Pass `--scopes` with the subset the repo needs.
5. Name two humans: CLI pin owner, token owner. Put both names in the ticket.
6. Confirm CI uses `CLOUDFLARE_API_TOKEN` and never `wrangler login` / `cf auth login`.
7. Run the token verify curl against the secret in the platform store, not against a value in git.
8. Refuse a pull request that “fixes Cloudflare” by pasting a token into chat, into `.dev.vars`, or into `wrangler.jsonc`.
9. Only then resume the coding agent.

## Further reading

{{< source href="https://github.com/cloudflare/workers-sdk/releases/tag/%40cloudflare/workers-auth%400.6.9" label="workers-auth 0.6.9: cf auth login requested unregistered email read scopes" >}}

{{< source href="https://developers.cloudflare.com/workers/wrangler/commands/general/" label="Official Wrangler login: --scopes-list, --scopes, CI uses tokens" >}}

{{< source href="https://developers.cloudflare.com/fundamentals/api/get-started/create-token/" label="Official API token create and /user/tokens/verify" >}}
