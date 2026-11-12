---
title: "Node.js Security Fixes Are Out: Is Every Place You Run Node Past the Fix?"
date: 2026-11-10T06:00:00+07:00
lastmod: 2026-11-12T08:20:00+07:00
draft: false
slug: "node-patch-day-where-your-version-lives"
description: "Node.js shipped security releases for lines 22, 24 and 26 on Nov 11, 2026. What the advisory lists, which parts matter for your setup, and a check for every place Node hides."
topics: ["backend"]
tags: ["nodejs", "security-releases", "docker", "github-actions", "cloudflare-pages", "patch-management", "agent-ops"]
cover: /covers/node-patch-day-where-your-version-lives.png
seo:
  primaryQuery: "Node.js security release November 11 2026"
  secondaryQueries:
    - "Node.js 22.23.5 24.22.3 26.13.1 security fixes"
    - "which Node.js version am I running in Docker and CI"
    - "how to pin Node version .nvmrc Dockerfile GitHub Actions"
---

On Wednesday, Node.js shipped the security fixes it had announced. The page that listed nothing on Tuesday now lists them all.

So the question in your team chat has changed. It is no longer "What will they fix?" It is "Are we affected?", and the honest first answer is still a question back: "Which Node, and where?"

This post began on Nov 10 as a way to answer that before the details landed. Now I have added what the advisory lists and a check against the fixed versions. The question is not whether Node patched it. It is whether every place you run Node got the patch.

<!--more-->

{{< note type="note" title="Refreshed on 2026-11-12" >}}
Written on Nov 10, before the release. New today: the next two sections, one on what the advisory lists and one on a version-floor check. Everything after them is the original list-making advice, and it still holds. "Wednesday" there means Nov 11.
{{< /note >}}

## What the advisory lists now

I re-read the advisory page live on Nov 12 at about 08:00 Jakarta time. Under Downloads it names three fixed versions: **22.23.5, 24.22.3 and 26.13.1**. It says the highest severity fixed in each line is HIGH.

It lists 16 CVEs: 7 high, 6 medium and 3 low. The release notes for 24.22.3 add one more low item, CVE-2026-123873, which the advisory page does not list. So "16" means what the advisory page lists, not a final count. The release also updates llhttp, undici and sqlite.

Here are the seven HIGH items in plain words, from the page's own descriptions:

| Part of Node | What the page says can happen | Lines |
|---|---|---|
| HTTP/2 server | Teardown trips an assertion and kills the process (CVE-2026-123863) | 24, 26 |
| HTTPS server | A zero-length TLS write can leak memory of other connections; plain `node:http` is not affected (CVE-2026-123864) | 22, 24, 26 |
| HTTP/2 server | Sessions are never cleaned up after a protocol error, leaking memory and file descriptors (CVE-2026-123865) | 22, 24, 26 |
| HTTP/2 server | Freed response memory can be sent to a peer (CVE-2026-123866) | 22, 24, 26 |
| TLS server | Remote crash when the server uses `SNICallback`, `OCSPRequest`, `newSession`, `resumeSession` or `addContext` (CVE-2026-126051) | 24, 26 |
| TLS 1.2 | A client can change the servername on renegotiation and bypass a per-host client-certificate policy (CVE-2026-123872) | 22, 24, 26 |
| HTTP/2 file serving | Memory corruption when a `respondWithFile()` stream is reset (CVE-2026-123874) | 24, 26 |

The page words every impact line as "affects all users in active release lines", and then describes triggers, such as a handler that responds before the request body ends. I read that as: patch every listed line, and use the trigger only to decide the order.

All seven describe Node answering network requests as an HTTP/2, HTTPS or TLS server. None describes a build step. **My inference, not the page's:** if Node only compiles your CSS and JavaScript in CI, these seven are not a hole in your build, though the host should still move. First in line are servers where Node itself terminates TLS or HTTP/2: server-side rendering, or a bare Express or Fastify server over HTTPS. Node behind nginx or Cloudflare comes next.

