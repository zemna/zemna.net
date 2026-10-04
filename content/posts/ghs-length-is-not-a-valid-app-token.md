---
title: "A 40-Character ghs_ Check Is Not a Valid App Token"
date: 2026-10-04T07:00:00+07:00
draft: false
slug: "ghs-length-is-not-a-valid-app-token"
description: "A 40-character check on a ghs_ string is not proof the GitHub App token is invalid. Print length, opacity, and the named App owner before you file a broken-auth ticket."
topics: ["developer-tools"]
tags: ["github", "github-apps", "ghs", "installation-tokens", "coding-agents", "change-control"]
cover: /covers/ghs-length-is-not-a-valid-app-token.png
seo:
  primaryQuery: "GitHub App ghs_ token 40 characters vs 520"
  secondaryQueries:
    - "stateless GitHub App installation token length"
    - "ghs_APPID_JWT opaque string check"
    - "named owner for GitHub App installation token"
---

The junior pastes a CI log. The GitHub App minted a `ghs_` string. The helper printed `invalid token: expected 40 characters`. They file the ticket: “the App token is broken.”

I stop the run there. A 40-character `ghs_` check is not a valid App token. GitHub’s public notes that named this field are blunt: newly minted GitHub App installation tokens still start with `ghs_`, and they are now about 520 characters instead of 40. Permissions, repository scoping, the one-hour expiry, and the installation-token REST endpoint did not change. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/] [Source: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app]

I already refused to treat a redirected dangerous `rm` as always-ask off in [Print the Redirect Before You File Always-Ask Off](/blog/print-the-redirect-before-you-file-always-ask-off/). I already refused to treat a laravel/ai lockfile line as a patched fetch client in [A Laravel/AI Lockfile Line Is Not a Patched Fetch Client](/blog/a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client/). I already refused to treat Copilot’s ready-to-approve line as a required merge vote in [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/). This post is the same desk rule for a GitHub App installation token. Print the length check. Print whether the string was treated as opaque. Name who owns the App answers.

The question is not whether the string is 40 characters. The question is whether the named owner can still tell a length check written for the legacy format from a token that GitHub already minted.

<!--more-->

![Three columns: 40-char check, opaque token, named App owner](/img/ghs-length-is-not-a-valid-app-token-1.png)

## The ticket that looks like a broken token

Juniors treat a `ghs_` string the way they treat a password field. Yesterday the helper accepted 40 characters. Today the helper rejected 520. They page the desk: “GitHub minted garbage” or “the token leaked because it is too long to be real.”

Two jobs collide on that line.

1. **Keep the App token honest.** Official docs: an installation access token authenticates as the App installation. It expires after one hour. The REST call is still `POST /app/installations/{installation_id}/access_tokens`. [Source: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app] [Source: https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/github-credential-types]
2. **Keep the string opaque.** The 2 October 2026 changelog: treat installation tokens as opaque strings. Look for validation that requires tokens to be exactly 40 characters, database columns with a small maximum length, proxies that truncate long `Authorization` headers, and redaction rules that only match the legacy pattern. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/]

If you only screenshot “length is not 40,” you will file broken-auth. You will not file the length check.

{{< note type="warning" title="Do not file broken-auth on a 40-character check" >}}
If a coding agent or a junior says the GitHub App token is invalid because it is not 40 characters, print the check that rejected it, the observed length (not the full secret), whether the string still starts with `ghs_`, and one human name on the App answers. A 40-character check is not a validity check.
{{< /note >}}

I do not invent a fake overnight outage of every GitHub App. I use the public contract. The length field is the ticket, not a version pin in the title.

## What GitHub actually rolled out

Read the 2 October 2026 changelog, then the April notice, then the docs page that still mints the token. Do not trust a social recap. Do not trust this post without those pages.

The named field, published 2 October 2026:

> The staged rollout of the stateless GitHub App installation token format, which began on April 27, 2026, is complete. By default, all newly minted GitHub App installation tokens will be in the stateless `ghs_APPID_JWT` format.

Installation tokens still start with `ghs_`, but they are now about 520 characters long instead of 40. Token permissions, repository scoping, the one-hour expiration, and the installation access token REST API endpoint are unchanged. Tokens minted before the change continue to work until they expire. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/]

That paragraph has three parts. Print all three on the ticket.

| Part | What it is | What it is not |
| --- | --- | --- |
| Prefix `ghs_` | GitHub App installation access token | A classic PAT (`ghp_`), a fine-grained PAT (`github_pat_`), or an OAuth token (`gho_`) |
| About 520 characters | New default length for newly minted installation tokens | Proof the token is truncated, leaked, or forged |
| Unchanged contract | Permissions, repo scope, one-hour expiry, same REST mint endpoint | A new permission you did not grant |

