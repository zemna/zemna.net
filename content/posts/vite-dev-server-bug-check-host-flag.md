---
title: "Vite Fixed a Critical Dev Server Bug: Check Whether Anyone on Your Team Runs It With --host"
date: 2026-11-13T07:00:00+07:00
draft: false
slug: "vite-dev-server-bug-check-host-flag"
description: "Vite's Nov 10 advisory is rated Critical, but it only reaches dev servers that are opened to the network. How to find your Vite versions and every place someone types --host, with two small scripts."
topics: ["frontend"]
tags: ["vite", "security-advisory", "dev-server", "docker-compose", "laravel", "vue", "npm", "patch-management"]
cover: /covers/vite-dev-server-bug-check-host-flag.png
seo:
  primaryQuery: "vite dev server remote code execution"
  secondaryQueries:
    - "vite --host security"
    - "check vite version npm"
    - "vite critical advisory update"
---

Somebody on every team has typed `vite --host`. The reason is ordinary: the page has to open on a phone, on a teammate's laptop, or from inside a container, and the dev server only answers on your own machine until you tell it otherwise.

This week that flag got a security rating. On Nov 10, 2026, the Vite team published an advisory rated **Critical**. A request sent to the dev server can make it read files it should refuse and run code. The sentence that decides whether you care is short: only apps that explicitly expose the dev server to the network are affected.

So the question for your team is not "are we on a bad Vite?" It is "does anyone here run the dev server where other machines can reach it, and which Vite is that?"

<!--more-->

The question is not whether the bug sounds scary. It is whether you can name every place your team starts a dev server and say who can open it.

## What the advisory says, in plain words

I re-read the advisory page on Nov 13 at about 08:00 Jakarta time. These are its own words, shortened:

| Question | What the page says |
|---|---|
| Title | Remote code execution using the `__vite-browser-external` virtual module |
| Published | Nov 10, 2026 |
| Rating | Critical, CVSS v4 score 9.1 |
| CVE number | "No known CVE" |
| Who is affected | Only apps that explicitly expose the Vite dev server to the network, using `--host` or the `server.host` config option |
| What a request can do | Get files read that the dev server's file allow list should block, and get code run through Vite's own evaluation of worker and glob code |
| Fixed in | 8.3.7, 8.2.5, 8.1.7, 7.3.8, 6.4.6; and `vite-plus` 1.5.1 |

"Remote code execution" is a heavy phrase, so here is the plain version. Someone who can send an HTTP request to your dev server can make the machine running it do something it was never meant to do. The dev server is the process behind `npm run dev`: it serves your app with hot reload, and it sits right next to your source files and your environment.

The page says the problem is that two virtual modules put a value taken from the URL into generated code without escaping it. I am not going to describe the request. You do not need it to decide what to do, and the advisory page has it if you must read it.

The page also notes that in Vite 8 the vulnerable code lives in the Rolldown bundler binary, not in Vite's own JavaScript. It says 8.3.7 and 8.2.5 rely on the fix in Rolldown 1.2.17, and 8.1.7 on the fix in Rolldown 1.1.7. That is why the 8.x fixes look like dependency bumps. It does not change what you do.

![Two panels. Left: the default dev server only answers on this machine. Right: with --host or host: true it listens on all addresses, LAN and public included.](/img/vite-dev-server-bug-check-host-flag-1.png)

## The one condition: who can open the address

The Vite docs describe the setting in a few short lines. `server.host` has the default `'localhost'`. Setting it to `0.0.0.0` or `true` makes the server listen on all addresses, "including LAN and public addresses". On the command line, that is `--host 0.0.0.0` or just `--host`.

LAN means the local network: the office Wi-Fi, the home router, a coworking space. "Public addresses" means the machine has an address the internet can reach, which is normal on a cloud box or a dev server you rent.

So there are three cases, and they are not equal:

1. **Default localhost.** Only your machine opens it. The advisory's condition is not met. Update anyway, but this is not an emergency.
2. **`--host` on a laptop on a trusted network.** Other machines on that network can reach it. How bad that is depends on who shares the network.
3. **`--host` on a shared dev box, a cloud workspace, or a container with its port published.** This is the case to fix first. The address is reachable by more people than you think, for longer than you think.

