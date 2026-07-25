---
title: "The Rollback Path Is the Real AI Coding Feature"
description: "A clean AI-generated diff is not ready for production until a team can disable it, restore its data path, and prove the prior behavior returned. Build rollback evidence into the change before the model writes the patch."
date: 2026-07-25T07:00:00+07:00
draft: false
slug: "ai-coding-rollback-path"
topics: ["backend-infrastructure"]
tags: ["ai-coding", "rollback", "feature-flags", "database-migrations", "laravel", "deployment-safety"]
cover: /covers/ai-coding-rollback-path.png
seo:
  primaryQuery: "AI coding rollback strategy"
  secondaryQueries:
    - "feature flag rollback deployment"
    - "reversible database migration Laravel"
    - "AI generated code production safety"
---

The most dangerous AI-generated change is not the obviously bad one. It is the tidy diff that passes a happy-path test, reaches staging, and leaves nobody able to answer one operational question: **how do we get back?**

A model can produce a controller, a migration, a queue handler, and a deployment file in minutes. That does not make the combined change reversible. The question is not whether this demos well; it is whether it survives maintenance, handoff, and local constraints. If the answer depends on someone remembering a chat transcript or improvising SQL during an incident, the change was not ready to merge.

This is a backend and infrastructure discipline, not an anti-AI argument. AI coding is useful when it reduces the cost of drafting a bounded implementation. It becomes risky when the speed of drafting hides the fact that a change crosses several recovery boundaries at once: application behavior, schema shape, data backfill, asynchronous work, configuration, and deployment.

<!--more-->

![A reversible AI-generated change has a switch, a data path, and a proof](/img/ai-coding-rollback-path-1.png)

## A diff is an implementation artifact, not a recovery plan

A code review often begins with the visible patch: renamed methods, new tests, a migration, an environment variable, and an updated workflow. Those are necessary inputs. They are not a rollback plan.

A rollback plan names four things before the change ships:

| Recovery question | Evidence that answers it | Owner |
|---|---|---|
| What behavior can be stopped? | A feature flag, routing rule, or deploy target | Application owner |
| What data shape remains safe? | A backward-compatible migration and restore procedure | Data owner |
| What external work must stop? | Queue pause, idempotency record, or provider switch | Operations owner |
| How do we know recovery worked? | A focused verification command and observable result | Reviewer or incident lead |

This table is deliberately small. It prevents a common failure mode in generated patches: the agent changes a database column, a PHP service, and a worker at the same time, while the review calls the whole thing “one feature.” It is one feature from a product viewpoint. Operationally it can be three different rollback mechanisms.

