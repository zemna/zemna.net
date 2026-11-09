---
title: "A Red Fork PR on Nov 9 or 16 May Be a GitHub Rehearsal, Not Your Bug"
date: 2026-11-09T06:00:00+07:00
draft: false
slug: "red-fork-pr-github-rehearsal-pull-request-target"
description: "GitHub will block pull_request_target on public repos from Dec 2, with practice blocks on Nov 9 and Nov 16. Here is how to tell a rehearsal from a real bug, and what to decide per workflow."
topics: ["devops"]
tags: ["github-actions", "pull-request-target", "github", "ci-cd", "fork-pull-requests", "security", "agent-ops"]
cover: /covers/red-fork-pr-github-rehearsal-pull-request-target.png
seo:
  primaryQuery: "pull_request_target blocked by default"
  secondaryQueries:
    - "github actions pull_request_target brownout november 9"
    - "pull_request_target failed run error annotation fork pull request"
    - "how to allow pull_request_target actions event policy"
---

At 23:00 Jakarta time tonight, some fork pull requests on public GitHub repositories will get a red X from a workflow that nobody changed.

If you maintain a public repo, the day will look like this. A contributor opens a pull request from their fork. A job you wrote last year fails in a few seconds. Your first guess is that something broke, so you open the file, read it twice, and find nothing wrong. Nothing is wrong. GitHub is rehearsing a rule it plans to switch on for good on December 2, 2026: the `pull_request_target` trigger is blocked by default on public repositories, unless a policy says it is allowed.

If you have never typed that word, here is all you need for now. A trigger is the line in a workflow file that says when the workflow runs. `pull_request_target` is the trigger that fires when someone opens a pull request, and it runs **your** version of the workflow, from **your** default branch, with **your** secrets in reach. People use it for small chores like adding a label to a fork's pull request, because the safer trigger cannot write to your repo from a fork.

The question is not whether GitHub's new default is right. The question is whether, tonight, you can tell a rehearsal red X from a real bug in under a minute, and whether you already know which of your workflows you will keep, change or switch off.

## What GitHub will do, in plain times

I read the GitHub changelog entry from November 2 and the two docs pages behind it this morning. GitHub calls the two practice windows brownouts; I call them rehearsals. Here is the schedule, with the times written for people who do not live in UTC.

| | First rehearsal | Second rehearsal | The real rule |
|---|---|---|---|
| Date | Nov 9, 2026 | Nov 16, 2026 | Dec 2, 2026 |
| UTC | 16:00–18:00 | 16:00–18:00 | from the start of the day |
| Jakarta (UTC+7) | 23:00–01:00 | 23:00–01:00 | — |
| San Francisco (UTC−8) | 08:00–10:00 | 08:00–10:00 | — |
| What you see | A failed run with an error annotation. The workflow does not execute. | Same | Same, with no window and no end |

The Dec 2 date used to be Nov 2. GitHub moved it. After each rehearsal window the default rule goes back to what the docs call evaluate mode, where workflows run again and you get warnings instead of failures.

Who is affected, by the changelog's own words: public repositories on GitHub Free, GitHub Team and GitHub Enterprise Cloud. Not GitHub Enterprise Server. Private and internal repositories are not affected.

![Timeline of the pull_request_target change: first rehearsal Nov 9 16:00 to 18:00 UTC, second rehearsal Nov 16 same hours, real enforcement Dec 2, with evaluate mode between the windows](/img/red-fork-pr-github-rehearsal-pull-request-target-1.png)

One more line from the docs matters if your repo is old. The default policy "does not replace an applicable event policy that you have already configured." So if someone on your team already wrote an Actions event policy that mentions `pull_request_target`, GitHub's default does not override it. If nobody did, the default is what applies to you.

The two pages are not worded identically. The changelog says all public repositories, unless a policy explicitly allows it. The docs say that on December 2 GitHub will enforce the default for affected repositories that were using the default policy before general availability. I plan around the stricter sentence, and so should you.

## Two triggers that look the same and behave very differently

A red X tonight only makes sense if you know what the trigger does. The docs explain it in a way a first-year developer can follow, so I will keep close to it.

| | `pull_request` | `pull_request_target` |
|---|---|---|
| Which workflow file runs | The one from the pull request's merge commit, so the fork's version | The one from your default branch |
| What `actions/checkout` gets by default | The pull request's merge commit | Your default branch |
| `GITHUB_TOKEN` | Read-only for fork pull requests | Your repo's token, which can write |
| Secrets | Withheld from fork pull requests | Available |

Read the first row again. With `pull_request`, a stranger's file runs, so GitHub takes the keys away. With `pull_request_target`, only your file runs, so GitHub hands the keys over. Both are safe as designed. The docs say it directly: by default no code from the fork is executed in `pull_request_target`.

