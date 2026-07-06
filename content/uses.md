---
title: "Uses"
date: 2026-07-06T21:06:00+07:00
draft: false
description: "The tools, stack, hosting, analytics, and publishing workflow behind zemna.net and the software systems I write about."
---

This page documents the working setup behind zemna.net. It is not a sponsored tool list. It is the stack I use, test, or write about.

## Writing and publishing

| Area | Current choice |
|---|---|
| Site generator | Hugo extended |
| Hosting | Cloudflare Pages |
| Domain | zemna.net |
| Source control | GitHub |
| Writing format | Markdown with Hugo frontmatter |
| Public feed | RSS and JSON feed |
| Design system | Token-driven custom Hugo theme |

The site is intentionally static. Static pages keep the operational surface small: no database, no login, no server runtime, and fewer moving parts to debug.

## Engineering stack I write from

| Area | Tools and systems |
|---|---|
| Backend | PHP, Laravel, REST APIs, SaaS systems |
| Frontend | Vue, JavaScript, CSS, HTML, Flutter |
| Desktop | .NET, C#, WPF, VB |
| Operations | Linux, cron, Cloudflare, observability scripts |
| Automation | Hermes Agent, coding agents, scheduled content and analytics loops |
| Databases | MySQL and application-level reporting workflows |

## AI and agent workflow

The recurring principle is simple: agents need verification, not blind trust.

My agent workflow usually includes:

1. A compact task brief.
2. A repository or system map.
3. Clear edit boundaries.
4. Real command output.
5. Artifact checks.
6. Rollback notes when the work is risky.

That is why many posts focus on artifact health, cron observability, model routing, cost control, and tool portability.

## Analytics and feedback loop

| Signal | Purpose |
|---|---|
| Google Search Console | Search queries, impressions, indexing signals |
| GA4 | Traffic and engagement readbacks |
| Ahrefs Webmaster Tools | SEO diagnostics and external visibility |
| Microsoft Clarity | Session-level UX clues |
| Postiz analytics | Social performance across X, Threads, Instagram, LinkedIn, TikTok |

Content decisions should not be based only on taste. The publishing loop checks search and social signals, then feeds the next topic and format decisions.

## Social publishing

Postiz is the current social publishing and analytics hub.

| Platform | Handle |
|---|---|
| X | @zemnanet |
| Instagram | @zemna |
| Threads | @zemna |
| LinkedIn | linkedin.com/in/zemnanet |
| TikTok | @zemnanet |
| GitHub | github.com/zemna |

## What I optimize for

I prefer tools that are:

- easy to verify
- cheap enough to run continuously
- replaceable when pricing or quality changes
- useful for a solo developer operating across Indonesia and Korea
- boring enough to maintain after the initial excitement fades

That is the lens behind most recommendations on this site.