Martin Fowler describes Parallel Change as a way to break a migration into reversible steps. The important idea is not the name. It is the order: introduce a compatible path, move callers deliberately, and remove the old path only after the new one has earned that right. [Source: https://martinfowler.com/bliki/ParallelChange.html]

For AI-generated code, make that order part of the prompt and the pull request template. Do not ask an agent to “replace the billing status field everywhere.” Ask it to add a compatible field, write the dual-read boundary, identify every writer, add tests for both representations, and stop before removal. The agent now has a boundary it can respect.

{{< note type="warning" title="Do not confuse revert with recovery" >}}
A Git revert restores source history. It does not automatically reverse a completed migration, cancel an already-dispatched job, undo an API call, or restore a record changed by the new code. Treat source rollback and operational recovery as separate checks.
{{< /note >}}

## Start with a bounded change and an explicit kill switch

A feature flag is useful only when it controls a behavior that still has a valid old path. A flag wrapped around an incomplete replacement is decoration. The application needs a stable default, a named new path, and a test that proves both paths remain reachable.

In Laravel, keep the flag decision at a boundary rather than scattering `if` statements through controllers, jobs, and views. One small adapter makes the decision inspectable and gives an incident responder one place to look.

```php
<?php
// app/Support/InvoiceDeliveryMode.php

namespace App\Support;

use Illuminate\Support\Facades\Config;

final class InvoiceDeliveryMode
{
    public static function useV2(): bool
    {
        return (bool) Config::get('features.invoice_delivery_v2', false);
    }
}
```

The service can now select an implementation without making the controller own deployment policy:

```php
<?php
// app/Services/InvoiceDeliveryService.php

namespace App\Services;

use App\Support\InvoiceDeliveryMode;

final class InvoiceDeliveryService
{
    public function send(int $invoiceId): void
    {
        if (InvoiceDeliveryMode::useV2()) {
            app(InvoiceDeliveryV2::class)->send($invoiceId);
            return;
        }

        app(InvoiceDeliveryV1::class)->send($invoiceId);
    }
}
```

The rollback command is then operationally honest: set the configured flag to false, reload the configuration in the deployment mechanism your team uses, and run a proof that exercises the V1 path. Do not call this safe merely because the application has a boolean. The old implementation must still be deployable, its dependencies must still exist, and its side effects must be compatible with records written while V2 was active.

A useful pull request section is therefore not “Rollback: flip flag.” Write the complete sentence instead:

> Set `invoice_delivery_v2=false`; confirm new dispatches resolve to V1; inspect the delivery receipt for a test invoice; retain V2 records for investigation; do not replay already accepted provider requests.

That last clause is where generated code needs human judgment. A model can propose retry code. It cannot decide which external effect is safe to repeat without the product and provider contract.

![Feature flag routes a reversible release](/img/ai-coding-rollback-path-1.png)

## Database rollback is usually a compatibility problem

Database changes are where “revert the deploy” becomes misleading. Once a migration has altered a shared schema or backfilled data, an older application version may not understand the result. GitLab’s migration guidance requires reversibility, while also documenting that production incidents can use a roll-forward strategy rather than a direct `db:rollback`. Both facts matter: reversible migrations are valuable, but the safest production recovery is sometimes a forward fix that restores compatibility. [Source: https://docs.gitlab.com/development/migration_style_guide/]

The practical pattern is expand, migrate, contract:

1. **Expand** the schema without invalidating the deployed application.
2. **Migrate** reads and writes while both representations are valid.
3. **Contract** only after verification and an agreed retention window.

For a Laravel migration, adding a nullable column is a different risk from renaming a column in place. The first creates room for compatible code. The second can break an older worker immediately. This migration deliberately expands only:

```php
<?php
// database/migrations/2026_07_25_000000_add_delivery_mode_to_invoices.php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::table('invoices', function (Blueprint $table): void {
            $table->string('delivery_mode')->nullable()->index();
        });
    }

    public function down(): void
    {
        Schema::table('invoices', function (Blueprint $table): void {
            $table->dropIndex(['delivery_mode']);
            $table->dropColumn('delivery_mode');
        });
    }
};
```

The `down()` method is not a permission slip to execute it blindly against a production table. It documents the inverse schema operation for this narrow migration. Before a real downgrade, confirm whether any deployed code still writes the column, whether a backfill has made it a source of truth, and whether dropping the column discards evidence needed for recovery.

The AI prompt should force those questions into the output. Require a migration note with: current readers, current writers, expected backfill state, backward-compatibility period, and the condition that permits removal. If the agent cannot list them from repository evidence, it should stop and ask for the missing boundary rather than fabricate one.

{{< field-note title="Field note" >}}
In Laravel SaaS maintenance, the expensive failure is rarely a syntax error in a generated migration. It is a change that works in a new web request while an older queue worker, scheduled command, or integration job still assumes yesterday’s schema. I keep database rollout notes beside the change because deployment and worker replacement do not happen at the same instant.
{{< /field-note >}}

![Expand, migrate, contract keeps database changes compatible](/img/ai-coding-rollback-path-2.png)

## Queues and external calls need their own reversal boundary

A rollback has to account for work already accepted by another system. Turning off a web route does not unsend an email. Reverting a deploy does not remove a queue message that has already been reserved. Re-running a job may duplicate a payment, notification, or webhook if the code does not use a stable business key.

Separate three actions in the change record:

| Action | What it does | What it does not do |
|---|---|---|
| Disable | Stops new work from entering the new path | Does not undo accepted work |
| Drain or pause | Controls queued work under an owned procedure | Does not repair a bad completed effect |
| Reconcile | Compares local records with downstream receipts | Does not replace a prevention mechanism |

For generated job code, ask the agent to make the idempotency boundary explicit. The application should claim a durable record before it performs the external side effect, then store the provider receipt after success. The exact storage and transaction design depend on the system, but the review question stays the same: what stable key lets a retry recognize that the effect already happened?

```php
<?php
// app/Jobs/SendInvoiceNotification.php

namespace App\Jobs;

use App\Models\DeliveryAttempt;
use App\Models\Invoice;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;

final class SendInvoiceNotification implements ShouldQueue
{
    use Queueable;

    public function __construct(public readonly int $invoiceId) {}

    public function handle(InvoiceNotifier $notifier): void
    {
        $key = "invoice-notification:{$this->invoiceId}";

        $attempt = DeliveryAttempt::firstOrCreate(
            ['idempotency_key' => $key],
            ['state' => 'claimed'],
        );

        if ($attempt->state === 'sent') {
            return;
        }

        $receipt = $notifier->send(Invoice::findOrFail($this->invoiceId));
        $attempt->update(['state' => 'sent', 'provider_receipt' => $receipt]);
    }
}
```

This is a teaching example, not a universal transaction recipe. A production design still has to define uniqueness at the database layer, failure states, retry timing, provider semantics, and concurrent workers. The point is that a queue retry is not a rollback command. It needs a durable decision record.

GitLab’s deployment documentation treats rollback as returning an environment to a previously successful deployment. That can restore application code quickly, but it does not settle the queue and data questions above. [Source: https://docs.gitlab.com/ci/environments/deployments/]

## Make proof after rollback a release requirement

A rollback that ends with “the deploy completed” is unverified. Define one proof per boundary before the first deployment. Keep it narrow enough to run under incident pressure and specific enough to reject a false recovery.

For the invoice example, the proof list is concrete:

- the configuration reports V1 as the active delivery path;
- a controlled test invoice creates one delivery attempt, not two;
- the receipt is stored against that attempt;
- the old worker can read current invoice rows;
- the health endpoint or log query shows no new V2 dispatches after the switch.

Run the same proof before enabling V2. That gives the release a baseline, not merely a recovery ritual. If the old path cannot pass its own controlled test before a rollout, a feature flag will only make the outage easier to toggle. Record the input identifiers, the deployment revision, and the returned receipt so an incident responder can compare the post-rollback state with the pre-release baseline without reconstructing the story from chat messages.

Put those checks in a script, a runbook, or a deployment job. The exact tool matters less than the artifact. A reviewer needs a command and output they can inspect later, not a paragraph that says “verified manually.”

```bash
#!/usr/bin/env bash
# scripts/verify-invoice-delivery-rollback.sh
set -euo pipefail

php artisan config:show features.invoice_delivery_v2
php artisan invoices:send-test --invoice=rollback-check
php artisan deliveries:assert-single-attempt --invoice=rollback-check
php artisan queue:monitor default --max=0
```

The command names are intentionally application-owned. A framework cannot know your success condition. Your repository can. If an AI agent proposes the script, require it to point each command at an existing application command or test target. Do not merge a plausible-looking verification script that calls utilities your project does not provide.

![A rollback proof checklist for an AI-assisted release](/img/ai-coding-rollback-path-3.png)

## Write the AI task so it cannot hide the missing decision

The fastest way to improve generated changes is to make the request structurally incomplete until recovery details exist. Add a short contract to the task:

```text
Change boundary: add invoice delivery V2 behind an existing application flag.
Do not remove V1 or rename existing database columns.
Before editing, list readers, writers, queue consumers, and external effects.
Deliver: migration plan, test command, rollback switch, post-rollback proof, and files not changed.
Stop if any required dependency or owner is absent from repository evidence.
```

This changes the agent’s job from “finish the feature” to “prepare a reversible change.” It also gives review a way to detect scope drift. If the output includes a new schema, an unbounded backfill, and a provider integration but no recovery owner, the task failed its contract even if tests are green.

The same principle belongs in code review. GitHub’s pull-request guidance includes deployment requirements for database migrations, rollback plans, and feature-flag configuration. Use that as a reminder to make recovery evidence reviewable, not as a checkbox to paste into every description. [Source: https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/customization-library/custom-instructions/pull-request-assistant]

For related operating patterns, connect this release boundary to the [AI Agent Operations](/ai-agent-operations/) hub, [Developer Tools](/developer-tools/), and [Laravel + Vue SaaS](/laravel-vue-saas/). The same habit appears in a different form in the [agent edit contract](/blog/the-agent-edit-contract-i-use-before-a-coding-agent-touches-a-repo/) and the [AI code review harness](/blog/a-repeatable-review-harness-for-ai-generated-code-after-the-first-merge-gate/): decisions become safer when they leave evidence another person can inspect.

Treat the rollback note as a versioned interface. It needs a named owner, a review date, and a removal condition. A flag that remains permanently because nobody owns the cleanup becomes a second implementation path with no contract. A migration that remains compatible forever creates the same debt in the database. Schedule the contract phase deliberately: remove the old path only after the live proof, worker fleet, data retention decision, and incident owner all agree that recovery no longer depends on it. That is how a temporary safety boundary stays temporary without becoming a surprise rewrite later.

## What you should do Monday morning

1. Pick one AI-assisted change that crosses an application and data boundary. Do not start with a rewrite.
2. Write the old path, new path, kill switch, data compatibility rule, queue or provider effect, and recovery proof in the pull request before implementation.
3. Add a test that proves the switch selects the old path as well as the new one.
4. For each migration, write down the last deployed reader and writer that must remain compatible. Delay destructive schema removal until that list is empty.
5. Run the rollback proof in a non-production environment and attach the command output to the change record.
6. Ask a reviewer who did not write the patch to perform the recovery steps from the artifacts alone. If they need a chat transcript, the rollback path is still missing.

The durable advantage of AI coding is not that it writes more code per hour. It is that a disciplined team can use it to draft smaller, better-specified changes. Keep the change reversible, preserve the evidence, and make the way back as concrete as the way forward, before a release needs it under real operational pressure.

## Further reading

- {{< source href="https://martinfowler.com/bliki/ParallelChange.html" label="Martin Fowler: Parallel Change" note="A concise explanation of reversible expand–migrate–contract change." >}}
- {{< source href="https://docs.gitlab.com/development/migration_style_guide/" label="GitLab: Migration Style Guide" note="Reversibility and production migration guidance." >}}
- {{< source href="https://docs.gitlab.com/ci/environments/deployments/" label="GitLab: Deployments" note="Environment rollback behavior." >}}