One medium item is for CI and agent hosts. CVE-2026-123871: an invalid proxy setting can print the raw proxy URL, credentials included, in an `ERR_PROXY_INVALID_CONFIG` message, which then lands in `stderr`, container logs or crash reports.

## Check a version against the fix

A list of versions is only useful if something compares it with the fix. This script says which versions are at or above the fixed version for their line. It judges only exact `x.y.z` values, because `lts` or `22` can mean anything, and it exits 1 if any value is behind, so a CI step can fail on it.

```python
#!/usr/bin/env python3
"""Compare Node.js versions with the Nov 11, 2026 security-release floors.
Usage: node_fix_floor.py VERSION [VERSION ...]    e.g. v26.12.1 24.22.3 lts
Exit 0 = every version is at or above its line's fix.
Exit 1 = at least one is behind, unfixed, or cannot be judged.
Exit 2 = no input."""
import re
import sys

# From the "Downloads" list on the advisory page.
FIXED = {22: (22, 23, 5), 24: (24, 22, 3), 26: (26, 13, 1)}


def judge(raw):
    text = raw.strip()
    m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", text)
    if not m:
        return False, "cannot judge: not an exact x.y.z (a floating tag or a line)"
    ver = tuple(int(part) for part in m.groups())
    line = ver[0]
    if line in FIXED:
        floor = FIXED[line]
        want = ".".join(map(str, floor))
        if ver >= floor:
            return True, f"ok: at or above {want}"
        return False, f"BEHIND: the fix for line {line} is {want}"
    if line > 26:
        return False, "cannot judge: newer than the lines on this list, read its notes"
    return False, "NO FIX on this list: not one of the lines 22/24/26"


def main(argv):
    if len(argv) < 2:
        print("give at least one version", file=sys.stderr)
        return 2
    worst = 0
    for raw in argv[1:]:
        good, why = judge(raw)
        print(f"{raw:<12} {why}")
        if not good:
            worst = 1
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

I ran it on a mix of inputs:

| Input | What it printed |
|---|---|
| `v26.12.1` | BEHIND: the fix for line 26 is 26.13.1 |
| `26.13.1` | ok: at or above 26.13.1 |
| `24.22.2` | BEHIND: the fix for line 24 is 24.22.3 |
| `22.23.4` | BEHIND: the fix for line 22 is 22.23.5 |
| `20.19.0` | NO FIX on this list: not one of the lines 22/24/26 |
| `lts` | cannot judge: not an exact x.y.z |

With `v26.13.1` and `24.22.3` the exit code was 0. With no input it exits 2. To make a job fail when its Node is behind, add one step after setup:

```yaml
      - name: Fail if this job's Node is behind the Nov 11 fix
        run: python3 tools/node_fix_floor.py "$(node -p process.version)"
