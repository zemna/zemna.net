---
title: "A Repeatable Review Harness for AI-Generated Code After the First Merge Gate"
date: 2026-07-07T07:00:00+07:00
draft: false
description: "The first merge gate catches obvious AI coding mistakes. A repeatable review harness catches the slower failures: drift, missing rollback paths, weak tests, and agent changes that look fine until production maintenance begins."
topics: ["tutorial", "ai-agents", "developer-tools"]
tags: ["ai-generated-code", "code-review", "ci", "release-engineering", "regression-testing", "agent-verification"]
cover: /covers/ai-code-review-harness.png
seo:
  primaryQuery: "ai code review harness"
  secondaryQueries:
    - "review ai generated code after merge"
    - "ai generated code regression testing"
    - "post merge review process for coding agents"
---

The first merge gate is where teams feel safe too early.

An AI agent opens a pull request. The code compiles. The unit tests pass. A human reviewer scans the diff, asks for two naming changes, and merges. Everyone moves on because the gate did its job.

Then the slower problems start. The new route bypasses an old authorization check. A background job retries forever because the agent copied the wrong timeout pattern. The test passes because it asserts a mocked response, not the real boundary. The rollback plan is missing because the change looked small. Three weeks later, another agent edits the same area and treats that weak pattern as local convention.

That is the part I care about. The question is not whether AI-generated code can pass review. The question is whether it survives maintenance, handoff, production rollback, and the next agent that touches it. Working as a software architect in Indonesia makes this practical rather than theoretical: vendor callbacks, deployment windows, and handoff notes decide whether a change survives the week.

This post is about the harness I want after the first merge gate: a repeatable, boring, evidence-heavy review loop for AI-generated code. Not another proof checklist. The proof checklist belongs before merge. This one runs after the first gate and keeps running while the code becomes part of the system.

<!--more-->

GitHub's own guidance on agent pull requests says reviewers should treat agent work as a collaboration artifact and review intent, tests, and risk rather than just the patch shape ([GitHub Blog](https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/)). The Code as Agent Harness survey describes harnesses as structured environments around agents, tasks, evaluation, and feedback loops rather than one-off prompts ([arXiv](https://arxiv.org/html/2605.18747v1)). That framing matters. If agents are going to submit production code, review cannot stay as a single human moment in a pull request UI.

I already use this mental model in my own agent operations work. The same thinking shows up in [/ai-agent-operations/](/ai-agent-operations/), [/developer-tools/](/developer-tools/), and the practical path I keep for new readers at [/start-here/](/start-here/). If you have read my pieces on [agent edit contracts](/blog/the-agent-edit-contract-i-use-before-a-coding-agent-touches-a-repo/) or [zero-cost observability for agent crons](/blog/zero-cost-observability-agent-crons/), this post is the missing middle: what happens after the code gets through the door.

![Review harness flow](/img/ai-code-review-harness-1.png)

## The first merge gate is necessary but too narrow

A merge gate answers a narrow question: "Can this change enter the main branch right now?" That is useful. It is also incomplete.

The gate usually checks static properties. Does it compile? Does it pass lint? Do tests pass? Did the reviewer approve? Is the diff small enough? Does the agent mention the issue number? Those checks are good because they are cheap and deterministic. Martin Fowler's writing on continuous integration still holds: frequent integration works when the mainline stays healthy and the feedback loop stays short ([Martin Fowler](https://martinfowler.com/articles/continuousIntegration.html)).

AI-generated code changes the failure profile. The obvious failure is a hallucinated API or broken import. Your CI catches that. The worse failure is plausible code that fits the local syntax but not the operational contract.

A few examples from real maintenance work:

- A generated migration adds a nullable column but the application path treats it as required.
- A generated queue worker handles the success path and silently eats the retry path.
- A generated test asserts what the mock was told to return.
- A generated refactor copies an old anti-pattern because the repo contains that pattern nearby.
- A generated fix changes behavior but leaves runbooks, dashboards, and alerts behind.

Those failures pass the merge gate because the gate is not watching for the system becoming harder to operate.

