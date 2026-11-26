---
title: "Laravel's Log File and .env Top a New Credential-Harvesting Ranking: Three Requests to Run on Your Own Site Today"
date: 2026-11-26T07:00:00+07:00
draft: false
slug: "laravel-env-log-credential-targets-three-requests"
description: "VulnCheck's Nov 23 report ranks Laravel secrets and .env files as the top two credential targets. Three requests, a 60-line script and a rotate-first checklist for your own site."
topics: ["tutorials"]
tags: ["laravel", "env-file", "credential-harvesting", "vulncheck", "document-root", "secrets-rotation", "ai-api-keys"]
cover: /covers/laravel-env-log-credential-targets-three-requests.png
seo:
  primaryQuery: "laravel .env file exposed check"
  secondaryQueries:
    - "storage/logs/laravel.log publicly accessible"
    - "laravel document root public folder"
    - "rotate laravel app_key after leak"
---

A new VulnCheck report ranks the credentials attackers ask for most, counted by how many different IP addresses asked. Number one is Laravel secrets: `storage/logs/laravel.log` and `APP_KEY` strings, requested from 4,784 distinct IPs. Number two is the `.env` file, from 2,840 IPs. Both are files that every Laravel project has.

Here is the part a junior developer can act on today. You can find out in about two minutes whether your own site hands out either file. It takes three requests from outside your network and one short Python script. I wrote the script, ran it against two stand-in servers on this machine, and will show you exactly what it printed.

The belief I want to retire is "nobody has attacked my app, so my `.env` is fine." The report's data does not support it, and I will show where. The question is not whether your framework is secure in the demo. It is whether the folder your web server points at, after the third handoff and the second Docker rewrite, is still the folder you meant.

<!--more-->

## What VulnCheck counted

The report is "Attackers Exploit CVEs to Harvest Credentials," dated Nov 23, 2026, by Patrick Garrity at VulnCheck. Its data source is VulnCheck Canaries, which the report uses as its record of attacker requests. Of 694 CVEs tagged in that data, 127 (18%) had at least one credential-harvesting request. Credential harvesting is 13.0% of all Canary exploitation records from January to November 2026, and the report says volume grew about six-fold from July to October, from roughly 17K to 99K records.

The ranking table counts distinct source IPs per credential type. These are the rows that matter for a Laravel developer, copied from the page:

| Rank | Credential | IPs | Records | CVEs | Where it is read from |
|---|---|---|---|---|---|
| 1 | Laravel secrets (`APP_KEY`, DB passwords in logs) | 4,784 | 72K | 14 | `storage/logs/laravel.log`, `APP_KEY` strings |
| 2 | `.env` files | 2,840 | 134K | 55 | `/.env`, `/app/.env`, `/api/.env`, `/proc/self/cwd/.env`, `/static/../.env` |
| 3 | Process environment variables | 2,341 | 44K | 54 | `/proc/self/environ`, `/proc/1/environ` |
| 13 | Package-registry tokens | 458 | 2.6K | 17 | `.npmrc`, `.pypirc`, `.composer/auth.json` |
| 14 | AI provider and coding-agent credentials | 406 | 1.8K | 27 | `~/.openai/config.json`, `OPENAI_API_KEY`, `~/.claude/.credentials.json` |

![Horizontal bar chart of distinct source IPs per credential type from the VulnCheck report: Laravel secrets 4,784, .env files 2,840, process environment 2,341, AWS keys 1,687, package-registry tokens 458, AI provider keys 406.](/img/laravel-env-log-credential-targets-three-requests-1.png)

Read the numbers for what they are. They are requests that VulnCheck's sensors saw, not a count of hacked sites, and not a count of Laravel installs. The page does not say how many of those requests would have succeeded against a real, correctly configured Laravel app. I did not look up which of the 14 Laravel-related CVEs apply to current 12.x or 13.x releases, so I will not name a vulnerable version or a percentage of sites at risk.

One more detail keeps this honest. The biggest growth in harvesting did not come from Laravel. The report says scanners first ramped up on a Vite file-read bug (CVE-2025-30208) in August and September, then moved to a Next.js middleware bypass (CVE-2025-29927), which alone accounted for 68K of October's 99K records. If you run a Vite dev server on a public port, that one is yours too, and the report names the `/@fs/` path as something to alert on.

