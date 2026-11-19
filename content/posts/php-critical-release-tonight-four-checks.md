---
title: "PHP Says Tonight's Security Release Is Critical: Four Checks on Your Own Server Before It Lands"
date: 2026-11-19T07:00:00+07:00
draft: false
slug: "php-critical-release-tonight-four-checks"
description: "php.net says tonight's security releases carry a CRITICAL issue that needs non-default or uncommon setups, and publishes no details yet. Four checks you can run before 21:00 WIB, with three scripts."
topics: ["tutorials"]
tags: ["php", "security-releases", "php-fpm", "laravel", "docker", "patch-management", "change-control"]
cover: /covers/php-critical-release-tonight-four-checks.png
seo:
  primaryQuery: "PHP critical security release November 19 2026"
  secondaryQueries:
    - "which PHP version does my web server use"
    - "php-fpm version vs php cli version"
    - "check PHP version in Docker and Laravel queue worker"
---

At 21:00 Jakarta time tonight, the PHP project will publish security releases. php.net has already said the highest severity is CRITICAL. It has not said what is broken, and it has not said which version number fixes it.

That is the whole announcement. The details and the fixed version numbers arrive with the release, around 14:00 UTC. By 21:30 WIB somebody in your team chat will type the question: "Are we affected?" The honest first answer is a question back: "Which PHP, and where?"

If you cannot answer that in a few minutes, today is the day to be able to. You do not need a single CVE detail for this. You need a short list of the places PHP runs for you, a name next to each place, and a way to read each version.

The question is not whether the notice sounds scary. It is whether you can say, before the details land, which PHP serves your web requests and who updates it.

<!--more-->

