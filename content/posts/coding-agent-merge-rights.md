---
title: "I Do Not Give a Coding Agent Merge Rights"
date: 2026-08-28T07:00:00+07:00
draft: false
slug: "coding-agent-merge-rights"
description: "A coding agent may open the pull request. A named human still owns the merge click. Treat GitHub agent merge and auto-merge as opt-in shortcuts, never as the default."
topics: ["developer-tools"]
tags: ["coding-agents", "github", "pull-requests", "merge", "branch-protection", "copilot", "code-review"]
cover: /covers/coding-agent-merge-rights.png
seo:
  primaryQuery: "coding agent merge rights"
  secondaryQueries:
    - "GitHub Copilot agent merge human review"
    - "do not let AI merge pull requests"
    - "named human merge owner for agent PRs"
---

The pull request is green. The agent asked for review. Someone is in a standup and enables **agent merge** so the branch can land while they talk.

That is the moment I stop the run. The agent may write the branch. The agent may push commits. The agent may request review. The merge button stays with a named human.

GitHub already treats Copilot pull requests as work that needs a human pass. The docs say to check the diff thoroughly before merging, and if the repository requires approvals, **your** approval of a Copilot pull request does not count toward that number. Another reviewer has to approve. [Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output]

I use that as policy, not as a product footnote. The question is not whether the agent can land the PR. The question is whether a person with a name still owns the click when the deploy path is Laravel, Vue, and a Monday morning database.

<!--more-->

![Coding agent stops here: Open PR, Review, then a named human merge](/img/coding-agent-merge-rights-1.png)

## The merge click is the product decision

