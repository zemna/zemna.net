---
title: "A Moved Self-Hosted Runner Deadline Is Not an All-Clear"
date: 2026-09-30T07:00:00+07:00
draft: false
slug: "a-moved-runner-deadline-is-not-an-all-clear"
description: "A GitHub changelog that moves a self-hosted runner date is not permission to skip the fleet. Print the moved date, the registration floor, the runtime floor, and the named Actions-runner owner before you file all-clear."
topics: ["developer-tools"]
tags: ["github-actions", "self-hosted-runners", "ci", "ghec", "coding-agents", "change-control"]
cover: /covers/a-moved-runner-deadline-is-not-an-all-clear.png
seo:
  primaryQuery: "self-hosted runner enforcement date moved is not all-clear"
  secondaryQueries:
    - "GitHub Actions self-hosted runner registration versus runtime floor"
    - "GET actions runners deprecations version GHEC"
    - "named owner for self-hosted runner upgrade"
---

Standup hears “the date moved.” Someone pasted the GitHub Changelog from 28 September 2026. The coding agent pasted the headline and filed all-clear: “we have extra time; skip the fleet this week.”

I stop the run there. A moved self-hosted runner deadline is not an all-clear. Official GitHub changelog for 28 September 2026 is blunt: the enforcement date for GitHub Actions minimum version requirements for self-hosted runners on GitHub Enterprise Cloud changed. The change ships Monday 28 September 2026. Full enforcement begins Tuesday 29 September 2026. That is instead of the date previously announced. The requirements themselves are unchanged. Today is Wednesday 30 September 2026. The extra day already ended. [Source: https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/]

I already refused to treat a 2,500+ Actions badge as an exact run inventory in [A 2,500+ Actions Count Is Not an Exact Run Inventory](/blog/a-2500-plus-actions-count-is-not-an-exact-run-inventory/). I already refused to treat `ubuntu-latest` as a runner image I already tested in [Ubuntu-latest Is Not a Runner Image You Already Tested](/blog/ubuntu-latest-is-not-a-tested-runner-image/). I already refused to treat a timed-out Laravel job as a killed worker pool in [A Timed-Out Job Is Not a Killed Worker](/blog/a-timed-out-job-is-not-a-killed-worker/). This post is the same desk rule for a moved date. Print the moved date. Print both floors. Name who owns the self-hosted fleet.

The question is not whether a moved date demos well in a screenshot. The question is whether the named owner can tell a moved date from a refused job before paging CI.

<!--more-->

![Three columns: moved date, full enforcement, named owner](/img/a-moved-runner-deadline-is-not-an-all-clear-1.png)

## The ticket that looks like extra time

Juniors treat “date has moved” the way they treat a calendar invite that slipped a week. The headline is kind. The queue is not.

Two jobs collide on that screen.

1. **Stop treating a one-day slip as a freeze.** GitHub’s own 28 September note says the change ships Monday and full enforcement begins Tuesday. The previous GHEC date on the June timeline was 25 September 2026. The new note does not reopen brownouts. It does not pause registration. It does not pause job execution. It moves the remaining full-enforcement day. [Source: https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/] [Source: https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/]
2. **Keep the two floors that did not move.** Runners below the registration minimum cannot register or reregister. Existing runners below the runtime minimum stop running jobs even if they were previously registered. The runtime floor is higher than the registration floor. A pin that only meets registration is not a pin that still picks up work. [Source: https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/] [Source: https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/]

If you only screenshot “date has moved,” you will file extra time. You will not file the fleet.

{{< note type="warning" title="Do not file all-clear on a moved date" >}}
If a coding agent or a junior says the fleet can wait, print the moved date, the full-enforcement day, GitHub Enterprise Cloud versus GitHub Enterprise Server, the registration floor, the runtime floor, and one human name on Actions runners before you close the ticket. A moved date is not an all-clear.
{{< /note >}}

I do not invent a fake overnight wipe. I use the public contract. The changelog page is the ticket, not a version pin in the title.

## Three tickets, one owner

Laravel plus Vue work on this desk still sits next to GitHub Actions: a workflow under `.github/workflows/`, a self-hosted label for PHPUnit, a coding agent that treats a moved date as a pause. Mixing the calendar, the registration floor, and the runtime floor into one “we are fine” thread hides the owner.

