---
title: "A Coding-Agent Policy Is Change Control, Not a Settings File"
slug: coding-agent-policy-change-control
date: 2026-07-17T07:00:00+07:00
draft: false
description: "Treat repository instructions for coding agents as a governed change-control system: owned, reviewed, scoped, evidenced, and reversible."
topics: ["developer-tools"]
tags: ["coding-agents", "repository-governance", "developer-tools", "change-control", "agent-instructions"]
cover: "/covers/coding-agent-policy-change-control.png"
seo:
  primaryQuery: "coding agent policy change control"
  secondaryQueries:
    - "AGENTS.md repository governance"
    - "repository instructions coding agents"
    - "AI coding agent policy ownership"
---

A repository instruction file is easy to underestimate. It looks like a convenient place to put a test command, a style preference, and a warning about migrations. That framing is wrong once a coding agent can open pull requests, change schemas, edit infrastructure, or run commands on behalf of a team.

The policy is not a settings file. It is a change-control surface.

That distinction changes the questions worth asking. Instead of “what should the agent know?” ask: who owns this rule; who reviews a change to it; where does it apply; what evidence proves it was followed; and how does the team undo a bad policy change? Those questions make an instruction file operational rather than decorative.

The major tools already expose the raw mechanics for repository-level guidance. OpenAI Codex supports global instructions, repository-root `AGENTS.md` files, and scoped overrides in subdirectories. {{< source href="https://developers.openai.com/codex/guides/agents-md" label="OpenAI Codex: AGENTS.md guide" >}} Anthropic documents `CLAUDE.md` as a place for coding standards, review criteria, and project rules in Claude Code workflows. {{< source href="https://docs.anthropic.com/en/docs/claude-code/github-actions" label="Anthropic: Claude Code GitHub Actions" >}} GitHub Copilot likewise supports repository instructions and path-specific instruction files. {{< source href="https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide" label="GitHub Docs: repository instructions" >}}

The mechanics are useful, but they do not decide governance for you. A path-specific file can narrow a rule; it cannot decide whether the exception is legitimate. A root file can name a test command; it cannot establish whether the command was actually run. Version control records a diff; it does not make the diff safe by itself.

{{< field-note title="Field note" >}}
In a Laravel and Vue maintenance workflow, the risk is a local instruction silently changing the accepted test, a migration boundary, or the artifact needed for handoff. A Modoo Laravel SaaS change needs a visible policy source, bounded diff, named verification command, inspectable evidence, and revert path.
{{< /field-note >}}

**Operational judgment: treat every repository-level coding-agent instruction as production process code, with an owner, a review path, bounded scope, required evidence, and a tested rollback.**

![Agent policy change control: ownership, review, proof, and rollback](/img/coding-agent-policy-change-control-1.png)

## A policy becomes real when it changes the operating system of the repository

A useful coding-agent policy changes what work is permitted, what work is required, and what proof must accompany a change. If it only restates preferences that nobody enforces, it is documentation. Documentation matters, but it does not control execution.

Consider a short instruction: “Run the test suite before changing a billing workflow.” It contains at least four hidden decisions:

1. Which suite is authoritative: unit, feature, browser, integration, or all of them?
2. Does the rule apply to every file under `app/Billing`, to a named service, or to a route group?
3. Does “before” mean before editing, before a pull request, before merge, or before deploy?
4. What evidence should a reviewer see: raw CI status, a command transcript, a linked artifact, or a result recorded in the pull request?

Without answers, an agent receives a sentence but the repository has no control. Worse, the sentence creates false confidence. A reviewer assumes a guardrail exists while the agent selects an interpretation that is locally convenient.

A policy should therefore describe decisions at the level where they are enforceable. The file can state the human-readable rule; a companion manifest or CI check can make key parts machine-checkable. This is not about turning every engineering decision into bureaucracy. It is about reserving explicit control for the work where an automated contributor expands the blast radius.

The best policy files are concise at the top and precise where the risk is real. They identify the default workflow, name prohibited actions, point to authoritative commands, and link to scoped rules. They do not become a second architecture handbook. The goal is a reliable route from instruction to behavior.

Here is a repository-root `AGENTS.md` designed as a contract rather than a pile of hints:

```md
# AGENTS.md

## Default delivery contract

- Keep changes within the requested scope. Do not refactor adjacent modules without an issue or explicit request.
- For application changes, run `composer test` and `npm run build` before requesting review.
- Include the commands run and their result in the pull-request description.
- Do not create, apply, or edit production migration plans without approval from the `database-owners` review group.
- Never add secrets, tokens, production exports, or customer data to the repository.

## Authority and escalation

- `CODEOWNERS` is authoritative for review routing.
- `policy/agent-policy.yaml` is authoritative for scoped controls and required evidence.
- If an instruction conflicts with a task request or a scoped policy, stop and explain the conflict in the pull request.

## Scoped instructions

- Read `app/Billing/AGENTS.md` before changing billing code.
- Read `resources/js/AGENTS.md` before changing Vue interfaces.
- Read `infra/AGENTS.md` before changing deployment or infrastructure files.
```

