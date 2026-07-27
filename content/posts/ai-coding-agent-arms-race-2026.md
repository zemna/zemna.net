---
title: "The AI Coding Agent Arms Race — Why Model Portability Matters More Than Benchmarks"
slug: "ai-agent-frameworks-in-2026-what-the-comparison-charts-dont-tell-you"
date: 2026-06-23T07:00:00+07:00
lastmod: 2026-07-27T08:00:00+07:00
draft: false
description: "A current guide to keeping AI coding-agent instructions, verification, approval, and rollback in the repository so a tool or model change does not rewrite release control."
topics: ["developer-tools"]
tags: ["coding-agents", "model-portability", "repository-policy", "agents-md", "claude-md", "copilot", "release-controls"]
cover: /covers/ai-coding-agent-arms-race-2026.png
seo:
  primaryQuery: "AI coding agent model portability"
  secondaryQueries:
    - "AGENTS.md repository instructions"
    - "coding agent release controls"
    - "AI coding tool migration checklist"
---

A coding-agent migration often starts with a model comparison, then fails somewhere much less glamorous: a test command was stored in a chat preset, a deployment warning existed only in one tool’s dashboard, or a local override quietly changed what the agent was allowed to touch.

That is the wrong place to discover the real dependency. The durable asset is not a model setting. It is the repository-owned release policy: which paths are protected, which command verifies a change, who approves an exception, what evidence must survive review, and how the team returns to safety when a tool behaves badly.

The question is not whether a coding agent demos well; it is whether its work survives maintenance, handoff, and local constraints.

<!--more-->

![Repository policy as the stable center: tools may change, while tests, approvals, evidence, and rollback remain](/img/ai-agent-arms-race-1-refresh.png)

## The portability problem is larger than a provider switch

Switching a model is easy to describe. Change an identifier, update an API key, rerun a prompt. Switching a coding-agent workflow is harder because the workflow includes much more than a request to a model. It contains instructions, directory conventions, allowed tools, review rules, test commands, CI status checks, deployment permissions, and the place where a reviewer looks for proof.

The major coding-agent products expose different mechanisms for keeping that context near the project. Current OpenAI Codex documentation says Codex reads `AGENTS.md` before work, combines global and project guidance, and lets files closer to the working directory appear later in the instruction chain. GitHub documents repository-wide Copilot instructions, path-specific instruction files, and `AGENTS.md` files whose nearest location takes precedence for an agent. Claude Code documents project `CLAUDE.md` files and path-scoped rules; it also makes an important boundary explicit: instructions are context, while a hook or other technical control is needed when an action must be enforced regardless of model judgment. [OpenAI Codex AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md) [GitHub Copilot instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)

Those are useful capabilities. They are not, by themselves, a release system.

A repository becomes portable when the contracts it needs do not disappear with a product change. If tomorrow’s team moves from one coding agent to another, it should still be able to answer five questions without opening an old chat transcript:

1. Which files or actions require additional review?
2. What is the smallest verification command for this change?
3. What evidence must a pull request carry?
4. Who can approve an exception?
5. How do we stop or reverse a failed change?

That is a different standard from “the new tool can read our instructions.” A tool can read them and still misinterpret them, skip a command, or produce a plausible result that lacks the artifact the next engineer needs.

{{< field-note title="Field note" >}}
In a Laravel and Vue maintenance workflow, the risky boundary is usually not the first generated controller or component. It is the point where a migration, queue job, authorization policy, environment setting, or release workflow crosses into an irreversible system. For Modoo Laravel SaaS work, keep the rule, the verification command, and the rollback note in versioned project files. The tool can change; the handoff contract should not.
{{< /field-note >}}

## Put the control plane in the repository

Repository instruction files work best when they identify the operating contract rather than trying to become an encyclopedia. A root file should establish common expectations. A scoped file should add a local hazard. CI should enforce the controls that are mechanical. A pull request should carry the human evidence.

The following example is an illustrative repository contract, not a vendor-specific configuration. The commands and owners are intentionally explicit so a reviewer can check them.

