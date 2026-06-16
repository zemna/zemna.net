---
title: "Colophon"
description: "How this site is built — stack, tools, decisions, and credits."
date: 2026-06-16
draft: false
---

# Colophon

This page documents the **how** of zemnanet — what the site is built with, what tools run it, and why those choices were made.

## Stack

| Layer | Tool | Why |
|---|---|---|
| **Site generator** | [Hugo](https://gohugo.io/) v0.140 extended | Go single binary, sub-second builds, no Node toolchain |
| **Hosting** | [Cloudflare Pages](https://pages.cloudflare.com/) | Free, global CDN, zemna.net already on Cloudflare |
| **Domain** | [zemna.net](https://zemna.net) on Cloudflare Registrar | Same provider, no extra DNS hops |
| **Content** | Markdown + Hugo frontmatter | Plain text, version-controlled, AI-friendly |
| **Versioning** | Git on [GitHub](https://github.com/zemnanet) | Public history, no vendor lock-in |
| **Deployment** | git push to `main` → Cloudflare Pages build | Zero-config CI; the only "ops" is git |
| **Search** | Pagefind (planned) | Static index, runs at build time, no JS framework |

## Typography

- **Inter** for UI, navigation, and English headlines — open source, broad weight range, readable at small sizes.
- **Noto Serif KR** for Korean editorial content — open source, designed for the Korean script.
- **JetBrains Mono** for code — ligatures for `=>` and `!=`, tabular numerals.

## Colors

Three brand colors, derived from a synthesis of **Korean hanji** (off-white) and **Indonesian batik** (navy + vermilion). Full palette and semantic mappings live in the [design system](/design-system/).

## Automation

Posts are drafted with AI assistance under the [zemnanet content pipeline](https://github.com/zemnanet) — a 5-agent team (Strategist, Writer, Designer, Editor, Analyst) defined as an internal Hermes workflow. Every post passes through a quality gate before it ships.

The IG and X accounts are managed via [Zernio](https://zernio.com). Posting schedule:

- X — daily at 10:00 WIB
- Instagram — daily at 12:00 WIB

## Accessibility

- Color contrast for body text: 13.2:1 (off-white on ink-600) — passes WCAG AAA.
- Color contrast for links: 4.7:1 — passes WCAG AA.
- Skip-to-content link is the first focusable element.
- All interactive elements have visible focus states.
- prefers-reduced-motion respected in transitions.

## Performance

- First Contentful Paint target: < 1.0s on 3G
- Total page weight (home): < 200KB
- No third-party scripts, no analytics pixels, no fonts loaded from Google
- All fonts self-hosted with `font-display: swap`

## Privacy

- No cookies, no localStorage beyond theme preference
- No analytics — server log only, no visitor tracking
- No email collection, no newsletter
- RSS is the only "follow" mechanism

## Credits

- Site framework: [Hugo](https://gohugo.io/)
- Color inspiration: Korean hanji paper, Indonesian batik textiles
- Korean typography: [Noto Serif KR](https://fonts.google.com/noto/specimen/Noto+Serif+KR) (SIL OFL)
- Sans typography: [Inter](https://rsms.me/inter/) (OFL)
- Mono typography: [JetBrains Mono](https://www.jetbrains.com/lp/mono/) (OFL)
- Iconography: [Lucide](https://lucide.dev/) (ISC)

— _Last updated {{ now.Format "January 2006" }}_
