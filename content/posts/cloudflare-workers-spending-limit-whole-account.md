---
title: "A Cloudflare Spending Limit Covers the Whole Account, So a Test Worker Can Interrupt Production"
date: 2026-11-16T06:00:00+07:00
draft: false
slug: "cloudflare-workers-spending-limit-whole-account"
description: "Cloudflare added spending limits for Workers on Nov 13, 2026. The limit is one switch for the whole account, so a test Worker can stop a production one. Here is what stops, what keeps running, and the commands to set an alert first."
topics: ["devops"]
tags: ["cloudflare", "cloudflare-workers", "spending-limits", "durable-objects", "cost-control", "cf-cli", "billing", "change-control"]
cover: /covers/cloudflare-workers-spending-limit-whole-account.png
seo:
  primaryQuery: "cloudflare workers spending limit"
  secondaryQueries:
    - "cloudflare error 1103 spending limit"
    - "cf billing spend-policies create"
    - "cloudflare workers email alert spend"
---

Open your Cloudflare dashboard and answer one question without scrolling: how many Workers live in the account that pays for production? Now answer a second one: which of them is the test one?

If the two lists share an account, this post is for you. On Friday, Nov 13, 2026, Cloudflare announced that you can set spending limits for Workers and Durable Objects. The announcement is good news. The one sentence inside the docs that decides whether it is good news *for you* is easy to skim past: a Workers limit applies to the whole account.

That means a limit is not "this app can spend $50." It is "everything in this account that runs a Worker can spend $50 together, and then it stops."

The question is not whether the new control works. The question is whether the person who turns it on knows which Worker will go dark first, and who gets the email when it does.

<!--more-->

## What Cloudflare announced on Nov 13

I re-read four official pages on Monday, Nov 16, 2026: the changelog entry, the billing guide, the Workers page and the cf CLI page. Cloudflare's own changelog opens like this:

> "You can now set spending limits for Workers and Durable Objects to help control unexpected usage costs, or receive email alerts while your applications keep running. Support for more products is coming soon."

Here is the short version, with the exact words kept where they matter.

| Fact | What the page says |
|---|---|
| Date | Nov 13, 2026 (changelog entry and "Last updated" on the guides) |
| Products covered | Workers and Durable Objects, each with its own separate limit |
| Two kinds of control | A **spending limit** blocks. An **email alert** only notifies. |
| What counts toward a Workers limit | Requests and CPU time, after included usage |
| What does not count | The Workers Paid subscription fee, and charges for other products |
| Unit | US dollars per subscription billing period |
| One limit per product | "You can have one enabled limit per product on an account." |
| Where to click | Billing, then **Spend Management** (the changelog calls the same screen **Spend limits**) |

Two things in that table are worth a second look. First, there are two controls with very different consequences. An email alert is a smoke detector. A spending limit is a circuit breaker. Second, the limit lives in the *billing period*, not on the calendar month. If your subscription renews on the 15th, the limit resets on the 15th.

