---
title: "I Swapped My LLM Backend — The API Call Worked on the First Try"
date: 2026-06-25T07:00:00+07:00
draft: false
topics: ["ai"]
cover: /covers/i-swapped-my-llm-backend.png
---

# I Swapped My LLM Backend — The API Call Worked on the First Try

The migration took eleven minutes. The fallout took three weeks. I switched our production agent from GPT-4o to a cheaper model on a Tuesday afternoon, confirmed the health check passed, and pushed it live. The API returned 200. The response body was valid JSON. Everything looked fine. It was not fine. Over the next twenty-one days, I watched our error rate climb 340%, our RAG pipeline silently return garbage, and our "deterministic" eval suite give everything a pass because it was never actually measuring what I thought it was. This post is about what breaks when you swap an LLM mid-project — not the API layer, which is the easy part, but everything built on top of it.

![Day 1 vs Day 21 — API 200 OK vs +340% error rate](/img/i-swapped-my-llm-backend-1.png)

## The Price Landscape That Forces Your Hand

LLM pricing dropped roughly 80% between 2025 and 2026. That kind of cost compression makes previous architecture decisions look insane. Here is what you're looking at right now for common mid-tier models:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|---|---|---|
| GPT-5.4 | $2.50 | $15.00 |
| Claude Sonnet 4.6 | $3.00 | $15.00 |
| DeepSeek V3.2 | $0.14 | $0.28 |

Running a code-review agent that processes 40,000 diffs per month, averaging 800 input tokens and 400 output tokens each, looks like this on GPT-5.4:

```
Monthly input:  40,000 × 800 tokens  = 32M tokens × $2.50/1M = $80.00
Monthly output: 40,000 × 400 tokens  = 16M tokens × $15.00/1M = $240.00
Total: $320.00/month
```

On DeepSeek V3.2, the same workload:

```
Monthly input:  32M tokens × $0.14/1M = $4.48
Monthly output: 16M tokens × $0.28/1M = $4.48
Total: $8.96/month
```

That's a 35x cost difference. You would be negligent to not at least evaluate the cheaper option. The problem is that "evaluating" it is not a benchmark run. It's a systems integration project.

## Prompt Re-Engineering Is Not Optional

Every model responds to prompts differently. This is not a secret. It is also not something you can paper over with a translation layer. We had 23 prompts in production across our classification agent, our summarization pipeline, our RAG synthesis loop, and our test generation workflow. Of those 23, seven produced materially different output on DeepSeek compared to GPT-5.4 using the identical prompt string.

The failure mode was not refusal or hallucination. It was subtler: changes in output formatting, different default verbosity levels, and inconsistent handling of negative constraints.

Here is a simplified version of a prompt that broke:

```python
SYSTEM_PROMPT = """
You are a code review assistant.
Analyze the following diff and return a JSON object with:
  - "issues": list of {severity, line, description}
  - "summary": one sentence summary
  - "recommendation": "approve" | "request_changes" | "comment"

Do not include any text outside the JSON object.
"""
```

GPT-5.4 followed the "no text outside JSON" instruction 99.2% of the time. DeepSeek V3.2 did it 91% of the time — and the 8% failures weren't random. They correlated with diffs longer than 600 tokens, which meant our longer, more complex PRs (the ones where correctness mattered most) were the ones getting out-of-band text prepended to the response. Our JSON parser was permissive enough to handle it, which meant the downstream consumer was reading summaries that the model had smuggled in as prose.

The fix was model-specific prompt engineering:

```python
SYSTEM_PROMPT_DEEPSEEK = """
You are a code review assistant. Respond with ONLY a JSON object.
No preamble. No explanation. No markdown fences.

Output schema:
{
  "issues": [{"severity": "...", "line": N, "description": "..."}],
  "summary": "...",
  "recommendation": "approve|request_changes|comment"
}

Diff to analyze:
{{diff_text}}
"""
```

This is the tax of model portability. Your prompts are not portable. Every model is a different user with different defaults, and your system prompt is the only lever you have. Budget time for re-engineering every prompt in your system. Multiply your estimate by three.

![Prompt compatibility heatmap across GPT-5.4, Claude Sonnet 4.6, and DeepSeek V3.2](/img/i-swapped-my-llm-backend-2.png)

## Embedding Reindexing Will Catch You Off Guard

If your project uses RAG — and most production projects do — you probably embedded your vector database with a specific model. OpenAI's text-embedding-3-large, Cohere's embed-v4, or a local model like Nomic. These embeddings occupy different vector spaces. They are not interchangeable.

