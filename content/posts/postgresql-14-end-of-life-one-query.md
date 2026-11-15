---
title: "PostgreSQL 14 Is End of Life: One Query to Check Your Version, and What to Reindex After the Update"
date: 2026-11-15T06:00:00+07:00
draft: false
slug: "postgresql-14-end-of-life-one-query"
description: "PostgreSQL 14 got its final release on Thursday, Nov 12, 2026. One query tells you which version you run, and one short list tells you what to reindex after you update."
topics: ["backend"]
tags: ["postgresql", "end-of-life", "security-update", "reindex", "pg-upgrade", "database", "laravel", "patch-management"]
cover: /covers/postgresql-14-end-of-life-one-query.png
seo:
  primaryQuery: "postgresql 14 end of life"
  secondaryQueries:
    - "how to check postgresql version"
    - "postgresql 14.25 reindex after update"
    - "upgrade postgresql 14 to 18 pg_upgrade"
---

Try this without opening a console: write down which PostgreSQL version your production database runs. Not the version you installed on your laptop. The one that answers your app today.

If you hesitated, this post is for you. On Thursday, Nov 12, 2026, the PostgreSQL project shipped the final release of version 14 and wrote, in its own announcement, that version 14 "is now end-of-life and will no longer receive security and bug fixes."

Your database did not stop on Thursday. It will answer queries tomorrow, and the day after. The change is quieter: the next time someone finds a security bug in version 14, nobody upstream is going to fix it. Whether that matters depends on a fact most teams have not written down.

<!--more-->

The question is not whether your database still works. It is whether you can say, in one sentence and with a name next to it, which version it runs and who decides when it moves.

## What the project actually announced

I re-read the announcement, the versioning policy page, the security page and the 14.25 release notes on Sunday, Nov 15, 2026. All four are on postgresql.org. This is the short version.

| Fact | What the page says |
|---|---|
| Release date | 2026-11-12 (a Thursday) |
| Versions released | 18.7, 17.12, 16.16, 15.20, 14.25, and 19 RC 2 |
| Security fixes | "52 security vulnerabilities and over 140 bugs" |
| Version 14 | "This is the final release of PostgreSQL 14" |
| Support window | A major version is supported for 5 years after its first release |
| 14 dates | First release Sep 30, 2021. Final release Nov 12, 2026 |
| 14.25 release notes | "expected to be the last PostgreSQL release in the 14.X series" |
| Minor update cost | No dump and reload, and no `pg_upgrade`, to apply this update |

One more number I counted myself. The security page has a table of every fixed issue with a "fixed in" column. I counted the rows that name this announcement: 52 rows, and 40 of them list 14.25 among the fixed versions. So the last version 14 release is not an empty goodbye. It carries most of the fixes. It is also the last one.

![Support end dates for PostgreSQL 13 to 18: 13 ended Nov 13, 2025, 14 ended Nov 12, 2026, then 15, 16, 17 and 18 run until Nov 2027, 2028, 2029 and 2030.](/img/postgresql-14-end-of-life-one-query-1.png)

{{< note type="note" title="Read the date, not the column" >}}
When I read the versioning table on Nov 15, the row for 14 still had "Yes" in the "Supported" column, while its "Final Release" cell said November 12, 2026 and the announcement said end-of-life. The date and the announcement agree with each other. Use them. Do not use the "Yes" as a reason to wait.
{{< /note >}}

## The one query

Run this against the database your app really uses. In a console, a SQL client, or `psql`:

```sql
SELECT current_setting('server_version')                  AS version,
       current_setting('server_version_num')::int / 10000 AS major,
       CASE
         WHEN current_setting('server_version_num')::int / 10000 <= 14
           THEN 'end of life: plan a major upgrade'
         ELSE 'supported: take the newest minor'
       END AS verdict;
```

On the test engine I used, this printed:

```text
 version | major |             verdict
---------+-------+----------------------------------
 18.6    |    18 | supported: take the newest minor
```

I ran it on PGlite 0.5.16, an embedded build of PostgreSQL 18.6, because this machine has no PostgreSQL server install. The `CASE` branch for 14 and older is plain arithmetic that I did not trigger on a 14 server. The `current_setting` calls and the division are what the query proves. The PostgreSQL docs describe `server_version` and `server_version_num` as read-only settings that report the server version.

