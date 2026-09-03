---
title: "Leave Copilot Approve Off"
date: 2026-09-03T07:00:00+07:00
draft: false
slug: "leave-copilot-approve-off"
description: "GitHub now prints a ready-to-approve assessment on every Copilot review. That line is a note. The admin switch that turns it into a required approval is off by default. Keep it off."
topics: ["backend-infrastructure"]
tags: ["github-copilot", "code-review", "pull-requests", "required-approvals", "change-control", "coding-agents"]
cover: /covers/leave-copilot-approve-off.png
seo:
  primaryQuery: "GitHub Copilot approve pull requests off by default"
  secondaryQueries:
    - "Copilot approval assessment vs required approvals"
    - "do not enable Copilot PR approvals"
    - "named human merge owner Copilot review"
---

The pull request is green. Copilot already reviewed it. The overview comment says the change is ready to approve. A junior on the desk reads that line as the missing vote.

I stop the run there. Ready-to-approve is Copilot's judgment in a comment. It is not a required approval. It is not Merge.

GitHub shipped this as public preview on 1 September 2026. Every Copilot code review now includes an approval assessment in the overview comment. Admins can later authorize Copilot to submit a real approval that counts toward the repository's required-approvals rule. That ability is **off by default** at enterprise, organization, and repository level. An assessment alone does not count toward merge requirements. [Source: https://github.blog/changelog/2026-09-01-copilot-code-review-can-now-approve-pull-requests/]

I already refused agent merge in [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/). This post is the review-line that landed after that refusal. The agent still opens the branch. Copilot still comments. A named human still owns required approvals and the Merge click.

The question is not whether Copilot writes a fluent review. The question is whether the team treats that fluency as a vote on the branch we deploy.

<!--more-->

![Ready to approve is a note: Copilot comment, required approvals open, named human Merge](/img/leave-copilot-approve-off-1.png)

## The line that looks like a vote

Copilot code review used to leave a **Comment** review. Docs still say that is the default: not Approve, not Request changes. That comment does not count toward required approvals and does not block merge. [Source: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review]

The new overview line is louder. It tells you whether Copilot considers the pull request ready to approve. GitHub's own changelog is blunt: the assessment is surfaced so **you** decide how to act on it. [Source: https://github.blog/changelog/2026-09-01-copilot-code-review-can-now-approve-pull-requests/]

On this desk that sentence is the whole policy. Copilot is extra reading. Extra reading is useful. Extra reading is not a reviewer seat.

Three lights still fool people:

1. CI is green.
2. Copilot printed ready-to-approve.
3. The PR description reads like a release note.

None of those lights is a required approval. Green CI means the checks you wired ran. The assessment is Copilot grading its own neighborhood. A fluent description is writing, not a rollback plan.

I already ranked “cheap code still needs a human review” in [Five Things I Refused This Week](/blog/five-refusals-this-week/). This week the refusal is narrower: I do not let an assessment close the required-approvals box.

{{< note type="warning" title="Assessment is not a required approval" >}}
If the merge box still asks for a human review, the Copilot line did not vote. Do not ask an admin to “just turn Copilot approve on” so standup can finish.
{{< /note >}}

{{< field-note title="Field note" >}}
On Laravel and Vue SaaS work the dangerous PR is ordinary: a migration, a middleware change, a `routes/web.php` edit, a GitHub Actions badge in a docs folder. Copilot will still write a confident overview. I treat that overview as a first pass I read on the train. I do not treat it as the DBA, the auth owner, or the person who has to revert the migration on Monday. The named merge owner from the merge-rights post still owns Merge. Copilot does not get a second identity that counts as that person.
{{< /field-note >}}

## What shipped, without turning it into a changelog

Keep the product facts short. They are the evidence, not the hook.

| What you see | What it does | Default |
| --- | --- | --- |
| Approval assessment in the Copilot overview comment | Tells you Copilot's judgment | On, in every Copilot review (public preview) |
| Copilot **Approve** review | Counts toward required approvals **only if** admins enabled it | Off |
| New commits after a Copilot approval | Dismiss that approval, same as a human review | Same as humans |

