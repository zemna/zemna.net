---
title: "24 Workers AI Models Passed Their Nov 20 Cutoff: One Grep, One Config Change"
date: 2026-11-24T07:00:00+07:00
draft: false
slug: "workers-ai-retired-model-ids-grep-config"
description: "Cloudflare moved the Workers AI retirement from Nov 15 to Nov 20. Here is a grep for the 24 retired model IDs, a one-place config pattern, and a 410 handler tested on mocks."
topics: ["devops"]
tags: ["workers-ai", "cloudflare-workers", "model-deprecation", "wrangler", "claude-api", "change-control", "grep"]
cover: /covers/workers-ai-retired-model-ids-grep-config.png
seo:
  primaryQuery: "workers ai model deprecation 410 5028"
  secondaryQueries:
    - "workers ai deprecated models november 20 2026"
    - "find @cf model ids in wrangler config"
    - "workers ai 5028 model deprecated error"
---

The Workers AI model catalog lost 24 models on Nov 20, 2026. Cloudflare's changelog says those models "will stop returning responses" and that requests to them fail with an HTTP `410 Gone` and error code `5028`. Today is Nov 24. The date has passed.

The part I find easy to miss is the date itself. The first notice said Nov 15. Cloudflare then wrote that it "moved the deprecation date to November 20, 2026." If your team planned around Nov 15, you may have read the notice, relaxed after the extension, and never looked again.

I did not call Cloudflare for this post, and I will not tell you how many apps broke or what your account sees. I have one question, and it is small: can someone on your team list, in one minute, every file that names an `@cf/` model? If the answer is "probably," this post is for you.

<!--more-->

The grep below takes about a minute. The config change takes an afternoon. The third piece, a 410 handler, is what makes the next retirement a log line instead of a support ticket. And because the same shape is coming from Anthropic on Nov 30 and Jan 22, the script I wrote covers those dates too.

## What Cloudflare actually said

I re-read the changelog entry dated Nov 5 and the Workers AI errors page this morning. Here is the part that matters.

| Item | What the page says |
|---|---|
| Original date | Nov 15, 2026 |
| Current date | Nov 20, 2026 ("moved the deprecation date") |
| Count | Twenty-four models (16 LLMs, 8 "other models") |
| After the date | Requests "will fail with an HTTP `410 Gone` error and error code `5028`" |
| Error table row | `5028`, HTTP `410`, "`${model}` was deprecated on `${date}`" |
| Advice | Move to newer models; check the pricing page |

The "other models" are not chat models. They include a text-to-speech model, four image models, a speech-to-text model, a vision model and an embedding model. Each has a suggested replacement on the page. The embedding replacement, `@cf/google/embeddinggemma-2`, is marked "available soon," so for that one the page gave you nowhere to move yet.

I compared the page against the list inside my script by machine: all 24 IDs match, and the only extra IDs on the page are the replacements. That check is why I trust the list below more than a copy I typed from memory.

![Timeline: Nov 5 notice, Nov 15 original date, Nov 20 new date when Workers AI models stop answering, today Nov 24, Nov 30 Claude Sonnet 4.5 retires, Jan 22 Claude Opus 4.5 retires.](/img/workers-ai-retired-model-ids-grep-config-1.png)

Two things this post does not claim. First, it does not claim a replacement behaves like the old model. Cloudflare lists replacements; whether your prompts, your token limits and your cost survive the swap is something you test. Second, it does not claim your app is down. A retired model ID only hurts if some code path still sends it.

## Step 1: a grep that lists every Workers AI model you name

Start with the dumbest tool that works. This prints every `@cf/` model ID in a repo, retired or not:

```bash
grep -rnoE "@cf/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+" . \
  --exclude-dir={.git,node_modules,vendor,.venv,.wrangler}
```

Here is what it printed on a throwaway folder I built for this post. The folder has five small files that imitate common setups: a Worker, an embedding helper, a Python voice script, a `.dev.vars` file and a Wrangler config.