Google's SRE book treats release engineering as a discipline of repeatability, automation, hermetic builds, and auditable releases, not as a heroic last step ([Google SRE](https://sre.google/sre-book/release-engineering/)). That is the right direction for AI code review. The harness should turn "we reviewed it" into a set of artifacts that can be replayed.

A post-merge harness should answer four questions:

| Question | Artifact |
|---|---|
| Did the agent change what it claimed? | intent record |
| Did the risky paths get exercised? | scenario tests |
| Can we see it in production? | signal map |
| Can we back it out? | rollback note |

Keep the table narrow because the point is discipline, not theater. If you cannot point to an artifact, the review did not happen in a way the next maintainer can use.

{{< field-note title="Field note" >}}
On Modoo Laravel SaaS projects, the dangerous agent change is rarely the file that looks complex. It is the tiny change that touches a queue, an import path, or a marketplace callback and then disappears into normal deployment flow. I want the harness to leave evidence near the system boundary: which job was touched, which alert should move, which rollback command exists, and which test proves the integration still behaves. That is maintenance work, not prompt craft.
{{< /field-note >}}

## What the harness actually reviews

A review harness is not one tool. It is a small operating system around AI-generated changes.

I split it into five lanes:

1. intent capture
2. risk classification
3. evidence generation
4. runtime observation
5. feedback into future agent work

The lanes are simple because simple survives. A harness with thirty categories becomes another abandoned checklist. A harness with five lanes can be automated, reviewed, and improved.

The first lane captures what the agent intended to do. This is not a marketing summary. It is a short machine-readable claim file attached to the pull request or generated after merge. It names the files, boundaries, assumptions, and rollback path.

The second lane classifies risk. Authentication, billing, data deletion, migrations, queues, external APIs, and permissions get treated differently from CSS cleanup. The risk lane decides which scenarios must run.

The third lane generates evidence. This includes tests, trace samples, screenshots, CLI output, migration dry runs, or replayed fixtures. A harness that cannot show evidence becomes an opinion machine.

The fourth lane watches runtime. Did the alert move? Did the job duration change? Did error rate climb? Did a cron still produce an artifact? For AI agent pipelines, I have written about [zombie detection](/blog/your-ai-agent-pipeline-has-no-zombie-detection-heres-how-to-add-it/) because exit code zero is not a success signal. The same rule applies to generated code.

The fifth lane feeds back into the next agent run. If the agent keeps forgetting rollback notes, change the agent contract. If it keeps writing shallow tests, add an evaluation fixture. If it keeps touching deprecated code, put a deny rule in the repo map.

Here is the smallest policy file I would accept in a production repo:

```yaml
# .review-harness/ai-change-policy.yml
version: 1
risk_lanes:
  auth:
    match:
      paths:
        - "app/Policies/**"
        - "app/Http/Middleware/**"
        - "routes/api.php"
    required_evidence:
      - authorization_scenario
      - negative_case_test
      - rollback_note
  queues:
    match:
      paths:
        - "app/Jobs/**"
        - "app/Console/Commands/**"
    required_evidence:
      - retry_behavior_test
      - idempotency_note
      - runtime_metric
  migrations:
    match:
      paths:
        - "database/migrations/**"
    required_evidence:
      - migration_dry_run
      - backward_compatibility_note
      - rollback_note
default_required_evidence:
  - intent_record
  - changed_files_summary
  - reviewer_signoff
```

This file does not judge code quality by itself. It tells the harness what kind of proof to ask for. That is already better than asking every reviewer to remember every production hazard while reading a 900-line generated diff at 5 p.m.

![Pull request evidence loop](/img/ai-code-review-harness-2.png)

## The claim file: make the agent say what changed

The fastest way to review AI-generated code is to force the agent to make falsifiable claims.

A human reviewer can skim a diff and infer intent. An agent should not get that benefit. Make it state intent in a durable file. The claim file should be short enough for humans and structured enough for automation.

I prefer a JSON file stored as a CI artifact, not necessarily committed forever. For high-risk changes, commit it under `.review-harness/claims/` so future agents can learn from it.