![Timeline with Oct 21, when two critical fixes shipped, Nov 19, tonight's next security release at 14:00 to 14:30 UTC, and Dec 31, when PHP 8.2 reaches end of life](/img/php-critical-release-tonight-four-checks-1.png)

{{< note type="note" title="Written before the release" >}}
I wrote this on the morning of Thursday, Nov 19, 2026, from the php.net pages as they stood then. Nothing here claims a CVE number or a fixed version for tonight's release, because none exists yet. If php.net already lists fixed versions when you read this, go there first and use the scripts below with those numbers.
{{< /note >}}

## What php.net says this morning

I read the php.net home page and the supported-versions page live this morning. Here is what is written there, and what is not.

| Question | What the page says |
|---|---|
| When | Thursday, 19 November 2026, between 14:00 and 14:30 UTC (21:00 to 21:30 WIB, my conversion) |
| Which versions | "all supported PHP versions" |
| How bad | "The highest severity is CRITICAL." |
| Who is exposed | "The issues rated CRITICAL require either non-default configuration or uncommon setups." |
| What to do | "prepare to upgrade promptly once the releases become available" |
| Details | "Technical details and fixed version numbers will be published alongside the releases." |
| Which CVEs | Not stated |
| Which version numbers fix it | Not stated |

The current releases on the same page are 8.5.12, 8.4.27, 8.3.36 and 8.2.35. Those four came out on Oct 21, and they fixed two critical vulnerabilities that can allow unauthenticated remote code execution. The October announcement said all PHP installations serving web requests were at risk, including PHP-FPM, Apache with mod_php, php-cgi, FrankenPHP and LiteSpeed, with the highest risk for mod_php. It also said, in plain words, that there are no complete mitigations and updating is the only safe choice.

Two more facts from that page matter for tonight. PHP 8.2 reaches end of life on 31 December 2026, and the supported-versions table agrees. And PHP 8.1 and older no longer receive updates from the PHP project, so "tonight's release for all supported versions" does not include them. Some Linux vendors backport fixes. Ask yours.

I will not guess past that. A blog post that invents the details of a release that does not exist yet is worse than no post.

## Check 1: where does PHP run for you?

Most people answer "PHP 8.4" and mean the one they get when they type `php -v`. That command tells you about the PHP **command line**, the one a terminal uses. It does not tell you about the PHP that answers web requests. Those are often different programs, installed in different places, updated by different people.

![Five boxes labelled Terminal, Web (FPM), Queue worker, Scheduler and Container, each with its own PHP, and the note that php -v in your terminal answers for the first box only](/img/php-critical-release-tonight-four-checks-2.png)

Here is a script that lists every PHP it can find on one machine. It checks the terminal PHP, any PHP-FPM binary (FPM is the background service that nginx or Apache usually hands web requests to), Apache's built-in PHP module, and every running Docker container that has a `php` inside.

```bash {linenos=inline}
#!/usr/bin/env bash
# php-where.sh: list every PHP this machine can run, one line each.
# Output: place<TAB>version   (save it: php-where.sh > inventory.tsv)
set -u

emit() { printf '%s\t%s\n' "$1" "$2"; }
ver()  { sed -n 's/^PHP \([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\).*/\1/p' | head -1; }

# 1. The PHP your terminal gets. This is the command line (CLI) only.
if command -v php >/dev/null 2>&1; then
  emit "cli:$(command -v php)" "$(php -v 2>/dev/null | ver)"
fi

# 2. PHP-FPM, the process nginx or Apache usually hands web requests to.
for bin in /usr/sbin/php-fpm* /usr/local/sbin/php-fpm; do
  [ -x "$bin" ] && emit "fpm:$bin" "$("$bin" -v 2>/dev/null | ver)"
done

# 3. PHP loaded inside Apache (mod_php). The version is not printed here.
if command -v apachectl >/dev/null 2>&1 && apachectl -M 2>/dev/null | grep -q 'php'; then
  emit "apache-mod_php" "unknown"
fi

# 4. Running containers: each one has its own PHP.
if command -v docker >/dev/null 2>&1; then
  docker ps --format '{{.Names}} {{.Image}}' 2>/dev/null | while read -r name image; do
    v="$(docker exec "$name" php -v 2>/dev/null | ver)"
    [ -n "$v" ] && emit "container:$name ($image)" "$v"
  done
fi
```

I ran this against a stand-in `php` that prints a real-looking version line, and it printed one tab-separated line with the path and `8.4.27`. On a real server you will see more lines. Run it on every machine that serves your app, not only the one you SSH into first.

The script cannot see everything. Three places need a human:

- **Queue workers and the scheduler.** If they run in their own container, the Docker part finds them. If they run under Supervisor or systemd on the host, they use whichever `php` the unit file names. Open the unit file and read the path.
- **Long-running app servers** such as FrankenPHP, Laravel Octane or RoadRunner. Add a line by hand. A server that stays alive keeps running the old binary until you restart it.
- **Other people's machines.** A shared host, a managed platform, a client's server. Write the line anyway, with "host" as the updater.

## Check 2: who updates each place?

A list of versions without a name next to each line is a list nobody owns. Add a column. Four answers cover almost every line.

| Where PHP comes from | Who updates it | How to read the version |
|---|---|---|
| OS package (apt, dnf) on a server you run | You or your ops person | `apt changelog php8.4-fpm` or `rpm -q --changelog php-fpm` |
| Docker image you build | Whoever owns the Dockerfile | `docker exec <name> php -v`, then the image tag |
| Shared or managed host | The host | Their panel or status page |
| Windows build from php.net | You | The download name, for example `8.5.12-1` |

Three details in that table are easy to get wrong.

**A package can be fixed without a new number.** The October announcement said Linux distributions and LTS vendors "received the patches in advance, so check your vendor for updated packages." Vendors often keep the upstream number and put the fix in the package revision. So after tonight, `php -v` printing an older number than php.net lists does not prove you are behind. The package changelog is the vendor's word on it. This is why the floor script in check 4 says "read its changelog" instead of announcing a verdict.

**A moving image tag moves only when you rebuild.** `FROM php:8.4-fpm` means "the newest 8.4 image when I last pulled". If nobody rebuilds, the tag does not move on its own. Rebuild and ask Docker to pull fresh base layers:

```bash
docker build --pull --no-cache -t myapp-web:$(date +%Y%m%d) .
docker compose up -d --force-recreate web queue scheduler
```

**Windows builds have their own suffix.** The PHP team also announced updated Windows builds named 8.5.12-1, 8.4.27-1, 8.3.36-1 and 8.2.35-1. The `-1` marks a rebuild with updated dependencies, and the PHP runtime version stays the same. If you run PHP on Windows, the file name tells you more than `php -v` does.

One more reminder for the updating step. A patched file on disk does not patch a process that started before the update. After the package changes, restart the web service and every worker. On Debian and Ubuntu, `needrestart` lists services that still run old code.

## Check 3: is your setup one of the unusual ones?

php.net says the CRITICAL issues need "non-default configuration or uncommon setups". I do not know which configuration, and tonight's page will say. But you can write down your own configuration now, so that at 21:30 the question becomes a lookup instead of an investigation.

php.net named a handful of settings last month. In the October announcements, for the two critical issues, these were `memory_limit`, `post_max_size`, `upload_max_filesize`, `session.upload_progress.enabled` and, on PHP 8.5, `fatal_error_backtraces`. A separate notice on the same page, with no date shown, added a third issue, CVE-2026-115560. It involves `session.serialize_handler` set to `php_binary` or `php_serialize` in configuration, then switched to `php` at runtime with `ini_set()` before `session_start()`, with upload progress still on. That notice says a full advisory comes "with the next release". php.net does not say whether tonight's release is that one. I am not connecting the two.

So this check is not "am I vulnerable tonight". It is "what does my web PHP actually run with". The script below prints those settings from the **web** PHP, lists per-pool overrides that beat `php.ini`, and greps your code for runtime session changes.

```bash {linenos=inline}
#!/usr/bin/env bash
# php-config-check.sh: show the settings php.net named last month, as the WEB PHP sees them.
# Usage: php-config-check.sh php-fpm8.4
#        php-config-check.sh "docker exec web php-fpm"
set -u

runner="${1:?pass the web PHP command, e.g. php-fpm8.4}"
keys='memory_limit|post_max_size|upload_max_filesize|session\.upload_progress\.enabled|session\.serialize_handler|fatal_error_backtraces'

show() { if [ -n "$1" ]; then printf '%s\n' "$1"; else echo "$2"; fi; }

echo "== php.ini values (what $runner reads) =="
show "$($runner -i 2>/dev/null | grep -E "^($keys) =>")" "nothing printed: wrong command?"

echo
echo "== per-pool overrides (these beat php.ini) =="
show "$(grep -rnE 'php_(admin_)?(value|flag)\[' /etc/php/*/fpm/pool.d/ /usr/local/etc/php-fpm.d/ 2>/dev/null)" \
  "none found in the usual folders"

echo
echo "== code that changes session settings at runtime =="
show "$(grep -rnE "ini_set\(\s*['\"]session\." --include='*.php' app config bootstrap routes public 2>/dev/null)" \
  "none found"
```

I tested it against a stand-in `php-fpm8.4` that prints phpinfo-style lines and a one-file code folder containing `ini_set('session.serialize_handler', 'php')`. It printed the five settings and flagged that line, and it printed `nothing printed: wrong command?` when I gave it a binary that does not exist. My first version printed "none found" even after a match, because `grep` exits with an error when one of the folders is missing. If you copy an older snippet from somewhere, check that case.

Run it from your project root so the code folders resolve. Two traps:

1. **Terminal PHP and web PHP read different `php.ini` files.** `php --ini` shows the terminal's. The script asks the FPM binary, which reads FPM's. If you use Apache's PHP module instead, request `phpinfo()` from localhost with `curl`, read the settings, and delete the file at once.
2. **Pool files win.** A line such as `php_admin_value[memory_limit] = 256M` in a pool file overrides `php.ini`, and php.net's own October advice told people to set some values in places "applications can't override".

Save the output next to the inventory. Tonight, the details will either name one of these settings or they will not. Either way you will not start from a blank page.

{{< note type="warning" title="This is not a substitute for the update" >}}
The October announcement said that configuration changes reduce exposure to specific attack paths and do not make an installation safe. The same holds tonight. The config check tells you what to read first. It does not tell you that you can skip the update.
{{< /note >}}

## Check 4: after 21:30 WIB, compare against the floor

Tonight you will get a set of fixed version numbers, one per supported line. I call each of those a **floor**: the lowest version on that line that carries the fix. The rule is simple and boring: copy the floors from php.net by hand, then let a script compare every place on your list against them.

![Three steps: read php.net, copy the floors, run the check, and four verdicts OK, BEHIND, NO FLOOR and CHECK BY HAND](/img/php-critical-release-tonight-four-checks-3.png)

```python {linenos=inline}
#!/usr/bin/env python3
"""php-floor-check.py: compare an inventory with the fixed versions php.net publishes.

Usage:
  php-floor-check.py inventory.tsv 8.5=X.Y.Z 8.4=X.Y.Z 8.3=X.Y.Z 8.2=X.Y.Z

Copy each floor from the php.net announcement. The script never guesses one.
Exit code: 0 if every row is OK, 1 if anything needs action or a human look.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def as_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2

    floors: dict[str, tuple[int, ...]] = {}
    for arg in argv[2:]:
        line, _, floor = arg.partition("=")
        if not re.fullmatch(r"\d+\.\d+", line) or not re.fullmatch(r"\d+\.\d+\.\d+", floor):
            print(f"bad floor '{arg}': use 8.4=8.4.NN with the real number")
            return 2
        floors[line] = as_tuple(floor)

    problems = 0
    for row in Path(argv[1]).read_text().splitlines():
        place, _, version = row.partition("\t")
        version = version.strip()
        match = re.fullmatch(r"(\d+\.\d+)\.\d+", version)
        if not match:
            print(f"CHECK BY HAND  {place}  (version: {version or 'empty'})")
            problems += 1
            continue
        line = match.group(1)
        if line not in floors:
            print(f"NO FLOOR       {place}  {version}  (no upstream fix for {line}: ask your vendor or upgrade)")
            problems += 1
        elif as_tuple(version) < floors[line]:
            floor = ".".join(map(str, floors[line]))
            print(f"BEHIND         {place}  {version}  (needs {floor})")
            problems += 1
        else:
            print(f"OK             {place}  {version}")

    if problems:
        print(f"\n{problems} place(s) need action. A distro package can carry the fix under an older number: read its changelog.")
        return 1
    print("\nEvery listed place is at or above the floor.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

I ran it against a made-up inventory with made-up floors. The floors `8.4.50`, `8.3.40` and so on are not real numbers. They only exist to show all four verdicts:

```text
$ python3 php-floor-check.py inventory.tsv 8.5=8.5.99 8.4=8.4.50 8.3=8.3.40 8.2=8.2.40
BEHIND         cli:/usr/bin/php  8.4.27  (needs 8.4.50)
BEHIND         fpm:/usr/sbin/php-fpm8.3  8.3.30  (needs 8.3.40)
NO FLOOR       container:web (php:8.1-fpm)  8.1.30  (no upstream fix for 8.1: ask your vendor or upgrade)
CHECK BY HAND  apache-mod_php  (version: unknown)
OK             fpm:/usr/sbin/php-fpm8.5  8.5.99

4 place(s) need action. A distro package can carry the fix under an older number: read its changelog.
```

The script exits with 1 when any place is not OK, so you can put it behind a deploy gate later. When you pass a floor that is not a plain `X.Y.Z`, it refuses and exits with 2. That refusal is deliberate. A floor typed from memory is the number that gets you into trouble.

## What I am not telling you to do tonight

- **Do not upgrade to PHP 8.6 because it is in the news.** The php.net page lists PHP 8.6.0 as planned for the same day, and its own text for the last release candidate says not to use it in production. That is a separate decision with a separate test plan. Tonight is a patch on the line you already run.
- **Do not wait for a perfect inventory.** A half-filled list with names beats a perfect list at midnight.
- **Do not trust a headline.** If a social post says a PHP bug "affects everyone", read the php.net page for the words "non-default configuration or uncommon setups" and for the CVE page itself.
- **Do not skip your older versions.** If your inventory has a PHP 8.1 line, the PHP project is not updating it. The only paths are a vendor backport or moving to a supported line.

{{< field-note title="Field note" >}}
On the Laravel and Vue SaaS projects I maintain, my rule is one inventory file in the repo, next to the deploy notes. It has three to six lines, one per place PHP runs, with the updater's name and the command that prints the version. The web container, the queue worker and the scheduler get separate lines even when they share an image, because a restart is a separate action for each. The test of that file is handoff. Someone who did not build the server should be able to patch it from the file alone, while I am offline.
{{< /field-note >}}

## What you should do Monday morning

Tonight is Thursday, so the first three items are for this evening. The rest waits for Monday.

1. Before 21:00 WIB, run `php-where.sh` on every machine that serves your app and save the output as `inventory.tsv`. Add the by-hand lines for queue workers, the scheduler and any long-running app server.
2. Put a name next to each line: who updates it, and how. If a line has no name, that is your first finding.
3. At 21:30 WIB, open php.net and read the announcement. Copy the fixed versions by hand into the `php-floor-check.py` command. If the page names a setting, run `php-config-check.sh` against your web PHP and read the output with that setting in mind.
4. Update the lines marked BEHIND, then restart the web service and every worker. Read the version again from inside the running process, not only from the terminal.
5. On Monday, commit the inventory file to the repo and link it from the deploy notes, so the next person starts from a list.
6. If the inventory has a PHP 8.2 line, put "Dec 31, 2026" on your calendar. That is the end of life date from php.net, and it is six weeks away.

If you are new to this site, start at [/start-here/](/start-here/). The inventory side of a PHP patch is the subject of [PHP 8.5.9 is a runtime patch contract, not an app deploy](/blog/php-8-5-9-runtime-patch-inventory/). The same "where does it run, who owns it" question applies to [Node.js](/blog/node-patch-day-where-your-version-lives/) and to [PostgreSQL 14 reaching end of life](/blog/postgresql-14-end-of-life-one-query/). More Laravel and Vue maintenance notes live under [/laravel-vue-saas/](/laravel-vue-saas/), and tools I keep are under [/developer-tools/](/developer-tools/).

## Further reading

{{< source href="https://www.php.net/index.php" label="php.net: upcoming critical security release notice and the October announcements" >}}

{{< source href="https://www.php.net/supported-versions.php" label="php.net: supported versions and end-of-life dates" >}}

{{< source href="https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp" label="GitHub advisory GHSA-6wmf-4rv5-p3rp (CVE-2026-109619, October)" >}}

{{< source href="https://www.php.net/downloads.php" label="php.net: downloads, including Windows builds" >}}