## The belief this corrects

Most of us sort security news by severity score. A 9.8 gets a meeting. A 5.3 gets a ticket that sits.

The report argues against that habit. It says medium-severity bugs make up just 6% of the CVEs tied to harvesting, yet account for 23% of harvesting records. It names two examples, Laravel log disclosure (CVE-2024-29291) and a Mailpit SSRF bug (CVE-2026-21859), and says neither gives code execution and both are rated 5.3.

Why would an attacker care about a 5.3? Because they are not after your server. They are after what your app already holds. The report puts it this way: "A single file like `.env` can hold database passwords, cloud keys and API tokens all at once." Its advice for a file-read or server-side request bug in an internet-facing app that holds secrets: treat it like a credential-exposure incident, "patch it, then rotate the keys the app could read."

For a junior developer the lesson has two halves:

- A bug that only lets someone read a file is not "low risk" if the file is `.env`.
- Patching closes the door but does not take back what already walked out. Rotation does that.

## Three requests, one script

The three paths come straight from the report's table: `/.env`, `/storage/logs/laravel.log`, and the traversal-shaped `/static/../.env`. Each one should answer with 404 or 403. If any answers with the file, you have a problem that is bigger than anything else on your board this week.

A normal Laravel app serves from `public/`, so none of these files sit inside the web root. The failure case is a web root pointed at the project folder, which happens with copy-pasted Docker files, shared hosting panels, and "I just need it working" afternoons. Laravel's own deployment page is blunt about it: serving the application from the project root "will expose many sensitive configuration files to the public Internet."

Two design choices in the script are worth explaining before you read it:

- **It never prints a response body.** If the request does return your real `.env`, the last thing you want is that text in your terminal scrollback or a CI log. It prints the status code and a verdict.
- **It decides by what the body looks like, not only the status code.** Many sites answer 200 for any path with a friendly page. A 200 that does not look like a `.env` or a Laravel log is marked `CHECK`, not `FAIL`, so you do not panic over a catch-all page.

```python {linenos=inline}
#!/usr/bin/env python3
"""Request three secret-shaped URLs on a site you own and say whether the body looks like the file.

usage: python3 check_secret_urls.py https://example.com
exit:  0 = nothing looked like a secret file, 1 = at least one FAIL, 2 = could not reach the site
Never prints a response body: a leaked secret should not land in your terminal history or CI log.
"""
import http.client
import re
import ssl
import sys
from urllib.parse import urlsplit

# (path sent exactly as written, regex that means "this is the real file")
CHECKS = [
    ("/.env", re.compile(r"(?m)^[A-Z][A-Z0-9_]{2,}\s*=")),
    ("/storage/logs/laravel.log", re.compile(r"(?m)^\[\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\] \w+\.[A-Z]+:")),
    ("/static/../.env", re.compile(r"(?m)^[A-Z][A-Z0-9_]{2,}\s*=")),
]


def fetch(base, path):
    u = urlsplit(base)
    port = u.port or (443 if u.scheme == "https" else 80)
    cls = http.client.HTTPSConnection if u.scheme == "https" else http.client.HTTPConnection
    kw = {"context": ssl.create_default_context()} if u.scheme == "https" else {}
    conn = cls(u.hostname, port, timeout=10, **kw)
    # http.client sends the path string untouched: no dot-segment squashing, no redirect following
    conn.request("GET", path, headers={"User-Agent": "own-site-secret-check/1.0", "Range": "bytes=0-4095"})
    r = conn.getresponse()
    body = r.read(4096).decode("utf-8", "replace")
    conn.close()
    return r.status, body


def main(base):
    worst = 0
    for path, pattern in CHECKS:
        try:
            status, body = fetch(base, path)
        except OSError as e:
            print(f"ERROR  {path:<28} {e}")
            return 2
        if status in (200, 206) and pattern.search(body):
            verdict, worst = "FAIL ", 1
        elif status in (200, 206):
            verdict = "CHECK"  # 200 but not the file: usually a catch-all page, confirm by eye
        elif 300 <= status < 400:
            verdict = "CHECK"  # redirect: look at where it goes
        elif status >= 500:
            verdict = "CHECK"  # an error page proves nothing
        else:
            verdict = "ok   "
        print(f"{verdict} {path:<28} HTTP {status}")
    return worst


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1].rstrip("/")))
```

