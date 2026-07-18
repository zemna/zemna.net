---
title: "Treat frontend file watching as a maintenance contract"
description: "A dev server that misses filesystem events is an unreliable feedback loop. Build proof for the path from edit to browser, then keep a rollback ready."
date: 2026-07-18T07:00:00+07:00
draft: false
slug: frontend-file-watch-reliability
topics: ["frontend-engineering"]
tags: ["vite", "chokidar", "file-watching", "developer-experience", "docker", "wsl2", "frontend-maintenance"]
cover: /covers/frontend-file-watch-reliability.png
seo:
  primaryQuery: "Vite file watching reliability"
  secondaryQueries:
    - "Vite usePolling WSL2"
    - "Chokidar watcher test"
    - "Docker bind mount frontend development"
---

A dev server that misses filesystem events is not a frontend nuisance. It is an unreliable feedback loop.

The visible symptom looks small: a component changes on disk and the browser does not update. The operational cost is larger. A developer edits again, refreshes manually, restarts the server, doubts the CSS, then doubts the build. The system has stopped giving a trustworthy answer to a simple question: “did the change I made reach the page I am looking at?”

That question crosses several boundaries. An editor writes a file. The filesystem exposes an event. A watcher receives it. Vite decides whether the module belongs in its graph. The dev server sends an HMR message or invalidates a resource. The browser receives it and renders the new state. A failure anywhere in that chain can look identical from the desk chair.

Treat that chain as a maintenance contract. Define the paths that must work, create a small test fixture, collect evidence at each boundary, and retain a rollback that returns the team to a known state. This is less glamorous than tuning a component library. It saves time precisely because it removes the ritual of random restarts.

![Edit-to-browser feedback loop](/img/frontend-file-watch-reliability-1.png)

## The contract starts with a precise failure statement

“Hot reload is broken” does not tell an operator what to test. A usable statement names the writer, the watched path, the process that should observe the change, and the browser result that counts as success.

For example:

> When a Linux editor saves `src/watch-fixture.ts` inside the frontend project, the watcher emits an `add` or `change` event for that exact path, Vite logs its update activity, and the open page displays the new marker without a full-page manual refresh.

That statement is deliberately narrow. It does not claim that every editor, mount, generated file, or browser extension behaves the same way. It gives you one deterministic route through the system. Once that route works, add the routes that reflect actual team work: a file saved by the editor used by the team, a file changed through a container bind mount, a Vue single-file component, a CSS asset, and a deletion or rename.

The contract should separate three classes of failure.

| Layer | Question to answer | Evidence that counts | Common wrong reaction |
| --- | --- | --- | --- |
| Write | Did the expected file change at the expected path? | A new marker in the file and a fresh modification timestamp | Changing a different copy of the project |
| Observe | Did the watcher emit a matching event? | Watcher output containing the absolute or normalized path | Restarting Vite without testing events |
| Deliver | Did the dev server and browser apply the change? | Vite output plus a visible browser marker or network evidence | Assuming every event means successful HMR |
| Recover | Can the known configuration be restored? | A committed config, documented command, and repeatable test | Editing config repeatedly with no baseline |

A contract also needs a time boundary, but do not turn it into a published performance claim. Pick a local acceptance window for the team, such as “the marker is visible before the operator performs another action.” Record observed durations during diagnosis if they help distinguish a lost event from a delayed event. Do not promise a number that your environment has not measured.

The important distinction is event absence versus event delay. If a probe sees no event after a controlled save, investigate the filesystem and the watcher path. If the probe sees the event but the page remains old, investigate Vite’s graph, HMR transport, asset handling, or browser state. That split prevents a storage problem from being disguised as a frontend problem.

## Make the edit-to-event proof independent of Vite

