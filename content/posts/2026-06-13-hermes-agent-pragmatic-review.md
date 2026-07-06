---
title: "A pragmatic review of Hermes Agent after six months"
date: 2026-06-13
description: "It's a personal AI agent. It's not a product for end-users. With that frame, it works better than anything else I've tried. Here's what works, what doesn't, and when I'd reach for something else."
topics: ["tools"]
tags: ["ai", "agents", "review", "hermes"]
draft: false
cover: "/covers/tools-cover.png"
author: "Shinjae Kang"
authorRole: "Senior Software Developer"
authorLocation: "Jakarta, Indonesia"
seo:
  primaryQuery: "Hermes Agent review"
  secondaryQueries:
    - "Hermes Agent practical review"
    - "local AI agent workflow"
    - "AI agent automation review"
---

I have been running Hermes as my primary AI agent for about six months. This is a pragmatic review — not sponsored, not a teardown. Just notes from daily use.

## What it is, and what it isn't

Hermes is a **personal AI agent**. It runs locally, talks to a CLI, a Telegram bot, a Slack workspace, a TUI, and a desktop app — all from the same core. It has skills, memory, scheduled jobs, and the ability to spawn sub-agents.

It is **not** a SaaS product. You run it on your own server (or your laptop). You bring your own API keys. You maintain the thing.

With that frame in mind, it's the best personal agent I've used.

## What works

- **Skills.** Once you've trained yourself to think in skills (one `.md` file per workflow), the rest of the agent setup gets out of your way. The skill system is the killer feature.
- **Memory.** Long-running sessions don't forget what matters. The 7-day-rolling built-in memory is small but well-curated; the optional supermemory backend is great when you have many sessions over time.
- **Scheduled jobs.** The cron system is reliable. I have it running ~15 jobs daily (server monitoring, email digests, social posting, content drafting) and haven't had a job silently fail in months.
- **Sub-agent delegation.** When a task has 3+ independent steps, spawning sub-agents is the right move. The system handles the parallelism well.

## What doesn't work

- **The terminal sandbox.** It's slow. Any heavy terminal work in the agent loop is going to feel sluggish.
- **The first session is rough.** A new install takes 30+ minutes of configuration. That's not unreasonable for a power-user tool, but it sets the wrong expectations.
- **The docs are excellent but sprawling.** The same information is sometimes in three places. Search is your friend.
- **Memory limits are real.** The built-in memory is intentionally small. If you need to keep a lot of context across sessions, you'll need the supermemory backend, which is its own subscription.

## When I'd reach for something else

- **If I just need a chatbot.** Use ChatGPT or Claude.ai directly. Hermes is overkill.
- **If I need an enterprise product with SSO, audit logs, and a sales team.** Hermes is not that. Use a SaaS agent platform.
- **If I'm not willing to maintain a server.** The maintenance burden is small but non-zero. If you want zero ops, use a hosted product.

## The one thing that might surprise you

The thing I didn't expect: **the agent's value scales with how much you invest in your own skills and memory.** The agent I have today is meaningfully better than the one I had three months ago — not because the software changed much, but because I've written better skills and curated better memory. It's a system that rewards investment.

---