If you only have a shell, this is the one-liner version. I did not run it here either, since there is no `psql`:

```bash
psql "$DATABASE_URL" -Atc "SHOW server_version;"
```

The trap is not the syntax. It is the word "your". Many teams have more than one place where a database lives: production, a staging copy, a read replica, the Docker image someone uses for local work, the CI service container. Run the query on each and write the answer in one row per place, with one name per row.

## Three answers, three plans

The query gives you a number. The number gives you one of three plans.

![A decision flow: the version query leads to three plans. 13 or older: already out of support. 14: update to 14.25 now and schedule a major upgrade. 15 to 18: take the newest minor and walk the reindex list.](/img/postgresql-14-end-of-life-one-query-2.png)

**13 or older.** The same policy table says version 13 had its final release on Nov 13, 2025. You were already past the line a year ago. This is not a patch task. It is a planned migration, and the plan below for 14 is your plan too.

**14.** Do two things, in this order. First, update to 14.25 now, because it is the last release that will carry those 40 listed fixes for your line. Then book the major upgrade as a real task with an owner and a date. A final release is a deadline for the second step, not a replacement for it.

**15 to 18.** You are inside the support window. Take the newest minor (15.20, 16.16, 17.12 or 18.7) and then read the post-update list in the next sections. The project's own policy page says the community considers minor upgrades "less risky than continuing to run an old minor version."

## If it says 14: update first, then book the move

A minor update on the same major version is the small job. Stop PostgreSQL, install the new binaries, start it again. The announcement says you do not have to dump and reload or use `pg_upgrade` for this one.

