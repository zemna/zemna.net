---
title: "Node.js Patch Day Is Wednesday: Write Down Where Your Version Lives Before You Know the CVEs"
date: 2026-11-10T06:00:00+07:00
draft: false
slug: "node-patch-day-where-your-version-lives"
description: "Node.js ships security releases on or shortly after Wednesday, Nov 11, and the page lists no CVEs yet. Find every place your Node version hides and name who patches each one."
topics: ["backend"]
tags: ["nodejs", "security-releases", "docker", "github-actions", "cloudflare-pages", "patch-management", "agent-ops"]
cover: /covers/node-patch-day-where-your-version-lives.png
seo:
  primaryQuery: "Node.js security release November 11 2026"
  secondaryQueries:
    - "which Node.js version am I running in Docker and CI"
    - "Node.js 22 24 26 security release affected versions"
    - "how to pin Node version .nvmrc Dockerfile GitHub Actions"
---

Node.js plans to ship security fixes on or shortly after tomorrow, and nobody outside the project knows yet what they fix.

That is the whole announcement. The Node.js project says new versions of three release lines will come out on or shortly after Wednesday, November 11, 2026. The highest severity is HIGH in each of the three lines. The sentence that should list the issues ends with a colon and then nothing. I read the page live at about 08:00 Jakarta time this morning, and the list was still empty.

So here is the question you will get in your team chat on Wednesday: "Are we affected?" The honest first answer is not yes or no. It is a question back: "Which Node?"

If you cannot answer that in one minute, today is the day to fix it. You do not need the CVE details for this part. You need a list of the places where Node runs and a name next to each one. When the details land, you read them against a list instead of against your memory.

<!--more-->

## What Node.js actually said

Here is everything the announcement page says, and I will not add to it.

The project will release new versions of the 26.x, 24.x and 22.x lines on or shortly after Wednesday, November 11, 2026. The highest severity fixed is HIGH, and it says so separately for each of the three lines. It also says: "End-of-Life versions are always affected when a security release occurs." There is no CVE list, no description of the bug and no hour of the day.

A "release line" is the number before the first dot. Node 22 is one line, and 22.23.4 is one version inside it. Node.js publishes a schedule that says which lines are supported. I read it today from the project's `nodejs/Release` repository:

| Line | Status on Nov 10, 2026 | On Wednesday's list? | Support ends |
|---|---|---|---|
| 26 (Lithium) | LTS since 2026-10-28 | Yes | 2029-04-30 |
| 24 (Krypton) | Maintenance LTS since 2026-10-20 | Yes | 2028-04-30 |
| 22 (Jod) | Maintenance LTS | Yes | 2027-04-30 |
| 25 | End-of-Life | No, but always affected | ended 2026-06-01 |
| 20 (Iron) | End-of-Life | No, but always affected | ended 2026-04-30 |

LTS means long-term support, the lines meant to run in production. Maintenance LTS is the later stage where a line gets fixes but no new features. End-of-Life means the project no longer releases for it. If any of your servers still run Node 20 or Node 25, the announcement's own sentence applies to them. Wednesday's list does not name them, and they are affected anyway.

![Release lines: 26, 24 and 22 are on the list; 25 and 20 are End-of-Life and affected anyway](/img/node-patch-day-where-your-version-lives-1.png)

## Five places a Node version hides

Ask a team "which Node do you run?" and you usually get one answer. The honest answer is often five.

| Place | How to read it | The trap |
|---|---|---|
| Your laptop | `node -v` | It is the one you tested on, so it feels like the answer |
| The CI runner | the setup step in the workflow file | The file says what you asked for, not what the runner had cached |
| The Docker image | the `FROM node:` line | A tag like `lts` moves without a commit |
| The build platform | its dashboard or a pin file | You never installed it, so you never looked |
| The machine your coding agent runs on | `node -v` in that shell | Nobody put it on any list |

The last row is the one I want you to look at. A coding agent runs shell commands, and shell commands call whatever `node` is on the path. Nobody chose that Node. It came with the host.

