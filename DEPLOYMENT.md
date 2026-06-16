# zemnanet — Cloudflare Pages Deployment Guide

This site is built with **Hugo** and deployed to **Cloudflare Pages** — a free static-hosting tier with global CDN, custom-domain support, and zero-config CI.

---

## 1. Prerequisites

- A Cloudflare account (you already have one — `zemna.net` is on Cloudflare)
- A GitHub repository with this Hugo site source code
- `zemna.net` DNS managed by Cloudflare (it is)

## 2. Push to GitHub

```bash
cd /home/linuxuser/projects/zemna.net
git init
git add .
git commit -m "feat: initial zemnanet site with design system v1.0.0"
git branch -M main
git remote add origin git@github.com:zemnanet/zemna.net.git
git push -u origin main
```

## 3. Connect to Cloudflare Pages

1. Go to https://dash.cloudflare.com → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. Select the `zemnanet/zemna.net` repository
3. **Build settings:**
   - **Framework preset**: Hugo
   - **Build command**: `hugo --minify`
   - **Build output directory**: `public`
   - **Environment variables** (advanced):
     - `HUGO_VERSION` = `0.140.0`
     - `HUGO_ENV` = `production`
4. **Save and Deploy**

First build takes ~30 seconds. The site is live at `zemnanet.pages.dev` immediately.

## 4. Custom domain (zemna.net)

1. In Cloudflare Pages → your project → **Custom domains** → **Set up a custom domain**
2. Enter `zemna.net` and `www.zemna.net`
3. Cloudflare will:
   - Detect the domain is already on Cloudflare DNS
   - Auto-create the required CNAME (`zemna.net` → `<project>.pages.dev`)
   - Provision a free Let's Encrypt cert
4. Wait 2-3 minutes for SSL provisioning

That's it. No DNS dance. No certificate request. The whole setup is about 5 minutes.

## 5. Subsequent deploys

Just push to `main`:

```bash
git push origin main
```

Cloudflare Pages detects the push, runs the build, and deploys. Build time: ~10-30 seconds.

## 6. Environment notes

### Hugo version pinning

The `HUGO_VERSION` env var must match the version in `hugo.toml` (extended). Current: **0.140.0**. To upgrade:

```bash
brew upgrade hugo  # local
# or: curl -fsSL -o hugo.tar.gz "https://github.com/gohugoio/hugo/releases/download/v0.X.Y/hugo_extended_0.X.Y_linux-amd64.tar.gz"
```

Then bump the env var in the Cloudflare Pages dashboard.

### i18n

The site is configured for `en` (default), `ko`, `id`. To add Korean/Bahasa content, create:

```
content/ko/posts/my-post.md
content/id/posts/my-post.md
```

With `language: "ko"` / `language: "id"` in the frontmatter. Hugo will pick the right file based on URL prefix (`/ko/posts/...`).

For now, the Korean and Bahasa pages are stubs. Translate as needed.

### Custom 404 page

`themes/zemnanet-theme/layouts/_default/404.html` provides a clean 404. Cloudflare Pages picks it up automatically.

### HTTP/3, Brotli, etc.

All on by default with Cloudflare Pages.

## 7. Local development

```bash
# install hugo (one-time)
curl -fsSL -o /tmp/hugo.tar.gz "https://github.com/gohugoio/hugo/releases/download/v0.140.0/hugo_extended_0.140.0_linux-amd64.tar.gz"
tar -xzf /tmp/hugo.tar.gz -C /tmp && sudo mv /tmp/hugo /usr/local/bin/

# dev server
hugo server --port 1313 --buildDrafts

# production build
hugo --minify

# output is in ./public
```

## 8. Content publishing

The `scripts/publish.sh` script is the entry point:

```bash
./scripts/publish.sh "The quiet consolidation in Korean dev tooling" "News" "korea,devtools"
# → content/posts/2026-06-16-the-quiet-consolidation-in-korean-dev-tooling.md
```

With the marketing-team Hermes skill installed, you can also delegate this:

```
User: "Write a Tuesday code-tip post about JavaScript state management"
Strategist → "Tue = Code. Topic: JS state. Hook: 'You don't need a library.'"
Writer → draft.md
Editor (content-ops/expert-panel) → score 92/100
Analyst → schedule for tomorrow 10:00 WIB
```

## 9. Monitoring

Cloudflare Pages dashboard shows:
- Build success/failure (with logs)
- Bandwidth used
- Request count
- Cache hit ratio

No server-side application monitoring is needed — the site is static.

## 10. Cost

**$0/month.** Cloudflare Pages free tier covers:
- Unlimited static requests
- 500 builds/month
- Unlimited bandwidth
- Free SSL
- 100 custom domains

## 11. What if I want to add a CMS later?

Don't. The whole point of this stack is **no CMS**. Content is Markdown in Git. The publisher (Hermes) is your CMS. You don't need anything else.

If you ever feel like you need a CMS, write a skill that wraps the publish.sh script. That's the equivalent operation.
