---
title: "A pragmatic review of Hermes Agent after six months"
date: 2026-06-13
description: "It's a personal AI agent. It's not a product for end-users. With that frame, it works better than anything else I've tried. Here's what works, what doesn't, and when I'd reach for something else."
topics: ["Tools"]
tags: ["ai", "agents", "review", "hermes"]
draft: false
cover: "/covers/tools-cover.png"
author: "Shinjae Kang"
authorRole: "Senior Software Developer"
authorLocation: "Jakarta, Indonesia"

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