The danger is a step that undoes that default. The docs call the result a "pwn request". Here is the example they give, marked insecure:

```yaml
# INSECURE. Provided as an example only (from the GitHub docs).
on:
  pull_request_target:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - name: Test
        run: make test
```

The checkout step alone is not the problem. The `make test` step is. It runs a `Makefile` that came from the fork, and it runs with your token and your secrets. The docs list the same shape in other costumes: setting `repository:` to the fork, using the `refs/pull/<number>/merge` ref, or fetching the pull request with `git fetch` or `gh pr checkout` and then running it. They also point out that this is not unique to this trigger. An `issue_comment` or `workflow_run` workflow that fetches and runs fork code has the same flaw.

That is why GitHub is changing the default. It is not saying every use is wrong. It is saying the safe default for a public repo is "blocked until a person says allowed".

![Comparison of pull_request and pull_request_target: which workflow file runs, what token it gets, whether secrets are available, and where the danger is a step that runs fork code](/img/red-fork-pr-github-rehearsal-pull-request-target-2.png)

## Step one: list which workflows will be hit

Before the first window opens, you want a list, not a feeling. GitHub's own page for this is **Policy insights**. The docs say that under Settings, then Actions, then Policies, there is a Policy insights page that shows runs that were blocked or would have been blocked. The changelog says to use it before the first rehearsal. Start there.

Policy insights tells you what ran. It does not tell you what is in your files. So I wrote a small scan for the other half: which workflow files mention the trigger, and do any of them have a shape the docs call risky. It is a plain text scan with no YAML parser, which means it can say "read this file" but never "this file is safe". It fails closed: a folder it cannot read exits with code 3 instead of looking clean.

```python {linenos=inline}
#!/usr/bin/env python3
"""find_prt.py REPO_DIR [REPO_DIR ...]

Exit codes: 0 = no workflow mentions pull_request_target
            1 = mentioned, no risky shape found
            2 = mentioned and at least one risky shape found
            3 = a repo folder or workflow file could not be read (fail closed)
"""
import re
import sys
from pathlib import Path

MENTION = re.compile(r"\bpull_request_target\b")
RISKY = {
    "checks out the PR head": re.compile(r"github\.event\.pull_request\.head\.(sha|ref)\b"),
    "points checkout at the fork": re.compile(r"github\.event\.pull_request\.head\.repo\b"),
    "uses the PR merge ref": re.compile(r"refs/pull/"),
    "turns off the checkout guard": re.compile(r"allow-unsafe-pr-checkout"),
    "fetches PR code by hand": re.compile(r"\bgh\s+pr\s+checkout\b|\bgit\s+fetch\b.*\bpull\b"),
}


def scan(repo: Path) -> int:
    if not repo.is_dir():
        print(f"UNREADABLE {repo}: not a folder")
        return 3
    folder = repo / ".github" / "workflows"
    if not folder.is_dir():
        print(f"NONE       {repo.name}: no .github/workflows folder")
        return 0
    status = 0
    for path in sorted(list(folder.glob("*.yml")) + list(folder.glob("*.yaml"))):
        try:
            lines = path.read_text().splitlines()
        except (OSError, UnicodeDecodeError) as err:
            print(f"UNREADABLE {path.relative_to(repo)}: {err}")
            status = max(status, 3)
            continue
        code = [(n, line.split("#", 1)[0]) for n, line in enumerate(lines, 1)]
        if not any(MENTION.search(text) for _, text in code):
            continue
        status = max(status, 1)
        print(f"USES       {path.relative_to(repo)}")
        for n, text in code:
            for reason, pattern in RISKY.items():
                if pattern.search(text):
                    print(f"  RISKY    line {n}: {reason}")
                    status = max(status, 2)
    if status == 0:
        print(f"NONE       {repo.name}: no workflow mentions pull_request_target")
    return status


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: find_prt.py REPO_DIR [REPO_DIR ...]")
    sys.exit(max(scan(Path(arg)) for arg in sys.argv[1:]))
```

I ran it on fixture repos I built for this post, including a labeler workflow, the docs' insecure example, a repo whose only mention is in a comment, and a folder that holds a file with broken bytes.

| Fixture | What it printed | Exit code |
|---|---|---|
| Labeler workflow, no checkout | `USES .github/workflows/label.yml` | 1 |
| The docs' insecure example | `USES ...test.yml` then `RISKY line 10: checks out the PR head` | 2 |
| Mention only inside a `#` comment | `NONE quiet: no workflow mentions pull_request_target` | 0 |
| Repo with no workflows folder | `NONE ... no .github/workflows folder` | 0 |
| A workflow file with bad bytes | `UNREADABLE ... 'utf-8' codec can't decode byte 0xff` | 3 |
| A path that does not exist | `UNREADABLE ... not a folder` | 3 |

