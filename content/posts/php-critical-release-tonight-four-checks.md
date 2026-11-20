---
title: "PHP Says Tonight's Security Release Is Critical: Four Checks on Your Own Server Before It Lands"
date: 2026-11-19T07:00:00+07:00
lastmod: 2026-11-20T08:00:00+07:00
draft: false
slug: "php-critical-release-tonight-four-checks"
description: "PHP shipped its Nov 19 security releases: 8.5.13, 8.4.28, 8.3.37 and 8.2.36. Updated Nov 20 with what each of the seven Critical advisories needs, and four checks you can run on your own server."
topics: ["tutorials"]
tags: ["php", "security-releases", "php-fpm", "laravel", "docker", "patch-management", "change-control"]
cover: /covers/php-critical-release-tonight-four-checks.png
seo:
  primaryQuery: "PHP critical security release November 19 2026"
  secondaryQueries:
    - "which PHP version does my web server use"
    - "php-fpm fastcgi_keep_conn CVE-2026-129289"
    - "php 8.5.13 8.4.28 8.3.37 8.2.36 security release"
---

PHP published its security releases on Thursday, Nov 19, at about 21:05 Jakarta time. php.net now lists the fixed versions, and the advisories name the conditions. I wrote the first version of this post that morning, before any of that existed. This is the same post with the missing half filled in.

The first question has not changed: "Which PHP, and where?" If you cannot answer that in a few minutes, you cannot answer "Are we affected?" either. The second question is new, and it is smaller than the headlines make it sound: which of the Critical conditions do you actually have?

The question is not whether the notice sounds scary. It is whether you can say which PHP serves your web requests, who updates it, and which settings it runs with.

<!--more-->

{{< note type="note" title="Updated on 2026-11-20" >}}
Written on the morning of Nov 19, before the release. Updated on Nov 20 at about 08:00 Jakarta time, after reading php.net and the advisories again. New: the next section, a rewritten check 3, and a real run of the floor script. Check 1, check 2 and the field note are as written.
{{< /note >}}

## Update, Nov 20: what the release pages say now

I read the php.net home page again this morning. I also pulled the 17 advisories that the php-src repository published on Nov 19, between 14:05 and 14:09 UTC, through the GitHub API. By their own severity labels, seven are Critical, four are High and six are Medium.

php.net lists four security releases, one per supported line. It also lists a fifth release that is not a patch: PHP 8.6.0, which it calls "a major update to the PHP language".

| Line | Fixed in | Before (Oct 21) |
|---|---|---|
| 8.5 | 8.5.13 | 8.5.12 |
| 8.4 | 8.4.28 | 8.4.27 |
| 8.3 | 8.3.37 | 8.3.36 |
| 8.2 | 8.2.36 | 8.2.35 |

The two advisories I opened in full list exactly these four numbers as the patched versions. Every Critical one has the same CVSS v4 score, 9.2, and every one needs something extra. I read all seven. This is my shortening of what each says it needs:

| CVE | What it needs | Where you read it |
|---|---|---|
| CVE-2026-129289, PHP-FPM request smuggling | A front end that keeps backend connections open (nginx `fastcgi_keep_conn on`, Apache `enablereuse=on`, HAProxy, LSAPI), and an app path that opens `php://input` without reading it fully | nginx or Apache config |
| CVE-2026-115560, session upload progress | Upload progress enabled, plus a reader of the same session store that uses a different `session.serialize_handler`, plus a gadget chain in the app | php.ini and pool files |
| CVE-2026-126714, session file half overwritten | The default `files` session handler, attacker influence over session data, an interrupted write, and a gadget chain | `session.save_handler` |
| CVE-2026-129474, magic-method backtrace | PHP 8.5 and later. The demonstrated remote attack needs `fatal_error_backtraces=1` and `zend.exception_ignore_args=0` | both settings on the web PHP |
| CVE-2026-129182, backtrace after shutdown | A follow-up to the October bug. Needs a fatal error during shutdown and an early diagnostic in the next request on the same worker. Per-directory Apache config or a front end that sends `PHP_VALUE` can supply it | pool and Apache config |
| CVE-2026-129496, timezone cache | A non-thread-safe build, a startup warning (an invalid `date.timezone`, a session setting warning) written through the file-based `error_log`, and an early request diagnostic in a fresh worker | `error_log`, `date.timezone` |
| CVE-2026-129481, interrupted session shutdown | PHP 8.3 and later. A fatal error in a callback during session cleanup; the report uses a stream resource held in the session, with OPcache off | session code, OPcache |

