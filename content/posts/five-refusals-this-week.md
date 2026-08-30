---
title: "Five Things I Refused This Week"
date: 2026-08-30T07:00:00+07:00
draft: false
slug: "five-refusals-this-week"
description: "A ranked cheat-sheet of five desk rules from this week: who pins the model, what .gitignore does not lock, who merges, who retries, and who still reads the diff."
topics: ["software-engineering"]
tags: ["coding-agents", "pull-requests", "code-review", "gitignore", "merge", "change-control"]
cover: /covers/five-refusals-this-week.png
seo:
  primaryQuery: "coding agent desk rules for pull requests"
  secondaryQueries:
    - "gitignore does not lock env files already tracked"
    - "named merge owner for agent pull request"
    - "abort is not stop retry owner"
---

The agent opened the pull request on Friday. Saturday morning nobody could name the model. The merge button still had no owner. The retry after abort sat in a chat log.

I did not ship a new tool this week. I refused five things. Rank them. Screenshot the list. Put the names on the ticket before Monday.

The question is not whether the agent demos well. The question is whether the change survives review, merge, retry, and the next person who has to roll it back.

<!--more-->

![Ranked cheat-sheet: five refusals this week](/img/five-refusals-this-week-1.png)

## The ranking, then the work

This is not a changelog. It is the five refusals from this desk this week, in the order I keep repeating them to the team.

| Rank | Refusal | What it forces on Monday |
| --- | --- | --- |
| 1 | The agent that wrote the PR does not pick the model | A named human writes author model and review model on the ticket before the first prompt |
| 2 | `.gitignore` is not a lock on `.env` | Treat ignore as a hint. Check tracked files. Turn on push protection |
| 3 | An agent PR has a named merge owner | One human owns the merge click. CODEOWNERS is a request, not that name |
| 4 | Abort is not stop | Abort needs a retry owner, a next time, and an artifact that proves the stop |
| 5 | Cheap code still needs a human review | Generated volume is not review capacity. Same model is a rewrite, not a review |

I already wrote the long form of rank 1 as [I Do Not Let a Coding Agent Pick Its Own Model](/blog/coding-agent-model-owner/). Rank 3 is the merge click from [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/). Rank 4 sits next to [A Green Cron Exit Is Not a Finished Job](/blog/a-green-cron-exit-is-not-a-finished-job/). This post is the ranked card, plus the files I actually put in the repo so a one-year developer can copy them.

{{< field-note title="Field note" >}}
On Laravel/Vue SaaS desks I keep the same five names even when the agent is fast: author model, review model, merge owner, retry owner, human reviewer. I do not Full-Auto a pull request I did not read. The agent writes the branch. A person still owns the ticket. That is how the work survives handoff when I am offline and someone else has to revert a migration.
{{< /field-note >}}

## 1. The agent that wrote the PR does not pick the model

