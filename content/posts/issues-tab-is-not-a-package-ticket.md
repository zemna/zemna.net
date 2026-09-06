---
title: "An Issues Tab Is Not a Laravel Package Ticket"
date: 2026-09-06T07:00:00+07:00
draft: false
slug: "issues-tab-is-not-a-package-ticket"
description: "GitHub Issues are off on most Laravel packages. The ticket is a pull request that documents the bug, with a named owner. laravel/framework Issues stay on."
topics: ["software-engineering"]
tags: ["laravel", "github-issues", "pull-requests", "coding-agents", "open-source", "socialite", "change-control"]
cover: /covers/issues-tab-is-not-a-package-ticket.png
seo:
  primaryQuery: "Laravel package GitHub issues disabled pull request"
  secondaryQueries:
    - "laravel socialite issues disabled open a PR"
    - "laravel framework issues still enabled"
    - "coding agent bug report as pull request"
---

The junior opens `laravel/socialite` and looks for the Issues tab. GitHub has nothing to click. Standup hears “we cannot file the OAuth bug.” The coding agent offers to post in Discord instead.

I stop the run there. A missing Issues tab is not a missing ticket. On most Laravel packages this week, the ticket is a pull request that names the failure. The chat thread is gossip.

Taylor Otwell wrote the rule in public on 3 September 2026: last week he disabled GitHub Issues on most Laravel open-source packages. If you hit a bug, describe it to a coding agent and open a PR. Even if the code is not great, iterate. The PR still documents the problem. Laravel News restated it on 4 September: this is for packages, not the main Laravel repo. [Source: https://x.com/taylorotwell/status/2095516796748996843] [Source: https://laravel-news.com/taylor-disabled-github-issues]

I already refused to treat a green `apt` line as a trusted key in [A Green apt Update Is Not a Trusted Key After Saturday](/blog/green-apt-is-not-a-trusted-key/). I already refused to treat one Copilot exclusion list as every surface in [Name the Copilot Surface Before You Trust the Exclusion List](/blog/name-the-copilot-exclusion-surface/). This post is the contribution-path version of the same desk rule. Name the repo. Name whether Issues are on. Name who owns the PR that documents the bug.

The question is not whether Taylor is “right about open source.” The question is whether your next Socialite failure becomes a fork, a Discord ping, or a PR a maintainer can review.

<!--more-->

![Issues tab is not the ticket: blank tab, failing test, named human opens a pull request](/img/issues-tab-is-not-a-package-ticket-1.png)

## The click that looks like a support desk

Juniors treat the Issues tab the way they treat a ticket queue. Empty tab. No queue. Stop.

GitHub does not work that way on these repos now. I checked the public API this morning, 6 September 2026, without inventing a list:

| Repo | `has_issues` | What that means on this desk |
| --- | --- | --- |
| `laravel/socialite` | `false` | Package. Do not hunt an Issues form. Document the bug in a PR. |
| `laravel/sanctum` | `false` | Same package rule. |
| `laravel/framework` | `true` | Framework Issues stay on. A framework bug still belongs there unless the contributing guide says otherwise. |

[Source: https://api.github.com/repos/laravel/socialite] [Source: https://api.github.com/repos/laravel/sanctum] [Source: https://api.github.com/repos/laravel/framework]

Taylor’s follow-up on the same day is the sentence I keep: people are struggling with this; Issues on the framework are still enabled; Issues on, for example, Socialite, are disabled; there were very few issues on these repositories. [Source: https://x.com/taylorotwell]

`open_issues_count` on a package repo is not a pile of bug tickets. GitHub’s REST API treats every pull request as an issue, so that field still counts open PRs when Issues are off. [Source: https://docs.github.com/en/rest/issues/issues] Socialite showed `has_issues=false` and `open_issues_count=3` on this run. Those three are PRs, not a hidden Issues queue. If a junior reads “3 issues” and opens a hunt for a form, they misread the API.

The desk rule is shorter than the timeline:

1. Package repo, Issues off → the artifact is a pull request.
2. Framework repo, Issues on → the artifact is still an issue until a maintainer asks for a PR.
3. A named human owns the PR body that states the failure, the version, and the test.

I do not let a coding agent “file the bug” by pasting the stack trace into a Slack channel titled `#laravel`. That is not documentation. That is a disappearing message.

{{< note type="warning" title="The tab is not the queue" >}}
If `has_issues` is false, `gh issue create` is the wrong tool. Fork, branch, failing test, pull request. Chat that says “I reported it” with no URL is not a ticket.
{{< /note >}}

{{< field-note title="Field note" >}}
On the Laravel and Vue SaaS apps I keep in production, Socialite and Sanctum sit in `composer.json` next to application code. When OAuth redirects break after a provider change, the junior’s first move is still the GitHub Issues search box. That box is gone on the package. The useful move is the same shape I use on [/laravel-vue-saas/](/laravel-vue-saas/): reproduce in the app, write the smallest failing test against the package API, open a PR with a named reviewer. Copilot does not get to open the PR. The person who already owns merge rights on this desk — I already refused to give a coding agent merge rights in [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/) — also owns “does this PR state the bug in one paragraph a maintainer can read.”
{{< /field-note >}}

## How I prove Issues are off before anyone types

Do not argue from a screenshot of a 404. Ask the repository object.

```bash {linenos=inline,hl_lines=[8,"12-14"]}
#!/usr/bin/env bash
set -euo pipefail
# Usage: ./check-issues-path.sh laravel/socialite
repo="${1:?owner/name}"

curl -sS -A "zemna-desk-check" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/${repo}" \
  | python3 -c '
import json, sys
d = json.load(sys.stdin)
name = d["full_name"]
flag = d["has_issues"]
prs = d["open_issues_count"]
print(f"{name} has_issues={flag} open_issues_count={prs}")
if flag:
    print("PATH=issues-or-pr (framework-style). Read CONTRIBUTING first.")
    raise SystemExit(0)
print("PATH=pull-request-only. Do not run gh issue create.")
raise SystemExit(2)
'
```

Exit 2 is the package path. I paste that line into the ticket on our side before anyone clones. Exit 0 is not “open an issue immediately.” It is “read the contributing file, then decide.”

A one-year developer can run this. They do not need a lecture about maintainer burnout. They need a boolean.

If the agent “already knows” Socialite has Issues because last month’s blog said so, throw the memory out. Settings change in a week. The API on this morning is the inventory.

![Package Issues off on Socialite and Sanctum; framework Issues on](/img/issues-tab-is-not-a-package-ticket-2.png)

## What “describe it to a coding agent” is allowed to mean

Taylor’s sentence is easy to abuse. A junior hears “coding agent” and dumps the whole vendor directory into a chat. The agent writes a 400-line patch that rewrites Socialite’s provider map. That is not the request.

The allowed agent job is a brief, then a failing test, then a small diff.

```text
You are not filing a GitHub Issue. Issues are disabled on this package.

Write a pull request that documents one failure.

Required in the PR body:
1. Package name and composer version we actually installed.
2. One paragraph: what we called, what we expected, what we got.
3. The smallest public API that fails. No app controllers.
4. A test that fails on current main and passes on this branch.

Forbidden:
- Rewriting the provider list “while we are here.”
- Adding a new OAuth provider.
- Closing with “let me know if you want more.”
- Claiming the Issues tab is broken. It is off on purpose.

Human owner of this PR: <name>. You draft. I open.
```

That prompt is the contribution contract. It is the same shape as [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/): the model drafts, a named human still clicks.

A realistic test is boring. It does not invent a Socialite CVE. It pins the behavior you already reproduced in the app:

```php
<?php

namespace Tests;

use Laravel\Socialite\Two\User;
use PHPUnit\Framework\TestCase;

final class OauthUserMappingTest extends TestCase
{
    public function test_email_stays_null_when_provider_omits_it(): void
    {
        $user = (new User)->map([
            'id' => 'abc',
            'nickname' => 'desk',
            'name' => 'Desk User',
            'email' => null,
            'avatar' => null,
        ]);

        $this->assertSame('abc', $user->getId());
        $this->assertNull($user->getEmail());
    }
}
```

Replace the mapping with the actual failure you have. Do not paste this test into a PR if your bug is a redirect URI. The point is the shape: public API, one assertion family, no application HTTP kernel.

Then the human opens the PR:

```bash
git checkout -b fix/document-null-email-from-provider
# add the failing test, then the smallest production change
git add -A
git commit -m "Document null email when the provider omits it"

gh pr create \
  --repo laravel/socialite \
  --title "Document null email when the provider omits it" \
  --body "$(cat <<'EOF'
## Failure
Composer package: laravel/socialite (version from composer.lock).
Call: User::map() with email key set to null.
Expected: getEmail() returns null.
Actual: <paste the actual return>.

## Why a PR
Issues are disabled on this package. This PR is the ticket.

Owner on our desk: <name>. Agent drafted the test. I ran it.
EOF
)"
```

If `gh pr create` is blocked because you have no fork, that is an access problem, not an Issues problem. Fork first. Do not reopen a debate about the Issues tab.

## Package versus framework, in one table I will not expand into drama

I am not writing a Taylor thinkpiece. I am writing a routing table.

| Surface | Issues | Your next artifact |
| --- | --- | --- |
| Laravel package (`socialite`, `sanctum`, same family Taylor named) | Off | Pull request that documents the bug |
| `laravel/framework` | On | Issue first unless `CONTRIBUTING.md` says to send a PR with a test |
| Your application repo | Your setting | Your ticket tracker. Do not file app bugs on Socialite. |
| Discord / X replies under the announcement | Noise | Not a ticket. Do not paste secrets there. |

Framework Issues staying on is not a loophole for package bugs. A Socialite mapping bug filed on `laravel/framework` is a misroute. Maintainers already said they were drowning in the old flow. Sending the package failure to the framework queue is how you recreate the queue on the one repo that still accepts Issues.

The opposite experiment exists, and I will not flatten it. On 19 August 2026 Fabien Potencier wrote that Symfony Language Tools disables pull requests and keeps Issues, because the reporter’s context is the scarce part and an agent can implement from a good issue. That experiment is only for `symfony/language-tools`. `symfony/symfony` still takes PRs. [Source: https://symfony.com/blog/experimenting-with-issue-first-open-source-contributions]

Two maintainers, two defaults, same year. Your job is to read the repo you are standing in, not to pick a side in a timeline argument.

![Read has_issues, write a failing test, human opens the PR; no issue create](/img/issues-tab-is-not-a-package-ticket-3.png)

## What I refuse to let a coding agent do with this news

This is a coding-agent week. The model will see “Issues disabled” and offer four “fixes.” I refuse all four.

**Open an issue anyway.** `gh issue create` against Socialite. GitHub rejects it or the form is gone. The agent retries three times and calls the platform broken. The platform is doing what the maintainer asked.

**File it on framework because that tab still works.** That moves package noise onto the one Laravel repo that kept Issues. I close that draft and point at `has_issues` on the package.

**Skip the test and send a 20-file refactor.** Taylor said even imperfect code is fine because it documents the problem. That is not permission to rewrite the package. A PR that does not state the failure in the first paragraph is not documentation. It is a drive-by.

**Declare the package unmaintained and vendor a fork in `composer.json` the same afternoon.** A missing Issues tab is not an abandoned repo. Socialite still accepts pull requests. Forking without a PR is how you inherit a private Socialite in six months with no owner.

The allowed agent job is narrower: read `has_issues`, write the failing test, draft the PR body, stop. A named human runs the test and opens the PR. That is the same recovery shape I already use on [/ai-agent-operations/](/ai-agent-operations/): an artifact on GitHub, not a chat that said “reported.”

Keep this next to [/developer-tools/](/developer-tools/) and [/start-here/](/start-here/). A pipeline that lets an agent open GitHub Issues on a package that turned them off is not an operations desk. It is a hope.

## Ordinary misses, not a thriller

The misses are boring. I am not going to invent a Socialite outage.

**The app bug is not a package bug.** Wrong `redirect` in `config/services.php`. The junior wants to “file Socialite.” I ask for the smallest repro outside the app. If the repro needs our domain and our session cookie, it stays in our tracker. Opening a PR on Socialite for our config is how you burn a maintainer’s morning.

**The agent cites last month’s contributing guide.** Cached docs still say “open an issue.” The API says `has_issues=false`. The API wins. Update the internal runbook in the same PR you use to teach the team.

**Someone pastes a customer access token into the PR body “for reproduction.”** A PR is public. Redact. Use a fake id. If the only repro is a live token, you do not have a package report. You have a security incident on your side.

**The PR title is `fix stuff` and the body is the agent’s chain of thought.** Maintainers asked for a document of the problem. The first eight lines must state the failure. I reject the draft and ask for those eight lines before `gh pr create`.

**A junior treats framework Issues as the new mega-queue for every Laravel package.** That recreates the burden Taylor turned off. Package bug, package repo, pull request.

These are the same family as “a green cron exit is not a finished job,” which I already wrote about and will not rewrite. The artifact here is the pull request URL. Show it.

![Refuse issue create, framework dump, twenty-file refactor, silent fork; named human opens the PR](/img/issues-tab-is-not-a-package-ticket-4.png)

## What you should do Monday morning

Do not wait for a Socialite incident. Run the inventory while the team still thinks Issues are a default.

1. Pick the Laravel packages you actually require. Start with `composer show laravel/socialite` and `composer show laravel/sanctum` if those names are in the lockfile. If you cannot name the packages, you do not have an inventory. Stop there and make the list.
2. Run `check-issues-path.sh owner/name` for each. Record `has_issues` in the internal runbook. False means PR path. True means read `CONTRIBUTING.md`.
3. Add one line to the coding-agent instructions: “If `has_issues` is false, do not call `gh issue create`. Draft a PR body and a failing test. A named human opens the PR.”
4. Pick one real bug you have been sitting on — mapping, redirect, or token refresh — and decide in writing: application ticket, or package PR. If you cannot decide, it is an application ticket.
5. If it is a package PR, open it with an owner name in the body. Do not leave the agent as the author of record on GitHub unless that is a person who will answer review comments.
6. Tell standup the three-line rule. Screenshot it. Link this post from [/laravel-vue-saas/](/laravel-vue-saas/) so juniors see the pattern: a missing Issues tab is a routing rule, not a dead project.

The Monday test is short: can a one-year developer point at Socialite and say, out loud, “the ticket is a pull request”? If they say “we cannot report bugs anymore,” you do not have a contribution path. You have a missing tab.

## Further reading

{{< source href="https://laravel-news.com/taylor-disabled-github-issues" label="Taylor disabled GitHub Issues on most Laravel open-source packages (Laravel News, 4 Sep 2026)" >}}

{{< source href="https://x.com/taylorotwell/status/2095516796748996843" label="Taylor Otwell on X: packages Issues off; describe the bug to a coding agent and open a PR (3 Sep 2026)" >}}

{{< source href="https://symfony.com/blog/experimenting-with-issue-first-open-source-contributions" label="Experimenting with Issue-First Open Source Contributions (Symfony Language Tools only, 19 Aug 2026)" >}}

Related on this site: [A Green apt Update Is Not a Trusted Key After Saturday](/blog/green-apt-is-not-a-trusted-key/), [Name the Copilot Surface Before You Trust the Exclusion List](/blog/name-the-copilot-exclusion-surface/), [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/), [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/), and the hubs at [/laravel-vue-saas/](/laravel-vue-saas/), [/ai-agent-operations/](/ai-agent-operations/), [/developer-tools/](/developer-tools/), and [/start-here/](/start-here/).