I checked mine this morning. The machine that runs my own agent jobs reports `v26.12.1`. The 26 line is on Wednesday's list, and the newest 26 on nodejs.org is `26.13.0`, released on 2026-10-28, so this host is one minor version behind. I had not written that down anywhere until now.

The repository for this very site has no `.nvmrc` and no `package.json`. Hugo builds it, and no file in the repository asks for Node. That is also an answer, and it is worth writing down: "not here" is a finding. Silence is not.

![Five places a Node version lives, each with how to read it and a blank owner line](/img/node-patch-day-where-your-version-lives-2.png)

## Step one: read the files

Files tell you what a human asked for. They are the cheapest thing to scan, so I scan them first. This script walks a repository and lists every place that names a Node version: `.nvmrc`, `.node-version`, `package.json`, `Dockerfile`, compose files and GitHub workflows. For each hit it says which release line the value belongs to and whether that line is on Wednesday's list.

It uses only the Python standard library. It reads nothing outside the folder you give it, and it fails closed: a folder it cannot read exits with code 3 instead of printing an empty, calm report.

```python
#!/usr/bin/env python3
"""List every place a repo names a Node.js version. Usage: find_node_pins.py PATH
Exit 3 = PATH unreadable. Finding nothing is NOT a clean result."""
import json
import os
import re
import sys

# Release lines, checked against nodejs/Release schedule.json on 2026-11-10.
# (status, on the Nov 11 security release list?)
LINES = {
    20: ("EOL since 2026-04-30", False),
    22: ("Maintenance LTS, EOL 2027-04-30", True),
    24: ("Maintenance LTS, EOL 2028-04-30", True),
    25: ("EOL since 2026-06-01", False),
    26: ("LTS, EOL 2029-04-30", True),
    27: ("alpha, not released", False),
}
CODENAMES = {"iron": 20, "jod": 22, "krypton": 24, "lithium": 26}
FLOATING = ("lts", "latest", "current", "node", "stable")
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "public", ".venv"}


def classify(spec):
    raw = spec.strip().strip("'\"")
    low = raw.lower()
    if not raw:
        return "empty", "read by a human"
    if "$" in raw or "{{" in raw:
        return "indirect", "value set elsewhere: follow it"
    if re.search(r"[<>^~|\s]", raw) and not low.startswith(("lts/", "lts-")):
        return "range", "range, not a pin: check what really runs"
    if low.startswith(FLOATING):
        return "floating", "moves when someone re-pulls or rebuilds"
    m = re.match(r"^v?(\d+)", low)
    if m:
        major = int(m.group(1))
    else:
        major = next((v for k, v in CODENAMES.items() if low.startswith(k)), None)
        if major is None:
            return "unknown", "read by a human"
    status, listed = LINES.get(major, ("older than 20", False))
    exact = bool(re.match(r"^v?\d+\.\d+\.\d+", low))
    kind = "exact patch" if exact else "line only"
    verdict = (
        "on Wednesday's list" if listed else "EOL: always affected, not on the list"
    )
    return f"{kind} (node {major}, {status})", verdict


def read_lines(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


def scan_file(path, rel):
    name = os.path.basename(path)
    out = []
    lines = read_lines(path)
    if name in (".nvmrc", ".node-version"):
        for i, ln in enumerate(lines, 1):
            if ln.strip():
                out.append((rel, i, name, ln.strip()))
                break
    elif name == "package.json":
        try:
            data = json.loads("\n".join(lines))
        except ValueError:
            out.append((rel, 1, "package.json", "UNREADABLE JSON"))
            return out
        eng = (data.get("engines") or {}).get("node")
        if eng:
            out.append((rel, 1, "engines.node", eng))
        vol = (data.get("volta") or {}).get("node")
        if vol:
            out.append((rel, 1, "volta.node", vol))
    elif name.lower().startswith("dockerfile") or name.lower().endswith(".dockerfile"):
        pat = re.compile(r"^\s*FROM\s+(?:--platform=\S+\s+)?node:(\S+)", re.I)
        for i, ln in enumerate(lines, 1):
            m = pat.match(ln)
            if m:
                out.append((rel, i, "FROM node:", m.group(1)))
    elif re.search(r"(^|/)(docker-)?compose[^/]*\.ya?ml$", rel):
        pat = re.compile(r"^\s*image:\s*['\"]?node:([^\s'\"#]+)")
        for i, ln in enumerate(lines, 1):
            m = pat.match(ln)
            if m:
                out.append((rel, i, "compose image: node:", m.group(1)))
    elif ".github/workflows/" in rel and name.endswith((".yml", ".yaml")):
        pat = re.compile(r"^\s*-?\s*(node-version(?:-file)?):\s*(.+?)\s*(?:#.*)?$")
        for i, ln in enumerate(lines, 1):
            m = pat.match(ln)
            if m:
                out.append((rel, i, m.group(1), m.group(2)))
    return out


def main(argv):
    if len(argv) != 2 or not os.path.isdir(argv[1]) or not os.access(argv[1], os.R_OK):
        print("ERROR: give a readable repo folder", file=sys.stderr)
        return 3
    root = argv[1]
    found = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            path = os.path.join(base, f)
            rel = os.path.relpath(path, root)
            try:
                found.extend(scan_file(path, rel))
            except OSError as exc:
                print(f"ERROR: cannot read {rel}: {exc}", file=sys.stderr)
                return 3
    if not found:
        print("NO NODE PINS FOUND. This is not 'safe'. The version comes from")
        print("somewhere this scan cannot see: host default, base image, laptop.")
        return 0
    print("| where | what | value | what it is | Wednesday |")
    print("|---|---|---|---|---|")
    for rel, line, what, value in sorted(found):
        kind, verdict = classify(value)
        if what == "node-version-file":
            kind, verdict = "points at a file", f"open {value.strip()} and read it too"
        print(f"| {rel}:{line} | {what} | `{value}` | {kind} | {verdict} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

I ran it on a fixture repository that I built to look like a small shop: an `.nvmrc`, a two-stage Dockerfile, a compose file, a `package.json` and a workflow. Here are the real rows it printed, trimmed to three columns:

| Where | Value | What the script said |
|---|---|---|
| `ci.yml:6` `node-version` | `24` | line only, on Wednesday's list |
| `ci.yml:11` `node-version-file` | `.nvmrc` | points at a file: open it and read it too |
| `ci.yml:16` `node-version` | `${{ matrix.node }}` | indirect: value set elsewhere, follow it |
| `.nvmrc:1` | `22` | line only, on Wednesday's list |
| `Dockerfile:1` `FROM node:` | `20-alpine` | Node 20, EOL: always affected, not on the list |
| `Dockerfile:5` `FROM node:` | `lts-trixie-slim` | floating: moves when someone re-pulls or rebuilds |
| `docker-compose.yml:3` | `25` | Node 25, EOL: always affected, not on the list |
| `package.json:1` `engines.node` | `>=18` | range, not a pin: check what really runs |

Eight rows, and the fixture is tiny. In a real repository the CI file, the Dockerfile and the pin file will not agree with each other. That is the finding. You do not have to fix anything yet. Just see it.

On this site's repository it printed "NO NODE PINS FOUND" and a warning that this is not the same as safe, which matches what I said above.

## Step two: ask the running thing, not the file

A file says what someone wanted. Only the running process says what it got. Files and reality drift apart, so check both before Wednesday.

On any machine where a person or an agent runs commands, three lines tell you the truth:

```bash
node -p "process.version"      # the Node on this machine, right now
which node                     # which copy, in case there are two
echo "${NODE_VERSION:-unset}"  # some platforms read this variable
```

In CI, make the job say out loud which Node it got. This is the setup step I would use. It reads the version from the same file your laptop uses, so there is one source of truth, and it prints the answer into the log:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc
          check-latest: true
      - name: Print the Node this job really got
        run: node -p "'node ' + process.version + ' on ' + process.platform"
```

