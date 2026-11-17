---
title: "Two Claude API Calls Stop Working on Nov 30: The Model String and the Fast Flag to Search For"
date: 2026-11-17T06:30:00+07:00
draft: false
slug: "claude-api-two-calls-stop-nov-30"
description: "On Nov 30, 2026, the Claude API stops serving claude-sonnet-4-5-20250929 and rejects speed: fast on claude-opus-4-8. Here is how to find both in your code, and why swapping the model string alone breaks the replacement."
topics: ["llm"]
tags: ["claude-api", "claude-sonnet-4-5", "claude-sonnet-5-5", "claude-opus-4-8", "fast-mode", "model-deprecation", "migration", "change-control"]
cover: /covers/claude-api-two-calls-stop-nov-30.png
seo:
  primaryQuery: "claude-sonnet-4-5-20250929 retirement"
  secondaryQueries:
    - "claude opus 4.8 fast mode removal"
    - "claude sonnet 5.5 migration 400 error"
    - "find which claude model my app uses"
---

On Monday, Nov 30, 2026, two kinds of Claude API request stop working. One names a model that retires that day: `claude-sonnet-4-5-20250929`. The other asks for `speed: "fast"` on `claude-opus-4-8`. Anthropic's docs say both in plain words, and on Sept 30 Anthropic notified developers who use Sonnet 4.5.

I do not doubt that someone read the notice. The question I would ask a team today is smaller and harder: can anyone list, in five minutes, every job that still sends that model string? It is easy to lose track of. The string sits in a `.env` file, a YAML agent config, a nightly script somebody wrote in the spring, and a test fixture. Nothing fails in code review. Nothing fails in staging, because staging was set up last month with the new string. Then a job nobody remembers returns errors on a Monday.

The question is not whether you can change a string. It is whether you know every place the string lives, and what else breaks the moment you change it.

<!--more-->

That second part is the one that catches people. The replacement model, `claude-sonnet-5-5`, rejects several settings that the old model accepted. A find-and-replace on the model name turns "it stops on Nov 30" into "it fails today, in a different way." So this post has three jobs: show you where the two calls hide, show you the settings to fix in the same edit, and give you one small test to run before the deadline.

## What the docs say today

I re-read four official Claude Platform pages on Tuesday, Nov 17, 2026: the model deprecations page, the fast mode page, the release notes, and the Sonnet 5.5 migration guide. Here is the short version, with exact words kept where they matter.

| Item | What the page says |
|---|---|
| Model string | `claude-sonnet-4-5-20250929` |
| State today | Deprecated (since Sept 30, 2026) |
| Retirement date | Nov 30, 2026 |
| Recommended replacement | `claude-sonnet-5-5` |
| After retirement | "Requests to retired models fail." |
| Fast mode on `claude-opus-4-8` | Deprecated, removal date Nov 30, 2026 |
| After removal | Requests to `claude-opus-4-8` with `speed: "fast"` "will return an error" |
| Fast mode replacement path | "migrate to Claude Opus 5.5" |
| `claude-opus-4-8` itself | Active, retirement "Not sooner than May 28, 2027" |

![Timeline from Sep 30, when the Sonnet 4.5 notice went out, to today, Nov 17, to Nov 30, when both calls stop. Thirteen days remain.](/img/claude-api-two-calls-stop-nov-30-1.png)

Three details in that table are easy to misread.

**"Tentative."** The column in the deprecations table is headed "Tentative retirement date". The notice section for Sonnet 4.5 lists the same day as a plain "Retirement date." I would plan for Nov 30 and treat any extension as a gift you were not promised.

**Two separate problems.** The first one stops the whole call, because the model is gone. The second one stops only the calls that ask for fast mode. The model itself, `claude-opus-4-8`, stays Active in the table. If you only search for the model string `claude-opus-4-8`, you will find a lot of calls that are fine, and miss which ones are not.

