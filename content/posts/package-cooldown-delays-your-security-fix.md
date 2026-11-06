---
title: "A Package Cooldown Also Delays Your Security Fix"
date: 2026-11-06T06:00:00+07:00
draft: false
slug: "package-cooldown-delays-your-security-fix"
description: "Composer's new cooldown policy holds back fresh releases so malware gets caught first. It holds back the patch for a real vulnerability too. Here is how to set the wait, who on the team may skip it, and how to leave a record when they do."
topics: ["developer-tools"]
tags: ["composer", "php", "laravel", "supply-chain", "security", "dependency-management", "ci", "change-control"]
cover: /covers/package-cooldown-delays-your-security-fix.png
seo:
  primaryQuery: "composer cooldown policy security fix"
  secondaryQueries:
    - "composer no-cooldown flag who can bypass"
    - "composer minimum release age config policy cooldown"
    - "laravel composer supply chain cooldown period"
---

Here is a week every PHP team will have soon.

On Monday you add a one-day cooldown to `composer.json`. From now on, `composer update` will not pick any version that has been public for less than 24 hours. It feels like a seatbelt. On Wednesday morning a library you depend on ships a patch for a real vulnerability. Your scheduled dependency job runs `composer update`, and the patch is not there. Composer resolved the old, vulnerable version, because the fixed one is only three hours old.

Nothing is broken. The policy did exactly what you asked. You asked it to wait.

That is the part of the new Composer cooldown that the release notes say plainly and most teams will skim past: **a cooldown applies to every new version, including the one that fixes your security hole.** The question is not whether a cooldown is a good idea. It is. The question is who on your team is allowed to skip the wait, and how anyone finds out later that they did.

<!--more-->

## What Composer actually shipped