I parse-checked that YAML with a YAML library. I did not run it on GitHub. Two details come from the `actions/setup-node` documentation. If you give both `node-version` and `node-version-file`, the action uses `node-version`. And `check-latest` defaults to `false`: the action first looks in the runner's local cache for a match and downloads a newer one only when the cache has nothing. By that description, an older cached patch inside your line can still be what the job uses after a patch release. `check-latest: true` makes the action confirm the cached copy is the newest first. The documentation notes that this is slower.

For Docker, name the line and rebuild with a fresh pull:

```dockerfile
# Name the line you chose on purpose, not "lts".
FROM node:24-trixie-slim
RUN node -p "'built with node ' + process.version"
```

```bash
docker build --pull --no-cache -t myapp:node-patch .
```

`--pull` tells Docker to always try to fetch a newer version of the base image, and `--no-cache` stops it reusing an old layer. I confirmed both flags in the `docker build --help` output on my host.

Pin the line, not the patch. A pin to one exact patch is out of date by the time Wednesday ends. The line you chose, plus a rebuild habit, plus a log line that prints the version, is a smaller thing to maintain.

![The file says what you asked for; the running process says what you got](/img/node-patch-day-where-your-version-lives-3.png)

## Floating names move without asking you

Some names look like pins and are not. `lts`, `latest` and `current` are moving labels.

