# Contributing

## Adding a blog post

### Option A: Shell script (fastest)

```bash
./scripts/publish.sh "The quiet consolidation in Korean dev tooling" "News" "korea,devtools"
```

The script:
- Generates a slug from the title
- Pre-fills category based on day-of-week (Mon=News, Tue=Code, etc.)
- Adds tags
- Inserts the voice-template reminder
- Creates `content/posts/<date>-<slug>.md`

### Option B: Hugo CLI

```bash
hugo new content/posts/my-post.md
```

### Option C: Manual

Create `content/posts/2026-MM-DD-slug.md` with this frontmatter:

```yaml
---
title: "Your title"
date: 2026-06-16
description: "Optional 1-2 sentence summary."
categories: ["News"]
tags: ["korea", "devtools"]
draft: false
series: "Optional series name"
---
```

## Extending the design system

1. **Add the new token** to `design-system/tokens.json` in the appropriate section (color, typography, spacing, etc.)
2. **Add it to `design-system/tokens.css`** as a CSS custom property under the matching comment block
3. **Reference it** in `themes/zemnanet-theme/assets/css/theme.css` or `article.css` using `var(--zn-your-token)`
4. **Bump the version** in `hugo.toml` → `params.designSystemVersion`
5. **Document it** in `content/design-system.md`

## Theme structure

- `themes/zemnanet-theme/layouts/` — Hugo Go templates
- `themes/zemnanet-theme/assets/css/` — CSS (built into `public/css/`)
- `themes/zemnanet-theme/static/` — static files (favicon, etc.)

### Adding a partial

```bash
# 1. create partial
echo '<div class="zn-my-thing">{{ . }}</div>' > themes/zemnanet-theme/layouts/partials/mything/thing.html

# 2. use in a template
{{ partial "mything/thing.html" . }}
```

### Adding a content type

Create `themes/zemnanet-theme/layouts/<kind>/<layout>.html` with the right base template:

```html
{{ define "main" }}
  <section class="zn-section">
    <div class="zn-container zn-container--default">
      <h1>{{ .Title }}</h1>
      {{ .Content }}
    </div>
  </section>
{{ end }}
```

## Voice & style guide

From the [social-media-voice-guide](https://github.com/zemnanet/social-media-voice-guide) skill:

- **Simple declarative sentences.** Short paragraphs.
- **Contrarian angles** backed by specific numbers and real examples.
- **No corporate speak.** No "I'm excited to share." No emoji in body text.
- **Open with a hook** that stops the scroll.
- **End with a payoff** — uncomfortable truth → "worth it" resolution.

For the blog (longer form):
- Add subheads (H2) every 300-500 words
- Use lists for parallel ideas
- Code blocks with proper syntax (` ```python ` etc.)
- Author byline + series box at the top; tags + share + author bio at the bottom

## Quality gate (the 90+ rule)

Every post should pass the [content-ops expert-panel](https://github.com/zemnanet/marketing-team/tree/main/content-ops) quality check before publishing:

- Hook strength: 90+
- Information density: 90+
- Voice consistency: 90+
- Concrete examples: 90+
- Factual grounding: 90+

If any score is below 90, revise and re-score. Three rounds max. If still below 90, it ships anyway with a note explaining the trade-off (some posts are intentionally rough).

## Commit conventions

```
post: title of new post
design: token-name or component-name change
fix: what was wrong and how
chore: maintenance, deps, etc.
```

## Pull requests

PRs welcome for:
- Typo fixes
- Token additions that have a clear use case
- Voice/style corrections
- Accessibility improvements

PRs will be declined for:
- "Make it pop" style changes
- Hard-coded colors in templates (use tokens)
- Adding a new font family without prior discussion
