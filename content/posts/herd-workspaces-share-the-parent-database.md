---
title: "Two Agents, One Database: Herd Workspaces Share the Parent DB by Default"
date: 2026-11-08T06:00:00+07:00
draft: false
slug: "herd-workspaces-share-the-parent-database"
description: "Laravel Herd workspaces give each coding agent its own branch, folder and subdomain, but the database stays shared unless you pick clone or empty. Here is how to check it and how to block a reset."
topics: ["laravel"]
tags: ["laravel-herd", "laravel", "coding-agents", "git-worktrees", "local-development", "database", "mysql", "postgresql", "agent-ops"]
cover: /covers/herd-workspaces-share-the-parent-database.png
seo:
  primaryQuery: "laravel herd workspaces shared database"
  secondaryQueries:
    - "herd workspace --database clone empty shared"
    - "herd.yml workspaces database clone hooks after_create"
    - "two coding agents same laravel database migrate:fresh"
---

Here is an afternoon a lot of Laravel teams are about to have.

You give two coding agents two jobs on the same app. One adds a login feature. The other builds a billing report. Each agent gets its own folder, its own git branch and its own address in the browser, so they cannot step on each other's files. You feel good about that. It looks like a clean setup.

Then the billing agent's tests start failing with a column that does not exist. Nothing in its code touches that column. The login agent just ran `php artisan migrate:fresh` to test its new migration, and `migrate:fresh` drops every table and builds them again. Both agents were pointed at the same database the whole time.

I am describing a setup, not telling you about something that happened to me. The reason I can describe it so exactly is that the Herd documentation says so in one plain sentence: "By default, workspaces share the database with their parent site." The feature is good. The default is the part to read twice.

The question is not whether two agents can work side by side on your laptop. They can. The question is whether you can tell, in ten seconds and without trusting anyone's memory, which database each of them is touching.

## What a workspace gives each agent, and what it does not

Laravel Herd is the local development app for PHP and Laravel. Herd 2 added workspaces. Here is how the official page describes one: an isolated copy of a site that lives on its own git branch and is served on its own domain.

Say your site is `shop.test` and you run this in its folder:

```bash
cd ~/Herd/shop
herd workspace feature-auth
```

Herd makes a copy-on-write clone of the project, checks out a new branch, links it as a new site and prints the URL. The docs say that URL is a subdomain of the parent, so this one is `feature-auth.shop.test`. A copy-on-write clone is fast and takes no extra disk space until files change. The workspace uses the same PHP version as its parent. It needs a git repository with at least one commit, and the Herd app must be running.

Read that list and ask what is separate. The branch is separate. The folder is separate. The address is separate. The `.env` file is a copy, and Herd updates four values in it: `APP_URL`, `SESSION_DOMAIN`, `SANCTUM_STATEFUL_DOMAINS`, and `DB_DATABASE` (only if the workspace has its own database). The page adds one more rule: Herd only updates variables that already exist in your `.env`.

What is not on the list is anything else that your `.env` points at. By the description on the page, every other value is copied across as it was. The docs talk about the database. They do not say anything about Redis, queues, the cache or mail. I am not saying those are shared. I am saying the page does not promise they are separate, so you check your own `.env`.

![What a workspace gives each agent: own git branch, folder, subdomain and .env copy; the database is shared by default, and Redis, queues, cache and mail are not covered by the docs](/img/herd-workspaces-share-the-parent-database-1.png)

| | Separate per workspace | Same as the parent by default |
|---|---|---|
| Code | Git branch, project folder | |
| Address | Subdomain such as `feature-auth.shop.test` | |
| `.env` | A copy with four values updated | Every other value |
| Database | Only if you ask for it | **Yes, shared** |
| Redis, queues, cache, mail | Not described in the docs | Check your `.env` |

## Three ways to give a workspace its data

The `--database` option decides what the workspace connects to. There are three modes.

| Mode | What Herd does | What it means for an agent |
|---|---|---|
| `shared` (default) | The workspace uses the parent's database. | A reset or a bad migration lands on everyone, including you. |
| `clone` | New database, all data copied from the parent. The app calls it "Copy". | The agent works on its own copy of real-shaped data. |
| `empty` | New empty database, then `php artisan migrate` runs on Laravel apps. | The agent starts from a blank schema and builds up. |

