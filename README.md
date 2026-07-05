# zemnanet

Personal blog at [zemna.net](https://zemna.net) — IT, AI, and dev tooling insights from a Korean senior dev working in Southeast Asia.

**Bridging Korean & Southeast Asian Tech.**

---

## Stack

- **Static site generator** — [Hugo](https://gohugo.io/) v0.140 extended
- **Hosting** — [Cloudflare Pages](https://pages.cloudflare.com/)
- **Domain** — zemna.net (Cloudflare Registrar)
- **Design system** — `design-system/` (token-first, single source of truth)
- **Content** — Markdown + Hugo frontmatter, version-controlled
- **Automation** — [Hermes marketing-team skill](https://github.com/zemnanet/marketing-team) (5-agent pipeline)
- **Social** — Zernio MCP, X at 10:00 WIB daily, IG at 12:00 WIB daily

## What's in this repo

```
zemna.net/
├── README.md                 ← this file
├── DEPLOYMENT.md             ← Cloudflare Pages setup guide
├── CONTRIBUTING.md           ← how to add posts / extend the design system
├── LICENSE                   ← MIT
│
├── hugo.toml                 ← site config (params, menu, taxonomies)
│
├── design-system/            ← token-first design system v1.0.0
│   ├── tokens.json           ← JSON source of truth
│   └── tokens.css            ← CSS custom properties build artifact
│
├── content/                  ← Markdown content
│   ├── _index.md
│   ├── about.md
│   ├── colophon.md
│   ├── design-system.md
│   └── posts/                ← blog posts
│       ├── 2026-06-12-ai-senior-developers.md
│       ├── 2026-06-13-hermes-agent-pragmatic-review.md
│       ├── 2026-06-14-indonesian-dev-scene-linux-moment.md
│       ├── 2026-06-15-stop-reaching-for-state-library.md
│       └── 2026-06-16-korean-devtool-consolidation.md
│
├── themes/zemnanet-theme/    ← custom Hugo theme (in-repo, not a submodule)
│   ├── theme.toml
│   ├── hugo.toml
│   ├── layouts/
│   │   ├── _default/
│   │   │   ├── baseof.html
│   │   │   ├── list.html
│   │   │   ├── single.html
│   │   │   ├── term.html
│   │   │   ├── page.html
│   │   │   └── 404.html
│   │   ├── index.html
│   │   └── partials/
│   │       ├── head/head.html
│   │       ├── header/header.html
│   │       ├── footer/footer.html
│   │       ├── brand/logo.html
│   │       └── scripts/theme-toggle.html
│   └── assets/css/
│       ├── tokens.css
│       ├── theme.css
│       └── article.css
│
├── static/                   ← favicon, og images
│
├── scripts/
│   └── publish.sh            ← one-shot publisher: title + category + tags → post
│
└── public/                   ← built output (gitignored)
```

## Quick start

```bash
# install hugo (if not present)
curl -fsSL -o /tmp/hugo.tar.gz "https://github.com/gohugoio/hugo/releases/download/v0.140.0/hugo_extended_0.140.0_linux-amd64.tar.gz"
tar -xzf /tmp/hugo.tar.gz -C /tmp && sudo mv /tmp/hugo /usr/local/bin/

# dev server
hugo server --port 1313 --buildDrafts

# publish a new post
./scripts/publish.sh "Title here" "News" "korea,devtools"

# production build
hugo --minify
```

## Design system

All visual decisions come from `design-system/tokens.json`. Three brand colors:
- **Navy** `#1A2238` — trust, structure
- **Off-white** `#FCFBF8` — page background, inspired by Korean hanji
- **Vermilion** `#E34234` — CTA, accent, inspired by Indonesian batik

Plus full 50-900 palettes, semantic colors, three font families (Inter / Noto Serif KR / JetBrains Mono), an 8px spacing scale, radius and shadow tokens, motion, and z-index.

See [content/design-system.md](content/design-system.md) for the full documentation. The docs are served at `/design-system/` on the live site.

## Authoring

Posts are written in Markdown with Hugo frontmatter:

```markdown
---
title: "The quiet consolidation in Korean dev tooling"
date: 2026-06-16
description: "Three acquisitions in twelve months."
categories: ["News"]
tags: ["korea", "devtools", "industry"]
draft: false
series: "Korean Tech in 2026"
---

The body goes here. Standard Markdown.
```

The `scripts/publish.sh` wrapper creates this for you. Or delegate to the Hermes marketing-team skill.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md). Short version: push to `main` → Cloudflare Pages auto-builds and deploys.

## License

MIT. The design system tokens are MIT-licensed and free to fork.

— _Shinjae Kang, Jakarta_
