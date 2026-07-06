---
title: "The Agent Edit Contract I Use Before a Coding Agent Touches a Repo"
date: 2026-07-04T07:00:00+07:00
draft: false
description: "A practical contract for giving coding agents repository context, edit boundaries, verification steps, and rollback paths before they touch code."
topics: ["tutorial", "ai-agents"]
cover: /covers/agent-edit-contract.png
---

A coding agent should not get write access just because the prompt sounds clear.

The prompt is the weakest part of the workflow. It is conversational, lossy, and too easy to expand while nobody is watching. The contract has to sit outside the chat: a short file that says what the agent may inspect, what it may change, what command proves the change, what artifact must exist, and how to roll back if the run gets clever in the wrong direction.

I started using this pattern after watching agent runs produce convincing summaries with no durable evidence behind them. The model had read files. It had explained the plan. It had even finished with a confident final answer. But the repo had no clean diff, no named test command, and no artifact that proved the change survived outside the chat transcript. That is not an engineering workflow. That is a story about an engineering workflow.

This is the contract I now put in front of a coding agent before it edits a repository.

![Five-step agent edit contract workflow: Map, Boundary, Test, Artifact, Rollback](/img/agent-edit-contract-1.png)

## The contract comes before the agent

The useful mental shift is simple: treat the agent like a worker entering a live production-adjacent codebase, not like autocomplete with a larger context window.

GitHub describes agentic workflows as repository automations that can triage issues, keep documentation aligned, open pull requests for code simplification, assess test coverage, investigate CI failures, and create repository health reports [Source: https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/]. The same post is careful about the boundary: these workflows are designed to augment CI/CD, not replace deterministic build, test, and release pipelines, and pull requests are not merged automatically [Source: https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/].

That distinction matters. The agent can do subjective work. CI still owns deterministic proof. Humans still own merge decisions. The contract connects those three layers.