Read that as a lookup, not a score. Rows 1, 2, 4 and 6 name a setting you can read in one command, and that is check 3. None of the pages I read says these bugs are being exploited. I also found no sentence saying they are not. Treat that as "not stated", not as "safe".

Updating is still the fix. Each Critical advisory lists a workaround, and each workaround is narrower than the update. php.net said the same thing in its October announcement: such measures "reduce exposure to specific attack paths but do not make an installation safe".

One change to the October advice matters. If you set `session.upload_progress.enabled=0` last month, keep it. The CVE-2026-115560 fix switches upload progress off by default, but the advisory says "an explicit setting overrides the new default", so a config that still says `1` stays on. If you need the feature, every reader and writer of that session store must use the same `session.serialize_handler`, even after the update. Separate FPM pools do not mean separate session storage.

What I did not verify: whether your distro package or Docker base image already ships these versions, the six Medium and four High advisories beyond their titles, and anything about my own server.

## What php.net said on Thursday morning

![Timeline from Oct 21 to Dec 31, with the Nov 19 release marked as upcoming and the note that the highest severity is CRITICAL](/img/php-critical-release-tonight-four-checks-1.png)

The picture above is the Thursday-morning snapshot, so its words "tonight" and "next" are history now. The php.net notice said the highest severity was CRITICAL, that the CRITICAL issues "require either non-default configuration or uncommon setups", and that technical details and fixed version numbers would be published alongside the releases. They were.

The releases before it were 8.5.12, 8.4.27, 8.3.36 and 8.2.35, from Oct 21. They fixed two critical bugs that can allow unauthenticated remote code execution. PHP 8.2 reaches end of life on 31 December 2026, and PHP 8.1 and older no longer get updates from the PHP project. Some Linux vendors backport fixes, so ask yours.

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

Two details in that table are easy to get wrong.

**A package can be fixed without a new number.** The October announcement said Linux distributions and LTS vendors "received the patches in advance, so check your vendor for updated packages." Vendors often keep the upstream number and put the fix in the package revision. So after the update, `php -v` printing an older number than php.net lists does not prove you are behind. The package changelog is the vendor's word on it. This is why the floor script in check 4 says "read its changelog" instead of announcing a verdict.

**A moving image tag moves only when you rebuild.** `FROM php:8.4-fpm` means "the newest 8.4 image when I last pulled". If nobody rebuilds, the tag does not move on its own. Rebuild and ask Docker to pull fresh base layers:

```bash
docker build --pull --no-cache -t myapp-web:$(date +%Y%m%d) .
docker compose up -d --force-recreate web queue scheduler
```

One more reminder for the updating step. A patched file on disk does not patch a process that started before the update. After the package changes, restart the web service and every worker. On Debian and Ubuntu, `needrestart` lists services that still run old code.

## Check 3: which of those conditions is yours?

The table above points at a short list of settings. The script below prints them from the **web** PHP, lists the per-pool overrides that beat `php.ini`, searches your nginx and Apache config for connection reuse, and searches your code for runtime session changes. Pass the folders that hold your web server and pool config if they are not in the usual places.