```text
./wrangler.jsonc:8:@cf/moonshotai/kimi-k2.6
./wrangler.jsonc:9:@cf/meta/llama-3.1-8b-instruct
./scripts/voice.py:3:@cf/myshell-ai/melotts
./src/embed.ts:2:@cf/google/embeddinggemma-300m
./src/embed.ts:3:@cf/black-forest-labs/flux-2-klein-9b
./src/index.ts:3:@cf/meta/llama-3.1-8b-instruct-fp8
./.dev.vars:1:@cf/qwen/qwq-32b
```

Seven IDs in five files, and one of them (`.dev.vars`) is a dotfile that many editors hide. Read that list by eye and you will probably miss which ones are retired. Notice the trap in lines 2 and 6: `llama-3.1-8b-instruct` and `llama-3.1-8b-instruct-fp8` differ by a suffix. Only the `-fp8` one is on Cloudflare's list. I make no claim about the other; it is simply not on this notice.

## Step 2: a script that knows the retired list

A grep cannot tell you which hits are on the notice, so the next script holds the 24 IDs and matches each one exactly. It matches whole IDs only, so `llama-3.1-8b-instruct` does not trigger the `-fp8` entry. It also holds the two Claude retirements, because the same question applies. It uses only the Python standard library.

```python {linenos=inline}
#!/usr/bin/env python3
"""List retired or retiring model IDs in a repo.

Usage: python3 audit_model_ids.py [path] [--today YYYY-MM-DD]
Exit code 1 when a retired or retiring ID is found.
"""
import re
import sys
from datetime import date
from pathlib import Path

# Workers AI: Cloudflare changelog of 2026-11-05. Stopped answering 2026-11-20.
WORKERS_AI = """
@cf/deepseek-ai/deepseek-r1-distill-qwen-32b @cf/nvidia/nemotron-3-120b-a12b
@cf/deepseek-ai/deepseek-v4-pro-0813 @cf/deepseek-ai/deepseek-v4-flash-0731
@cf/qwen/qwq-32b @cf/qwen/qwen3-30b-a3b-fp8 @cf/moonshotai/kimi-k2.6
@cf/moonshotai/kimi-k2.7-code @cf/zai-org/glm-5.2 @cf/zai-org/glm-5.3-flash
@cf/meta-llama/llama-2-7b-chat-hf-lora @cf/google/gemma-2b-it-lora
@cf/google/gemma-7b-it-lora @cf/meta/llama-3.1-8b-instruct-fp8
@cf/meta/llama-3.2-1b-instruct @cf/meta/llama-3.2-3b-instruct
@cf/myshell-ai/melotts @cf/stabilityai/stable-diffusion-xl-base-1.0
@cf/runwayml/stable-diffusion-v1-5-inpainting
@cf/bytedance/stable-diffusion-xl-lightning @cf/lykon/dreamshaper-8-lcm
@cf/openai/whisper-tiny-en @cf/llava-hf/llava-1.5-7b-hf
@cf/google/embeddinggemma-300m
""".split()

# (pattern, date it stops, label). Claude dates: model-deprecations page.
DATED = [(re.escape(m) + r"(?![A-Za-z0-9._-])", date(2026, 11, 20), "Workers AI")
         for m in WORKERS_AI]
DATED += [
    (r"claude-sonnet-4-5(?:-20250929)?(?![0-9])", date(2026, 11, 30), "Claude Sonnet 4.5"),
    (r"claude-opus-4-5(?:-20251101)?(?![0-9])", date(2027, 1, 22), "Claude Opus 4.5"),
]
COMPILED = [(re.compile(p), d, label) for p, d, label in DATED]

SKIP = {".git", "node_modules", "vendor", ".venv", "dist", "build", ".wrangler"}
NAMES = {".dev.vars", ".env", "wrangler.toml", "wrangler.json", "wrangler.jsonc"}
SUFFIXES = {".ts", ".js", ".mjs", ".py", ".php", ".json", ".jsonc", ".toml",
            ".yaml", ".yml", ".env", ".sh", ".md"}


def main(root: Path, today: date) -> int:
    hits = 0
    for p in sorted(root.rglob("*")):
        if not p.is_file() or SKIP & set(p.parts):
            continue
        if p.name not in NAMES and p.suffix not in SUFFIXES:
            continue
        for n, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
            for rx, when, label in COMPILED:
                m = rx.search(line)
                if not m:
                    continue
                days = (when - today).days
                state = f"GONE since {when}" if days <= 0 else f"stops {when} ({days}d)"
                print(f"{state:24} {p.relative_to(root)}:{n}  {m.group(0)}  [{label}]")
                hits += 1
    print(f"\n{hits} hit(s).")
    return 1 if hits else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    today = date.today()
    if "--today" in sys.argv:
        today = date.fromisoformat(sys.argv[sys.argv.index("--today") + 1])
        args = [a for a in args if a != sys.argv[sys.argv.index("--today") + 1]]
    sys.exit(main(Path(args[0] if args else "."), today))
```

