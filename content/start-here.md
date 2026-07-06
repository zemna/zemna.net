---
title: "Start Here"
date: 2026-07-06T21:05:00+07:00
draft: false
description: "A guided path through zemna.net's core software architecture notes on AI agents, automation proof, tool choices, and maintainable systems."
---

zemna.net is not a news feed. It is a working notebook for software systems that need to survive real maintenance.

If you are new here, read these paths in order.

## 1. Agent boundaries

Start with the contract before the agent touches a repository.

- [The Agent Edit Contract I Use Before a Coding Agent Touches a Repo](/blog/the-agent-edit-contract-i-use-before-a-coding-agent-touches-a-repo/)
- [Your Coding Agent Needs a Map, Not a Bigger Context Window](/blog/your-coding-agent-needs-a-map-not-a-bigger-context-window/)

The core idea: context is not the same as permission. A useful agent needs a map, boundaries, verification, and rollback.

## 2. Automation proof

Automation is only useful when the output can be trusted.

- [Your Cron Job Is Not Healthy Until the Artifact Proves It](/blog/your-cron-job-is-not-healthy-until-the-artifact-proves-it/)
- [Why AI Cron Jobs Lie to You: The Exit 0 With Empty Output Pattern](/blog/why-ai-cron-jobs-lie-to-you-the-exit-0-with-empty-output-pattern/)
- [Zero-Cost Observability for Agent Crons](/blog/zero-cost-observability-agent-crons/)

The core idea: process status is not proof of work. Check fresh artifacts, useful output, and downstream delivery.

## 3. Tool judgment

Tools are useful until they become load-bearing without an exit path.

- [Before You Adopt a Beta Library, Prove the Exit Path](/blog/before-you-adopt-a-beta-library-prove-the-exit-path/)
- [I Swapped My LLM Backend: The API Call Worked on the First Try](/blog/i-swapped-my-llm-backend-the-api-call-worked-on-the-first-try/)
- [Open Weights Just Ate the API Margin](/blog/open-weights-api-margin/)

The core idea: the best tool is the one you can verify, afford, and replace when the assumptions change.

## 4. Frontend systems

Generated UI still needs engineering discipline.

- [Code That Renders Is Not Code You Can Trust](/blog/code-that-renders-is-not-code-you-can-trust/)
- [The JavaScript I Deleted With CSS: A 2026 Survival Guide](/blog/the-javascript-i-deleted-with-css-a-2026-survival-guide/)
- [Vue 3.6 Vapor Mode: No Virtual DOM, No Rewrite](/blog/vue-3.6-vapor-mode-no-virtual-dom-no-rewrite/)

The core idea: correctness includes behavior, accessibility, performance, and future edits.

## 5. Regional context

I write from Indonesia as a Korean programmer and software architect. That context matters because tooling, pricing, hiring, infrastructure, and business constraints are not identical everywhere.

- [The Indonesian developer scene is having its Linux moment](/blog/the-indonesian-developer-scene-is-having-its-linux-moment/)
- [The quiet consolidation in Korean dev tooling](/blog/the-quiet-consolidation-in-korean-dev-tooling/)

## How to use this site

- Use [Topics](/topics/) when you know the engineering area.
- Use [Tags](/tags/) when you know the tool or pattern.
- Use [Search](/) from the header when you remember a phrase.
- Use [RSS](/index.xml) if you prefer quiet updates.