[Source: https://developers.cloudflare.com/changelog/post/2026-11-13-spend-management/]
[Source: https://developers.cloudflare.com/billing/manage/spend-management/]

![One account, one shared Workers limit: a test Worker and a production Worker count toward the same gauge, and both stop when it is reached.](/img/cloudflare-workers-spending-limit-whole-account-1.png)

## The sentence that decides everything

Here is the sentence from the Workers page, word for word:

> "A Workers limit applies to the whole account, rather than one application or environment. For example, a test Worker can reach the shared limit and interrupt a production Worker in the same account."

Read it as a junior would on a Friday afternoon. You have a side project, a staging Worker, a half-finished experiment from last month, and the one Worker that real users hit. All of them are in one account because that was the easy way to start. You set a limit "to be safe." Nothing in that flow asks which Worker you are protecting.

The billing guide repeats the same boundary from another angle: "Workers and Durable Objects limits cannot target an individual Worker, Durable Object namespace, or billing metric." You choose one number for the combined usage of that product across the account.

So the honest picture is a shared gauge. A runaway test loop fills it. When it is full, the production Worker is on the wrong side of the line, even though production did nothing wrong.

{{< note type="warning" title="Read this before you turn on Block usage" >}}
A Workers limit has no "only this Worker" setting. If a test Worker and a production Worker share an account, a blocking limit protects your bill and puts your production traffic at risk in the same move. Decide that trade on purpose.
{{< /note >}}

[Source: https://developers.cloudflare.com/workers/platform/spend-management/]

## What stops, and what keeps running

When the limit takes effect, the Workers page says Cloudflare "rejects new invocations of your Workers." It lists what that includes. I turned the list into a table with one extra column: what a junior will notice first.

| What the Worker was doing | At the limit | What you will notice |
|---|---|---|
| Answering incoming HTTP requests | Rejected | Visitors see error `1103` |
| Running on a Cron Trigger | Rejected | The scheduled code does not run |
| Consuming a queue (a queue consumer invocation) | Rejected | The consumer code does not run |
| Handling an Email Worker invocation | Rejected | The email handler does not run |
| Being called by another Worker or a Durable Object | Rejected | The caller's call fails |
| Static assets served without running your Worker | **Keep running** | Files still load |

The last row is the useful one. The page says: "Static assets served without running your Worker continue to be available." It also adds the catch: "Requests that need Worker code, such as requests routed through `run_worker_first`, can fail." And it says that a limit "does not delete your Workers or assets."

Notice the second and third rows. A failed web page is loud. A cron job that never fires and a queue that stops draining are quiet. If your Workers do background work, the first symptom of a limit may be a report that is a day late, not an error.

![Timeline of the docs example: a $50 Workers limit, near limit at $40, limit reached at $50, new invocations blocked, resume at the next billing period.](/img/cloudflare-workers-spending-limit-whole-account-2.png)

## The error you will see: 1103

HTTP visitors who hit a blocked Worker "receive error `1103`." The next sentence is the one to keep: "This error has other causes, so check Billing > Spend Management before contacting support."

That is a debugging order, and it saves an hour:

1. A visitor or a monitor reports error 1103.
2. Do not open a support ticket first. Open **Billing**, then **Spend Management**.
3. Look at the **Workers** row. Is the limit marked as reached?
4. If yes, you found it. If no, 1103 has another cause, and now you can say you ruled the limit out.

One more detail from the Workers page: "Requests rejected by the spending limit are not billed as Worker invocations." The blocked request does not add to your bill. It also does not reach your code, so your own logs will not show it.

## A limit is not an exact bill

The docs are plain about this, and I will quote it rather than soften it:

> "A spending limit is not an exact maximum bill. Usage reporting and blocking take time, so usage can continue after the threshold is reached."

The billing guide adds three more facts that change how you set the number.

- **The limit counts spend already recorded.** The guide's example: saving a $50 limit after the product has already accrued $60 "can trigger a pause as soon as Cloudflare evaluates the policy." If you set a low limit late in the billing period, you can block yourself on the first evaluation.
- **"Limit reached" is a record, not a proof.** The dashboard status reflects a recorded threshold event. The guide says that **Limit reached** "does not confirm that blocking has finished propagating."
- **The invoice is the final record.** In the guide's words: "Your invoice is the final record of charges."

The practical reading for a junior: treat the limit as a brake, not a wall. A brake slows the car. It does not promise the car stops at the painted line.

{{< note type="note" title="Different control, different job" >}}
If what worries you is one slow invocation that burns CPU, the Workers page points to a different setting: the per-invocation CPU time limit. A spending limit covers the account's total. Do not use one to do the other's job.
{{< /note >}}

## Four controls, four jobs

The billing guide has a small table that I keep open when I explain this to someone new. I shortened the wording.

| Control | Scope | At the threshold |
|---|---|---|
| Spending limit | Workers or Durable Objects, across the account | Blocks supported operations |
| Email alert | Workers or Durable Objects, across the account | Emails you; the product keeps running |
| Budget alert | Account-wide usage-based spend | Emails your recipients; products keep running |
| AI Gateway spend limit | AI requests through your gateway, by user, model or provider | Blocks matching requests until the budget window resets |

If your Worker calls a model through AI Gateway, that last row is a separate control with its own page. A Workers limit "does not include Durable Objects, Workers AI, Workers KV, R2, or other products." Each has separate charges. Do not assume one number covers your whole stack.

## Alert first, limit second

If you are not sure which Worker should stop, start with the control that stops nothing. An email alert tells you the spend is moving and leaves every Worker running. The guide says a policy with an email address sends notifications at 80% and 100% of the threshold, so a $20 alert can notify you at $16 and at $20.

The cf CLI can show you what it would do before it does it. The docs say: "To preview the request without creating a policy, add `--dry-run`." Use that first.

```bash {linenos=inline}
# Preview an email alert for Workers at $20. Nothing is created.
cf billing spend-policies create \
  --name 'Workers $20 email alert' \
  --product-id workers \
  --enabled true \
  --threshold-cents 2000 \
  --action notification \
  --notification-email billing@example.com \
  --dry-run
```

`--threshold-cents` is a whole number of US cents, so `2000` means $20 and zero is not supported. `--action notification` means email only. Replace the address with a mailbox a human reads.

Remove `--dry-run` to create the alert. The guide says you can create several alerts, including next to a limit, so a second one at a higher number is fine.

Once an alert has run for a week and you know your normal spend, add the limit. This is the command from Cloudflare's changelog, with the optional notification address added:

```bash {linenos=inline,hl_lines=[6,7]}
# A $50 Workers limit that blocks, with an email address attached.
cf billing spend-policies create \
  --name 'Workers $50 spending limit' \
  --product-id workers \
  --enabled true \
  --threshold-cents 5000 \
  --action usage_block \
  --notification-email billing@example.com
```

The two highlighted lines are the ones that matter. `5000` means $50, and `usage_block` means the limit blocks. If you get HTTP `409`, the guide says an enabled limit already exists for that product: update it, or turn it off before enabling another.

Now a gotcha that the dashboard path hides. The billing guide says: "Spending limits created in the dashboard do not automatically have an email recipient." To get notified, update the policy with a `notification_email`. The changelog says you also choose a notification email on the setup screen, so the two pages read slightly differently. Trust what your own screen shows. If you are not sure, run `cf billing spend-policies list` and read the policy back.

## Resume: three ways back

At 2 a.m. the hard part is not knowing what the limit does. It is knowing how to turn it back. The guide lists three options in **Spend Management**:

| Action | Result |
|---|---|
| Raise the limit above the product's current spend | Restores operations, keeps a higher limit |
| Turn the limit **Off** | Restores operations, keeps the saved amount |
| **Remove limit** and confirm | Restores operations, removes the policy |

"Changes can take a few minutes to apply." And: "Turning the same limit off and on does not reset this period's spend." The block also ends on its own at the start of the next subscription billing period, and an enabled limit stays configured for the new period.

From the terminal, an update replaces the whole policy, so you must pass every required option again, plus the policy's current `version`:

```bash {linenos=inline}
# 1. Find the policy and read its current version.
cf billing spend-policies list
cf billing spend-policies get <POLICY_ID>

# 2. Raise the Workers limit to $100. --if-match refuses to overwrite
#    someone else's newer change.
cf billing spend-policies update <POLICY_ID> \
  --if-match <VERSION> \
  --name 'Workers $100 spending limit' \
  --product-id workers \
  --enabled true \
  --threshold-cents 10000 \
  --action usage_block \
  --notification-email billing@example.com
```

Two error codes are worth knowing now, so you meet them calm instead of at 2 a.m. `412` means someone changed the policy: fetch it again, read the new settings, retry with the current version. `428` means you forgot `--if-match`. Both are in the CLI guide's error table.

The guide is blunt about the cost of resuming: "Further usage can incur charges once service resumes." Resuming is a spending decision. It belongs to a named person, not to whoever is awake.

## Name the owner before you turn it on

A limit without an owner is a trap with a timer. Write four lines on the ticket before you save anything:

```text
Cloudflare Workers spending control
  Product:        workers  (Durable Objects is a separate policy)
  Type:           email alert at $__ first; limit at $__ after one week
  Notified:       __________@________   (a mailbox a human reads)
  Blocked first:  list every Worker in this account, test ones included
  Allowed to raise or remove the limit:  __________
  Resume check:   open Billing > Spend Management, Workers row
```

The `Blocked first` line is the one that earns its keep. It forces someone to open the Workers list and read every name. If one of those names is production and another is a test Worker with a loop in it, you have just found the reason to split accounts or to start with an alert only.

![Three choices: email alert only, limit with Block usage, or both; each shows what keeps running and who is told.](/img/cloudflare-workers-spending-limit-whole-account-3.png)

{{< field-note title="Field note" >}}
On the Laravel/Vue SaaS desks I maintain, the shared switch is an old problem: one queue worker, one cron user, one API key serving both staging and production. The failure I plan for is rarely the big bill. It is the switch with the whole team's name on it that someone else flips by accident. A spending limit is one more switch of that kind.

To be clear about my own work: I read the docs on Nov 16 and ran nothing against a Cloudflare account for this post, and I have no incident of my own to report. What I would put on the ticket before enabling a Block usage limit is the owner block above, plus one rule: the person who raises the limit at 2 a.m. is named in advance, and they are not "whoever sees the email first."
{{< /field-note >}}

## What this post is not saying

- It is not saying you should turn on a blocking limit. For many accounts the right first step is an email alert.
- It is not saying every account is at risk. If your account holds one Worker, the shared gauge has one occupant.
- It is not saying the limit is a guaranteed cap. Cloudflare says plainly that it is not an exact maximum bill.
- It is not covering products the docs list separately. Durable Objects has its own limit and its own docs page, which I did not read for this post. KV, R2 and Workers AI have their own charges. AI Gateway has its own spend limits page.
- It is not saying anything about prices or plans. Look at your own Billing page for numbers.
- It is not a claim that your site is affected. A static site that serves files without running a Worker keeps running, by the docs' own rule.

## What you should do Monday morning

1. Open **Billing**, then **Spend Management**, in the Cloudflare account that pays for production. Find the **Workers** row. Write down whether a limit or alert exists today.
2. Open the Workers list for that account. Write every Worker name on the ticket. Mark each one **production**, **staging** or **test**. If production and test share the account, say so out loud in standup.
3. Create an email alert first with `cf billing spend-policies create ... --action notification --dry-run`. Read the preview. Then remove `--dry-run`.
4. Put a mailbox a human reads in `--notification-email`. Check the dashboard-created ones: the guide says they have no recipient by default.
5. Write down who may raise, turn off or remove a limit, and the one place they do it: Billing, then Spend Management.
6. Wait a week. Read the alerts. Only then decide whether a blocking limit is worth the shared-gauge risk, and at what number.
7. Add one line to your incident runbook: "Error 1103: open Billing, then Spend Management before filing a support ticket."

## What this connects to

This is a change-control problem more than a billing one: a shared setting, a named owner, a way back. I made the same argument about Wrangler config in [A Missing Previews Block Is Not a License to Reuse Production Bindings](/blog/missing-previews-block-is-not-production-bindings/), where preview and production shared more than the team realized. The Durable Objects side of Cloudflare has its own surprise in [A Green Wrangler Deploy Is Not an Immediate Durable Object Code Cutover](/blog/green-deploy-is-not-do-cutover/).

If a coding agent runs your deploys and could save a limit for you, read [I Do Not Give a Coding Agent Merge Rights](/blog/coding-agent-merge-rights/) first. Cloudflare's own changelog even offers a prompt for a coding agent to set the limit. The command is short; the decision about *which Worker should stop* is not. The wider family of agent-operations checks lives in [/ai-agent-operations/](/ai-agent-operations/), the tool notes are under [/developer-tools/](/developer-tools/), and new readers should start at [/start-here/](/start-here/).

## Further reading

{{< source href="https://developers.cloudflare.com/changelog/post/2026-11-13-spend-management/" label="Cloudflare changelog: Set spending limits for Workers and Durable Objects" >}}

{{< source href="https://developers.cloudflare.com/billing/manage/spend-management/" label="Cloudflare Billing: Spending limits and alerts" >}}

{{< source href="https://developers.cloudflare.com/workers/platform/spend-management/" label="Cloudflare Workers: Spending limits" >}}

{{< source href="https://developers.cloudflare.com/billing/manage/spend-management/cli/" label="Cloudflare Billing: Manage spending limits and alerts with the cf CLI" >}}