When we evaluated switching models, the vendor suggested we could "just re-run the same embedding model through the cheaper LLM." That statement was technically true and practically useless. Our vector database had 2.1 million chunks indexed with embeddings generated by OpenAI's text-embedding-3-large. We were not also running a separate embedding model for retrieval at query time — we were using the same model to embed the query and the documents.

If we swapped the LLM backend but kept our embeddings, we needed to keep using the same embedding model for queries. But the vendor's all-in-one migration guide assumed we would swap the embedding model too, which meant:

```bash
# Reindexing 2.1M chunks with new embedding model
# At ~500 chunks/second on a 4-GPU node:
echo "Total chunks: 2100000"
echo "Throughput: 500 chunks/sec"
echo "Time: $(( 2100000 / 500 / 3600 )) hours"
# = 1.17 hours for the embedding compute

# But add retry logic, validation, and index swap:
echo "Realistic estimate with validation + rollback plan:"
echo "~4 hours for reindex + ~2 hours for index swap = 6 hours"
```

That's the best case. If your chunking strategy interacts with the model (e.g., you use the LLM to generate summaries before embedding), you are also reprocessing every document through the new model. Our 2.1M chunks came from roughly 400,000 source documents. Running each through the summarization step on DeepSeek took longer per document but was cheaper. The math worked out, but the orchestration was not trivial.

The real gotcha: during reindexing, your RAG system is either unavailable or serving stale results. You need a migration strategy. We ran dual indices for 48 hours:

```python
class DualIndexRouter:
    def __init__(self, old_index, new_index, split_ratio=0.0):
        self.old = old_index
        self.new = new_index
        self.split = split_ratio  # fraction routed to new index

    def query(self, embedding, top_k=10):
        if random.random() < self.split:
            return self.new.search(embedding, top_k)
        return self.old.search(embedding, top_k)

    def promote_new(self):
        """Call after validation passes."""
        self.split = 1.0

    def rollback(self):
        """Call if new index regresses."""
        self.split = 0.0
```

We shifted traffic 5% → 25% → 50% → 100% over four days. Day at 25% was when we caught that the new embedding model returned adjacent-but-wrong results for our medical documentation queries. The semantic similarity scores were high (0.87+) but the results were off-topic. We rolled back, adjusted our chunking strategy, and started over.

## Eval Suite Blind Spots Are Where Death Lives

Our eval suite had 847 test cases. It reported 96% pass rate on GPT-5.4. After the switch, it reported 94% pass rate on DeepSeek. Two percentage points. Management saw a near-identical number. Engineering knew that the number was lying.

Here is why: our eval cases were checking for structural correctness, not semantic correctness. They validated:

1. Is the output valid JSON?
2. Does the JSON contain the required keys?
3. Is the "recommendation" field one of the allowed values?

They did not check whether the summary was accurate, whether the identified issues were real, or whether the severity ratings were appropriate. The eval suite was built for the original model's output patterns. When DeepSeek produced structurally valid but semantically different output, the evals passed because they were measuring the wrong thing.

The fix was adding LLM-as-judge checks to the eval pipeline:

```python
def eval_with_judge(self, test_case: dict, model_output: dict) -> dict:
    judge_prompt = f"""
    Original query: {test_case['input']}
    Reference answer: {test_case['expected']}
    Model answer: {json.dumps(model_output)}

    Rate on these criteria (1-5 each):
    - factual_accuracy: Does the model output match ground truth?
    - specificity: Are claims concrete, not vague?
    - relevance: Did the model address the actual question?

    Output as JSON: {{"factual_accuracy": N, "specificity": N, "relevance": N}}
    """
    judgment = self.judge_model.chat(judge_prompt)
    return {
        "model_output": model_output,
        "scores": judgment,
        "pass": judgment["factual_accuracy"] >= 4
    }
```

Implementing this dropped our "blind pass" rate from 94% to 71% — which was the real number. Those 23 failing cases that the original eval suite was silently ignoring? They represented real regressions our users had been complaining about for weeks.

![Structural vs Semantic eval scores comparison](/img/i-swapped-my-llm-backend-3.png)

## Pinning vs Floating Aliases: The Deployment Decision Nobody Discusses

Most developers use floating model aliases in their API calls:

```python
response = openai.chat.completions.create(
    model="gpt-5.4",  # this resolves to whatever the latest version is
    messages=[...],
)
```

This is convenient. It is also a deployment risk you are accepting without realizing it. `gpt-5.4` today might not be the same `gpt-5.4` in three weeks. The provider pushes version updates, and behavioral drift between versions is real. We discovered this when our production output quality changed overnight with no code changes on our side.

The alternative is pinning to specific version strings:

```yaml
# config/models.yml
code_review:
  provider: openai
  model: gpt-5.4-nano-2026-03-15
  api_version: "2026-03-15"
  temperature: 0.1
  max_tokens: 2048

summarization:
  provider: openai
  model: gpt-5.4-nano-2026-03-15
  fallback: claude-sonnet-4-6-2026-05-12
```

Pinned versions mean you control when updates happen. You test against the new version, validate your full eval suite, and then switch. The cost is maintenance overhead — you need a process for reviewing and accepting updates.

The floating alias approach means the provider controls when updates happen. You test post-hoc, usually by noticing something is wrong. The cost is unpredictable behavioral drift.

For production systems, pin your versions. The config overhead is the point. You want to make the invisible visible, and you want every model change to be a deliberate action, not a passive consequence of someone else's deployment calendar.

## Shadow Deployments Are the Only Safe Way To Migrate

I mentioned at the top that the migration took eleven minutes. That was the technical swap. The migration that actually mattered — the one that didn't cause a three-week incident — was the shadow deployment we should have done first.

Here is the playbook:

```python
class ShadowDeployment:
    """Route traffic to both old and new model. Serve old model's responses.
       Log new model's responses for comparison."""

    async def handle_request(self, request):
        # Serve from old model
        old_response = await self.old_model.chat(request)

        # Async call to new model (don't block response)
        asyncio.create_task(
            self._shadow_compare(request, old_response)
        )
        return old_response

    async def _shadow_compare(self, request, old_response):
        new_response = await self.new_model.chat(request)
        diff = self.comparator.compare(old_response, new_response)
        self.logger.info("shadow_diff", extra={
            "request_id": request.id,
            "semantic_similarity": diff.similarity,
            "structural_match": diff.structures_match,
            "latency_delta_ms": diff.latency_delta,
            "cost_per_1k_tokens": self._cost_estimate(new_response),
        })
        self.metrics.histogram("shadow.similarity", diff.similarity)

    def promote_when(self, criteria):
        """Check if new model meets promotion criteria."""
        return (
            self.metrics.mean("shadow.similarity") > 0.92
            and self.metrics.p95("shadow.latency") < criteria.max_latency_ms
            and self.metrics.count("shadow.structural_failures") == 0
        )
```

Run shadow for at least one full business cycle. For us, that was one week. Our shadow logs revealed the prompt issues and embedding issues before a real user ever saw a bad response. The eleven-minute migration should have been preceded by a seven-day shadow period. We skipped it because the health check passed and the benchmarks looked good.

## The Actual Cost of Switching

Let me lay out the real numbers from our migration (preliminary test run, before rolling out to the live 40,000 monthly diffs):

| Item | Time | Cost |
|---|---|---|
| Initial eval run | 2 hours | — |
| Shadow deployment (1 week) | 7 days | $12.40 |
| Prompt re-engineering (7 of 23 prompts) | 3 days | — |
| Embedding reindex + validation | 1 day | |
| Dual-index serving (48 hours) | 2 days | $3.80 |
| Fixing evals | 1 day | — |
| **Total** | **~2 weeks** | **$16.20 + compute** |

The point is not the specific numbers. The point is that switching LLM models is not an API change. It is a systems integration project. The API is the easy part. The hard parts are everything that accumulated on top of the API during the previous months of development: prompts, eval suites, chunking strategies, caching assumptions, and latency budgets.

## What I Would Do Differently

If I were starting a production LLM project today, here is what I would build in from day one:

1. **Model config in YAML, not in code.** Swap the model via config change, not code deploy. This forces you to design the abstraction correctly.

2. **Shadow comparison as a first-class feature.** Not an afterthought. The ability to compare two models side-by-side on real production traffic is the most valuable infrastructure you can build.

3. **Semantic evals, not structural.** Every eval should answer "is the output correct?" not "does the output look like we expected?"

4. **Pinned versions with documented update process.** Know exactly which model version is running. Know the process for testing and promoting a new version.

5. **Portable prompts with model-specific overrides.** Accept that prompts are not universal. Build the infrastructure to maintain per-model prompt variants without duplicating your entire logic.

## The Bottom Line

The API call is the least interesting part of an LLM integration. Switching models is trivially easy at the transport layer and punishingly difficult at every layer above it. Until you have done it, you will underestimate the cost by a factor of five. Until you have shadow-tested the new model against real traffic, you will assume the wrong things are breaking. Build for portability now, or pay for the migration later. The migration is always more expensive than the preparation.

![Eleven-minute migration vs three-week fallout — config change is the easy part](/img/i-swapped-my-llm-backend-4.png)