Why would anyone add `--host`? A container, a cloud workspace, a remote dev box and a coding agent's preview window all have the same problem: the browser is not on the machine that runs the server. The flag is a reasonable answer to a real need. It also tends to stay in a script long after the demo is over.

## Check 1: which Vite is each place running

A version number in `package.json` is a range, not an answer. `^8.3.6` allows 8.3.6 until the lockfile moves. And Vite often comes in twice: your own copy, plus one inside a tool that bundles it, such as a test runner.

This script reads the tree that `npm ls` prints and compares each Vite with the advisory's affected ranges. It only judges exact `x.y.z` values. A pre-release or a range is reported as `CHECK`, because guessing is how a list goes wrong. It exits 1 if anything is behind.

```python
#!/usr/bin/env python3
"""Compare Vite versions with the ranges in GHSA-p4f5-76q4-ffq7.

Usage: vite_floor.py VERSION [VERSION ...]      e.g. 8.3.6 7.3.8 5.4.0
   or: npm ls vite --all --json > ls.json; vite_floor.py --npm-ls ls.json
Exit 0 = every version is outside the listed ranges.
Exit 1 = at least one is inside a listed range or cannot be judged.
Exit 2 = no input.
"""
import json
import re
import sys

# From the advisory's "Affected versions" list (package: vite).
AFFECTED = [
    ((4, 0, 0), (6, 4, 5), "move to 6.4.6 or newer"),
    ((7, 0, 0), (7, 3, 7), "7.3.8 is the patched release"),
    ((8, 0, 0), (8, 1, 6), "8.1.7 is the first patched release"),
    ((8, 2, 0), (8, 2, 4), "advisory lists 8.2.5 as patched"),
    ((8, 3, 0), (8, 3, 6), "8.3.7 is the patched release"),
]


def parse(text):
    m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", text.strip())
    return tuple(int(x) for x in m.groups()) if m else None


def judge(text):
    v = parse(text)
    if v is None:
        return "CHECK", "not an exact x.y.z (pre-release or range): read it by hand"
    for low, high, hint in AFFECTED:
        if low <= v <= high:
            return "BEHIND", hint
    return "ok", "outside the listed ranges"


def walk(node, found):
    for name, info in (node.get("dependencies") or {}).items():
        if name == "vite" and "version" in info:
            found.add(info["version"])
        walk(info, found)


def main(argv):
    versions = []
    if argv[:1] == ["--npm-ls"] and len(argv) == 2:
        found = set()
        walk(json.load(open(argv[1])), found)
        versions = sorted(found)
    else:
        versions = argv
    if not versions:
        print("no versions given")
        return 2
    bad = 0
    for text in versions:
        status, why = judge(text)
        bad += status != "ok"
        print(f"{status:6} {text:12} {why}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

I ran it on a throwaway project with Vite 8.3.6 installed, then again after moving to the current `latest`:

```bash
$ npm ls vite --all --json > ls.json && python3 vite_floor.py --npm-ls ls.json
BEHIND 8.3.6        8.3.7 is the patched release
$ echo $?
1

