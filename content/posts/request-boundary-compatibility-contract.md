---
title: "The Request Boundary Is Your Compatibility Contract"
date: 2026-07-15T07:00:00+07:00
draft: false
slug: request-boundary-compatibility-contract
description: "Treat Laravel and Inertia request boundaries as explicit compatibility contracts: validate and normalize input, serialize durable job payloads, lock responses with fixtures, and leave a clean rollback seam."
topics: ["tutorial"]
tags: ["laravel", "inertia", "validation", "queues", "feature-tests", "api-contracts", "maintenance"]
cover: /covers/request-boundary-compatibility-contract.png
seo:
  primaryQuery: "Laravel request boundary compatibility contract"
  secondaryQueries:
    - "Laravel FormRequest validation normalization"
    - "Laravel queue job serialization"
    - "Inertia feature testing validation"
---

A request is not a bag of values that happens to arrive at a controller. It is a compatibility promise between at least four pieces of software: the browser that sends intent, the Laravel code that interprets it, any queued work that outlives the HTTP request, and the client code that consumes the next response.

That promise becomes visible when a small maintenance change lands badly. A field renamed in Vue still submits the old key. A controller accepts both shapes for a while, then a queued job receives an Eloquent model whose state has changed by the time it runs. A response prop quietly changes from `null` to an empty array. Nobody changed the product decision, but a deploy now has two dialects of the same request in production.

I treat these seams as contracts because maintenance work and handoffs are easier when local constraints are written down in code rather than remembered by the person who last touched the form. The contract does not need a large schema platform. In a Laravel and Inertia application, it can be a FormRequest, a small payload DTO, feature tests, and a deliberate rollback point.

This article follows one narrow route: raw input, validation and normalization, job payload serialization, response fixtures, and a rollback seam. The point is not to make every request elaborate. The point is to make changes legible when the request crosses time, process, or team boundaries.

{{< note >}}
A compatibility contract describes accepted input and promised output at a boundary. It does not promise that every internal implementation detail stays frozen forever.
{{< /note >}}

![Five-stage request compatibility flow from raw input to rollback](/img/request-boundary-compatibility-contract-1.png)

## Start with the request you actually receive

Consider an account settings form that lets an administrator assign a display name, a timezone, and a notification preference. The browser has already made choices before Laravel sees anything: unchecked checkboxes may be absent, text fields are strings, and an old tab can submit a version of the form that predates today's deployment.

The tempting controller starts like this:

```php
public function update(Request $request, Account $account): RedirectResponse
{
    $account->update($request->all());

    RebuildAccountDigest::dispatch($account);

    return back();
}
```

This is short, but it mixes every concern that becomes expensive later. The request shape is implicit. The persistence shape is implicit. The job input is implicit. The response contract is implicit. If a field needs a compatibility alias, somebody has to decide where that alias belongs, and the answer is often "somewhere near the controller."

Write down the input contract first. That does not mean documenting every browser quirk in prose. It means deciding which fields are accepted, which legacy names remain accepted during a migration, what their canonical form is, and which values should never enter the rest of the application.

A useful question is: if an older client submits this request tomorrow, can the server either process it deterministically or reject it with a clear validation error? If the answer depends on incidental controller code, the boundary has not been defined yet.

Laravel's validation layer is a good home for this work. A form request authorizes and validates before the controller action receives it, and Laravel documents hooks for preparing input before validation and for accessing the validated result. See the official [validation documentation](https://laravel.com/docs/13.x/validation) for the lifecycle and available rules.

Do not accept an old key forever just because accepting it is easy. Set an expiry condition in the issue or migration plan: a client release date, a compatibility window, or a measured absence of the old traffic shape. The contract should make temporary support obvious enough that somebody can remove it.

| Boundary question | Weak answer | Contract answer |
| --- | --- | --- |
| What input is allowed? | Whatever the controller can use | Rules live in one request class |
| How are old clients handled? | A conditional near persistence | A named alias with a removal decision |
| What reaches queued work? | An HTTP model or raw request values | A scalar, versioned payload |
| What does the client receive next? | Whatever the page happens to share | A tested prop shape or redirect behavior |
| How do we back out? | Revert several unrelated edits | Keep an explicit seam around the new path |

This approach also makes review more honest. Reviewers can discuss whether a legacy `notify_by_email` key belongs in the contract without getting distracted by the database update or queue dispatch that follows.

## Validate and normalize before business code sees the data

Validation is not only rejection. It is the place to turn the accepted wire format into the application format. That distinction matters because a request can be valid while still being inconvenient or unsafe for downstream code.