_I keep my full setup notes at [github.com/zemnanet/hermes-config](https://github.com/zemnanet/hermes-config) (mirror only — the real config is on my server)._

{{< field-note title="Field note" >}}
The useful part of an agent is not the chat transcript. It is the repeatable operating loop around tools, files, cron jobs, and verification. If that loop is not inspectable, the agent feels impressive but cannot be trusted for daily work.
{{< /field-note >}}

## What you should do Monday morning

1. Choose one recurring assistant task.
2. Add a real verification step that produces a file, status code, or diff.
3. Keep the task only if the next run can prove what changed.

## Refresh note

This piece is now part of the site's operating archive. Read it as a decision pattern, not as a frozen news item: check whether the tool, model, or platform detail has changed, then keep the underlying verification habit if it still reduces operational risk.

## Deep refresh
## What changed after using it longer

The part I keep coming back to is not model quality. Model quality changes every month. The durable question is whether an agent can live inside an operating system of checks.

A chat-first assistant feels useful when the task is small. A local agent becomes useful when it can touch files, inspect previous work, run commands, schedule follow-up checks, and report back with evidence. That is also where it becomes risky. Once an assistant can act, you need stronger boundaries than "please be careful."

My practical checklist for an agent environment is now:

1. Can it read the source of truth directly?
2. Can it modify files through reviewable diffs?
3. Can it run the same verification command a human would run?
4. Can it remember durable preferences without saving temporary noise?
5. Can scheduled jobs produce artifacts that later tasks can read?
6. Can it fail loudly when a tool or network call blocks the real path?

Hermes fits my workflow best when I treat it as an operations shell with reasoning attached. It is less useful when I treat it as a magic worker that should know everything without inspecting the system.

## Where I still keep guardrails

I do not let agent confidence replace verification. If the task touches deployment, content publishing, cron jobs, or external APIs, the final answer has to be backed by a command result, file diff, HTTP status, or another concrete handle.

That sounds strict, but it prevents a common failure: the assistant says a thing is done because the plan is coherent, not because the artifact exists.

The rule I use is simple: no artifact, no completion.

For a coding task, the artifact is usually a diff and test output. For a blog task, it is a built page and live URL. For a social task, it is a scheduled post ID or a clear blocker. For a cron task, it is the next run time, the script path, and the saved output location.

## Practical setup I would repeat

If I were setting this up again from zero, I would start with three workflows instead of trying to automate everything:

| Workflow | First useful automation |
|---|---|
| Blog publishing | Build, metadata audit, image check, live URL verification. |
| Social scheduling | Read latest analytics, propose one experiment, wait for approval when needed. |
| Server monitoring | Alert only on thresholds that require a human decision. |

The important part is to make each workflow closed-loop. A daily blog job should read yesterday's strategy. A social job should read analytics. A monitoring job should stay silent when there is nothing useful to say.

That is the difference between an assistant that performs activity and an assistant that compounds judgment.

## Related operating notes

- [Closed Loop Beats More Automation](/blog/closed-loop-beats-more-automation/)
- [Zero-Cost Observability for Agent Crons](/blog/zero-cost-observability-agent-crons/)
- [Developer Tools and Model Choices](/developer-tools/)

## What would make the setup fail

The setup fails when every successful run depends on private context in my head.

That is why I now prefer visible artifacts over clever prompts. If an agent needs to know how to publish a post, the steps should be in the repo or a script. If an agent needs analytics, the output should be saved where the next job can read it. If a cron job makes a decision, the inputs should be visible after the run.

This is slower on day one, but faster after the third repeat. The assistant stops being a one-off helper and becomes part of the operating system.

## How to verify this advice

Treat this as a small operating experiment around **Hermes Agent operations**.

The failure mode to watch is **assistant activity without proof**. It usually does not look dramatic at first. It looks like one convenient shortcut, one skipped check, or one tool decision that nobody writes down. A month later, the team has more output but less confidence in what actually changed.

A practical verification loop has four parts.

1. **Name the decision.** Write the decision in one sentence. If the team cannot name it, the team cannot improve it.
2. **Name the evidence.** Decide what would prove the decision helped. That might be a passing test, a smaller diff, a faster rollback, a lower bill, a clearer support path, or a page that earns impressions in Search Console.
3. **Name the counter-signal.** Decide what would prove the decision is not working. This prevents the team from defending a bad choice just because it was exciting at the start.
4. **Name the next review date.** A decision without a review date becomes architecture sediment.

For this topic, the metric I would watch is **artifact-backed completion**.

That metric does not need to be perfect. It only needs to be concrete enough that the next review is not based on memory. If the metric improves, keep the pattern and document it. If the metric stays flat, change the approach. If the metric gets worse, rollback or narrow the scope.

This is the operating habit I want the site to teach. A post should not end with a clever opinion. It should leave the reader with a way to test the opinion in their own repo, workflow, or team.

The same habit connects the rest of the site: [Start Here](/start-here/), [AI Agent Operations](/ai-agent-operations/), [Laravel and Vue SaaS Notes](/laravel-vue-saas/), and [Developer Tools and Model Choices](/developer-tools/). The topics are different, but the standard is the same: choose deliberately, leave proof, and keep the exit path visible.