$ npm install vite@8.3.8     # npm "latest" on Nov 13
$ npm ls vite --all --json > ls.json && python3 vite_floor.py --npm-ls ls.json
ok     8.3.8        outside the listed ranges
$ echo $?
0
```

On a hand-made fixture with a second, nested Vite, it also caught the copy you do not own:

```text
BEHIND 7.3.7        7.3.8 is the patched release
BEHIND 8.3.6        8.3.7 is the patched release
```

That nested 7.x copy is the common surprise. Updating your own `vite` line does not touch it. The fix there is to update the tool that carries it, or to use an override that your package manager supports, and to run the check again after.

![Three checks in order: which Vite, who adds --host, who can reach it.](/img/vite-dev-server-bug-check-host-flag-2.png)

For the exact floors by line, here is the same list from the advisory as a picture. The 4.x and 5.x lines have no patched release of their own, so the move there is to 6.4.6 or newer. That is a major upgrade and deserves a plan, not a Friday-evening `npm update`.

![A table of patched Vite versions per line: 8.3.7, 8.2.5, 8.1.7, 7.3.8, 6.4.6.](/img/vite-dev-server-bug-check-host-flag-3.png)

One detail from the registry is worth knowing. The advisory lists 8.2.5 as patched. The npm registry lists 8.2.4 and then 8.2.6, with no 8.2.5 in between. GitHub has a tag for each. So if you are on the 8.2 line and run `npm install`, you get 8.2.6, which is past the listed fix. If your tooling insists on the exact number from the advisory, it will not find it on npm.

## Check 2: who adds `--host`

A version check says what you run. It does not say whether the condition is met. For that, look for the places where someone opens the server to the network. They are boring and they are few:

- `package.json` scripts: `"dev": "vite --host"`
- `vite.config.*`: `server: { host: true }` or `host: '0.0.0.0'`
- `docker-compose*.yml`: a `ports:` line that publishes the dev port on every address
- README or onboarding docs: "run `npx vite --host` so your phone can open it"

This script reads those files and prints each hit with a file and line number. It does not start anything and it does not edit anything. It also collects any `--port` value it sees and treats that port like the default 5173 when it reads compose files, because a team that changed the port still publishes the same port.

```python
#!/usr/bin/env python3
"""Find places where a Vite dev server may be opened to the network.

Usage: vite_host_scan.py [REPO_DIR]
Exit 0 = nothing found. Exit 1 = something to look at. Exit 3 = bad path.

Looks for: the --host flag, a host option set to true or 0.0.0.0 in a Vite
config, and compose port mappings for the dev port that are not bound to
127.0.0.1. It reads files only. It does not start anything.
"""
import json
import re
import sys
from pathlib import Path

SKIP = {"node_modules", ".git", "dist", "vendor", "build", ".next", ".nuxt"}
TEXT_NAMES = ("Dockerfile", "Makefile", "Procfile")
TEXT_SUFFIX = (".md", ".sh", ".yml", ".yaml", ".json", ".js", ".ts",
               ".mjs", ".mts", ".cjs", ".cts", ".env", ".example")

HOST_FLAG = re.compile(r"(?<![\w-])--host(?![\w-])")
HOST_OPT = re.compile(r"""\bhost\s*:\s*(true|['"]0\.0\.0\.0['"]|['"]::['"])""")
PORT_FLAG = re.compile(r"--port[=\s]+(\d{2,5})")
PORT_LINE = re.compile(r"""^\s*-\s*['"]?(?P<map>[\d.:]+)['"]?\s*$""")


def files(root):
    for p in root.rglob("*"):
        if not p.is_file() or SKIP & set(p.relative_to(root).parts):
            continue
        if p.name.startswith(TEXT_NAMES) or p.suffix in TEXT_SUFFIX:
            yield p


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 3
    hits, ports = [], {"5173"}
    for p in files(root):
        try:
            lines = p.read_text(errors="replace").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            ports.update(PORT_FLAG.findall(line))
            if HOST_FLAG.search(line) and "vite" in line.lower():
                hits.append((p, n, "flag", line.strip()))
            elif p.name.startswith("vite.config") and HOST_OPT.search(line):
                hits.append((p, n, "config", line.strip()))
    for p in files(root):
        if "compose" not in p.name or p.suffix not in (".yml", ".yaml"):
            continue
        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            m = PORT_LINE.match(line)
            if not m:
                continue
            mapping = m.group("map")
            if any(port in mapping for port in ports) and not mapping.startswith("127.0.0.1"):
                hits.append((p, n, "port", line.strip()))
    for p, n, kind, text in hits:
        print(f"{kind:6} {p.relative_to(root)}:{n}  {text}")
    print(f"ports checked: {sorted(ports)}")
    print(f"{len(hits)} place(s) to look at")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