Composer 2.11.0 was announced on the Private Packagist blog on 29 October 2026. The headline feature is a **cooldown dependency policy**: it "withholds newly published package versions for a configurable period of time before Composer will install them." [Source: https://blog.packagist.com/composer-2-11-release/]

Why now? The Packagist team says most malicious releases they saw on Packagist.org in recent months came from attackers who briefly took over a legitimate package, for example through a compromised GitHub account. Composer 2.10 already blocks versions once they are flagged as malware. The gap is the time between "published" and "flagged." A cooldown closes some of that gap. Their own wording: automated scanners can flag the first problems within minutes, so even one hour helps; reports that need a human take longer, so a few hours up to a day catches more. They are honest about the limit too: a cooldown "cannot guarantee that a malicious release is flagged in time." [Source: https://blog.packagist.com/composer-2-11-release/]

Some other people call this a "minimum release age." Same idea.

The facts worth pinning in your team ticket:

| Question | Answer from the docs |
|---|---|
| On by default? | No. Off until you set a `period`. |
| Where is it set? | `config.policy.cooldown` in `composer.json`, global config, or env var |
| What does it affect? | `update`, `require`, `init`, `create-project` |
| Does `composer install` change? | No. It installs exactly what `composer.lock` says |
| Never withheld | `dev-main` style dev versions, platform packages like PHP and extensions |
| Skip it once | `--no-cooldown` on `update`, `require`, `remove`, `create-project` |
| Skip it for some packages | `ignore` list, with a reason per entry |

Sources: the release post and the Composer config docs. [Source: https://getcomposer.org/doc/06-config.md#cooldown]

One more detail is the reason this policy is trustworthy at all. Composer did not ship cooldowns in 2.10 because the only date in package metadata was the `time` field, and whoever publishes the release controls it. An attacker can backdate a malicious tag by weeks and walk straight through a cooldown. Packagist.org now records a `published-time` for every version, based on when Packagist itself first saw it. If a repository you use does not report that timestamp, the command fails and names the package, so a missing date never quietly turns the policy off. [Source: https://blog.packagist.com/composer-2-11-release/]

That is good engineering. It also means the clock starts when Packagist sees the release, not when the maintainer tagged it. If you are waiting for a fix, that is the clock you are on.

### The setting itself

This is the full configuration for a typical Laravel app. One day of cooldown, and an exemption for your own internal packages:

```json
{
    "config": {
        "policy": {
            "cooldown": {
                "period": "1 day",
                "ignore": {
                    "mycompany/*": "Internal packages, reviewed in our own PRs"
                }
            }
        }
    }
}
```

The `period` accepts a string like `"6 hours"` with the units second, minute, hour, day or week, or a plain number of seconds. Relative words like `"tomorrow"` are rejected. [Source: https://getcomposer.org/doc/06-config.md#cooldown]

The `ignore` entry is worth a second look. It takes a reason string. Write a real one. Six months from now, someone will ask why `mycompany/*` skips the wait, and "We trust the code in our own packages" (the docs example) is a fine answer only if it is still true. If a contractor can push tags to one of those repos, it is not.

![One clock, two kinds of release: a hijacked release is flagged inside the one-day cooldown, while a real security fix waits the same 24 hours](/img/package-cooldown-delays-your-security-fix-1.png)

## Where the delay hits the security fix

Read this paragraph from the release post twice:

> A cooldown period applies to every new version, including releases that fix security vulnerabilities. With a cooldown period of one day, Composer will not install a security fix during the first day after its release unless you tell it to.

[Source: https://blog.packagist.com/composer-2-11-release/]

Why not let security fixes skip the wait automatically? Because the attacker in this story has the maintainer's keys. They can publish a fake security advisory themselves, or ship a malicious version right after a real advisory goes out. Any rule that says "advisories skip the cooldown" hands the attacker the bypass. The Packagist team chose not to build that hole, and I agree with them.

So the decision lands on you. Composer gives you one tool for it:

```bash
composer update --no-cooldown vendor/package
```

`--no-cooldown` only skips the cooldown. Blocking of versions with security advisories, malware blocking, and your other policies stay on. That is different from `--no-blocking`, which the docs contrast it with. [Source: https://getcomposer.org/doc/06-config.md#cooldown]

The trap is not the flag. The trap is that the flag only helps **if somebody notices the vulnerability**. The release post says it directly: the longer your cooldown, the longer every fix for a vulnerability you are not actively tracking is delayed. [Source: https://blog.packagist.com/composer-2-11-release/]

That gives you a tradeoff you can actually reason about:

| Cooldown | Malware window covered | Unnoticed security fix delayed by |
|---|---|---|
| none | none | 0 |
| 6 hours | automated scanners, mostly | up to 6 hours |
| 1 day | most automated + many manual reviews | up to 1 day |
| 7 days | more manual reviews | up to 7 days |

The left column comes from the Packagist explanation of detection times. The right column is just arithmetic. The Composer docs use `"7 days"` in their example; the release post recommends a few hours to a day as the balance point. I start teams at one day. A week is a decision you should make on purpose, with a named person watching advisories, not a number you copy from a docs example.

## Two behaviors that will surprise a junior on your team

Neither of these is a bug. Both will cause a confused Slack message the first week.

**First: a full `composer update` can move a package backwards.** If your lock file already has a version that is still inside the cooldown, a full update re-checks every package and can replace it with an older release. If no older version fits your constraints, the update fails. A partial update like `composer update vendor/package` leaves every other locked package alone. [Source: https://getcomposer.org/doc/06-config.md#cooldown]

So the sequence "someone ran `--no-cooldown` for a fix on Wednesday, someone else ran a plain `composer update` on Wednesday afternoon" can quietly undo the fix. The second person did nothing wrong by their own understanding. The lock file diff is the only place this shows up, which is one reason the record I describe below matters.

**Second: your lock file will look outdated right after you upgrade.** Composer 2.11 marks the lock file as outdated when the `policy` config changes. 2.10 ignored that by mistake. If your project already has any `policy` config, you will see a lock warning after upgrading Composer until you update the lock. [Source: https://blog.packagist.com/composer-2-11-release/] Tell the team before they see it, or someone will "fix" it with a full update on a Friday.

![What each Composer command does with a held version: install follows the lock, a partial update is safe for a fix, a full update can undo it](/img/package-cooldown-delays-your-security-fix-2.png)

## Who may run --no-cooldown

This is the part I would actually spend a meeting on. A cooldown is a team rule. A bypass flag that anyone can type, with no trace, turns the rule into a suggestion.

My default split for a small product team:

| Role | May run `--no-cooldown`? | Condition |
|---|---|---|
| Any developer, local branch | Yes | Experiments only, never merged as-is |
| On-call or security owner | Yes, for a named package | Linked advisory or CVE in the PR |
| CI on the main branch | No | CI never bypasses on its own |
| AI coding agent | No | Agents propose; a human runs the bypass |

The last row is the one I feel strongest about. Packagist notes that Private Packagist can enforce a cooldown "independently of the Composer version their developers, AI agents, and CI systems use." [Source: https://blog.packagist.com/composer-2-11-release/] They list agents next to developers and CI for a reason. An agent that hits "this version is withheld" in the middle of a task will look for the shortest path to green, and `--no-cooldown` is one flag away. Write it into your agent instructions: a withheld version is a stop-and-report, not a problem to solve.

The CI row matters just as much. If your pipeline sets `COMPOSER_POLICY_COOLDOWN_PERIOD=0` to "unblock a build," you have turned the policy off for everyone, silently. The docs show that exact line as the way to disable the cooldown temporarily. [Source: https://getcomposer.org/doc/06-config.md#cooldown] Search your CI config for it.

{{< field-note title="Field note" >}}
On the Laravel SaaS projects I maintain, the dependency rule that held up longest was never the clever one. It was "every lock file change says why." When a package moved, the PR said which advisory, which ticket, or which feature needed it. Cooldowns make that rule more important, not less, because now there are two kinds of lock change: the normal one that waited, and the fast one that skipped the wait. If you cannot tell them apart in `git log`, you cannot audit your own supply chain. I would rather have one boring commit trailer than a dashboard nobody opens.
{{< /field-note >}}

## A bypass that leaves a record

Here is the small script I would hand to whoever owns security fixes. It refuses to run without a package name and an advisory ID, runs a partial update with the bypass, re-runs the audit, and writes a commit with trailers that `git log` can search later.

```bash
#!/usr/bin/env bash
# security-fast-path.sh: skip the Composer cooldown for ONE package, with a record.
# Usage: ./security-fast-path.sh vendor/package GHSA-xxxx-xxxx-xxxx "short reason"
set -euo pipefail

PKG="${1:?package name required, e.g. vendor/package}"
ADVISORY="${2:?advisory or CVE id required}"
REASON="${3:?one-line reason required}"
WHO="$(git config user.email)"

composer --version

# Partial update: other locked packages stay where they are.
composer update --no-cooldown "$PKG"

# The bypass skips only the cooldown. Prove the advisory is gone.
composer audit --locked

git add composer.json composer.lock
git commit -m "security: fast-path ${PKG} past cooldown" \
  -m "${REASON}" \
  -m "Cooldown-Bypass: ${PKG}" \
  -m "Advisory: ${ADVISORY}" \
  -m "Bypassed-By: ${WHO}"

echo "Done. Open a PR and link ${ADVISORY}."
```

`composer audit` checks installed packages for known security advisories, and `--locked` audits what is in the lock file rather than what is in `vendor/`. If the fix landed, the advisory you passed in should be gone from the output. If it is still there, `set -e` stops the script before it commits. The Composer CLI docs say `audit` exits with `0` when there are no issues and `1` when it finds packages matching a policy, which includes advisories and malware flags. [Source: https://getcomposer.org/doc/03-cli.md#audit] That also means an unrelated open advisory stops the script. Good. Deal with that one first, or write down why you are accepting it.

Finding every bypass later is then one command:

```bash
git log --grep="Cooldown-Bypass:" --format="%h %ad %s" --date=short
```

That is the whole audit trail. No new tool, no new dashboard.

![Who may run --no-cooldown: developer on a local branch and the security owner yes, CI on main and AI coding agents no](/img/package-cooldown-delays-your-security-fix-3.png)

## CI that waits, and fails loudly when it cannot

The second half is making sure CI respects the same rule the developers do. Two failure modes to guard against: an old Composer binary that does not know about the cooldown at all, and a pipeline variable that turns it off.

On the first one: Private Packagist sells its organization-level cooldown as protecting "projects that have not updated to Composer 2.11 yet." [Source: https://blog.packagist.com/composer-2-11-release/] Read that the other way round. A `composer.json` setting needs a Composer binary that knows the setting. If a runner image is still on an older version, your policy is a comment.

```yaml
# .github/workflows/dependencies.yml (excerpt)
name: dependencies
on:
  pull_request:
    paths: ["composer.json", "composer.lock"]

jobs:
  composer-policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Refuse to run with the cooldown disabled
        run: |
          if [ "${COMPOSER_POLICY_COOLDOWN_PERIOD:-unset}" = "0" ]; then
            echo "COMPOSER_POLICY_COOLDOWN_PERIOD=0 disables the cooldown. Remove it." >&2
            exit 1
          fi

      - name: Set up PHP with Composer 2.11
        uses: shivammathur/setup-php@v2
        with:
          php-version: "8.4"
          tools: composer:2.11.0

      - name: Show the Composer version in the log
        run: composer --version

      - name: Install exactly what the lock says
        run: composer install --no-interaction --prefer-dist

      - name: Audit the lock file
        run: composer audit --locked
```

The `install` step is deliberate. CI on a pull request should install the lock file, not resolve a new one. The cooldown only matters at the moment someone runs `update` or `require`. That is the PR author's machine, your dependency-bot job, or an agent. Those are the places to check, and the commit trailer from the script above is how a reviewer tells a waited update from a fast one.

If you want reviewers to see it without reading trailers, add one checkbox to the pull request template:

```markdown
### Dependencies
- [ ] No lock file change
- [ ] Lock file changed after the normal cooldown
- [ ] Lock file changed with `--no-cooldown` for: ___ (advisory link: ___)
```

Three boxes. A junior developer understands it on the first read, and the third one makes the bypass visible in the place people actually look.

## What the cooldown does not do

It is worth being blunt about the edges so nobody oversells this in a team meeting.

- **It does not scan code.** It only waits. Detection is still Packagist's malware flagging and the security advisory database. The wait just gives them time.
- **It does not protect `dev-main`.** Dev versions represent moving branches and are never withheld. If your app depends on a `dev-` branch of anything, the cooldown does nothing for it.
- **It does not help VCS, path, or artifact repositories the same way.** Those only have the publisher-controlled `time` field. You can set `require-published-time` to `false` for a repository you trust, which falls back to `time`, but you are back to trusting the publisher's clock. [Source: https://blog.packagist.com/composer-2-11-release/]
- **It does not touch `composer install`.** Your production deploy that runs `install` from a committed lock file behaves exactly as before. The cooldown protects the moment the lock file is written, not the moment it is read.

That last point is also the good news. Turning on a cooldown is low risk for deploys. The risk is entirely in the update workflow, which is where your team's habits live.

The same lesson keeps coming back across tools: green output tells you a step ran, not that the step did what you think. I wrote about the generated-code version of that in [Code That Renders Is Not Code You Can Trust](/blog/code-that-renders-is-not-code-you-can-trust/), and about lock files that claim a fix the code does not have in [A Laravel/AI Lockfile Line Is Not a Patched Fetch Client](/blog/a-laravel-ai-lockfile-line-is-not-a-patched-fetch-client/). A cooldown is the same shape of problem, aimed at time instead of code.

## What you should do Monday morning

1. **Upgrade Composer everywhere first.** Laptops, CI images, Docker build stages. Run `composer self-update` and check `composer --version` shows 2.11 or newer. A policy the binary does not know is a comment.
2. **Warn the team about the lock file warning.** If you already have any `policy` config, everyone sees "lock file outdated" after upgrading. Say so in the channel before they see it.
3. **Add a one-day cooldown** with the `composer.json` snippet above. Start at one day, not seven.
4. **Write a real reason on every `ignore` entry.** If you cannot write one sentence explaining why a package skips the wait, it should not skip it.
5. **Name who may run `--no-cooldown`.** One on-call or security owner per project. Put it in the README. Agents and CI are not on the list.
6. **Add the bypass script and the PR checkbox.** Every bypass gets a commit trailer and an advisory link.
7. **Search your CI for `COMPOSER_POLICY_COOLDOWN_PERIOD=0`** and delete it, or make the build fail on it.
8. **Make sure someone actually watches advisories.** The bypass only works if a person notices the vulnerability. A cooldown without an advisory watcher is a delay you added to every fix and told nobody about.

If you are setting this up across several projects, the broader tooling notes live on [Developer Tools](/developer-tools/), and the Laravel and Vue maintenance posts are collected on [Laravel + Vue SaaS](/laravel-vue-saas/).

## Further reading

- {{< source href="https://blog.packagist.com/composer-2-11-release/" label="Composer 2.11 release post (Private Packagist blog)" >}}
- {{< source href="https://getcomposer.org/doc/06-config.md#cooldown" label="Composer config docs: cooldown" >}}
- {{< source href="https://github.com/composer/composer/releases/tag/2.11.0" label="Composer 2.11.0 release on GitHub" >}}
