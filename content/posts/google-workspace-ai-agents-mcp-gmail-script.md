---
title: "From Feb 1, Google Says AI Agents Must Use Its Workspace MCP Servers. Does Your Gmail Script Count?"
date: 2026-11-28T07:00:00+07:00
draft: false
slug: "google-workspace-ai-agents-mcp-gmail-script"
description: "Google's Workspace AI Tools Addendum takes effect Feb 1, 2027. A tool driven by an AI model must use Google's MCP servers. Three questions, a scanner, and the Gmail tool list."
topics: ["ai-agents"]
tags: ["google-workspace", "gmail-api", "mcp", "oauth", "ai-agents", "apps-script", "api-quotas"]
cover: /covers/google-workspace-ai-agents-mcp-gmail-script.png
seo:
  primaryQuery: "google workspace ai tools addendum mcp requirement"
  secondaryQueries:
    - "gmail api ai agent must use mcp february 2027"
    - "google workspace use this client for an ai-powered agent oauth"
    - "gmail mcp server tools list send_message reply"
---

On Nov 24, 2026, Google published a short contract called the Workspace AI Tools Addendum, and one sentence in it matters to anyone who has a script that reads Gmail, Drive or Calendar. The sentence says a tool must use a Google MCP server "where the GWS Access Tool is or is driven by an AI Agent, an AI Harness or an AI model or service employing an AI model."

If that is your Python cron, your Apps Script, or your Laravel queue job, the useful question is not "will Google break my Gmail API calls." The pages I read do not say that. The useful question is smaller and you can answer it in an afternoon: does a model decide anything inside my script, and if it does, which door does it use to reach Gmail?

The experience-based judgment I keep coming back to is this: a rule like this is never about the demo that works today, it is about the three scripts nobody remembers owning in February. This post reads Google's own pages, gives you three questions to sort your scripts, and ships a small scanner that I ran on made-up fixtures.

<!--more-->

## What Google actually published

Three official pages carry the news. I re-read all of them on Nov 28, 2026.