The Docker Official Image documentation for `node` lists which tags point at which build. Today the tags `26`, `current`, `latest`, `lithium`, `lts` and `lts-lithium` all sit on the same Debian 13 build of the 26 line. By Node's own schedule, 26 became LTS on 2026-10-28, so an image built from `node:lts` in September and one built this week can be different major versions. Nobody edited the Dockerfile. The label moved.

Cloudflare Pages does the same thing in a quieter way. Its build image documentation (updated 2026-10-26) says the default Node.js in the v3 build image is 22.23.4, and you override it with a `NODE_VERSION` environment variable or with an `.nvmrc` or `.node-version` file. For minor versions of preinstalled software it says "May be updated to the latest available minor version without notice", and that applies if you have not overridden the default. It also says the v3 system does not detect the Node version from `package.json` `engines`. So the `engines` row in the table above is not read on that platform.

22.23.4 is also the newest version of the 22 line on nodejs.org today, released on 2026-10-20, so Cloudflare's default looks current right now. The point is not that it is old. The point is that the version lives in a place you did not write it, and someone else decides when it moves.

## The loud part is the old lines

Wednesday's list names three lines. Your problem is more likely a fourth.

Node 20 reached End-of-Life on 2026-04-30. Node 25 reached End-of-Life on 2026-06-01. The announcement says End-of-Life versions are always affected. When a security release happens, a line the project no longer touches is behind by definition.

In the fixture above, two of eight rows are on an End-of-Life line. In a real repository I expect the old line to hide in the places nobody opens: a worker container, a one-off script image, a CI job added for one release and never touched again. If you find one, the fix is a move to a supported line. It is a planned task with an owner, not a patch. Node 27 is an alpha, so it is not a place to hide from the list.

## What I would not do before the details land

- **Do not guess the CVEs.** The page lists none. Anything you read before Wednesday about what is fixed is a guess.
- **Do not let the coding agent "upgrade Node" in one file.** That fixes one of five places and makes the other four look fine. Ask for the diff against your list.

## Wednesday, once the notes appear

When the advisory text is published, read it with the list open and ask three things:

1. Which of my lines are fixed, and to which version?
2. What part of Node does each issue touch? Network code and file permissions are different risks from a rarely used built-in.
3. Is that part in a request path on one of my servers, or only in a build tool?

Question 3 matters most for a typical Laravel and Vue project, where Node does not serve a single request. It builds the assets. A build step still runs code with your deploy keys in reach, but this tells you the order in which to patch.