A dev server has several jobs. Do not use it as the only instrument for diagnosing a watcher. Start with a small watcher that observes one file and prints the events it receives. Chokidar is the relevant baseline for Vite’s `server.watch` options because Vite forwards those watcher options to Chokidar. [Vite’s server options](https://vite.dev/config/server-options) document that relationship directly.

Install the probe dependency only in a project that already manages Node dependencies. The command below writes no application source and keeps the dependency explicit:

```bash
npm install --save-dev chokidar
node scripts/watch-probe.mjs src/watch-fixture.ts
```

Create `scripts/watch-probe.mjs` with the following code. It watches the path supplied on the command line, prints a ready signal, and exits cleanly when interrupted. It does not modify the watched file.

```js
// scripts/watch-probe.mjs
import chokidar from 'chokidar'
import path from 'node:path'

const target = process.argv[2]

if (!target) {
  console.error('Usage: node scripts/watch-probe.mjs <path>')
  process.exit(1)
}

const resolvedTarget = path.resolve(target)
const watcher = chokidar.watch(resolvedTarget, {
  ignoreInitial: true,
  persistent: true,
})

watcher
  .on('ready', () => console.log(`READY ${resolvedTarget}`))
  .on('all', (event, filePath) => console.log(`${event.toUpperCase()} ${filePath}`))
  .on('error', (error) => console.error(`WATCH_ERROR ${error.message}`))

async function close() {
  await watcher.close()
  process.exit(0)
}

process.on('SIGINT', close)
process.on('SIGTERM', close)
```

Open a second terminal and make a controlled, observable edit. This Python snippet changes only the designated fixture by appending a marker that includes the current UTC timestamp. It is suitable for a disposable fixture, not for a source file whose content matters.

```python
# scripts/touch-watch-fixture.py
from datetime import datetime, timezone
from pathlib import Path

fixture = Path('src/watch-fixture.ts')
marker = datetime.now(timezone.utc).isoformat()
fixture.write_text(
    f"export const watchFixture = '{marker}'\n",
    encoding='utf-8',
)
print(f"WROTE {fixture.resolve()} {marker}")
```

Run it with:

```bash
python3 scripts/touch-watch-fixture.py
```

The probe result gives a clean decision point. `WROTE` followed by `CHANGE` for the same resolved target proves that the write crossed into the watcher. `WROTE` without an event tells you not to spend the next hour changing HMR settings. Check the project path, process location, editor location, mount topology, and watcher mode first.

Chokidar documents `usePolling` as false by default. Its polling mode uses `fs.watchFile`, and the project notes that polling is sometimes necessary on network filesystems or other nonstandard situations. It also documents `CHOKIDAR_USEPOLLING` and `CHOKIDAR_INTERVAL`; the default interval is 100 ms. Those are configuration facts, not permission to enable polling everywhere. Source: [Chokidar README](https://github.com/paulmillr/chokidar).

Keep the probe in the repository or in a documented maintenance folder. A one-time shell command pasted into a chat vanishes just when a new laptop or a new container image recreates the problem.

![Native events versus documented polling decision](/img/frontend-file-watch-reliability-2.png)

## Turn Vite settings into an explicit operating choice

Once the standalone probe establishes whether events arrive, configure Vite for the actual topology. Vite passes `server.watch` settings to Chokidar. The default is not “use polling.” An explicit configuration should say which path the team supports and why.

For a project edited by processes in the same normal filesystem environment as the Vite process, keep the setting minimal:

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    watch: {
      ignored: ['**/.git/**', '**/node_modules/**'],
    },
  },
})
```

This does not claim that an ignore list fixes missed events. It makes the intended scope readable and avoids accidental observation of obvious large directories. Vite already skips several directories by default, including `.git/`, `node_modules/`, test results, its cache directory, and its build output directory. Do not override defaults until a test shows a reason.

For a WSL2 route where files are edited by Windows applications, or where Docker runs with a WSL2 backend, Vite documents a known filesystem watching limitation. Its recommended path is to use WSL2 applications for editing and to move the project outside the Windows filesystem. Vite also documents `{ usePolling: true }` as an alternative and warns that polling leads to high CPU utilization.

If the project must use that alternative, make it visible and reversible:

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const usePolling = process.env.VITE_USE_POLLING === 'true'

export default defineConfig({
  plugins: [vue()],
  server: {
    watch: usePolling
      ? { usePolling: true, interval: 300 }
      : undefined,
  },
})
```