Most teams leave the picker on **Auto** because the product copy says it will choose a good model. GitHub documents Auto as an intelligent router: it tracks health and availability, scores task complexity, and sends the work to a supported model under your plan and admin policies. Paid Copilot plans get a 10% discount on model cost while Auto is selected in Chat, CLI, the Copilot app, or the cloud agent. You can see which model answered: hover in Chat, read the CLI line, or look next to Auto in the app. [Source: https://docs.github.com/en/copilot/concepts/models/auto-model-selection]

That is a vendor default. It is not a name on the ticket.

When I open an agent pull request six hours later, I need two strings a junior can read:

- Author model: the model that wrote `routes/web.php`
- Review model: the model that is allowed to comment, if any — and it is not the author

Auto answers “which model felt cheap and available just now.” The pull request answers “which model authored this diff, and who decided that.” Keep those on a named human. I do not let the agent that wrote the branch pick either string.

GitHub also says Auto will not include models blocked by admin policy, models outside the plan, or models excluded by data-residency rules. [Source: https://docs.github.com/en/copilot/concepts/models/auto-model-selection] Availability is a floor. Assignment is a person.

Put both models in the pull request template. If the template is empty, I stop the run. I do not start a second session to “just try Auto.”

```markdown {linenos=inline,hl_lines=[3,"5-8"]}
## Agent session (required)

- Author model: (human-pinned, not Auto)
- Review model: (different from author, or “human only”)
- Pinned by: @username
- Ticket: PROJ-1234

Auto is not a model name. If you cannot fill author model, do not open the PR.
```

## 2. `.gitignore` is not a lock on `.env`

GitHub’s own ignore guide is short. You create `.gitignore` so Git skips files on **new** commits. If the file is already checked in, you untrack it first:

```shell
git rm --cached FILENAME
```

[Source: https://docs.github.com/en/get-started/git-basics/ignoring-files]

That is the whole trap. A coding agent can add `.env` to `.gitignore` and still leave `.env` in history. A junior sees the ignore rule and believes the secret is locked. Git does not untrack a file because you listed it.

Git’s own manual says the same thing in one line: a gitignore file specifies untracked files to ignore. Files already tracked are not affected. To stop tracking one, use `git rm --cached`, then add the pattern so it does not come back. [Source: https://git-scm.com/docs/gitignore]

I refuse the sentence “we gitignored it, so it is safe.”

Monday check, in this order:

1. Is `.env` in `.gitignore`? Necessary. Not sufficient.
2. Does `git ls-files` still list `.env` or `.env.local`? If yes, it is tracked. Untrack, rotate the secret, rewrite history only with a named owner.
3. Is GitHub push protection on? Ignore files do not scan commits. Push protection blocks known secret patterns before they land.

GitHub documents push protection as secret scanning that stops hardcoded credentials **before** they reach the repository: command line, GitHub UI, uploads, REST, and (for public repos) the GitHub MCP server. Repository-level push protection needs GitHub Secret Protection and is off by default until an admin turns it on. User-level push protection on github.com is on by default for pushes to **public** repositories. [Source: https://docs.github.com/en/code-security/concepts/secret-security/push-protection]

So: ignore is local Git advice. Push protection is a server gate. Neither one is “the agent promised it would not paste `.env`.”

```python {linenos=inline,hl_lines=["12-18"]}
#!/usr/bin/env python3
"""Fail CI if secret-like paths are still tracked."""
from __future__ import annotations

import subprocess
import sys

PATTERNS = (".env", ".env.local", ".env.production", "credentials.json")


def tracked_files() -> list[str]:
    out = subprocess.check_output(["git", "ls-files"], text=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


def main() -> int:
    hits = [
        path
        for path in tracked_files()
        if path == ".env" or path.endswith("/.env") or any(path.endswith(p) for p in PATTERNS)
    ]
    if hits:
        print("tracked secret-like paths:")
        for path in hits:
            print(f"  {path}")
        print("gitignore is not a lock. untrack, rotate, then rerun.")
        return 1
    print("no tracked secret-like paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run that in CI. If it fails, the agent does not “fix gitignore” and call the job green. A person rotates the key.

![Three stations: gitignore hint, still tracked, then push protection](/img/five-refusals-this-week-2.png)

## 3. An agent PR has a named merge owner

CODEOWNERS is useful. It is not the merge owner.

GitHub requests reviews from code owners when a pull request touches their paths. Owners need write access. Draft PRs do not auto-request them; marking ready for review does. If required reviews are on, an admin can also require a code-owner approval. When several owners match one pattern, **any** of them is enough. [Source: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners]

That last sentence is why I still write a human name on the ticket. `@team-backend` is a group. The merge click is one person who will revert the migration at 02:00.

I do not give the coding agent merge rights. I do not treat “CODEOWNERS requested review” as “someone owns merge.” I do not let the author agent click merge because the checks are green.

Protect `main`. Require a pull request. Require a review from a person who is not the agent bot. Put the merge owner in the template.

```text {linenos=inline}
# .github/CODEOWNERS
# Last matching pattern wins. Any listed owner can satisfy
# "require review from code owners" — that is not a merge owner.

*                       @desk-reviewers
/routes/                @shinjae
/database/migrations/   @shinjae
/.github/CODEOWNERS     @shinjae
```

Then the ticket still has:

```markdown
- Merge owner: @shinjae
- Agent merge: forbidden
- Green checks: not a merge
```

If you cannot name the merge owner, the pull request stays open. I would rather miss a Friday ship than merge an agent diff with an empty owner field.

## 4. Abort is not stop

Abort is a keystroke. Stop is a decision with an owner.

I have watched sessions die in three different ways that all look like “we stopped”:

- The human hit escape. The agent still had a retry queued.
- The tool returned empty output and the harness printed success.
- The cron exited 0 and nobody checked the artifact.

A green exit is not a finished job. I wrote that for long-running agent work in [A Green Cron Exit Is Not a Finished Job](/blog/a-green-cron-exit-is-not-a-finished-job/) and in the production framing of [Long-Running AI Agents — From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/). The same rule sits on a five-minute coding-agent abort.

I refuse “we aborted, so we are done.”

Abort requires three fields:

1. Retry owner (a person, not “the agent will resume”)
2. Next attempt time, or an explicit **do not retry**
3. Artifact: log path, last tool name, last file touched

If those three are missing, the abort is a pause with a leak. The next session starts in the same directory, sees a half-written migration, and continues.

```python {linenos=inline,hl_lines=["20-27"]}
#!/usr/bin/env python3
"""Write an abort record. Missing owner fails the job."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = ("retry_owner", "next_action", "last_artifact")


def main() -> int:
    record = {
        "aborted_at": datetime.now(timezone.utc).isoformat(),
        "retry_owner": os.environ.get("RETRY_OWNER", "").strip(),
        "next_action": os.environ.get("NEXT_ACTION", "").strip(),  # retry|hold|close
        "last_artifact": os.environ.get("LAST_ARTIFACT", "").strip(),
        "ticket": os.environ.get("TICKET", "").strip(),
    }
    missing = [key for key in REQUIRED if not record[key]]
    if missing:
        print("abort is not stop. missing:", ", ".join(missing))
        return 1
    if record["next_action"] not in {"retry", "hold", "close"}:
        print("next_action must be retry, hold, or close")
        return 1
    path = Path("artifacts/abort-record.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The file is the stop. Chat is not the stop. See also the hub on [AI agent operations](/ai-agent-operations/) for the same artifact habit on longer jobs.

![Abort is a keystroke; stop has retry owner, next time, and artifact](/img/five-refusals-this-week-3.png)

## 5. Cheap code still needs a human review

Writing code got cheap. Reviewing it did not.

I refuse Full-Auto on a pull request I did not read. I refuse “the author model reviewed itself.” Same model on both sides is a rewrite with extra steps.

A junior can still do this on Monday:

- Read the diff, not the agent summary
- Run the test the PR claims, on your machine
- Check migrations, `.env` samples, and auth paths by hand
- Leave one review comment that a person wrote

If the team cannot review the volume, cut the volume. Do not add a second agent to “review faster.” That is how you get a pile of confident PRs and zero merge owners.

{{< note type="warning" title="Full-Auto is not a reviewer" >}}
Full-Auto is a session mode. A reviewer is a named human who can revert the change. Do not merge unread agent PRs because the queue is long.
{{< /note >}}

This is the rule that still bites. The other four are gates. This one is the queue. Cheap generation without cheap review fills GitHub with work that looks done.

## Put the five names on one ticket

I keep one block at the bottom of every agent ticket. Copy it. Do not invent a sixth tool.

```markdown
## Desk names (required before first prompt)

1. Author model: ________ (human-pinned)
2. Review model: ________ (not the author, or human only)
3. Merge owner: @________
4. Retry owner: @________
5. Human reviewer: @________ (reads the diff)

Forbidden: Auto as a model name. Agent merge. Abort without a record.
Secret check: `git ls-files | grep -E '(^|/)\.env'` must be empty.
```

![Ticket fields: author model, review model, merge owner, retry owner, human reviewer](/img/five-refusals-this-week-4.png)

If any line is blank, I do not start the agent. If the agent already started, I stop, fill the lines, then continue. That is slower than Auto. It is how the Laravel app still boots after the weekend.

For the longer production shape — heartbeats, ownership, and what “done” means when a job runs for hours — start at [Long-Running AI Agents — From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/) and the [developer tools](/developer-tools/) hub.

## What you should do Monday morning

1. Paste the five-name block into your pull request template. Require author model, merge owner, and human reviewer before the agent opens a PR.
2. Run `git ls-files` and fail CI if `.env` is tracked. Ignore is not a lock. Rotate anything that was committed.
3. Turn on GitHub push protection where you have Secret Protection. Know that user-level protection on github.com covers public repos by default, not every private repo.
4. Set merge owner to a person. Keep CODEOWNERS. Do not treat “any code owner approved” as that person.
5. On abort, write `artifacts/abort-record.json` with retry owner, next action, and last artifact. No record means you did not stop.
6. Review one unread agent PR yourself today. If you cannot finish it, do not open another agent session.

## Further reading

{{< source href="https://docs.github.com/en/copilot/concepts/models/auto-model-selection" label="GitHub Docs: Copilot auto model selection" >}}

{{< source href="https://docs.github.com/en/get-started/git-basics/ignoring-files" label="GitHub Docs: Ignoring files" >}}

{{< source href="https://docs.github.com/en/code-security/concepts/secret-security/push-protection" label="GitHub Docs: Push protection" >}}

{{< source href="https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners" label="GitHub Docs: About code owners" >}}