The 14.25 release notes add a warning for your line: "several different bugs have been discovered that could result in index corruption. Examine the changelog entries below that mention REINDEX, and reindex any indexes you have that might be affected." So on 14 the reindex list is part of the same job. Read the entries that mention `REINDEX` in the [14.25 release notes](https://www.postgresql.org/docs/release/14.25/), and do the reindex steps in the next section.

Then the real decision. Here is the runway each supported line has, from the policy page:

| Major version | Final release date | Time left from today |
|---|---|---|
| 15 | Nov 11, 2027 | about a year |
| 16 | Nov 9, 2028 | about 2 years |
| 17 | Nov 8, 2029 | about 3 years |
| 18 | Nov 14, 2030 | about 4 years |

A move to 15 puts you in the same place in about a year. A move to 18 buys the longest runway. That is a judgment, not a rule. If an extension or a framework you depend on is not ready for 18, the right target is the newest line they support.

PostgreSQL 19 is also close. The announcement lists 19 RC 2 and says general availability is planned for Nov 19, 2026. My own habit is not to make a brand new `.0` the first target of a production move in the same week it ships. You may decide differently, and a staging copy is the place to find out.

A major upgrade is the one step in this post that needs a rehearsal. The tool for it is `pg_upgrade`, and it has a dry-run mode that the docs describe as "check clusters only, don't change any data":

```bash
pg_upgrade --check \
  --old-bindir=/usr/lib/postgresql/14/bin \
  --new-bindir=/usr/lib/postgresql/18/bin \
  --old-datadir=/var/lib/postgresql/14/main \
  --new-datadir=/var/lib/postgresql/18/main
```

The paths are Debian-style examples. Use your own. The new cluster has to exist before you run it, and the docs list the exact steps. I did not run this command here. The docs also say that after a `--check` run the old cluster was unmodified and can be restarted. The versioning policy adds that you can go from one major version to another without stopping at each one in between, but it recommends reading the release notes of every version you skip.

If your database is a managed service from a cloud provider, the provider sets its own support dates, and its console shows the version you run. I did not check any provider's dates for this post. Look them up before you rely on them, and treat the upstream date above as the earliest point at which the project stops helping.

## If it says 15 to 18: take the minor, then walk the list

Update the binaries first. Do the reindex steps after, not before. The announcement says to reindex after updating, and that way the rebuild runs on the fixed code.

The announcement lists these post-update steps. I turned each into a line you can match against your own database.

![A checklist of six post-update steps: GIN indexes, pg_trgm GiST indexes, missing chunk number errors, bpchar B-tree indexes, incremental backups, and NOT NULL NO INHERIT on partitioned tables, each with its action.](/img/postgresql-14-end-of-life-one-query-3.png)

| If you have... | Do this after updating |
|---|---|
| GIN indexes you suspect are affected | `REINDEX INDEX your_index_name;` |
| `pg_trgm` GiST indexes (`gist_trgm_ops`) | Reindex them |
| `missing chunk number` errors when reading a table | `REINDEX TABLE your_table_name;` (this also rebuilds its TOAST table index) |
| B-tree indexes on `bpchar` columns declared without a length | Reindex them. `char(n)` columns are not affected |
| Incremental backups | Take a new full backup and use it as the base for later incremental ones |
| Partitioned tables | Run the announcement's `NOT NULL NO INHERIT` query and repair what it finds |

Finding the candidates is a catalog lookup. These two queries list the GIN indexes and the `pg_trgm` GiST indexes in the database you are connected to:

```sql
SELECT 'gin' AS kind,
       i.indexrelid::regclass::text AS index_name,
       i.indrelid::regclass::text   AS table_name
FROM pg_index i
JOIN pg_class c ON c.oid = i.indexrelid
JOIN pg_am am   ON am.oid = c.relam
WHERE am.amname = 'gin'
UNION ALL
SELECT 'pg_trgm gist',
       i.indexrelid::regclass::text,
       i.indrelid::regclass::text
FROM pg_index i
JOIN pg_class c ON c.oid = i.indexrelid
JOIN pg_am am   ON am.oid = c.relam
JOIN pg_opclass oc ON oc.oid = ANY (i.indclass::oid[])
WHERE am.amname = 'gist' AND oc.opcname = 'gist_trgm_ops'
ORDER BY 1, 3, 2;
```

I ran this on a throwaway database with three GIN indexes (an array column, a `jsonb` column and a `gin_trgm_ops` text index) and one `gist_trgm_ops` index. It returned the three GIN rows and the one trigram GiST row, and it did not list the plain B-tree indexes. That is the only claim I am making about it: it finds those two index types. It does not tell you whether a given index is damaged.

The `bpchar` lookup works the same way. `atttypmod = -1` is how the catalog marks a `bpchar` column declared without a length:

```sql
SELECT i.indexrelid::regclass AS index_name,
       i.indrelid::regclass   AS table_name,
       a.attname              AS column_name
FROM pg_index i
JOIN pg_class c ON c.oid = i.indexrelid
JOIN pg_am am   ON am.oid = c.relam
JOIN pg_attribute a ON a.attrelid = i.indrelid
                   AND a.attnum = ANY (i.indkey::int2[])
WHERE am.amname = 'btree'
  AND a.atttypid = 'bpchar'::regtype
  AND a.atttypmod = -1
ORDER BY 2, 1;
```

On the same test database it returned the one B-tree index on the `bpchar` column and skipped the `char(5)` one. The partitioned-table query is copied from the announcement. I ran it too. It returned no rows, and I could not make it return one, because the 18.6 engine refuses to create that constraint on a partitioned table ("not-null constraints on partitioned tables cannot be NO INHERIT"). So I know the query is valid SQL. I do not know what it prints on a database that has the problem.

One practical warning before you reindex a large table. The REINDEX docs say a plain `REINDEX` "locks out writes but not reads of the index's parent table," and that it blocks nearly every query that wants to use the index being rebuilt. `REINDEX CONCURRENTLY` takes lighter locks, but it is not free. This same release fixes a case where an index rebuilt with it on a TOAST table could miss later updates. Time the reindex on a copy of your data, and pick a quiet window for the real one.

## What this post is not saying

The security list is long, and a long list invites a panic. A few limits keep it calm.

- I did not read exploit details, and this post does not contain any. The project's page lists each issue with a score.
- I did not label any issue "critical". I only read the scores the project prints, and they run from 3.1 to 8.8.
- The scores are not trivia. By my count 35 of the 52 score 8.0 or higher. 32 of those 35 carry "privileges required: low", which is the scoring system's way of saying the attacker needs a login that can already connect. The other 3 need a person to do something first: two involve restoring a dump, one involves logical replication.
- I have no claim about any of these being used against anyone. The announcement does not make one, and I did not look for one.
- Not every fix applies to every version. 40 of 52 rows list 14.25. The other 12 do not list 14.
- The announcement does not name Laravel, PHP or any app framework. The only Laravel-shaped line is that your `DB_CONNECTION=pgsql` host is where this lives.

That last line is also the cheapest first step if you run Laravel. This finds the setting in an app folder:

```bash
grep -nE '^DB_(CONNECTION|HOST|PORT|DATABASE)=' .env
```

The value tells you where the database is. It does not tell you the version. Only the query above does.

{{< field-note title="Field note" >}}
On the Laravel and Vue projects I look after, and the Modoo Laravel SaaS projects are that shape, the database version is the fact least likely to be on a list. The app version lives in `composer.lock`, the Node version lives in a pin file, and the database lives in a console or a compose file that one person set up once. When that person is not in the room, nobody can answer the first question in this post. I did not look at any production database to write this, so I cannot tell you how common a 14 is. What I can say is that the repair for this kind of gap is not a tool. It is a row in a runbook: place, version, owner, next review date.
{{< /field-note >}}

## What you should do Monday morning

These fit in one sitting, whatever day you read this.

1. **List every place a PostgreSQL server runs for your app.** Production, staging, replicas, CI, and the local Docker image. Put one row per place in a note.
2. **Run the one query on each.** Write the `version` and `major` columns next to the row.
3. **Rows on 15 to 18:** schedule the newest minor (15.20, 16.16, 17.12 or 18.7). Put the reindex list from this post in the same ticket.
4. **Rows on 14:** update to 14.25 first. Read the `REINDEX` entries in its release notes. Then open a second ticket for the major upgrade with an owner and a date.
5. **Rows on 13 or older:** the ticket already should exist. If it does not, open it today and say "past final release since Nov 13, 2025."
6. **Run the GIN, trigram and `bpchar` queries** on each database that is on the update list. Reindex only what they find.
7. **If you use incremental backups,** take a new full backup after the update and make it the base.
8. **Rehearse the major upgrade** with `pg_upgrade --check` on a copy before you pick a date.
9. **Write the next review date** on every row. Version 15 has until Nov 11, 2027.

## What this connects to

It is the same habit as [a Laravel signed-link advisory](/blog/laravel-signed-url-expiry-two-conditions/), [a Vite dev-server advisory](/blog/vite-dev-server-bug-check-host-flag/) and [a Node patch day](/blog/node-patch-day-where-your-version-lives/): a list of places, a check against the fix, one name per row. If you share a database between agents or workspaces, [Two Agents, One Database](/blog/herd-workspaces-share-the-parent-database/) is the other half of the question. A health check that passes through a database blip is its own trap, covered in [A /readyz 200 Through a Postgres Blip](/blog/a-readyz-200-is-not-a-healthy-store/).

The hub pages go wider: [Laravel and Vue SaaS notes](/laravel-vue-saas/), [developer tools](/developer-tools/), [AI agent operations](/ai-agent-operations/), and the [start here](/start-here/) page.

## Further reading

- {{< source href="https://www.postgresql.org/about/news/postgresql-187-1712-1616-1520-1425-and-19-rc-2-released-3442/" label="PostgreSQL announcement: 18.7, 17.12, 16.16, 15.20, 14.25 and 19 RC 2 released" >}}
- {{< source href="https://www.postgresql.org/support/versioning/" label="PostgreSQL versioning policy: support window and final release dates" >}}
- {{< source href="https://www.postgresql.org/support/security/" label="PostgreSQL security page: the table of fixed issues" >}}
- {{< source href="https://www.postgresql.org/docs/release/14.25/" label="PostgreSQL 14.25 release notes" >}}
- {{< source href="https://www.postgresql.org/docs/current/sql-reindex.html" label="PostgreSQL docs: REINDEX and its locking behavior" >}}
- {{< source href="https://www.postgresql.org/docs/current/pgupgrade.html" label="PostgreSQL docs: pg_upgrade and its --check mode" >}}