Run on the same folder with `--today 2026-11-24`, it prints:

```text
GONE since 2026-11-20    .dev.vars:1  @cf/qwen/qwq-32b  [Workers AI]
GONE since 2026-11-20    scripts/voice.py:3  @cf/myshell-ai/melotts  [Workers AI]
stops 2026-11-30 (6d)    scripts/voice.py:4  claude-sonnet-4-5-20250929  [Claude Sonnet 4.5]
stops 2027-01-22 (59d)   scripts/voice.py:5  claude-opus-4-5  [Claude Opus 4.5]
GONE since 2026-11-20    src/embed.ts:2  @cf/google/embeddinggemma-300m  [Workers AI]
GONE since 2026-11-20    src/index.ts:3  @cf/meta/llama-3.1-8b-instruct-fp8  [Workers AI]
GONE since 2026-11-20    wrangler.jsonc:8  @cf/moonshotai/kimi-k2.6  [Workers AI]

7 hit(s).
```

Five Workers AI hits, one Sonnet hit, one Opus hit. The non-`fp8` line stayed quiet, as intended. The exit code is 1, so you can put it in CI and let it fail the build the next time a date lands.

The Claude rows come from Anthropic's model-deprecations page, which I also re-read this morning. It says `claude-sonnet-4-5-20250929` retires Nov 30, 2026, with `claude-sonnet-5-5` as the replacement. It says that on Nov 23 Anthropic notified developers about Claude Opus 4.5: retirement Jan 22, 2027, deprecated model `claude-opus-4-5-20251101`, replacement `claude-opus-5-5`, and that "this retirement includes `claude-opus-4-5`, the same model's ID without a date." That is why the Opus pattern catches both spellings. The Sonnet side, including the settings that break after a swap, is covered in [Two Claude API Calls Stop Working on Nov 30](/blog/claude-api-two-calls-stop-nov-30/). I will not repeat it here.

### What a grep cannot see

A script over a repo finds what the repo says. It cannot find these:

- A model name stored in a database row or a KV entry, such as "which model for which customer."
- A value typed into a dashboard variable and never committed.
- Another team's Worker in the same Cloudflare account.
- A no-code tool or a notebook that calls the API directly.

For those, I would search your request logs for the text `5028` or `was deprecated on`, since that is the wording on Cloudflare's error page. If you keep no logs, the first user report is your log. Plan the next one differently, which is the next section.

## Step 3: put the model ID in one place

When a model name is a string literal inside a function, a retirement means a code change in whichever function someone forgot. When the name is one config value, a retirement is one edit that a reviewer can read in ten seconds.