| Ticket | What it means | What you do | Owner |
| --- | --- | --- | --- |
| Changelog says the date moved | Calendar slipped one day | Print ship day and full-enforcement day. Do not close the fleet | Named human who owns Actions runners |
| Runner cannot register | Below the registration floor | Stop `./config.sh` on the old image. Recreate from a current binary | Same named human |
| Runner is online and still idle | Below the runtime floor, or auto-update is off and the 30-day window closed | Print `version` from the runners list and the deprecation dates for that version | Same named human |

Do not paste one headline and call the fleet current. If the screen says the date moved, you are on a calendar ticket. If `./config.sh` fails on an old image, you are on a registration ticket. If the runner is online and jobs stay queued, you are on a runtime ticket.

{{< details summary="Dates and floors are evidence, not the hook" >}}
GitHub published the moved-date note on 28 September 2026. Status on that page: Retired. Ship day: Monday 28 September 2026. Full enforcement: Tuesday 29 September 2026. Scope: GitHub Enterprise Cloud. GitHub Enterprise Server is not impacted. GitHub Enterprise Cloud with Data Residency already began enforcement on 31 July 2026. Registration floor named in that note: below `2.329.0` cannot register or reregister. Runtime floor named in that note: a higher version than the registration minimum; existing runners below it stop jobs even if previously registered. June 12 already said `2.329.0` is the registration minimum, not a permanent job-execution pin, and that auto-update off (including ARC `disableUpdate=true`) needs a manual cadence. Print those strings on the ticket. Do not put `2.329.0` in a social title as a version hook. [Source: https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/] [Source: https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/]
{{< /details >}}

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: `phpunit.xml` next to `vite.config.js`, a workflow that `runs-on: self-hosted`, and a coding agent that files “we can skip” because the changelog headline said the date moved. I treat that fleet as a named owner’s artifact, the same way I treat a capped Actions count. The person who owns [/laravel-vue-saas/](/laravel-vue-saas/) on this desk also owns “which runner is allowed to pick up this PHPUnit job.” A coding agent does not get to close the ticket from a headline so standup looks calm. I already wrote the sibling rule for a 2,500+ count that is not an inventory, and for `ubuntu-latest` that is not a tested image. This is the sibling for a moved date that is not an all-clear.
{{< /field-note >}}

![Three tickets: moved date, cannot register, online but idle](/img/a-moved-runner-deadline-is-not-an-all-clear-2.png)

## What the list and deprecation endpoints actually return

I do not invent a fake JSON field. I use the public contract.

