---
title: "A 2,500+ Actions Count Is Not an Exact Run Inventory"
date: 2026-09-29T07:00:00+07:00
draft: false
slug: "a-2500-plus-actions-count-is-not-an-exact-run-inventory"
description: "A GitHub Actions badge that says 2,500+ is a capped count, not a run inventory. Print the cap, the 1,000-item page, a date-range filter, and the named Actions owner before you file missing runs."
topics: ["devops"]
tags: ["github-actions", "workflow-runs", "ci", "pagination", "coding-agents", "change-control"]
cover: /covers/a-2500-plus-actions-count-is-not-an-exact-run-inventory.png
seo:
  primaryQuery: "GitHub Actions 2500+ is not an exact run count"
  secondaryQueries:
    - "GitHub Actions API total_count 1000 pagination cap"
    - "narrow workflow run query with created date range"
    - "named owner for GitHub Actions run inventory"
---

Standup hears “we have 2,500 runs.” Someone pasted the Actions tab. The coding agent pasted `total_count` from `GET /repos/{owner}/{repo}/actions/runs`. The junior files missing-runs: “the rest of the history vanished.”

I stop the run there. A 2,500+ Actions count is not an exact run inventory. Official GitHub changelog for 25 September 2026 is blunt: queries for workflow runs in the Actions API and UI still paginate up to 1,000 items, and if the number of found records exceeds 2,500, GitHub reports “2,500+” instead of an exact number. Larger queries often timed out and returned however many records had been counted before the timeout. The cap is the honest number. The exact inventory is a different ticket. [Source: https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/]

I already refused to treat a timed-out Laravel job as a killed worker pool in [A Timed-Out Job Is Not a Killed Worker](/blog/a-timed-out-job-is-not-a-killed-worker/). I already refused to treat `ubuntu-latest` as a runner image I already tested in [Ubuntu-latest Is Not a Runner Image You Already Tested](/blog/ubuntu-latest-is-not-a-tested-runner-image/). I already refused to treat an auto-started Codex background server as compatible settings in [An Auto-Started Codex Background Server Is Not Compatible Settings](/blog/auto-start-is-not-compatible-settings/). This post is the same desk rule for Actions history. Print the cap. Print the page. Name who owns the workflow-run query.

The question is not whether a dashboard demos a big number. The question is whether the named owner can tell a capped count from a missing run before paging CI.

<!--more-->

![Three columns: 2,500+ capped count, 1,000 item page, named Actions owner](/img/a-2500-plus-actions-count-is-not-an-exact-run-inventory-1.png)

## The ticket that looks like missing history

Juniors treat `2,500+` the way they treat a database `COUNT(*)`. The badge is large. The list stops. They file “GitHub deleted our runs.”

Two jobs collide on that screen.