This has a useful property: it names authority. The agent is not asked to invent precedence. It also avoids the tempting but brittle pattern of duplicating every command in every directory. The root file establishes the delivery contract; the scoped files describe local hazards.

That approach maps cleanly to the instruction mechanisms supplied by Codex and Copilot: root instructions establish a broad default, while directory or path-specific instructions carry local constraints. The important point is not the filename. The point is that inheritance and scope need the same design attention as application configuration.

## Ownership is the first control, not an afterthought

A policy without an owner is a comment with a filename. Someone needs authority to decide whether a policy rule is current, whether it conflicts with delivery needs, and whether an exception is acceptable.

Ownership should follow the risk of the decision, not the person who happened to write the first file. Platform engineering can own common command conventions and CI evidence requirements. Database maintainers should own migration and data-access rules. Security should own secret-handling and sensitive-operation boundaries. A product team can own local workflow details, provided they do not weaken repository-wide protections.

This is why `CODEOWNERS` alone is insufficient. It routes a review, but it usually does not express the purpose, evidence, expiry, or rollback of a policy change. A small manifest closes that gap. It gives reviewers a stable object to discuss and gives CI a structured input.

```yaml
# policy/agent-policy.yaml
version: 1
policyOwner: platform-engineering
reviewGroups:
  default:
    - platform-engineering
controls:
  - id: application-verification
    scope:
      paths: ["app/**", "routes/**", "resources/js/**"]
    requiredEvidence:
      commands:
        - "composer test"
        - "npm run build"
    owner: application-maintainers
    changeReview:
      requiredGroups: ["application-maintainers"]
    rollback:
      strategy: "revert policy commit and restore previous CI rule"
  - id: database-change-gate
    scope:
      paths: ["database/migrations/**", "app/Billing/**"]
    prohibitedActions:
      - "apply production migration"
    requiredEvidence:
      pullRequestFields: ["migration-plan", "rollback-plan"]
    owner: database-owners
    changeReview:
      requiredGroups: ["database-owners", "security"]
    rollback:
      strategy: "disable scoped override, revert merged migration, follow incident runbook"
```

The manifest is deliberately unglamorous. Its value comes from being reviewable and testable. It says that a rule has a named owner, a scope, required proof, and a recovery path. Those fields make it far harder to slip a broad exception into a friendly-looking documentation edit.

There is also a social benefit. When a developer wants to relax a rule, the conversation becomes concrete: which control changes, which paths are affected, who accepts the risk, and when will the exception end? That is healthier than debating whether an agent “should be trusted.” Trust is too vague to review. A bounded control is reviewable.

![Policy ownership approval flow using CODEOWNERS](/img/coding-agent-policy-change-control-4.png)

## Review policy changes like changes to delivery infrastructure

A policy edit can alter hundreds of future changes. That makes its leverage different from a normal feature patch. A one-line instruction that says “skip browser tests for admin work” changes the operating behavior of every agent that reads it. It deserves review proportional to that leverage.

Use a dedicated pull-request template for policy changes. Require the author to describe the behavioral delta, affected paths, reason, enforcement mechanism, expiration when relevant, and rollback. Do not accept “clarity” as a sufficient explanation when the result weakens a guardrail or expands an agent’s authority.

A practical review checklist looks like this:

| Review question | Why it matters | Evidence to request |
|---|---|---|
| What behavior changes? | Prevents prose-only reviews | Before/after examples of allowed and blocked actions |
| Which paths inherit the rule? | Catches accidental broad scope | Glob expansion or repository path list |
| Who owns the risk? | Assigns a decision-maker | Required approval from the named group |
| What proves compliance? | Turns intent into an observable control | CI job, command log, artifact, or PR field |
| How is it reversed? | Makes failure recoverable | Revert plan and any follow-up operational step |
| When does an exception expire? | Stops temporary bypasses from becoming permanent | Date, issue link, and removal owner |

The policy pull request should itself exercise the policy where possible. If a new rule requires `composer test`, the CI check validating the manifest should run that command or verify an equivalent pipeline status. If a rule restricts deployment files, a fixture or test should demonstrate that a change in `infra/` triggers the expected review requirement.

This is where many teams stop too early. They write a good policy but do not test its interpretation. Natural language has edges: path globs overlap, a root rule collides with an exception, a renamed directory becomes uncovered, or an agent reads an older instruction due to checkout state. Treat these as test cases, not as hypothetical annoyances.