A mention inside an `if:` condition counts as a hit too. That is on purpose. A false hit costs you two minutes of reading. A missed hit costs you a red X you do not understand.

## Step two: give each workflow one of three answers

For every file on your list, you are allowed exactly three answers. The docs lay them out as options for each affected workflow, and the changelog gives the same two policy choices.

![Decision flow for one workflow: can it use pull_request, then switch; does it need pull_request_target and never run fork code, then allow it by file; otherwise leave it blocked](/img/red-fork-pr-github-rehearsal-pull-request-target-3.png)

**1. Switch to `pull_request`.** If the job only needs to build and test the fork's code, it does not need your secrets, so it does not need this trigger. The docs ask this first: "Can you use `pull_request` instead?" For most test and lint jobs the answer is yes, and the red X goes away for good.

**2. Allow it, narrowly.** If the job really needs your token, such as a labeler or a triage bot that writes to the pull request, you can allow the trigger in an Actions event policy. The changelog says to use workflow file targeting to allow specific workflows, not the whole repo. That keeps the allow list as short as the list of jobs that need it.

Here is the shape of a job that earns that allow. It never checks out the fork, and its permissions are written down:

```yaml
# .github/workflows/label.yml - allowed by name in the event policy
name: label
on:
  pull_request_target:
permissions:
  contents: read
  pull-requests: write
  issues: write
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v7
```

The permission block follows the `actions/labeler` README. There is no `actions/checkout` with a `ref`, and no step that builds or runs the pull request's files. The docs' warning applies in full: allow it only if the checked-out code is "only ever inspected as data and never executed".

**3. Leave it blocked.** If nobody can say why the workflow uses the trigger, that is your answer. Leaving the default in place is a valid choice in both the changelog and the docs. A job that stops running and a secret that stays private is a better trade than a job nobody owns.

Two warnings from me. Do not write a bypass for the fork's code. If a workflow needs secrets **and** needs to run the fork's build, the right fix is to split it, with a safe job that builds the fork's code with no secrets and a separate trusted job that treats the result as untrusted data. The docs say a `workflow_run` workflow should treat artifacts from other workflows as untrusted data, because they can come from a fork. And the docs' escape hatch, `allow-unsafe-pr-checkout: true` on `actions/checkout`, is named to be easy to spot in a code review. Keep it that way. If you ever see it in a diff, stop and ask why.

## Step three: read the red X tonight

Now the part you will actually meet at 23:00. A contributor's pull request shows a failed check. Three questions settle it, in this order.

1. **Is the event `pull_request_target`?** If the failed workflow runs on `pull_request`, `push` or anything else, this is not the rehearsal. Look for the usual causes.
2. **Is the time inside 16:00–18:00 UTC on Nov 9 or Nov 16?** The changelog says blocked attempts in that window create failed runs. Outside it, the same workflow should run again with warnings.
3. **Does the run's annotation say it was blocked?** The changelog says blocked runs carry an error annotation. Open the run and read it. I have not seen the exact words of that message, so I will not quote one. Read yours.

A time match is a hint. Only the annotation is proof. To save you from eyeballing timestamps, here is a second small script. It reads the output of `gh run list` and says which failed `pull_request_target` runs sit inside a published window.

```bash
gh run list --event pull_request_target --status failure --limit 50 \
  --json createdAt,event,conclusion,workflowName,displayTitle,url > runs.json
python3 brownout_check.py runs.json
```

```python {linenos=inline}
#!/usr/bin/env python3
"""brownout_check.py RUNS.json - which failed runs sit inside a brownout window.

Exit codes: 0 = no failed pull_request_target runs
            1 = every failed run sits inside a brownout window
            2 = at least one failed run is OUTSIDE the windows (look at it)
            3 = file missing or not the JSON we expected (fail closed)
"""
import json
import sys
from datetime import datetime
from pathlib import Path

WINDOWS = [
    ("2026-11-09T16:00:00Z", "2026-11-09T18:00:00Z"),
    ("2026-11-16T16:00:00Z", "2026-11-16T18:00:00Z"),
]


def when(stamp: str) -> datetime:
    return datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def inside(stamp: str) -> bool:
    moment = when(stamp)
    return any(when(a) <= moment < when(b) for a, b in WINDOWS)


def main(path: str) -> int:
    try:
        runs = json.loads(Path(path).read_text())
        failed = [r for r in runs if r["event"] == "pull_request_target" and r["conclusion"] == "failure"]
        verdicts = [(r, inside(r["createdAt"])) for r in failed]
    except (OSError, ValueError, KeyError, TypeError) as err:
        print(f"UNREADABLE {path}: {err!r}")
        return 3
    for run, hit in verdicts:
        label = "WINDOW " if hit else "OUTSIDE"
        print(f"{label} {run['createdAt']}  {run['workflowName']}  {run['url']}")
    if not verdicts:
        print("NONE    no failed pull_request_target runs in this file")
        return 0
    return 1 if all(hit for _, hit in verdicts) else 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: brownout_check.py RUNS.json")
    sys.exit(main(sys.argv[1]))
```

