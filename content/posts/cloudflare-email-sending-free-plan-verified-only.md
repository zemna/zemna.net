---
title: "Your Cloudflare Worker Can Email You Alerts on the Free Plan. It Cannot Email Anyone Else"
date: 2026-11-27T07:00:00+07:00
draft: false
slug: "cloudflare-email-sending-free-plan-verified-only"
description: "Cloudflare put Email Sending on the Workers Free plan on Nov 24, but only for verified destination addresses. A tested sender, a grep for sends that only work for you, and one alert to run on Monday."
topics: ["devops"]
tags: ["cloudflare", "cloudflare-workers", "email-sending", "workers-free-plan", "transactional-email", "alerts", "error-handling"]
cover: /covers/cloudflare-email-sending-free-plan-verified-only.png
seo:
  primaryQuery: "cloudflare email sending workers free plan"
  secondaryQueries:
    - "E_RECIPIENT_PLAN_RESTRICTED cloudflare"
    - "cloudflare workers send_email binding verified destination address"
    - "cloudflare email sending free plan limits"
---

On Nov 24, 2026, Cloudflare announced that Email Sending is available on the Workers Free plan. If you read only the headline, it sounds like free transactional email for your app: signup confirmations, password resets, receipts. It is not that. The changelog says the free plan sends "to the verified destination addresses in your account," and to send to arbitrary addresses you upgrade to the Workers Paid plan.

Here is the part that costs a junior developer an afternoon. Every test you will ever write for this feature sends mail to yourself, and yourself is a verified address. So the test passes. The first real user signs up with an address you never verified, and the send fails. The mail code was fine. The plan rule was the problem.

I read the changelog and four pages of Cloudflare's docs on the day, wrote a small sender that names each failure in plain words, and ran it against a stand-in for the Workers email binding on this machine. The experience-based judgment I will keep repeating is simple: the question is not whether a send works for the address you tested, it is whether it survives the first address you did not.

<!--more-->

## What Cloudflare actually announced

Here is what the Nov 24 changelog entry says, in short:

- Email Sending now works on the Workers Free plan.
- You can onboard sending domains, which are domains you own that mail is sent from.
- You can send to verified destination addresses at no cost, "during development and testing."
- You upgrade to Workers Paid "when going to production to send to arbitrary addresses."
- The three ways to send are the Workers binding, the REST API and SMTP.
- The stated use for the free tier: "alerts, reports, and notifications to your own team without a paid plan."
- Sends to verified destination addresses "do not count toward the monthly quota or the daily sending limits."

A verified destination address is an email address in your Cloudflare account that has confirmed it is yours. You add it in the dashboard under Compute, Email Service, Email Routing, Destination Addresses. Cloudflare sends a verification email to that address, and someone has to open it and select "Verify email address." Until that click happens, the address is listed as pending. The Destination Addresses page lets you resend the verification email or delete an address.

Destination addresses are shared at the account level, so one verified address works for every domain in the account. The limits page lists 200 destination addresses per account. A team alert list is nowhere near that, but a user table is.

That is the whole story. A destination address is something you collect by hand, one confirmation email at a time. It is a short allow-list for your team, not a place to put your customers.

## The rule in one table

The limits page is explicit about who can receive mail:

| Plan | Sending domain onboarded | Recipient | Result |
|---|---|---|---|
| Workers Free | yes | A verified destination address | Sends. Free. Not counted toward monthly quota or daily limits. |
| Workers Free | yes | Any other address | Fails with `E_RECIPIENT_PLAN_RESTRICTED` |
| Workers Paid | yes | Any address | Sends |
| Any | yes, but the binding sets `destination_address` | A different address | Fails with `E_RECIPIENT_NOT_ALLOWED` |

The last row is a separate thing and I will come back to it. It is a restriction you choose on a binding, not a rule of your plan.

![A Worker calls env.EMAIL.send. Sending to oncall@example.com, a verified destination address, is delivered for free and is not counted in the quota. Sending to new-user@gmail.example, an address that is not verified, throws E_RECIPIENT_PLAN_RESTRICTED.](/img/cloudflare-email-sending-free-plan-verified-only-1.png)

