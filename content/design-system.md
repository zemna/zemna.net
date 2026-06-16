---
title: "Design System"
description: "The zemnanet design system — tokens, components, and patterns used across zemna.net, social media, and any zemnanet-owned surface."
date: 2026-06-16
draft: false
---

# zemnanet Design System

A single source of truth for the **visual** and **typographic** language used across:

- zemna.net (this website)
- Blog posts and series
- Social media graphics (IG carousels, X headers, podcast covers)
- Any presentation, README, or tool that says "zemnanet" on it

The system is **token-first** — every visual decision is a named token. No hard-coded values in templates. No drift between surfaces.

## Tokens

The token set lives in the theme source at `themes/zemnanet-theme/assets/css/tokens.css`. The production build publishes the minified CSS custom properties at [`/css/tokens.min.css`](/css/tokens.min.css).

### Color — Brand palette

Three colors carry the brand. Everything else is a derivative.

| Token | Hex | Role |
|---|---|---|
| `--zn-navy-700` | `#1A2238` | Brand navy. Trust, structure, body emphasis on light backgrounds. |
| `--zn-offwhite-50` | `#FCFBF8` | Brand off-white. Page background. Inspired by Korean hanji. |
| `--zn-vermilion-500` | `#E34234` | Brand vermilion. CTAs, links, accent. Inspired by Indonesian batik. |

Full palettes (50–900 scales) are defined in `tokens.json` for both primary colors.

### Color — Semantic

| Token | Hex | Use |
|---|---|---|
| `--zn-success` | `#3A7D44` | Positive deltas, builds passing |
| `--zn-warning` | `#D4922B` | Caution, deprecated APIs |
| `--zn-danger`  | `#C42B1F` | Errors, breaking changes |
| `--zn-info`    | `#2E4073` | Informational notes |

### Color — Theme

Light and dark themes are defined as semantic tokens (`--zn-bg`, `--zn-text`, etc.) that flip automatically with `prefers-color-scheme: dark` or `[data-theme="dark"]`.

### Typography

Three font families:

- **Sans** — `Inter` for UI, navigation, headlines
- **Serif** — `Noto Serif KR` for editorial long-form Korean content
- **Mono** — `JetBrains Mono` for code, file paths, technical values

Type scale runs from `--zn-text-xs` (12px) to `--zn-text-6xl` (60px), all on a 1.25 ratio.

### Spacing

8px base scale, `--zn-space-0` (0) through `--zn-space-32` (128px). T-shirt sizes for components, raw px values for layout.

### Radius

`--zn-radius-{none,sm,md,lg,xl,2xl,full}`. Most cards use `lg` (8px). Pills use `full` (9999px).

### Shadow

`--zn-shadow-{none,xs,sm,md,lg,xl,inner}`. All shadows use the navy base color at low alpha so dark-mode shadows stay coherent.

## Components

Component patterns are documented inline in the Hugo theme at `themes/zemnanet-theme/layouts/`. Naming convention is BEM with a `zn-` prefix:

- `zn-container` — page container, with size modifiers (`--narrow`, `--default`, `--wide`, `--full`, `--prose`)
- `zn-button` — button, with variants (`--primary`, `--accent`, `--ghost`)
- `zn-card` — content card with cover + body + footer
- `zn-tag` — taxonomy pill
- `zn-prose` — long-form article typography
- `zn-icon-button` — square icon-only button (theme toggle, search, share)

Every component is a `layouts/partials/<area>/<component>.html` file. Add or modify there.

## Usage rules

1. **Never hard-code a color in a template.** Use the nearest semantic token. If the right token doesn't exist, add it to `tokens.json` first.
2. **Never hard-code a font size in CSS outside the type scale.** Use `--zn-text-*`.
3. **Never hard-code spacing.** Use `--zn-space-*`.
4. **Token changes are a breaking change.** When bumping a token, grep for all uses and update in the same commit.
5. **The system applies to social media too.** When generating IG or X graphics, the same colors and type go on the image. No "social exception" palette.

## How to extend

1. Add the new token to `design-system/tokens.json` (and a comment in `tokens.css` so the build artifact gets the comment too)
2. Rebuild CSS: `hugo server` will pick up the change automatically
3. Reference via `var(--zn-your-new-token)` in `theme.css` / `article.css`
4. Document it on this page

## Versioning

The design system is versioned. Current version: **1.0.0**.

When making breaking changes, bump the version in `hugo.toml` under `params.designSystemVersion` and add a migration note in the [colophon](/colophon/).
