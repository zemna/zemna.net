---
title: "Developer Tools and Model Choices"
date: 2026-07-06T21:52:00+07:00
draft: false
description: "A curated hub for choosing developer tools, AI coding agents, model backends, open weights, and design systems without losing operational control."
---

Developer tools are not neutral. They shape review habits, cost structure, portability, and how quickly a small team can recover when a workflow breaks.

This hub collects the posts where the question is not "is the tool impressive?" but "what does this tool make easier or harder to operate?"

## Coding agents and workflow tools

1. [A pragmatic review of Hermes Agent after six months](/blog/a-pragmatic-review-of-hermes-agent-after-six-months/)
2. [OpenCode Dethroned Cursor and Claude Fable 5 Got Suspended](/blog/opencode-fable5-ai-coding-shakeup/)
3. [The Agent Edit Contract I Use Before a Coding Agent Touches a Repo](/blog/the-agent-edit-contract-i-use-before-a-coding-agent-touches-a-repo/)
4. [AI Agent Frameworks in 2026: What the Comparison Charts Don't Tell You](/blog/ai-agent-frameworks-in-2026-what-the-comparison-charts-dont-tell-you/)

The key test is not whether the demo looks autonomous. The key test is whether the tool can operate inside your repo's proof, review, and rollback rules.

## Models and backend choices

1. [GLM 5.2 Just Became the Best Open-Weights Model](/blog/glm-5-2-open-weights/)
2. [Open Weights Just Ate the API Margin](/blog/open-weights-api-margin/)
3. [I Swapped My LLM Backend: The API Call Worked on the First Try](/blog/i-swapped-my-llm-backend-the-api-call-worked-on-the-first-try/)
4. [The AI Coding Agent Arms Race](/blog/the-ai-coding-agent-arms-race-why-model-portability-matters-more-than-benchmarks/)

Benchmarks are useful for narrowing options. Operating cost, fallback behavior, and migration friction decide what survives in a real workflow.

{{< field-note title="Tooling lens" >}}
I prefer tools that keep the exit path visible. A tool can be powerful and still be a bad fit if the prompt, state, cost, or output format cannot move when the vendor changes direction.
{{< /field-note >}}

## Design systems and publishing tools

1. [How I Dissected 54 Design Systems and Transplanted Linear.app DNA Into My Hugo Blog in One Day](/blog/linear-design-system-hugo/)
2. [The quiet consolidation in Korean dev tooling](/blog/the-quiet-consolidation-in-korean-dev-tooling/)
3. [The Indonesian developer scene is having its Linux moment](/blog/the-indonesian-developer-scene-is-having-its-linux-moment/)

Tooling is also positioning. The stack you choose tells readers whether you value speed, control, cost, portability, or polish.

## What to do Monday morning

1. List the tools that would be painful to replace.
2. For each one, write the export, fallback, or adapter path.
3. Keep the tools that make verification easier. Question the ones that only make demos prettier.