For repositories that use Claude Code in GitHub Actions, `CLAUDE.md` can carry standards and review criteria, while the workflow provides a place to collect or require evidence. For Copilot, repository and path-specific instruction files let the team place rules near the code they govern. Neither feature eliminates the need to review the instruction changes with the same care used for workflow or CI changes.

## Scoped overrides should narrow risk, never hide it

Scoped overrides are essential. A monorepo has different safety needs in a marketing site, a shared library, a payments service, and infrastructure. A single global policy either becomes too vague to help or too rigid to use.

But an override is not a loophole. It is an explicit local contract with a parent rule, a bounded path, and a reason for being different.

Start with a simple inheritance model:

- The root policy defines non-negotiable repository controls: secrets, protected branches, evidence format, and escalation.
- A directory policy adds controls that are specific to its domain.
- A scoped policy can tighten the root rule without special approval.
- A scoped policy that weakens a root control requires the owner of the root control, a written rationale, an expiry, and an observable compensating control.

For example, a Vue interface directory can require a visual verification step without changing database rules. A billing directory can require a migration plan and a reviewer from the payment domain without imposing that ceremony on copy changes. The rule remains legible because its path and authority are clear.

A bad override says, “Tests are optional in this directory because changes are urgent.” A workable override says, “For `resources/js/experiments/**`, the browser suite is replaced for seven days by an approved preview checklist, linked issue, named owner, and a mandatory restoration date.” The second statement remains uncomfortable by design: it forces the team to acknowledge the tradeoff.

Scoped instructions should link upward rather than restate every parent rule. Repetition causes drift. If `app/Billing/AGENTS.md` copies the root secret policy, one update eventually lands in only one file. Prefer a short local file that declares the additional rule, names its owner, and points to the root contract.

```md
# app/Billing/AGENTS.md

This directory inherits `/AGENTS.md` and `policy/agent-policy.yaml`.

## Additional billing controls

- A change affecting invoices, payment state, or refunds requires a written rollback note.
- Do not alter migration files after they have merged.
- Before review, run the billing feature tests named by the CI workflow and attach the job URL.
- Escalate ambiguous payment-state changes to `database-owners` and `billing-maintainers`.
```

The filesystem supports this model well, but review must verify it. When adding an override, inspect the actual changed paths, not just the author’s summary. When moving a directory, search for instruction files and manifest scopes that referenced the old location. When deleting a local policy, confirm that its protections are inherited elsewhere.

![Scoped repository policy tree: root, scope, and protected boundaries](/img/coding-agent-policy-change-control-2.png)

## Evidence artifacts separate compliance from assertion

“Agent followed instructions” is not useful evidence. A reviewer needs an artifact tied to the change: a passing CI job, a command result, a migration plan, a screenshot from a visual check, a security scan, or an approved exception record.

Evidence should be proportionate. Requiring a production-like test environment for a documentation typo wastes time and teaches people to bypass the process. Requiring no evidence for a schema change is reckless. The policy should state the smallest artifact that materially reduces uncertainty for each class of work.

A repository can validate structural policy requirements in CI even when it cannot prove every human judgment. The following script checks that a changed policy manifest contains required control fields and that every referenced owner is declared. It is not a complete governance engine. It is a cheap tripwire against malformed policy edits.

```python
#!/usr/bin/env python3
# scripts/validate_agent_policy.py
from pathlib import Path
import sys
import yaml

path = Path("policy/agent-policy.yaml")
data = yaml.safe_load(path.read_text())
errors = []

if not data.get("policyOwner"):
    errors.append("policyOwner is required")

for control in data.get("controls", []):
    control_id = control.get("id", "<unnamed>")
    for field in ("scope", "owner", "changeReview", "rollback"):
        if not control.get(field):
            errors.append(f"{control_id}: missing {field}")
    paths = control.get("scope", {}).get("paths", [])
    if not paths:
        errors.append(f"{control_id}: scope.paths must not be empty")
    groups = control.get("changeReview", {}).get("requiredGroups", [])
    if not groups:
        errors.append(f"{control_id}: required review group is missing")

if errors:
    print("Agent policy validation failed:")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print("Agent policy validation passed")
```

Wire this into pull requests that touch `AGENTS.md`, `CLAUDE.md`, Copilot instruction files, `CODEOWNERS`, or `policy/**`. The trigger list matters: an agent policy is made of more than one file. An approval rule changed in `CODEOWNERS` can weaken the policy even when the manifest remains untouched.

Preserve the evidence where reviewers already work. A pull-request checklist is better than a separate dashboard nobody opens. CI annotations are better than a shell transcript pasted into a chat thread. If an agent opens the pull request, require it to identify commands it ran, commands it did not run, and deviations from policy. Failure to run a required command is not automatically failure of the change; it is an escalation event that needs a human decision.

### Field note: keep the contract close to the stack you operate