{{< field-note title="Field note" >}}
On the Laravel and Vue projects I look after, Node does the front-end build and nothing else. In a project like that, it sits in the CI job that compiles the front end, in the Docker stage that copies the result, and on whatever laptop ran the build last. Because it never serves a request, nobody puts it on the patch list. The PHP version has an owner. The database has an owner. The Node that has the deploy credentials in reach during the build often has neither. The question is not whether the fix is easy to apply. It is whether the person who applies it knows every place it has to go.
{{< /field-note >}}

## What this connects to

This is the same shape as my notes about rules that change on a date. In [A Red Fork PR on Nov 9 or 16 May Be a GitHub Rehearsal, Not Your Bug](/blog/red-fork-pr-github-rehearsal-pull-request-target/), the answer was a list of workflows with an owner for each. In [Your Overnight Agent Job Has a Login With an End Date](/blog/agent-job-login-has-an-end-date/), it was a list of jobs and the date each login stops working. This post is the same habit for the runtime itself.

It also pairs with [A Package Cooldown Also Delays Your Security Fix](/blog/package-cooldown-delays-your-security-fix/). A cooldown is a rule about packages. The runtime underneath is not a package in your lockfile, and a late runtime patch costs the same. [Long-Running AI Agents: From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/) covers the agent side: name the owner of everything the agent runs on. More notes of this kind are on [AI Agent Operations](/ai-agent-operations/) and [Developer Tools](/developer-tools/), and [Start Here](/start-here/) lists the order to read them.

## What I did and did not verify

On 2026-11-10 I read the Node.js announcement page for the November 11 security releases (scraped live), the `schedule.json` file in `nodejs/Release`, the release index at `nodejs.org/dist/index.json`, the Docker Official Image README for `node`, the Cloudflare Pages build image documentation, and the `actions/setup-node` README and advanced usage page. I also ran `node -p process.version` and `which node` on my own host and looked at this site's repository.

I ran the scanner on a fixture, on an empty folder, on a missing path (exit code 3) and on this site's repository. I parse-checked the workflow YAML but did not run it on GitHub, and I did not build the Docker image because the Docker daemon is not running on this host.

I do not know what Wednesday's issues are, which APIs they touch, or at what hour the releases will ship. The announcement says "on or shortly after". The release lines, dates and tag lists above can change after today, so re-read the sources before you act on this.

## What you should do Monday morning

These fit in one sitting before Wednesday's release. If you are reading this after it, do them first and then read the advisory.

1. **Make the list.** Five rows: laptop, CI, Docker, build platform, agent host. Add a row for every other place Node runs.
2. **Run the scanner on every repository you ship.** Copy its table into the list. Treat "no pins found" as "version comes from elsewhere", and go find where.
3. **Run the three lines on every host that runs commands**, including your coding agent's. Write the real answer next to the file's answer.
4. **Find every End-of-Life line.** Node 20 and Node 25 get a task with an owner and a date.
5. **Replace floating names** (`lts`, `latest`, `current`) with a named line, and make CI and the Docker build print the version.
6. **Check your build platform's default.** If you never set `NODE_VERSION` or a pin file, write down that the platform decides.
7. **Name one person per row who patches it.** One name, not a team.
8. **Tell your agent in writing** not to change a Node version in one file without showing the diff against the list.
9. **Open the advisory with the list next to it** when it lands on Wednesday.

## Further reading

- {{< source href="https://nodejs.org/en/blog/vulnerability/november-2026-security-releases" label="Node.js: Wednesday, November 11, 2026 Security Releases" >}}
- {{< source href="https://github.com/nodejs/Release#release-schedule" label="Node.js Release Working Group: release schedule" >}}
- {{< source href="https://developers.cloudflare.com/pages/configuration/build-image/" label="Cloudflare Pages: Build image" >}}
- {{< source href="https://github.com/actions/setup-node" label="actions/setup-node README" >}}
- {{< source href="https://github.com/docker-library/docs/tree/master/node" label="Docker Official Image: node" >}}