**Which platforms.** The page says its dates apply to Anthropic-operated platforms: the Claude API, Claude Platform on AWS, Claude Models on Google Cloud (Anthropic managed) and Microsoft Foundry. Amazon Bedrock and Claude Models on Google Cloud (Google managed) set their own schedules, and the page says a model's dates "can differ" there. I did not read those tables. If your calls go through Bedrock or Google's managed offering, read their model tables before you trust Nov 30 or any other date.

One more number worth keeping: the docs promise "at least 60 days' notice before model retirement for publicly released models." Sept 30 to Nov 30 is 61 days. The window was fair. It is also now 13 days.

If you run Claude Code or use claude.ai, this post is not about you. It is about API calls that you or your team wrote.

## Find the two calls

The two calls hide in three kinds of places. Search all three.

**1. Code.** A plain text search finds the model string. This works anywhere with a shell:

```bash
# Find both model names. Read each hit: opus-4-8 alone is fine, opus-4-8 + fast is not.
grep -rnE "claude-sonnet-4-5|claude-opus-4-8" . \
  --exclude-dir={.git,node_modules,vendor,.venv}
```

Notice that `claude-sonnet-4-5` without the date also matches. Some teams write a shorter name. I could not find a page that says the short name points at the dated one, so I treat any `claude-sonnet-4-5` hit as a call to fix, and let the first test call prove which model it reaches.

**2. Things that are not code.** The string lives in `.env` files, CI variables, YAML agent configs, a database row that holds "which model for which job," a no-code automation tool, or a notebook. A grep over the repo finds the first three. For the rest, ask the person who set it up. If that person left, this is where Monday goes wrong.

**3. The usage export.** The deprecations page describes an audit that catches callers you do not know about. It says: go to the Usage page in the Claude Console, click Export, and read the CSV, which is "broken down by API key and model." That is the check I would run first, because it finds the key that another team created and forgot. If a row shows `claude-sonnet-4-5-20250929` under a key you do not recognize, you have a person to ask.

![Three places to search: code, config and CI, and the Claude Console usage export. Each feeds one list of calls to fix.](/img/claude-api-two-calls-stop-nov-30-2.png)

### A script that reads each hit for you

The grep above gives you every line with the name. It does not tell you which Opus 4.8 calls ask for fast mode, because the `speed` setting is usually a few lines away. This script, which uses only the Python standard library, handles that. It also lists settings in the same file that fail on the replacement model, which the next section explains.

```python {linenos=inline}
#!/usr/bin/env python3
"""List Claude API calls in a repo that stop working on 2026-11-30.

Usage: python3 audit_claude_models.py [path]
Exit code 1 when anything on the Nov 30 list is found.
"""
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "vendor", ".venv", "dist", "build"}
SUFFIXES = {".py", ".ts", ".js", ".php", ".go", ".rb", ".java", ".cs", ".json",
            ".yaml", ".yml", ".toml", ".env", ".sh", ".txt", ".md"}

SONNET_45 = re.compile(r"claude-sonnet-4-5(-20250929)?\b")
OPUS_48 = re.compile(r"claude-opus-4-8\b")
FAST = re.compile(r"""speed["']?\s*[:=]\s*["']fast["']|fast-mode-2026-02-01""")

# Settings the Sonnet 5.5 migration guide says return a 400 error.
TRAPS = {
    "thinking budget": re.compile(r"budget_tokens"),
    "thinking disabled": re.compile(r"""thinking.{0,60}["']disabled["']"""),
    "sampling setting": re.compile(r"""\b(temperature|top_p|top_k)\b["']?\s*[:=]"""),
    "forced tool choice": re.compile(r"""tool_choice.{0,60}["'](tool|any)["']"""),
    "old output_format": re.compile(r"\boutput_format\b"),
    "old beta header": re.compile(
        r"interleaved-thinking-2025-05-14|fine-grained-tool-streaming-2025-05-14"
    ),
}


def files(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in SUFFIXES and not (SKIP_DIRS & set(p.parts)):
            yield p


def main(root: Path) -> int:
    stops = 0
    for path in files(root):
        lines = path.read_text(errors="ignore").splitlines()
        moving = False
        for n, line in enumerate(lines, 1):
            if SONNET_45.search(line):
                print(f"STOPS NOV 30  {path}:{n}  Sonnet 4.5 model string")
                stops += 1
                moving = True
            if OPUS_48.search(line):
                near = lines[max(0, n - 16): n + 15]
                if any(FAST.search(x) for x in near):
                    print(f"STOPS NOV 30  {path}:{n}  Opus 4.8 next to speed=fast")
                    stops += 1
        if moving:  # this file will be edited, so list the traps in it too
            for n, line in enumerate(lines, 1):
                for label, rx in TRAPS.items():
                    if rx.search(line):
                        print(f"400 ON 5.5    {path}:{n}  {label}")
    print(f"\n{stops} call(s) on the Nov 30 list.")
    return 1 if stops else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
```