The April 24 notice already warned the field: if your application expects installation tokens to be exactly 40 characters long, it will not handle the new format. Length varies with the data stored in the token. The JWT is signed by a GitHub-internal issuer. Client apps must not validate that JWT and must not take a dependency on its contents. [Source: https://github.blog/changelog/2026-04-24-notice-about-upcoming-new-format-for-github-app-installation-tokens/]

The May 15 note adds a shape check you can print without decoding: a stateless token is a `ghs_`-prefixed JWT. It is longer (about 520 characters) and contains two dots. A stateful token is a short opaque string with no dots. GitHub’s recommended regex for both formats is `ghs_[A-Za-z0-9\.\-_]{36,}`. The old pattern `ghs_[A-Za-z0-9]{36}` does not match the new tokens. [Source: https://github.blog/changelog/2026-05-15-github-app-installation-tokens-per-request-override-header/]

{{< details summary="Where the pin sits after the decision, not in the title" >}}
Staged rollout began 27 April 2026. The per-request header `X-GitHub-Stateless-S2S-Token` on `POST /app/installations/:installation_id/access_tokens` forced `enabled` (stateless) or `disabled` (classic opaque) during the rollout. GitHub will deprecate that header on 30 November 2026. After that date GitHub will no longer respect the header, and all eligible apps always receive stateless tokens. Remove the header from production before that date. Scope in the public notes: GitHub Enterprise Cloud and Data Residency. GitHub Enterprise Server is not impacted. The format change applies to GitHub App installation server-to-server tokens, including Actions `GITHUB_TOKEN`. Do not put the header name or the November date in the title. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/] [Source: https://github.blog/changelog/2026-05-15-github-app-installation-tokens-per-request-override-header/]
{{< /details >}}

## Four checks before you file

A mid-senior screenshots this list. A junior who only has the log still has a ticket they can close.

1. **Print the check, not the secret.** If the helper says `len == 40` or `len != 40`, that is the ticket. Do not paste the full `ghs_` string into Slack. Print prefix, length, and whether two dots sit after `ghs_`.
2. **Mark opaque vs decoded.** If any line splits the token on `.` and inspects payload claims, that is a second ticket. GitHub says the JWT is internal and clients must not validate it. [Source: https://github.blog/changelog/2026-04-24-notice-about-upcoming-new-format-for-github-app-installation-tokens/]
3. **Mark storage and headers.** `VARCHAR(40)`, a 64-byte secret box, or a proxy that truncates `Authorization` will fail this field even when GitHub minted a good token. GitHub names those three places on the 2 October page. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/]
4. **Write one human name.** `GITHUB_APP_TOKEN_OWNER`. A coding agent does not own the App answers. A Slack channel does not own them.

![Four checks: Print the length check, Treat token as opaque, Check storage headers, Named App owner](/img/ghs-length-is-not-a-valid-app-token-2.png)

Those four lines are the whole post. Everything below is how you print them without turning this page into a token-bypass recipe.

## Print the length without minting a live token

Do not mint a production installation token to “prove” the new length. Do not log a live `ghs_` string. The public changelog already states 40 versus about 520. You need a classifier on a logged check, plus synthetic fixtures.

Copy this probe. It classifies a string. It never calls GitHub. It never prints the secret.

```python
#!/usr/bin/env python3
"""Classify a ghs_ string shape. Never mint. Never print the secret."""
from __future__ import annotations

import re
import sys

PREFIX = "ghs_"
LEGACY_EXACT = 40
STATELESS_ABOUT = 520
BOTH_FORMATS = re.compile(r"^ghs_[A-Za-z0-9.\-_]{36,}$")
LEGACY_EXACT_RE = re.compile(r"^ghs_[A-Za-z0-9]{36}$")


def redact(token: str) -> str:
    if not token.startswith(PREFIX):
        return f"len={len(token)} prefix=other"
    return f"ghs_… len={len(token)} dots_after_prefix={token[len(PREFIX):].count('.')}"


def classify(token: str) -> dict[str, bool | str | int]:
    after = token[len(PREFIX) :] if token.startswith(PREFIX) else ""
    dots = after.count(".")
    length = len(token)
    return {
        "redacted": redact(token),
        "length": length,
        "starts_with_ghs": token.startswith(PREFIX),
        "legacy_exact_40": length == LEGACY_EXACT,
        "about_520": abs(length - STATELESS_ABOUT) <= 40,
        "dots_after_prefix": dots,
        "looks_stateless_jwt_shape": token.startswith(PREFIX) and dots == 2,
        "matches_both_formats_regex": bool(BOTH_FORMATS.match(token)),
        "matches_legacy_exact_regex": bool(LEGACY_EXACT_RE.match(token)),
        "this_field": token.startswith(PREFIX)
        and length != LEGACY_EXACT
        and (dots == 2 or abs(length - STATELESS_ABOUT) <= 40),
    }


def main() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        print("empty")
        return 2
    info = classify(raw)
    for key, value in info.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it against fixtures you generated locally, not against a minted secret:

```python
#!/usr/bin/env python3
"""Synthetic fixtures only. Do not paste a live ghs_ token here."""
from probe_ghs_length import classify

LEGACY = "ghs_" + ("A" * 36)  # 40 chars, no dots
# Shape only: prefix + app id + two-dot JWT-like body. Not a GitHub signature.
STATELESS = "ghs_123456_" + ("B" * 80) + "." + ("C" * 200) + "." + ("D" * 200)


def main() -> None:
    legacy = classify(LEGACY)
    stateless = classify(STATELESS)
    assert legacy["length"] == 40
    assert legacy["dots_after_prefix"] == 0
    assert legacy["this_field"] is False
    assert stateless["starts_with_ghs"] is True
    assert stateless["dots_after_prefix"] == 2
    assert stateless["length"] != 40
    assert stateless["this_field"] is True
    print("legacy", legacy["redacted"])
    print("stateless", stateless["redacted"])


if __name__ == "__main__":
    main()
```

A helper that still does `if len(token) != 40: raise` will reject the second fixture and accept the first. That helper is this field. GitHub already told you the second fixture is the new default shape. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/] [Source: https://github.blog/changelog/2026-05-15-github-app-installation-tokens-per-request-override-header/]

Scan the repo for the check. This search does not mint a token.

```python
#!/usr/bin/env python3
"""Find length==40 / VARCHAR(40) checks. Read-only. No network."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(".")
NEEDLES = [
    re.compile(r"len\([^)]*\)\s*==\s*40"),
    re.compile(r"len\([^)]*\)\s*!=\s*40"),
    re.compile(r"length\s*==\s*40"),
    re.compile(r"ghs_\[[A-Za-z0-9]+\]\{36\}"),
    re.compile(r"varchar\s*\(\s*40\s*\)", re.I),
    re.compile(r"VARCHAR2\s*\(\s*40\s*\)", re.I),
]


def main() -> int:
    hits = 0
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".py", ".php", ".js", ".ts", ".go", ".rb", ".sql"}:
            continue
        if any(part in {".git", "vendor", "node_modules"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if any(n.search(line) for n in NEEDLES):
                print(f"{path}:{i}:{line.strip()[:160]}")
                hits += 1
    print(f"hits={hits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

If the scan prints `len(token) == 40` next to a `ghs_` helper, you have this field. If the scan prints nothing, do not file this post’s ticket. File storage, proxy truncation, or a different prefix.

![Flow: ghs_ prefix, length not 40, two dots, named owner](/img/ghs-length-is-not-a-valid-app-token-3.png)

Official mint path, for the owner who still needs the endpoint on the ticket. This is the documented call. It is not a bypass. Replace the placeholders. Do not commit the JWT.

```bash
# Documented mint. Placeholders only. Do not log the response token.
curl --request POST \
  --url "https://api.github.com/app/installations/INSTALLATION_ID/access_tokens" \
  --header "Accept: application/vnd.github+json" \
  --header "Authorization: Bearer JWT" \
  --header "X-GitHub-Api-Version: 2026-03-10"
```

[Source: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app]

After you mint in a throwaway shell, print `len` and prefix only. Then delete the shell history line. Do not paste the body into the ticket.

## Neighbor tickets that are not this field

Print these so a junior does not collapse every `ghs_` headline into a length check.

1. **Expired after one hour.** Installation access tokens expire after one hour. A 520-character string that GitHub minted at 07:00 and a 401 at 08:05 is expiry, not length. [Source: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app] [Source: https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/github-credential-types]
2. **Wrong prefix.** `ghp_`, `github_pat_`, `gho_`, `ghu_`, and `ghr_` are other credential types. A 40-character check on a classic PAT is a different ticket. [Source: https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/github-credential-types]
3. **Header still in production after 30 November 2026.** `X-GitHub-Stateless-S2S-Token` is a temporary override. GitHub will stop respecting it on 30 November 2026. Leaving `disabled` in production is not a length check and is not a permanent opt-out. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/]
4. **Client JWT validation.** Splitting the token and verifying GitHub’s internal issuer is the opposite of the April notice. Do not “fix” length by decoding claims. [Source: https://github.blog/changelog/2026-04-24-notice-about-upcoming-new-format-for-github-app-installation-tokens/]
5. **A laravel/ai lockfile line.** Fetch client, not a GitHub App token. Already a post. [Source: https://zemna.net/blog/a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client/]
6. **A redirected dangerous `rm`.** Always-ask, not `ghs_`. Already a post. [Source: https://zemna.net/blog/print-the-redirect-before-you-file-always-ask-off/]
7. **Copilot approve.** A ready-to-approve line is not a merge vote. Already a post. [Source: https://zemna.net/blog/leave-copilot-approve-off/]

If the log says `401` and `len=40` on a token minted 90 minutes ago, you are on neighbor 1. If the log says `len=520` and `expected 40`, you are on this field.

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a GitHub App that opens pull requests from CI, a coding agent that copies a “token must be 40 characters” helper from an old gist, and a `VARCHAR(64)` column that truncates the new string before the API call. I treat `GITHUB_APP_TOKEN_OWNER` the same way I treat a migration owner. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “did this helper reject a `ghs_` string because it was not 40 characters.” A coding agent does not get to close a broken-auth ticket because the length check failed. I already wrote the sibling rule for a lockfile line that is not a patched fetch client, and for a redirect that is not always-ask off. This is the sibling for a length check that is not a valid App token.
{{< /field-note >}}

## What you must not do

Forbidden:

1. File “the App token is invalid” without printing the check, the observed length, the prefix, and one human name.
2. Put `ghs_APPID_JWT`, `520`, or `2 October 2026` in the title as a version-style hook. The numbers are evidence after the decision.
3. Paste a live installation token into Slack, the wiki, or this ticket.
4. Decode the JWT payload and treat claims as an App permission grant.
5. Leave `X-GitHub-Stateless-S2S-Token: disabled` in production as a permanent opt-out. GitHub deprecates the header on 30 November 2026. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/]
6. Write a token-bypass recipe: forging `ghs_` strings, skipping App authentication, or widening permissions because the length check failed.
7. Treat GitHub Enterprise Server as this rollout. Public notes say GHES is not impacted. [Source: https://github.blog/changelog/2026-04-24-notice-about-upcoming-new-format-for-github-app-installation-tokens/]
8. Mix this field with expiry, a classic PAT, a laravel/ai lockfile line, or a redirected `rm`. Those are other posts.
9. Recommend buying a scanner, a seat, or a plan because a helper rejected 520 characters.
10. Clone the lockfile post, the redirected-rm post, the sandbox-equals post, or the runner-deadline post as a synonym. Those URLs already shipped. GSC this week has no striking-distance query that asks for another copy.

Allowed:

1. Print prefix, length, and dots. Redact the rest.
2. Classify synthetic fixtures with `probe_ghs_length.py`. Do not mint to demo.
3. Scan the repo for `len == 40` and `VARCHAR(40)`.
4. Name one human as `GITHUB_APP_TOKEN_OWNER`.
5. Widen storage to at least 520 characters after the owner prints the column.
6. Remove the temporary header from production once both shapes are accepted, and before 30 November 2026.
7. Keep expiry, wrong-prefix, and JWT-decoding as separate tickets.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about 520 characters is not permission to skip the four lines.

![Print four lines: Check, Length, Prefix, Owner](/img/ghs-length-is-not-a-valid-app-token-4.png)

## What you should do Monday morning

1. Open the repo that actually ships the GitHub App. Export `GITHUB_APP_TOKEN_OWNER` to a human name. Run the length-check scanner. Write `this_field=True` or `False` on the ticket next to that name.
2. For every `this_field=True` row, answer in one sentence: the helper rejected a `ghs_` string because length was not 40, or it rejected it for another reason. If you cannot answer, the ticket is “owner missing,” not “token invalid.”
3. Print storage: column type, secret-box max length, and any proxy that truncates `Authorization`. If the column is shorter than 520, file storage, then length. GitHub names both. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/]
4. If someone pastes `X-GitHub-Stateless-S2S-Token: disabled` as the close of this ticket, split it. Header removal is a dated change-control item (30 November 2026), not a length check. [Source: https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/]
5. Confirm coding-agent instructions on this desk name the same owner and forbid “token invalid” without the four lines. Forbid pasting a live `ghs_` string. Forbid decoding the JWT.
6. Confirm the mint still uses `POST /app/installations/{id}/access_tokens` with an App JWT in `Authorization: Bearer`. Do not invent a second mint path. [Source: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app]

The question is not whether the changelog demos well in a gist. The question is whether the named owner can still tell a 40-character check from a token GitHub already minted after handoff.

## Further reading

{{< source href="https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/" label="GitHub Changelog — Stateless GitHub App installation tokens rolled out" >}}

{{< source href="https://github.blog/changelog/2026-05-15-github-app-installation-tokens-per-request-override-header/" label="GitHub Changelog — Per-request override header" >}}

{{< source href="https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app" label="GitHub Docs — Generating an installation access token" >}}