Here is the Wrangler config after the change. The binding is the same one the Workers AI docs show (`"ai": { "binding": "AI" }`, available as `env.AI`). The model IDs move into `vars`:

```jsonc
{
  "name": "support-bot",
  "main": "src/index.ts",
  "compatibility_date": "2026-11-01",
  "ai": { "binding": "AI" },
  "vars": {
    // Replacements come from the Nov 5 changelog. Test your prompts before you ship.
    "CHAT_MODEL": "@cf/zai-org/glm-5.3",
    "CHAT_MODEL_FALLBACK": "@cf/google/gemma-4-26b-a4b-it"
  }
}
```

I picked these because the changelog lists them: `@cf/zai-org/glm-5.3` under "frontier model needs," and `@cf/google/gemma-4-26b-a4b-it` under "smaller model needs." I did not compare them. Quality, latency and cost are yours to test. I left the embedding model out of the config on purpose: its replacement was "available soon" when I read the page, so check the catalog before you point production at it.

Two details make this pattern pay off:

1. **Keep one name per job, not per call site.** `CHAT_MODEL` is "the model for the reply endpoint." If the summarizer and the reply endpoint share a model today but could diverge tomorrow, give them separate names.
2. **Keep a fallback, but a different one.** A fallback to a model from the same notice is worse than no fallback. It looks safe in review.

![Before: the model ID appears in five places across code, env files, scripts and a dashboard. After: one vars block in the Wrangler config feeds the code, with a fallback and a logged error.](/img/workers-ai-retired-model-ids-grep-config-2.png)

## Step 4: treat 410 as a named error

A config change finds the next retirement faster. A handler makes the failure readable when you miss it. The Workers AI docs show the call as `env.AI.run(model, input)`, and the errors page gives the code, the status and the message text. I wrote one small wrapper around that call:

```ts {linenos=inline}
export interface Env {
  AI: { run(model: string, input: unknown): Promise<unknown> };
  CHAT_MODEL: string;
  CHAT_MODEL_FALLBACK?: string;
}

export class ModelRetiredError extends Error {
  tried: string[];
  constructor(tried: string[]) {
    super(`Workers AI model retired: ${tried.join(", ")}`);
    this.tried = tried;
  }
}

// Cloudflare's error table: 5028 / HTTP 410 / "<model> was deprecated on <date>".
export function isRetired(err: unknown): boolean {
  const e = err as { status?: number; code?: number | string; message?: string };
  const text = String(e?.message ?? err);
  return e?.status === 410 || Number(e?.code) === 5028 || /\b5028\b|was deprecated on/.test(text);
}

export async function runChat(env: Env, input: unknown): Promise<unknown> {
  const models = [env.CHAT_MODEL, env.CHAT_MODEL_FALLBACK].filter(Boolean) as string[];
  const tried: string[] = [];
  for (const model of models) {
    tried.push(model);
    try {
      return await env.AI.run(model, input);
    } catch (err) {
      if (!isRetired(err)) throw err; // 429, 400, timeouts: not our business here
      console.error(JSON.stringify({ event: "workers_ai_model_retired", model }));
    }
  }
  throw new ModelRetiredError(tried);
}
```

The wrapper does three things. A retired model moves to the fallback and logs a structured line you can alert on. If every model is retired, it throws one error that names every model it tried. Any other error, such as a `429` with code `3040` from the errors table, is rethrown untouched, so a busy day never looks like a retirement.

I tested it with four cases in Node, against a fake `env.AI` that throws on purpose:

```text
1 pass: fell back after 410/5028 -> @cf/old -> @cf/new
2 pass: ModelRetiredError names both models
3 pass: 429 rethrown, fallback not called
4 pass: message-only error recognised
```

This is the honest limit of that test. The fake errors have the shape I assumed: a `status`, a `code`, and the documented message text. I did not call Workers AI, so I have not seen what `env.AI.run` throws for a retired model on your account. That is why `isRetired` accepts any one of three signals, and why you should run one real call against a retired ID in a preview environment and read what comes back before you trust the check.

