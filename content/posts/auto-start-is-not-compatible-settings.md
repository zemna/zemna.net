---
title: "An Auto-Started Codex Background Server Is Not Compatible Settings"
date: 2026-09-28T07:00:00+07:00
draft: false
slug: "auto-start-is-not-compatible-settings"
description: "An auto-started Codex background server is not proof session settings match. Print auto-start, the recovery choice, and the named Codex owner before you file an all-clear."
topics: ["ai-agents"]
tags: ["codex", "background-server", "coding-agents", "change-control", "daemon-auto-start"]
cover: /covers/auto-start-is-not-compatible-settings.png
seo:
  primaryQuery: "Codex auto-start background server is not compatible settings"
  secondaryQueries:
    - "Codex daemon_auto_start default is not a settings match"
    - "Codex recovery choices when background server settings are incompatible"
    - "named owner for Codex background server sessions"
---

The junior pastes a terminal. `codex` opened. Chat is quiet. They file an all-clear: “the background server is compatible.”

I stop the run there. An auto-started Codex background server is not compatible settings. The public Codex CLI notes that named this field are blunt: automatic background-server startup is enabled for eligible interactive sessions, with recovery choices when server settings are incompatible. That is a launch path. It is not a signed match between this session and the shared server. [Source: https://github.com/openai/codex/releases/tag/rust-v0.157.0] [Source: https://github.com/openai/codex/pull/47318]

I already refused to treat a green wrangler deploy as an immediate Durable Object cutover in [A Green Wrangler Deploy Is Not an Immediate Durable Object Code Cutover](/blog/green-deploy-is-not-do-cutover/), a `/readyz` 200 through a Postgres blip as a healthy store in [A /readyz 200 Through a Postgres Blip Is Not a Healthy Store](/blog/a-readyz-200-is-not-a-healthy-store/), and a timed-out job as a killed worker in [A Timed-Out Job Is Not a Killed Worker](/blog/a-timed-out-job-is-not-a-killed-worker/). This post is the same desk rule for a Codex prompt that opened. Print auto-start. Print the recovery choice. Name who owns the Codex session.

The question is not whether the CLI looks open. The question is whether the named owner can still tell “eligible launch started a shared server” from “this session’s required settings match that server.”

<!--more-->

![Three columns: Auto-start, Recovery choice, Named owner](/img/auto-start-is-not-compatible-settings-1.png)

## The ticket that looks like all-clear

Juniors treat a quiet Codex prompt the way they treat a green LED on a rack. The command returned. The composer is empty. They page nobody. They tell chat the shared background server matches this desk.

Two jobs collide on that prompt.

1. **Start a shared local server for eligible interactive launches.** Public release text: automatic background-server startup is enabled for eligible interactive sessions. The PR that promoted the field: `daemon_auto_start` is stable and on by default for those launches. It is no longer an `/experimental` toggle you have to remember to flip. [Source: https://github.com/openai/codex/releases/tag/rust-v0.157.0] [Source: https://github.com/openai/codex/pull/47179]
2. **Keep this session’s required settings honest against that shared server.** Public PR text: automatic daemon launches used to fall back to embedded mode in silence when shared feature settings differed from the session’s requirements. Changing those settings affects other clients. Restarting the server interrupts active or queued work. The product now offers explicit recovery: run without the daemon, restart with the required settings, or cancel. Default is cancel. Restart needs confirmation. [Source: https://github.com/openai/codex/pull/47318]

If you only screenshot “the prompt opened,” you will file all-clear. You will not file the recovery choice.

{{< note type="warning" title="Do not file all-clear on an auto-started Codex server" >}}
If a coding agent or a junior says the background server is compatible because `codex` opened, print whether auto-start applied, which recovery choice ran (or that none was needed), and one human name on the Codex session before you close the ticket. An open prompt is not a settings match.
{{< /note >}}

I do not invent a fake overnight outage. I use the public contract. The auto-start field is the ticket, not a version pin in the title.

## What auto-start actually is

Public release, 25 September 2026, GitHub tag `rust-v0.157.0` (`00c972e`): enabled automatic background-server startup for eligible interactive sessions, with recovery choices when server settings are incompatible. That sentence is two fields glued with a comma. Split them. [Source: https://github.com/openai/codex/releases/tag/rust-v0.157.0]

Field one is launch. PR `#47179`: promote `daemon_auto_start` to stable and enable it by default for eligible interactive launches. Remove its entry from `/experimental`. [Source: https://github.com/openai/codex/pull/47179]

Field two is mismatch. PR `#47318`: silent embedded fallback hid a settings fight. Recovery is now explicit. The earlier opt-in PR `#46117` added `features.daemon_auto_start` disabled by default. Do not treat that opt-in PR as today’s default. [Source: https://github.com/openai/codex/pull/47318] [Source: https://github.com/openai/codex/pull/46117]

`--no-daemon` is a named recovery path, not a compatibility stamp. PR `#46088`: run with `--no-daemon` without starting or probing the shared server, even when it is already running. Preserve the flag through `resume` and `fork`. Reject combinations with `--remote`, `codex agents`, and `codex queue`, which require a server connection. [Source: https://github.com/openai/codex/pull/46088]

Read that twice.

- **Auto-start applied, prompt opened, no recovery menu:** you have an eligible launch that attached. You still do not have a printed match of required settings versus saved overrides.
- **Recovery menu appeared, someone picked cancel:** you have a mismatch the product refused to paper over. Default is cancel. That is not “settings are compatible.” [Source: https://github.com/openai/codex/pull/47318]
- **Someone reran with `--no-daemon`:** you have an embedded session that skipped the shared server. That is not proof the shared server matches. It is proof this launch did not use it. [Source: https://github.com/openai/codex/pull/46088]

{{< details summary="Pins are evidence, not the hook" >}}
GitHub published `rust-v0.157.0` on 25 September 2026 (release page: 25 Sep 02:31). The npm tarball this morning at `https://registry.npmjs.org/@openai/codex/latest` answered `0.157.1`. Print GitHub tag and npm `latest` as two columns. Do not treat `npx @openai/codex@latest` as the GitHub tag that named auto-start. Do not put those numbers in the title. This post is auto-start versus a settings match, not a patch table. Do not treat `0.157.1` as a new field. [Source: https://github.com/openai/codex/releases/tag/rust-v0.157.0] [Source: https://registry.npmjs.org/@openai/codex/latest]
{{< /details >}}

![Auto-start clock is not a settings-match clock](/img/auto-start-is-not-compatible-settings-2.png)

I keep one table on the ticket.

| What you saw | What it is | What it is not |
| --- | --- | --- |
| `codex` opened after an eligible interactive launch | Auto-start applied for a shared local server | Proof required settings match that server |
| Recovery menu: run without daemon / restart / cancel | A named mismatch the product will not hide | An all-clear |
| Default cancel on that menu | The public default | Permission to restart for other clients |
| Confirmed restart on a managed daemon | A named owner decision after one recheck | A coding-agent default |
| `--no-daemon` | This launch skipped the shared server | Proof the shared server is healthy |
| `--remote`, `codex agents`, `codex queue` | Commands that require a server connection | A `--no-daemon` substitute |
| Quiet composer after a package or privilege error | A failed required-daemon start | A compatible background server |

[Source: https://github.com/openai/codex/releases/tag/rust-v0.157.0] [Source: https://github.com/openai/codex/pull/47318] [Source: https://github.com/openai/codex/pull/46088]

The junior screenshot is the first row. They want the third column. Print the second column first.

Name the owner. I use `CODEX_SESSION_OWNER` the same way I use a migration owner. The person who owns Codex on this desk also owns “did auto-start attach, did recovery run, did anyone confirm a restart.” A coding agent does not get to file all-clear because the prompt was empty.

Do not heading-clone the NUL-in-rule post. That post is matcher bytes versus a wildcard. This post is auto-start versus a settings match. Do not heading-clone a `--bg` or waiting-for-input post. Those are other clocks.

## Probe the two fields, do not write a disable recipe

I keep a probe in the repo the coding agent uses, not in a gist on a laptop. It does not call `codex features disable daemon_auto_start`. It does not pass `--no-daemon` for you. It classifies the launch record that already exists.

```python
#!/usr/bin/env python3
"""Classify a Codex auto-start ticket. Do not flip daemon_auto_start."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

OWNER = os.environ.get("CODEX_SESSION_OWNER", "").strip()
RECORD = Path(os.environ.get("CODEX_LAUNCH_RECORD", "codex-launch-record.json"))
OUT = Path("codex-autostart-ticket.json")

ALLOWED_RECOVERY = {
    "none_printed",
    "run_without_daemon",
    "restart_confirmed",
    "cancel",
    "error_no_daemon_guidance",
}


def load_record(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def classify(rec: dict) -> dict:
    auto = bool(rec.get("auto_start_applied"))
    recovery = str(rec.get("recovery_choice") or "none_printed")
    if recovery not in ALLOWED_RECOVERY:
        recovery = "none_printed"
    prompt_open = bool(rec.get("prompt_opened"))
    if recovery == "run_without_daemon":
        verdict = "EMBEDDED_LAUNCH_IS_NOT_A_SHARED_MATCH"
    elif recovery == "restart_confirmed":
        verdict = "RESTART_NAMED_ON_TICKET"
    else:
        verdict = "AUTO_START_IS_NOT_COMPATIBLE_SETTINGS"
    return {
        "auto_start_applied": auto,
        "recovery_choice": recovery,
        "prompt_opened": prompt_open,
        "verdict": verdict,
    }


def main() -> int:
    if not OWNER:
        print("MISSING_CODEX_SESSION_OWNER", file=sys.stderr)
        return 2
    result = classify(load_record(RECORD))
    result["owner"] = OWNER
    result["record"] = str(RECORD)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The script does not start Codex. It does not talk to a socket. `VERDICT=AUTO_START_IS_NOT_COMPATIBLE_SETTINGS` means you do not have an all-clear. You have a launch whose recovery choice is missing, cancelled, or an error that printed `--no-daemon` guidance. Then open the Codex ticket. Put those four lines on it: owner, auto-start applied, recovery choice, prompt opened.

A second probe is the launch record the desk already writes. Copy the shape as evidence of the fields, not as a hide-the-mismatch recipe.

```json
{
  "auto_start_applied": true,
  "recovery_choice": "none_printed",
  "prompt_opened": true,
  "command": "codex"
}
```

That file names a quiet prompt. It does not name a settings match. If the junior pastes it and files “the background server is compatible,” they mixed the two jobs the same way they mix a green wrangler deploy with a Durable Object cutover.

{{< note type="danger" title="Do not ship a settings-bypass how-to" >}}
This post names `--no-daemon` once, as the public recovery path the product already prints. It does not tell you to disable `daemon_auto_start`. A flag on that key is change control for the named Codex owner. A coding agent does not pick it in chat. [Source: https://github.com/openai/codex/pull/47318] [Source: https://github.com/openai/codex/pull/46088]
{{< /note >}}

Print the ticket from the probe file. Empty owner is a fail, not a skip.

```bash
export CODEX_SESSION_OWNER="${CODEX_SESSION_OWNER:-}"
export CODEX_LAUNCH_RECORD="${CODEX_LAUNCH_RECORD:-codex-launch-record.json}"
python3 scripts/probe_codex_autostart.py
python3 -c "import json,pathlib; print(json.loads(pathlib.Path('codex-autostart-ticket.json').read_text())['verdict'])"
```

![Four-line ticket: owner, auto-start, recovery, prompt](/img/auto-start-is-not-compatible-settings-3.png)

{{< field-note title="Field note" >}}
On a Laravel plus Vue SaaS the mix is ordinary: a coding agent runs `codex` on a checkout, the prompt opens, and a junior files “server is compatible” while another IDE client still holds the shared daemon with different feature overrides. I treat `CODEX_SESSION_OWNER` the same way I treat a migration owner. The person who owns [/ai-agent-operations/](/ai-agent-operations/) on this desk also owns “did auto-start attach, or did this session skip a mismatch.” A coding agent does not get to close a Codex ticket because the composer was empty. I already wrote the sibling rule for a green deploy that is not an immediate Durable Object cutover, and for a ready bit that is not a healthy store. This is the sibling for an auto-started background server that is not compatible settings.
{{< /field-note >}}

## Recovery is a choice, not a compatibility stamp

Public PR `#47318` is the recovery contract: run without the daemon, restart with the required settings, or cancel. Default is cancel. Restart needs confirmation, is allowed only for managed daemons with a feature mismatch, then rechecks once. Noninteractive required-daemon failures return an error with `--no-daemon` guidance. Optional attachment keeps its fallback. Saved overrides persist until someone confirms a change. If saved overrides already match, do not restart. Changing those settings affects other clients. Restarting may interrupt active or queued work. That is why cancel is the default. [Source: https://github.com/openai/codex/pull/47318]

Desk translation:

1. **Cancel is the default.** A quiet Enter is not a restart.
2. **Restart is owned.** It changes the shared server. Other clients feel it.
3. **`--no-daemon` is this launch only.** It does not repair the shared server for the next `codex agents` call.
4. **A required-daemon error that prints `--no-daemon` guidance is a fail.** It is not an all-clear with a footnote.

Public issues that named the error text, not a desk anecdote:

- Arch package report: default interactive launch exits with `this CLI has no complete local package; install a packaged Codex CLI or use the standalone installer` plus `To work without the background server, rerun the same command with --no-daemon`. Official complete package starts the daemon. Incomplete package layout does not. [Source: https://github.com/openai/codex/issues/48050]
- Windows report: default launch exits with `start the Windows daemon from a non-elevated terminal; shared clients must not inherit administrator privileges` plus the same `--no-daemon` guidance. [Source: https://github.com/openai/codex/issues/48043]

I cite those issues as public error strings. I do not turn them into a morning runbook. The ticket is still “auto-start applied, required daemon failed.”

{{< details summary="Config layers are not this ticket either" >}}
Official config basics: Codex reads personal defaults from `~/.codex/config.toml` and project overrides from `.codex/config.toml` when the project is trusted. Precedence, highest first: CLI flags and `--config` overrides, then project config files, then profile files, then user config, then system config, then built-in defaults. That list resolves a model or approval policy. It is not a signed match against a running background server. Do not paste a `config.toml` screenshot as proof the daemon is compatible. [Source: https://developers.openai.com/codex/config-basic]
{{< /details >}}

A coding agent that restarts so this checkout can attach is writing the outage for the other window. Keep the shared daemon on the named owner. If this session needs different feature overrides, file “mismatch, cancel, named owner decides.” `--no-daemon` stays local to this launch. PR `#46088`: do not start or probe the shared server, even when it is already running. Preserve the flag through `resume` and `fork`. Commands that require a server connection stay rejected. [Source: https://github.com/openai/codex/pull/46088]

If chat was quiet while another IDE still held the daemon, file “shared server occupied.” Do not file all-clear.

![This session and another client share one locked server](/img/auto-start-is-not-compatible-settings-4.png)

## What you must not do

Forbidden:

1. File a “background server is compatible” ticket without printing auto-start applied, the recovery choice or `none_printed`, whether the prompt opened, and one human name on the Codex session.
2. Put a Codex version in the title or the first line. The pin is evidence after the decision.
3. Mix this field with a green-deploy Durable Object ticket, a `/readyz` store ticket, a timed-out job ticket, a NUL-in-rule ticket, or a Remove-Item ticket. Those are other posts.
4. Write a disable-`daemon_auto_start` how-to, a standing `--no-daemon` runbook, or a “confirm restart in CI” recipe. The public notes already state recovery defaults to cancel. You do not need a live skip-the-match recipe. [Source: https://github.com/openai/codex/pull/47318]
5. Treat `npx @openai/codex@latest` as GitHub tag `rust-v0.157.0`. This morning `registry.npmjs.org/@openai/codex/latest` answered `0.157.1` while the 25 September GitHub tag that named auto-start is `rust-v0.157.0`. Print both. [Source: https://github.com/openai/codex/releases/tag/rust-v0.157.0] [Source: https://registry.npmjs.org/@openai/codex/latest]
6. Recommend buying ChatGPT, a plan, or a seat because one prompt stayed empty.
7. Treat `--no-daemon` as proof the shared server matches. Official PR: that flag skips the shared server. [Source: https://github.com/openai/codex/pull/46088]
8. Treat a quiet prompt as “required settings already match.” Official PR: default recovery is cancel; restart needs confirmation because other clients share the server. [Source: https://github.com/openai/codex/pull/47318]
9. Mix `codex agents` / `codex queue` / `--remote` with an embedded `--no-daemon` launch. Official PR: those commands require a server connection. [Source: https://github.com/openai/codex/pull/46088]
Allowed:

1. Print whether this launch was an eligible interactive auto-start.
2. Print the recovery choice: `none_printed`, `run_without_daemon`, `restart_confirmed`, `cancel`, or `error_no_daemon_guidance`.
3. Name one human as `CODEX_SESSION_OWNER`.
4. Keep other clients on the shared daemon until that owner confirms a restart.
5. Print `codex --version` and npm `latest` after the decision, in a details block, not in the title.
6. File “auto-start applied, settings not printed as a match” as the ticket title when those two columns disagree.

GSC this week still has no striking-distance query on the green-deploy post, the `/readyz` post, or the timed-out-job post. I am not refreshing those URLs. This is a new field, not a synonym of Sunday’s deploy clock or Saturday’s ready bit.

If you need the broader habit, start at [/ai-agent-operations/](/ai-agent-operations/). Tooling notes live under [/developer-tools/](/developer-tools/). Laravel plus Vue notes live under [/laravel-vue-saas/](/laravel-vue-saas/). A first-week map is at [/start-here/](/start-here/).

A changelog bullet about automatic background-server startup is not permission to skip the settings match.

## What you should do Monday morning

1. Open the repo that actually ships. Export `CODEX_SESSION_OWNER` to a human name. Write a `codex-launch-record.json` for the last interactive launch. Run `probe_codex_autostart.py`. Write the verdict on the ticket next to that name.
2. Print the last Codex launch. Write whether auto-start applied, whether a recovery menu appeared, and which choice ran. If the menu is absent, write `none_printed`. If the process printed `--no-daemon` guidance and exited, write `error_no_daemon_guidance`. [Source: https://github.com/openai/codex/pull/47318]
3. If chat was quiet after a prompt opened, file “auto-start applied.” Decide whether required settings were printed as a match. Official language: recovery choices exist when server settings are incompatible; default is cancel. [Source: https://github.com/openai/codex/releases/tag/rust-v0.157.0] [Source: https://github.com/openai/codex/pull/47318]
4. If someone pastes only an empty composer, reject the review until the named owner can show four lines: owner, auto-start applied, recovery choice, prompt opened.
5. Print `codex --version` and the npm `latest` for `@openai/codex`. If the laptop is behind the 25 September 2026 GitHub tag that named auto-start, do not treat the local pin as those fields. Compare GitHub tag and `latest`, then decide an upgrade as change control, not as a social post. [Source: https://github.com/openai/codex/releases/tag/rust-v0.157.0] [Source: https://registry.npmjs.org/@openai/codex/latest]
6. Confirm coding-agent instructions on this desk name the same owner and forbid “the background server is compatible” without the four lines: owner, auto-start applied, recovery choice, prompt opened.

The question is not whether an empty composer demos well in a gist. The question is whether the named owner can still tell an auto-started shared server from a session whose required settings actually match after handoff.

## Further reading

{{< source href="https://github.com/openai/codex/releases/tag/rust-v0.157.0" label="GitHub — Codex rust-v0.157.0 release notes" >}}

{{< source href="https://github.com/openai/codex/pull/47318" label="GitHub — Offer explicit recovery for incompatible background servers" >}}

{{< source href="https://github.com/openai/codex/pull/47179" label="GitHub — Enable automatic daemon startup by default" >}}
