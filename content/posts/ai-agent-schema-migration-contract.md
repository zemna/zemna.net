---
title: "The Schema Change an AI Coding Agent Cannot Safely Guess"
description: "A generated migration that runs locally is not a production contract. Before an AI coding agent rewrites columns, require expand steps, dual-read boundaries, backfill evidence, worker compatibility, and an explicit rollback decision."
date: 2026-07-28T07:00:00+07:00
draft: false
slug: "ai-agent-schema-migration-contract"
topics: ["ai-agents"]
tags: ["coding-agents", "database-migrations", "laravel", "expand-contract", "schema-compatibility", "agent-verification"]
cover: /covers/ai-agent-schema-migration-contract.png
seo:
  primaryQuery: "AI coding agent database migration safety"
  secondaryQueries:
    - "expand contract schema migration Laravel"
    - "AI generated migration compatibility checklist"
    - "dual write dual read migration agent"
---

An AI coding agent can open your repository, invent a migration class, rename a column in three models, and produce a green local test suite before lunch. That speed is useful. It is also the trap.

The dangerous output is not a broken SQL statement. The dangerous output is a tidy schema change that looks complete because `php artisan migrate` succeeded on a developer laptop. Production still has old queue workers, dual readers, partially backfilled rows, cached Eloquent attributes, and a rollback path that only exists as a chat transcript. The model guessed a destination schema. It did not own the compatibility contract that keeps live traffic safe while both shapes exist.

The question is not whether the agent demos well. The question is whether the change survives maintenance, handoff, and local constraints. If nobody can answer “what still works while old and new code run together,” the migration is not ready to merge.

<!--more-->

![A migration file is not a contract — agent draft versus compatibility gates](/img/ai-agent-schema-migration-contract-1.png)

## Why agents keep collapsing five problems into one file

A human maintainer usually feels the seams. Renaming `status` to `lifecycle_state` is not one edit. It is at least five coupled problems:

| Problem | What can break | Evidence required before merge |
|---|---|---|
| Schema shape | Deploys, replicas, `down()` usefulness | Additive migration first; destructive steps deferred |
| Application writes | New API path writes one shape; old path writes another | Dual-write or single-writer boundary |
| Application reads | Old workers and new web processes disagree | Dual-read adapter with explicit preference order |
| Data movement | Historical rows still hold the old value | Backfill job with progress artifact and idempotency |
| Runtime topology | Queue workers keep old code and connection state | Restart/drain plan and a compatibility check |

An agent sees a repository and a prompt like “normalize invoice status naming.” That prompt rewards a single PR with one migration, model updates, factory updates, and a couple of feature tests. The PR looks coherent in Git. Operationally it can still delete the only safe intermediate state.