For a Laravel/Vue product, a root contract can establish the common test and review expectations, while `app/`, `database/`, and `resources/js/` each carry narrower rules. In a Modoo or Hermes-driven workflow, use the agent’s repository instructions as an input to review, not as a substitute for review. The durable pattern is the same: local context informs execution; repository ownership decides exceptions; CI and pull-request artifacts record what occurred.

That approach avoids invented claims about a particular team’s velocity or outcomes. It is a workflow design that can be inspected in the repository.

## Rollback is the test of whether policy has been engineered

Every policy change has a failure mode. A new command may be unavailable in a clean CI runner. A path match may block unrelated work. A strict requirement may turn out to be applied at the wrong layer. An exception may stay long after the emergency that justified it.

If the response is “we will edit the file again,” the policy has no real rollback plan. A proper rollback identifies the commit to revert, the enforcement it changed, the owner who can authorize reversal, and the safety action needed if the affected code already shipped.

Separate policy rollback from product rollback. Reverting a rule that required migration plans does not revert a migration. Reverting a guard that blocked deployment files does not remove a bad deployment. The policy record should say which operational runbook applies once a rule failure affects a released system.

Practice rollback on low-risk policy changes. Introduce a harmless required field in a manifest, confirm CI blocks an incomplete edit, then revert it and confirm normal changes proceed. This validates the policy delivery chain: discovery, inheritance, review routing, enforcement, and recovery.

Temporary overrides deserve special handling. Put an expiry date and removal issue in the rule itself or its manifest. Add a scheduled check that flags expired entries. A temporary bypass without an expiry is an unreviewed permanent policy change disguised as urgency.

![Coding-agent policy change control timeline: propose, verify, and revert](/img/coding-agent-policy-change-control-3.png)

## What you should do Monday morning

Do not begin by writing a 500-line instruction manual. Start with one repository and one risky workflow.

1. Inventory every current instruction surface: `AGENTS.md`, `CLAUDE.md`, Copilot instruction files, `CODEOWNERS`, CI workflows, pull-request templates, and local agent configuration that has leaked into the repository.
2. Choose the highest-leverage rule already present. Good candidates include migration changes, deployment configuration, secrets, dependency updates, or payment flows.
3. Name the owner and review group for that rule. If nobody can accept responsibility, the rule is not ready to govern automated work.
4. Write a compact root contract with a default test command, evidence expectation, escalation rule, and links to local instructions.
5. Add one scoped override for a genuinely different directory. State what it adds, not a full copy of the root policy.
6. Create a small manifest like the example above and a CI check that validates its required fields.
7. Open a policy-change pull request using the review table in this article. Ask reviewers to challenge scope, evidence, and rollback rather than copyediting prose.
8. Add an expiry check for temporary overrides and schedule its review with the team that owns the control.

This sequence produces a working control loop quickly. It also reveals where policy is being asked to solve a tooling problem. If the team cannot reliably run a test command, fix the test environment. Do not hide that weakness behind a vague agent instruction.

## How to verify this advice

Verification should happen in a real repository, against a real pull-request path.

First, create a test branch that changes a file inside and outside a scoped directory. Confirm that the instructions and required reviewers differ exactly as intended. If the result is surprising to a human reviewer, it will be surprising to an agent.

Second, make an intentionally incomplete policy-manifest edit: remove an owner, scope path, review group, or rollback strategy. Run the validation script locally and in CI. It should fail with a direct, actionable message. Restore the field and confirm the check passes.

Third, simulate an exception. Add a temporary scoped override with an expiry and compensating evidence requirement. Confirm that the designated owners must approve it, the pull request exposes the expiry, and an automated check can find it after the date passes.

Fourth, test a rollback. Revert a harmless policy commit in a branch, run the same CI gate, and verify that the previous behavior returns. Record any manual action required. This is the moment where a policy stops being a document and proves it is part of your delivery system.

Finally, sample a merged agent-assisted pull request. Can a reviewer locate the applicable instructions, see the commands or artifacts, identify the approver for any exception, and understand the rollback plan? If not, improve the policy’s evidence route before adding more rules.

## Further reading

- {{< source href="https://developers.openai.com/codex/guides/agents-md" label="OpenAI Codex documentation on AGENTS.md, hierarchy, and scoped instructions" >}}
- {{< source href="https://docs.anthropic.com/en/docs/claude-code/github-actions" label="Anthropic documentation on Claude Code GitHub Actions and CLAUDE.md project rules" >}}
- {{< source href="https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide" label="GitHub documentation on repository and path-specific Copilot instructions" >}}
- Browse more operating patterns in [Developer Tools](/developer-tools/), [AI Agent Operations](/ai-agent-operations/), and [Laravel + Vue SaaS](/laravel-vue-saas/).

The useful outcome is not an impressive policy file. It is a repository where coding-agent instructions have accountable owners, reviewable changes, deliberate scope, visible evidence, and a way back when the rule is wrong.