```

I built a small fixture that has every case: a script with `--host`, a second script with `--host 0.0.0.0 --port 5174`, a config with `host: true`, a doc that tells people to use the flag, and a compose file with one open port and one bound to `127.0.0.1`. This is what it printed:

```text
$ python3 vite_host_scan.py vitedemo
flag   package.json:4  "dev": "vite --host",
flag   package.json:6  "preview-lan": "vite --host 0.0.0.0 --port 5174"
config vite.config.ts:4  host: true,
flag   docs/dev.md:1  Run `npx vite --host` so your phone can open it.
port   docker-compose.yml:6  - "5173:5173"
ports checked: ['5173', '5174']
5 place(s) to look at
$ echo $?
1
```

Look at the compose file in that fixture. `"127.0.0.1:5174:5174"` was not flagged, and `"5173:5173"` was. That is the whole point of the `port` rule: the same kind of port, published two ways, is two different answers to "who can reach it".

I also ran the scanner on this site's own repository. It found nothing and exited 0. That is a check of the scanner, not proof that no Laravel starter ever passes `--host`. I did not look at any.

Run it from the root of every repo that has a front end, and add it to the places you read when someone says "it works on my phone".

## The release notes did not say "security"

This is the part that surprised me, and it is why a version bump alone is a bad plan.

The npm package for 8.3.7 went out on Nov 9, 2026, at 10:25 UTC. The advisory is dated Nov 10. I read the GitHub release body for v8.3.7. Under Bug Fixes it has one line, an update of Rolldown to v1.2.18, plus lint rules, a test cleanup and a sourcemap change. The words "security", "advisory" and "vulnerability" do not appear in it.

The release bodies for 8.2.5, 8.1.7, 7.3.8 and 6.4.6 each say only "Please refer to CHANGELOG.md for details". I did not open those changelog files.

None of this is a complaint. Fixing first and publishing the advisory a day later is a common way to run disclosure, and the advisory is where the Vite team wrote the details. It does mean one practical thing for you: if your update routine is "read the release notes and update what looks important", this release did not look important. A package cooldown adds to it. I wrote about that in [A Package Cooldown Also Delays Your Security Fix](/blog/package-cooldown-delays-your-security-fix/). If your rule delays new releases by a week, your dev tooling stays on the vulnerable version for the whole week. `latest` was already 8.3.8 on Nov 11, published at 02:49 UTC.

## When you do need another device to open it

There are fair reasons to want a phone, a colleague or a container to reach the dev server. A few options keep the exposure small. These are my suggestions, not the advisory's.

**Publish the container port on your own machine only.** In compose, put `127.0.0.1` in front of the mapping:

```yaml
services:
  web:
    build: .
    command: npm run dev
    ports:
      # reachable from this machine only; other machines cannot open it
      - "127.0.0.1:5173:5173"