Here is a FormRequest that supports a temporary legacy key, removes whitespace noise, and gives the controller only a canonical shape:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

final class UpdateAccountPreferencesRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()?->can('update', $this->route('account')) ?? false;
    }

    protected function prepareForValidation(): void
    {
        $legacyNotification = $this->input('notify_by_email');

        $this->merge([
            'display_name' => trim((string) $this->input('display_name')),
            'timezone' => trim((string) $this->input('timezone')),
            'email_notifications' => $this->has('email_notifications')
                ? $this->boolean('email_notifications')
                : filter_var($legacyNotification, FILTER_VALIDATE_BOOL, FILTER_NULL_ON_FAILURE),
        ]);
    }

    public function rules(): array
    {
        return [
            'display_name' => ['required', 'string', 'max:80'],
            'timezone' => ['required', 'string', Rule::in(timezone_identifiers_list())],
            'email_notifications' => ['required', 'boolean'],
        ];
    }

    public function payload(): array
    {
        return $this->safe()->only([
            'display_name',
            'timezone',
            'email_notifications',
        ]);
    }
}
```

There are a few design choices worth keeping explicit.

First, normalize only values whose meaning you own. Trimming a display name is a product decision. Coercing a checkbox is an interface decision. Converting an arbitrary opaque identifier or user-provided rich text inside `prepareForValidation()` can erase information the product intended to preserve. The boundary should make meanings clearer, not make every input look tidy.

Second, avoid passing `$request->all()` beyond the boundary. Laravel offers validated and safe data access specifically so application code can work from values that have passed the rules. The [validation documentation](https://laravel.com/docs/13.x/validation) describes these validated-input APIs. A small `payload()` method has another benefit: it creates a named, reviewable list when a field is added or removed.

Third, decide whether absent and false mean the same thing. HTML forms make this easy to blur. In this example, the current form sends `email_notifications` when it has the field. A legacy form sends `notify_by_email`. If neither is present, validation fails rather than silently choosing a preference. That is intentional: an ambiguous input should not create an account setting by accident.

{{< field-note title="Field note" >}}
On Modoo Laravel SaaS maintenance, a form change often crosses a PHP request object, a delayed job, and a Vue page. A request-level `payload()` method gives future maintainers one place to inspect the public shape without introducing a separate mapping library.
{{< /field-note >}}

A FormRequest is also a useful location for compatibility telemetry if your application has it. Record use of the old key at the edge, not after the value has been normalized away. The metric should count the legacy contract, not infer it from a resulting boolean. Keep the telemetry temporary and delete it with the alias.

## Serialize a durable payload for queued work

HTTP requests are short lived. Queued jobs are not. That difference turns a controller-to-job call into a second boundary, even when both live in the same repository.

Laravel queues support jobs and documents how queued jobs receive serialized state; the official [queue documentation](https://laravel.com/docs/13.x/queues) also covers queued job structure and model serialization behavior. The maintenance rule I use is simpler than the framework's full capability: dispatch scalar, purposeful data whenever the job's behavior depends on the request contract.

A job should not need to reconstruct what a checkbox meant at the time of the request. It should receive the canonical result. It should also not assume an Eloquent model still contains the same values when a worker eventually handles the job.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\UpdateAccountPreferencesRequest;
use App\Jobs\RebuildAccountDigest;
use App\Models\Account;
use Illuminate\Http\RedirectResponse;

final class AccountPreferencesController
{
    public function update(
        UpdateAccountPreferencesRequest $request,
        Account $account,
    ): RedirectResponse {
        $payload = $request->payload();

        $account->fill($payload)->save();

        RebuildAccountDigest::dispatch(
            accountId: $account->id,
            preferences: $payload,
            contractVersion: 1,
        );

        return to_route('accounts.preferences.edit', $account);
    }
}
```

```php
<?php

namespace App\Jobs;

use App\Models\Account;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;


final class RebuildAccountDigest implements ShouldQueue
{
    use Dispatchable;
    use Queueable;


    /** @param array{display_name: string, timezone: string, email_notifications: bool} $preferences */
    public function __construct(
        public readonly int $accountId,
        public readonly array $preferences,
        public readonly int $contractVersion,
    ) {
    }

    public function handle(): void
    {
        $account = Account::query()->findOrFail($this->accountId);

        if ($this->contractVersion !== 1) {
            throw new \LogicException('Unsupported account preference payload.');
        }

        app(AccountDigestBuilder::class)->rebuild(
            account: $account,
            displayName: $this->preferences['display_name'],
            timezone: $this->preferences['timezone'],
            emailNotifications: $this->preferences['email_notifications'],
        );
    }
}
```