Run it only against a site you own: `python3 check_secret_urls.py https://your-site.example`. Exit code 1 means at least one `FAIL`, so you can drop it into a deploy step.

Line 29, the `conn.request` call, is the one that matters for the third path. `curl` squashes `..` out of a URL before it sends anything, so a plain `curl https://site/static/../.env` quietly becomes a request for `/.env`. Python's `http.client` sends the string you give it. If you use curl for this check, add `--path-as-is`.

## What I ran, and what I did not

I built a throwaway folder that looks like a Laravel project: a `.env` with obviously fake values, a `storage/logs/laravel.log` with one fake error line, and a `public/` folder with `index.php` and `robots.txt`. Then I started two plain Python file servers on localhost, one with the project folder as its web root and one with `public/` as its web root.

```text
=== A: document root = project folder
FAIL  /.env                        HTTP 200
FAIL  /storage/logs/laravel.log    HTTP 200
FAIL  /static/../.env              HTTP 200
exit=1
=== B: document root = public/
ok    /.env                        HTTP 404
ok    /storage/logs/laravel.log    HTTP 404
ok    /static/../.env              HTTP 404
exit=0
=== nothing listening on the port
ERROR  /.env                        [Errno 111] Connection refused
exit=2
```

![Two web roots side by side. Left: the web root is the project folder, so .env, storage/logs and public/ are all reachable. Right: the web root is public/, so only index.php and assets are reachable and .env and storage stay outside.](/img/laravel-env-log-credential-targets-three-requests-2.png)

I also checked the raw-path claim instead of trusting my memory. I ran a tiny server that answers every request by echoing the path it received:

```text
curl default           -> raw path received: /.env
curl --path-as-is      -> raw path received: /static/../.env
python http.client     -> raw path received: /static/../.env
```

Here is what this does not prove, in plain terms:

- **No real Laravel app was involved.** This host has no PHP, so I could not run `php artisan serve` or a real framework. The test proves the script classifies three situations correctly. It does not prove anything about Laravel's own routing.
- **The third path on server A is not a traversal bug.** Python's file server normalizes the path itself, so `/static/../.env` became `/.env`. On a stand-in it only shows the script sends that path unchanged.
- **No nginx, Apache or Docker was tested.** The nginx lines below are quoted from Laravel's documentation, not run here.
- **Nothing was requested against a live site that I do not own.**

## If any request returns the file

Do these in order. The order is the point.

1. **Close the door first.** Point the web root at `public/`. In nginx that is the `root` line. Laravel's deployment page shows `root /srv/example.com/public;` and a block that refuses hidden files:

   ```nginx
   server {
       listen 80;
       server_name example.com;
       root /srv/example.com/public;

       location ~ /\.(?!well-known).* {
           deny all;
       }
   }
   ```

   Do not "fix" it by moving `index.php` to the project root. The same page warns against exactly that.

2. **Assume the file was read, then rotate.** Everything inside that `.env` or log: the database password, mail and payment keys, third-party API tokens, cloud keys, and the `APP_KEY`. Do the rotation even if your access log shows no hits. Logs rotate and not every proxy keeps them.
3. **Rotate `APP_KEY` with care.** Laravel's encryption page documents `APP_PREVIOUS_KEYS`, a comma-separated list of old keys that lets the app still decrypt data written before the change. My reading, not a line from the page: if the old key leaked, keep it in that list only until you have re-encrypted or discarded the data it protected, then remove it.
4. **Watch for the use of what was taken.** The report suggests monitoring cloud audit logs for credentials used from unexpected places and watching AI provider dashboards for unexpected usage.

![Three-step flow: 1 close the door by pointing the web root at public/, 2 rotate every key the file held including APP_KEY, 3 watch cloud audit logs and AI provider usage.](/img/laravel-env-log-credential-targets-three-requests-3.png)

## The same file holds your AI keys now