```json
{
  "change_id": "pr-1842",
  "author": "coding-agent",
  "summary": "Add idempotent retry handling for marketplace import jobs",
  "system_boundary": "queue:marketplace-imports",
  "assumptions": [
    "provider event IDs are stable across retries",
    "duplicate imports must not create duplicate order rows"
  ],
  "risk_lanes": ["queues", "external-api"],
  "expected_evidence": [
    "retry_behavior_test",
    "idempotency_note",
    "runtime_metric"
  ],
  "rollback": {
    "type": "feature-flag",
    "flag": "marketplace_import_retry_v2",
    "owner": "platform"
  }
}
```

There are two important details here.

First, the agent must name assumptions. Bad generated code often hides in assumptions: "this field always exists," "this callback only arrives once," "this user can see this resource." When assumptions become text, reviewers can attack them.

Second, the rollback path is part of review. If the rollback plan is "revert the PR," the change is not ready for risky lanes. Reverting a migration, a queue contract, or an external API behavior is not the same as reverting a button color.

Augment's CTO checklist for AI coding pushes teams to set boundaries, review generated code, and keep humans responsible for architecture and security decisions ([Augment](https://www.augmentcode.com/guides/cto-ai-coding-checklist)). A claim file turns that advice into a concrete handoff artifact. The agent can write it. CI can validate it. The reviewer can reject it.

You can enforce the claim file with a tiny script:

```bash
#!/usr/bin/env bash
# scripts/verify-ai-claim.sh
set -euo pipefail

CLAIM_FILE="${1:-.review-harness/claim.json}"

required_fields=(summary system_boundary assumptions risk_lanes expected_evidence rollback)

if [[ ! -f "$CLAIM_FILE" ]]; then
  echo "missing claim file: $CLAIM_FILE" >&2
  exit 1
fi

for field in "${required_fields[@]}"; do
  if ! jq -e ".${field}" "$CLAIM_FILE" >/dev/null; then
    echo "missing field: ${field}" >&2
    exit 1
  fi
done

if [[ "$(jq '.assumptions | length' "$CLAIM_FILE")" -eq 0 ]]; then
  echo "claim file must name at least one assumption" >&2
  exit 1
fi

jq -r '.expected_evidence[]' "$CLAIM_FILE" | sort -u
```

That script is intentionally plain. The goal is not a clever framework. The goal is to make missing review evidence fail loudly.

## Put the harness in CI, but do not stop at CI

CI is the right place to start because it is already the team's shared gate. But the post-merge harness should not pretend CI sees everything.

Use CI for deterministic checks:

- claim file exists and has required fields
- risk lanes match changed paths
- required evidence artifacts exist
- targeted tests ran
- migration dry run completed
- generated code did not touch denied paths

Use runtime systems for behavior checks:

- queue duration
- retry count
- error rate
- authorization failures
- import duplicate count
- feature flag exposure
- rollback execution result

Here is a GitHub Actions workflow that implements the CI half. It assumes the claim file exists and the policy file from earlier lives in the repo.

```yaml
# .github/workflows/ai-review-harness.yml
name: ai-review-harness

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  push:
    branches: [main]

jobs:
  harness:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: read
    steps:
      - uses: actions/checkout@v4

      - name: Install tools
        run: |
          sudo apt-get update
          sudo apt-get install -y jq

      - name: Verify AI claim file
        run: |
          scripts/verify-ai-claim.sh .review-harness/claim.json \
            | tee /tmp/required-evidence.txt

      - name: Run targeted queue tests
        if: contains(hashFiles('app/Jobs/**'), '') == false
        run: |
          php artisan test --testsuite=Feature --filter=Queue

      - name: Check required evidence artifacts
        run: |
          while read -r evidence; do
            test -f ".review-harness/evidence/${evidence}.md" || {
              echo "missing evidence artifact: ${evidence}" >&2
              exit 1
            }
          done < /tmp/required-evidence.txt

      - name: Upload harness artifacts
        uses: actions/upload-artifact@v4
        with:
          name: ai-review-harness
          path: |
            .review-harness/claim.json
            .review-harness/evidence/*.md
```

