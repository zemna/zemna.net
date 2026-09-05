---
title: "A Green apt Update Is Not a Trusted Key After Saturday"
date: 2026-09-05T07:00:00+07:00
draft: false
slug: "green-apt-is-not-a-trusted-key"
description: "GitHub CLI’s Linux signing key expires Saturday 5 September 2026. Last night’s green apt update is not a trusted keyring. Name the owner of the image before the next CI layer runs apt."
topics: ["devops"]
tags: ["github-cli", "apt", "gpg", "linux-packages", "docker", "change-control", "ci"]
cover: /covers/green-apt-is-not-a-trusted-key.png
seo:
  primaryQuery: "GitHub CLI Linux signing key expires September 5 2026"
  secondaryQueries:
    - "gh apt keyring replacement after Saturday"
    - "Dockerfile GitHub CLI keyring owner"
    - "green apt update not a trusted GPG key"
---

The CI job is green. Last night `apt-get update` returned zero. The runner still has `gh`. Standup hears “Linux packages are fine.”

I stop the run there. A green last update is a timestamp. It is not a trusted key.

Today is Saturday, 5 September 2026. GitHub’s changelog is blunt: the current PGP key for the GitHub CLI Linux package repositories expires on this date. Beginning with the first release after that date, APT and RPM repository metadata and newly published RPM packages will be signed with just the replacement key. [Source: https://github.blog/changelog/2026-09-03-github-cli-linux-package-signing-key-expires-september-5/]

If this box installed `gh` from the official APT or RPM repos before 8 April 2026 and nobody reran the setup, the local keyring is still the old file. Last night’s green `apt update` only proves the old key was still alive at that hour. It does not prove the replacement key is on disk.

I already refused to treat a Copilot overview as a merge vote in [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/). I already refused to treat one exclusion list as every Copilot surface in [Name the Copilot Surface Before You Trust the Exclusion List](/blog/name-the-copilot-exclusion-surface/). This post is the package-trust version of the same desk rule. Name who owns the keyring on the image. Name which install path you used. Do not treat a green `apt` line as recovered trust.

The question is not whether GitHub published a new key in April. The question is whether the Dockerfile that still copies last year’s `githubcli-archive-keyring.gpg` will survive the first `apt-get update` after the old key dies.

<!--more-->

![Green apt is not trust: last night exit 0, Saturday expiry, named image owner](/img/green-apt-is-not-a-trusted-key-1.png)

## The green line that looks like a security check

Juniors read `apt-get update` the way they read a green CI badge. Exit zero. Cache refreshed. Move on.

Package managers do not work that way. APT and RPM verify repository metadata against a key they already trust. If the only key on disk is the one that expires today, last night’s refresh is a successful verify of a key that is about to stop counting. After expiry, the same command prints `EXPKEYSIG` or `NO_PUBKEY` and the job dies in a layer that used to be boring.

GitHub already lived this once. In September 2024 the GitHub CLI PGP key expired and Linux installs broke. The emergency fix was to extend that same key. This rotation is the planned replacement, announced on 8 April 2026 with a keyring that holds both keys, then restated on 3 September 2026 as the Saturday deadline. [Source: https://github.com/cli/cli/issues/13118] [Source: https://github.blog/changelog/2026-04-08-new-pgp-signing-key-for-github-cli-linux-packages/]

The desk rule is shorter than the changelog:

1. Last `apt update` exit 0 is a clock, not a key inventory.
2. Official APT/RPM `gh` is the path that cares. Homebrew, Conda, Windows, macOS, source, and a GitHub Releases `.deb` are different paths.
3. A named human owns the keyring file on every image that still runs `apt-get update`.

I do not let a coding agent “fix apt” by adding `--allow-unauthenticated` or by deleting the repo file so the build goes green. That is not a key rotation. That is turning the verify off.

{{< note type="warning" title="Green is not the replacement key" >}}
If `gpg --show-keys` on the keyring file lists only the old fingerprint, last night’s update did not save you. Download the current keyring before the next `apt-get update`, not after the job is already red.
{{< /note >}}

{{< field-note title="Field note" >}}
On Laravel and Vue SaaS images the dangerous layer is ordinary: a PHP-FPM base, a `gh` install so the deploy job can open a release, then `apt-get update` later for `unzip` or `git`. The agent that “helps” with Docker will copy a `curl | gpg` snippet from 2024 and pin a checksum that only covers the old key. I treat that layer as a named owner’s file, the same way I treat a migration. The person who owns `/ai-agent-operations/` on this desk also owns “does this image still trust `cli.github.com` after Saturday.” Copilot does not get to rewrite the keyring as a drive-by lint.
{{< /field-note >}}

## Who this hits, and who it does not

GitHub’s own table is the only one I keep. I do not invent extra platforms.

| Install path | After Saturday |
| --- | --- |
| Official APT (`apt` / Debian / Ubuntu) installed before 8 April 2026, setup never rerun | Yes. Replace the keyring file. |
| Official RPM (`dnf` / `yum` / `zypper`) installed before 8 April 2026, setup never rerun | Yes. Re-add the repo file so the new key imports. |
| Official Linux install **after** 8 April 2026, following current docs | No. That keyring already contains the replacement. Still verify if you do not remember. |
| Windows or macOS | No. |
| Homebrew, Conda, community packages | No. Those paths do not use this PGP key. |
| Build from source | No. |
| Direct `.deb` or standalone archive from GitHub Releases | No. |

[Source: https://github.blog/changelog/2026-09-03-github-cli-linux-package-signing-key-expires-september-5/] [Source: https://github.com/cli/cli/issues/13118]

The trap is the mixed fleet. Laptops on Homebrew look fine. CI is Debian. The production bastion is Ubuntu 22.04 with a keyring copied in 2023. One green laptop is not a fleet check.

I also do not treat “we do not use `gh`” as a pass if a base image still has `/etc/apt/sources.list.d/github-cli.list`. GitHub’s own Docker note says you can remove that list file if `gh` is leftover in a parent image, so `apt-get update` stops trying to verify a repo you do not need. [Source: https://github.com/cli/cli/issues/13118]

Unused repo plus expired key is still a red `apt-get update`. The build does not care that you never call `gh`.

![Which install path trusts this GitHub CLI Linux key: APT and RPM yes; Homebrew Conda Windows macOS source Releases deb no](/img/green-apt-is-not-a-trusted-key-2.png)

## Prove the keyring. Do not argue about last install date.

If nobody remembers when `gh` landed on the box, do not guess April. Show the file.

On Debian and Ubuntu the current recommended path is `/etc/apt/keyrings/githubcli-archive-keyring.gpg`. Older setups used `/usr/share/keyrings/githubcli-archive-keyring.gpg`. If both are missing, read `signed-by=` from `/etc/apt/sources.list.d/github-cli.list`. [Source: https://github.com/cli/cli/issues/13118]

```bash {linenos=inline,hl_lines=[1,8]}
#!/usr/bin/env bash
# Fail the job unless the GitHub CLI keyring contains TWO keys.
set -euo pipefail
KEYRING="${1:-/etc/apt/keyrings/githubcli-archive-keyring.gpg}"
if [[ ! -f "$KEYRING" ]]; then
  echo "missing keyring: $KEYRING" >&2
  exit 2
fi
mapfile -t fps < <(gpg --show-keys --with-colons "$KEYRING" | awk -F: '$1=="fpr" {print $10}')
printf 'fingerprints (%d):\n' "${#fps[@]}"
printf '  %s\n' "${fps[@]}"
need_old='2C6106201985B60E6C7AC87323F3D4EA75716059'
need_new='7F38BBB59D064DBCB3D84D725612B36462313325'
ok=0
for f in "${fps[@]}"; do
  [[ "$f" == "$need_new" ]] && ok=1
done
if [[ "$ok" -ne 1 ]]; then
  echo "replacement key $need_new is not on disk" >&2
  exit 3
fi
```

Two public keys is the pass. GitHub’s sample `gpg --show-keys` output lists:

- Old key `2C6106201985B60E6C7AC87323F3D4EA75716059` (rsa4096, created 2022-09-06, expires 2026-09-05)
- New key `7F38BBB59D064DBCB3D84D725612B36462313325` (rsa4096, created 2026-04-07)

[Source: https://github.com/cli/cli/issues/13118]

I keep those fingerprints in the script as evidence, not as the title of a blog post. The human sentence is: “Does this file contain the April replacement?” If the answer is one key, you are not done.

On RPM systems the check is the imported `gpg-pubkey` packager `GitHub CLI <opensource+cli@github.com>`. One imported key is the old story. A second entry is the replacement. GitHub’s issue lists the exact `dnf` / `yum` / `zypper` re-add commands. Follow the heading that matches how you installed, not a random Stack Overflow paste. [Source: https://github.com/cli/cli/issues/13118]

{{< details summary="What the failure looks like when the old key is already dead" >}}
GitHub published the strings so you can grep logs instead of guessing:

`EXPKEYSIG 23F3D4EA75716059` plus `NO_PUBKEY 5612B36462313325`

`OpenPGP check for package ... from repo "gh-cli" has failed`

`The GPG keys listed for the "packages for the GitHub CLI" repository are already installed but they are not correct for this package.`

`Expired on 2026-09-05T12:44:10Z` on certificate `2C6106201985B60E6C7AC87323F3D4EA75716059`

Those lines are a missing replacement key. They are not permission to skip verify. [Source: https://github.com/cli/cli/issues/13118]
{{< /details >}}

## Replace the file, then update. Not the other way around.

Existing APT users replace the keyring, then run `apt update`. GitHub’s commands (wget or curl) write `https://cli.github.com/packages/githubcli-archive-keyring.gpg` to `/etc/apt/keyrings/` and `chmod go+r`. Then:

```bash
sudo apt update
sudo apt install gh
```

If your `signed-by=` still points at `/usr/share/keyrings/...`, either update that path in the download command or move the source entry to the recommended `/etc/apt/keyrings/` location. The file you refresh must be the file APT actually uses. [Source: https://github.com/cli/cli/issues/13118]

I do not “upgrade `gh` first” on a box whose metadata signature is already failing. The package you want is behind the verify. The keyring is the first artifact.

New installs follow the current Linux doc. That file already ships both keys. No extra ceremony. [Source: https://github.com/cli/cli/blob/trunk/docs/install_linux.md]

RPM users re-fetch `https://cli.github.com/packages/rpm/gh-cli.repo` with the `config-manager` variant they already use (DNF5 `--overwrite --from-repofile`, DNF4 `--add-repo`, yum-config-manager, or zypper remove/add). When the manager asks to import keys, check the fingerprints against the two values above before typing yes. [Source: https://github.com/cli/cli/issues/13118]

I do not recommend a product. I do not tell you to buy GitHub. I tell you to trust the file GitHub already published, or to stop using that repo.

![File then update: download current keyring, confirm two keys, then apt update](/img/green-apt-is-not-a-trusted-key-3.png)

## Docker and CI are the real Saturday outage

The laptop is the easy box. You run two commands and drink coffee.

The image is the incident. A layer from March added the GitHub CLI repo. A later layer runs `apt-get update` to install `jq`. That later layer never saw the keyring file. Cache is warm. Saturday’s first rebuild after expiry is the first time metadata is signed with only the new key.

GitHub’s Docker note matches that shape. If you own the layer that added the keyring, rebuild it so it pulls the current file. If you do not own that layer, add a new layer **before** any `apt-get update` that fetches the updated keyring. [Source: https://github.com/cli/cli/issues/13118]

```dockerfile {linenos=inline,hl_lines=[4,5,6]}
# Before ANY apt-get update that will hit cli.github.com
USER root
RUN mkdir -p -m 755 /etc/apt/keyrings \
 && curl -fsSL -o /etc/apt/keyrings/githubcli-archive-keyring.gpg \
      https://cli.github.com/packages/githubcli-archive-keyring.gpg \
 && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
```

Put that `RUN` above the update. Not after. Not in a comment. Not in a wiki page the agent never reads.

If the image does not need `gh` at all, delete `/etc/apt/sources.list.d/github-cli.list` in a layer you own, then update. Do not leave a dead repo in a PHP base because “it was already there.”

Same rule for GitHub Actions `container:` images and for self-hosted runners that `apt-get update` at job start. The named owner is the person who can merge a Dockerfile change today, not the person who first installed `gh` in 2023.

I already treat agent edit contracts as unfinished without a review vote in the Copilot-approve post. I treat agent Docker edits the same way here. An agent may draft the `RUN`. A named human confirms:

- the URL is `https://cli.github.com/packages/githubcli-archive-keyring.gpg`
- the layer order is keyring, then update
- no `--allow-insecure-repositories`
- no checksum copied from a 2024 gist unless it matches the file you just downloaded on this run

The question is not whether the snippet demos well. The question is whether it survives the next image rebuild after 12:44 UTC today, which is the expiry timestamp GitHub printed on the old certificate. [Source: https://github.com/cli/cli/issues/13118]

## What I refuse to let a coding agent do to apt

This is a coding-agent week, not a distro-admin week. The agent will see a red `apt-get update` and offer four “fixes.” I refuse all four.

**Skip verify.** `--allow-unauthenticated`, `Acquire::AllowInsecureRepositories`, `gpgcheck=0`. The job goes green. The trust model is gone. I revert the line and open a ticket named “keyring,” not “apt flaky.”

**Pin a blog checksum.** The agent copies a `sha256sum` from a tutorial written in April for a file that moved in September. Checksums are useful. Yesterday’s checksum of a two-key file is not a substitute for `gpg --show-keys` on the file you just fetched.

**Delete the error by deleting the package.** `apt-get remove gh` without removing `github-cli.list` leaves the repo. The next update still verifies metadata. You removed the CLI. You did not remove the trust failure.

**Rewrite the source list to HTTP or to a mirror nobody owns.** I do not follow a random `packages.example` because the agent “found a mirror.” Official file, official host, or remove the repo.

The allowed agent job is narrower: fetch the official keyring, print two fingerprints, fail the build if the replacement is missing. That is the same shape as a recovery CLI gate: an artifact on disk, not a chat message that said “done.”

Keep this next to [/ai-agent-operations/](/ai-agent-operations/) and [/developer-tools/](/developer-tools/). A pipeline that lets an agent patch Docker when apt is red, without a keyring fixture, is not an operations desk. It is a hope.

![Agent may draft, human owns the keyring: four refused apt shortcuts versus fetch official file and fail if replacement missing](/img/green-apt-is-not-a-trusted-key-4.png)

## Failure modes I have already seen (ordinary, not a thriller)

I am not going to invent a Saturday outage. The misses are boring.

**The laptop was updated in May. CI was not.** Homebrew on the Mac never used this key. The Debian workflow still copies a keyring from a `COPY` in the repo. One person says “I already fixed gh.” They fixed a path that was never affected.

**The keyring file was refreshed. `signed-by=` was not.** APT still points at `/usr/share/keyrings/githubcli-archive-keyring.gpg`. You wrote the new file to `/etc/apt/keyrings/`. Two files. One of them is a museum. `gpg --show-keys` on the wrong path is a false pass.

**A cached Docker layer still has the March keyring.** You added a later `RUN curl ... keyring` after `apt-get update`. Layer order is the bug. Rebuild with `--no-cache` on the keyring layer, or invalidate it with a real change above the update.

**Someone “fixed” Actions by switching the job to a GitHub Releases `.deb`.** That path is unaffected, and it is a valid escape if you own the checksum. It is not a silent swap in a PR titled “chore: apt.” Document the install path on the runbook. Do not leave half the fleet on APT and half on a pinned `.deb` with no owner.

**The base image vendor will rotate later.** Your `FROM` still has the repo. Waiting on upstream is not a named owner. Either add the keyring layer today or drop the repo today.

**An agent opened a PR that only bumps a comment.** `# key expires 2026-09-05`. Comments do not verify signatures. I close that PR and ask for the `gpg --show-keys` output in the ticket.

These are the same family as “green cron exit is not a finished job,” which I already wrote about and will not rewrite. The artifact here is the keyring file. Show it.

## What you should do Monday morning

Saturday is the expiry date. Do not wait for Monday if CI runs today. If you are reading this after the weekend, do the same list. Do not skip step 1 because the laptop was fine.

1. Pick one Linux box or image that still has `github-cli.list` or `gh-cli.repo`. If you cannot name one, you do not have an inventory. Stop there and make the list.
2. Run `gpg --show-keys` on the APT keyring, or list RPM `gpg-pubkey` entries for `opensource+cli@github.com`. Count keys. One is a fail. Two with the replacement fingerprint is a pass.
3. If it fails, download `https://cli.github.com/packages/githubcli-archive-keyring.gpg` (APT) or re-add `https://cli.github.com/packages/rpm/gh-cli.repo` (RPM) using GitHub’s commands for your manager. Then `apt update` / `dnf update gh`. Not before.
4. Open the Dockerfile or the Actions `container:` image that runs `apt-get update`. Confirm a keyring `RUN` sits **above** that update, or confirm the GitHub CLI repo file is gone. Merge that change with a named owner in the PR body.
5. Paste the two-fingerprint check into the image build. Empty output is a failed build. Chat saying “I rotated the key” is not an artifact.
6. Tell standup the three-line rule. Screenshot it. Link this post from [/start-here/](/start-here/) and from the Copilot-approve post so juniors see the pattern: a green signal is not the control.

The Monday test is short: can a one-year developer point at last night’s `apt` log and say, out loud, “that is a clock”? If they say “apt was green so the key is fine,” you do not have package trust. You have a timestamp.

## Further reading

{{< source href="https://github.blog/changelog/2026-09-03-github-cli-linux-package-signing-key-expires-september-5/" label="GitHub CLI Linux package signing key expires September 5 (GitHub Changelog, 3 Sep 2026)" >}}

{{< source href="https://github.blog/changelog/2026-04-08-new-pgp-signing-key-for-github-cli-linux-packages/" label="New PGP signing key for GitHub CLI Linux packages (GitHub Changelog, 8 Apr 2026)" >}}

{{< source href="https://github.com/cli/cli/issues/13118" label="Upcoming PGP signing key rotation for GitHub CLI Linux packages (cli/cli#13118)" >}}

Related on this site: [Leave Copilot Approve Off](/blog/leave-copilot-approve-off/), [Name the Copilot Surface Before You Trust the Exclusion List](/blog/name-the-copilot-exclusion-surface/), [Five Things I Refused This Week](/blog/five-refusals-this-week/), and the hubs at [/ai-agent-operations/](/ai-agent-operations/), [/developer-tools/](/developer-tools/), and [/laravel-vue-saas/](/laravel-vue-saas/).