Herd names a new database after the parent database and the branch. The docs give `shop_feature_auth` as the example, and that name matters later, because it is how you can see the difference. It supports MySQL, MariaDB, PostgreSQL and SQLite, based on the `DB_CONNECTION` in your `.env`. For MySQL and MariaDB it copies with `mysqldump`. For PostgreSQL it creates the database from a template of the parent. For SQLite it copies the database file.

You can also set the default for the whole project in `herd.yml`, so nobody has to remember the flag:

```yaml
# herd.yml
workspaces:
  database: clone
```

![Three ways to give a workspace its data: shared (default, one reset hits everyone), clone (new database with data copied from the parent), empty (new database, then migrate runs); Herd falls back to shared if it cannot create the new database](/img/herd-workspaces-share-the-parent-database-2.png)

That is one line, and it is the single most useful thing in this post. Everything after it is about the case where one line is not enough.

One practical note on `clone`. It makes a copy of your local data for every workspace. If your local database is a dump of real customer data, each clone is another copy of that data on your machine. That is my reading of what "copies all data" means, not a line from the docs. Decide on purpose whether a clone or an `empty` database plus seeders is right for that project.

## Creating a workspace is not proof it has its own database

This is the part I would underline in the docs. Right after the list of supported databases there is this sentence: "If Herd can't create the database, it falls back to the shared database and tells you why."

Read it as a machine would. You ran `herd workspace feature-auth --database=clone`. The workspace was created. The URL was printed. By every signal a script can see, the command worked. But if the copy step failed, you are on the shared database, with a message that scrolled past in a terminal that an agent may never read.

I can think of one realistic way to hit this on PostgreSQL, and I want to be clear that it is my inference and not something I tested. The PostgreSQL manual says that when you copy a database with `CREATE DATABASE ... TEMPLATE`, no other sessions can be connected to the source database while it is being copied, and the command fails if any other connection exists when it starts. The Herd docs say that for PostgreSQL the workspace database is created from a template of the parent. If your app, a queue worker or a database GUI is connected to the parent at that moment, the copy has a reason to fail. Whether Herd handles that by waiting, retrying or falling back is not something the docs say, and I could not run Herd to find out. Herd runs on macOS and Windows, and my publishing host is Linux.

So the fix is not to avoid `clone`. The fix is to stop treating "the workspace exists" as "the workspace is isolated". Those are two facts, and only the second one protects your data.

Herd gives you two places to look. `herd workspaces` lists each workspace with its parent site, URL, PHP version, database and type. And the workspace's own `.env` has a `DB_DATABASE` value, which Herd points at the new database when it creates one. If that value is the same as the parent's, the workspace is sharing.

## A check that reads the `.env` files and refuses to guess

The second place is the one a script can read, so here is a script. It takes the parent folder and one or more workspace folders, reads `DB_CONNECTION`, `DB_HOST`, `DB_PORT` and `DB_DATABASE` from each `.env`, and says which folders point at the same database. It never prints a password.

Two choices are deliberate. First, if it cannot read a database name, that is a failure, not a pass. A folder with no `.env`, or an `.env` with no `DB_DATABASE`, exits with code 2. Second, for SQLite it compares the resolved file path, because two folders that both say `database/database.sqlite` are only the same database if the path resolves to the same file.

