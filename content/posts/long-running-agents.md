---
title: "Long-Running AI Agents — From Demos to Production"
date: 2026-06-19
draft: false
cover: /covers/long-running-agents.png
topics: ["ai-agents", "software-engineering", "devops", "llm"]
---

Anthropic found that even frontier models fail 4 specific ways when you let them work longer than 5 minutes. I hit all of them before I figured out the fix.

Not in theory. In practice. I had an agent that was supposed to build a working authentication module over a weekend. By Monday morning it had committed 23 times, declared the feature done three separate times, and left the app in a state where `npm start` didn't even work. The commits looked great in the log. The code did not work.

That weekend cost me two days of debugging. But it taught me more about agent orchestration than any paper or demo. This post is what I wish someone had written before I started.

## The 4 Failure Modes (And Why They Happen)

Anthropic's research on long-running agents identified four specific failure modes that show up consistently when you push past the 5-minute mark. Understanding them is the first step to fixing them.

**1. Declaring victory too early.** The agent finishes a visible part of the task, reports success, and stops. The auth routes exist but tokens never expire. The API returns 200 but the response body is wrong. The agent sees a green checkmark in its own output and calls it done.

**2. Leaving buggy state.** The agent makes a change, hits an error, works around it, and moves on. But the workaround introduced a silent bug — a missing migration, a hardcoded URL, a race condition that only shows up under load. The agent doesn't circle back.

**3. Marking features done prematurely.** This is the most dangerous one. The agent maintains some kind of task list and marks items complete based on whether code was written, not whether the code works. A feature marked "done" in the task tracker can be completely broken in production.

**4. Spending time figuring out how to run the app.** The agent burns 30 minutes trying to figure out the project's build system, another 20 on environment variables, and another 15 on why Docker won't start. Zero minutes on actual engineering.

These aren't model problems. They're orchestration problems. The model is capable. The system around it is not.

![Four failure modes of long-running AI agents — premature victory declaration, buggy state, premature feature marking, and environment setup cycles](/images/long-running-agents-inline-1.png)

## The Initializer Agent Pattern

The first pattern that actually worked for me came from Anthropic's playbook: the **initializer agent**. Instead of telling one agent to build an entire feature, you split the work into two phases.

The initializer agent does one thing: it reads the codebase, understands the structure, and sets up the project scaffolding. A feature list file with a structured JSON list of end-to-end feature descriptions. A git repository. An `init.sh` script that can run the development server. A progress notes file that the next agent will read. Not code. The scaffolding for code.

```yaml
# initializer-agent.yaml
role: |
  You are an initializer agent. Your job is to read the codebase
  and produce an implementation plan. Do NOT write any code.

  Output format:
  1. Files to create (with paths)
  2. Files to modify (with specific changes described)
  3. Test strategy
  4. Dependencies to install
  5. Risk areas

context:
  - Full project structure
  - Existing test patterns
  - Current tech stack documentation
```

Then a second agent — the worker — executes that plan one step at a time. One feature. One commit. One test run. Then the next.

This separation matters because it prevents the agent from simultaneously planning and doing, which is where most of the failure modes originate. When an agent is trying to figure out what to build and how to build it at the same time, it cuts corners on both.

## Git Commits as a Recovery Mechanism

Here's a pattern that saved me more than once: **every meaningful agent action produces a git commit**. Not as an afterthought. As the primary unit of progress.

```bash
# Agent workflow after each completed step
git add -A
git commit -m "feat(auth): add JWT token generation

- Implements RS256 signing with rotating keys
- Token expiry set to 24h with refresh token support
- Tests: 12 passing, 0 failing
- Covers: token generation, expiry, refresh flow"
```

Why this works:

- **Recovery.** When the agent goes off the rails — and it will — you `git bisect` to find where things broke. You don't debug the agent's reasoning. You debug the diff.
- **Audit trail.** Every commit tells you what the agent did and why. The commit message is the agent's explanation of its own work.
- **Rollback granularity.** If step 7 of a 12-step plan introduces a bug, you revert step 7. You don't throw away the entire weekend's work.

I run this with a branch-per-agent pattern. The agent works on `feature/auth-module`. When it's done and tests pass, I merge to main. If it fails, the main branch stays clean and I can inspect the mess in isolation.

## Incremental Progress: One Feature at a Time

The Faros 2026 survey found that **85% of developers now use AI tools** in their workflow. Engineering throughput is up. But quality is down. They call this "acceleration whiplash" — the gap between how fast you can generate code and how fast you can verify it works.

The fix is boring and effective: **one feature at a time, verified before moving on.**

Here's what that looks like in practice with a LangGraph workflow:

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class AgentState(TypedDict):
    features: list[str]
    completed: list[str]
    current_feature: str | None
    test_results: dict[str, bool]
    git_sha: str | None

def plan_next_feature(state: AgentState) -> AgentState:
    remaining = [f for f in state["features"] if f not in state["completed"]]
    if not remaining:
        return {"current_feature": None, **state}
    return {"current_feature": remaining[0], **state}

def implement_feature(state: AgentState) -> AgentState:
    # Agent implements ONE feature
    # Commits to git
    # Runs tests
    return state

def verify_and_gate(state: AgentState) -> AgentState:
    # Human gate: did this feature actually work?
    # If yes, mark complete and move to next
    # If no, fix and re-verify
    return state

def should_continue(state: AgentState) -> Literal["continue", "done"]:
    remaining = [f for f in state["features"] if f not in state["completed"]]
    return "done" if not remaining else "continue"