Here is what it printed on Tuesday morning, run against a small folder I built for this post. The folder holds four files that imitate common setups: a summarizer with sampling settings and a thinking budget, a review bot on Opus 4.8 with `speed: "fast"`, a classifier with forced tool choice, and a YAML config with the short model name.

```text
STOPS NOV 30  fixture/app/summarize.py:8  Sonnet 4.5 model string
400 ON 5.5    fixture/app/summarize.py:10  sampling setting
400 ON 5.5    fixture/app/summarize.py:11  thinking budget
STOPS NOV 30  fixture/app/review_bot.ts:3  Opus 4.8 next to speed=fast
STOPS NOV 30  fixture/app/classify.py:2  Sonnet 4.5 model string
400 ON 5.5    fixture/app/classify.py:4  thinking disabled
400 ON 5.5    fixture/app/classify.py:6  forced tool choice
STOPS NOV 30  fixture/config/agents.yaml:2  Sonnet 4.5 model string
400 ON 5.5    fixture/config/agents.yaml:3  forced tool choice

4 call(s) on the Nov 30 list.
```

Two limits to know. The script is a text search, so it misses a model name built from pieces at run time (for example `"claude-" + family + "-4-5"`). And it cannot see a prefilled assistant message, which is the sixth thing in the next section; that one you read by eye.

## Changing the string is only the first edit

Now the part that turns a one-line change into a small project. The replacement model, `claude-sonnet-5-5`, refuses settings that Sonnet 4.5 accepted. "Refuses" here means the API answers with HTTP 400, which is its way of saying "this request is invalid," and your call fails with no answer at all.

The Sonnet 5.5 migration guide lists the changes by starting model. For code that runs on Sonnet 4.5 today, these are the ones that return an error:

| If your request has | What Sonnet 5.5 does | What the guide says to do |
|---|---|---|
| `temperature`, `top_p` or `top_k` | 400 error | Remove them |
| `thinking: {"type": "enabled", "budget_tokens": N}` | 400 error | Remove the budget, set an effort level |
| `thinking: {"type": "disabled"}` | 400 error | Send `{"type": "between_tools"}` instead, at `high` effort or below |
| A last message from the assistant (a "prefill") | 400 error | Ask for the format in the system prompt, or use structured outputs |
| `tool_choice` of type `tool` or `any` | 400 error | Use `auto`, mark the tool `strict: true`, say in the prompt when to use it |
| `output_format` | Deprecated; 400 without a beta header | Use `output_config.format` |
| Beta header `interleaved-thinking-2025-05-14` | Not needed | Remove it |
| Beta header `fine-grained-tool-streaming-2025-05-14` | Replaced | Set `eager_input_streaming: true` on the tool |

