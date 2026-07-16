---
title: "Laravel Image Processing Is an Adoption Contract, Not an Upload Feature"
date: 2026-07-16T07:00:00+07:00
draft: false
slug: "laravel-image-processing-adoption-contract"
description: "A Laravel image workflow should preserve originals, produce deterministic variants, isolate processing behind a seam, and remain operable after the demo is gone."
topics: ["laravel", "architecture", "image-processing"]
tags: ["laravel", "php", "queues", "filesystem", "testing"]
cover: "/covers/laravel-image-processing-adoption-contract.png"
seo:
  primaryQuery: "laravel image processing architecture"
  secondaryQueries:
    - "laravel image upload queue"
    - "laravel filesystem image variants"
    - "laravel image processing tests"
---

A file input and `Storage::putFile()` can make image work look finished. The browser accepts a JPEG, the application stores it, and a page renders something back. That is a demo.

The production question is different: what does the rest of the application get to rely on after an image arrives?

Does an upload retain the original bytes? Can a profile page request a 320-pixel square image without knowing which driver made it? Can a failed worker retry safely? Can an operator explain why a variant is missing, regenerate it after changing a crop rule, and roll back a bad release without deleting customer data?

Those are adoption questions. They decide whether image processing becomes a maintained part of a Laravel application or a fragile corner of a form request.

Laravel's official documentation gives us durable pieces for this work: request validation, uploaded files, filesystem disks, queues, database transactions, events, HTTP testing, fake storage, and faked queues. Laravel 13.20 also documents a first-party, driver-based Image API for common transformations. That API can be a good processor implementation, but the decoder configuration, output policy, optimizer, and image CDN remain integration choices. Treat those choices as seams, keep their behavior outside the application's public contract, and make the contract plain.

![Upload lifecycle: validate, store the original, record the asset, queue processing, then deliver.](/img/laravel-image-processing-adoption-contract-1.png)

{{< field-note title="Field note" >}}
The image pipeline that impresses during a demo is usually the one that transforms the upload inside the request and immediately returns a polished thumbnail. The image pipeline that survives handoff keeps the original, records state, and lets the expensive or fallible step happen later. Local development, shared hosting, object storage, worker availability, and the next engineer's ability to reproduce a failure matter more than a fast demo.
{{< /field-note >}}

## Define the contract before choosing an image library

Start with nouns and promises, not package names. A useful model has an `image_assets` record for the user-supplied original and `image_variants` records for derived files. The original is evidence. A variant is disposable output.

The asset contract can be small:

| Concern | Contract | Why it matters |
| --- | --- | --- |
| Original | Store the accepted upload under a private, immutable object key | Regeneration and support remain possible |
| Metadata | Record disk, key, MIME type, byte size, and optional checksum | The database identifies the object without guessing paths |
| Variant identity | A variant has a named recipe and deterministic key | Repeated jobs do not create random duplicate files |
| Availability | A variant is `pending`, `ready`, or `failed` | The UI and operators see real state |
| Delivery | The application resolves a URL or response from a variant record | Views do not assemble storage paths |
| Deletion | Deletion is an explicit lifecycle operation | Orphan cleanup does not erase an original by accident |

Do not put a public URL in the contract when the asset may be private. Laravel's filesystem documentation distinguishes file URLs from temporary URLs. A disk can provide a URL for publicly accessible files, while `temporaryUrl` is for time-limited access on supported drivers. The right delivery method depends on the disk and visibility policy. The rest of the application should call an asset presenter or delivery service, not reach directly into `Storage` from every Blade template and API resource.

A named recipe is more than `thumbnail`. Make the rule legible: `avatar-square-320-v1`, `article-hero-1440-v2`, or `listing-card-640-v1`. The final suffix makes a future change boring. When the crop rule changes, add a new recipe. Do not silently overwrite an existing variant and call it an upgrade. Existing pages, caches, and screenshots may rely on the previous output.

