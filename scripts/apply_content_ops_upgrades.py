#!/usr/bin/env python3
"""Apply editorial operating upgrades to published posts.

Adds, idempotently:
- `seo.primaryQuery` and `seo.secondaryQueries` frontmatter
- one field-note shortcode
- one `What you should do Monday morning` section

The snippets are curated per post so the content stays specific instead of using
site-wide boilerplate.
"""
from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "content" / "posts"

DATA: dict[str, dict[str, object]] = {
    "2026-06-12-ai-senior-developers.md": {
        "primary": "ai replacing senior developers",
        "secondary": ["senior developers and AI", "AI software engineering judgment", "why senior developers still matter"],
        "field": "When I review AI-assisted work, the difference is not whether the model can write a controller or a component. The difference is whether someone notices the missing migration, the weak rollback path, and the quiet product tradeoff. That is still senior work.",
        "monday": ["Pick one AI-generated change from last week.", "Write down the decision a senior reviewer had to make.", "Turn that decision into a reusable checklist item before the next review."],
    },
    "2026-06-13-hermes-agent-pragmatic-review.md": {
        "primary": "Hermes Agent review",
        "secondary": ["Hermes Agent practical review", "local AI agent workflow", "AI agent automation review"],
        "field": "The useful part of an agent is not the chat transcript. It is the repeatable operating loop around tools, files, cron jobs, and verification. If that loop is not inspectable, the agent feels impressive but cannot be trusted for daily work.",
        "monday": ["Choose one recurring assistant task.", "Add a real verification step that produces a file, status code, or diff.", "Keep the task only if the next run can prove what changed."],
    },
    "2026-06-14-indonesian-dev-scene-linux-moment.md": {
        "primary": "Indonesian developer scene Linux moment",
        "secondary": ["Indonesia developers Linux", "Indonesian software engineering ecosystem", "Jakarta developer tools"],
        "field": "In Indonesia, tooling shifts rarely arrive as one official migration. They show up in small decisions: a cheaper server, a Linux-first deploy path, a team member comfortable with terminals, and a project that no longer needs a Windows-only workaround.",
        "monday": ["Audit one workflow that still assumes a specific desktop OS.", "Move the deployment or verification step to a Linux-friendly script.", "Document the exact command so the next developer can repeat it."],
    },
    "2026-06-15-stop-reaching-for-state-library.md": {
        "primary": "stop reaching for a state library",
        "secondary": ["frontend state library overuse", "Vue state management decision", "when not to use state management library"],
        "field": "Most frontend state problems I see are ownership problems first. Before adding a store, name who owns the data, when it expires, and which screen is allowed to mutate it. The library should come after that map, not before it.",
        "monday": ["Pick one shared state object in your app.", "Write its owner, lifetime, and invalidation rule.", "Remove one global state path that is only used by a single screen."],
    },
    "2026-06-16-korean-devtool-consolidation.md": {
        "primary": "Korean developer tooling consolidation",
        "secondary": ["Korean dev tools", "developer tool consolidation", "software tooling market Korea"],
        "field": "Consolidation is easiest to miss when every individual tool still looks useful. The signal is not one tool disappearing. It is the moment procurement, onboarding, and team habit all start preferring the same smaller set.",
        "monday": ["List the tools your team pays for and the tools it actually opens daily.", "Mark every overlap in review, docs, monitoring, and deployment.", "Choose one overlap to remove before buying another seat."],
    },
    "2026-06-16-linear-design-system-hugo.md": {
        "primary": "Linear design system Hugo blog",
        "secondary": ["Hugo design system", "Linear app inspired blog design", "token driven static site"],
        "field": "A design system only starts paying back when future changes become boring. If a color, spacing rule, or card treatment still needs a one-off decision every time, it is not a system yet. It is a memory burden disguised as taste.",
        "monday": ["Pick one repeated component on your site.", "Replace any hard-coded color or spacing with a token.", "Change the token once and verify the component updates everywhere."],
    },
    "2026-06-17-glm-5-2-just-became-the-best-open-weights-model.md": {
        "primary": "GLM 5.2 open weights model",
        "secondary": ["best open weights model", "GLM 5.2 coding", "open weights LLM operations"],
        "field": "A model switch is only real when it survives the boring tests: same prompt, same tool contract, same fallback path, and the same budget ceiling. Benchmarks help shortlist. The operating harness decides whether the model belongs in production.",
        "monday": ["Run one existing coding prompt against your current model and the candidate model.", "Compare diff quality, tool failures, and token cost.", "Do not switch until rollback is a config change, not a rewrite."],
    },
    "2026-06-18-opencode-fable5-ai-coding-agent-shakeup.md": {
        "primary": "OpenCode AI coding agent shakeup",
        "secondary": ["OpenCode coding agent", "AI coding agent market", "Claude Fable suspension"],
        "field": "The lesson from tool shakeups is not to chase every winner. The lesson is to keep your work portable: prompts, test commands, and acceptance checks should survive when the agent shell changes.",
        "monday": ["Move one agent instruction out of a vendor-specific chat and into the repo.", "Add the test command beside it.", "Try the same task with a second agent and compare only the final verified artifact."],
    },
    "2026-06-20-autonomous-ai-agent-cron-pipelines.md": {
        "primary": "autonomous AI agent cron pipelines",
        "secondary": ["AI agent cron pipeline", "zombie task detection", "scheduled AI automation"],
        "field": "A cron agent that only reports success is a liability. A cron agent that leaves a timestamped artifact, a reasoned summary, and a failure path can become part of operations.",
        "monday": ["Find one scheduled agent job that says done without a durable artifact.", "Make it write a timestamped output file.", "Alert only after that file exists and passes a basic sanity check."],
    },
    "2026-06-26-why-ai-cron-jobs-lie-to-you-exit-zero-empty-output.md": {
        "primary": "AI cron jobs exit 0 empty output",
        "secondary": ["cron job exit 0 empty output", "AI automation verification", "agent cron reliability"],
        "field": "Exit codes are transport signals, not product truth. For agent jobs, I care more about the object produced, the count changed, and the next consumer that can read it than about the command ending cleanly.",
        "monday": ["Add an output-size check to one cron job.", "Fail the job when the output is empty or unchanged unexpectedly.", "Send the alert with the artifact path, not just the exit code."],
    },
    "2026-06-29-open-weights-api-margin.md": {
        "primary": "open weights API margin",
        "secondary": ["open weights vs API models", "LLM API margin", "open model cost strategy"],
        "field": "The pragmatic move is not to worship open weights or APIs. It is to make the boundary explicit: which calls need managed reliability, which calls need cost control, and which calls must be portable when pricing changes.",
        "monday": ["Classify your top five LLM calls by cost, latency, and failure impact.", "Move one low-risk batch call behind a provider abstraction.", "Keep managed APIs for the calls where uptime is worth the margin."],
    },
    "agent-edit-contract.md": {
        "primary": "agent edit contract",
        "secondary": ["AI coding agent handoff", "agent repository contract", "coding agent workflow"],
        "field": "The contract is not bureaucracy. It is a way to make the agent expose its assumptions before touching the repo. The payoff is fewer impressive diffs that hide broken intent.",
        "monday": ["Add a short edit contract to one repo.", "Require scope, files, tests, and rollback before the first patch.", "Reject the next agent run if it cannot name those four things."],
    },
    "ai-agent-frameworks-2026.md": {
        "primary": "AI agent frameworks 2026",
        "secondary": ["agent framework comparison", "AI agent framework architecture", "LangGraph CrewAI AutoGen comparison"],
        "field": "Framework choice matters less than boundary choice. If the framework cannot make state, retries, tool calls, and handoff artifacts visible, it will feel fast in demos and expensive in maintenance.",
        "monday": ["Pick one framework candidate and model your real failure path.", "Check how it stores state, retries, and tool output.", "Choose the framework that makes debugging boring, not the one with the prettiest demo."],
    },
    "ai-coding-agent-arms-race-2026.md": {
        "primary": "AI coding agent arms race 2026",
        "secondary": ["AI coding agent portability", "coding agent benchmarks", "model portability for developers"],
        "field": "The arms race rewards switching. Production rewards portability. The team that can move prompts, tests, and acceptance gates across tools gets the upside without becoming a hostage to one vendor cycle.",
        "monday": ["Write your coding-agent acceptance checks outside the tool UI.", "Run the same change through two agents.", "Keep the agent whose output is easiest to verify and rollback."],
    },
    "ai-generated-ui-correctness.md": {
        "primary": "AI generated UI correctness",
        "secondary": ["AI UI code review", "frontend correctness checks", "generated UI testing"],
        "field": "A rendered UI is only the first checkpoint. The real review asks whether the state transitions, empty states, error states, accessibility labels, and product promises still match the system behind it.",
        "monday": ["Take one generated UI component.", "Test empty, loading, error, and permission states.", "Do not merge until one non-happy-path screenshot exists."],
    },
    "artifact-health-checks-for-agent-cron-jobs.md": {
        "primary": "artifact health checks for cron jobs",
        "secondary": ["cron artifact verification", "agent cron health check", "scheduled job monitoring artifact"],
        "field": "The artifact is the cheapest truth source. If the job claims it updated a report, the report path, modified time, row count, and summary should all be checkable before anyone receives a success message.",
        "monday": ["Pick one cron output file.", "Check modified time, size, and expected marker text.", "Make the success notification include those three values."],
    },
    "beta-library-exit-path.md": {
        "primary": "beta library exit path",
        "secondary": ["adopting beta libraries", "dependency rollback plan", "software library exit strategy"],
        "field": "A beta dependency is not risky because it is unfinished. It is risky when the app learns its shape too deeply. The exit path should be designed before the integration spreads.",
        "monday": ["Find one dependency that is hard to remove.", "Put an adapter around the first call site.", "Write the rollback command before the next upgrade."],
    },
    "closed-loop-beats-more-automation.md": {
        "primary": "closed loop automation",
        "secondary": ["automation feedback loop", "AI automation metrics", "closed loop content operations"],
        "field": "Automation without readback creates motion. Closed-loop automation creates judgment. The difference is whether the next run changes because the last run produced evidence.",
        "monday": ["Choose one automated workflow.", "Define the metric that proves it helped.", "Make the next run read that metric before choosing the same action again."],
    },
    "coding-agent-needs-a-map.md": {
        "primary": "coding agent repository map",
        "secondary": ["AI coding agent context map", "repo map for coding agents", "agent context engineering"],
        "field": "More context is not the same as better orientation. A small map that names ownership, boundaries, tests, and dangerous files can outperform a giant context window full of noise.",
        "monday": ["Create a repo map for one service.", "Include entry points, test commands, and files the agent should not touch casually.", "Use it in the next agent run and compare the diff quality."],
    },
    "cron-patterns-lie.md": {
        "primary": "cron patterns that lie",
        "secondary": ["cron job false success", "cron monitoring patterns", "scheduled job reliability"],
        "field": "Cron failure usually hides in the space between command success and business success. Treat every scheduled job as a product workflow with an observable output, not just a shell command.",
        "monday": ["Pick one cron job that reports success today.", "Write the business condition it is supposed to change.", "Alert on that condition, not only on command failure."],
    },
    "i-swapped-my-llm-backend.md": {
        "primary": "swap LLM backend",
        "secondary": ["LLM backend migration", "provider abstraction for LLM", "model backend switching"],
        "field": "A backend swap feels easy when the first API call works. The real test is whether prompts, streaming, tool calls, retries, cost tracking, and fallback semantics still behave the same way under pressure.",
        "monday": ["Wrap one LLM call behind a local interface.", "Record latency, cost, and output shape before and after the swap.", "Keep the old backend available until the failure modes are known."],
    },
    "long-running-agents.md": {
        "primary": "long running AI agents production",
        "secondary": ["AI agents from demos to production", "long running agent failure modes", "production AI agent orchestration"],
        "field": "Long-running agents do not fail like short prompts. They drift, forget partial decisions, and declare victory against their own checklist. Production needs external checkpoints the agent cannot simply talk past.",
        "monday": ["Break one long agent task into checkpoints.", "Require a real artifact at each checkpoint.", "Stop the run when an artifact is missing instead of letting the agent explain it away."],
    },
    "the-javascript-i-deleted-with-css-2026-survival-guide.md": {
        "primary": "CSS replacing JavaScript 2026",
        "secondary": ["modern CSS features 2026", "delete JavaScript with CSS", "frontend performance CSS"],
        "field": "Deleting JavaScript is not minimalism for its own sake. It is a reliability move when the browser can now handle layout, interaction, or state without another runtime edge case.",
        "monday": ["Find one UI behavior implemented with JavaScript.", "Check whether CSS now supports it natively.", "Delete the script only if accessibility and browser support still pass."],
    },
    "vue-3-6-vapor-mode.md": {
        "primary": "Vue 3.6 Vapor Mode",
        "secondary": ["Vue Vapor Mode", "Vue no virtual DOM", "Vue 3.6 performance"],
        "field": "The right question is not whether Vapor Mode is impressive. It is where a compiler-driven path removes enough runtime cost to matter without making the team relearn the product.",
        "monday": ["Pick one isolated Vue component with measurable render cost.", "Prototype the new path beside the current implementation.", "Measure bundle and interaction cost before talking about migration."],
    },
    "your-ai-agent-pipeline-has-no-zombie-detection.md": {
        "primary": "AI agent zombie detection",
        "secondary": ["zombie AI agent pipeline", "agent pipeline monitoring", "detect stuck AI automation"],
        "field": "A zombie agent is dangerous because it looks busy enough to avoid attention. The fix is not more logging. The fix is a freshness contract that says what should change, by when, and who gets paged when it does not.",
        "monday": ["Add a freshness timestamp to one agent pipeline.", "Define the maximum acceptable age for the next artifact.", "Alert on stale output, not just crashed processes."],
    },
    "zero-cost-observability-agent-crons.md": {
        "primary": "zero cost observability for agent crons",
        "secondary": ["agent cron observability", "cron monitoring without paid tools", "AI automation observability"],
        "field": "The cheapest observability stack is a consistent artifact trail. Once the artifact, alert, and rollback path exist, paid tools become an amplifier instead of a substitute for operational discipline.",
        "monday": ["Pick one agent cron that already writes output.", "Add artifact metadata, a simple alert, and one rollback command.", "Only then decide whether paid monitoring would add signal."],
    },
}