The docs name the error for the middle row. In the Workers API error table, `E_RECIPIENT_PLAN_RESTRICTED` means the recipient is not a verified destination address and the account plan allows sending only to verified destination addresses. The changelog's own example handles it like this: it catches the error and returns an HTTP 403 with the text "Recipient is not a verified destination address."

Read that example again with a signup form in mind. A 403 from your mail function, inside the request that creates an account, is a signup that fails for the first stranger who tries it.

## Why your first test passes anyway

Think about how you would test a new mail feature on a Friday afternoon. You set `to` to your own address, run it, and the email arrives. Green.

Your own address passes for two reasons at once. You verified it so that you can receive the test. And the free plan allows exactly that case, because the feature was built for exactly that case: development and testing.

![Two lanes. Day 1, you test it: to you@yourdomain.com, a verified address, HTTP 200, passes. Day 2, the first real user signs up: to user.email, not verified, HTTP 403 or 500, fails.](/img/cloudflare-email-sending-free-plan-verified-only-2.png)

There is nothing wrong with the Free plan here, and Cloudflare did not hide the rule. The failure comes from the way a developer tests, which is with the one recipient that is guaranteed to work. It is a fixture problem, not a framework problem.

The fix is not clever. Test once with a recipient that is not on your verified list, and write down that the expected result on the free plan is the error. If you later upgrade to Workers Paid, that same test is the one that tells you the upgrade took effect.

## A sender that says why it failed

Cloudflare's Workers API page gives the shape of failure: errors from the email binding are thrown as standard `Error` objects with a `code` property, and a malformed argument throws a `TypeError` with no `code` at all. The error-code table has more than twenty entries. You do not need to handle all of them. You need to sort them into a few piles that tell a human what to do.

Here is `src/alerts.js`, which I wrote and ran. It never throws on a mail failure. It returns a small result object whose `kind` says which pile the failure belongs to:

```js {linenos=inline}
// src/alerts.js -- one place that sends mail and says, in plain words, what went wrong.
const KIND_BY_CODE = {
  E_RECIPIENT_PLAN_RESTRICTED: "plan",   // recipient is not a verified destination address
  E_RECIPIENT_NOT_ALLOWED: "binding",    // binding's destination_address / allowed_destination_addresses
  E_SENDER_NOT_VERIFIED: "binding",      // binding's allowed_sender_addresses
  E_SENDER_DOMAIN_NOT_AVAILABLE: "setup",
  E_SENDER_DOMAIN_NOT_CONFIGURED: "setup",
  E_EMAIL_SENDING_NOT_READY: "retry-later",
  E_RATE_LIMIT_EXCEEDED: "retry-later",
  E_DAILY_LIMIT_EXCEEDED: "retry-later",
  E_INTERNAL_SERVER_ERROR: "retry-later",
  E_RECIPIENT_SUPPRESSED: "recipient",
  E_VALIDATION_ERROR: "bad-input",
};

export async function sendMail(env, message) {
  try {
    const res = await env.EMAIL.send(message);
    return { ok: true, messageId: res.messageId };
  } catch (error) {
    // A malformed send() argument throws a TypeError with no code property.
    if (error instanceof TypeError) {
      return { ok: false, kind: "bad-input", code: null, message: error.message };
    }
    const code = error && error.code ? error.code : null;
    const kind = KIND_BY_CODE[code] ?? "unknown";
    console.error("mail failed:", kind, code);
    return { ok: false, kind, code, message: error.message };
  }
}

// Alerts always go to ONE address you own. The address is config, never user input.
export function sendAlert(env, subject, text) {
  return sendMail(env, { from: env.ALERT_FROM, to: env.ALERT_TO, subject, text });
}
```

The request-style handler from the changelog, rewritten on top of that sender, is the part that turns a plan error into the 403 you saw above. It is in the same file, and I ran it as cases 5 and 6 below:

```js
export async function fetchHandler(request, env) {
  const to = new URL(request.url).searchParams.get("to");
  const r = await sendMail(env, { from: env.ALERT_FROM, to, subject: "Hello", text: "Hello from the Worker." });
  if (r.ok) return new Response("Alert sent");
  if (r.kind === "plan") {
    return new Response("Recipient is not a verified destination address", { status: 403 });
  }
  return new Response(`mail failed: ${r.kind}`, { status: 500 });
}
```