![The new model name on the left, five settings that return a 400 error on the right: sampling values, thinking budget, thinking disabled, prefilled assistant message, forced tool choice.](/img/claude-api-two-calls-stop-nov-30-3.png)

The error text for each is quoted in the guide, so you can search your logs for it later. Two examples: `"thinking.type.enabled" is not supported for this model` and `This model does not support assistant message prefill. The conversation must end with a user message.`

Here is what the edit looks like for the summarizer from my test folder. This is the before:

```python
resp = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2000,
    temperature=0.2,
    thinking={"type": "enabled", "budget_tokens": 4000},
    messages=[
        {"role": "user", "content": text},
        {"role": "assistant", "content": "Summary:"},   # prefill
    ],
)
```

And this is the after, following the guide line by line:

```python {hl_lines=[2,4,5]}
resp = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2000,
    output_config={"effort": "medium"},
    system="Reply with one short summary paragraph. Start with the summary itself.",
    messages=[{"role": "user", "content": text}],
)
```

Four things changed in that edit, and only one of them is the model name. The sampling setting is gone. The thinking budget became an effort level. The prefill `"Summary:"` became an instruction in the system prompt. The guide's own advice for a prefill that was only a preamble is "ask in the system prompt for a direct answer."

A word on `"effort": "medium"`. That value is my starting point, not a recommendation for your workload. The guide says there is "no fixed mapping from a budget to an effort level, so run your evaluations at two or three levels." The default on the Claude API is `high`, and the guide says the levels are recalibrated, so a setting does not mean what it meant before. Treat the effort level as something you test, not something you copy.

## Calls that succeed, but come back different

Some changes do not return an error. They change what comes back. These are the ones a green test run hides, so they are worth a second look.

**Thinking is on by default.** On Sonnet 5.5, a request with no `thinking` field runs with adaptive thinking. On Sonnet 4.5 the same request ran without it. The guide names three consequences:

- The response can start with `thinking` blocks, so code that reads `content[0].text` breaks or returns nothing.
- In a loop that calls tools, you must pass the `thinking` blocks back unchanged.
- `max_tokens` now covers thinking plus text, and thinking tokens are billed as output tokens. A limit that was generous before can cut an answer short.

The first one is the easiest to fix and the most common to hit. Read the blocks by type:

```python
# Before: breaks when the first block is a thinking block
answer = resp.content[0].text

# After: take the text blocks, whatever comes first
answer = "".join(block.text for block in resp.content if block.type == "text")
```

**More tokens for the same text.** The guide says Sonnet 5.5 uses the Sonnet 5 tokenizer, so against Sonnet 4.5 "the same text produces about 30 percent more tokens, depending on the content." If you set `max_tokens` close to the real answer length, or you watch a monthly token budget, recount. Images are the same story in a larger size: the guide says a 2000×1500 image costs about 2.5 times as many tokens on Sonnet 5.5.

**Notes between tool calls go quiet.** If your agent shows its progress messages to a user, the guide says notes "longer than a sentence or two" now come back as `thinking` blocks, empty by default. No request fails. The interface just stops showing those notes. The fix is a display setting described in the guide, and the symptom is a user asking why the agent went silent.

I am not giving prices or benchmarks here, on purpose. The official pricing page is the place for the cost side. My point is narrower: swapping the string is a test, and the test needs more than a 200 status.

## The fast flag

Now the second call. Fast mode is a request setting that asks for faster output. The fast mode page says it delivers "up to 2.5x higher output tokens per second at premium pricing," and that you opt in with `speed: "fast"`. On Opus 4.8, that setting is deprecated, and the page says plainly what happens next:

> "Removal date: November 30, 2026. After removal, requests to `claude-opus-4-8` with `speed: "fast"` will return an error."

Notice what the docs do not say: a status code. "Will return an error" is all they commit to, so do not write code that depends on a specific number.

You have three honest options, and the right one depends on whether you need the speed.