- The [Workspace AI Tools Addendum](https://workspace.google.com/terms/ai-tools), "Last modified: November 24, 2026."
- The [usage tiers and quotas page](https://developers.google.com/workspace/guides/quota-usage-tiers) for Workspace APIs and MCP servers, "Last updated 2026-11-26 UTC."
- The Workspace Updates blog post of Nov 24, which says Workspace MCP servers and the Workspace CLI are "generally available."

Two short definitions first, because the rest depends on them. An **MCP server** (Model Context Protocol) is a standard way for an AI tool to call functions on another service. Google hosts these servers, and your agent connects to a URL like `https://gmailmcp.googleapis.com/mcp/v1` and asks for the list of tools it can call. A **REST API** is the normal Gmail API your script already calls, such as `users.threads.list`.

The Addendum defines an "AI Agent" as "goal-oriented artificial intelligence (AI) systems or workflows that perform actions or tasks on your behalf in a supervised or autonomous manner." It defines a "GWS Access Tool" very broadly: "any AI Agent, AI Harness, software, application, AI model, service employing an AI model, or other tool that can be used to obtain or access user data via a GWS Access Point."

Then comes the rule that matters, term 1 of the Additional Terms:

> The GWS Access Tool must use a Google MCP where the GWS Access Tool is or is driven by an AI Agent, an AI Harness or an AI model or service employing an AI model. You may not obfuscate or otherwise allow any GWS Access Tool to avoid classification as a GWS Access Tool or to circumvent this requirement to use a Google MCP.

One wording detail is worth knowing. The Addendum names "a Google MCP." The blog post and the tiers page say "Workspace MCP servers or the Workspace CLI." The CLI is named in the announcement, not in the Addendum's own sentence. If you run agents in a terminal, read the CLI guide and ask which of the two your tool is meant to use.

![Timeline of the three Google Workspace dates: Nov 24 2026, Feb 1 2027, Apr 1 2027](/img/google-workspace-ai-agents-mcp-gmail-script-1.png)

## Three dates, counted from today

| Date | Days from Nov 28 | What the Google pages say |
| --- | --- | --- |
| Nov 24, 2026 | already past | Standard and Scaled tiers launch. The Addendum page is dated this day and the new API quotas dashboard starts to roll out. |
| Feb 1, 2027 | 65 | The Addendum takes effect. The blog says "technical enforcement begins." Agent callers of the REST APIs are held to Standard quotas. |
| Apr 1, 2027 | 124 | Scaled Tier billing starts. Gmail, Calendar and Drive MCP on the Scaled Tier is "billed from the first request." |

The day counts are my arithmetic from the dates on the page: Nov 28 to Feb 1 is 65 days, and Feb 1 to Apr 1 is 59 more.

The Standard Tier is free. For the generally available Workspace MCP servers the page gives "up to 5,000 requests per day, per project, per product." The same page says "some MCP tools count as multiple requests because they make multiple API calls," so the number of tool calls and the number of requests counted against the 5,000 are not the same thing. Google says it expects less than 1% of active Workspace developers to need more than Standard.

I am not quoting Scaled Tier prices. The pricing page has four billing buckets and worked examples. I did not verify a price I would be willing to put in front of you, so there is none here.

## Does your script count? Three questions

The sentence in term 1 has a condition: the tool "is or is driven by" an AI agent or model. So sort your scripts with these three questions. This is my reading of the text, not legal advice, and Google has not published an example list.

1. **Does a model decide anything inside the script?** A model that classifies mail, drafts a reply, or picks which file to open is a model in the loop. A script that applies a label when the sender equals one fixed address is not.
2. **Does it reach Workspace through the REST API with its own OAuth client?** A model-driven script that does this is the case the Feb 1 date is about. The tiers page says agent callers that use REST directly are limited to Standard quotas from Feb 1, "regardless of the tier selected."
3. **Do you need a send, reply or move that the MCP server does not give you?** This one is a gap check, and the next sections show why it is real.

A script with no model in it is not the target of term 1, in my reading. Two cautions. First, the clause "You may not obfuscate or otherwise allow any GWS Access Tool to avoid classification" means you should not hide a model call in a helper to keep a script out of the pile. Second, the other terms apply to any access tool. Read literally, the retention and model-training limits in term 2 cover a plain script too: no storing Google Technical Information for more than 30 days, no using user data for "model training, fine-tuning, evaluation dataset building, or model distillation." A no-model script that exports mail into a training set is still on the wrong side of those lines.

![Decision flow: model in the loop, own OAuth client on REST, gap check for send and reply](/img/google-workspace-ai-agents-mcp-gmail-script-2.png)

## Scan your own folders

You cannot answer question 1 by memory. This scanner is a plain Python file that walks a folder, finds files that reach Workspace, and says whether a model SDK appears in the same file or the same folder. It runs no code and it only reads text. It cannot see your OAuth client settings, and a model reached through a wrapper library it does not know will be missed.

```python
#!/usr/bin/env python3
"""List files that reach Google Workspace and say whether a model sits nearby.

Heuristic only: it reads text, it does not run anything and it cannot see
your OAuth client settings.
"""
import re
import sys
from pathlib import Path

REACHES = {
    "rest-url": re.compile(r"(gmail|drive|calendar-json|docs|sheets)\.googleapis\.com"),
    "python-client": re.compile(r"googleapiclient"),
    "node-client": re.compile(r"""from ['"]googleapis['"]|require\(['"]googleapis['"]\)"""),
    "apps-script": re.compile(r"\b(GmailApp|DriveApp|CalendarApp|ScriptApp\.getOAuthToken)\b"),
}
MCP = re.compile(r"(gmail|drive|calendar|docs|sheets|slides|chat|tasks)mcp\.googleapis\.com")
MODEL = re.compile(
    r"openai|anthropic|generativelanguage\.googleapis\.com|ollama|litellm"
    r"|chat\.completions|messages\.create|generateContent",
    re.I,
)
SKIP = {".git", "node_modules", "vendor", ".venv", "__pycache__", "dist"}
EXT = {".py", ".js", ".ts", ".gs", ".php", ".rb", ".go", ".sh"}


def scan(root: Path):
    files = [p for p in root.rglob("*")
             if p.is_file() and p.suffix in EXT and not (SKIP & set(p.parts))]
    text = {p: p.read_text(errors="replace") for p in files}
    model_dirs = {p.parent for p, t in text.items() if MODEL.search(t)}
    for p, t in sorted(text.items()):
        hits = [name for name, rx in REACHES.items() if rx.search(t)]
        if MCP.search(t):
            hits.append("mcp")
        if not hits:
            continue
        in_file = bool(MODEL.search(t))
        near = p.parent in model_dirs
        if "mcp" in hits and not [h for h in hits if h != "mcp"]:
            verdict = "already on MCP"
        elif in_file:
            verdict = "REVIEW: model call and Workspace call in one file"
        elif near:
            verdict = "CHECK: model code in the same folder"
        else:
            verdict = "no model seen (inference: probably not an agent)"
        print(f"{p.relative_to(root)} | {','.join(hits)} | {verdict}")


if __name__ == "__main__":
    scan(Path(sys.argv[1] if len(sys.argv) > 1 else "."))
```

I wrote seven small fixture files to test it: a Gmail digest that also calls an OpenAI client, an invoice labeller with no model, an Apps Script that replies through the Anthropic API, a Drive export with a separate summarizer next to it, a file that already points at the Gmail MCP URL, and a notes file that only imports `ollama`. This is the real output:

```text
digest/nightly_digest.py | python-client | REVIEW: model call and Workspace call in one file
invoices/label_invoices.py | python-client | no model seen (inference: probably not an agent)
mcp/agent_config.py | mcp | already on MCP
reports/fetch_report.py | python-client | CHECK: model code in the same folder
sheet-bot/Code.gs | apps-script | REVIEW: model call and Workspace call in one file
```

The `notes.py` fixture does not appear because it never touches Workspace. The `CHECK` line is the one to read by hand: `fetch_report.py` only exports a Drive file, but a summarizer sits in the same folder, and whether the two are wired together is a question only a person can answer. The scanner is a first pass, not a verdict.

## What the Gmail MCP server lists today

Question 3 asks whether the MCP door has the tool you need. Google's [Gmail MCP reference](https://developers.google.com/workspace/gmail/api/reference/mcp) lists two endpoints, `https://gmailmcp.googleapis.com/mcp/v1` and `https://gmailmcp.googleapis.com/mcp/v1self`. I compared the two tool lists with a short script. The primary endpoint lists 30 tools and the self-mode endpoint lists 25. The five that only the primary endpoint lists:

| Tool | `/mcp/v1` | `/mcp/v1self` |
| --- | --- | --- |
| `send_message` | listed | not listed |
| `reply` | listed | not listed |
| `forward` | listed | not listed |
| `apply_sensitive_message_label` | listed | not listed |
| `apply_sensitive_thread_label` | listed | not listed |
| `create_draft`, `search_threads`, `get_thread`, `trash_message` and 21 more | listed | listed |

The configuration guide explains the difference this way. The primary endpoint "uses MCP form elicitation for user approvals," meaning the server can ask the human to confirm a sensitive action. If your MCP host does not support form elicitation, the guide points to the `/mcp/v1self` endpoint, which "exposes only tools and results that work without form elicitation under default policy, although specific calls might still require approval depending on policy and target resources."

Put that next to the blog's own sentence: "Routine actions like creating a draft stay seamless, while admins can set rules that prompt users to confirm sensitive actions in third-party AI tools." My reading, labelled as inference: a mail-sending agent that runs with nobody watching is the awkward case. Sending is listed only where approvals can happen, and the self-mode list has no send at all. I did not find a Google page that says an unattended job can send mail through either endpoint. That is the first thing I would test, and it is not something I can conclude from reading.

Two more gaps, from comparing names on two pages. The [pricing and billing tiers page](https://developers.google.com/workspace/guides/quota-pricing) lists the REST methods `messages.batchDelete` and `watch` among Gmail API operations. The MCP tool list has `trash_message` and `trash_thread` but no tool with either of those names. Names do not have to match one to one, so treat this as a thing to check, not a finding.

![Gmail MCP endpoint tool lists: 30 on the primary endpoint, 25 on self mode, and the five tools that differ](/img/google-workspace-ai-agents-mcp-gmail-script-3.png)

## What switching looks like

For an agent host, the change is a config entry instead of a Google client library. This is the shape the configuration guide gives for a host that reads `mcp_config.json`, with your own client ID and secret in place of the placeholders:

```json
{
  "mcpServers": {
    "gmail": {
      "serverUrl": "https://gmailmcp.googleapis.com/mcp/v1",
      "oauth": {
        "clientId": "OAUTH_CLIENT_ID",
        "clientSecret": "OAUTH_CLIENT_SECRET"
      }
    }
  }
}
```

The test prompts on that page show what the tool names look like when an agent calls them: `gmail.search_threads`, `gmail.get_thread`, `gmail.create_draft`. To see the full tool specifications yourself, the reference page gives this request:

```bash
curl --location 'https://gmailmcp.googleapis.com/mcp/v1' \
  --header 'content-type: application/json' \
  --header 'accept: application/json, text/event-stream' \
  --data '{ "method": "tools/list", "jsonrpc": "2.0", "id": 1 }'
```

I did not run it. The servers use OAuth 2.0, so a real call needs a signed-in client, and I did not sign in to a Workspace account for this post.

## The OAuth checkbox and two special cases

Both the blog and the configuration guide name one concrete setting. In the Google Cloud console, under Google Auth Platform and Clients, an OAuth client used by an agent has to have **Use this client for an AI-powered agent** selected. The blog calls the underlying field `is_agentic` and says traditional non-agent features "should use a separate OAuth client." The blog also says requiring agents to identify themselves in OAuth is how admins get to manage agent access in the Admin console.

That checkbox is the one place where the rule becomes something you can look at. If your scanner shows a `REVIEW` file, find its OAuth client and see whether the box is ticked. If one client serves both a model-driven script and an ordinary feature, the guide says to create a separate client for the agent.

Two cases from the troubleshooting section matter to people who run small scripts:

- **Service accounts with domain-wide delegation.** You cannot select the checkbox, because those accounts are not managed under Clients. The page says requests "aren't rejected for missing the agent setting," that access is governed by the delegation settings your Workspace administrator manages, and that the MCP servers "still return form elicitation prompts" on sensitive calls.
- **Apps Script.** You cannot select the checkbox on the default OAuth client that Apps Script creates for your script. To call the MCP servers from Apps Script, you create your own client, use the OAuth2 for Apps Script library, and send the token that library returns "instead of the token from `ScriptApp.getOAuthToken`." The page adds that Apps Script projects that do not call the MCP servers "aren't affected."

## What I ran, and what I did not

I read the three Google pages and the Gmail MCP reference, saved them locally, and quoted from them. I wrote the scanner and six fixture files and ran it. I counted the tool lists and the day counts with a short script. I did not call a Google MCP server, sign in to Workspace, test an unattended send, or read any Scaled Tier price. I also did not test how Google decides that a script is "driven by" a model.

## What this post is not saying

- It is not saying Google is removing the Gmail API. The pages do not say that, and the tiers page says REST projects under standard limits keep running as they do today.
- It is not saying your script breaks on Feb 1. The pages say agent callers of REST are held to Standard quotas, and technical enforcement of the MCP-or-CLI requirement begins that day.
- It is not saying a personal script is in scope or out of scope. The pages do not give an example, and I would not guess.
- It is not saying how many developers are affected beyond Google's own statement that it expects less than 1% of active Workspace developers to need more than the Standard Tier.

{{< field-note title="Field note" >}}
The review habit I trust for a rule like this is the same one I use for a dependency audit: start from the list of credentials, not from the code. In a Laravel codebase a Gmail or Drive integration usually sits in a queued job or an artisan command, with a Google client library and a stored refresh token. Search for the client library first, then search the same folders for a model SDK, and only then read the files that match both. This post is a design argument from reading public pages, not a war story: I did not hit this rule on a real account. If you keep several small services, as in the [AI agent operations notes](/ai-agent-operations/), keep one table of every OAuth client, which script uses it, and whether a model is in that script. That table makes the Admin console's API controls page much easier to read.
{{< /field-note >}}

## What you should do Monday morning

1. Run the scanner on every repo and every Apps Script project you own. Write down each `REVIEW` and `CHECK` line.
2. For each of those, answer question 1 in one sentence: what does the model decide? If the answer is "nothing," write that down too.
3. Open Google Auth Platform, then Clients, and match each model-driven script to its OAuth client. If the same client also serves a non-agent feature, plan a second client.
4. Open the new API quotas dashboard in the Google Cloud console for each project and check its usage against the Standard limits, including the 5,000 requests per day per product for MCP. The tiers page says that if every project is within Standard limits, you do not need to change tiers.
5. For one script that sends or replies, write down whether it needs `send_message` or `reply`, and decide how you will test it on `/mcp/v1` and on `/mcp/v1self` before Feb 1.
6. Put Feb 1 and Apr 1 in the team calendar.

If this was useful, a neighbouring check is worth doing in the same session. [The Cloudflare Email Sending post](/blog/cloudflare-email-sending-free-plan-verified-only/) is another "works for the address you tested" rule. [Your overnight agent job has a login with an end date](/blog/agent-job-login-has-an-end-date/) covers expiring credentials. The [AI agent operations hub](/ai-agent-operations/), the [developer tools notes](/developer-tools/) and [start here](/start-here/) collect the rest.

## Further reading

{{< source href="https://workspace.google.com/terms/ai-tools" label="Workspace AI Tools Addendum (Google)" >}}

{{< source href="https://developers.google.com/workspace/guides/quota-usage-tiers" label="Usage tiers and quotas for Google Workspace APIs and MCP servers" >}}

{{< source href="https://developers.google.com/workspace/guides/configure-mcp-servers" label="Configure the Google Workspace MCP servers" >}}

{{< source href="https://developers.google.com/workspace/gmail/api/reference/mcp" label="Gmail MCP reference: gmailmcp.googleapis.com" >}}

{{< source href="https://developers.google.com/workspace/guides/quota-pricing" label="Understand Google Workspace API and MCP server pricing and billing tiers" >}}

{{< source href="https://workspaceupdates.googleblog.com/2026/11/mcp-servers-cli-standardized-usage-tiers-now-available.html" label="Workspace Updates: MCP servers, CLI, standardized usage tiers (Nov 24, 2026)" >}}