Taking `to` from a query string is only a test harness. In a real app that value would come from your user table, which is exactly the situation this post is about.

Each pile maps to a different person's job:

- **`plan`** means a human decision. Either the recipient needs to be verified, or the account needs Workers Paid. No retry fixes it.
- **`binding`** means your own Wrangler config blocked the send. Someone edited a restriction. Fix the config.
- **`setup`** means the sending domain is not onboarded or not configured. A one-time job in the dashboard.
- **`retry-later`** covers the limits and the "setup in progress" code. These are the only failures a retry can fix.
- **`bad-input`** is your code passing something malformed.

Why bother with piles? Because the most common bad habit with a failed email is a bare `catch {}` or a `console.log` nobody reads. If your alert mailer fails and says nothing, you get silence, and silence looks exactly like a healthy system. I wrote about that shape in [a green cron exit is not a finished job](/blog/a-green-cron-exit-is-not-a-finished-job/), and the [zero-cost observability notes for agent crons](/blog/zero-cost-observability-agent-crons/) cover it from the other side: leave one small proof that the thing happened.

The Wrangler file that goes with it is short. The binding block is the one from the docs, and the two `vars` are your own sender and your own verified address:

```jsonc
{
  "name": "alert-worker",
  "main": "src/index.js",
  "vars": {
    "ALERT_FROM": "alerts@yourdomain.com",
    "ALERT_TO": "oncall@example.com"
  },
  "send_email": [{ "name": "EMAIL" }]
}
```

`ALERT_FROM` has to be an address on a sending domain you onboarded to Email Service. The send-bindings page says the sender address must belong to an onboarded Email Service domain. `ALERT_TO` has to be a verified destination address, or the first alert fails with the plan error you just read about.

## What I ran, and what I did not

I wrote a stand-in for `env.EMAIL` in Node. It knows only what the docs say: a send to an address outside the verified set throws an error with `code: "E_RECIPIENT_PLAN_RESTRICTED"`, a send with no `to`, `cc` or `bcc` throws a `TypeError` with no code, and a pinned binding refuses any other recipient with `E_RECIPIENT_NOT_ALLOWED`. Then I ran six cases through the sender above, including the changelog's request-style handler.

This is the real output. The sender also wrote one `console.error` line per failure (for example `mail failed: plan E_RECIPIENT_PLAN_RESTRICTED`) to the terminal; I left those lines out below to keep the table readable.

```text
1 alert to your verified address             {"ok":true,"messageId":"fake-1"}
2 signup mail to a customer, Free plan       {"ok":false,"kind":"plan","code":"E_RECIPIENT_PLAN_RESTRICTED","message":"recipient is not a verified destination address"}
3 send() with no recipient                   {"ok":false,"kind":"bad-input","code":null,"message":"send() needs at least one of to, cc or bcc"}
4 pinned binding, other verified address     {"ok":false,"kind":"binding","code":"E_RECIPIENT_NOT_ALLOWED","message":"recipient not allowed by binding"}
5 changelog-style handler, verified recipient {"status":200,"body":"Alert sent"}
6 changelog-style handler, customer recipient {"status":403,"body":"Recipient is not a verified destination address"}
```

Case 4 is worth a second look. The recipient `ops@example.com` is verified, yet the send still fails, because the binding was pinned to a different address. A verified recipient is necessary on the free plan, not always sufficient.

Here is what this run does not prove, plainly:

- **No email was sent.** I did not call Cloudflare. The stand-in only encodes the documented error behavior, so what it proves is that my sorting code handles those shapes. It proves nothing about Cloudflare's servers, delivery, or timing.
- **No Cloudflare account was touched.** I did not onboard a sending domain, verify an address or deploy a Worker for this post.
- **The error texts are mine.** The `code` strings come from the docs table. The `message` strings in the stand-in are my own wording, so do not match on them in real code. Match on `code`.
- **I did not check Paid plan numbers.** The post does not quote prices or monthly quotas, because I did not read the pricing page. The only quota fact here is the changelog's statement about verified sends.

## Find the sends that only work for you

