---
title: "How I Dissected 54 Design Systems and Transplanted Linear.app DNA Into My Hugo Blog in One Day"
date: 2026-06-16T18:00:00+07:00
draft: false
slug: "linear-design-system-hugo"
description: "How a Hugo blog adopted a token-driven design system from real references, turning brand choices into reusable CSS and publishing rules."
cover: "covers/linear-design-system.png"
topics: ["build"]
tags: ["design-system", "hugo", "linear", "css", "ai-agent", "build-in-public", "hermes"]
seo:
  primaryQuery: "Linear design system Hugo blog"
  secondaryQueries:
    - "Hugo design system"
    - "Linear app inspired blog design"
    - "token driven static site"
---

This morning I opened my blog and thought: this looks like a 2015 Tistory template. So I told my Hermes agent, in exactly these words: "This looks like garbage. Go through all 54 design systems and rebuild it with the best one."

It did.

## Why Linear.app Won Out of 54

The `popular-web-designs` skill in Hermes has templates for 54 real-world design systems — Stripe, Linear, Vercel, Notion, Figma, and 49 others. The agent loaded them all and surfaced five recommendations:

| System | Strengths | Fit |
|---|---|---|
| **Linear.app** | Dark-mode-native, 3-tier weight system, indigo accent | ★★★★★ |
| Vercel | Black & white precision, Geist font | ★★★★ |
| Stripe | Signature purple gradients, marketing polish | ★★★ |
| Sanity | Red accent, editorial-first layout | ★★★ |
| Framer | Bold + motion-forward | ★★ |

Linear won for one reason: it's the reference implementation for an IT/developer blog. Dark mode by default. No fluff. Three font weights that make code blocks and technical prose feel like they belong together. The indigo accent (`#5e6ad2`) is restrained enough to disappear when you're reading and present enough to guide your eye when you're scanning.

## Extracting the DNA: Design Tokens Into Hugo CSS

Linear's system boils down to a handful of principles:

```css
/* Near-black canvas — no gray-wash, no gradient tricks */
--zn-surface-0: #08090a;

/* Three-tier weight — Linear's signature */
--zn-wt-read:   400;  /* body */
--zn-wt-ui:     510;  /* UI emphasis */
--zn-wt-strong: 590;  /* headings */

/* Semi-transparent white borders — dark-on-dark depth */
--zn-border-subtle:  rgba(255, 255, 255, 0.05);
--zn-border:         rgba(255, 255, 255, 0.08);
--zn-border-strong:  rgba(255, 255, 255, 0.12);
```

I ported these into Hugo's `assets/css/tokens.css`, then rewrote `theme.css`, `article.css`, `featured.css`, and `interactions.css` to follow Linear's rules. 811 lines added, 706 removed.

The trickiest part was keeping Zemna's brand identity intact while adopting Linear's structure:

| Element | Zemna Brand | Linear DNA (adopted) |
|---|---|---|
| Primary | Navy `#1A2238` | Indigo `#5e6ad2` (accent only) |
| Accent | Vermilion `#E34234` | Preserved (Zernio brand consistency) |
| Background | — | `#08090a` (Linear's marketing black) |
| Font | D2Coding | Inter Variable + cv01/ss03 |

The rule: **Linear's skeleton, Zemna's colors.** Indigo stays in CTAs and highlights. Vermilion keeps the Zernio connection alive. Nothing clashes.

## Swapping AI Models Mid-Task (Unplanned Experiment)

This turned into an accidental model comparison. Three different models worked on the same codebase:

| Model | Provider | What It Excelled At |
|---|---|---|
| **MiniMax-M3** | — | Initial passes. Design intuition is there, but detail drift piles up. |
| **GLM-5.1** | OpenCode Go | Structural thinking. Templates, template logic, bug fixes. Fast and accurate. |
| **GPT-5.5** | OpenAI Codex | Full audit + polish. Logo design, SEO metadata, link checking, the final 10%. |

Takeaway: **one model end-to-end is worse than a pipeline.** GLM for architecture, MiniMax for drafts, GPT for finishing. Treat them like a human team and the output is better than any single model's best.

## What Changed in One Afternoon

```
┌──────────────────────┐     ┌──────────────────────┐
│  Before              │     │  After               │
│  ───────             │     │  ─────               │
│  Gray-wash default   │ ──► │  #08090a dark canvas │
│  Single weight font  │     │  3-tier weight system│
│  No taxonomy pages   │     │  /tags/ + /categories/│
│  Text-only hero      │     │  Jakarta skyline bg  │
│  No brand mark       │     │  Z-bridge logo       │
│  Broken OG meta      │     │  Full SEO + favicons  │
│  8rem hero padding   │     │  5rem (3rem mobile)  │
└──────────────────────┘     └──────────────────────┘
```

Three Git commits. 21 files changed. 1,500+ lines of CSS rewritten. One cover image generated (Jakarta skyline at golden hour, Bauhaus-inspired geometric abstract).

## What I Learned

1. **Choosing from 54 is faster than choosing from 3.** More options force clearer criteria. You stop asking "which one looks nice" and start asking "which one was built for my exact use case."

2. **AI agents respond better to blunt feedback.** "This looks like garbage" produced a better result than "let's improve the design." Sugarcoating wastes tokens.

3. **Static sites can have real design systems.** Hugo + CSS custom properties is enough. You don't need a React component library or a design tool. Design tokens in `:root` get you 90% of the way.

4. **Models have specialties — use them.** GLM for structure, GPT for polish. A multi-model pipeline beats any single model. This isn't a hot take; I literally watched it happen on my own codebase this afternoon.

---

Live site: [zemna.net](https://zemna.net)

Post URL: [zemna.net/blog/linear-design-system-hugo/](https://zemna.net/blog/linear-design-system-hugo/)

GitHub: [github.com/zemna/zemna.net](https://github.com/zemna/zemna.net)

{{< field-note title="Field note" >}}
A design system only starts paying back when future changes become boring. If a color, spacing rule, or card treatment still needs a one-off decision every time, it is not a system yet. It is a memory burden disguised as taste.
{{< /field-note >}}

## What you should do Monday morning

1. Pick one repeated component on your site.
2. Replace any hard-coded color or spacing with a token.
3. Change the token once and verify the component updates everywhere.

## Refresh note

This piece is now part of the site's operating archive. Read it as a decision pattern, not as a frozen news item: check whether the tool, model, or platform detail has changed, then keep the underlying verification habit if it still reduces operational risk.

## Deep refresh
## What I would keep from this experiment

The most useful part of this design-system exercise was not copying a look. It was forcing every visual choice into a named decision.

A personal technical blog can easily become a pile of one-off CSS. One card gets a slightly different radius. One page gets a different container. One article needs a special layout. After a few weeks, the site still works, but nobody can explain the system.

Tokens prevent that drift when they are treated as the source of truth.

For zemna.net, the important tokens are not only colors. They include spacing, container widths, typography, card radius, shadow strength, and motion duration. Those are the choices that make a site feel consistent across home, blog list, article detail, hub pages, and social previews.

## The difference between inspiration and imitation

Using Linear.app as a reference is useful because the product has strong hierarchy and restraint. But a blog should not become a Linear clone. The site still needs its own content rhythm, author voice, and developer notebook feel.

The parts worth borrowing are structural:

1. Sharp contrast between surface and content.
2. Clear interaction states.
3. Quiet borders instead of decorative noise.
4. Small motion that confirms behavior.
5. Dense but readable metadata.

The parts to avoid copying blindly are brand-specific: product screenshots, startup language, and overly polished marketing patterns that do not fit a personal engineering blog.

## What made the Hugo version work

Hugo is a good fit for this because the theme can stay close to the content. The same repository holds Markdown, layouts, CSS assets, image derivatives, and validation scripts.

That makes the design system operational. A change is not finished when CSS looks right locally. It is finished when:

1. Hugo builds.
2. Metadata checks pass.
3. Internal links still resolve.
4. The generated HTML contains the expected layout hooks.
5. The live site serves the new fingerprinted CSS.

That final point matters. Without fingerprinted CSS, Cloudflare can keep serving an older layout long enough to make a correct fix look broken.

## How to extend this safely

When adding a new visual component, I now try to answer these before writing CSS:

| Question | Good answer |
|---|---|
| Is this a new pattern or a variant? | Prefer variant unless the structure is truly new. |
| Which token controls spacing? | No one-off pixel values. |
| Which page proves the mobile behavior? | Check a real route, not an empty mockup. |
| Does light mode still work? | Avoid dark-only transparent white surfaces. |
| Can the verification script catch regressions? | Add a built-site check when possible. |

Related notes:

- [Start Here](/start-here/)
- [Developer Tools and Model Choices](/developer-tools/)
- [The JavaScript I Deleted With CSS](/blog/the-javascript-i-deleted-with-css-a-2026-survival-guide/)

## The maintenance payoff

The payoff showed up later, when the site needed article TOC changes, wider content, hub pages, WebP images, and CSS cache busting.

Without a design system, each fix would have been a visual argument. With the system in place, the question became smaller: which container, which spacing token, which component family, which verification check?

That is the real reason to build tokens for a personal site. Not because tokens are fashionable. Because future changes become safer, and a solo operator can keep the site coherent without redesigning it every week.

## How to verify this advice

Treat this as a small operating experiment around **token-driven blog design**.

The failure mode to watch is **one-off visual fixes accumulating drift**. It usually does not look dramatic at first. It looks like one convenient shortcut, one skipped check, or one tool decision that nobody writes down. A month later, the team has more output but less confidence in what actually changed.

A practical verification loop has four parts.

1. **Name the decision.** Write the decision in one sentence. If the team cannot name it, the team cannot improve it.
2. **Name the evidence.** Decide what would prove the decision helped. That might be a passing test, a smaller diff, a faster rollback, a lower bill, a clearer support path, or a page that earns impressions in Search Console.
3. **Name the counter-signal.** Decide what would prove the decision is not working. This prevents the team from defending a bad choice just because it was exciting at the start.
4. **Name the next review date.** A decision without a review date becomes architecture sediment.

For this topic, the metric I would watch is **repeatable layout and CSS verification**.

That metric does not need to be perfect. It only needs to be concrete enough that the next review is not based on memory. If the metric improves, keep the pattern and document it. If the metric stays flat, change the approach. If the metric gets worse, rollback or narrow the scope.

This is the operating habit I want the site to teach. A post should not end with a clever opinion. It should leave the reader with a way to test the opinion in their own repo, workflow, or team.

The same habit connects the rest of the site: [Start Here](/start-here/), [AI Agent Operations](/ai-agent-operations/), [Laravel and Vue SaaS Notes](/laravel-vue-saas/), and [Developer Tools and Model Choices](/developer-tools/). The topics are different, but the standard is the same: choose deliberately, leave proof, and keep the exit path visible.