```

Vite inside the container still has to listen on the container's address, so the app can accept the connection. What changed is who can reach the published port: your own machine. It is smaller, not zero. Other containers on the same Docker network can still reach it.

**Use a tunnel instead of a public address, when the server is on a remote box.** Leave Vite on localhost on that box and forward a port from your laptop:

```bash
# Run Vite on the dev box WITHOUT --host, then from your laptop:
ssh -N -L 5173:127.0.0.1:5173 devbox
# Open http://localhost:5173 on your laptop.
```

**Say it in the repo.** If a script must keep `--host`, put the reason next to it, in the README, with the name of the person who owns it. A flag with an owner gets removed when the need ends. A flag without one lives for years.

One more setting sits next to this one. The Vite docs mark `server.allowedHosts: true` with a DANGER note and link a different advisory, GHSA-vg6x-rcgg-rjx6, about DNS rebinding. That is a different bug with a different condition. I did not read that advisory for this post. Add `allowedHosts` to the same search and read the docs line yourself.

{{< field-note title="Field note" >}}
The dev server is the one piece of a Laravel and Vue stack that nobody puts on a patch list, because it is "only for development". On the Laravel and Vue projects I look after, and the Modoo SaaS projects are that shape, the person who types `--host` is usually not the person who reviews the compose file or the shared dev box, and neither of them owns the lockfile. Each is reasonable alone. The advisory is a reminder that "only for development" is a promise about where the server runs, not a property of the software. The question is not whether the fix is one command. It is whether anyone owns the place where the command has to run.
{{< /field-note >}}

## What this does not say

Short list, so nobody reads more into it than the page says:

- It does not say every Vite user is affected. The page names one condition.
- It does not say a production build is affected. The page is about the dev server, and I did not test a build.
- It does not give a CVE number. The page says "No known CVE". If one appears later, quote the page, not this post.
- It does not say which frameworks pass `--host` by default. I did not check any.
- It does not tell 4.x and 5.x users which exact version to take. It lists no patched release in those lines, so "6.4.6 or newer" is my reading of the list, not a sentence from the page.

## What I did and did not verify

On Nov 13 at about 08:00 Jakarta time I read the advisory page (GHSA-p4f5-76q4-ffq7) in full, the Vite "server options" docs page, the GitHub release bodies for 8.3.8, 8.3.7, 8.2.6, 8.2.5, 8.1.7, 7.3.8 and 6.4.6, and the npm registry record for `vite` (dist-tags and publish times).

I ran both scripts on the inputs shown: a real throwaway project with Vite 8.3.6 and then 8.3.8, a hand-made `npm ls` fixture with a nested copy, a fixture repo for the scanner, an empty folder (exit 0), a missing path (exit 3) and this site's repository. I did not run the exploit and I did not test any fix. I did not open the CHANGELOG files, the Rolldown releases, `vite-plus`, or the second advisory. Re-read the advisory before you act: a later edit can move the floors or add a CVE.

## What you should do Monday morning

These fit in one sitting, whatever day you read this.

1. **Write down every place a dev server starts:** laptops, the shared dev box, containers, cloud workspaces, CI preview jobs. One line each.
2. **Run the version check on each repo:** `npm ls vite --all --json > ls.json`, then `python3 vite_floor.py --npm-ls ls.json`. Fix the `BEHIND` rows first, including nested copies.
3. **Run the scanner on each repo** and read every hit. Put a name next to each one that stays.
4. **Fix shared boxes and published ports first.** A laptop on a home network is the smallest risk, a shared dev box the biggest.
5. **Change `"5173:5173"` to `"127.0.0.1:5173:5173"`** in compose files where the only reader is you.
6. **Search for `allowedHosts`** in the same pass and read the docs warning before you leave it set to `true`.
7. **Check your update rule.** If a cooldown or a "read the release notes first" habit delays tooling updates, add an exception for advisories.
8. **On 4.x or 5.x, open a ticket** for the upgrade to 6.4.6 or newer, with an owner and a date.

## What this connects to

Same habit as [Node.js Security Fixes Are Out: Is Every Place You Run Node Past the Fix?](/blog/node-patch-day-where-your-version-lives/): a list of places, a check against the fix, and one name per row. [Two Agents, One Database: Herd Workspaces Share the Parent DB by Default](/blog/herd-workspaces-share-the-parent-database/) is the same kind of dev-environment default that nobody wrote down. More notes of this kind are on [Laravel and Vue SaaS](/laravel-vue-saas/), [Developer Tools](/developer-tools/) and [AI Agent Operations](/ai-agent-operations/), and [Start Here](/start-here/) lists the reading order.

## Further reading

- {{< source href="https://github.com/vitejs/vite/security/advisories/GHSA-p4f5-76q4-ffq7" label="Vite advisory GHSA-p4f5-76q4-ffq7: Remote code execution using the __vite-browser-external virtual module" >}}
- {{< source href="https://vite.dev/config/server-options" label="Vite docs: Server options (server.host and server.allowedHosts)" >}}
- {{< source href="https://github.com/vitejs/vite/releases" label="Vite releases on GitHub" >}}
- {{< source href="https://www.npmjs.com/package/vite?activeTab=versions" label="vite on npm: versions" >}}
- {{< source href="https://github.com/vitejs/vite/security/advisories" label="Vite security advisories list" >}}
