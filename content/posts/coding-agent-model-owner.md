---
title: "I Do Not Let a Coding Agent Pick Its Own Model"
date: 2026-08-29T07:00:00+07:00
draft: false
slug: "coding-agent-model-owner"
description: "The agent that writes the diff does not choose the model for that pull request. A named human pins the model before the session starts. Auto is a vendor default, not an owner."
topics: ["ai-agents"]
tags: ["coding-agents", "model-selection", "github-copilot", "cursor", "pull-requests", "code-review"]
cover: /covers/coding-agent-model-owner.png
seo:
  primaryQuery: "coding agent should not pick its own model"
  secondaryQueries:
    - "named human pins AI model for pull request"
    - "GitHub Copilot Auto model is not a model owner"
    - "stop coding agent from choosing review model"
---

The session is already running. The agent opened a pull request, wrote a confident summary, and asked for review. Nobody on the ticket can say which model produced the diff.

That is the moment I stop the run. The agent may write the branch. The agent may open the pull request. The agent does not choose the model for that work. A named human writes the model on the ticket before the first prompt.

Yesterday I wrote the merge click. Merge stays with a person. Today's refusal is one gate earlier: the model that authors the change, and the model that reviews it, are human picks. Auto is a vendor default. It is not a name.

<!--more-->

![Three stations: ticket names the model, session uses it, review uses another](/img/coding-agent-model-owner-1.png)

## Auto is a default, not a desk

Most teams leave the model picker on **Auto** because it feels like a grown-up setting. The product copy says the tool will pick a good model for the task. That sentence is true as marketing. It is false as ownership.

GitHub documents the enterprise version of this default. Administrators can set `model` to `auto` in `managed-settings.json` so **new conversations start with Copilot auto model selection**. Users can still switch per conversation. The file lives in the source organization's `.github-private` repository. Copilot pulls it on authenticate and refreshes it hourly. [Source: https://github.blog/changelog/2026-07-01-enterprises-can-default-to-auto-model-selection/]

Read the subject. The **enterprise** set Auto as the start state. The **user** can still change the conversation. Neither of those people is written on the pull request. When I open an agent PR six hours later, I cannot reconstruct which model wrote `routes/web.php`.