The deterministic key should include the asset's stable identifier and the recipe name. A generated UUID is enough for the asset identity; a content hash is useful only if the product has a defined deduplication policy. Laravel can generate UUIDs through `Str::uuid()`, and the filesystem can write a stream or an uploaded file. Neither choice changes the contract: write the original once, derive variants from it, and keep the mapping in the database.

{{< note >}}
Do not treat the browser-provided filename as an object key. Laravel documents methods for getting an uploaded file's original name and extension, but the client supplied name is not a stable storage identity. Generate the application key yourself.
{{< /note >}}

An asset record also gives you a place to put ownership and authorization. An avatar belongs to a user. A product image belongs to a catalog item. A private document preview may belong to an account. That association is an application rule, so keep it in your model layer instead of burying it inside a directory convention.

For a broader view of keeping Laravel boundaries readable as a product grows, see [our Laravel and Vue SaaS guide](/laravel-vue-saas/). The same principle applies here: transport, persistence, background work, and presentation should agree on a small interface.

## Accept uploads as untrusted input and persist the original first

Laravel's validation documentation supports file rules such as `image`, `mimes`, `mimetypes`, `max`, and dimension rules. Use rules that express the product requirement. An avatar upload can require an image and cap size. A publisher workflow may accept a narrower set of MIME types. Validation is the front door, not image processing.

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\GenerateImageVariant;
use App\Models\ImageAsset;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class AvatarUploadController
{
    public function store(Request $request)
    {
        $validated = $request->validate([
            'avatar' => ['required', 'image', 'max:5120', 'dimensions:min_width=160,min_height=160'],
        ]);

        $file = $validated['avatar'];
        $assetId = (string) Str::uuid();
        $originalKey = "images/originals/{$assetId}/source";

        $disk = 'private';
        $stored = $file->storeAs(
            dirname($originalKey),
            basename($originalKey),
            ['disk' => $disk]
        );

        $asset = DB::transaction(function () use ($request, $file, $assetId, $disk, $stored) {
            return ImageAsset::create([
                'id' => $assetId,
                'user_id' => $request->user()->id,
                'disk' => $disk,
                'original_key' => $stored,
                'mime_type' => $file->getMimeType(),
                'byte_size' => $file->getSize(),
                'status' => 'pending',
            ]);
        });

        GenerateImageVariant::dispatch($asset->id, 'avatar-square-320-v1');

        return response()->json([
            'asset_id' => $asset->id,
            'status' => $asset->status,
        ], 202);
    }
}
```

This uses Laravel's uploaded-file storage support rather than moving files with ad hoc PHP paths. The exact disk configuration belongs in `config/filesystems.php`; the application code names a disk and asks the filesystem abstraction to store the file. That makes a local disk, an S3-compatible object store, and a test fake interchangeable at the call site.

There is one uncomfortable boundary here: the object store write and the database transaction are not one atomic transaction. If the file write succeeds and the database insert fails, an original can be orphaned. If the database commit succeeds and dispatch later fails, the asset can remain pending. Do not hide this with a comment about atomicity. Pick a repair rule.

A practical rule is to write the original first, create the record in a database transaction, then enqueue work after the record exists. A scheduled maintenance command can find objects without records under the originals prefix and records whose originals are missing. Laravel's scheduler and filesystem methods give you the building blocks; your retention period and deletion policy remain product decisions.

For strict delivery semantics, Laravel queues also document dispatching jobs after database transactions commit. Use the queue configuration or dispatch option described for your Laravel version when a worker must never observe an uncommitted asset record. The important point is not the syntax. It is the ordering: workers should only receive committed identities.

{{< source href="https://laravel.com/docs/13.x/filesystem" label="Laravel 13.x filesystem documentation" >}}

## Make variants deterministic, idempotent, and outside the request

A resize operation has CPU, memory, decoder behavior, and failure modes. It does not belong on the critical path of a normal upload response. Laravel queues exist to move time-consuming work out of the web request. The controller should acknowledge the accepted original and let the client render a pending state or keep the previous image until a ready variant exists.

Use one job per asset and recipe. The job reads the original from the configured disk, invokes a processor behind an interface, writes the variant, and marks the variant ready. The processor is the seam. Laravel's first-party Image API is one driver-based option; an application may also choose another library, a native tool, or a remote transformation service. Each choice has different runtime requirements and output behavior.

```php
<?php