```bash {linenos=inline}
#!/usr/bin/env bash
# php-config-check.sh: print the settings the Nov 19 advisories name, as the WEB PHP sees them,
# then look for the front-end lines that keep FastCGI connections open.
# Usage: php-config-check.sh php-fpm8.4 [config-folder ...]
#        php-config-check.sh "docker exec web php-fpm" /etc/nginx /etc/php
set -u

runner="${1:?pass the web PHP command, e.g. php-fpm8.4}"
shift
dirs=("$@")
[ "${#dirs[@]}" -eq 0 ] && dirs=(/etc/nginx /etc/apache2 /etc/haproxy /etc/php /usr/local/etc)

keys='fatal_error_backtraces|zend\.exception_ignore_args|session\.upload_progress\.enabled|session\.serialize_handler|session\.save_handler|error_log|date\.timezone'

# Print the captured text, or a fallback line when nothing matched.
show() { if [ -n "$1" ]; then printf '%s\n' "$1"; else echo "$2"; fi; }
# Drop lines whose first non-space character is a comment marker.
live() { grep -vE ':[0-9]+:[[:space:]]*[#;]'; }

echo "== php.ini values (what $runner reads) =="
show "$($runner -i 2>/dev/null | grep -E "^($keys) =>")" "nothing printed: wrong command?"

echo
echo "== per-pool overrides (these beat php.ini) =="
show "$(grep -rnE 'php_(admin_)?(value|flag)\[' "${dirs[@]}" 2>/dev/null | live)" \
  "none found in: ${dirs[*]}"

echo
echo "== front end keeps FastCGI connections open? =="
show "$(grep -rnEi 'fastcgi_keep_conn[[:space:]]+on|enablereuse=on' "${dirs[@]}" 2>/dev/null | live)" \
  "none found in: ${dirs[*]}"

echo
echo "== code that changes session settings at runtime =="
show "$(grep -rnE "ini_set\(\s*['\"]session\." --include='*.php' app config bootstrap routes public 2>/dev/null)" \
  "none found"
```

I tested it against a stand-in `php-fpm` that prints phpinfo-style lines, a sample nginx file with one live and one commented-out `fastcgi_keep_conn on;`, an Apache file with `enablereuse=on`, a pool file, and a one-file code folder containing `ini_set('session.serialize_handler', 'php')`. It printed the settings, the pool override, the live nginx line and the Apache line (not the commented-out one), and the code line. When I gave it a binary that does not exist and an empty folder, it printed `nothing printed: wrong command?` and `none found`. It never printed the PHP version or any verdict. That part is yours.

Run it from your project root so the code folders resolve. Three traps:

1. **Terminal PHP and web PHP read different `php.ini` files.** `php --ini` shows the terminal's. The script asks the FPM binary, which reads FPM's. If you use Apache's PHP module instead, request `phpinfo()` from localhost with `curl`, read the settings, and delete the file at once.
2. **Pool files win.** A line such as `php_admin_value[memory_limit] = 256M` in a pool file overrides `php.ini`.
3. **A hit in the connection-reuse section is the line to act on first.** The advisory's interim fix is to turn reuse off, and the update is the real fix. No hit is the good answer for that row only. The other six rows are separate questions.

Save the output next to the inventory. After the update, run it again and compare.

{{< note type="warning" title="This is not a substitute for the update" >}}
Every Critical advisory this week lists a workaround, and each one also names the upgrade. The config check tells you what to read first. It does not tell you that you can skip the update.
{{< /note >}}

## Check 4: compare against the floor

The fixed versions in the table near the top are the **floors**: the lowest version on each line that carries the fix. The rule is simple and boring: copy the floors from php.net by hand, then let a script compare every place on your list against them.

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

I ran it with the real floors against a made-up inventory of six places. The inventory is invented. The verdicts are the script's own output:

```text
$ python3 php-floor-check.py inventory.tsv 8.5=8.5.13 8.4=8.4.28 8.3=8.3.37 8.2=8.2.36
OK             cli:/usr/bin/php  8.4.28
BEHIND         fpm:/usr/sbin/php-fpm8.4  8.4.27  (needs 8.4.28)
OK             container:web (php:8.5-fpm)  8.5.13
BEHIND         container:queue (php:8.3-fpm)  8.3.36  (needs 8.3.37)
NO FLOOR       container:old (php:8.1-fpm)  8.1.30  (no upstream fix for 8.1: ask your vendor or upgrade)
CHECK BY HAND  apache-mod_php  (version: unknown)

4 place(s) need action. A distro package can carry the fix under an older number: read its changelog.
```

Look at the first two lines. The terminal PHP is fixed and the web PHP is not. That is the whole reason this post starts with "Which PHP, and where?".

The script exits with 1 when any place is not OK, so you can put it behind a deploy gate later. When you pass a floor that is not a plain `X.Y.Z`, it refuses and exits with 2. That refusal is deliberate. A floor typed from memory is the number that gets you into trouble.

## What I am not telling you to do

- **Do not move to PHP 8.6 because it shipped the same day.** php.net calls it "a major update to the PHP language". The fixes for the line you run are in 8.5.13, 8.4.28, 8.3.37 and 8.2.36. Moving to 8.6 is a separate decision with its own test plan.
- **Do not skip your older versions.** If your inventory has a PHP 8.1 line, the PHP project is not updating it. The only paths are a vendor backport or moving to a supported line.

{{< field-note title="Field note" >}}
On the Laravel and Vue SaaS projects I maintain, my rule is one inventory file in the repo, next to the deploy notes. It has three to six lines, one per place PHP runs, with the updater's name and the command that prints the version. The web container, the queue worker and the scheduler get separate lines even when they share an image, because a restart is a separate action for each. The test of that file is handoff. Someone who did not build the server should be able to patch it from the file alone, while I am offline.
{{< /field-note >}}

## What you should do Monday morning

The first four items are for today, Friday. The rest waits for Monday.

1. Run `php-where.sh` on every machine that serves your app and save the output as `inventory.tsv`. Add by-hand lines for queue workers, the scheduler and any long-running app server.
2. Put a name next to each line: who updates it, and how. If a line has no name, that is your first finding.
3. Run `php-floor-check.py` with the four floors from the table. Update the lines marked BEHIND, then restart the web service and every worker. Read the version again from inside the running process, not only from the terminal.
4. Run `php-config-check.sh` against your web PHP. If the connection-reuse section prints a line, read the CVE-2026-129289 advisory before your next deploy.
5. On Monday, commit the inventory file to the repo and link it from the deploy notes, so the next person starts from a list.
6. If the inventory has a PHP 8.2 line, put "Dec 31, 2026" on your calendar. That is the end of life date from php.net, six weeks away.

If you are new to this site, start at [/start-here/](/start-here/). The inventory side of a PHP patch is the subject of [PHP 8.5.9 is a runtime patch contract, not an app deploy](/blog/php-8-5-9-runtime-patch-inventory/). The same "where does it run, who owns it" question applies to [Node.js](/blog/node-patch-day-where-your-version-lives/) and to [PostgreSQL 14 reaching end of life](/blog/postgresql-14-end-of-life-one-query/). More Laravel and Vue maintenance notes live under [/laravel-vue-saas/](/laravel-vue-saas/), and tools I keep are under [/developer-tools/](/developer-tools/).

## Further reading

{{< source href="https://www.php.net/index.php" label="php.net: release announcements and the Nov 19 security notice" >}}

{{< source href="https://github.com/php/php-src/security/advisories/GHSA-qc49-hpvq-g2w6" label="GitHub advisory GHSA-qc49-hpvq-g2w6 (CVE-2026-129289, PHP-FPM request smuggling)" >}}

{{< source href="https://github.com/php/php-src/security/advisories/GHSA-658j-r8rw-q6mx" label="GitHub advisory GHSA-658j-r8rw-q6mx (CVE-2026-115560, session serializer mismatch)" >}}

{{< source href="https://www.php.net/supported-versions.php" label="php.net: supported versions and end-of-life dates" >}}