{{< field-note title="Field note" >}}
On the Laravel and Vue projects I maintain, I hold myself to the same rule: a model name is configuration, never a literal inside a service class. In Laravel that means a `config/ai.php` key read from an environment variable, one key per job. I did not audit those projects for this post, so I am not telling you a story about a rescue. I am telling you what I would look at first: whether a retirement date forces a code review, or just a config review. The question is not whether the replacement is better. It is whether you can change the name, see the change, and undo it in the same afternoon.
{{< /field-note >}}

## The same shape is coming from other places

Two dates on the Claude side are close enough to matter this week, and the same script and the same config pattern apply:

| Provider | ID | Date | Replacement named by the provider |
|---|---|---|---|
| Cloudflare Workers AI | 24 `@cf/` IDs (list above) | Nov 20, 2026 (passed) | See the changelog table |
| Anthropic | `claude-sonnet-4-5-20250929` (and `claude-sonnet-4-5`) | Nov 30, 2026 | `claude-sonnet-5-5` |
| Anthropic | `claude-opus-4-5-20251101` (and `claude-opus-4-5`) | Jan 22, 2027 | `claude-opus-5-5` |

Anthropic's page says it gives "at least 60 days' notice before model retirement for publicly released models." From Nov 23 to Jan 22 is 60 days, so the Opus window is the full length. The Sonnet window is nearly gone. Cloudflare's entry is dated Nov 5, first said Nov 15, and was later moved to Nov 20. I would not plan around the idea that every provider gives you two months.

If you want a wider view of keeping a coding agent and its tools on a short leash, the checklist lives under [/ai-agent-operations/](/ai-agent-operations/), and the cost side of a Cloudflare account is in [why a Cloudflare spending limit covers the whole account](/blog/cloudflare-workers-spending-limit-whole-account/).

## What this post is not saying

- It is not saying your Worker is failing. I did not see your traffic.
- It is not saying a replacement model is a drop-in. Cloudflare says to move to newer models "for the best token efficiency and throughput." That is their statement, not my measurement.
- It is not saying a fallback list is always right. A fallback that quietly answers with a weaker model can hide a retirement for weeks, which is why the wrapper logs every time it uses one.
- It is not a measurement of how many apps use these models. I do not have that number.

## What you should do Monday morning

1. Run the `grep` from Step 1 in every repository that talks to Workers AI, including the ones owned by people who left. Read the `.dev.vars` file too.
2. Run `audit_model_ids.py` and read every line. Treat "GONE" as a bug today and "stops" as a dated ticket with an owner.
3. Search your Worker logs for `5028` and `was deprecated on`. If a hit shows up, you now know which route and which customer.
4. Move each model name into one `vars` entry, one per job, and pick a fallback from outside the retired list.
5. Add the `runChat` wrapper (or your own), and make `workers_ai_model_retired` an alert instead of a log you read later.
6. Run one real call against a retired ID in a preview environment, and write down the exact error you get. Fix `isRetired` if it differs from what I assumed.
7. Put the script in CI with a date list, so the next retirement fails a build before it fails a user.

## Further reading

{{< source href="https://developers.cloudflare.com/changelog/post/2026-11-05-planned-model-deprecations/" label="Cloudflare changelog: Planned model deprecations on Workers AI" >}}

{{< source href="https://developers.cloudflare.com/workers-ai/platform/errors/" label="Workers AI: Errors" >}}

{{< source href="https://developers.cloudflare.com/workers-ai/configuration/bindings/" label="Workers AI: Workers bindings" >}}

{{< source href="https://platform.claude.com/docs/en/about-claude/model-deprecations" label="Claude Platform: Model deprecations" >}}

More tool notes are under [/developer-tools/](/developer-tools/), and new readers should start at [/start-here/](/start-here/).
