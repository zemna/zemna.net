---
title: "Name the Copilot Surface Before You Trust the Exclusion List"
date: 2026-09-04T07:00:00+07:00
draft: false
slug: "name-the-copilot-exclusion-surface"
description: "A Copilot content exclusion is a policy row. App and CLI now honor it. Agent chat in the editor still can. Name the owner of the list and of the surface before you call a secret recovered."
topics: ["tutorials"]
tags: ["github-copilot", "content-exclusion", "coding-agents", "secrets", "change-control", "vs-code"]
cover: /covers/name-the-copilot-exclusion-surface.png
seo:
  primaryQuery: "GitHub Copilot content exclusion agent mode"
  secondaryQueries:
    - "Copilot CLI content exclusion generally available"
    - "Copilot Agent mode ignores content exclusion"
    - "named owner Copilot exclusion list"
---

A junior opens `.env`, sees no ghost text, and closes the laptop. The exclusion list is in repository settings. Inline suggestions stayed quiet. Standup hears "secrets are off Copilot."

I stop the run there. Quiet inline is one surface. It is not every surface.

On 2 September 2026 GitHub made content exclusion generally available in the Copilot app and Copilot CLI for Copilot Business and Copilot Enterprise. Those two products now skip excluded files as context. The same week, GitHub's own docs still say Edit mode and Agent mode in Copilot Chat do not support content exclusion. [Source: https://github.blog/changelog/2026-09-02-content-exclusions-generally-available-in-copilot-app-and-cli/] [Source: https://docs.github.com/en/copilot/concepts/context/content-exclusion]

The list is real. The gap is also real. A policy row in settings is not a recovered secret.

I already left Copilot's ready-to-approve line as a comment, not a vote, in [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/). I already kept Merge on a named human in [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/). This post is the file-boundary version of the same desk rule. Name who owns the exclusion list. Name which Copilot surface you tested. Do not treat one green check as the whole product.

The question is not whether GitHub added a settings page. The question is whether the path you care about still reaches Agent chat when a person is tired.

<!--more-->

![Quiet inline is one surface: INLINE and APP CLI honor the list, AGENT CHAT still warns](/img/name-the-copilot-exclusion-surface-1.png)

## The list does four things. It does not do a fifth.

GitHub documents what content exclusion is for. When a path is excluded:

- Inline suggestions stay off in that file.
- That file does not feed inline suggestions in other files.
- That file does not feed Copilot's responses on the surfaces that honor the policy.
- Copilot code review on github.com does not review that file.