namespace App\Jobs;

use App\Contracts\ImageProcessor;
use App\Models\ImageAsset;
use App\Models\ImageVariant;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Support\Facades\Storage;

class GenerateImageVariant implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public string $assetId,
        public string $recipe,
    ) {
    }

    public function handle(ImageProcessor $processor): void
    {
        $asset = ImageAsset::findOrFail($this->assetId);
        $key = "images/variants/{$asset->id}/{$this->recipe}.jpg";

        $variant = ImageVariant::firstOrCreate(
            ['image_asset_id' => $asset->id, 'recipe' => $this->recipe],
            ['disk' => $asset->disk, 'object_key' => $key, 'status' => 'pending']
        );

        if ($variant->status === 'ready' && Storage::disk($variant->disk)->exists($variant->object_key)) {
            return;
        }

        $source = Storage::disk($asset->disk)->get($asset->original_key);
        $result = $processor->make($source, $this->recipe);

        Storage::disk($variant->disk)->put($variant->object_key, $result->contents());

        $variant->forceFill([
            'mime_type' => $result->mimeType(),
            'byte_size' => $result->byteSize(),
            'status' => 'ready',
            'failed_at' => null,
        ])->save();
    }
}
```

The job checks both database state and object existence because database state alone cannot prove that an object survived a lifecycle event. A retry after `put()` succeeds but before the database update should write the same deterministic key again. That is safe when the recipe is deterministic and the write has replacement semantics. If the processor produces nondeterministic output, fix the processor or version the recipe. Do not make retries create fresh names.

Set queue retry and timeout values from measured behavior in your environment. The Laravel queue documentation covers attempts, backoff, failed jobs, and job middleware. Your application should decide which errors are retryable. A transient object-store timeout is not the same as an unsupported image format. Record a failure code and message that an operator can act on, while keeping raw decoder details out of public responses.

![Variant state flow for pending, processing, ready, retryable failure, and terminal failure.](/img/laravel-image-processing-adoption-contract-2.png)

A useful refinement is to separate acquisition from processing. The web request writes an original. The worker resolves a recipe. The processor returns bytes and metadata. The storage adapter writes the output. A delivery service turns a ready variant into a public URL, temporary URL, or streamed response. That separation makes a later CDN migration a delivery concern, not a controller rewrite.

{{< details summary="The integration seam to document" >}}
Document `ImageProcessor::make(string $source, string $recipe)` as an application contract. State the allowed input types, crop and orientation rules, output format, quality policy, maximum decoded dimensions, error types, and whether output is deterministic. Bind that contract in the service container. The adapter can change without changing controllers, jobs, or views.
{{< /details >}}

## Keep storage, delivery, and deletion as separate policies

Laravel's filesystem abstraction is deliberately broad. It can write and read files on configured disks, generate URLs for disks that support them, and generate temporary URLs where supported. That broadness is a reason to avoid inventing a single global `public_path()` convention.

Originals and variants often deserve different visibility. A customer upload may need to stay private, while a finished public product thumbnail can live on a public disk. Or both can remain private and be delivered through a controller after authorization. The contract should name which one applies per asset category.

```php
<?php

namespace App\Http\Controllers;