| Choice | What you do | What to check first |
|---|---|---|
| Drop the flag | Delete `speed` from the request. `claude-opus-4-8` stays Active in the table | You lose the faster output. Does anyone wait on this call? |
| Move to Opus 5.5 | The page names it as the way to keep fast mode | Read the Opus 5.5 migration guide: it is a different model with its own changes |
| Another supported model | The page lists Fable 5.2 and Mythos 5.2 as supporting fast mode | That is a model decision, not a flag decision |

The cheapest fix, if speed is a nice-to-have, is the first one. In code it is a single deleted line:

```diff
 response = client.messages.create(
     model="claude-opus-4-8",
     max_tokens=4096,
-    speed="fast",
     messages=messages,
 )
```

If you also send the beta header `fast-mode-2026-02-01` on that call, remove it in the same edit. The fast mode page lists that header as required for Opus 4.8, and the script above searches for it so the two travel together.

One trap deserves its own paragraph. The fast mode page shows a fallback pattern: catch the rate limit error, remove `speed`, retry. That pattern handles a 429 when you run out of fast capacity. It is not a guard against the flag being removed. Open your retry code and read which errors it catches. If it only catches `RateLimitError`, the removal on Nov 30 sails straight past it.

## Run one test before the deadline

You cannot roll back to a retired model. That sentence is why the order of operations matters. After Nov 30, "put the old model back" is not an option, so the rollback path has to exist before the date, as a switch between old and new that you can flip while both still work.

Put the model string in one place and read it from the environment. Then run one real call against the replacement. This is the script I would start from:

```python
import os

import anthropic

client = anthropic.Anthropic()

# One place for the model string, so the switch and the rollback are one line.
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")

resp = client.messages.create(
    model=MODEL,
    max_tokens=2000,
    output_config={"effort": "medium"},   # start here, then try one level up and down
    system="Answer directly. Start with the answer, not a preamble.",
    messages=[{"role": "user", "content": "Summarize this ticket in two sentences: ..."}],
)

print("model        :", resp.model)
print("stop_reason  :", resp.stop_reason)
print("block types  :", [block.type for block in resp.content])
print("tokens in/out:", resp.usage.input_tokens, resp.usage.output_tokens)

text = "".join(block.text for block in resp.content if block.type == "text")
assert text.strip(), "no text block came back: check block types and max_tokens"
print(text)
```

I want to be exact about what I did with it. I compiled it with Python on Tuesday morning and it compiled. I did not run it, because that needs an API key and I have not called the Claude API for this post. The request shape follows the Sonnet 5.5 migration guide's own example: an effort level, no sampling values, no thinking budget. If your installed SDK rejects `output_config`, update the SDK first; I did not check which SDK release added it.

What the output tells you:

- `stop_reason` should say the model finished. A `refusal` here is new information; the guide says Sonnet 5.5 declines in more categories than Sonnet 5.
- `block types` shows whether a `thinking` block comes first. If it does, every place that reads `content[0]` is a bug.
- The token counts give you the first real number for the cost question, from your own prompt.

Then run your normal tests with `CLAUDE_MODEL=claude-sonnet-5-5` and compare the answers, not just the status. Do this early. The deprecations page says the same in its own words: "Test your applications with newer models well before the retirement date of your current model."

## Name who owns the date

A deadline with no owner turns into a Monday incident. Before you close this tab, write four lines on a ticket:

```text
Claude API retirement, Nov 30, 2026
  Calls found:     ___ (model string)   ___ (opus-4-8 + fast)
  Owner per call:  ____________________   (a name, not a team)
  Switch date:     Wed Nov 25  (leaves Fri and Mon as buffer)
  Rollback until:  Nov 29      (the old model stops on Nov 30)
  Usage export:    checked on ____ by ____  (no unknown API keys)
```

The `Owner per call` line is where this earns its keep. Reading a CSV of API keys is how you find out that "the nightly summarizer" belongs to someone in a team you do not work with. Better to find them on Nov 17 than on Nov 30.

