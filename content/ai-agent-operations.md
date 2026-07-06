---
title: "AI Agent Operations"
date: 2026-07-06T21:50:00+07:00
draft: false
description: "A curated hub for building AI agent workflows that leave proof, avoid zombie tasks, survive provider changes, and fit real software operations."
---

AI agents are useful when they become part of operations, not when they only produce impressive transcripts.

This hub collects the posts on agent boundaries, cron verification, repository maps, model portability, and artifact proof. Read these as a working system: each article answers one failure mode in the same operating loop.

## Start with the operating contract

1. [The Agent Edit Contract I Use Before a Coding Agent Touches a Repo](/blog/the-agent-edit-contract-i-use-before-a-coding-agent-touches-a-repo/)
2. [Your Coding Agent Needs a Map, Not a Bigger Context Window](/blog/your-coding-agent-needs-a-map-not-a-bigger-context-window/)
3. [Long-Running AI Agents: From Demos to Production](/blog/long-running-ai-agents-from-demos-to-production/)

The goal is simple: the agent should know the repo boundary before it starts, and the human should know what evidence to inspect when it finishes.

## Then add proof to scheduled work

1. [Why AI Cron Jobs Lie to You: The Exit 0 With Empty Output Pattern](/blog/why-ai-cron-jobs-lie-to-you-the-exit-0-with-empty-output-pattern/)
2. [Your Cron Job Is Not Healthy Until the Artifact Proves It](/blog/your-cron-job-is-not-healthy-until-the-artifact-proves-it/)
3. [Zero-Cost Observability for Agent Crons](/blog/zero-cost-observability-agent-crons/)
4. [Your AI Agent Pipeline Has No Zombie Detection](/blog/your-ai-agent-pipeline-has-no-zombie-detection-heres-how-to-add-it/)

If a scheduled agent cannot prove what changed, it is not automation yet. It is a diary entry with a timestamp.

{{< field-note title="Operating lens" >}}
For a small team, the practical question is not "which agent is smartest?" The practical question is "which agent leaves behind enough proof for the next operator to trust or rollback the result?"
{{< /field-note >}}

## Keep tools portable

1. [AI Agent Frameworks in 2026: What the Comparison Charts Don't Tell You](/blog/ai-agent-frameworks-in-2026-what-the-comparison-charts-dont-tell-you/)
2. [The AI Coding Agent Arms Race: Why Model Portability Matters More Than Benchmarks](/blog/the-ai-coding-agent-arms-race-why-model-portability-matters-more-than-benchmarks/)
3. [I Swapped My LLM Backend: The API Call Worked on the First Try](/blog/i-swapped-my-llm-backend-the-api-call-worked-on-the-first-try/)
4. [Open Weights Just Ate the API Margin](/blog/open-weights-api-margin/)

The stable asset is not a provider. It is the contract around prompts, tools, tests, fallbacks, and cost.

## What to do Monday morning

1. Pick one agent workflow that matters.
2. Add a repo map, an artifact check, and a rollback command.
3. Do not scale the workflow until the next run can prove what changed.