[Source: https://docs.github.com/en/copilot/concepts/context/content-exclusion]

Those four bullets are the product. They are useful. I use them. I do not stretch them.

The fifth thing people invent is "Agent chat cannot see this path." GitHub does not sell that sentence. The concepts page says content exclusion is currently not supported in Edit and Agent modes of Copilot Chat in Visual Studio Code and other editors. The how-to page repeats it: Agent mode in Copilot Chat in IDEs does not support content exclusion. [Source: https://docs.github.com/en/copilot/concepts/context/content-exclusion] [Source: https://docs.github.com/en/copilot/managing-github-copilot-in-your-organization/configuring-content-exclusions-for-github-copilot]

If the desk's threat is "a coding agent `cat`s `.env` while it works," the settings row does not close that threat. The agent is a different product surface. It reads files with tools. The list is a policy the inline engine and several chat paths consult. Agent mode is not on that list.

{{< note type="warning" title="One quiet editor is not a recovered secret" >}}
Open an excluded file. Confirm ghost text is gone. That proves inline. It does not prove Agent chat, Edit mode, a symlink, or a session that loaded the policy thirty minutes ago.
{{< /note >}}

## What shipped on 2 September, as evidence not as a hook

Keep the product facts short.

| Surface | Exclusion after 2 Sep 2026 | Plan GitHub named |
| --- | --- | --- |
| Copilot app | Honors enterprise / org / repo exclusion; excluded files are not used as context | Copilot Business, Copilot Enterprise |
| Copilot CLI | Same | Copilot Business, Copilot Enterprise |
| Inline in supported IDEs | Already in the content-exclusion docs | Copilot Business, Copilot Enterprise |
| Copilot Chat Ask (supported IDEs) | Honors the list on the documented chat path | Copilot Business, Copilot Enterprise |
| Copilot code review on github.com | Honors the list | Copilot Business, Copilot Enterprise |
| Edit mode in Copilot Chat | Docs: not supported | Same plans, gap still documented |
| Agent mode in Copilot Chat | Docs: not supported | Same plans, gap still documented |

[Source: https://github.blog/changelog/2026-09-02-content-exclusions-generally-available-in-copilot-app-and-cli/] [Source: https://docs.github.com/en/copilot/concepts/context/content-exclusion]

The concepts availability table on GitHub Docs still lists Copilot app and Copilot CLI as not applicable for inline suggestions. I do not treat that grid as a denial of the 2 September changelog. The changelog is the product statement for those two surfaces. The same concepts page still carries the Edit/Agent gap. [Source: https://docs.github.com/en/copilot/concepts/context/content-exclusion]

Website and GitHub Mobile exclusion is still public preview and subject to change. I do not treat preview as a production fence. [Source: https://docs.github.com/en/copilot/concepts/context/content-exclusion]

I do not recommend a plan. I do not recommend an upgrade. If the org is not on Business or Enterprise, this settings page is not the control you think it is. GitHub limits who can configure the list: repository administrators, organization owners, and enterprise owners. People with the Maintain role can view a repository list. They cannot edit it. [Source: https://docs.github.com/en/copilot/managing-github-copilot-in-your-organization/configuring-content-exclusions-for-github-copilot]

That last line is an ownership fact. A maintainer who "checked the box" did not own the box.

## The Agent chat hole is the one juniors will hit this week

Agent mode is the mode people turn on when the task is "fix the login" or "wire the queue." Copilot then picks files, offers edits, and runs commands. GitHub's IDE docs describe that loop. They also describe the exclusion gap in the same product family. [Source: https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide]

On this desk the failure looks ordinary:

1. Org admin added `**/.env` and `secrets.json`.
2. A developer opens VS Code, stays in Agent mode from yesterday.
3. The agent searches the repo, reads `.env`, and pastes a connection string into a "fix" it is proud of.
4. Inline on `.env` was already quiet, so the room believed the file was dark.

Nothing in that story is a GitHub outage. The list did its four jobs. Agent mode was never one of them.

I treat Agent mode like an unattended checkout. If a human is not watching the tool calls, the exclusion list is not the babysitter. Put secrets out of the working tree, or keep Agent mode off that clone. Do not argue with the settings page.

{{< field-note title="Field note" >}}
Laravel SaaS trees on this desk carry `.env`, `storage/oauth-private.key`, and the occasional vendor dump under `storage/app`. Vue admin trees carry `.env`, local HTTPS certs, and screenshot fixtures that still show real emails. Copilot is useful on `routes/web.php` and a Vue form. It is not invited to the key files. The exclusion list is one fence for inline and for Copilot app/CLI after 2 September. It is not the fence for Agent chat. The named owner of the list (usually the org admin) is a different person from the named owner of Agent mode on a laptop (the developer who clicked the mode switch). Both names go in the runbook. I do not let one person say "we excluded it" while another person leaves Agent mode on overnight.
{{< /field-note >}}

![Exclusion list with .env and secrets.json still reaches Agent chat context](/img/name-the-copilot-exclusion-surface-2.png)

### Other holes GitHub already named

Do not invent extra drama. GitHub already listed the rest.

**Semantic leftovers.** Copilot can still use type information, hover definitions, and general project properties such as build configuration when the IDE hands those over from an excluded file. The source file is dark. The type of `DATABASE_URL` in another file is not. [Source: https://docs.github.com/en/copilot/concepts/context/content-exclusion]

**Symlinks and remote disks.** Content exclusions do not apply to symbolic links or to repositories on remote filesystems. A path you excluded in settings can still be reached through a link. [Source: https://docs.github.com/en/copilot/concepts/context/content-exclusion]

**Thirty minutes, then reload.** After you add or change exclusions, GitHub says it can take up to 30 minutes to take effect in IDEs that already loaded the settings. JetBrains and Visual Studio: close and reopen. VS Code: Command Palette → `Developer: Reload Window`. Vim/Neovim: fetched when you open a file. [Source: https://docs.github.com/en/copilot/managing-github-copilot-in-your-organization/configuring-content-exclusions-for-github-copilot]

**The client sends the repo URL.** After you configure exclusion, the Copilot client sends the current repository URL to GitHub so the server can return the right policy. GitHub says those URLs are not logged. I still treat that as a network fact, not as a reason to put production secrets in a clone that talks to Copilot. [Source: https://docs.github.com/en/copilot/concepts/context/content-exclusion]

None of those bullets are "the feature is fake." They are the feature's edges. A junior who only tested ghost text never saw them.

## Write the list so a human can grep it

Repository settings use one path per line, fnmatch, case insensitive:

```text
# Ignore env files anywhere in this repository.
- "**/.env"
- "**/.env.*"

# Ignore named secret files anywhere.
- "secrets.json"
- "secret*"

# Ignore the Laravel storage tree.
- "/storage/**"

# Ignore a single hot file.
- "/src/some-dir/kernel.rs"
```

That shape is GitHub's documented repository format, not a local invention. Comments start with `#`. [Source: https://docs.github.com/en/copilot/managing-github-copilot-in-your-organization/configuring-content-exclusions-for-github-copilot]

Organization and enterprise lists can also exclude files outside Git. The `"*":` root means every filesystem root the Copilot client can see:

```text
# All .env files, Git and not Git.
"*":
  - "**/.env"

https://github.com/example/app.git:
  - "secrets.json"
  - "/storage/**"
```

Enterprise rules apply to every Copilot user in the enterprise. Organization rules apply to users who received a Copilot seat from that organization. Those two scopes are not the same person-set. Name which scope you edited. [Source: https://docs.github.com/en/copilot/managing-github-copilot-in-your-organization/configuring-content-exclusions-for-github-copilot]

I keep a copy of the intended paths in the runbook, next to the GitHub UI. The UI is the source of truth. The runbook is how a junior knows what "we excluded secrets" was supposed to mean on Monday.

## A contract file the team can fail in CI

GitHub will not fail your build when Agent mode reads `.env`. Your own checklist can.

This file does not call GitHub. It records which surfaces the desk claims to have tested, and it fails if someone marks Agent mode as covered.

```python
#!/usr/bin/env python3
"""Desk contract for Copilot content exclusion.

GitHub honors the list on some surfaces and documents a gap on others.
This file is our record, not GitHub's API.
"""

from __future__ import annotations

SURFACES = {
    "inline_suggestions": "honors_list",
    "ask_chat": "honors_list",
    "copilot_code_review_github": "honors_list",
    "copilot_app": "honors_list",  # GA 2026-09-02
    "copilot_cli": "honors_list",  # GA 2026-09-02
    "edit_mode": "gap",
    "agent_mode": "gap",
}

REQUIRED_PATHS = (
    "**/.env",
    "secrets.json",
    "/storage/**",
)


def assert_contract(claimed_covered: dict[str, str]) -> None:
    for surface, status in SURFACES.items():
        claimed = claimed_covered.get(surface)
        if claimed is None:
            raise SystemExit(f"missing surface in runbook: {surface}")
        if status == "gap" and claimed == "honors_list":
            raise SystemExit(
                f"{surface} is a documented gap; do not mark it covered"
            )


if __name__ == "__main__":
    # Example: a junior filled Agent mode as covered. This must fail.
    runbook = {
        "inline_suggestions": "honors_list",
        "ask_chat": "honors_list",
        "copilot_code_review_github": "honors_list",
        "copilot_app": "honors_list",
        "copilot_cli": "honors_list",
        "edit_mode": "gap",
        "agent_mode": "honors_list",  # wrong
    }
    assert_contract(runbook)
```

Run it once. It exits. That is the point. Change `agent_mode` to `gap` and the contract passes. The code is a seatbelt for the story people tell in standup, not a replacement for GitHub's test.

GitHub's own chat test is still the one I want a junior to run by hand:

1. Open a file that is not excluded. Confirm inline still offers a suggestion.
2. Open an excluded file. Confirm inline stays quiet.
3. Attach only the excluded file in Copilot Chat (Ask). Prompt: `explain this file`.
4. If the list is live, Copilot does not use the file and does not list it as a reference.

[Source: https://docs.github.com/en/copilot/managing-github-copilot-in-your-organization/configuring-content-exclusions-for-github-copilot]

Then, separately, switch to Agent mode and ask the same question. If the agent reads the file, write that down. Do not "fix" the notes to match the settings page.

![Exclusion changes can take 30 minutes; reload with Developer Reload Window](/img/name-the-copilot-exclusion-surface-3.png)

### Two named owners, one reload

I write two names on the exclusion page of the runbook.

**List owner.** The person who can edit repository, organization, or enterprise Copilot content exclusion. Usually an org owner. Maintain is not enough to edit.

**Surface owner.** The person who decides whether Agent mode is allowed on a clone that still contains excluded paths. Usually the developer at the laptop. On a shared agent box, it is the person who started the unattended job.

If those names are the same human, say so. If they are not, do not let the list owner announce "secrets are dark" while the surface owner leaves Agent mode on.

Reload is part of ownership. A list change that nobody reloaded is a pending change. GitHub already told you it can take thirty minutes. I do not argue with a session that started before the edit.

Organization owners and enterprise owners can also drive the list through GitHub's REST API for Copilot content exclusion. Those endpoints are public preview and subject to change. I use the API when the org already versions other policies as code. I do not treat an API write as instant on every IDE. The 30-minute window still applies. [Source: https://docs.github.com/en/copilot/managing-github-copilot-in-your-organization/configuring-content-exclusions-for-github-copilot] [Source: https://docs.github.com/rest/copilot/copilot-content-exclusion-management]

A tiny operator check after an API or UI edit:

```bash
#!/usr/bin/env bash
# After an exclusion edit: do not declare victory from the settings page.
set -euo pipefail

echo "1. Reload the IDE (VS Code: Developer: Reload Window)."
echo "2. Open a non-excluded file. Confirm inline still suggests."
echo "3. Open an excluded file. Confirm inline is quiet."
echo "4. Ask-mode chat: attach only the excluded file, prompt: explain this file."
echo "5. Agent mode: same prompt. Record whether the file was read."
echo "6. Write list-owner and surface-owner names in the runbook."
```

That script prints. A person still has to do the clicks. Automation that only curls the settings API has not tested Agent mode.

Exclusion is file context. Approve-off is review votes. Merge-rights is the deploy click. They look related because Copilot is in all three screens. They fail in different rooms.

- A quiet `.env` with Agent mode on is a context leak.
- A ready-to-approve overview with required approvals still open is a comment, not a vote. See [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/).
- A green agent PR with nobody named on Merge is a process leak. See [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/).

I keep all three in the same [AI agent operations](/ai-agent-operations/) habit: name the human, name the artifact, refuse the shortcut that looks like a finished job. For day-to-day tooling around that habit, start at [developer tools](/developer-tools/) and [start here](/start-here/).

Do not collapse them into one Copilot policy. An org can exclude `.env` and still turn on Copilot approvals. An org can leave approvals off and still run Agent mode on a clone full of keys. Each switch has its own owner.

## What you should do Monday morning

1. Open the Copilot content exclusion page for the repo you actually ship. Confirm you are an admin, not Maintain-only.
2. Add the paths you mean, in GitHub's documented format. At minimum: `**/.env`, `secrets.json`, and the Laravel `storage` tree if that tree holds keys.
3. Reload the IDE. Do not wait for a feeling. VS Code: `Developer: Reload Window`.
4. Run GitHub's Ask-mode test: `explain this file` on an excluded path. Confirm the file is not a reference.
5. Switch to Agent mode. Repeat the prompt. Write the result in the runbook, even if you dislike it.
6. Write two names: list owner, surface owner. If Agent mode is allowed on that clone, the surface owner owns the leak.
7. Do not ask anyone to buy a Copilot plan to "make Agent mode honor the list." GitHub has not documented that as a purchase. Keep secrets out of the working tree instead.

If step 5 shows the agent still reading `.env`, you did not fail the exclusion feature. You found the documented gap. Move the file, or turn Agent mode off on that clone.

![Name LIST OWNER and SURFACE OWNER; Agent mode sits under the surface owner](/img/name-the-copilot-exclusion-surface-4.png)

## Further reading

{{< source href="https://github.blog/changelog/2026-09-02-content-exclusions-generally-available-in-copilot-app-and-cli/" label="GitHub Changelog: content exclusions GA in Copilot app and CLI (2 Sep 2026)" >}}

{{< source href="https://docs.github.com/en/copilot/concepts/context/content-exclusion" label="GitHub Docs: content exclusion for Copilot" >}}

{{< source href="https://docs.github.com/en/copilot/managing-github-copilot-in-your-organization/configuring-content-exclusions-for-github-copilot" label="GitHub Docs: excluding content from Copilot" >}}