{{< field-note title="Field note" >}}
On the Laravel/Vue SaaS desks I maintain, model names are the kind of setting that gets copied. The usual homes are an `.env` file, a queue job class, and a config array that someone duplicated for a new feature. When a model retires, the search is never "find the one place." It is "find every place a person once copied this to."

To be clear about my own work: I ran the audit script on a folder I built on Tuesday morning to look like those setups, and I read the docs. I did not run it on a production repository and I did not call the Claude API. What I would do on a real project is keep the model string in a single config key per feature, so that a retirement notice becomes a one-line change and a test, not a search through every place the string was ever copied.
{{< /field-note >}}

## What this post is not saying

- It is not saying the replacement model is better or worse for your job. I give no prices and no benchmarks, and the official pages are where those live.
- It is not saying Nov 30 is certain to the hour. The docs call the table dates tentative and do not say a time of day.
- It is not saying your Amazon Bedrock or Google-managed calls stop on Nov 30. The docs say those platforms set their own dates, and I did not read their tables.
- It is not saying `claude-sonnet-5-5` is a drop-in replacement. The migration guide exists because it is not.
- It is not covering Claude Code, claude.ai, or Haiku models. It covers the two API calls above.
- It is not claiming I have migrated anything. I read the pages and ran a text search on a test folder.

## What you should do Monday morning

Monday, Nov 23, is the last Monday before the deadline. Use it.

1. Run `grep -rnE "claude-sonnet-4-5|claude-opus-4-8" .` in every repository you maintain, or run the audit script and read each line it prints.
2. Open the Claude Console, go to Usage, click Export, and read the CSV by API key and model. Write down every key that still shows `claude-sonnet-4-5-20250929` and who owns it.
3. For each Opus 4.8 hit, decide: drop `speed: "fast"`, or move to a model that supports fast mode. Write the decision on the ticket with a name next to it.
4. In each file that holds a Sonnet 4.5 string, search for the six settings in the table: sampling values, thinking budget, `thinking: disabled`, prefill, forced `tool_choice`, `output_format`.
5. Move the model string into one config key per feature, read from the environment.
6. Run the smoke test with `CLAUDE_MODEL=claude-sonnet-5-5`. Read the block types and the stop reason, not only the status.
7. Flip the setting on Wed Nov 25, watch your logs for the two error messages quoted above, and keep the old string available until Sunday, Nov 29.

## What this connects to

This is change control for a model name: a shared setting, a named owner, a way back. I made a similar case in [I Do Not Let a Coding Agent Pick Its Own Model](/blog/coding-agent-model-owner/), where the question was who may change the string. A date like Nov 30 forces the same decision with a clock attached. The rollback side of it is covered in [The Rollback Path Is the Real AI Coding Feature](/blog/ai-coding-rollback-path/), and the habit of writing down who approved a change is in [A Coding-Agent Policy Is Change Control, Not a Settings File](/blog/coding-agent-policy-change-control/).

If you run agents on a schedule, the wider checklist lives in [/ai-agent-operations/](/ai-agent-operations/). Tool notes are under [/developer-tools/](/developer-tools/), and new readers should start at [/start-here/](/start-here/).

## Further reading

{{< source href="https://platform.claude.com/docs/en/about-claude/model-deprecations" label="Claude Platform: Model deprecations" >}}

{{< source href="https://platform.claude.com/docs/en/build-with-claude/fast-mode" label="Claude Platform: Fast mode" >}}

{{< source href="https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide" label="Claude Platform: Claude Sonnet 5.5 migration guide" >}}

{{< source href="https://platform.claude.com/docs/en/models/opus-5-5/migration-guide" label="Claude Platform: Claude Opus 5.5 migration guide" >}}

{{< source href="https://platform.claude.com/docs/en/release-notes/overview" label="Claude Platform: Release notes" >}}