```python {linenos=inline}
#!/usr/bin/env python3
"""workspace_db_check.py PARENT WORKSPACE [WORKSPACE ...]

Say out loud which workspaces point at the same database as another one.
Exit codes: 0 = every database is different, 1 = at least two share one,
2 = could not read a database name (fail closed).
"""
import sys
from pathlib import Path


def read_env(folder: Path) -> dict:
    values = {}
    for line in (folder / ".env").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.removeprefix("export ").partition("=")
        values[key.strip()] = value.strip().strip("\"'")
    return values


def identity(folder: Path) -> str:
    env = read_env(folder)
    kind = env.get("DB_CONNECTION", "")
    if kind == "sqlite":  # a file: the same absolute path means the same data
        path = Path(env.get("DB_DATABASE") or "database/database.sqlite")
        return f"sqlite:{(path if path.is_absolute() else folder / path).resolve()}"
    name = env.get("DB_DATABASE", "")
    if not kind or not name:
        raise ValueError("DB_CONNECTION or DB_DATABASE missing in .env")
    host, port = env.get("DB_HOST", "127.0.0.1"), env.get("DB_PORT", "default")
    return f"{kind}://{host}:{port}/{name}"  # never print the password


def main(folders: list) -> int:
    seen, unreadable, shared = {}, False, False
    for raw in folders:
        folder = Path(raw)
        try:
            ident = identity(folder)
        except (OSError, ValueError) as err:
            print(f"UNREADABLE {folder.name}: {err}")
            unreadable = True
            continue
        if ident in seen:
            print(f"SHARED     {folder.name} uses the same database as {seen[ident]}: {ident}")
            shared = True
        else:
            seen[ident] = folder.name
            print(f"OK         {folder.name} -> {ident}")
    return 2 if unreadable else 1 if shared else 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: workspace_db_check.py PARENT WORKSPACE [WORKSPACE ...]")
    sys.exit(main(sys.argv[1:]))
```

I ran it against fixture folders that look like Herd workspaces: a parent called `shop`, one workspace with `DB_DATABASE=shop_feature_auth` (what a clone should look like), and others that still say `shop`. I also made the `.env` files untidy on purpose: a commented-out line, quoted values, an `export` prefix. Here is what it printed.

| Case | What the script printed | Exit code |
|---|---|---|
| Parent plus a clone (`shop_feature_auth`) | `OK` for both | 0 |
| Parent plus a workspace still on `shop` | `SHARED shop-shared uses the same database as shop` | 1 |
| Parent, one clone, two workspaces still on `shop` | `OK`, `OK`, then two `SHARED` lines | 1 |
| Workspace `.env` has no `DB_DATABASE` | `UNREADABLE ... DB_CONNECTION or DB_DATABASE missing` | 2 |
| Workspace folder has no `.env` | `UNREADABLE ... No such file or directory` | 2 |
| SQLite, each folder has its own file | `OK` for both | 0 |
| SQLite, one `.env` holds the absolute path to the parent file | `SHARED ... sqlite:/.../lite/database/database.sqlite` | 1 |

I also grepped the output of the first case for the fixture password and found nothing, which is the point of printing only the connection, host, port and name.

What this does not prove is what a real Herd workspace's `.env` looks like for SQLite, or whether Herd writes `DB_DATABASE` in the form I assumed. The docs say it points `DB_DATABASE` at the new database and names it like `shop_feature_auth`, so the MySQL and PostgreSQL cases follow the documented shape. Run the script on your first real workspace and look at the output before you trust it.

## Three checks, from soft to hard

A script on its own does nothing until something runs it. Here are three places to run it, and they are not equal. I list them from weakest to strongest on purpose.