The `if` expression above is deliberately conservative; in a real repo I usually replace it with a changed-files step that maps paths to lanes. The key pattern is the artifact upload. You want the review record to survive the merge.

For runtime checks, create a small post-deploy job. It does not need to be fancy. It should ask whether the thing you were worried about moved.

```bash
#!/usr/bin/env bash
# scripts/post-deploy-ai-harness.sh
set -euo pipefail

service="${1:?service name required}"
window="${2:-30m}"

php artisan queue:monitor --queue=marketplace-imports --window="$window"
php artisan harness:check-duplicates --service="$service" --window="$window"
php artisan harness:check-error-budget --service="$service" --window="$window"

printf 'post-deploy harness passed for %s over %s\n' "$service" "$window"
```

That script is not universal. It is a template for the shape of the check: name the boundary, inspect a narrow window, fail if the operational contract broke. In a Laravel system, these checks can be Artisan commands. In a Node service, they can be npm scripts. In a Kubernetes setup, they can query Prometheus and logs.

{{< note type="warning" title="Do not turn the harness into a second fake gate" >}}
A harness that only checks whether a Markdown file exists will decay. The evidence file must contain output, links, commands, or test names that a maintainer can replay. If the artifact cannot help during an incident, it is paperwork.
{{< /note >}}

![Rollback package diagram](/img/ai-code-review-harness-3.png)

## Regression tests for agent behavior, not just product behavior