A coding agent is useful when the work is bounded: tests, docs, a small refactor, a fixture. GitHub's own walkthrough for the coding agent is issue → plan → pull request → **you** review. Copilot tags you. You approve, comment, or ask for changes. Then the change follows the repo's merge and deploy process. The person who created the issue is not the final approver. [Source: https://github.blog/ai-and-ml/github-copilot/assigning-and-completing-issues-with-coding-agent-in-github-copilot/]

That last sentence is the whole article.

Teams still skip it because three lights look like permission:

1. CI is green.
2. Copilot code review left a thumbs-up.
3. The PR description reads like a release note.

None of those lights is a merge owner. Green CI means the checks you wired ran. Copilot review is another agent reading the same branch. A fluent description is a writing skill, not a rollback plan.

I already wrote the pre-edit side of this in [the agent edit contract](/blog/the-agent-edit-contract-i-use-before-a-coding-agent-touches-a-repo/): map, boundary, test command, artifact, rollback. I already wrote the policy side in [coding-agent policy as change control](/blog/coding-agent-policy-change-control/): instruction files are governed, not a sticky note. Today's refusal is the last gate those posts assumed. If the agent can merge, the contract was theatre.

{{< note type="warning" title="Green checks do not click Merge" >}}
A required status check answers “did this command pass.” Merge answers “does this change belong on the branch we deploy.” Keep those questions on different people when the author is an agent.
{{< /note >}}

## What GitHub actually ships (and what it still asks you to click)

I am not arguing with the vendor. I am reading the buttons.

**Cloud agent / coding agent.** You assign an issue. Copilot opens a branch and a pull request, pushes as it works, then requests review. GitHub Actions workflows **do not run automatically** when Copilot pushes. You click **Approve and run workflows** in the merge box, unless a repository administrator turns that protection off. GitHub's changelog is blunt about the default: Copilot is treated like an outside contributor; workflows stay quiet until a human approves them, because Actions can reach tokens and secrets. [Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output] [Source: https://github.blog/changelog/2026-03-13-optionally-skip-approval-for-copilot-coding-agent-actions-workflows/]

That default exists because an agent PR that edits `.github/workflows/` is not “just another refactor.”

**Required reviews.** If the repo requires pull request approvals, the person who asked Copilot to open the PR does not satisfy that requirement by approving Copilot's work. Another reviewer must approve. [Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output]

**Agent merge in the Copilot app.** This is the new temptation. GitHub documents it in one paragraph: when **you** want to merge, you enable **agent merge** at the top of the app. The session then reads the pull request, tries to fix what is blocking it, and merges **as soon as GitHub allows**. It runs in the background and turns itself off after the merge. [Source: https://docs.github.com/en/copilot/how-tos/github-copilot-app/managing-issues-and-pull-requests]

Read the subject of that sentence. **You** enable it. The agent does not wake up with merge rights. You handed it the last meter.

**Classic auto-merge.** Same shape. People with **write** permission enable auto-merge on a pull request that cannot merge yet. GitHub merges later, after required reviews and status checks pass. Auto-merge is available on public repos with Free, and on public and private repos with Pro, Team, and Enterprise. [Source: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request]

Auto-merge is a queue, not a personality. If a human with write access turns it on for an agent PR, the human still made the merge decision. They just scheduled it.

**Teams + extra approval.** On 21 August 2026 GitHub shipped shared Copilot sessions from Microsoft Teams. Repository administrators can require **an additional approval** for pull requests attributed to the Teams Copilot integration identity. If the repo already requires two approvals, that setting makes three for those Copilot-created PRs. GitHub's stated reason: keep a human in the loop before agent-authored work ships. [Source: https://github.blog/changelog/2026-08-21-shared-agentic-work-with-github-copilot-in-microsoft-teams/]

That is current product behavior, not a manifesto. I treat it as the floor, not a feature to disable so the standup can go faster.

![Four stations: issue assigned, PR opened, approve Actions, named human merges](/img/coding-agent-merge-rights-2.png)

## Write access is already merge access unless the branch says no

Here is the token trap that junior developers hit in the first week.

A fine-grained GitHub token with `contents: write` can push. The same permission is what `gh pr merge` needs. There is no first-class “open PRs but never merge” bit. GitHub users have asked for that split; the discussion is public. Until it exists, **branch protection and rulesets are the wall**, not the PAT form. [Source: https://github.com/orgs/community/discussions/182732]

So the operational rule is simple:

- The agent token may push to an agent branch (`copilot/…`, `agent/…`).
- `main` (or `production`) requires a pull request, required checks, and required reviews from people who are not the agent.
- Nobody enables auto-merge or agent merge on that PR except the named merge owner.
- CODEOWNERS covers migrations, workflows, auth, and billing paths.

Protected branches already support “require pull request reviews before merging,” code owners, dismissing stale approvals, and “the most recent reviewable push must be approved by someone other than the person who pushed it.” [Source: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches]

That last option matters for agent PRs. The agent can keep pushing “one more fix” after you looked. If stale approvals are not dismissed, you merged a different diff than the one you read.

{{< details summary="What I put on main before an agent is allowed to open PRs" >}}
Require a pull request. Require the test workflow and the merge-owner check below. Require one approving review from someone with write access who is not the PR author. Dismiss stale reviews on new pushes. Restrict who can push to `main`. Do not add the agent (or the automation identity) as a bypass actor “to keep CI moving.”
{{< /details >}}

## A merge-owner check you can run on Monday

I do not want a philosophy channel. I want a failing check with a person's GitHub login on it.

The label format is `merge-owner:<github-login>`. The check fails on agent-looking authors until that label exists and matches a real collaborator. It never calls the merge API.

```yaml {linenos=inline,hl_lines=[18,"24-28"]}
# .github/workflows/agent-merge-owner.yml
name: agent-merge-owner
on:
  pull_request:
    types: [opened, reopened, labeled, unlabeled, ready_for_review, synchronize]

jobs:
  named-human:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: read
    steps:
      - name: Require a named merge owner on agent pull requests
        env:
          AUTHOR: ${{ github.event.pull_request.user.login }}
          AUTHOR_TYPE: ${{ github.event.pull_request.user.type }}
          LABELS: ${{ join(github.event.pull_request.labels.*.name, ',') }}
        run: |
          set -eu
          author_lc=$(printf '%s' "$AUTHOR" | tr '[:upper:]' '[:lower:]')
          looks_agent=0
          # Starting denylist only. Copilot PR authors show up as Copilot in
          # the UI; confirm the login in your org and keep this list in git.
          case "$author_lc" in
            copilot|*[bot]*) looks_agent=1 ;;
          esac
          if [ "$AUTHOR_TYPE" = "Bot" ]; then
            looks_agent=1
          fi
          if [ "$looks_agent" -eq 0 ]; then
            echo "Human-looking author $AUTHOR; merge-owner label optional"
            exit 0
          fi
          echo "$LABELS" | tr ',' '\n' | grep -E '^merge-owner:[A-Za-z0-9-]+$' > /tmp/owners || true
          if [ ! -s /tmp/owners ]; then
            echo "Agent PR from $AUTHOR needs label merge-owner:<github-login>"
            exit 1
          fi
          echo "Merge owner label present:"
          cat /tmp/owners
```

That workflow is a seatbelt. It does not replace review. A label is cheap. Reading the diff is the job.

For protected paths I still want CODEOWNERS, because a label on the PR does not mean the migration file had a DBA look at it:

```text
# .github/CODEOWNERS
/.github/workflows/ @desk-lead
/database/migrations/ @desk-lead
/app/Http/Middleware/ @desk-lead
/routes/ @desk-lead
```

Replace `@desk-lead` with the GitHub user or team that actually gets paged. A team named `frontend` is not a merge owner. A login that answers Slack at 17:40 is.

Before anyone talks about enabling auto-merge, print the PR as GitHub sees it. This command merges nothing:

```bash
#!/usr/bin/env bash
# scripts/inspect-agent-pr.sh — read-only. Never calls gh pr merge.
set -euo pipefail
PR="${1:?usage: inspect-agent-pr.sh <number>}"
gh pr view "$PR" --json number,author,isDraft,mergeStateStatus,reviewDecision,autoMergeRequest,labels,url
echo "---"
gh api "repos/{owner}/{repo}/pulls/${PR}" --jq '{
  user: .user.login,
  user_type: .user.type,
  mergeable_state: .mergeable_state,
  auto_merge: .auto_merge,
  requested_reviewers: [.requested_reviewers[].login]
}'
```

If `auto_merge` is not null on an agent PR, someone already scheduled the landing. Disable it before you argue about the diff.

{{< source href="https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output" label="GitHub Docs: Review output from Copilot" >}}
{{< source href="https://docs.github.com/en/copilot/how-tos/github-copilot-app/managing-issues-and-pull-requests" label="GitHub Docs: Copilot app issues and pull requests" >}}

![Before agent merge: named owner, diff read, Actions approved, rollback named](/img/coding-agent-merge-rights-3.png)

## The four questions I ask on an agent PR

I use the same four questions on Laravel + Vue work and on a static site. The stack changes. The questions do not.

**1. Who is the merge owner?** A GitHub login, written on the ticket and on the `merge-owner:` label. Not “the team.” Not “whoever is online.” If that person is in a meeting, the PR waits. Agent merge exists to survive CI lag **after** a human decided. It does not exist to skip the decision.

**2. Did a human read this exact diff?** Not the first diff. The current one. If the agent pushed after your review, GitHub can dismiss the approval when you turn on stale-review dismissal. Leave that on for agent branches.

**3. Did a human approve Actions?** Default Copilot PRs sit there with quiet workflows until someone clicks **Approve and run workflows**. Skipping that click because “it's only tests” is how a workflow file change inherits secrets. GitHub added an admin opt-out in March 2026. I leave the default on for any repo that deploys. [Source: https://github.blog/changelog/2026-03-13-optionally-skip-approval-for-copilot-coding-agent-actions-workflows/]

**4. What is the revert command, and who runs it?** A SHA, a `git revert`, a migration rollback, a Cloudflare rollback, a feature flag. If the answer is “we will open another agent session,” you do not have a rollback. You have a sequel.

{{< field-note title="Field note" >}}
On Laravel + Vue SaaS work I care about this gate more than I care about the model name. An agent PR that “just fixes a filter” still touches `database/migrations`, `routes/web.php`, or an Inertia page that finance opens every morning. Green PHPUnit does not mean the sales-mix screen still exports a PNG. The merge owner is the person who can restore the previous migration and the previous Vue page without waiting for the agent to “try again.” I keep that name on the ticket the same way I keep a rollback owner on a chart-library change: if nobody will say the name out loud, the PR stays open.
{{< /note >}}

This is the same maintenance instinct as [not adding a second chart stack mid-sprint](/blog/second-chart-stack-mid-sprint/): a green lockfile is not permission. Here a green agent PR is not permission.

## What I tell the team in three lines

I keep the spoken rule short enough to screenshot.

1. Agents open pull requests. Humans merge them.
2. Copilot review is extra reading, not the required approval.
3. Agent merge and auto-merge stay off until the named owner has read the current diff.

If someone wants a faster path for docs-only PRs, we still name the owner. We do not invent a second policy that says “the agent can merge when the folder is `docs/`.” Folder heuristics fail the first time a docs PR changes a workflow badge that points at a deploy pipeline.

For agent-authored work coming from chat surfaces, I use GitHub's own extra-approval idea as the template. Teams Copilot PRs can require one more human than your normal rule. That is the right direction: **raise** the merge bar for agent identity, do not lower it because the session was visible in a channel. [Source: https://github.blog/changelog/2026-08-21-shared-agentic-work-with-github-copilot-in-microsoft-teams/]

![Three-line desk rule: agents open PRs, humans merge, named owner on the label](/img/coding-agent-merge-rights-4.png)

## Failure modes I have already seen (without inventing a thriller)

I am not going to write a fake outage. The failure modes are ordinary.

**The author approves the agent.** GitHub already refuses to count that approval toward required reviews on Copilot PRs. People still click Approve out of habit. The merge stays blocked, they get frustrated, and someone with admin rights adds a bypass. The bypass is the incident. Keep admins off the bypass list for the agent identity.

**Actions stay off, CI looks “empty,” someone merges anyway.** Default Copilot PRs do not run workflows until you approve them. An empty check list is not a pass. It is an unstarted test run. [Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output]

**Agent merge is left on from the last PR.** The Copilot app says agent merge survives app restarts and turns off after **that** pull request merges. The danger is the human who enables it as a personal default. Make “enable agent merge” a per-PR action by the named owner, same as enabling classic auto-merge.

**Token can merge because token can write.** If the agent runs `gh pr merge` with the developer's PAT, branch protection is the only brake. Put the brake on `main` before you give the agent a token.

**Reviewer reads v1, agent pushes v4, merge uses v4.** Dismiss stale approvals. Require a review of the latest push. GitHub documents both settings. [Source: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches]

If you want a deeper review harness after the first merge gate exists, use [the repeatable review harness for AI-generated code](/blog/a-repeatable-review-harness-for-ai-generated-code-after-the-first-merge-gate/). This post is the gate before that harness matters.

## What you should do Monday morning

1. Write the merge owner on the next agent ticket as a GitHub login. If you cannot name one, do not start the agent.
2. Turn on required reviews for `main`, dismiss stale approvals, and require a review of the latest push. Confirm the agent identity is **not** a bypass actor.
3. Leave **Require approval for workflow runs** on for Copilot cloud agent unless you have a written exception with an expiry date.
4. Add `.github/workflows/agent-merge-owner.yml` and the `merge-owner:<login>` label convention. Add CODEOWNERS for migrations, workflows, and auth routes.
5. Run `scripts/inspect-agent-pr.sh` on every open agent PR. If `auto_merge` is set, disable it, then read the diff.
6. Tell the team the three-line rule in standup. Screenshot it. Do not add a fourth line about exceptions until you have a dated exception ticket.
7. Link this rule from `/developer-tools/` and from the agent edit contract you already use. Pre-edit boundaries without a merge owner are unfinished.

The Monday test is ugly and short: can a new developer point at a PR and say who is allowed to click Merge? If the answer is “the agent, once CI is green,” you do not have a merge policy. You have a hope.

## Further reading

{{< source href="https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output" label="Review output from Copilot (GitHub Docs)" >}}

{{< source href="https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request" label="Automatically merging a pull request (GitHub Docs)" >}}

{{< source href="https://github.blog/changelog/2026-08-21-shared-agentic-work-with-github-copilot-in-microsoft-teams/" label="Shared agentic work with GitHub Copilot in Microsoft Teams (21 Aug 2026)" >}}

Related on this site: [the agent edit contract](/blog/the-agent-edit-contract-i-use-before-a-coding-agent-touches-a-repo/), [coding-agent policy change control](/blog/coding-agent-policy-change-control/), and the operating hubs at [/ai-agent-operations/](/ai-agent-operations/), [/developer-tools/](/developer-tools/), and [/start-here/](/start-here/).