use App\Models\ImageVariant;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class ImageVariantController
{
    public function show(Request $request, ImageVariant $variant)
    {
        abort_unless($variant->status === 'ready', 404);
        abort_unless($request->user()->can('view', $variant->imageAsset), 403);

        return Storage::disk($variant->disk)->response(
            $variant->object_key,
            "{$variant->recipe}.jpg",
            ['Content-Type' => $variant->mime_type]
        );
    }
}
```

A controller response is one verified Laravel filesystem pattern. A URL from `Storage::url()` is another, when the disk and visibility are appropriate. A temporary URL is another, when supported by the disk. Do not promise that one works everywhere. Declare the delivery policy in the asset category and test it against the configured driver.

Deletion needs the same care. Deleting an image from a page must answer: delete which records, which objects, and when? The safest default is to mark the asset deleted in the database, remove variants first, and remove the original only after the retention rule allows it. A background job can perform object deletion. If it fails, the record retains enough identity to retry. This prevents a controller timeout from leaving a half-deleted asset whose state nobody understands.

Laravel model events can help initiate cleanup, but do not make event timing your only operational story. A maintenance command that reconciles database records and storage prefixes gives the team a repair path. That path should log asset IDs, keys, and action results. It should support dry-run output before destructive operations.

For the operational side of this choice, [our developer tools notes](/developer-tools/) and [AI agent operations guide](/ai-agent-operations/) are useful context: prefer tools that make a repair observable and repeatable over scripts that only work on the original author's laptop.

## Test the boundary you own, then test the adapter separately

Image work gets hard to test when tests decode actual pixels everywhere. Laravel's fakes let you test the application boundary without requiring production object storage or a queue worker. `Storage::fake()` supplies a fake disk, and Laravel's test utilities include fake uploaded files. `Queue::fake()` lets a test assert that the application dispatched the correct job.

The upload endpoint test should prove the contract: accepted input creates an asset, stores an original on the named disk, and dispatches one recipe job. It should not assert a particular library call from the controller.

```php
<?php

namespace Tests\Feature;