This example does not assert that 300 ms is optimal. It provides a deliberate local value that an operator can test, record, and change through an environment variable. A team can run the normal route by default and turn on polling only for the affected topology:

```bash
VITE_USE_POLLING=true npm run dev
```

The rollback is equally explicit:

```bash
VITE_USE_POLLING=false npm run dev
```

Do not hide `usePolling` behind an unlabelled condition that detects an operating system. The problem is not an operating-system brand. The problem is whether the writer’s filesystem events reliably reach the watcher. An editor, project directory, Docker Desktop configuration, and process placement together define that route.

Vite’s documentation also says that setting `server.watch` to `null` disables file watching. That option has a legitimate place in a controlled environment where automatic updates are intentionally absent. It is not a repair for an unreliable loop. Disabling observation turns uncertainty into a known absence; it does not restore feedback.

## Test the complete route, including assets and the browser

A watcher event alone is not the product of development. A browser update alone is not enough evidence either, because a manual refresh, a cached resource, or a separate server can produce a convincing but misleading result. Run a small matrix that checks the full route.

Use a fixture import in a page that has no production importance. The module below gives the page a visible token. It is intentionally plain TypeScript so the first test does not depend on a component compiler.

```ts
// src/watch-fixture.ts
export const watchFixture = 'initial-marker'
```

Then render it in a development-only location, such as a diagnostics route guarded from production navigation:

```vue
<script setup lang="ts">
import { watchFixture } from './watch-fixture'
</script>

<template>
  <output data-testid="watch-fixture">{{ watchFixture }}</output>
</template>
```

The operator workflow is simple:

1. Start the standalone probe and wait for its `READY` line.
2. Start the Vite dev server with its output retained in a terminal or log pane.
3. Open the diagnostics route and note the initial marker.
4. Run the fixture writer once.
5. Confirm the probe printed the event for the fixture.
6. Confirm Vite reported the relevant file update, if its log format exposes it.
7. Confirm the marker in the already-open page changed before any manual browser action.
8. Record pass or fail against the exact route: editor/process, project path, container state, environment variables, and browser.

For asset behavior, repeat the test with a small imported CSS file or a source-controlled image fixture. Do not overwrite a shared logo or a generated asset to test the chain. The test should be safe to run on a branch and easy to revert with `git restore`.

The test needs one negative case. Stop the probe, edit the fixture, and verify that the absence of a running probe produces no false success record. Then restore it. This confirms that the test operator is reading the instrument rather than merely seeing familiar terminal noise.

A browser check should remain visible to a human, even if you later add automation. A data attribute and changing marker are stronger evidence than a subjective glance at a layout. If browser automation is available in your stack, assert the `data-testid` text after the controlled write. Keep the terminal evidence in the failure report, because browser automation cannot explain a missing filesystem event.

{{< note >}}
A full-page reload is not the acceptance condition for an HMR check. It can prove that the browser can fetch current files, while concealing a failed event-to-HMR path. Record it separately when it is useful.
{{< /note >}}

## Bind mounts are a topology, not an explanation

Docker bind mounts are useful because they make a host file or directory available inside a container. Docker documents bind mounts for sharing source code or build artifacts between a host development environment and a container. That fact tells you where to inspect first: the host path, the container target path, and the process that watches inside the container.

It does not prove any watcher behavior by itself. Do not turn “we use a bind mount” into an explanation for missed events without the probe evidence.

A small Compose example makes the mapping inspectable:

```yaml
services:
  frontend:
    image: node:lts
    working_dir: /app
    volumes:
      - type: bind
        source: .
        target: /app
    command: npm run dev -- --host 0.0.0.0
```

For a running container, inspect the mount rather than trusting the Compose file you intended to run:

```bash
docker inspect frontend --format '{{range .Mounts}}{{println .Type .Source "->" .Destination}}{{end}}'
```