DEEP_REFRESH = {
    "2026-06-12-ai-senior-developers.md",
    "2026-06-13-hermes-agent-pragmatic-review.md",
    "2026-06-14-indonesian-dev-scene-linux-moment.md",
    "2026-06-15-stop-reaching-for-state-library.md",
    "2026-06-16-korean-devtool-consolidation.md",
    "2026-06-16-linear-design-system-hugo.md",
    "2026-06-17-glm-5-2-just-became-the-best-open-weights-model.md",
    "2026-06-18-opencode-fable5-ai-coding-agent-shakeup.md",
    "2026-06-20-autonomous-ai-agent-cron-pipelines.md",
    "2026-06-26-why-ai-cron-jobs-lie-to-you-exit-zero-empty-output.md",
}


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    _, fm, body = text.split("---", 2)
    return fm.strip("\n"), body.lstrip("\n")


def dump_seo(data: dict[str, object]) -> str:
    secondary = data["secondary"]
    assert isinstance(secondary, list)
    lines = ["seo:", f"  primaryQuery: \"{data['primary']}\"", "  secondaryQueries:"]
    for item in secondary:
        lines.append(f"    - \"{item}\"")
    return "\n".join(lines)


def add_seo(fm: str, data: dict[str, object]) -> str:
    if re.search(r"^seo:\s*$", fm, flags=re.M):
        return fm
    return fm.rstrip() + "\n" + dump_seo(data) + "\n"