The sender above handles failure well, but the better outcome is to find the risky sends before a user does. In a real project, the dangerous call sites have one thing in common: the `to` field comes from a user record, not from a fixed alert address.

I built a four-file fixture to show the search. One file is an alert helper that sends to `env.ALERT_TO`. One is a signup handler that sends to `user.email`. One is a weekly newsletter loop. One is the Wrangler file.

```bash
$ grep -rnE "EMAIL\.send\(" src | grep -v "ALERT_TO"
src/weekly.js:2:  for (const u of users) await env.EMAIL.send({ from: "news@yourdomain.com", to: [u.email], subject: "Weekly", text: "..." });
src/signup.js:2:  await env.EMAIL.send({ from: "welcome@yourdomain.com", to: user.email, subject: "Welcome", text: "Hi" });

$ grep -n "send_email" wrangler.jsonc
1:{ "name": "demo", "main": "src/alerts.js", "send_email": [{ "name": "EMAIL" }] }
```

The first command lists every `EMAIL.send(` call that does not mention `ALERT_TO`. In the fixture it found two lines: the signup and the weekly loop. Those are the two sends that cannot work on the free plan unless every recipient is a verified address. The alert helper was correctly left out.

This search is crude on purpose. It finds only calls written as `EMAIL.send(`, so a wrapper with another name, or a binding called something else, will slip past it. It reads one line at a time, so a `to` that spans several lines can be misjudged. It cannot tell you whether an address is verified. Treat the output as a list of places to read, not a verdict.

If you run a Laravel and Vue product on a different mail provider today, the same grep logic applies there: the mail calls that take their recipient from a database column are the ones to read before you change plans or providers. The [Laravel and Vue SaaS notes](/laravel-vue-saas/) collect more pre-change reading like this.

## Pin the binding to your own address

Cloudflare's send-bindings page describes three restrictions you can put on a `send_email` entry. Each entry supports one restriction choice:

- `destination_address`: the binding can send only to that one address.
- `allowed_destination_addresses`: the binding can send only to addresses on a list.
- `allowed_sender_addresses`: the binding can send only from addresses on a list.

A send outside the destination restrictions fails with `E_RECIPIENT_NOT_ALLOWED`. A send from an address outside the sender list fails with `E_SENDER_NOT_VERIFIED`.

For an alert Worker, the first one is a cheap safety rail. The page's own example:

```jsonc
{
  "send_email": [
    { "name": "NOTIFY_OPS", "destination_address": "ops@yourdomain.com" }
  ]
}
```

With that binding, even a bug that puts a customer address into `to` cannot send a message to the customer. The binding refuses before anything leaves. The plan rule stops a free account from mailing strangers because of billing. A pinned binding stops your code from mailing strangers because you decided it should.

I did not deploy a pinned binding for this post. The configuration above is quoted from the docs page, and my stand-in only simulates its refusal.

## Where the numbers moved

The changelog has a second part that is easy to skip, and it matters if you already watch your mail traffic. Messages that you send from a sending domain to verified destination addresses now count as Email Sending traffic. Before, that capability was an Email Routing feature and those messages were recorded as Email Routing traffic.

Practical effects, taken from the page:

- These messages show up in the Email Sending activity log and analytics.
- They no longer appear in Email Routing analytics.
- Email Sending events such as `message.delivered` and `message.bounced` are published to your event subscriptions for them.
- In the GraphQL Analytics API, you find them by filtering the Email Sending datasets on a new `isVerifiedRecipient` field.
- Messages sent from a domain that has only Email Routing configured are unchanged.

If you have a dashboard or a monthly report that counted alert emails from Email Routing, expect that count to move. If you count deliveries from event subscriptions, your handler now receives events for sends to verified addresses as well.

The limits page adds one line that belongs next to this: when an account reaches its daily sending limit, a Workers binding send fails with `E_DAILY_LIMIT_EXCEEDED`. The changelog says verified sends are exempt from those daily limits, so an alert-only Worker on the free plan should not hit that one.