use App\Jobs\GenerateImageVariant;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Queue;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class AvatarUploadTest extends TestCase
{
    use RefreshDatabase;

    public function test_an_avatar_upload_stores_an_original_and_queues_a_variant(): void
    {
        Storage::fake('private');
        Queue::fake();

        $user = User::factory()->create();
        $file = UploadedFile::fake()->image('avatar.jpg', 640, 640);

        $response = $this->actingAs($user)->postJson('/avatar', [
            'avatar' => $file,
        ]);

        $response->assertAccepted();

        $asset = $user->imageAssets()->firstOrFail();

        Storage::disk('private')->assertExists($asset->original_key);

        Queue::assertPushed(GenerateImageVariant::class, function ($job) use ($asset) {
            return $job->assetId === $asset->id
                && $job->recipe === 'avatar-square-320-v1';
        });
    }
}
```

The job needs a separate test with a fake `ImageProcessor`. Feed it fixed source bytes, have the fake return fixed output bytes and metadata, call `handle()`, then assert the variant record is ready and the fake disk contains the deterministic key. Add a retry test: run the job twice and assert there is still one variant record and one key. Add a missing-original test. Add a processor-exception test that records failure according to your chosen policy.

Test the real processor adapter at a smaller level. Keep a fixture image with known dimensions and orientation. Assert the output dimensions, MIME type, and crop location that the recipe promises. This is where you discover differences between local machines and production images. It is also where you pin down whether an underlying decoder respects EXIF orientation. Laravel does not define that behavior, so the adapter specification must.

{{< note >}}
A fake image upload is excellent for request and storage behavior. It is not evidence that your chosen decoder handles every production image. Keep adapter tests with real fixtures and run them in the same runtime family used by workers.
{{< /note >}}

For a concise walkthrough of keeping feature tests around visible user behavior, see [our Laravel and Vue SaaS guide](/laravel-vue-saas/). The image case follows the same rule: test the application promise, not accidental implementation detail.

## Plan changes and rollback as part of the recipe

The easiest image change to deploy is a new recipe name. `article-hero-1440-v2` can coexist with `article-hero-1440-v1`. New requests can use v2 after it is generated; old pages can keep v1 until a migration completes. If v2 has a bad crop rule, switch the resolver back to v1 and stop enqueueing v2. The original remains intact.

Overwriting a key such as `hero.jpg` removes that rollback. Caches may serve a mixture of old and new bytes. A user can refresh into a different crop. An incident becomes an argument about CDN invalidation instead of a database update. Versioned recipes turn the rollback into a clear, reversible maintenance decision.

![Versioned recipe rollback keeps the original while the resolver switches variants.](/img/laravel-image-processing-adoption-contract-3.png)

Use a migration plan for mass regeneration:

1. Add the new recipe and processor support without changing delivery.
2. Backfill variants in bounded queue batches.
3. Measure job failures and inspect sampled outputs through the normal delivery path.
4. Switch the resolver for new and eligible existing assets.
5. Keep the previous recipe until the retention window ends.
6. Delete old variants with a logged, dry-run-capable maintenance command.

This is deliberately low data and reversible. You do not need invented throughput claims to decide whether it works. Count assets selected, jobs completed, failed jobs, variants ready, and variants missing after a reconciliation pass. Inspect a small set of representative inputs: portrait orientation, transparency if supported, large dimensions, unusual filenames, and an image near the size boundary. Those checks reveal real integration problems.

Do not ship a schema change, a new processor, and a destructive cleanup in one release. Each changes a different layer. A phased rollout leaves a place to stop.

{{< source href="https://laravel.com/docs/13.x/queues" label="Laravel 13.x queues documentation" >}}

## What you should do Monday morning

Write down one asset category, one original policy, and one variant recipe. Pick the category already causing the most support friction, often avatars, listing photos, or article heroes. Do not begin by installing a processor.

Create an `image_assets` table that records ownership, disk, original key, MIME type, byte size, and status. Create an `image_variants` table with an asset foreign key, recipe, disk, object key, status, and error fields. Add a uniqueness constraint on the asset and recipe pair. This makes duplicate dispatches visible as an integrity rule rather than a production mystery.

Then implement the smallest vertical slice:

- validate one upload type with Laravel validation;
- write the accepted original to a private disk using Laravel's filesystem;
- create the asset record;
- dispatch one queue job after the record is committed;
- make a fake processor return fixed bytes;
- write the deterministic variant key;
- expose `pending`, `ready`, and `failed` states to the caller;
- add the upload feature test and the job idempotency test.

Leave the real image adapter behind the interface until this path works. When you add it, document the local prerequisites: installed PHP extensions or binary, memory expectations, supported input formats, worker image or container details, and fixture tests. That documentation is part of the adoption contract. A teammate must be able to run it without rediscovering hidden machine state.

Finally, add a maintenance command in dry-run mode that compares asset records to original objects and variant records to variant objects. Run it in staging before you need it. Recovery work is much cheaper when it is a known command instead of a late-night exploration of a bucket prefix.

## Further reading

These Laravel official documentation pages are the factual base for the framework patterns in this article. They describe the framework facilities; the asset model, recipe naming, processor interface, and retention policy are application design choices.

- [Laravel validation: validating files](https://laravel.com/docs/13.x/validation#validating-files)
- [Laravel requests: retrieving uploaded files](https://laravel.com/docs/13.x/requests#retrieving-uploaded-files)
- [Laravel filesystem](https://laravel.com/docs/13.x/filesystem)
- [Laravel image manipulation](https://laravel.com/docs/13.x/images)
- [Laravel queues](https://laravel.com/docs/13.x/queues)
- [Laravel database: transactions](https://laravel.com/docs/13.x/database#database-transactions)
- [Laravel testing](https://laravel.com/docs/13.x/testing)
- [Laravel task scheduling](https://laravel.com/docs/13.x/scheduling)

The upload is a single request. The adoption contract is everything that lets the next request, the next worker retry, and the next engineer handle the image without guesswork.
