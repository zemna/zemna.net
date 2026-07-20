---
title: "Git trailers turn a commit into a handoff contract"
description: "Use Git trailers, CI checks, and Git notes to make each commit carry a compact, reviewable handoff record."
date: 2026-07-20T07:00:00+07:00
draft: false
slug: git-trailers-handoff-contract
topics: ["tutorial"]
tags: ["git", "git-trailers", "commit-messages", "continuous-integration", "developer-workflow", "code-review"]
cover: "/covers/git-trailers-handoff-contract.png"
seo:
  primaryQuery: "git trailers handoff contract"
  secondaryQueries: ["git interpret-trailers tutorial", "validate git commit trailers ci", "git notes review links"]
---

A commit already records code and a message. For a team that hands work between people, time zones, and automated checks, that is often not enough. Someone needs to know what changed, what verified it, where the review discussion lives, and whether there is a follow-up that should not vanish into a chat thread.

Senior engineering judgment is often less about adding a new system and more about noticing when an existing primitive has been left underused. Git commit messages already have a footer area, Git already knows how to parse it, and CI already has a stable commit object to inspect. That is a good place to put a small contract.

Git trailers are structured footer lines in a commit message, such as `Reviewed-by:`, `Tested-by:`, or a team-defined `Runbook:`. `git interpret-trailers` can parse and add those lines; it does not make a workflow mandatory by itself. The enforcement comes from people, hooks, CI, or repository rules that choose to inspect the result. [Source: https://git-scm.com/docs/git-interpret-trailers]

This tutorial builds a practical pattern: trailers hold the durable minimum, CI validates the shape, and Git notes hold supplementary links that do not belong in every commit message. It is a narrow pattern, but it gives a commit enough context to become a credible handoff point.

![Structured Git trailers as a commit handoff contract](/img/git-trailers-handoff-contract-1.png)

{{< note >}}
A handoff contract should be short enough that authors keep using it. If a required footer feels like a compliance essay, it will be copied badly or omitted. Start with fields that answer a real question during review, incident response, or the next shift.
{{< /note >}}

## What Git trailers actually give you

A trailer is a line with a token and a value, normally placed at the end of a commit message. By default, Git recognizes `:` as the trailer separator in message text; `=` is accepted in a `--trailer` command-line argument for compatibility. A blank line separates the message body from the trailer block. That placement matters: the footer remains readable to humans and recognizable to Git tooling. [Source: https://git-scm.com/docs/git-interpret-trailers]

The familiar `Signed-off-by:` footer is a trailer, but it is not the only useful one. A product team can define a tiny vocabulary around the questions that recur after code lands:

| Trailer | Question it answers | Example value |
|---|---|---|
| `Review:` | Where is the decision record? | `https://code.example/reviews/482` |
| `Verify:` | What concrete check passed? | `ci:deploy-smoke` |
| `Runbook:` | Where is the operational procedure? | `billing-retry` |
| `Follow-up:` | What deliberately remains? | `OPS-173` |

This is not a claim that Git validates those meanings. Git sees structured text. Your team decides what `Verify:` means, which values are acceptable, and whether a missing footer blocks a merge. The benefit comes from a shared convention that is cheap to parse with both a shell command and a human eye.

The distinction between subject, body, and footer is useful. The subject should still describe the change in ordinary language. The body should explain a decision when a diff cannot. The trailers should be facts or references with a stable shape. Do not bury `Verify: ci:deploy-smoke` in a paragraph where a script has to guess whether it is current, quoted, or hypothetical.

A concrete message looks like this:

```git
fix(billing): retry idempotent webhook delivery

Keep the provider event ID as the idempotency key so a retry does not
create a second invoice update after a transient upstream timeout.

Review: https://code.example/reviews/482
Verify: ci:unit,ci:deploy-smoke
Runbook: billing-webhook-retries
Follow-up: OPS-173
```

Git's `interpret-trailers` command has options for parsing, adding, replacing, and filtering trailers. It also supports configuration for aliases and placement behavior. That lets a repository standardize its writing without asking every contributor to memorize string surgery. [Source: https://git-scm.com/docs/git-interpret-trailers]

The first discipline is restraint. A footer full of project management metadata is a second issue tracker hidden in a commit. Keep only details whose absence causes a repeated handoff failure. On a Modoo Laravel SaaS project, for example, a `Runbook:` reference earns its place if an on-call engineer needs it after a queue or webhook change. A `Verify:` entry earns its place if an agent-run check has a named result a human can inspect.

{{< source href="https://git-scm.com/docs/git-interpret-trailers" label="Git interpret-trailers documentation" >}}

## Design a small contract before you automate it

The useful schema is the one a reviewer can check without opening another system. Begin with two required trailers and one optional trailer. For a service repository, a sensible first version is:

- `Review:` required for changes merged through a review system.
- `Verify:` required, carrying one or more named checks.
- `Runbook:` optional, only where a production procedure is relevant.
- `Follow-up:` optional, only for a consciously deferred item.

Avoid a generic `Status:` trailer. Its values turn into ambiguous prose: “done”, “ready”, “checked”. Prefer an identifier that points at an observable artifact or a normalized check name. `Verify: ci:phpunit` gives CI something precise to compare. `Verify: tested locally` gives an auditor very little.

Choose token spelling once. Git's configuration supports trailer keys, and the documentation describes how trailer names can be configured and used by `interpret-trailers`. [Source: https://git-scm.com/docs/git-interpret-trailers] The policy choice remains yours: use title-style tokens such as `Review:` consistently, or lower-case tokens if your tooling expects them. Do not accept both forever unless you deliberately normalize them.

Here is a repository-local configuration example. It gives contributors short aliases while preserving the canonical trailer keys in the message:

```bash
git config trailer.review.key "Review: "
git config trailer.review.where end
git config trailer.verify.key "Verify: "
git config trailer.verify.where end
git config trailer.runbook.key "Runbook: "
git config trailer.followup.key "Follow-up: "

git interpret-trailers --trailer "review:https://code.example/reviews/482" \
  --trailer "verify:ci:phpunit" \
  --trailer "runbook:billing-webhook-retries" \
  < .git/COMMIT_EDITMSG
```

The command reads input and writes the transformed message to standard output unless you choose an in-place workflow around it. Test the exact behavior in your repository before putting it in a hook. The manual documents options such as `--trailer`, `--parse`, and configuration-driven behavior; those details are why invoking Git is safer than maintaining a home-grown footer parser. [Source: https://git-scm.com/docs/git-interpret-trailers]

A contract also needs an escape hatch. Some commits have no external review link: an emergency repair, an imported upstream patch, or a mechanical version bump. Decide whether `Review: none` is an allowed explicit value or whether a different trailer such as `Exception:` names an approved reason. The point is not to remove judgment. It is to make exceptions visible instead of indistinguishable from omission.

Do the same for verification. A documentation-only change may not run the same suite as a migration. Your CI policy can accept a small vocabulary, such as `ci:docs`, `ci:phpunit`, `ci:deploy-smoke`, and `manual:staging-check`, then reject free-form values. That makes reporting possible later without pretending that a token proves the test was meaningful.

![A compact Git trailer schema with an exception path](/img/git-trailers-handoff-contract-2.png)

{{< details summary="A schema question worth asking in review" >}}
If the author writes `Verify: ci:phpunit`, can the reviewer identify the matching job and its commit SHA? If the answer is no, either rename the value to match the job or stop treating the trailer as evidence. Names are only useful when they join to something real.
{{< /details >}}

## Add trailers without turning commits into manual paperwork

Typing the same footer lines is tolerable for a week and irritating after a quarter. The goal is not to conceal the data entry but to make the correct entry the easy one. Use a commit-message template for discoverability, then use `git interpret-trailers` for modifications that need predictable placement.

A lightweight template makes the contract visible at commit time:

```git
# .gitmessage
# Explain the change and any decision a future reader needs.

Review:
Verify:
# Runbook:
# Follow-up:
```

Configure it for a developer with `git config commit.template .gitmessage`, or document an equivalent repository setup. Commented lines guide the author without becoming message content. The two blank-line boundary remains important: trailers belong after the body, not mixed into it.

For repeatable local setup, a small script can take values from the current branch or environment. Keep scripts conservative: a missing review URL should remain obvious, not be silently fabricated. This example appends only the fields supplied by the caller:

```bash
#!/usr/bin/env bash
set -euo pipefail

message_file="$1"
review_url="${2:-}"
verify_name="${3:-}"

args=()
[[ -n "$review_url" ]] && args+=(--trailer "Review:$review_url")
[[ -n "$verify_name" ]] && args+=(--trailer "Verify:$verify_name")

git interpret-trailers "${args[@]}" < "$message_file" > "$message_file.tmp"
mv "$message_file.tmp" "$message_file"
```

A `prepare-commit-msg` hook can call a script like this, but do not make the hook your only guard. Client-side hooks are local configuration. They help authors; they do not define a repository-wide assurance boundary. CI or the hosting platform must check the committed object after push.

`git log` helps you inspect the result without custom tooling. Its pretty formats can render trailer fields, and its `%(trailers)` placeholder has options to filter by key and change separators. The official `git log` documentation describes these pretty-format placeholders and their trailer-related options. [Source: https://git-scm.com/docs/git-log]

For example, a maintainer can see a recent ledger of review and verification references:

```bash
git log --pretty=format:'%h %s%n%(trailers:key=Review,separator=%x2c)%n%(trailers:key=Verify,separator=%x2c)%n' -20
```

Use this as a visibility tool, not proof that the commit meets policy. It reports whatever is in the message. A typo in a token, a stale URL, or an invented check name still looks structured. That is precisely why the validation layer exists.

There is also a social benefit to a template: it asks the author about handoff at the same moment they choose a commit message. A reviewer does not need to reconstruct where validation happened from scattered comments. The commit offers a compact index, while the diff and external systems still hold the evidence.

## Validate the contract in CI, and keep validation honest

CI should validate syntax and repository conventions, then link a trailer value to real evidence when an integration can do so. Start with syntax. A shell check can extract trailer lines through Git instead of splitting arbitrary commit text itself. The example below checks the commit under test, requires exactly one `Review:` and `Verify:` line, and restricts verification names to a known set.

```bash
#!/usr/bin/env bash
set -euo pipefail

sha="${1:?pass a commit SHA}"
trailers="$(git show -s --format='%(trailers:only,unfold)' "$sha")"

review_count="$(printf '%s\n' "$trailers" | grep -c '^Review: https://code\.example/' || true)"
verify_values="$(printf '%s\n' "$trailers" | sed -n 's/^Verify: //p')"

[[ "$review_count" -eq 1 ]] || { echo "need one Review: URL" >&2; exit 1; }
[[ -n "$verify_values" ]] || { echo "need Verify:" >&2; exit 1; }

while IFS= read -r value; do
  case "$value" in
    ci:phpunit|ci:deploy-smoke|ci:docs|manual:staging-check) ;;
    *) echo "unknown Verify value: $value" >&2; exit 1 ;;
  esac
done <<< "$verify_values"
```

The command relies on the `%(trailers)` formatting support documented for `git log` and related pretty formats. [Source: https://git-scm.com/docs/git-log] If your runner checks a merge commit rather than a pull request head, pass the SHA you mean to certify. This detail is easy to miss: a correct script against the wrong object gives a clean but irrelevant result.

Here is a minimal CI job shape. Adapt the event names and checkout behavior to your provider, but keep the core rule visible: fetch enough history for the target SHA, then validate that SHA.

```yaml
name: commit-handoff-contract
on:
  pull_request:

jobs:
  trailers:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Validate commit trailers
        run: |
          for sha in $(git rev-list origin/${{ github.base_ref }}..HEAD); do
            ./scripts/check-trailers.sh "$sha"
          done
```

The policy must say what happens for a branch with several commits. You can require every commit to comply, validate only the eventual squash-merge message, or validate a release commit created by automation. Each option answers a different question. Requiring every commit creates a useful internal record but increases friction during iterative work. Checking the final merge commit makes the handoff artifact cleaner but loses intermediate context. Pick one and state it in the repository contribution guide.

For Modoo Laravel SaaS work, agent verification deserves a clear boundary. An agent can run `php artisan test`, a static analysis job, or a staging smoke check and then propose `Verify: ci:phpunit`. The CI system should still record the actual job outcome against the real SHA. The trailer says what the commit claims was checked; the CI result says whether the named system accepted that claim. Do not collapse those two records.

{{< field-note >}}
On Laravel SaaS repositories with queue, payment, or webhook paths, keep the trailer vocabulary tied to verification that a maintainer can locate. For example, `Verify: ci:phpunit` can refer to the named test job, while `Runbook: billing-webhook-retries` points an operator to the procedure. If an agent prepares the commit, a human reviewer should verify that both references match the diff and the target SHA before merge.
{{< /field-note >}}

![CI validation connecting commit trailers to a verified artifact](/img/git-trailers-handoff-contract-3.png)

Validation should fail clearly. “Trailer policy failed” makes people rerun a job without learning anything. “Commit abc123 needs one Review: URL” tells the author what to repair. Also distinguish malformed from unauthorized: a URL with the wrong host is not the same mistake as no URL. Clear failure text keeps a contract from becoming a superstition.

## Use Git notes for supplementary evidence, not required context

Commit messages are replicated with commits and appear in normal history views. That makes them a good home for durable, compact handoff facts. Sometimes you need supporting material that is too changeable, too long, or too specific for the footer: a review summary, a benchmark document, a deployment transcript, or an incident timeline.

Git notes attach information to objects without changing those objects. The `git notes` documentation describes adding, showing, copying, merging, and removing notes, with notes stored under refs such as `refs/notes/commits`. [Source: https://git-scm.com/docs/git-notes] This separation is useful because adding a note does not rewrite the commit SHA.

Add a concise supplementary note after the durable commit is created:

```bash
git notes add -m "Staging verification: https://ci.example/runs/9912
Review summary: https://code.example/reviews/482#decision" 8f3c2ab

git notes show 8f3c2ab
git log --show-notes=refs/notes/commits -1 8f3c2ab
```

Do not put a required review URL only in a note. Git notes do not automatically transfer during a normal clone in the way commits and ordinary remote-tracking refs do. Teams need explicit fetch and push configuration for notes refs. The Git notes manual documents notes ref handling and configuration; test the refspecs used by your remote before making notes part of an operational workflow. [Source: https://git-scm.com/docs/git-notes]

Use an explicit setup such as this:

```bash
git config --add remote.origin.fetch '+refs/notes/*:refs/notes/*'
git push origin refs/notes/commits

git fetch origin '+refs/notes/*:refs/notes/*'
git log --show-notes=refs/notes/commits --oneline -5
```

Treat those commands as an example to adapt, not a universal repository default. Notes can have their own access expectations and merge behavior. The documentation covers notes merge strategies and notes ref configuration, so decide who may write them and how conflicts should be handled. [Source: https://git-scm.com/docs/git-notes]

The dividing line is straightforward:

| Put it in a trailer | Put it in a Git note |
|---|---|
| A compact item required to understand or validate the handoff | A supplementary link, transcript, or summary |
| Data every clone and normal log view should carry | Data your team fetches through an explicit notes-ref workflow |
| A stable identifier such as `Runbook: billing-webhook-retries` | A long operational observation or review rationale |

This avoids a common failure mode: notes become a secret second commit message. Keep the contract in trailers; use a note to add context after the fact without changing history. If the note contains a URL essential during an incident, also ensure the runbook or ticket system has the durable reference. Git alone should not be your only retrieval path for live operations.

![Git trailers and Git notes for durable and supplementary handoff context](/img/git-trailers-handoff-contract-4.png)

### Make the contract useful in everyday Git history

A contract works only when it helps someone who did not write the change. Use `git log` views that put the handoff fields near the subject. The `git log` documentation covers formatting, decorations, and trailer display controls, so make a shared alias after you confirm it renders well in your terminal. [Source: https://git-scm.com/docs/git-log]

For example:

```bash
git config alias.handoff "log --decorate --pretty=format:%C(auto)%h%Creset %s%n%(trailers:key=Review,separator=%x2c)%n%(trailers:key=Verify,separator=%x2c)%n"
git handoff -15
```

The alias is intentionally boring. It does not try to fetch a dashboard, resolve a ticket, or decide whether a test is trustworthy. It puts the two questions that slow a handoff into the history view: where was this reviewed, and what verification label did the author record?

Use the same restraint in code review. A reviewer should ask whether the trailers describe the change, not merely whether they are present. A migration that alters a production table with `Verify: ci:docs` is structurally valid and semantically wrong. A queue retry change with a runbook token that names an unrelated service is equally unhelpful. Automation can catch shape; review catches fit.

This pattern pairs well with a repository's existing working agreements. The guides on [developer tools](/developer-tools/) and [AI agent operations](/ai-agent-operations/) are useful places to document the command wrappers and human verification boundary. New contributors can start with [/start-here/](/start-here/) before adopting the local template, hooks, and aliases.

A small monthly audit closes the loop. Sample a handful of merged commits. Can a maintainer open the `Review:` destination? Does every `Verify:` value correspond to a job that exists? Were notes available to a fresh clone that followed the documented refspec setup? If the answer is no, fix the convention or the automation. Do not add another trailer as punishment.

The aim is a commit that says enough to be picked up without a meeting. It is not a replacement for review, CI, documentation, or operational judgment. It is the join between them: a stable object, a compact structured footer, and optional supplementary notes where their explicit distribution model is understood.

## What you should do Monday morning

1. Open one active repository and inspect ten recent merge commits with `git log --format=fuller -10`. Write down the two handoff questions that repeatedly require searching elsewhere.
2. Define exactly two required trailers. A practical starting point is `Review:` and `Verify:`. Write accepted values and one explicit exception rule in the contribution guide.
3. Add a `.gitmessage` template that shows those fields, then test a real commit message through `git interpret-trailers --parse`. Confirm that the blank-line boundary and token spelling behave as expected. [Source: https://git-scm.com/docs/git-interpret-trailers]
4. Add a CI check against the exact commit SHA your merge policy certifies. Make its error messages identify the missing or invalid field.
5. Decide whether Git notes solve a real supplementary-link problem. If yes, document and test explicit notes fetch and push refspecs with a fresh clone. Do not treat notes as automatically available. [Source: https://git-scm.com/docs/git-notes]
6. After one week, review false failures and ignored fields. Remove friction before expanding the schema. A two-field contract that people trust is better than a large footer no one reads.

## Further reading

- [Git `interpret-trailers` documentation](https://git-scm.com/docs/git-interpret-trailers) [Source: https://git-scm.com/docs/git-interpret-trailers]
- [Git notes documentation](https://git-scm.com/docs/git-notes) [Source: https://git-scm.com/docs/git-notes]
- [Git log documentation](https://git-scm.com/docs/git-log) [Source: https://git-scm.com/docs/git-log]