![Three checks from soft to hard: a hook after create that only warns, an agent's first command that can be skipped, and a wrapper for resets that blocks with exit code 3](/img/herd-workspaces-share-the-parent-database-3.png)

**1. A hook after the workspace is created (warns).** The `herd.yml` workspaces section can run commands after creation. The docs say hooks run line by line in the workspace directory with the workspace's PHP version, and they get environment variables including `HERD_WORKSPACE_PARENT_PATH`, `HERD_WORKSPACE_PATH` and `HERD_WORKSPACE_DATABASE_MODE`. The same page says that if a command fails, Herd stops the hook, shows a warning, **and keeps the workspace**. So a hook can tell a person something is wrong. It cannot stop the workspace from existing.

```yaml
# herd.yml
workspaces:
  database: clone
  env:
    CACHE_PREFIX: "{{branch}}_"
    REDIS_PREFIX: "{{branch}}_"
  hooks:
    after_create:
      - sh -c 'printf "%s" "$HERD_WORKSPACE_PARENT_PATH" > .workspace-parent'
      - sh -c 'python3 tools/workspace_db_check.py "$HERD_WORKSPACE_PARENT_PATH" "$HERD_WORKSPACE_PATH"'
```

A few honest notes on that file. The `env` block and the `{{branch}}` placeholder are both in the docs, and `env` is how you set values that are not already in your `.env`. Laravel reads `REDIS_PREFIX` in its Redis config, and its upgrade guide names `CACHE_PREFIX` as the cache prefix variable, so both are real knobs; check that your own config still reads them. The hook lines follow the documented environment variables, but I could not run Herd's hook runner, so the first real run is your test. Wrapping each line in `sh -c` is my choice, so the variables expand whether or not Herd runs hooks through a shell. Finally, Herd bases a workspace on the last pushed state of the branch unless you pass `--local`, so `tools/workspace_db_check.py` has to be committed and pushed before it exists in a new workspace. Add `.workspace-parent` to `.gitignore`.

**2. A rule the agent reads first (asks).** Put the rule where your agent reads its instructions, with the exact command:

```markdown
## Database rule for workspaces
Before any command that changes data (migrate, db:seed, tests that use the
dev database), run:

    python3 tools/workspace_db_check.py "$(cat .workspace-parent)" "$PWD"

If it does not print OK for this folder, stop and tell the human.
To reset the database, use `bin/fresh-here`, never `php artisan migrate:fresh`.
```

This works most of the time and costs nothing. It is still a request. An agent can skip a line in a long file, and a person in a hurry can too.

**3. A wrapper that is the only way to reset (blocks).** This is the one with teeth. `bin/fresh-here` reads the parent path that the hook saved, runs the check, and only then runs `migrate:fresh`. Any answer other than "all different" stops it.

```bash
#!/usr/bin/env bash
# bin/fresh-here - the only way agents in this repo reset a database.
# Refuses to run when this folder shares a database with its parent.
set -eu
PARENT="$(cat .workspace-parent 2>/dev/null || true)"
if [ -z "$PARENT" ]; then
  echo "BLOCKED: no .workspace-parent file. Is this a workspace? Ask a human."
  exit 3
fi
if ! python3 tools/workspace_db_check.py "$PARENT" "$PWD"; then
  echo "BLOCKED: this folder may share a database. Not running migrate:fresh."
  exit 3
fi
exec php artisan migrate:fresh "$@"
```

I tested the wrapper with a stand-in `php` that only prints what it was asked to run, because there is no PHP on my host. That proves the gate, not the migration. Three runs:

| Folder | What printed | Exit code |
|---|---|---|
| Workspace with its own database | `OK` for both, then `php would run: artisan migrate:fresh --seed` | 0 |
| Workspace still on the parent's database | `SHARED ...`, then `BLOCKED: this folder may share a database` | 3 |
| Folder with no `.workspace-parent` file | `BLOCKED: no .workspace-parent file` | 3 |

The third row is the fail-closed case. A folder that is not a workspace, or a workspace the hook never ran in, gets blocked instead of waved through. That matters more than it sounds. A check that fails open is worse than no check, because you start to trust it.

The limit is stated in the picture above, and it is a hard limit: the wrapper only protects you when resets go through it. A raw `php artisan migrate:fresh` typed by a person or an agent skips it. Laravel's own docs warn that `migrate:fresh` drops all tables, and that on shared databases it drops them regardless of their prefix. So the wrapper is a rail, not a wall, and the instruction file from step 2 is what keeps people on the rail.

## Which mode to pick

This is where I have an opinion, and it is short.

- **Agents that run migrations or tests that reset data: `clone` or `empty`.** If the agent's job touches the schema, it should never share the parent's database.
- **`empty` when the migrations and seeders can rebuild everything you need.** Docs say Herd runs `php artisan migrate` on an empty database, which builds the tables. If you need seeded data, your agent runs the seeders afterward. If the schema is old or has migrations that only work on a database with data in it, `empty` will tell you quickly.
- **`clone` when the work depends on realistic data.** A reporting feature is a good example. You pay with a copy of the data per workspace, as noted above.
- **`shared` on purpose, for one read-only helper.** A second agent that only reads, for example one that writes documentation from the live schema, is fine on the shared database. Say so in writing, so a later teammate knows it was a choice.

The mistake is not choosing `shared`. The mistake is getting `shared` by accident. A one-line `database: clone` in `herd.yml` removes the accident for the common case, and the check above catches the case where Herd falls back.

{{< field-note title="Field note" >}}
On the Laravel SaaS projects I maintain, I treat "which database am I on" the same way I treat "which server am I on". It is a fact you read off the screen, not a thing you remember. That habit predates coding agents. What agents change is how many people, and how many processes, are typing commands at once without your memory in the loop. The lesson from earlier Laravel and Vue maintenance work carries over unchanged: a name you can see, such as a database called `shop_feature_auth`, survives a handoff. A rule that lives in one person's head does not. I do not trust a setup until a script can answer the question for me.
{{< /field-note >}}

## What this connects to

If you already run agents on a schedule, this is the same family of problem I wrote about in [Your Overnight Agent Job Has a Login With an End Date](/blog/agent-job-login-has-an-end-date/): a quiet fact about the environment decides whether the job works, and the tool can look fine while the fact is wrong. A shared database is a quiet fact. So is a login date.

It is also a close cousin of the problem in [Long-Running AI Agents: From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/): more than one agent working at once means shared state needs an owner. The agent pages on [AI Agent Operations](/ai-agent-operations/) collect the rest of these notes, and the Laravel and Vue side lives on [Laravel + Vue SaaS](/laravel-vue-saas/).

## What I did and did not verify

I read the Herd workspaces and `herd.yml` pages, the Herd 2.1.0 changelog and the Laravel News write-up on 2026-11-08. The 2.1.0 notes (2026-11-05) say workspaces now work independently of Herd Studio and list no change to the database default. I did not find a changelog line that changes the shared default, so the docs page is still the source of truth, and it can change.

I ran the check script and the wrapper myself, on fixture folders and with a stand-in `php`. I did not run Herd, `herd workspace`, Herd's hooks, a real MySQL or PostgreSQL clone, or PHP. The PostgreSQL template point is the manual's rule applied to Herd's documented method, and I have not seen Herd fail that way.

## What you should do Monday morning

1. **Run `herd workspaces`** on the project you use agents on. Read the database column for each workspace.
2. **Open the `.env` of two workspaces and the parent.** Compare `DB_DATABASE` by eye once. If two are the same, you have a shared database, whatever you thought you set up.
3. **Add `workspaces: database: clone` or `empty` to `herd.yml`**, commit it, and push it so new workspaces get it.
4. **Copy `workspace_db_check.py` into `tools/`**, commit and push it, and run it on your first real workspace. Check that it reads the `.env` the way Herd wrote it.
5. **Add the `after_create` hook** and watch the first creation to see the output where you can read it.
6. **Write the database rule into your agent instructions**, with the exact command.
7. **Put resets behind `bin/fresh-here`** and stop using raw `migrate:fresh` in agent runs.
8. **Look at `CACHE_PREFIX`, `REDIS_PREFIX`, queue names and mail settings** in your `.env`. The docs do not say they are separated, so decide for each one whether sharing is fine.
9. **Check where your tests connect.** If they use the dev database, a test run resets it too.

If you collect habits like these into a team routine, [Start Here](/start-here/) lists the posts in the order I would read them, and [Developer Tools](/developer-tools/) has the tool-side notes.

## Further reading

- {{< source href="https://herd.laravel.com/docs/macos/sites/workspaces" label="Laravel Herd docs: Workspaces (databases, .env, hooks)" >}}
- {{< source href="https://herd.laravel.com/docs/macos/sites/herd-yaml" label="Laravel Herd docs: herd.yml, configuring workspaces" >}}
- {{< source href="https://herd.laravel.com/docs/macos/changelog" label="Laravel Herd changelog (2.1.0 notes)" >}}
- {{< source href="https://laravel-news.com/laravel-herd-2" label="Laravel News: Laravel Herd 2, coding agents, workspaces, cloud deploys" >}}
- {{< source href="https://www.postgresql.org/docs/current/manage-ag-templatedbs.html" label="PostgreSQL manual: template databases and CREATE DATABASE" >}}