Row 14 in the table is the newest. VulnCheck says that since May 2026, attackers have looked for OpenAI, Anthropic, Google Gemini, Hugging Face and other AI provider keys. In total, 1,756 attempts from 406 unique IP addresses across 27 CVEs. The report lists three ways they look: config files, environment variable names such as `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`, and key formats such as `sk-ant-`, `sk-proj-` and `sk-or-v1-`.

Coding agent credential files show up too, but at small scale. The report says requests for Claude Code's `~/.claude/.credentials.json`, OpenAI Codex's `~/.codex/auth.json` and Cline's MCP settings each came from five or fewer IP addresses. Its own words: "It's early, but attackers have clearly added these files as targets."

The practical question for a Laravel developer in 2026 is simple. Does the `.env` on that server also hold an AI provider key, and is that key allowed to do more than this one project needs? A leaked database password hurts. A leaked unrestricted AI key can be resold or used to run workloads at your expense, which the report names as a risk.

You can answer the first half with a search that prints file names and never the keys. I ran this on the same fixture, once on the project folder and once on `public/`:

```bash
grep -rIlE 'sk-(ant|proj|or-v1)-' \
  --exclude-dir=vendor --exclude-dir=node_modules .
```

On the project folder it printed `./.env`. On the clean `public/` folder it printed nothing and exited with status 1, which is how `grep` says "no match." The prefixes come from the report, so this search finds keys in those three formats only. It will not find a key that has another shape.

For the second half, the report's advice is to scope AI keys to the smallest set of models and projects possible, and to rotate them on the same plan as your cloud credentials.

{{< field-note title="Field note" >}}
The release-checklist line I trust most is a boring one: request `/.env` from outside, and expect a 404. It costs one command, and it catches the mistake that no code review will, because the mistake is in a server file or a Docker line, not in a pull request. On a Laravel handoff I would read three things before any application code: the web server's `root`, whether `APP_DEBUG` is on in production (Laravel's deployment page says the debug option decides how much error detail users see), and who can read `storage/logs`. Maintenance is mostly this kind of question. If you run several Laravel and Vue projects, as in the [Laravel and Vue SaaS notes](/laravel-vue-saas/), put the three-request check in the shared deploy script once instead of remembering it per project.
{{< /field-note >}}

## What this post is not saying

- It is not saying your Laravel site is being hacked right now, or that any share of Laravel sites leak. The report counts requests against its own sensors.
- It is not saying Laravel is insecure. A web root on `public/`, which is how the framework is meant to be served, answers the three requests with 404 in my test.
- It is not saying a clean result proves safety. Three 404s prove three paths are closed. They say nothing about your dependencies, your Vite dev server, or the keys already sitting in a backup.
- It does not say how many of the 14 Laravel-related CVEs affect current Laravel versions. I did not look them up.

## What you should do Monday morning

1. Run the script against each site you own, from a machine outside your office network. Write the three result lines in the ticket.
2. If any line says `FAIL`, stop and follow the steps above, in that order. Door first, then rotation.
3. Open the web server config for every project and read the `root` line once. Write down which folder it names.
4. Search each `.env` for AI provider keys with the `grep` above, note which projects hold one, and check that each key is scoped to that project only.
5. Add the script to your deploy step so a bad web root fails the release instead of reaching a user. For the wider habit of leaving a small proof after each change, see [zero-cost observability for agent crons](/blog/zero-cost-observability-agent-crons/) and [one version check and one grep for a Laravel signed link](/blog/laravel-signed-url-expiry-two-conditions/).

If you run AI coding agents on the same servers, the [AI agent operations hub](/ai-agent-operations/) collects notes on what those agents can read, and the [developer tools notes](/developer-tools/) cover which tools get which keys.

## Further reading

{{< source href="https://www.vulncheck.com/blog/credential-harvesting" label="VulnCheck: Attackers Exploit CVEs to Harvest Credentials (Nov 23, 2026)" >}}

{{< source href="https://laravel.com/docs/13.x/deployment" label="Laravel: Deployment (web server configuration and the public directory)" >}}

{{< source href="https://laravel.com/docs/12.x/encryption" label="Laravel: Encryption (gracefully rotating encryption keys)" >}}