Cursor's agent layer is the same shape with more moving parts. Built-in subagents exist so the parent can hand off search, shell, and browser work. Cursor's docs say the Explore helper uses a **faster model by default**, and custom helpers default to `model: inherit` unless you pin a model ID in the markdown frontmatter. Team admins can block a model; then Cursor falls back. On the public forum, Cursor staff added the operational detail: when the main agent launches a built-in helper, it picks a model from what is available. [Source: https://cursor.com/docs/subagents] [Source: https://forum.cursor.com/t/subagent-allowed-models/167531]

So the stack already has three choosers:

1. The org default (often Auto, or “unconfigured models follow the global policy”).
2. The parent agent, when it launches a helper.
3. The fallback, when the pin is blocked or the plan does not include that model.

None of those choosers is the person who will revert the Laravel migration on Monday.

{{< note type="warning" title="Auto does not sign the ticket" >}}
A model picker set to Auto answers “which model feels cheap and capable right now.” A pull request answers “which model authored this diff, and who decided that.” Keep those questions on a named human.
{{< /note >}}

## What GitHub actually ships this week (evidence, not the hook)

I am not writing a Copilot changelog. I am using one product fact as evidence.

On 26 August 2026 GitHub started rolling out **global model policy** for Copilot Business and Copilot Enterprise. Enforcement runs through 1 September, so enterprises see it at different times. Unconfigured generally available models move to **Delegate to default policy**. If that policy is enabled — and enabled is the default — those models become available to users. Explicit enable or disable on a model is preserved. Open-weight models (GitHub names DeepSeek and Kimi) and models not covered by GitHub's data retention agreement stay disabled by default, regardless of the policy. [Source: https://github.blog/changelog/2026-08-26-global-model-policy-generally-available/] [Source: https://docs.github.com/en/copilot/concepts/models/default-availability]

That is a useful org switch. It is not a per-PR model owner.

The four states in the model settings after rollout:

| State | Meaning for a junior on the desk |
| --- | --- |
| Enabled | An admin turned this model on on purpose. |
| Disabled | An admin turned this model off on purpose. |
| Delegate to enterprise / org | This model follows a parent setting. |
| Delegate to default policy | Nobody configured this model. It follows the global switch. |

If the global switch is on, a model the team never discussed can appear in the picker. That is the point of the policy: users get new GA models without an admin ticket. [Source: https://docs.github.com/en/copilot/concepts/models/default-availability]

I keep the policy as a floor: open-weight and retention-gap models stay off unless someone names them. I do not treat “now available” as “now allowed on this PR.” Availability is not assignment.

GitHub policies apply where users authenticate: IDEs, github.com, Copilot CLI. Not every policy hits every surface. The Copilot app and Copilot CLI have separate client policies. [Source: https://docs.github.com/en/copilot/concepts/policies]

That last sentence is why a wiki page is not enough. The person who starts the agent in the IDE and the person who starts it in the CLI can see different pickers. The ticket still has to name the model.

![Available in the org picker is not assigned on the ticket](/img/coding-agent-model-owner-2.png)

## The agent that wrote the diff does not review the diff

The second failure is quieter than Auto.

A coding agent writes a pull request. Someone pastes “review this” into a new chat. The review chat is also on Auto, or worse, on the same model that just authored the change. The review comes back green. The team feels covered.

I already said Copilot code review is extra reading, not the required approval, in [the merge-rights post](/blog/coding-agent-merge-rights/). This is the model version of that sentence. A second pass with the same model is a rewrite, not a review.

Cursor's subagent docs make the pin explicit. Custom subagents are markdown with YAML frontmatter. `model: inherit` uses the parent. A specific model ID uses that model unless the team blocked it, the plan does not include it, or a legacy Max Mode rule overrides it. Then Cursor falls back. [Source: https://cursor.com/docs/subagents]

I use that as a desk rule, not as a product endorsement:

- Author session: a named model, written on the ticket.
- Review session: a **different** named model, or a human with no agent in the loop.
- Helper subagents: `inherit` for the author path, or a pinned cheap model for search only — never a surprise upgrade into the review path.

If the review model equals the author model, I do not call it a review. I call it a second draft.

{{< details summary="Why inherit is not a pin" >}}
`inherit` means “whatever the parent is using right now.” If the parent is Auto, the child is Auto. If the parent got nudged onto a new GA model after last week's policy rollout, the child follows. Pin the ID when the work is a review, a migration, or anything you will have to explain to finance.
{{< /details >}}

## What I write on the ticket before the first prompt

I do not start the agent until four fields exist. They fit in the issue body. They also fit in a PR template.

```markdown
## Model desk
- model-owner: @zemna
- author-model: named-fast-model
- review-model: named-review-model
- auto: forbidden
```

`named-fast-model` and `named-review-model` are placeholders for IDs your org actually licenses. The required part is the four fields, not a brand.

The owner is a GitHub login. Not “the team.” Not “whoever is online.” If that person is in a meeting, the agent waits.

`auto: forbidden` is the line juniors need. Auto is allowed for throwaway questions in a personal scratch repo. It is not allowed on a PR that can touch `database/migrations`, `.github/workflows`, or an Inertia page the office opens every morning.

I keep a tiny check so the PR cannot look “ready” with an empty model desk.

```bash {linenos=inline,hl_lines=[12,18,24]}
#!/usr/bin/env bash
# scripts/inspect-agent-model.sh
# Fail the PR if the model desk is missing or set to Auto.
set -euo pipefail

body_file="${1:-}"
if [[ -z "${body_file}" || ! -f "${body_file}" ]]; then
  echo "usage: $0 <pr-body.txt>" >&2
  exit 2
fi

body="$(tr '[:upper:]' '[:lower:]' < "${body_file}")"

need() {
  local key="$1"
  if ! grep -Eq "${key}:[[:space:]]*[^[:space:]]+" <<< "${body}"; then
    echo "missing ${key}" >&2
    exit 1
  fi
}

need "model-owner"
need "author-model"
need "review-model"

if grep -Eq 'author-model:[[:space:]]*auto\b' <<< "${body}"; then
  echo "author-model cannot be auto" >&2
  exit 1
fi
if grep -Eq 'review-model:[[:space:]]*auto\b' <<< "${body}"; then
  echo "review-model cannot be auto" >&2
  exit 1
fi
if grep -Eq 'author-model:[[:space:]]*(.+)' <<< "${body}" \
   && grep -Eq 'review-model:[[:space:]]*(.+)' <<< "${body}"; then
  author="$(sed -n 's/.*author-model:[[:space:]]*//Ip' "${body_file}" | head -1 | tr -d '[:space:]')"
  review="$(sed -n 's/.*review-model:[[:space:]]*//Ip' "${body_file}" | head -1 | tr -d '[:space:]')"
  if [[ "${author,,}" == "${review,,}" ]]; then
    echo "review-model must differ from author-model" >&2
    exit 1
  fi
fi

echo "model desk ok"
```

Wire it as a required check on agent PRs. A missing field is a red X, not a comment someone scrolls past.

For Cursor custom agents that the parent is allowed to spawn, pin the review helper. Do not leave it on inherit if the parent is Auto.

```markdown
---
name: pr-reviewer
description: Reads the current diff only. Does not edit. Use after tests pass.
model: named-review-model
readonly: true
---

You review the current git diff. You do not choose a different model.
You do not spawn further agents. You report: what you read, what
broke, what you did not run.
```

Cursor will still fall back if the team blocked that model or the plan does not include it. That fallback is why the ticket still names a human. When the pin cannot run, the owner stops the session. The agent does not silently continue on a cheaper surprise. [Source: https://cursor.com/docs/subagents]

![Four fields before the first prompt: model-owner, author-model, review-model, auto forbidden](/img/coding-agent-model-owner-3.png)

## Org policy is a fence. The ticket is the assignment.

Cursor Enterprise can restrict which models a team sees. The strictest list belongs on the **team**. Organization Groups only widen access; they do not tighten below what the team already allows. New models are not auto-enabled for every enterprise team; the org opts in. Auto-review in the IDE uses a small classifier model; blocking those classifier models turns Auto-review off even if Run Modes still lists it. [Source: https://cursor.com/docs/enterprise/model-and-integration-management]

GitHub's fence is the model policy plus `managed-settings.json`. Setting `"model": "auto"` makes Auto the default for new conversations in the clients that honor the file. Users can still pick another model for that conversation. Team specialization can mark `model` overridable so one group uses `"model": "unmanaged"` while everyone else keeps the enterprise default. [Source: https://github.blog/changelog/2026-07-01-enterprises-can-default-to-auto-model-selection/] [Source: https://docs.github.com/en/copilot/reference/enterprise-managed-settings-reference]

I use the fence. I do not confuse it with the assignment.

| Layer | What it answers | What it does not answer |
| --- | --- | --- |
| Global / default model policy | Which models exist in the picker | Which model this PR used |
| `managed-settings.json` `model` | What a **new** chat starts on | What the running session is on |
| Team model allow-list | What a developer is allowed to click | What they did click |
| Ticket `author-model` | The assignment | Nothing — this is the record |

If you only have the first three rows, you have procurement. You do not have a paper trail.

I already treat instruction files as change control in [coding-agent policy as change control](/blog/coding-agent-policy-change-control/). Same instinct here. A sticky note in chat that says “use the smart one” is not an artifact. The four fields in the issue body are.

{{< field-note title="Field note" >}}
On Laravel + Vue SaaS work the model name matters less than the split. An author model that is cheap and fast is fine for a Pest test and a Vue filter. The review model is the one that has to notice a migration that rewrites a unique index the sales-mix export still assumes. I write both names on the ticket the same way I write a rollback owner on a chart-library change. If nobody will say the review model out loud, the agent does not start. Fast Beauty Indonesia's PHP/Vue surfaces are ordinary here: a “small” agent PR still reaches `database/migrations` and an Inertia page. The model desk is the person who can still explain that page without asking the agent to try again.
{{< /field-note >}}

## Failure modes I have already seen (no thriller)

I am not going to invent an outage. The misses are ordinary.

**The picker was Auto, the PR says nothing.** Six hours later nobody can answer “which model.” You cannot reproduce the session. You cannot compare cost. You cannot tell a junior why the style of the diff changed mid-afternoon.

**The parent spawned a helper on a model you never allowed.** Cursor's public forum answer is direct: the main agent picks a model for built-in subagents from what is available; a broader allow-list for every subagent does not exist yet; turning models off in settings is the closest control; custom subagents can pin `model:` in frontmatter. [Source: https://forum.cursor.com/t/subagent-allowed-models/167531]

**A new GA model appeared after the global policy rolled out.** Unconfigured models follow the default. If the default is enabled, the picker grew. Explicit disables stay. Open-weight and retention-gap models stay off unless someone enables them. [Source: https://docs.github.com/en/copilot/concepts/models/default-availability]

**Review ran on the author model.** The comments are fluent. The bug in the migration is still there. Fluency is not coverage.

**The pin was blocked and the tool fell back.** Cursor documents the fallback. If you treat “the session continued” as success, you accepted a model you did not name. Stop. Write the fallback on the ticket or close the session.

**Someone enabled Auto for the org because “users can still switch.”** True. They will not switch when the standup is late. Defaults are the product.

This sits next to [the agent edit contract](/blog/the-agent-edit-contract-i-use-before-a-coding-agent-touches-a-repo/): map, boundary, test command, artifact, rollback. The model desk is the missing line on that contract. A map without a model owner is a tour. A merge owner without a model owner is a last click on work nobody can reproduce.

![Five ordinary misses: empty Auto ticket, helper surprise, new GA in picker, same-model review, silent fallback](/img/coding-agent-model-owner-4.png)

## What I tell the team in three lines

I keep the spoken rule short enough to screenshot.

1. A named human picks the author model and the review model before the agent starts.
2. Auto is not a model name. Same model is not a review.
3. If the pin cannot run, stop. Do not accept a silent fallback.

If someone wants a faster path for docs-only PRs, we still fill the four fields. We do not invent a second policy that says “Auto is fine when the folder is `docs/`.” Folder heuristics fail the first time a docs PR changes a workflow badge that points at a deploy.

The merge rule from yesterday still stands. Agents open pull requests. Humans merge them. Today's rule is the one that makes that merge reviewable: you know which model you are merging.

## What you should do Monday morning

1. Add the four fields to the issue template: `model-owner`, `author-model`, `review-model`, `auto: forbidden`. Require a GitHub login, not a team name.
2. Copy `scripts/inspect-agent-model.sh` into the repo. Make it a required check on PRs labeled `agent`. Fail on Auto and on matching author/review models.
3. Open your Copilot **Models** page. For each GA model, set Enabled or Disabled on purpose. Do not leave **Delegate to default policy** on anything you are not willing to see in a junior's picker this week. [Source: https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/manage-default-models]
4. If you use `managed-settings.json`, read the `model` key as a **start state for new chats**, not as a per-PR pin. Do not set `"model": "auto"` on a repo where agent PRs ship to production unless you also require the ticket fields. [Source: https://docs.github.com/en/copilot/reference/enterprise-managed-settings-reference]
5. For Cursor, pin `model:` on every custom review subagent. Turn off models you refuse. Treat a fallback as a stop, not a convenience. [Source: https://cursor.com/docs/subagents]
6. On the next agent PR, fill the four fields before the first prompt. If you cannot name the review model, do not start the agent.
7. Link this rule from [/ai-agent-operations/](/ai-agent-operations/) and from the merge-rights note. A merge owner who does not know the model is merging a stranger.

The Monday test is ugly and short: can a new developer open the PR and say which model wrote it, which model reviewed it, and who decided both? If the answer is “Auto, I think,” you do not have a model policy. You have a hope.

The question is not whether Auto demos well. The question is whether the assignment survives handoff, a Monday revert, and a junior reading the ticket without you in the room.

## Further reading

{{< source href="https://github.blog/changelog/2026-08-26-global-model-policy-generally-available/" label="GitHub Changelog: Global model policy generally available (26 Aug 2026)" >}}

{{< source href="https://docs.github.com/en/copilot/concepts/models/default-availability" label="GitHub Docs: About default availability of Copilot models" >}}

{{< source href="https://cursor.com/docs/subagents" label="Cursor Docs: Subagents (model inherit vs pin)" >}}

Related on this site: [I do not give a coding agent merge rights](/blog/coding-agent-merge-rights/), [the agent edit contract](/blog/the-agent-edit-contract-i-use-before-a-coding-agent-touches-a-repo/), [coding-agent policy as change control](/blog/coding-agent-policy-change-control/), and the hubs at [/ai-agent-operations/](/ai-agent-operations/), [/developer-tools/](/developer-tools/), and [/start-here/](/start-here/).