The command exposes the daemon’s source and destination paths. Docker notes that bind mounts are created on the Docker daemon host, not on the client. It also notes that Docker Desktop runs the daemon inside a Linux VM and provides mechanisms for sharing native host paths. Those are reasons to capture the actual mount mapping in an incident note instead of assuming the path on one screen is the path watched by the process.

Docker documentation also warns that a bind mount can obscure existing files at its destination. That matters during diagnosis. If the container image contains a working `node_modules` directory but a bind mount overlays `/app`, the effective tree can differ from the image’s tree. Do not infer the source of a loaded module from the Dockerfile alone. Inspect the running container and the watched path.

{{< field-note >}}
For a Laravel/Vue SaaS, make this contract part of ordinary maintenance. Test a Vue module served through Vite, a Blade or Inertia entry point that imports it, and one asset route used by the local application shell. Keep the diagnostic fixture outside billing, auth, and customer workflows. The goal is not to test Laravel business logic; it is to prove that the frontend feedback path remains trustworthy while the application is maintained. See also [Laravel/Vue SaaS](/laravel-vue-saas/) for the broader application-maintenance context.
{{< /field-note >}}

![Proof artifacts for the frontend feedback loop](/img/frontend-file-watch-reliability-3.png)

## Operate changes with evidence and a rollback

Polling is an operational change. So is moving a project directory, changing an editor’s execution context, altering a bind mount, or upgrading a container base image. Treat each change as a small release with a before state, an acceptance test, and a rollback command.

A practical change record fits in a pull request description or maintenance note:

- **Problem route:** state the editor/process, project location, Vite process location, and whether a container is involved.
- **Baseline evidence:** attach or quote the probe result and browser marker result before the change.
- **Change:** name the config line, environment variable, or directory move.
- **Acceptance:** list the exact fixture test and all required evidence.
- **Rollback:** name the commit, environment variable, or prior configuration that restores the baseline.
- **Owner and review date:** assign a person or team and a date to remove temporary workarounds when the topology changes.

This record prevents a common maintenance trap: polling remains enabled forever because nobody remembers why it entered the configuration. An explicit `VITE_USE_POLLING` switch gives the team a direct test. Run the normal mode and polling mode against the same fixture. If both pass after a project move or editor change, remove the workaround through review rather than leaving it as folklore.

Do not couple the watcher change to a broad frontend cleanup. A refactor, new dependency, Docker image update, and polling configuration in one pull request create too many moving pieces when the browser stops updating. Keep the first repair narrow. Follow-up cleanup can be separate once the feedback loop has evidence behind it.

Internal documentation deserves the same restraint. The [developer tools hub](/developer-tools/) is a useful place to connect this check to local setup, scripts, and troubleshooting standards. A [start here guide](/start-here/) can tell new contributors where the diagnostic route and maintenance notes live. Neither page needs a grand claim. They should tell a developer what to run and what a passing result looks like.

## What you should do Monday morning

1. Choose one disposable TypeScript or Vue fixture in the frontend project and place a visible marker on a diagnostics route.
2. Add the Node watcher probe and run it against the fixture from the same environment that runs Vite.
3. Make one controlled write with the fixture script. Save the probe output, Vite output, and browser marker result in the issue or pull request.
4. If the probe receives no event, map the writer and watcher paths before touching HMR settings. For container work, inspect the running bind mount.
5. If the probe receives the event but the page stays old, inspect Vite’s module path, HMR connection, and browser state. Keep this as a delivery-layer investigation.
6. On WSL2 routes affected by edits from Windows applications or Docker with a WSL2 backend, prefer the Vite-documented route: edit with WSL applications and keep the project outside the Windows filesystem. Use polling only when the team has tested that route and accepts its CPU cost.
7. Put any polling switch behind an explicit environment variable, document the rollback command, and schedule a re-test when the editor, filesystem location, or container topology changes.

The maintenance target is plain: a controlled edit produces a traceable event and a visible browser result. When that target fails, the evidence tells you where to work. When it passes, developers can trust the loop again.

### Further reading

- [Vite server options: `server.watch`](https://vite.dev/config/server-options)
- [Chokidar README](https://github.com/paulmillr/chokidar)
- [Docker bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)