{{< field-note title="Field note" >}}
The mail bug I trust least is the one that only fires for strangers. The shape is always the same: a staging setup where every notification lands in the team's own inbox, a launch day, and a first customer whose address was never in anyone's test data. A code review sees a correct `send()` call. Nothing in the diff shows the recipient rule, because the rule lives in a plan, a dashboard list, or a Wrangler file. This post is a design argument, not a war story: I did not hit this failure on a real account. When I read a Cloudflare Worker for the first time, I look for three things before the application code: what binding sends mail, who the `to` field comes from, and where a failed send is reported. If you run several small services, as in the [AI agent operations notes](/ai-agent-operations/), put the sorted-failure sender in one shared module once, so a plan error looks the same in every project and shows up in the one place you already read.
{{< /field-note >}}

## What this post is not saying

- It is not saying the free plan is a trick. The changelog states the verified-address limit in its first paragraph, and the limits page repeats it.
- It is not saying Cloudflare Email Sending is wrong for your product. If your app needs to mail arbitrary users, the stated route is Workers Paid, and I did not evaluate that plan's price or deliverability.
- It is not a delivery report. I never sent a real message, so I cannot say anything about inbox placement, spam filtering or latency.

## What you should do Monday morning

![Four steps: 1 verify your address under Destination Addresses and click the email link; 2 onboard a sending domain you own; 3 send one failure alert to that address from a Worker in try/catch; 4 grep every EMAIL.send call whose to is not your alert address.](/img/cloudflare-email-sending-free-plan-verified-only-3.png)

1. **Verify one address.** In the Cloudflare dashboard open Compute, Email Service, Email Routing, Destination Addresses. Add the address that should receive alerts, and click the link in the verification email. The docs list unverified addresses as pending, and I did not test what a send to a pending address does, so finish the click before the first send.
2. **Onboard one sending domain.** Pick a domain you own, and use an address on it as `ALERT_FROM`. The docs say the sender must belong to an onboarded domain, and `E_SENDER_DOMAIN_NOT_AVAILABLE` is what you get otherwise.
3. **Send one alert to yourself, from inside a `try/catch`.** Use the `sendAlert` function above. Make the failure case visible: log the `kind` and `code`, and make the job exit with an error if `ok` is false. Write down the result in the ticket.
4. **Send once to an address you own but did not verify, and expect the error.** On the free plan the expected result is `E_RECIPIENT_PLAN_RESTRICTED`. I did not run this step on a real account, so confirm it yourself instead of trusting my stand-in.
5. **Run the grep.** List every `EMAIL.send(` call that does not use your alert address. For each line, write one sentence: who is the recipient, and are they verified.
6. **Decide on purpose.** If any recipient is a customer, either verify the whole set (not realistic past a handful), move that traffic to a plan or provider that sends to arbitrary addresses, or leave the call out of the free-plan Worker.

If you run Workers for other jobs, two earlier notes cover neighbouring Cloudflare surprises. [A Workers spending limit covers the whole account](/blog/cloudflare-workers-spending-limit-whole-account/) explains why a test Worker can reach production, and [24 Workers AI models passed their Nov 20 cutoff](/blog/workers-ai-retired-model-ids-grep-config/) is another one-grep check you can add to the same Monday. The [AI agent operations hub](/ai-agent-operations/) and the [developer tools notes](/developer-tools/) collect the rest of the checklist habits, and [start here](/start-here/) lists where to begin.

## Further reading

{{< source href="https://developers.cloudflare.com/changelog/post/2026-11-24-email-sending-workers-free/" label="Cloudflare changelog: Email Sending is now available on the Workers Free plan (Nov 24, 2026)" >}}

{{< source href="https://developers.cloudflare.com/email-service/api/send-emails/workers-api/" label="Cloudflare Email Service: Email Sending Workers API (binding, send(), error codes)" >}}

{{< source href="https://developers.cloudflare.com/email-service/platform/limits/" label="Cloudflare Email Service: Limits (verified destination addresses, daily limits)" >}}

{{< source href="https://developers.cloudflare.com/email-service/configuration/destination-addresses/" label="Cloudflare Email Service: Destination addresses (how to verify one)" >}}

{{< source href="https://developers.cloudflare.com/email-service/configuration/send-bindings/" label="Cloudflare Email Service: Send bindings (destination_address and allowlists)" >}}