I ran it on fixture JSON in the shape of those `--json` fields, not on real GitHub output.

| Fixture | What it printed | Exit code |
|---|---|---|
| Two failed runs at 16:12 and 17:59 UTC | two `WINDOW` lines | 1 |
| Same two, plus one at 18:00:00 UTC, plus a failed `push` run | two `WINDOW`, one `OUTSIDE`; the `push` run is ignored | 2 |
| Empty list | `NONE no failed pull_request_target runs` | 0 |
| File that is not JSON, wrong shape, or missing | `UNREADABLE ...` | 3 |

The 18:00:00 row is on purpose. The window is written as 16:00–18:00, and I treat 18:00:00 as outside. If GitHub's edge is a minute different, an `OUTSIDE` line is a reason to open the run, not to panic.

{{< field-note title="Field note" >}}
I read a workflow file the way I read a cron entry on a server I inherited. It runs on its own, it holds credentials, nobody remembers who wrote it, and the last time anyone read it is the day it was written. On the Laravel and Vue projects I look after, the review that matters is rarely the application code. It is the folder of automation around the code, because that folder has keys. A change like this one is annoying for exactly one afternoon. After that you own a list of every job that holds a key, and a name next to each. I would pay a red X for that list.
{{< /field-note >}}

## What this connects to

This is the same kind of problem I wrote about in [Your Overnight Agent Job Has a Login With an End Date](/blog/agent-job-login-has-an-end-date/): a rule about the environment changes on a date, the tool keeps looking fine, and the first sign is a failure that blames the wrong thing. It also touches the point in [Two Agents, One Database](/blog/herd-workspaces-share-the-parent-database/): a default that someone else chose is still your risk until you have read it.

It matters more if coding agents open pull requests for you or against you. An agent that edits a `Makefile` or a test script looks harmless in a diff. The docs' warning is about what runs with your token after the diff is merged into the job. [Long-Running AI Agents: From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/) covers the same habit from the agent side: name the owner of every thing that holds a credential. More of these notes live on [AI Agent Operations](/ai-agent-operations/) and [Developer Tools](/developer-tools/), and [Start Here](/start-here/) lists the order I would read them.

## What I did and did not verify

I read the GitHub changelog entry "pull_request_target blocked by default December 2", the docs page "Securely using pull_request_target", the docs page "Governing execution of GitHub Actions workflows", the `actions/labeler` README and the `gh run list` manual on 2026-11-09. Every date, window, scope and option in this post comes from those pages.

I ran both scripts myself, on fixture folders and fixture JSON. I did not run `gh` (it is not installed on my host), I did not look at a real Policy insights page, and I have not seen a real brownout failure. So I do not know the exact words of the error annotation, and I did not test a real event policy. The labeler example follows its README and was not run on GitHub. The docs and changelog also differ slightly on which repos are enforced on Dec 2, as noted above, and they can change again.

## What you should do Monday morning

You have until 16:00 UTC, which is 23:00 in Jakarta.

1. **Open Settings, then Actions, then Policies** on each public repo you maintain. Check whether an event policy already exists. If it does, the default does not override it.
2. **Open Policy insights** on the same page and list every workflow it says would be blocked.
3. **Run `find_prt.py` on a local clone** of each repo. Any `RISKY` line gets read by a human today, before anything else.
4. **Give every workflow one of the three answers**: switch to `pull_request`, allow by file name, or leave blocked. Put one named owner next to each.
5. **Tell your reviewers and regular contributors** that red X marks on fork pull requests between 23:00 and 01:00 Jakarta time, 16:00–18:00 UTC, may be the rehearsal. One sentence in the pinned issue or the contributing page is enough.
6. **Read the annotation before you debug.** If it says blocked, close the tab.
7. **Re-run the failed checks after the window** on any pull request that is still open. The changelog says the rule returns to evaluate mode afterward and workflows run with warnings.
8. **Put Nov 16 in your calendar.** The second window is the same two hours.
9. **If an agent opens fork pull requests for you**, check that none of its workflows run its own checkout with the pull request head.

## Further reading

- {{< source href="https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2/" label="GitHub changelog: pull_request_target blocked by default December 2" >}}
- {{< source href="https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target" label="GitHub Docs: Securely using pull_request_target" >}}
- {{< source href="https://docs.github.com/en/actions/how-tos/administer/control-workflow-execution" label="GitHub Docs: Governing execution of GitHub Actions workflows" >}}
- {{< source href="https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/" label="GitHub Security Lab: Preventing pwn requests" >}}
- {{< source href="https://cli.github.com/manual/gh_run_list" label="GitHub CLI manual: gh run list" >}}