Official REST: `GET /orgs/{org}/actions/runners` lists self-hosted runners for an organization. Authenticated users need admin access on the org. The example response includes `name`, `os`, `status`, `busy`, `ephemeral`, `version`, and `labels`. Anyone writing “the runner is fine” without `version` is guessing. [Source: https://docs.github.com/en/rest/actions/self-hosted-runners]

Official REST also documents `GET /orgs/{org}/actions/runners/deprecations/{version}`. GitHub’s 3 September 2026 Actions update says the same path exists at repository, organization, or enterprise level as `GET /actions/runners/deprecations/{version}`. The 3 September note says the response includes `runner_version`, `runtime_deprecates_at`, and `registration_deprecates_at`. The docs example on the self-hosted-runners page shows `runner_version` and `runtime_deprecates_at`. If a key is absent in the JSON you actually saved, print `MISSING`. Do not invent a date. [Source: https://docs.github.com/en/rest/actions/self-hosted-runners] [Source: https://github.blog/changelog/2026-09-03-github-actions-early-september-2026-updates/]

Save the list. Save one deprecation payload. Probe the files. Do not live-loop the API from a coding agent until someone names the owner.

```python {linenos=inline,hl_lines=[18,"24-31"]}
#!/usr/bin/env python3
"""Print moved-date vs floors from saved GitHub JSON. No live token."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REGISTRATION_FLOOR = "2.329.0"


def ver_tuple(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v.split(".") if p.isdigit())


def main() -> int:
    runners_path = Path(sys.argv[1])
    dep_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    payload = json.loads(runners_path.read_text(encoding="utf-8"))
    rows = payload.get("runners") or []
    print(f"RUNNER_COUNT={len(rows)}")
    print(f"REGISTRATION_FLOOR={REGISTRATION_FLOOR}")
    for r in rows:
        name = r.get("name")
        version = str(r.get("version") or "")
        status = r.get("status")
        busy = r.get("busy")
        below_reg = (
            bool(version) and ver_tuple(version) < ver_tuple(REGISTRATION_FLOOR)
        )
        print(
            f"name={name} version={version} status={status} "
            f"busy={busy} below_registration_floor={below_reg}"
        )
    if dep_path and dep_path.exists():
        dep = json.loads(dep_path.read_text(encoding="utf-8"))
        print(f"DEP_RUNNER_VERSION={dep.get('runner_version', 'MISSING')}")
        print(
            "DEP_REGISTRATION="
            f"{dep.get('registration_deprecates_at', 'MISSING')}"
        )
        print(
            f"DEP_RUNTIME={dep.get('runtime_deprecates_at', 'MISSING')}"
        )
    print("VERDICT=moved date is not all-clear")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run it against files the named owner saved, not against a headline:

```bash
python3 probe_runner_floors.py runners.json deprecation.json
```

A green `status: online` next to `below_registration_floor=True` is still a registration ticket the next time that box needs `./config.sh`. A green `status: online` with a `runtime_deprecates_at` already in the past is a runtime ticket even if the box registered last year.

{{< note type="danger" title="Do not skip the deprecation call" >}}
Listing runners without the deprecation payload is a screenshot of names. GitHub added the deprecation API so you can print registration and runtime dates for a version. A coding agent that only prints `version` and files all-clear is skipping the second floor.
{{< /note >}}

![Two cards: list runners with version, deprecation dates](/img/a-moved-runner-deadline-is-not-an-all-clear-3.png)

## Registration floor versus runtime floor

June 12 already split the work. September 28 said the requirements are unchanged.

**Registration.** To configure or reregister, the runner must be on `2.329.0` or later. That is the minimum for the new architecture to recognize the runner. Older binaries fail `./config.sh`. They do not quietly self-upgrade after an old config script. [Source: https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/]

**Runtime.** To keep executing jobs, the runner must install each new runner release within 30 days of publication. Auto-update on meets that rule when the box can reach the update service. Auto-update off, including Actions Runner Controller with `disableUpdate=true`, needs a manual cadence. A runner pinned forever at the registration minimum will, in GitHub’s own words, not pick up jobs. Any release — major, minor, or patch — counts as an available update. A critical security update pauses job queuing until applied. [Source: https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/]

That is why the 28 September note repeats two bullets, not one. Below the registration floor: no register, no reregister. Below the runtime floor: stop running jobs even if previously registered. [Source: https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/]

A workflow file does not prove either floor.

```yaml {linenos=inline,hl_lines=[8,12]}
name: phpunit
on: [push]
jobs:
  phpunit:
    runs-on: [self-hosted, linux, x64]
    steps:
      - uses: actions/checkout@v4
      - name: This label is not a runner version
        run: php artisan test
```

`runs-on` tells Actions which label to match. It does not print `version`. It does not print `registration_deprecates_at`. It does not print `runtime_deprecates_at`. The owner still opens the runners list and the deprecation payload.

If you need a live check after the files exist, the public org-scoped curl shape is the one in the docs. Replace `ORG` and `VERSION`. Do not paste a token into a ticket.

```bash {linenos=inline,hl_lines=[6,12]}
curl -sS -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  "https://api.github.com/orgs/ORG/actions/runners" \
  -o runners.json

curl -sS -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  "https://api.github.com/orgs/ORG/actions/runners/deprecations/VERSION" \
  -o deprecation.json
```

Save. Probe. Write the verdict next to `ACTIONS_RUNNER_OWNER`. Then close the laptop.

Scope still matters. The 28 September shift is GitHub Enterprise Cloud. GitHub Enterprise Server is not impacted by that note. Data Residency already enforced on 31 July 2026. A GHES screenshot is the wrong org. A GHEC screenshot of “date moved” on Wednesday 30 September is a day after full enforcement, not a pause. [Source: https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/]

![Two floors: registration versus runtime; online is not picking up jobs](/img/a-moved-runner-deadline-is-not-an-all-clear-4.png)

## What you must not mix into this ticket

This is not yesterday’s capped count. A 2,500+ badge is an inventory ticket. [A 2,500+ Actions Count Is Not an Exact Run Inventory](/blog/a-2500-plus-actions-count-is-not-an-exact-run-inventory/) already owns that field.

This is not the runner-label ticket. `ubuntu-latest` moving later this year is a pin-and-test ticket for GitHub-hosted images. [Ubuntu-latest Is Not a Runner Image You Already Tested](/blog/ubuntu-latest-is-not-a-tested-runner-image/) already owns that field.

This is not the queue-timeout ticket. A job clock that kills one `queue:work` process is a Laravel worker ticket. [A Timed-Out Job Is Not a Killed Worker](/blog/a-timed-out-job-is-not-a-killed-worker/) already owns that field.

GSC this week still has no striking-distance query on those URLs. I am not refreshing them. This is a new field: a moved self-hosted runner deadline is not an all-clear.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

## What you must not do

Forbidden:

1. File an all-clear ticket without printing the moved date, the full-enforcement day, GHEC versus GHES, the registration floor, the runtime floor, and one human name on Actions runners.
2. Put a runner version in the title or the first line as a version-style hook. The field name is the moved date, not a pin table.
3. Mix this field with a 2,500+ run inventory, an `ubuntu-latest` image pin, or a Laravel job timeout. Those are other posts.
4. Treat “the date moved” as extra weeks. The 28 September note moved remaining full enforcement to 29 September 2026. [Source: https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/]
5. Treat GitHub Enterprise Server as covered. The note says GHES is not impacted. [Source: https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/]
6. Treat a runner at the registration minimum as permanently able to run jobs. June 12 already said that pin is not a permanent execution floor. [Source: https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/]
7. Leave auto-update off, including ARC `disableUpdate=true`, and still file all-clear. That fleet needs a named upgrade cadence. [Source: https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/]
8. Write a permission-bypass, a forged registration, or a runner that pretends to be newer than the binary on disk.
9. Recommend buying Actions minutes, a Copilot plan, or a seat because a self-hosted box is old.
10. Close the ticket from `runs-on: self-hosted` in YAML. Labels are not versions.

Allowed:

1. Print ship day, full-enforcement day, and org type (GHEC, GHEC with Data Residency, or GHES).
2. Save `GET /orgs/{org}/actions/runners` and one deprecation payload. Run `probe_runner_floors.py`.
3. Name one human as `ACTIONS_RUNNER_OWNER`.
4. Recreate runners from a current binary before `./config.sh` when registration is the ticket.
5. Turn auto-update on, or schedule the manual cadence, when runtime is the ticket.
6. Leave GHES out of this note unless a later official page says otherwise.

A changelog bullet about a moved date is not permission to skip the owner.

## What you should do Monday morning

1. Open the org that actually ships. Export `ACTIONS_RUNNER_OWNER` to a human name. Save one runners list and one deprecation payload. Run `probe_runner_floors.py`. Write the verdict on the ticket next to that name.
2. Open the 28 September changelog from the incident. Copy ship day. Copy full-enforcement day. Copy GHEC versus GHES. If today is after 29 September 2026 on GHEC, file “full enforcement already began,” not “we have extra time.” [Source: https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/]
3. If a box needs to register, compare `version` to the registration floor before `./config.sh`. If a box is already registered and jobs sit queued, compare `runtime_deprecates_at` for that version. Do not reuse the headline. [Source: https://docs.github.com/en/rest/actions/self-hosted-runners] [Source: https://github.blog/changelog/2026-09-03-github-actions-early-september-2026-updates/]
4. If someone pasted only a YAML `runs-on` label, reject it. Point at the runners list and the deprecation endpoint.
5. Confirm coding-agent instructions on this desk name the same owner and forbid “the date moved, skip the fleet” without the six lines: owner, ship day, enforcement day, org type, registration floor, runtime floor.
6. Do not refresh the 2,500+ post, the ubuntu-latest post, or the timed-out-job post. Those URLs already exist. This URL is the unused moved-date field.

The question is not whether a moved date demos well in a screenshot. The question is whether the named owner can still tell a moved date from a refused job after handoff.

## Further reading

{{< source href="https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved/" label="GitHub Changelog — Self-hosted runner version enforcement date has moved" >}}

{{< source href="https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/" label="GitHub Changelog — Minimum version enforcement timeline for self-hosted runners" >}}

{{< source href="https://docs.github.com/en/rest/actions/self-hosted-runners" label="GitHub Docs — REST API endpoints for self-hosted runners" >}}