workflow = StateGraph(AgentState)
workflow.add_node("plan", plan_next_feature)
workflow.add_node("implement", implement_feature)
workflow.add_node("verify", verify_and_gate)

workflow.set_entry_point("plan")
workflow.add_edge("plan", "implement")
workflow.add_edge("implement", "verify")
workflow.add_conditional_edges("verify", should_continue, {
    "continue": "plan",
    "done": END
})
```

The key insight: the `verify` step uses **LangGraph's `interrupt()`** for a human checkpoint. The agent doesn't get to decide if its own work is done. That decision belongs to a person, or at minimum to an automated end-to-end test suite that the agent didn't write.

## Context Engineering: The Discipline Nobody Talks About

**Context engineering** — the practice of carefully controlling what information an agent has access to at any given point in time — has emerged as a discipline in its own right in 2026. ByteByteGo's trends report identified persistent always-on agents as a key trend, and the industry is waking up to the fact that context management is what separates agents that drift from agents that deliver.

This matters enormously for long-running agents. A 5-minute task can hold everything in context. A 3-day task cannot. And the quality of your context management directly determines whether the agent stays coherent or drifts into hallucination.

Microsoft Conductor approaches this with explicit **context control modes**:

```yaml
# conductor-workflow.yaml
steps:
  - name: analyze_requirements
    context_mode: accumulate    # Full history available
    model: claude-sonnet-4-20250514

  - name: implement_feature
    context_mode: last_only     # Only the plan, not the analysis
    model: claude-sonnet-4-20250514

  - name: code_review
    context_mode: explicit      # Only specific files passed in
    model: claude-sonnet-4-20250514
    context:
      - src/auth/jwt.ts
      - src/auth/middleware.ts
      - tests/auth.test.ts
```

Three modes, each solving a different problem:

- **`accumulate`** — the agent needs full history. Use this for planning and analysis.
- **`last_only`** — the agent only needs the current plan. Use this for implementation, where old context is noise.
- **`explicit`** — you hand-pick what the agent sees. Use this for review and testing, where irrelevant context causes the agent to make connections that don't exist.

I use a similar pattern in my own setup. Each agent step gets a context manifest — a specific list of files, documentation sections, and previous outputs. The agent doesn't get to "look around" the codebase. It gets exactly what it needs and nothing more.

![Context window visualization showing how different modes allocate tokens across a multi-day agent run](/images/long-running-agents-inline-2.png)

## End-to-End Testing as the Source of Truth

Anthropic's recommendation for Puppeteer MCP — using a real browser to test your agent's work — changed how I validate agent output. Unit tests can pass while the app is broken. A browser doesn't lie.

```typescript
// e2e-test.ts — runs after each agent step
import { chromium } from 'playwright';

async function verifyAuthFlow() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Test 1: Registration
  await page.goto('http://localhost:3000/register');
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'securePassword123');
  await page.click('#submit');
  await page.waitForURL('/dashboard');

  // Test 2: Token refresh
  const cookies = await page.context().cookies();
  const token = cookies.find(c => c.name === 'auth_token');
  if (!token) throw new Error('No auth token after registration');

  // Test 3: Protected route access
  const response = await page.goto('http://localhost:3000/api/protected');
  if (response?.status() !== 200) {
    throw new Error('Protected route inaccessible after auth');
  }

  await browser.close();
  return { passed: true, steps: 3 };
}
```

This test runs after every agent commit. If it fails, the agent's "done" status is revoked and it goes back to fix the issue. No human needed for verification. The browser is the judge.

## The Real Gap: Spend vs. Outcomes

The Faros 2026 Engineering Report tells a story most teams are living right now: volume is up, quality is down, and the gap between the two is widening. The "AI Acceleration Whiplash" — their term for this pattern — shows that throwing more AI at the problem without investing in the surrounding infrastructure just makes the gap bigger.

This isn't because AI tools are bad. It's because we're using them the way we use hammers — swinging at everything and hoping something gets nailed down. The teams that are closing this gap are the ones investing in the unglamorous infrastructure around the agents:

- **State management.** LangGraph, Conductor, or a custom state machine. The agent needs a brain that persists across sessions.
- **Recovery mechanisms.** Git commits, checkpoints, rollback procedures. The agent will fail. The question is how fast you recover.
- **Verification pipelines.** E2E tests, human gates, automated quality checks. The agent doesn't grade its own homework.
- **Context discipline.** Controlled inputs, explicit context modes, no free-roaming access to the codebase.

![Full agent infrastructure — initializer, worker, git, tests, human gate](/images/long-running-agents-inline-2.png)

## What I'd Do Differently

If I were starting over today, here's the stack I'd build on:

1. **Initializer + worker split.** Always. No exceptions. Planning and doing are different cognitive tasks and they need different agent configurations.

2. **Git as the source of truth.** Every agent action is a commit. Every commit is verified. The git log is the project timeline.

3. **Human gates at every feature boundary.** The agent proposes. The human disposes. At least until the verification pipeline is mature enough to replace that gate — and that takes months, not days.

4. **Context control from day one.** Don't wait until the agent starts hallucinating. Build the context manifest system before you need it.

5. **E2E tests written by humans, run by agents.** The test suite is the contract. The agent's job is to fulfill it. The human's job is to define what "fulfill" means.

The agents that work across days aren't smarter than the ones that work across minutes. They're wrapped in better engineering. The model is the easy part. The system around it is where the real work lives.