```md
# AGENTS.md

## Delivery contract

- Keep edits inside the requested boundary.
- Run `composer test` for PHP application changes.
- Run `npm run build` for Vue application changes.
- Record commands run and failures in the pull request.
- Do not apply production migrations or change deployment configuration.
- Escalate any conflict between this file and a task request.

## Protected paths

- `database/migrations/**`: require a migration plan and rollback note.
- `infra/**`: require platform-owner approval.
- `resources/js/**`: require the Vue build and visual-check evidence.
```

The point is not that every repository should use these exact commands. The point is that the decision is visible, reviewable, and versioned. A team can replace a model or agent runtime without translating hidden dashboard settings into a new tool’s vocabulary.

Make the root contract short enough to read. It should name the default verification route, prohibited actions, source of authority, and escalation behavior. Long instruction files lose the property that makes them useful: an agent and a reviewer can locate the relevant rule before work starts. Claude Code’s guidance recommends specific, concise, structured project instructions and recommends path-scoped rules when a rule only matters in part of a codebase. That is sound repository design even when the team does not use Claude Code. [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)

A concise policy also makes product differences manageable. Codex uses its own discovery chain. Copilot offers repository-wide and path-specific instruction types. Claude Code reads `CLAUDE.md` rather than `AGENTS.md`, while its documentation provides an `@AGENTS.md` import pattern for sharing a common source. Do not pretend their loading rules are identical. Keep the high-value contract in a canonical project document, then add small adapters where a tool needs a different filename or format.

| Control | Repository-owned source | What a tool may provide | What still needs review |
|---|---|---|---|
| Default test command | Root policy or documented script | Instruction discovery | Whether the command matches the changed boundary |
| Protected-path rule | Versioned policy and ownership file | Scoped instructions | Scope, exception, and affected files |
| Approval boundary | CODEOWNERS, CI, deployment policy | PR or agent integration | Whether approval actually occurred |
| Evidence format | PR template and artifact convention | Agent summary | Whether the artifact proves the claimed result |
| Rollback | Runbook and revert route | A generated suggestion | Whether rollback is safe for the released state |

## Scope rules like code, not prose

A broad instruction such as “be careful with billing changes” is not a control. It does not identify a path, action, reviewer, proof, or response when the rule conflicts with delivery pressure. A scoped instruction can do that work because it has a boundary.

GitHub’s current documentation gives a concrete model: a repository-wide instruction can apply to all requests, path-specific instruction files apply to matching paths, and multiple relevant instruction types can be used together. It also documents `AGENTS.md` discovery for agents. Codex documents a root-to-working-directory chain and an override filename. Claude Code documents project instructions plus rules that can be scoped with YAML `paths` frontmatter. These are three different implementations of the same architectural concern: local context must narrow a general rule without silently erasing it. [GitHub Copilot instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) [OpenAI Codex AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md) [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)

Use that flexibility to make rules stricter near risk, not to hide a bypass. A directory policy should say what it adds and who owns it. It should point back to the root contract instead of copying everything. Repetition creates drift: a secret-handling rule copied into five files eventually changes in only one.

```md
# database/migrations/AGENTS.md

This directory inherits the repository delivery contract.

## Additional migration controls

- Describe the forward and rollback path in the pull request.
- Do not edit a migration that has already been released.
- Attach the targeted test command and its result.
- Ask `database-owners` to review an irreversible data change.
```

This file is intentionally narrow. It does not restate the whole project. It names a hazard that the root policy cannot safely ignore.

A scope review should test the policy itself. Change a file inside a protected directory and one outside it. Confirm that the intended instruction source, reviewer requirement, and verification expectation differ as designed. Then move or rename a directory in a branch and look for stale paths. The policy is part of the system architecture; it deserves fixtures and negative cases.

![Scoped policy tree: a root delivery contract and focused controls for app, database, frontend, and infrastructure paths](/img/ai-agent-arms-race-2-refresh.png)

## Make instructions a guide and enforcement a separate layer

The most expensive mistake is treating a model-facing sentence as a hard stop. It is not. An agent can misunderstand a rule, a prompt can omit relevant context, and a tool can run from a directory that activates a different local instruction.

Claude Code’s documentation states this boundary clearly: `CLAUDE.md` is context, not enforced configuration, and a `PreToolUse` hook is appropriate when an action must be blocked regardless of what the model decides. The general lesson applies everywhere. Use instruction files for intent, rationale, and workflow context. Use branch protection, CI, permission controls, deployment approvals, and hooks for requirements that must not be optional. [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)

For a Laravel/Vue repository, a useful division looks like this:

- The instruction file tells the agent which test to run, which directories are sensitive, and what record to attach.
- The pull-request template asks the author to name the commands, evidence, and rollback.
- CI checks a deterministic condition, such as required files or a policy manifest.
- Branch and deployment controls decide whether a protected change can merge or release.
- A human reviewer judges the case that cannot be reduced to a shell command.

Here is a small, working Python validator for an illustrative YAML policy manifest. It does not claim to understand the entire repository. It deliberately catches malformed control records before they become trusted documentation.

```python
#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

policy = yaml.safe_load(Path("policy/agent-policy.yaml").read_text())
errors = []

for control in policy.get("controls", []):
    name = control.get("id", "<unnamed>")
    for field in ("owner", "paths", "evidence", "rollback"):
        if not control.get(field):
            errors.append(f"{name}: missing {field}")

if errors:
    print("policy validation failed")
    print("\n".join(f"- {error}" for error in errors))
    raise SystemExit(1)

print("policy validation passed")
```

Pair it with a minimal policy document:

```yaml
controls:
  - id: database-change
    owner: database-owners
    paths:
      - database/migrations/**
    evidence:
      - migration-plan
      - rollback-plan
    rollback: revert-policy-and-follow-release-runbook
  - id: frontend-build
    owner: application-maintainers
    paths:
      - resources/js/**
    evidence:
      - npm-run-build
      - visual-check
    rollback: revert-change-and-rebuild-assets
```

This is not a governance product. It is a cheap tripwire. The value is that a policy edit now has an executable structural check, an owner, a path set, an evidence requirement, and a recovery reference. That is enough to turn an instruction change from an unreviewed prose edit into a change someone can reason about.

## Evaluate an agent migration with a repository harness

Do not benchmark a migration only by asking two tools to implement the same clean feature. A production evaluation should exercise your actual boundaries: project discovery, a constrained edit, a targeted test, a rejected action, an inspectable artifact, and a rollback route.

Build a small harness before you change the default agent. It need not be complex. It needs to make differences visible and repeatable.

```sh
#!/usr/bin/env sh
set -eu

policy_check="python3 scripts/validate_agent_policy.py"
app_check="composer test -- --filter=Invoice"
ui_check="npm run build"

printf '%s\n' "1. Read the applicable repository instructions"
printf '%s\n' "2. Propose files to change before editing"
printf '%s\n' "3. Run: $policy_check"
printf '%s\n' "4. Run the targeted check: $app_check or $ui_check"
printf '%s\n' "5. Record output path, changed files, and rollback command"
```

The comparison should score evidence, not a leaderboard claim. Did the agent identify the correct local policy? Did it respect a protected path? Did it run the named command? Did it distinguish a failing test from a successful release? Can a reviewer find the output without opening the original session? Can the patch be reverted without losing the record of what happened?

| Harness gate | Pass condition | Failure response |
|---|---|---|
| Policy discovery | Agent names the applicable root and scoped rule | Stop and fix discovery or file placement |
| Change boundary | Proposed paths match the task boundary | Narrow the task or require human review |
| Verification | Named command produces an inspectable result | Mark as incomplete; do not infer success |
| Approval | Required owner is visible on the review path | Hold merge or release |
| Rollback | Revert and operational follow-up are named | Add a recovery plan before proceeding |

This gives model portability a practical meaning. The team is not trying to make every agent behave identically. It is testing whether each candidate can participate in the same controlled delivery system. A weaker tool can still be useful for low-risk discovery. A stronger tool still should not acquire deployment authority merely because it produces convincing code.

![Migration harness flow: discover policy, propose bounded change, verify, approve, retain evidence, and preserve rollback](/img/ai-agent-arms-race-3-refresh.png)

## Preserve the evidence after the chat disappears

A chat session is a poor system of record. It is hard to search during an incident, inaccessible to many reviewers, and easily detached from the commit that eventually shipped. A release control needs artifacts that live where the engineering work lives.

Keep a small evidence record in the pull request, commit trailer, build artifact, or a versioned runbook. The record should say which instruction sources applied, which commands ran, which results failed, which exception was approved, and what rollback path applies. A tool-generated summary is useful only after a reviewer can locate its supporting evidence.

A simple pull-request section is enough to start:

```md
## Agent-assisted change record

- Applicable policy: `AGENTS.md`, `database/migrations/AGENTS.md`
- Changed paths: `app/Invoices`, `database/migrations`
- Verification: `composer test -- --filter=Invoice`
- Evidence: CI job URL and migration-plan attachment
- Approval: `database-owners`
- Rollback: revert commit; follow invoice-release runbook
```

Do not require the same evidence for a documentation typo and a schema change. Proportion matters. Excess ceremony teaches teams to route around controls. Missing evidence for an externally visible action leaves a gap that no later model comparison can repair.

The repository should also retain a way to disable an agent path without deleting the facts needed to diagnose it. Separate policy rollback from product rollback. Reverting a rule that required a migration plan does not undo a migration. Disabling an agent workflow does not retract an already-sent message. Name both actions in the relevant runbook so the next maintainer does not confuse them during a failure.

## Treat the policy migration as a release of its own

When a team adopts a new coding agent, it commonly migrates prompts first and controls last. Reverse that order. Start by moving the repository-owned contract, exercise it in a disposable branch, and verify that the target tool reaches the correct instruction source from the directories where developers actually work. Only then make the new tool a default.

The first rollout should be deliberately narrow. Give the agent a task with an obvious boundary and no irreversible release authority. Ask it to name the instruction sources it used, propose paths before editing, run the required check, and package the resulting evidence. Run one negative case too: place a task in a protected directory and confirm the workflow stops for approval rather than treating the request as a normal patch. The negative case tells you more about operational safety than a polished happy-path demo.

Keep the old route available until the new route has produced repeatable artifacts across maintenance work. This is not indecision. It is a rollback design. A team should be able to turn off the new agent integration, preserve its run records for review, and continue delivery through the existing protected branch and deployment process. The model may be new. The release control should remain familiar.

## What you should do Monday morning

1. Inventory instruction surfaces in one repository: `AGENTS.md`, `CLAUDE.md`, Copilot files, CI workflows, approval configuration, and pull-request templates.
2. Choose one risky boundary: migrations, deployment configuration, secrets, a payment workflow, or a customer-visible queue action.
3. Write a short root delivery contract that names a verification command, evidence expectation, protected action, and escalation behavior.
4. Add one local rule that tightens the control for the chosen directory. Do not duplicate the root file.
5. Put required fields—owner, paths, evidence, rollback—into a small policy manifest and validate its shape in CI.
6. Run the same bounded repair task with the current agent and a candidate replacement. Compare the policy discovery, changed paths, test output, and rollback record.
7. Keep deployment authority in the existing protected path while the agent proves it can produce dependable artifacts.
8. Review the harness after a real maintained change. If another engineer cannot locate the rule and evidence quickly, fix the contract before expanding agent authority.

The winning coding-agent setup is not the one with the most impressive comparison chart. It is the one a team can replace without rewriting its definition of a safe change.

## Further reading

- {{< source href="https://developers.openai.com/codex/agent-configuration/agents-md" label="OpenAI Codex — AGENTS.md discovery, layering, and verification" >}}
- {{< source href="https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions" label="GitHub Docs — repository, path-specific, and agent instructions" >}}
- {{< source href="https://docs.anthropic.com/en/docs/claude-code/memory" label="Claude Code Docs — CLAUDE.md, path-scoped rules, and enforcement boundary" >}}

Continue with [AI Agent Operations](/ai-agent-operations/), [Developer Tools](/developer-tools/), and [Laravel + Vue SaaS](/laravel-vue-saas/) for the surrounding delivery practices.