The research language points in the same direction. The 2026 survey "Code as Agent Harness" frames code not only as generated output, but as the medium through which agents use repositories, tests, traces, workflows, and execution state as shared artifacts [Source: https://arxiv.org/html/2605.18747v1]. That is the phrase I keep coming back to: shared artifacts. If the only artifact is a chat answer, the workflow is too soft.

Here is the minimal contract I use:

```markdown
# Agent Edit Contract

## 1. Repo map
- Entry points:
- Callers and callees checked:
- Related tests:
- Files inspected before editing:

## 2. Task boundary
- Allowed change:
- Explicit non-goals:
- Files the agent may edit:
- Files the agent must not edit:

## 3. Verification command
- Required command:
- Expected success signal:
- Failure output to preserve:

## 4. Artifact proof
- Artifact path or URL:
- Freshness rule:
- Minimum substance:
- Domain assertion:

## 5. Rollback note
- Revert command:
- Files to inspect after revert:
- Human approval checkpoint:
```

This is intentionally boring. Boring survives production better than a beautiful prompt.

## Step 1: make the agent draw the repo map

The first output from the agent should not be code. It should be a map.

A map is not a full repository summary. Full summaries waste context and create false confidence. A map is scoped to the edit. It names entry points, nearby tests, related types, and the files the agent inspected before touching anything.

For a Laravel and Vue application, a useful repo map for a billing settings change can look like this:

```yaml
repo_map:
  feature: billing-settings-notification-toggle
  backend_entrypoints:
    - routes/web.php
    - app/Http/Controllers/BillingSettingsController.php
  frontend_entrypoints:
    - resources/js/Pages/Billing/Settings.vue
    - resources/js/Components/Form/SwitchField.vue
  data_paths:
    - app/Models/Team.php
    - database/migrations/*_add_billing_notifications_to_teams.php
  tests_to_check:
    - tests/Feature/BillingSettingsTest.php
    - resources/js/Pages/Billing/__tests__/Settings.spec.ts
  commands:
    backend_test: php artisan test --filter=BillingSettingsTest
    frontend_test: npm run test -- Settings.spec.ts
```

The exact tool is less important than the shape. The agent must prove it understands the neighborhood before it changes the house.

This is where code-graph thinking helps. A previous note on structure-first workflows described the pattern as giving the agent structural sources of truth before raw repository volume: code graphs, targeted tests, artifact contracts, and alert rules managed as code. That pattern is stronger than asking for a bigger context window because it defines what the agent has to know, not how many tokens it gets.

The map also catches the first class of bad tasks: the prompt that sounds small but crosses a hidden boundary. If the agent cannot name the caller, callee, route, component, or test, the right action is not to edit. The right action is to inspect more.

![Repository map zones for an agent edit contract](/img/agent-edit-contract-2.png)

## Step 2: freeze the task boundary

After the map, freeze the boundary.

The boundary has two jobs. It tells the agent what success means, and it tells the agent what not to improve. The second part is the one developers skip.

Agents are dangerous when they are helpful in adjacent areas. A bug fix becomes a refactor. A refactor becomes a formatting pass. A formatting pass becomes a diff nobody can review in one sitting. The contract blocks that expansion before it starts.

Use a boundary like this:

```markdown
## Task Boundary

Allowed change:
- Add a persisted billing notification toggle for team owners.
- Render the toggle on the existing Billing Settings page.
- Save the value through the existing settings controller.

Non-goals:
- Do not redesign the Billing Settings page.
- Do not rename existing Vue components.
- Do not change subscription billing logic.
- Do not introduce a new state management library.
- Do not edit unrelated formatting.

Editable files:
- app/Http/Controllers/BillingSettingsController.php
- app/Models/Team.php
- resources/js/Pages/Billing/Settings.vue
- tests/Feature/BillingSettingsTest.php
- resources/js/Pages/Billing/__tests__/Settings.spec.ts

Protected files:
- config/cashier.php
- app/Services/BillingProvider.php
- resources/js/Layouts/AppLayout.vue
```

This boundary makes review possible. It also gives the agent a stopping rule. When the model proposes an adjacent cleanup, the answer is not "maybe later." The answer is "outside the contract."

Augment's CTO checklist makes a related point about AI agent changes needing to be reviewable as bounded, revertable units [Source: https://www.augmentcode.com/guides/cto-ai-coding-checklist]. I do not treat that as procurement advice. I treat it as a daily workflow rule: one contract, one revertable unit.

A good boundary also names protected files. That sounds heavy until the first time an agent fixes a UI bug by editing a billing provider. Protected files are cheap insurance.

## Step 3: name the verification command before the edit

The test command must be written before the agent changes code.

If the command appears only after implementation, the model will often choose the command that makes the run look clean. That is backwards. The contract should name the command while the desired behavior is still independent from the proposed patch.

For the Laravel/Vue example, the verification block can be explicit:

```bash
# Backend behavior
php artisan test --filter=BillingSettingsTest

# Frontend component behavior
npm run test -- Settings.spec.ts

# Static checks for changed frontend files
npm run lint -- resources/js/Pages/Billing/Settings.vue
```

This is working shell, not pseudocode. It can be copied into CI, a local terminal, or an agent instruction. If one of these commands does not exist in the repo, that is useful information. The agent should report the missing command and propose the nearest existing command instead of inventing a passing test.

The verification command should include three fields:

| Field | Purpose | Example |
|---|---|---|
| Required command | The exact command to run | `php artisan test --filter=BillingSettingsTest` |
| Expected signal | What success looks like | Exit code zero and a passing named test |
| Failure record | What to preserve if it fails | Full output path or CI log URL |

GitHub's agentic workflow guidance says to start with low-risk outputs such as comments, drafts, or reports before enabling pull request creation, and to be specific about what good looks like, including format, links, and when to stop [Source: https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/]. A test command is the coding version of "what good looks like."

Without it, the final answer becomes the success signal. That is where silent failures enter.

## Step 4: require artifact proof, not a success sentence

The most common agent failure is not a crash. It is a clean sentence with no usable artifact.

For scheduled jobs, I use artifact-based health checks: the process is not healthy because it exits zero; it is healthy when the expected artifact exists, is fresh, has substance, and passes a domain assertion. The same idea belongs in coding agent work.

For a code edit, the artifact can be a commit SHA, patch file, test log, generated screenshot, built asset, deployed preview URL, or pull request. The contract should define it before the run.

```json
{
  "artifact_contract": {
    "handle": "pull_request_url_or_commit_sha",
    "freshness": "created during this agent run",
    "minimum_substance": {
      "changed_files_min": 1,
      "test_log_required": true,
      "summary_required": true
    },
    "domain_assertion": [
      "billing setting persists after save",
      "team owner can toggle the setting",
      "non-owner cannot update billing settings"
    ]
  }
}
```

Notice what this contract does not say. It does not say "agent completed successfully." Completion is not evidence. Evidence is a handle that another system or human can inspect.

This is especially important when agents run in background processes. A background process can finish after the parent session has moved on. A subagent can time out during reporting even after it wrote the file. A script can exit zero with an empty output file. The artifact contract gives you a second layer of truth outside the agent's narration.

![Artifact proof checks: Handle, Freshness, Substance, Domain Assertion](/img/agent-edit-contract-3.png)

Here is a small verifier I use for file-based artifacts:

```python
from pathlib import Path
from datetime import datetime, timezone


def verify_artifact(path: str, min_bytes: int, max_age_minutes: int) -> None:
    artifact = Path(path)
    if not artifact.exists():
        raise SystemExit(f"missing artifact: {artifact}")

    size = artifact.stat().st_size
    if size < min_bytes:
        raise SystemExit(f"artifact too small: {size} bytes")

    mtime = datetime.fromtimestamp(artifact.stat().st_mtime, tz=timezone.utc)
    age = (datetime.now(timezone.utc) - mtime).total_seconds() / 60
    if age > max_age_minutes:
        raise SystemExit(f"artifact stale: {age:.1f} minutes old")

    text = artifact.read_text(errors="replace")
    required = ["BillingSettingsTest", "PASS", "billing notification"]
    missing = [token for token in required if token not in text]
    if missing:
        raise SystemExit(f"artifact missing required tokens: {missing}")

    print(f"artifact ok: {artifact} ({size} bytes, {age:.1f} minutes old)")


if __name__ == "__main__":
    verify_artifact("storage/logs/agent-billing-test.log", 200, 30)
```

The script is deliberately small. It checks existence, substance, freshness, and a domain assertion. Those four checks catch more bad automation than a polished final summary.

## Step 5: write rollback before implementation

Rollback is not a confession that the task will fail. Rollback is what keeps a small task small.

The contract should include the exact revert path before the edit starts. For a branch-based workflow, that can be direct:

```bash
# See the current diff
git status --short
git diff --stat

# Revert only the current agent branch to main
git fetch origin main
git reset --hard origin/main

# Remove untracked files created by the run
git clean -fd
```

For a pull request workflow, the rollback note should be attached to the PR body or handoff:

```markdown
## Rollback

If this change misbehaves after merge:
1. Revert commit `<commit-sha>` from the merge commit.
2. Run `php artisan test --filter=BillingSettingsTest`.
3. Confirm `/billing/settings` renders for a team owner.
4. Check application logs for billing provider errors.
```

This is where the human checkpoint belongs. GitHub Next describes Crane as a migration assistant that plans, executes, and verifies code migrations in small agentic steps while keeping humans in control [Source: https://githubnext.com/projects/agentic-workflows/]. The phrase "small agentic steps" is the operational part. Rollback is what keeps each step small enough to reverse.

If the rollback note is hard to write, the task is too large. Split it before the agent edits.

## The full contract template

Here is the version I keep around and adapt per repo:

```markdown
# Agent Edit Contract: <task-name>

## Repo map
- Feature or bug:
- Entry points:
- Callers/callees inspected:
- Related tests:
- Commands discovered:

## Boundary
- Allowed change:
- Non-goals:
- Editable files:
- Protected files:

## Verification
- Required command 1:
- Required command 2:
- Expected success signal:
- Failure output path:

## Artifact proof
- Required handle:
- Freshness rule:
- Minimum substance:
- Domain assertion:

## Rollback
- Revert command:
- Post-revert test:
- Human approval checkpoint:

## Final handoff format
The agent must end with:
1. Files changed
2. Commands run
3. Artifact handle
4. Known risks
5. Rollback note
```

I usually paste this into the issue, PR description, or `docs/agent-contracts/<task>.md`. The location matters less than the fact that it is outside the chat window and reviewable by another person.

The final handoff format is part of the contract. Without it, the agent chooses what to emphasize. With it, every run produces the same evidence shape.

| Contract layer | Bad final answer | Useful final answer |
|---|---|---|
| Repo map | "I inspected the relevant files." | "Inspected controller, Vue page, model, and two tests." |
| Verification | "Tests pass." | "Ran `php artisan test --filter=BillingSettingsTest`; log at `storage/logs/agent-billing-test.log`." |
| Artifact | "The change is ready." | "PR #142 with 5 changed files and test log attached." |
| Rollback | "Revert if needed." | "Revert commit `<sha>`, rerun named test, inspect billing settings route." |

That table is the difference between a chat transcript and an engineering record.

![Review table comparing weak handoff and useful handoff](/img/agent-edit-contract-4.png)

## What you should do Monday morning

Pick one repo and add one contract file. Do not roll this out across every project first. Start with the next small agent-assisted change and make the contract visible.

Use this checklist:

1. Create `docs/agent-contracts/` or add a contract section to your issue template.
2. Require a repo map before edits.
3. Name the editable files and protected files.
4. Write the test command before implementation.
5. Define the artifact handle: PR, commit, preview URL, test log, or generated report.
6. Add a rollback note before the agent writes code.
7. Reject final answers that do not include files changed, commands run, artifact handle, known risks, and rollback.

If that feels too strict, apply it only to tasks that touch production paths, billing, auth, migrations, background jobs, or shared UI components. Those are exactly the tasks where a confident agent summary is not enough.

One more rule helps: keep the first contract small enough to review in five minutes. A contract that becomes a second specification document will not survive the week. The point is not paperwork. The point is to force five facts into the open before the model writes code: where it looked, what it is allowed to change, how proof works, where the proof lives, and how to undo the run. If those facts are missing, the task is not ready for automation.

The contract does not make the agent slower. It makes the agent's work inspectable before the diff becomes somebody else's incident. That is the trade I want.

## Further reading

- GitHub Blog: Agentic Workflows and Continuous AI — https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/
- Code as Agent Harness survey — https://arxiv.org/html/2605.18747v1
- GitHub Next: Agentic Workflows — https://githubnext.com/projects/agentic-workflows/