1. **Stop a query that used to lie with a partial count.** GitHub’s own reason: queries that retrieve more than 2,500 records frequently timeout and return the number of records found before the timeout rather than the true count. The new badge is less precise and more accurate. [Source: https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/]
2. **Keep listing the page you can actually fetch.** The same note says paginated results still go up to 1,000 items. Official REST docs for list-workflow-runs already said that endpoint returns up to 1,000 results for each search when you use `actor`, `branch`, `check_suite_id`, `created`, `event`, `head_sha`, or `status`. [Source: https://docs.github.com/en/rest/actions/workflow-runs]

If you only screenshot “2,500+,” you will file missing history. You will not file the query.

{{< note type="warning" title="Do not file missing runs on a 2,500+ badge" >}}
If a coding agent or a junior says the run history vanished, print the query filters, the 2,500+ cap, the 1,000-item page, a `created` date range, and one human name on Actions before you page GitHub support. A capped count is not a deleted inventory.
{{< /note >}}

I do not invent a fake overnight wipe. I use the public contract. The changelog page is the ticket, not a version pin in the title.

## Three tickets, one owner

Laravel plus Vue work on this desk still sits next to GitHub Actions: a workflow under `.github/workflows/`, a coding agent that treats `total_count` as `COUNT(*)`, a junior who writes a scraper because the badge stopped climbing. Mixing the cap, the page, and the date window into one “Actions is broken” thread hides the owner.

| Ticket | What it means | What you do | Owner |
| --- | --- | --- | --- |
| UI or API reports 2,500+ | Found records exceeded 2,500 | Do not call it 2,500 exact runs | Named human who owns the workflow-run query |
| List stops at 1,000 items | Search pagination cap on that query | Page inside the cap. Do not scrape past it | Same named human |
| You need a specific week | Exact inventory for that window | Add `created` (date range). Narrow workflow, event, status, branch, or actor | Same named human |

Do not paste one badge and call the history complete. If the screen says `2,500+`, you are on a cap ticket. If `workflow_runs.length` is 1,000 and the next page is empty, you are on a page ticket. If you need last Tuesday’s failed deploy, you are on a date-range ticket.

{{< details summary="Dates and caps are evidence, not the hook" >}}
GitHub published the query-results note on 25 September 2026. The change is rolling out on github.com and GitHub Enterprise Cloud. Filters named in that note: workflow, event, status, branch, or actor. Pagination named in that note: up to 1,000 items. Cap named in that note: report “2,500+” when found records exceed 2,500. REST docs still list `per_page` max 100 and `page` for the list-runs endpoint. Print those strings on the ticket. Do not put `2,500+` in a social title as a version hook. Do not treat Enterprise Server as covered unless a later note says so. [Source: https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/] [Source: https://docs.github.com/en/rest/actions/workflow-runs]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: `phpunit.xml` next to `vite.config.js`, a workflow that runs on every push, and a coding agent that files “CI history is gone” because the Actions tab now says 2,500+. I treat that query as a named owner’s artifact, the same way I treat a queue timeout. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “which run window is allowed to be counted.” A coding agent does not get to scrape past the cap so standup looks complete. I already wrote the sibling rule for a timed-out job that is not a killed worker, and for `ubuntu-latest` that is not a tested image. This is the sibling for a capped count that is not an inventory.
{{< /field-note >}}

![Three tickets: 2,500+ cap, 1,000 page, date range](/img/a-2500-plus-actions-count-is-not-an-exact-run-inventory-2.png)

## What the list endpoint actually returns

I do not invent a fake JSON field. I use the public contract.

Official REST: `GET /repos/{owner}/{repo}/actions/runs` lists workflow runs for a repository. Anyone with read access can use it. The example response includes `total_count` as a number next to a `workflow_runs` array. Query parameters include `actor`, `branch`, `event`, `status`, `per_page` (max 100), `page`, and `created` for a date-time range. [Source: https://docs.github.com/en/rest/actions/workflow-runs]

Official REST also states the 1,000-result search cap when those filter parameters are in use. That sentence was already in the docs before this week’s badge. Octokit maintainers confirmed the same hard cap in a public discussion: paging past entry 1,000 returns empty lists even when an earlier `total_count` looked higher. [Source: https://docs.github.com/en/rest/actions/workflow-runs] [Source: https://github.com/orgs/octokit/discussions/81]

This week’s changelog adds the count behavior. Do not mix the two.

1. **Page of runs.** Up to 1,000 items for a filtered search. `per_page` still max 100, so ten pages is the search window, not infinity. [Source: https://docs.github.com/en/rest/actions/workflow-runs] [Source: https://docs.github.com/rest/using-the-rest-api/using-pagination-in-the-rest-api]
2. **Reported total.** If found records exceed 2,500, GitHub reports “2,500+” instead of attempting the exact number. That is the new honesty. [Source: https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/]

Copy the docs example as a probe, not as a bypass recipe.

```bash
# Probe the list endpoint. Do not page past the documented search cap.
export ACTIONS_RUNS_OWNER="shinjae"
export GH_REPO="OWNER/REPO"
export CREATED_RANGE="2026-09-22T00:00:00+07:00..2026-09-29T00:00:00+07:00"

gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  "/repos/${GH_REPO}/actions/runs?per_page=100&page=1&created=${CREATED_RANGE}" \
  --jq '{owner: env.ACTIONS_RUNS_OWNER, total_count, run_len: (.workflow_runs|length), first_id: .workflow_runs[0].id}'
```

[Source: https://docs.github.com/en/rest/actions/workflow-runs]

`created` is the filter GitHub asked you to add when a script used to pull more than 2,500 matching runs from one query. Narrow the window. Do not write a second loop that walks `page=11` hoping the 1,000 cap moved. [Source: https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/]

## Print the cap before you file missing runs

A coding agent will still print `total_count` and stop. That is how the wrong ticket gets filed.

Treat three strings as different fields.

1. **Exact integer under 2,500.** The query is small enough that GitHub still attempts an exact count. Still not an inventory of the whole repo forever. It is the count for that filter.
2. **Badge or report of 2,500+.** Found records exceeded 2,500. Stop calling it 2,500. Stop calling it 3,000. File “query hit the cap.”
3. **Array length 1,000.** You hit the search page cap. The next page is not a secret inventory. Narrow `created`, `branch`, `event`, or `status`.

I keep a small probe in the app that actually ships. It does not scrape. It refuses to treat a cap as a total.

```python
#!/usr/bin/env python3
"""Probe GitHub Actions run queries. A cap is not an inventory."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

CAP_TOTAL = 2500
CAP_PAGE = 1000


def main() -> int:
    owner = os.environ.get("ACTIONS_RUNS_OWNER", "").strip()
    payload = Path(os.environ.get("ACTIONS_RUNS_JSON", "actions-runs.json"))
    if not owner:
        print("VERDICT=NO_OWNER")
        return 2
    if not payload.is_file():
        print("VERDICT=NO_PAYLOAD")
        return 2

    data = json.loads(payload.read_text(encoding="utf-8"))
    raw_total = data.get("total_count")
    runs = data.get("workflow_runs") or []
    run_len = len(runs)

    total_text = str(raw_total).strip()
    print(f"OWNER={owner}")
    print(f"TOTAL_FIELD={total_text}")
    print(f"RUN_LEN={run_len}")

    if total_text in {"2500+", "2,500+", "2500"} and run_len >= min(CAP_PAGE, run_len):
        if total_text in {"2500+", "2,500+"} or (
            isinstance(raw_total, int) and raw_total >= CAP_TOTAL
        ):
            print("VERDICT=CAPPED_COUNT_NOT_INVENTORY")
            return 0

    if run_len >= CAP_PAGE:
        print("VERDICT=PAGE_CAP_NOT_INVENTORY")
        return 0

    if isinstance(raw_total, int) and raw_total < CAP_TOTAL:
        print("VERDICT=FILTERED_COUNT_UNDER_CAP")
        return 0

    print("VERDICT=INSUFFICIENT_QUERY")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

Save one API page to `actions-runs.json`. Run the probe in the repo that ships.

```bash
export ACTIONS_RUNS_OWNER="shinjae"
export ACTIONS_RUNS_JSON="actions-runs.json"
python3 scripts/probe_actions_run_cap.py
```

`VERDICT=CAPPED_COUNT_NOT_INVENTORY` means you do not have a wipe. Then open the Actions tab. Copy the filters. Copy the badge. Put those four lines on the ticket: owner, badge, `run_len`, verdict.

A second probe is the date window itself. Print `created`, the workflow file name, `event`, `status`, and `branch`. If the unfiltered query is 2,500+ and last Tuesday’s window is 37, you are looking at the changelog, not a deletion.

![Probe checklist: owner, badge 2,500+, run_len, verdict](/img/a-2500-plus-actions-count-is-not-an-exact-run-inventory-3.png)

## What a date range is for

GitHub’s own remediation is one sentence: if your integrations or scripts rely on retrieving more than 2,500 matching workflow runs from a single query, narrow your filters, for example by adding a date range, to retrieve the specific runs you need. [Source: https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/]

That is the Monday move. It is not a scrape.

Official REST `created` uses GitHub’s date-range search syntax. Put a start and an end. Keep the window small enough that found records stay under the cap you care about for that ticket. [Source: https://docs.github.com/en/rest/actions/workflow-runs]

```yaml
# .github/workflows/ci.yml — evidence only. Do not treat this file as a run inventory.
name: CI
on:
  push:
    branches: [main]
  pull_request:
jobs:
  phpunit:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - name: Run PHPUnit
        run: php artisan test
```

The workflow file tells you which job ran. It does not tell you how many historical runs exist. For last week’s failed deploy you still query with `created` and `status=failure`. For “how busy is this repo this year” you accept 2,500+ and you stop.

I do not write a pager that walks until GitHub 404s. Pagination docs say most endpoints cap `per_page` at 100. The Actions search cap is 1,000 results per filtered search. Walking `page=11` after a 1,000 cap is how juniors burn an hour and still file the wrong ticket. [Source: https://docs.github.com/rest/using-the-rest-api/using-pagination-in-the-rest-api] [Source: https://docs.github.com/en/rest/actions/workflow-runs]

{{< note type="danger" title="Do not scrape past the cap" >}}
A second loop after page 10 is not a fix. GitHub asked you to narrow filters. A coding agent that keeps paging is writing a bypass, not an inventory.
{{< /note >}}

## What you must not mix into this ticket

This is not last week’s queue timeout. A job clock that kills one `queue:work` process is a Laravel worker ticket. [A Timed-Out Job Is Not a Killed Worker](/blog/a-timed-out-job-is-not-a-killed-worker/) already owns that field.

This is not the runner-label ticket. `ubuntu-latest` moving later this year is a pin-and-test ticket. [Ubuntu-latest Is Not a Runner Image You Already Tested](/blog/ubuntu-latest-is-not-a-tested-runner-image/) already owns that field.

This is not the Codex auto-start ticket. A background server that is not compatible settings is a change-control ticket. [An Auto-Started Codex Background Server Is Not Compatible Settings](/blog/auto-start-is-not-compatible-settings/) already owns that field.

GSC this week still has no striking-distance query on those URLs. I am not refreshing them. This is a new field: a capped Actions count is not an exact run inventory.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

![Do-not-mix: queue timeout, ubuntu-latest, Actions 2,500+](/img/a-2500-plus-actions-count-is-not-an-exact-run-inventory-4.png)

## What you must not do

Forbidden:

1. File a “run history vanished” ticket without printing the query filters, the 2,500+ cap, the 1,000-item page, a `created` range, and one human name on Actions.
2. Put a GitHub API version, a runner image, or `2,500+` as a version-style hook in the title or the first line beyond the field name this post already uses.
3. Mix this field with a Laravel job timeout, an `ubuntu-latest` migration, or a Codex auto-start settings ticket. Those are other posts.
4. Treat `total_count: 2500` or a `2,500+` badge as `COUNT(*)`.
5. Page past the documented 1,000-result search cap to “finish the inventory.”
6. Write a scraper, a headless clicker, or an export-all script because the badge stopped climbing.
7. Recommend buying Actions minutes, a Copilot plan, or a seat because the count capped.
8. Claim GitHub Enterprise Server already flipped unless a later official note says so. The 25 September note names github.com and GitHub Enterprise Cloud. [Source: https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/]
9. Treat an empty eleventh page as proof of deletion. The search cap already explains an empty page after 1,000. [Source: https://docs.github.com/en/rest/actions/workflow-runs]
10. Ignore GitHub’s own fix: narrow filters, for example a date range, to retrieve the specific runs you need. [Source: https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/]

Allowed:

1. Print the badge, `total_count`, `len(workflow_runs)`, `per_page`, and `page`.
2. Add `created`, `branch`, `event`, `status`, `actor`, or workflow filters until the window fits the ticket.
3. Name one human as `ACTIONS_RUNS_OWNER`.
4. Keep last week’s failed deploy as a dated query, not as a full-repo count.
5. Leave the unfiltered tab at 2,500+ and stop.

A changelog bullet about a more accurate count is not permission to skip the owner.

## What you should do Monday morning

1. Open the repo that actually ships. Export `ACTIONS_RUNS_OWNER` to a human name. Save one `GET /repos/{owner}/{repo}/actions/runs` page to `actions-runs.json`. Run `probe_actions_run_cap.py`. Write the verdict on the ticket next to that name.
2. Open the Actions tab from the incident. Copy the badge. Copy the filters. If it says 2,500+, file “query hit the cap,” not “GitHub deleted runs.”
3. If you need last week’s failed deploy, add `created` for that week and `status=failure`. Do not reuse the unfiltered total. [Source: https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/] [Source: https://docs.github.com/en/rest/actions/workflow-runs]
4. If someone pasted a pager that walks `page=11` after 1,000 items, reject it. Point at the REST search cap. [Source: https://docs.github.com/en/rest/actions/workflow-runs]
5. Confirm coding-agent instructions on this desk name the same owner and forbid “the run history vanished” without the four lines: owner, badge, `run_len`, verdict.
6. Do not refresh the timeout post, the ubuntu-latest post, or the auto-start post. Those URLs already exist. This URL is the unused Actions-count field.

The question is not whether a 2,500+ badge demos well in a screenshot. The question is whether the named owner can still tell a capped count from a missing run after handoff.

## Further reading

{{< source href="https://github.blog/changelog/2026-09-25-changes-to-query-results-in-the-github-actions-api-and-ui/" label="GitHub Changelog — Changes to query results in the GitHub Actions API and UI" >}}

{{< source href="https://docs.github.com/en/rest/actions/workflow-runs" label="GitHub Docs — REST API endpoints for workflow runs" >}}

{{< source href="https://docs.github.com/rest/using-the-rest-api/using-pagination-in-the-rest-api" label="GitHub Docs — Using pagination in the REST API" >}}