def add_field_note(body: str, data: dict[str, object]) -> str:
    if "{{< field-note" in body:
        return body
    note = dedent(f"""

{{{{< field-note title=\"Field note\" >}}}}
{data['field']}
{{{{< /field-note >}}}}
""")
    # Prefer placing the field note before an existing Monday action or final section.
    match = re.search(r"\n## What you should do Monday morning\b", body, flags=re.I)
    if match:
        return body[: match.start()] + note + body[match.start() :]
    return body.rstrip() + note + "\n"


def add_monday(body: str, data: dict[str, object]) -> str:
    if re.search(r"^## What you should do Monday morning\b", body, flags=re.M | re.I):
        return body
    steps = data["monday"]
    assert isinstance(steps, list)
    section = "\n## What you should do Monday morning\n\n" + "\n".join(
        f"{i}. {step}" for i, step in enumerate(steps, start=1)
    ) + "\n"
    return body.rstrip() + "\n" + section


def add_deep_refresh_note(body: str, filename: str) -> str:
    if filename not in DEEP_REFRESH or "## Refresh note" in body:
        return body
    section = dedent("""

## Refresh note

This piece is now part of the site's operating archive. Read it as a decision pattern, not as a frozen news item: check whether the tool, model, or platform detail has changed, then keep the underlying verification habit if it still reduces operational risk.
""")
    return body.rstrip() + section + "\n"


def main() -> int:
    changed = []
    for filename, data in DATA.items():
        path = POSTS / filename
        if not path.exists():
            raise FileNotFoundError(path)
        text = path.read_text()
        fm, body = split_frontmatter(text)
        new_fm = add_seo(fm, data)
        new_body = add_field_note(body, data)
        new_body = add_monday(new_body, data)
        new_body = add_deep_refresh_note(new_body, filename)
        new_text = "---\n" + new_fm.rstrip() + "\n---\n\n" + new_body.rstrip() + "\n"
        if new_text != text:
            path.write_text(new_text)
            changed.append(filename)
    print(f"Applied content ops upgrades to {len(changed)} posts")
    for item in changed:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