```

The floor moves with every security release, so keep the file in a repository with an owner.

## Where my own list stands this morning

- **My agent host.** `node -p process.version` printed `v26.12.1`. The script says BEHIND, because the 26 line's fix is 26.13.1. The host reported the same value on Nov 10. It has not moved; the target did.
- **Cloudflare Pages.** The build image page, read live, was last updated Oct 26 and still lists 22.23.4 as the default Node, one patch below 22.23.5. I do not know when the default moves. If you want to decide, set `NODE_VERSION` yourself.
- **Docker Hub.** The Docker Official Image tags `22`, `24`, `26` and `lts` show updates between Nov 11 19:25 UTC and Nov 12 00:56 UTC. I did not pull them. A new base image does not change your image: it gets the fix only when you rebuild with a fresh pull.

## What the page said on Nov 10, before the release

On Nov 10 the page named three lines, gave HIGH as the ceiling, and had an empty list. One sentence on it still matters: "End-of-Life versions are always affected when a security release occurs."

A "release line" is the number before the first dot: Node 22 is one line, 22.23.4 one version inside it. The schedule, from `nodejs/Release` on Nov 10:

| Line | Status on Nov 10, 2026 | In the Nov 11 release? | Support ends |
|---|---|---|---|
| 26 (Lithium) | LTS since 2026-10-28 | Yes | 2029-04-30 |
| 24 (Krypton) | Maintenance LTS since 2026-10-20 | Yes | 2028-04-30 |
| 22 (Jod) | Maintenance LTS | Yes | 2027-04-30 |
| 25 | End-of-Life | No, but always affected | ended 2026-06-01 |
| 20 (Iron) | End-of-Life | No, but always affected | ended 2026-04-30 |

LTS means long-term support, the lines meant for production. Maintenance LTS gets fixes but no new features. End-of-Life means no more releases.

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

My own agent host was one of those rows, and its reading is in the section above.

The repository for this very site has no `.nvmrc` and no `package.json`, because Hugo builds it. "Not here" is a finding worth writing down. Silence is not.

![Five places a Node version lives, each with how to read it and a blank owner line](/img/node-patch-day-where-your-version-lives-2.png)

## Step one: read the files

Files tell you what a human asked for, and they are the cheapest thing to scan. This script walks a repository and lists every place that names a Node version: `.nvmrc`, `.node-version`, `package.json`, `Dockerfile`, compose files and GitHub workflows. For each hit it says which release line the value belongs to and whether that line is in the Nov 11 release.

It uses only the Python standard library and fails closed: a folder it cannot read exits with code 3 instead of printing a calm, empty report.

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

Eight rows, and the fixture is tiny. In a real repository the CI file, the Dockerfile and the pin file will not agree with each other. That is the finding. On this site's repository it printed "NO NODE PINS FOUND" and a warning that this is not the same as safe.

## Step two: ask the running thing, not the file

A file says what someone wanted. Only the running process says what it got. On any machine where a person or an agent runs commands, three lines tell you the truth:

```bash
node -p "process.version"      # the Node on this machine, right now
which node                     # which copy, in case there are two
echo "${NODE_VERSION:-unset}"  # some platforms read this variable
```

In CI, make the job say out loud which Node it got. This setup step reads the version from the same file your laptop uses and prints the answer into the log:

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

I parse-checked that YAML with a YAML library. I did not run it on GitHub. By the `actions/setup-node` documentation, `check-latest` defaults to `false`: the action takes a match from the runner's cache first, so an older patch inside your line can survive a release. `check-latest: true` makes it confirm the cached copy is the newest first, which is slower.

For Docker, name the line and rebuild with a fresh pull:

```dockerfile
# Name the line you chose on purpose, not "lts".
FROM node:24-trixie-slim
RUN node -p "'built with node ' + process.version"
```

```bash
docker build --pull --no-cache -t myapp:node-patch .
```

`--pull` always tries to fetch a newer base image, and `--no-cache` stops Docker reusing an old layer. Pin the line, not the patch: a pin to one exact patch is out of date at the next release. The line, a rebuild habit and a log line that prints the version are less to maintain.

![The file says what you asked for; the running process says what you got](/img/node-patch-day-where-your-version-lives-3.png)

## Floating names move without asking you

`lts`, `latest` and `current` look like pins and are moving labels.

On Nov 10 the Docker Official Image docs put the tags `26`, `current`, `latest`, `lithium`, `lts` and `lts-lithium` on the same build of the 26 line. Since 26 became LTS on 2026-10-28, an image built from `node:lts` in September and one built this week can be different majors. Nobody edited the Dockerfile. The label moved.

Cloudflare Pages does it quietly: unless you set `NODE_VERSION` or a pin file, its default Node "may be updated to the latest available minor version without notice". On Nov 10 the same page said the v3 system does not read `engines` in `package.json`, so that row in the scanner table above means nothing there.

## The loud part is the old lines

The release names three lines. Your problem is more likely a fourth.

Node 20 reached End-of-Life on 2026-04-30 and Node 25 on 2026-06-01. The announcement says End-of-Life versions are always affected, and no fix is coming for them. In the fixture above, two of eight rows are on an End-of-Life line. I expect the old line to hide where nobody looks: a worker container, a one-off script image, a CI job added for one release. The fix is a move to a supported line, a planned task with an owner.

{{< field-note title="Field note" >}}
On the Laravel and Vue projects I look after, Node does the front-end build and nothing else. It sits in the CI job that compiles the front end, in the Docker stage that copies the result, and on whatever laptop ran the build last. Because it never serves a request, nobody puts it on the patch list. The PHP version has an owner. The database has an owner. The Node that has deploy credentials in reach during the build often has neither. The question is not whether the fix is easy to apply. It is whether the person applying it knows every place it has to go.
{{< /field-note >}}

## What this connects to

Same habit as [A Red Fork PR on Nov 9 or 16 May Be a GitHub Rehearsal, Not Your Bug](/blog/red-fork-pr-github-rehearsal-pull-request-target/) (workflows with an owner) and [Your Overnight Agent Job Has a Login With an End Date](/blog/agent-job-login-has-an-end-date/) (jobs with a date), here for the runtime. [A Package Cooldown Also Delays Your Security Fix](/blog/package-cooldown-delays-your-security-fix/) is the package-side twin. [Long-Running AI Agents: From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/) covers the agent side. More notes of this kind are on [AI Agent Operations](/ai-agent-operations/) and [Developer Tools](/developer-tools/), and [Start Here](/start-here/) lists the reading order.

## What I did and did not verify

On 2026-11-12 at about 08:00 Jakarta time I read the advisory page and the 24.22.3 release notes live. I also read `nodejs.org/dist/index.json` (it lists 26.13.1, 24.22.3 and 22.23.5 as the newest of their lines), Cloudflare's build image page, and the Docker Hub tag records for `22`, `24`, `26` and `lts` (update times only). I did not open the notes for 22.23.5 or 26.13.1, so the CVE-to-line mapping comes from the advisory page alone.

I ran the floor script on the inputs shown and on my own host. On Nov 10 I ran the scanner on a fixture, an empty folder, a missing path (exit code 3) and this site's repository. I did not pull any Docker image, run the CI step on GitHub, or test any CVE. Re-read the sources before you act, because a later release can move the floors.

## What you should do Monday morning

These fit in one sitting, whatever day you read this.

1. **Run the floor check on every row of your list:** `python3 node_fix_floor.py "$(node -p process.version)"`.
2. **Patch in this order:** servers where Node terminates TLS or HTTP/2, Node behind a proxy, CI runners and agent hosts, then laptops.
3. **Rebuild Docker images with `--pull --no-cache`** and make the build print `process.version`.
4. **Write next to each row** whether Node answers network requests there or only builds assets.
5. **Move every End-of-Life line** (Node 20, Node 25) to a supported one, with an owner and a date.
6. **Replace floating names** (`lts`, `latest`, `current`) with a named line, and set `NODE_VERSION` on your build platform.
7. **Put one name next to each row,** one person, not a team.

## Further reading

- {{< source href="https://nodejs.org/en/blog/vulnerability/november-2026-security-releases" label="Node.js: Wednesday, November 11, 2026 Security Releases" >}}
- {{< source href="https://nodejs.org/en/blog/release/v24.22.3/" label="Node.js 24.22.3 (LTS) release notes" >}}
- {{< source href="https://github.com/nodejs/Release#release-schedule" label="Node.js Release Working Group: release schedule" >}}
- {{< source href="https://developers.cloudflare.com/pages/configuration/build-image/" label="Cloudflare Pages: Build image" >}}
- {{< source href="https://github.com/actions/setup-node" label="actions/setup-node README" >}}
- {{< source href="https://github.com/docker-library/docs/tree/master/node" label="Docker Official Image: node" >}}