Plans listed for the preview: Copilot Pro, Pro+, Max, Business, and Enterprise. Public preview, subject to change. [Source: https://github.blog/changelog/2026-09-01-copilot-code-review-can-now-approve-pull-requests/] [Source: https://docs.github.com/en/copilot/concepts/agents/code-review]

Docs split the admin work into two repository toggles under Copilot → Code review → Auto-approval:

- **Allow Copilot to approve pull requests** — Copilot may submit an approving review.
- **Allow Copilot approvals to count toward merge requirements** — that approving review satisfies required approvals.
- **File paths** — optional globs; up to 15; if set, the approval counts only when **every** changed file matches a glob. Blank means all files. [Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review]

I do not turn either toggle on. I document them so a junior can recognize the screen if someone else did.

Organization options for “Count Copilot approvals toward merge requirements” are: Enabled everywhere, Let repositories decide, Enable for selected repositories, Disabled everywhere. [Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review]

Enterprise policy for “Allow Copilot to approve pull requests”: Let organizations decide, Enable for selected organizations, **Disabled everywhere** (this is the default). [Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review]

Read that last row twice. GitHub's default at enterprise is **Disabled everywhere**. Matching the vendor default is not a hot take. It is the floor.

![Two Copilot approval switches, both OFF](/img/leave-copilot-approve-off-2.png)

## How I inspect a PR before anyone argues about the line

I do not argue with a screenshot. I pull the review objects.

Request Copilot as a reviewer the way GitHub documents, then read `state`. Default Copilot reviews show as comment reviews, not approvals. REST accepts `copilot-pull-request-reviewer[bot]`. CLI accepts `@copilot`. [Source: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review]

```shell {linenos=inline,hl_lines=[8,18]}
#!/usr/bin/env bash
# inspect-copilot-review.sh OWNER/REPO PR_NUMBER
set -euo pipefail
REPO="${1:?usage: inspect-copilot-review.sh OWNER/REPO PR_NUMBER}"
PR="${2:?}"

echo "== reviewDecision =="
gh pr view "$PR" --repo "$REPO" --json reviewDecision,reviews,autoMergeRequest \
  --jq '{reviewDecision, autoMergeRequest, reviews: [.reviews[] | {author: .author.login, state: .state, submittedAt}]}'

echo "== Copilot review rows =="
gh api "repos/${REPO}/pulls/${PR}/reviews" --jq '
  [.[]
   | select(.user.login | test("copilot"; "i"))
   | {user: .user.login, state: .state, submitted_at: .submitted_at}]
'

echo "== FAIL if Copilot submitted APPROVED =="
if gh api "repos/${REPO}/pulls/${PR}/reviews" --jq '
  any(.[]; (.user.login | test("copilot"; "i")) and (.state == "APPROVED"))
' | grep -qx true; then
  echo "Copilot left APPROVED. Someone enabled Copilot approve. Named human still owns Merge."
  exit 2
fi
echo "No Copilot APPROVED row. Assessment-only is the expected default."
```

`reviewDecision` is GitHub's merge-box summary: `APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED`, or empty when the repo does not require reviews. A Copilot comment review does not flip that field to `APPROVED` on a repo that still requires a human. If it does, the admin switch is on. Stop the merge and name who flipped it.

I keep the same inspect habit I use on hung agent jobs in [Building a Background Agent Recovery CLI: The Three-Gate Check](/blog/building-a-background-agent-recovery-cli-the-three-gate-check/): chat said done is not the artifact. Here, overview said ready is not the vote.

## Put the rule on the pull request, not in Slack

A spoken rule dies at the next standup. Put three lines on the PR template. If the template is empty, I do not start the agent.

```markdown {linenos=inline,hl_lines=[3,"6-9"]}
## Review contract (required)

- Copilot assessment (ready / not ready):
- Copilot review state (COMMENTED / APPROVED / CHANGES_REQUESTED):
- Required approvals owner: @username
- Merge owner: @username

Copilot assessment is a note.
Copilot APPROVED is a policy incident unless a dated exception ticket exists.
Do not ask an admin to enable Copilot approve to clear this box.
```

The merge owner line is the same name as the merge-rights post. I do not invent a second owner called “Copilot” because the overview was polite.

For agent-authored work, GitHub already refuses to count **your** approval of a Copilot coding-agent PR toward required reviews. Another reviewer has to approve. [Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output]

That rule and this rule stack. The person who prompted the agent is not the required approval. Copilot is not the required approval either. You still need a named human who did not write the branch.

## New commits wipe the vote — if you ever had one

GitHub is consistent here. If an admin enabled Copilot approvals and Copilot submitted Approve, a new push dismisses that approval the same way it dismisses a human review. You request a new Copilot review to get a fresh one. [Source: https://github.blog/changelog/2026-09-01-copilot-code-review-can-now-approve-pull-requests/] [Source: https://docs.github.com/en/copilot/concepts/agents/code-review]

That is why “require approval of the most recent reviewable push” still matters. I already used that setting as a failure mode in the merge-rights post: reviewer reads v1, agent pushes v4, merge uses v4. Copilot does not get a special stale-approval exemption.

If automatic Copilot review is on without **Review new pushes**, Copilot reviews once. Later commits keep the old overview unless someone clicks the re-review control next to Copilot in Reviewers. [Source: https://docs.github.com/en/copilot/concepts/agents/code-review]

Desk rule: the assessment you screenshot at 09:00 is dead after the 09:40 force-push. Read the current diff. Do not merge from memory of a green Copilot banner.

```shell {linenos=inline,hl_lines=[6,12]}
#!/usr/bin/env bash
# latest-reviewable-sha.sh OWNER/REPO PR_NUMBER
set -euo pipefail
REPO="${1:?}"
PR="${2:?}"

HEAD="$(gh api "repos/${REPO}/pulls/${PR}" --jq .head.sha)"
echo "head=$HEAD"

gh api "repos/${REPO}/pulls/${PR}/reviews" --jq --arg head "$HEAD" '
  .[]
  | select(.user.login | test("copilot"; "i"))
  | {user: .user.login, state: .state, commit_id, matches_head: (.commit_id == $head)}
'
```

If `matches_head` is false, the Copilot row is about an older commit. I do not care whether that row was COMMENTED or APPROVED. It is stale.

![New commits dismiss the Copilot vote](/img/leave-copilot-approve-off-3.png)

## Automatic review is not automatic approval

People conflate three settings because they sit in nearby menus.

**Automatic Copilot code review** (branch ruleset: Automatically request Copilot code review) asks Copilot to comment. Optional: review new pushes, review drafts. [Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review]

**Review effort** is Lite or Balanced. Lite is the faster pass. Balanced spends more AI credits. GitHub's concept doc estimates about $0.05–$1 USD of AI credits for Lite and $0.25–$5 USD for Balanced, not counting Actions minutes. Those ranges move as models change. They are cost, not permission. [Source: https://docs.github.com/en/copilot/concepts/agents/code-review]

**Copilot approvals** are the admin switches above. Separate product. Off by default.

I allow automatic **comments** on some repos the same way I allow a linter. I do not allow automatic **votes**. If a teammate wants Copilot on every PR, they get comments. They do not get a shortcut past required approvals.

GitHub also says Copilot is not guaranteed to spot every issue and you should supplement with a human review. [Source: https://docs.github.com/en/copilot/concepts/agents/code-review]

That sentence is the vendor's own floor. I do not spend a meeting lowering it.

## What I tell the team in three lines

Screenshot this. Do not add a fourth line about docs-only exceptions. Folder heuristics fail the first time a “docs” PR edits a workflow badge.

1. Copilot assessment is a note you read.
2. Copilot approve stays off. Nobody asks an admin to turn it on to clear the merge box.
3. A named human still owns required approvals and Merge.

That is the same spine as the merge-rights three-liner, with the new review-line named. I do not replace merge-rights. I add the assessment so juniors stop pointing at the overview and saying “it already approved.”

For operating context, keep this next to [/ai-agent-operations/](/ai-agent-operations/) and [/developer-tools/](/developer-tools/). Pre-edit contracts without a review-vote policy are unfinished.

![Three desk lines: assessment is a note, Copilot approve stays off, named human owns Merge](/img/leave-copilot-approve-off-4.png)

## Failure modes I have already seen (ordinary, not a thriller)

I am not going to invent an outage. The misses are boring.

**The junior treats the assessment as the missing approval.** Merge box still says Review required. They ping an admin. The admin looks at Copilot → Code review → Auto-approval because the menu label sounds like the fix. That click is the incident. Walk them back to the PR template instead.

**Someone enables “Allow Copilot to approve” but leaves “count toward merge requirements” off.** Copilot now leaves Approve in the timeline. Humans read the green check and skip the diff. The merge box is still honest. The social pressure is not. Keep both toggles off so the timeline does not lie.

**Path globs look like a safe subset.** “Only `*.md`.” The next PR adds `.github/workflows/deploy.yml` because the docs PR updated a status badge. If every file must match the glob, the Copilot approval stops counting — unless the glob is `**` or the list is blank. Do not design a glob policy. Leave the feature off.

**Automatic review without Review new pushes.** Copilot commented on the first draft. Five commits later the overview is archaeology. Re-request review or read the current `head.sha` yourself.

**Author plus Copilot as the two approvals.** On Copilot coding-agent PRs, the person who started the agent does not count. Copilot, by default, does not count either. You still need a different human. If an admin turned Copilot approvals on, you now have an agent author plus an agent vote. That is one identity family, not two reviewers.

**Budget blocks reviews, someone merges anyway.** Copilot Business and Enterprise block code review when the user budget or enterprise spending limit is exhausted. [Source: https://docs.github.com/en/copilot/concepts/agents/code-review] A missing Copilot review is not a pass. It is a missing comment. Human review still happens.

## What you should do Monday morning

1. Open one open pull request that Copilot already reviewed. Find the overview assessment. Write on the ticket: “note, not a vote.”
2. Run `inspect-copilot-review.sh` on that PR. Confirm Copilot `state` is not `APPROVED`. If it is, name the admin who enabled Auto-approval and turn the switches back off.
3. Open the repository Copilot → Code review screen. Confirm **Allow Copilot to approve pull requests** is off. Confirm **Allow Copilot approvals to count toward merge requirements** is off. Do not turn them on.
4. If you own an organization, confirm the org setting is **Disabled everywhere** (or that no one selected Enabled everywhere). If you own an enterprise, confirm **Disabled everywhere** is still the policy.
5. Paste the review-contract block into `.github/pull_request_template.md`. Require a merge owner login. Empty template means the agent does not start.
6. Keep required reviews on `main`, dismiss stale approvals, and require a review of the latest push. Copilot does not get a stale-approval exemption.
7. Tell standup the three-line rule. Screenshot it. Link this post from the merge-rights post and from [/start-here/](/start-here/).

The Monday test is short: can a one-year developer point at the Copilot overview and say, out loud, “that is a note”? If they say “Copilot already approved, so we can merge,” you do not have a review policy. You have a banner.

## Further reading

{{< source href="https://github.blog/changelog/2026-09-01-copilot-code-review-can-now-approve-pull-requests/" label="Copilot code review can now approve pull requests (GitHub Changelog, 1 Sep 2026)" >}}

{{< source href="https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review" label="Configuring code review by GitHub Copilot (GitHub Docs)" >}}

{{< source href="https://docs.github.com/en/copilot/concepts/agents/code-review" label="About GitHub Copilot code review (GitHub Docs)" >}}

Related on this site: [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/), [Five Things I Refused This Week](/blog/five-refusals-this-week/), [Building a Background Agent Recovery CLI](/blog/building-a-background-agent-recovery-cli-the-three-gate-check/), and the hubs at [/ai-agent-operations/](/ai-agent-operations/), [/developer-tools/](/developer-tools/), and [/laravel-vue-saas/](/laravel-vue-saas/).