LLM regression testing is usually described as checking whether model outputs stay stable across versions, prompts, or datasets ([FutureAGI](https://futureagi.com/glossary/llm-regression-testing/)). That idea applies directly to coding agents. The product test asks, "Does the application still work?" The agent regression test asks, "Does the agent still produce reviewable, maintainable changes under our rules?"

Both matter.

I like to keep a small suite of agent review fixtures. Each fixture is a fake task or captured historical task with an expected review outcome. The agent does not need to solve the whole product. It needs to demonstrate that it respects the repo contract.

Example fixtures:

| Fixture | Expected failure |
|---|---|
| migration without rollback | missing rollback note |
| queue job without idempotency | missing idempotency evidence |
| auth policy edit | missing negative authorization test |
| external API callback | missing replay fixture |

The harness can run these fixtures weekly or before changing the agent prompt. If the agent starts passing code while skipping evidence, the prompt or tool wrapper regressed.

Here is a small TypeScript test for a claim validator. It is not testing your product. It is testing the review harness itself.

```ts
// tests/claim-validator.test.ts
import { describe, expect, it } from "vitest";
import { validateClaim } from "../src/claim-validator";

const baseClaim = {
  change_id: "fixture-queue-1",
  author: "coding-agent",
  summary: "Change queue retry behavior",
  system_boundary: "queue:imports",
  assumptions: ["provider event IDs are stable"],
  risk_lanes: ["queues"],
  expected_evidence: ["retry_behavior_test", "idempotency_note"],
  rollback: { type: "feature-flag", flag: "import_retry_v2" }
};

describe("validateClaim", () => {
  it("rejects queue changes without idempotency evidence", () => {
    const claim = {
      ...baseClaim,
      expected_evidence: ["retry_behavior_test"]
    };

    expect(validateClaim(claim)).toEqual({
      ok: false,
      missing: ["idempotency_note"]
    });
  });

  it("accepts a queue claim with rollback and evidence", () => {
    expect(validateClaim(baseClaim)).toEqual({ ok: true, missing: [] });
  });
});
```

The important move is to test the harness against known bad agent behavior. Most teams only test the application. Then they change the coding agent prompt, switch models, or add a new tool and wonder why review quality drifts.

This is where the Code as Agent Harness framing earns its keep. A harness is not a prompt wrapper. It includes tasks, evaluators, environment constraints, and feedback ([arXiv](https://arxiv.org/html/2605.18747v1)). For production software teams, the evaluator should include maintainability and operational proof.

## Feed production evidence back into the next prompt

The post-merge harness becomes valuable when it changes future agent behavior.

If the agent gets a review comment saying "add idempotency evidence," that comment helps once. If the harness records that missing evidence and updates the agent instruction, it helps every later queue change.

I keep a small feedback file in the repo. It is not a giant constitution. It is a list of concrete lessons the agent must follow when touching specific boundaries.

```yaml
# .review-harness/agent-feedback.yml
boundaries:
  queue:marketplace-imports:
    required_patterns:
      - "Use idempotency keys for provider event IDs."
      - "Add a retry test with the same event delivered twice."
      - "Name the metric that should move after deploy."
    denied_patterns:
      - "Do not swallow exceptions without reporting."
      - "Do not create order rows before duplicate checks."
  auth:api:
    required_patterns:
      - "Add one positive and one negative authorization case."
      - "Mention the policy or middleware that enforces access."
```

The next time an agent starts work, the repo wrapper can load the relevant boundary section into context. This is better than telling the agent to "be careful." It names the scars.

There is also a management benefit. The harness separates agent quality problems from product quality problems. If the app fails because a business rule changed, that is normal software work. If the agent repeatedly skips rollback notes, that is a harness or instruction failure. Fix the system that produces changes, not only the single change.

For smaller teams, this matters because review time is finite. You do not want senior engineers re-teaching the same lesson every week. You want the harness to remember.

![Minimal review harness checklist](/img/ai-code-review-harness-4.png)

## What you should do Monday morning

Do not build the whole harness at once. Start with one risky lane and make it real.

Pick one boundary where AI-generated code can hurt you. I would choose queues, auth, billing, migrations, or external API callbacks. Then do this:

1. Create `.review-harness/ai-change-policy.yml` with one lane.
2. Require a claim file for AI-authored or AI-assisted pull requests in that lane.
3. Add one CI step that rejects missing assumptions and rollback notes.
4. Add one evidence artifact that contains real command output.
5. Add one post-deploy check for the runtime signal that should move.
6. Save one lesson into `agent-feedback.yml` after the first review.

That is enough for week one.

Here is the Monday version for a queue-heavy Laravel codebase:

```bash
mkdir -p .review-harness/evidence scripts
cp /tmp/templates/ai-change-policy.yml .review-harness/ai-change-policy.yml
cp /tmp/templates/claim.json .review-harness/claim.json
chmod +x scripts/verify-ai-claim.sh

scripts/verify-ai-claim.sh .review-harness/claim.json
php artisan test --filter=MarketplaceImportJobTest
php artisan queue:monitor --queue=marketplace-imports --window=30m
```

Replace the template paths with your own files. The commands are intentionally ordinary. A review harness should feel like normal engineering work.

After that, add one small rule to your agent prompt or agent wrapper:

```text
When changing files matched by .review-harness/ai-change-policy.yml,
create or update .review-harness/claim.json before proposing the diff.
Name assumptions, required evidence, and rollback path. Do not mark the task
complete until scripts/verify-ai-claim.sh passes.
```

That rule will not make the agent perfect. It will make the agent easier to review. That is the target.

If you already run agent crons, connect the same concept to artifact checks. I wrote about cron artifacts in [The 5 Cron Patterns That Lie to You](/blog/the-5-cron-patterns-that-lie-to-you-exit-0-doesnt-mean-success/) because scheduled agents often report success while leaving no useful output. A code review harness has the same principle: success is not "the agent said done." Success is a replayable artifact plus a signal that the system still behaves.

### Further reading

- GitHub Blog, [Agent pull requests are everywhere. Here's how to review them.](https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/)
- Martin Fowler, [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)
- Google SRE Book, [Release Engineering](https://sre.google/sre-book/release-engineering/)

A repeatable harness will feel slow for the first few changes. Then it becomes the place where the team stores judgment.

That is the part worth keeping. AI-generated code does not need magical review. It needs the same production discipline we already apply to releases, incidents, migrations, and handoffs. The difference is volume. Agents can produce more changes than your team can carefully remember. So stop relying on memory.

Make the agent leave claims. Make CI collect evidence. Make production signals answer back. Make the next prompt inherit the lesson.