The `contractVersion` is not mandatory for every job. Add it when the payload has a meaningful lifetime, multiple deploy versions may overlap, or a queue worker can process old messages after a contract change. Its job is not to make old messages magically valid. Its job is to fail with a recognizable reason and force a conscious policy: support version 1, migrate the message, discard it safely, or drain the queue before release.

Avoid sending the request itself, closures that capture request state, or a broad model instance solely because it is convenient. Laravel can serialize models in queued jobs, but that does not turn the model into a snapshot of the user's request. A primary key plus the concrete values the job needs makes the dependency visible.

The same rule applies to authorization. Authorize the HTTP action at the request boundary. If the queued operation has its own sensitive effect, define what authorization context it needs rather than assuming the original request is still present. Workers have their own execution environment and failure modes.

{{< source href="https://laravel.com/docs/13.x/queues" label="Laravel 13.x queues documentation" >}}

![Durable queue payload with an identifier and decision values](/img/request-boundary-compatibility-contract-2.png)

## Make the response shape a fixture, not an accident

Inertia deliberately keeps server-side validation tied to familiar Laravel behavior. Its documentation explains that validation errors are exposed to the client through the Inertia flow, and its forms documentation covers form helpers and error handling. Read the official [Inertia validation guide](https://inertiajs.com/docs/v3/the-basics/validation) and [forms guide](https://inertiajs.com/docs/v3/the-basics/forms) before deciding how your application presents a particular failure.

The practical point is narrower: do not let the page response become an undocumented byproduct of controller code. The client depends on props, redirects, errors, and sometimes preserved state. Treat the part your page consumes as a fixture.

For a settings page, a stable response may expose this exact shape:

```php
return inertia('Accounts/Preferences/Edit', [
    'account' => [
        'id' => $account->id,
        'displayName' => $account->display_name,
    ],
    'preferences' => [
        'timezone' => $account->timezone,
        'emailNotifications' => $account->email_notifications,
    ],
]);
```

Do not share the whole account model just because serialization makes it easy. That leaks unrelated fields into a front-end dependency surface and encourages the page to reach into data it does not own. A small response fixture says what the page is allowed to expect.

This also keeps input and output naming decisions separate. The request uses `display_name` because it is an HTTP payload defined by a Laravel app. The Inertia page receives `displayName` because that is the local client convention. A mapper at the boundary is less glamorous than a global naming rule, but it prevents one side's conventions from silently becoming the other side's contract.

A response fixture should include the empty cases your UI distinguishes. Is a missing optional preference `null`, omitted, or an empty string? Pick one and test it. Those three values behave differently in Vue templates, TypeScript types, and form reset code.

## Test the contract at the seams

Unit tests are useful for parsing edge cases, but the dangerous regressions here happen when Laravel's request lifecycle, routing, middleware, validation, dispatching, and Inertia response assembly meet. Feature tests are the right level for that route.

Laravel's [HTTP tests documentation](https://laravel.com/docs/13.x/http-tests) documents request helpers, response assertions, and testing patterns. Use them to state the behavior that a client or worker needs, not incidental framework internals.

```php
<?php

use App\Jobs\RebuildAccountDigest;
use App\Models\Account;
use App\Models\User;
use Illuminate\Support\Facades\Queue;

it('normalizes the legacy notification key and dispatches a canonical job payload', function () {
    Queue::fake();

    $user = User::factory()->create();
    $account = Account::factory()->for($user)->create([
        'display_name' => 'Before',
        'timezone' => 'UTC',
        'email_notifications' => false,
    ]);

    $response = $this->actingAs($user)->put(route('accounts.preferences.update', $account), [
        'display_name' => '  River Labs  ',
        'timezone' => 'Asia/Jakarta',
        'notify_by_email' => '1',
    ]);

    $response->assertRedirect(route('accounts.preferences.edit', $account));

    expect($account->fresh())
        ->display_name->toBe('River Labs')
        ->timezone->toBe('Asia/Jakarta')
        ->email_notifications->toBeTrue();

    Queue::assertPushed(RebuildAccountDigest::class, function (RebuildAccountDigest $job) use ($account) {
        return $job->accountId === $account->id
            && $job->contractVersion === 1
            && $job->preferences === [
                'display_name' => 'River Labs',
                'timezone' => 'Asia/Jakarta',
                'email_notifications' => true,
            ];
    });
});

it('rejects an ambiguous notification preference', function () {
    $user = User::factory()->create();
    $account = Account::factory()->for($user)->create();

    $this->actingAs($user)
        ->from(route('accounts.preferences.edit', $account))
        ->put(route('accounts.preferences.update', $account), [
            'display_name' => 'River Labs',
            'timezone' => 'Asia/Jakarta',
        ])
        ->assertRedirect(route('accounts.preferences.edit', $account))
        ->assertSessionHasErrors('email_notifications');
});
```

Add a test for the GET response fixture too. The exact assertion depends on the Inertia testing helpers installed in the application, but the intent should remain concrete: assert the component and the fields the page consumes. Do not write a broad "response is successful" test and call that a contract test.

```php
it('returns the preferences fixture expected by the edit page', function () {
    $user = User::factory()->create();
    $account = Account::factory()->for($user)->create([
        'display_name' => 'River Labs',
        'timezone' => 'Asia/Jakarta',
        'email_notifications' => true,
    ]);

    $this->actingAs($user)
        ->get(route('accounts.preferences.edit', $account))
        ->assertInertia(fn ($page) => $page
            ->component('Accounts/Preferences/Edit')
            ->where('account.id', $account->id)
            ->where('account.displayName', 'River Labs')
            ->where('preferences.timezone', 'Asia/Jakarta')
            ->where('preferences.emailNotifications', true)
        );
});
```

The test names matter. A future maintainer should see "canonical job payload" and know exactly why changing a request key affects a queue assertion. Tests are not only guards; they are the fastest explanation available during a handoff.

![Four checkpoints for testing request-contract seams](/img/request-boundary-compatibility-contract-3.png)

## Leave a rollback seam before you need one

A rollback seam is a small place where you can reverse or bypass a new contract path without turning a production incident into a forensic project. It is not a feature flag for every line of code. It is an intentional boundary around a risky change.

For a request migration, the seam may be a dedicated mapper that accepts both `notify_by_email` and `email_notifications`. For a response migration, it may be a page prop adapter that can emit the old and new key during a short transition. For queue work, it may be a version switch that routes version 1 and version 2 payloads to separate handlers while old messages drain.

Keep the seam near the boundary. A controller flag that changes a dozen internal branches creates more uncertainty than it removes. A named `AccountPreferencesPayload::fromRequest()` mapper or a `PreferencesResponse::forAccount()` transformer is easy to disable, inspect, and delete.

The rollback decision needs a limit. Write down what you will roll back: acceptance of a new input key, dispatch of a new job version, or presentation of a new response prop. Also write down what remains irreversible, such as a database value already persisted. That distinction changes incident response. Reverting a response adapter is often safe; reverting a destructive migration needs a separate plan.

A compatibility window should have an owner and an end condition. Otherwise the seam becomes permanent archaeology. Add a test that uses the legacy input only while the alias is supported. When the window closes, delete the branch and delete that test in the same change. The removal is proof that the application now speaks one dialect again.

For related operating habits, see [Laravel and Vue SaaS notes](/laravel-vue-saas/), the [developer tools index](/developer-tools/), and [how this site starts technical work](/start-here/). They are different topics, but they share the same preference: small explicit interfaces beat hidden coordination.

## What you should do Monday morning

1. Pick one form that dispatches a job or returns a page with several props. List its raw input keys, validated keys, persisted fields, queued values, and client-facing response fields on one screen.
2. Move normalization and legacy aliases into a FormRequest. Add a `payload()` method that returns only the canonical values used by the controller.
3. Change one queued job to accept a scalar identifier plus the values it needs from the request contract. Add a contract version if old jobs can survive a deployment.
4. Write one feature test for a valid legacy or current submission, one for a rejected ambiguous submission, and one for the Inertia response fields the page reads.
5. Name the rollback seam and set a removal condition. Put the removal date or client-release dependency in the issue that introduced the compatibility path.

## How to verify this advice

Run the change against a representative browser request, then compare the evidence at every seam: the Form Request's validated payload, the persisted record, the queued job payload, and the Inertia props consumed by the page. Keep the assertions in a feature test so the evidence survives the next refactor. Finally, exercise the rollback seam in a non-production environment and confirm that it reverses only the intended boundary without leaving a second contract path active.

The next request change will still have tradeoffs. The difference is that the tradeoffs now have a home: the boundary, its tests, and its temporary compatibility code. That is enough structure to change a Laravel and Inertia application without asking every maintainer to reconstruct history from controllers and queue logs.

## Further reading

- [Laravel validation](https://laravel.com/docs/13.x/validation)
- [Laravel queues](https://laravel.com/docs/13.x/queues)
- [Inertia validation and forms](https://inertiajs.com/docs/v3/the-basics/validation) and [forms](https://inertiajs.com/docs/v3/the-basics/forms)