Martin Fowler’s Parallel Change pattern, also called expand and contract, exists exactly for this class of problem: break a backward-incompatible interface change into expand, migrate, and contract phases so clients can move deliberately. [Source: https://martinfowler.com/bliki/ParallelChange.html]

Prisma’s data guide states the same order for schema work: expand the schema, expand the interface, migrate data, then contract only after the new path has earned that right. [Source: https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern]

Use that order as the agent brief. Do not ask the model to “replace the column everywhere.” Ask it to stop after the expand step unless every compatibility check already has an artifact.

{{< note type="warning" title="Local green is not production compatibility" >}}
Laravel’s migration tooling can run, roll back a batch, and pretend SQL. Those commands prove the migration file is executable. They do not prove old workers, new readers, and partially backfilled rows agree. Treat `migrate` success as necessary and insufficient. [Source: https://laravel.com/docs/migrations]
{{< /note >}}

## Give the agent a stop line, not a destination schema

The first control is the prompt boundary. A coding agent is good at drafting the expand migration and the dual-read helper. It is a poor owner of the contract phase because contraction depends on production evidence the repository cannot see.

A practical brief looks like this:

```text
Task: prepare an expand-only schema change for invoices.status -> lifecycle_state.

Allowed work:
1. Additive migration that adds nullable lifecycle_state.
2. Dual-read helper that prefers lifecycle_state and falls back to status.
3. Dual-write helper used by the one approved writer path.
4. Feature tests for old-only rows, new-only rows, and dual-populated rows.
5. Backfill job stub with chunking and idempotent updates.
6. Pull request notes listing what is intentionally NOT done.

Forbidden work:
- dropColumn('status')
- renameColumn('status', 'lifecycle_state')
- mass-updating all readers/writers in one pass
- claiming rollback is safe without a decision table

Stop after expand + dual-read/write + tests. Do not implement the contract phase.
```

That stop line changes the review. Reviewers no longer argue with a 40-file “cleanup.” They check whether the expand artifacts are honest.

Laravel’s schema builder makes additive work easy: `nullable()` columns, separate `renameColumn`, and explicit `dropColumn` later. The existence of those APIs is not permission to compress them into one agent turn. [Source: https://laravel.com/docs/migrations]

## Expand first: additive schema only

Here is an expand migration that an agent can draft safely. It adds a column. It does not rename or drop anything.

```php
<?php
// database/migrations/2026_07_28_070000_add_lifecycle_state_to_invoices_table.php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('invoices', function (Blueprint $table) {
            $table->string('lifecycle_state', 32)->nullable()->after('status');
            $table->index('lifecycle_state');
        });
    }

    public function down(): void
    {
        Schema::table('invoices', function (Blueprint $table) {
            $table->dropIndex(['lifecycle_state']);
            $table->dropColumn('lifecycle_state');
        });
    }
};
```

Why this shape matters:

- `nullable()` keeps old writers valid while new writers learn the field.
- `down()` only reverses the additive step. That is a real local recovery path for the expand batch.
- No application behavior is forced by the schema alone. Behavior moves in later deploys.

Laravel documents that `migrate:rollback` rolls back the last batch, optionally by `--step` or `--batch`. That is useful for the expand file. It is not a substitute for operational recovery after a destructive contract step has already rewritten production data. [Source: https://laravel.com/docs/migrations]

![Expand, migrate, and contract timeline — contraction is earned](/img/ai-agent-schema-migration-contract-2.png)

## Dual-read is the application contract the agent usually skips

Schema compatibility without read compatibility is theater. Old rows still have `status`. New rows may have `lifecycle_state`. Mixed rows appear during backfill. The application needs one boundary that understands all three states.

```php
<?php
// app/Support/InvoiceLifecycle.php

namespace App\Support;

use App\Models\Invoice;
use InvalidArgumentException;

final class InvoiceLifecycle
{
    public static function read(Invoice $invoice): string
    {
        if (filled($invoice->lifecycle_state)) {
            return (string) $invoice->lifecycle_state;
        }

        if (filled($invoice->status)) {
            return self::mapLegacyStatus((string) $invoice->status);
        }

        throw new InvalidArgumentException("Invoice {$invoice->id} has no lifecycle value.");
    }

    public static function write(Invoice $invoice, string $state): void
    {
        $state = self::assertKnown($state);

        // Dual-write during migrate phase. Contract phase removes the legacy field later.
        $invoice->lifecycle_state = $state;
        $invoice->status = self::toLegacyStatus($state);
    }

    private static function mapLegacyStatus(string $status): string
    {
        return match ($status) {
            'open' => 'issued',
            'paid' => 'settled',
            'void' => 'cancelled',
            default => throw new InvalidArgumentException("Unknown legacy status [{$status}]"),
        };
    }

    private static function toLegacyStatus(string $state): string
    {
        return match ($state) {
            'issued' => 'open',
            'settled' => 'paid',
            'cancelled' => 'void',
            default => throw new InvalidArgumentException("Unknown lifecycle state [{$state}]"),
        };
    }

    private static function assertKnown(string $state): string
    {
        self::toLegacyStatus($state);

        return $state;
    }
}
```

This helper is deliberately boring. Boring is the point. An agent loves scattering `lifecycle_state ?? status` through controllers, jobs, policies, exports, and Vue props. Every scattered fallback becomes a future miss. One adapter gives the review one seam and gives incident response one place to patch.

For Laravel/Vue SaaS admin screens, the same rule applies on the API boundary: serialize through the helper, not through raw model attributes. That keeps mobile clients, Horizon jobs, and browser sessions on one compatibility story. See the broader boundary discipline in [/laravel-vue-saas/](/laravel-vue-saas/) and the agent operations checklist in [/ai-agent-operations/](/ai-agent-operations/).

## Compatibility tests the agent must not “summarize away”

A green factory test that only creates new-shape rows is a false comfort. Require fixtures for the three production states that actually exist during migration.

```php
<?php
// tests/Feature/InvoiceLifecycleCompatibilityTest.php

namespace Tests\Feature;

use App\Models\Invoice;
use App\Support\InvoiceLifecycle;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class InvoiceLifecycleCompatibilityTest extends TestCase
{
    use RefreshDatabase;

    public function test_read_prefers_lifecycle_state_when_both_exist(): void
    {
        $invoice = Invoice::factory()->create([
            'status' => 'open',
            'lifecycle_state' => 'settled',
        ]);

        $this->assertSame('settled', InvoiceLifecycle::read($invoice));
    }

    public function test_read_maps_legacy_only_rows(): void
    {
        $invoice = Invoice::factory()->create([
            'status' => 'paid',
            'lifecycle_state' => null,
        ]);

        $this->assertSame('settled', InvoiceLifecycle::read($invoice));
    }

    public function test_write_dual_populates_both_columns(): void
    {
        $invoice = Invoice::factory()->create([
            'status' => 'open',
            'lifecycle_state' => null,
        ]);

        InvoiceLifecycle::write($invoice, 'cancelled');
        $invoice->save();

        $invoice->refresh();
        $this->assertSame('cancelled', $invoice->lifecycle_state);
        $this->assertSame('void', $invoice->status);
    }
}
```

If the agent cannot produce these three cases, the change is not “almost done.” It has not started the migrate phase.

{{< details summary="Optional deep dive: what not to put in the first PR" >}}
Keep reporting queries, search indexes, and analytics warehouses out of the first expand PR unless they are on the critical path. Broad “update every SQL string in the repo” sweeps are how agents create accidental contract work inside an expand change. Track those consumers as a checklist artifact, then migrate them in deliberate follow-up pulls.
{{< /details >}}

## Backfill is a job with an artifact, not a migration side effect

Agents often stuff data rewriting into `up()`. That couples schema deploy time to data volume and turns every rollback discussion into guesswork.

Prefer a chunked, idempotent job the operator can observe:

```php
<?php
// app/Jobs/BackfillInvoiceLifecycleState.php

namespace App\Jobs;

use App\Models\Invoice;
use App\Support\InvoiceLifecycle;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

class BackfillInvoiceLifecycleState implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;

    public function __construct(public readonly int $afterId = 0)
    {
    }

    public function handle(): void
    {
        $rows = Invoice::query()
            ->where('id', '>', $this->afterId)
            ->whereNull('lifecycle_state')
            ->orderBy('id')
            ->limit(500)
            ->get();

        if ($rows->isEmpty()) {
            Log::info('invoice_lifecycle_backfill_complete', ['after_id' => $this->afterId]);

            return;
        }

        foreach ($rows as $invoice) {
            // whereNull('lifecycle_state') above guarantees read() maps legacy status.
            $invoice->lifecycle_state = InvoiceLifecycle::read($invoice);
            $invoice->saveQuietly();
        }

        $lastId = (int) $rows->last()->id;
        Log::info('invoice_lifecycle_backfill_chunk', [
            'from' => $this->afterId,
            'to' => $lastId,
            'count' => $rows->count(),
        ]);

        self::dispatch($lastId)->delay(now()->addSeconds(2));
    }
}
```

Operational rules around that job:

1. Dispatch only after the expand migration is live on every node that serves traffic.
2. Log chunk progress as an artifact. “It ran” is not evidence.
3. Keep the job idempotent: already-filled rows are skipped.
4. Do not start the contract phase while the count of `lifecycle_state IS NULL` is unknown.

Laravel’s queue docs warn that jobs dispatched inside database transactions can run before the parent transaction commits. Use `after_commit` on the connection or `->afterCommit()` on the dispatch when backfill or follow-up work is tied to a transactional write. [Source: https://laravel.com/docs/queues]

## Workers are part of the schema change

This is the failure mode teams rediscover after a clean web deploy: schema is new, HTTP code is new, queue workers are still old.

Laravel queue workers are long-lived processes. Deployment guidance exists because code loaded at worker boot is not magically replaced by a web release. Horizon or `queue:work` processes need a deliberate restart/drain plan. [Source: https://laravel.com/docs/queues]

For an agent-driven migration PR, require a short topology note in the pull request:

```markdown
## Runtime topology
- Web/API: deploy release A with dual-read helper
- Queue workers: drain or restart before relying on dual-write behavior
- Scheduler: confirm no legacy command writes `status` directly
- Compatibility check before contract:
  - SELECT count(*) FROM invoices WHERE lifecycle_state IS NULL
  - sample old worker job against dual-populated row
  - rollback decision owner: @data-owner
```

Without that note, the agent’s “all references updated” claim is incomplete. References in source control are not the only consumers. Running processes are consumers too.

![Workers are schema consumers — restart order on the deploy timeline](/img/ai-agent-schema-migration-contract-3.png)

## Rollback is a decision table, not a git revert slogan

Git can restore source. It cannot automatically un-backfill millions of rows or resurrect a dropped column’s meaning for every downstream report. Build a decision table before the agent is allowed near contraction.

| Situation | Safe response | Unsafe response |
|---|---|---|
| Expand migration fails locally | `migrate:rollback` for the expand batch | Hand-edit production |
| Dual-read bug in web only | Feature-flag or patch helper; keep column | Drop new column under traffic |
| Backfill mapping error | Stop job; fix map; re-run idempotent job | Contract early to “finish” |
| Old worker still writing legacy only | Restart/drain workers; keep dual-read | Rename/drop legacy column |
| Contract already dropped `status` | Restore from backup/expand forward if needed | Assume `git revert` rebuilds data |

Laravel’s `down()` method should reverse the operations in `up()`. That statement is precise and limited. It is a migration-file concern, not a full incident recovery plan. [Source: https://laravel.com/docs/migrations]

For AI-generated changes, put the decision table in the PR template. The model can draft rows. A human owner still signs the “who decides to contract” cell. Related rollback discipline for broader AI coding changes lives in the earlier field note on recovery paths: [/blog/ai-coding-rollback-path/](/blog/ai-coding-rollback-path/).

{{< field-note title="Field note" >}}
On Laravel/Vue maintenance work for long-lived SaaS admin systems, the migrations that hurt are rarely the ones that fail in CI. They are the ones that pass CI, ship behind a quiet afternoon deploy, and leave a report exporter or a queue consumer reading the old column for one more day. I now treat every agent-proposed schema PR as incomplete until it names the dual-read boundary, the backfill artifact, the worker restart step, and the person who can stop contraction. The model can draft the expand file in seconds. The contract is still an operations decision. That boundary is what keeps agent speed from becoming weekend recovery work. More of the operating posture is collected under [/developer-tools/](/developer-tools/) and [/start-here/](/start-here/).
{{< /field-note >}}

## What to demand in the pull request before anyone merges

Use this checklist as a hard gate. If an item is missing, the PR stays in expand draft mode.

1. **Prompt boundary attached** — expand allowed; contract forbidden unless evidence links are present.
2. **Additive migration only** — no `renameColumn` / `dropColumn` on the live legacy field in the first PR.
3. **Single read/write adapter** — no scattered `??` fallbacks across the codebase.
4. **Three-state tests** — legacy-only, new-only, dual-populated.
5. **Backfill job + progress artifact** — chunk size, idempotency, completion log or metric.
6. **Worker/topology note** — who restarts what, and in which order.
7. **Rollback decision table** — owner named for go/no-go on contraction.
8. **Explicit non-goals** — warehouse queries, one-off scripts, and external integrations listed as follow-ups.

This is also how you evaluate coding agents week to week. A model that produces a prettier destructive migration is not “better at backend work.” A model that respects the stop line and leaves clean expand artifacts is safer in a real repository. For harness thinking beyond schema work, see [/ai-agent-operations/](/ai-agent-operations/) and the resume-boundary audit pattern in [/blog/audit-agent-resume/](/blog/audit-agent-resume/).

## A short anti-pattern catalog from agent diffs

| Agent habit | Why it fails | Replace with |
|---|---|---|
| One migration that renames and rewrites data | No dual-running window | Expand migration + backfill job |
| “Updated all references” via global search | Misses runtime workers and SQL outside app code | Consumer checklist + topology note |
| Inline mapping copied into 12 files | Future mapping fix becomes a scavenger hunt | One adapter module |
| `down()` empty on a destructive change | Local rollback theater | Expand-first design so `down()` stays real longer |
| Contract PR opened same day as expand | No evidence the migrate phase finished | Separate PR after metrics go to zero |

![Merge gate checklist for agent-generated schema PRs](/img/ai-agent-schema-migration-contract-4.png)

## What you should do Monday morning

1. Pick one schema change currently sitting in an agent branch or a human PR and label its true phase: expand, migrate, or contract.
2. If it is still pretending to be “one migration,” split out an additive expand file and block destructive SQL.
3. Introduce or extract a single dual-read/dual-write adapter; delete scattered fallbacks as you touch them.
4. Add the three-state compatibility tests before any more feature work lands on that branch.
5. Create or restore a chunked backfill job with a progress log; measure `NULL` new-column count.
6. Write the worker restart order into the PR and into the deploy checklist your team actually uses.
7. Name a human owner for the contract go/no-go decision; do not leave that cell blank for the model.
8. Update your coding-agent prompt library with an expand-only stop line for schema tasks.
9. Link the PR to the rollback decision table and to one internal hub page your team already maintains.
10. Only after the migrate-phase evidence is boring—near-zero NULL counts, restarted workers, green compatibility tests—open a separate contract PR.

## Further reading

{{< source href="https://martinfowler.com/bliki/ParallelChange.html" label="Martin Fowler — Parallel Change (expand and contract)" >}}

{{< source href="https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern" label="Prisma Data Guide — Expand and contract pattern for schema changes" >}}

{{< source href="https://laravel.com/docs/migrations" label="Laravel docs — Database migrations" >}}

{{< source href="https://laravel.com/docs/queues" label="Laravel docs — Queues, after_commit, and workers" >}}

If you maintain agent workflows around repository evidence rather than chat confidence, continue with [/blog/audit-agent-resume/](/blog/audit-agent-resume/), [/blog/ai-coding-rollback-path/](/blog/ai-coding-rollback-path/), and the operating hubs at [/ai-agent-operations/](/ai-agent-operations/) and [/developer-tools/](/developer-tools/).
