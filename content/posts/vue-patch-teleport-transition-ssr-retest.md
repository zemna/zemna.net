---
title: "Vue's Latest Patch Touches Teleport, Transition and SSR CSS Variables: Where to Re-test Before You Bump"
date: 2026-11-22T07:00:00+07:00
draft: false
slug: "vue-patch-teleport-transition-ssr-retest"
description: "Vue's Nov 20 patch fixes SSR CSS variables on Teleport roots, Transition classes that never leave, and Teleport hydration. A repo scanner, a real before/after test, and what to re-run before you bump."
topics: ["frontend"]
tags: ["vue", "ssr", "teleport", "transition", "patch-management", "laravel", "inertia", "testing"]
cover: /covers/vue-patch-teleport-transition-ssr-retest.png
seo:
  primaryQuery: "vue teleport ssr css v-bind missing"
  secondaryQueries:
    - "vue transition enter-to class stays on element"
    - "vue ssr hydration teleport nested same target"
    - "vue keepalive ssr css variables v-bind"
---

Every Vue app has a pop-up somewhere. A modal, a tooltip, a dropdown that has to sit on top of everything else, so someone wrapped it in `<Teleport to="body">`. It looks right in the browser. Then a teammate turns on server rendering, and the first paint of that pop-up is missing a style.

On Nov 20, 2026, Vue shipped a patch release that fixes that exact shape of bug, plus a few neighbours: a CSS class that stays on an element after the animation was cancelled, and a hydration mix-up when one teleport sits inside another. The changelog marks none of it as a security fix. None of it needs a weekend. But all of it lives in the parts of a Vue app that nobody tests on purpose.

So the useful question is not "should we upgrade?" It is "which of our own pages touch these features, and how would we see it break?"

<!--more-->

The question is not whether the patch notes sound relevant. It is whether you can name the files in your own repo that use the feature, and show the difference on one of them.

## What the patch lists, in plain words

I read the Vue `CHANGELOG.md` on `main` on Nov 22, about 08:00 Jakarta time. The entry for 3.5.46 is dated 2026-11-20. The GitHub release for the same tag was published on 2026-11-20 at 08:18 UTC, and its body only points to the changelog. The previous patch, 3.5.45, is dated 2026-11-05. On the npm registry the `latest` tag is 3.5.46 and the `rc` tag is 3.6.0-rc.16, so Vue 3.6 is still a release candidate.

The changelog has sixteen lines under "Bug Fixes". Here are the ones that matter for an everyday app, grouped by what they touch. The wording in the middle and right columns is mine; the issue and pull request pages say more.

| Fix area | What in your app touches it | How you would see it break |
|---|---|---|
| CSS variables in server rendering: `compiler-ssr` "inject css vars into the content of keep-alive and teleport"; "inject css vars through root loops and fragments" | A component with `v-bind()` inside `<style>` whose root is a `<Teleport>`, a `<KeepAlive>`, or a `v-for` | The server HTML has no `--hash-name:` style on that element. It looks unstyled until JavaScript takes over |
| CSS variables after a root change: `runtime-dom` "apply css vars to teleported content replaced without patching the teleport" | A component inside a Teleport that swaps its own root element | The new element misses the variable, so a width or colour from `v-bind()` is ignored |
| Teleport hydration: `hydration` "claim disabled teleport target anchors before nested teleports" | A `<Teleport :disabled="...">` that contains another Teleport to the same target, on a server-rendered page | Later teleports to that target are matched against the wrong server HTML. The pull request calls the comment-node case "silent misbinding in production" |
| Transition: "ignore stale enter callbacks on a reused element", "ignore stale leave callbacks on a reused element", "only skip enter for the element that is leaving" | `<Transition>` with `v-show`, such as hover tooltips and menus that open and close fast | A class like `*-enter-to` stays on the element, or the next show does not animate |
| `shared`: "handle objects without a prototype in looseEqual" | `v-model` on radios and checkboxes where the value is an object with no prototype, such as `Object.create(null)` | An error instead of a comparison |

## Find the places in your own repo first

Before you test anything, you need a list. The patch only matters where you use these features, and most teams cannot say from memory which components use `<Teleport>`.

This script reads `.vue` files and prints each place where a Teleport, KeepAlive or Transition tag appears, and each `v-bind()` inside a `<style>` block. It also flags Teleports that target `body` or can be disabled, and prints one extra line for any file that has both a `v-bind()` and a Teleport or KeepAlive, because that pairing is what the CSS-variable fix is about. It reads files and nothing else.

```python
#!/usr/bin/env python3
"""List the places in a Vue repo that the Vue 3.5.46 fix list touches.

Usage: vue_retest_scan.py [REPO_DIR]
Exit 0 = nothing found. Exit 1 = places to re-test. Exit 3 = bad path.
"""
import re
import sys
from pathlib import Path

SKIP = {"node_modules", ".git", "vendor", "dist", "build", "public", ".nuxt", ".output", "storage"}
TAGS = {
    "teleport": re.compile(r"<teleport\b", re.I),
    "keepalive": re.compile(r"<(keepalive|keep-alive)\b", re.I),
    "transition": re.compile(r"<(transition|transitiongroup|transition-group)\b", re.I),
}
STYLE_BLOCK = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
TO_BODY = re.compile(r"""\bto\s*=\s*["']body["']""")
DISABLED = re.compile(r"(:disabled|\bdisabled\b)")


def scan_file(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        for area, rx in TAGS.items():
            if rx.search(line):
                note = ""
                if area == "teleport":
                    if TO_BODY.search(line):
                        note += " [to=body]"
                    if DISABLED.search(line):
                        note += " [disabled]"
                hits.append((area, number, line.strip()[:90] + note))
    for block in STYLE_BLOCK.finditer(text):
        start_line = text.count("\n", 0, block.start(1)) + 1
        for offset, line in enumerate(block.group(1).splitlines()):
            if "v-bind(" in line:
                hits.append(("cssvars", start_line + offset, line.strip()[:90]))
    return hits


def main(argv):
    root = Path(argv[0] if argv else ".")
    if not root.is_dir():
        print(f"not a folder: {root}")
        return 3
    totals = {"teleport": 0, "keepalive": 0, "transition": 0, "cssvars": 0}
    files_with = {}
    for path in sorted(root.rglob("*.vue")):
        if SKIP & set(path.relative_to(root).parts):
            continue
        hits = scan_file(path)
        if not hits:
            continue
        rel = path.relative_to(root)
        files_with[str(rel)] = {a for a, _, _ in hits}
        for area, number, text in hits:
            totals[area] += 1
            print(f"{area:10} {rel}:{number}  {text}")
    pairs = sorted(f for f, a in files_with.items() if "cssvars" in a and ({"teleport", "keepalive"} & a))
    for f in pairs:
        print(f"pair       {f}  v-bind() in a file with Teleport or KeepAlive")
    if not files_with:
        print("nothing found")
        return 0
    print("files: %d | teleport %d | keepalive %d | transition %d | cssvars %d | pairs %d" % (
        len(files_with), totals["teleport"], totals["keepalive"], totals["transition"], totals["cssvars"], len(pairs)))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

I ran it on a small fixture I made: a modal with `<Teleport to="body">` and a `v-bind()` style, a tooltip with `<Transition>` and `v-show`, and a page with `<KeepAlive>` and a disabled teleport. I also put a `.vue` file inside `node_modules` to check that it is skipped.

```text
$ python3 vue_retest_scan.py fixture
teleport   resources/js/Components/Modal.vue:5  <Teleport to="body"> [to=body]
cssvars    resources/js/Components/Modal.vue:10  .modal { color: v-bind(color); }
transition resources/js/Components/Tooltip.vue:2  <Transition name="fade">
keepalive  resources/js/Pages/Tabs.vue:2  <KeepAlive><component :is="tab" /></KeepAlive>
teleport   resources/js/Pages/Tabs.vue:3  <teleport to="#portal" :disabled="isMobile"><p>x</p></teleport> [disabled]
pair       resources/js/Components/Modal.vue  v-bind() in a file with Teleport or KeepAlive
files: 3 | teleport 2 | keepalive 1 | transition 1 | cssvars 1 | pairs 1
$ echo $?
1
```

An empty folder printed `nothing found` and exited 0. A missing path printed `not a folder` and exited 3. On this site's repository, a Hugo site with no `.vue` files, it found nothing, which says the scanner works, not that any Vue app is clean.

It has one blind spot. It pairs `v-bind()` and `<Teleport>` only inside one file. If the Teleport sits in a child component and the `v-bind()` is in the parent, the file is not paired. Treat the `pair` line as the first place to look, not the only one.

## Test 1: the CSS variable that went missing on the server

The Vue docs describe the `v-bind()` feature in `<style>` like this: the value is "compiled into a hashed CSS custom property, so the CSS is still static", and the property is "applied to the component's root element via inline styles". In plain words: your style says `color: v-bind(color)`, Vue turns that into `color: var(--hash-color)` and puts `--hash-color: red` on the component's root element.

Now ask what the root element is when the root is a `<Teleport>`. A Teleport does not render an element of its own. The pull request for this fix says that `KeepAlive` and `Teleport` "render their children without an element of their own in SSR, so the props bound to them never reach the output".

To check it, I made two throwaway projects. One has `vue@3.5.45` and one has `vue@3.5.46`, each installed with exact versions, together with the matching `@vue/compiler-sfc` and `@vue/server-renderer`. The same script compiles three tiny components for server rendering and prints the HTML. Here are the three components, shortened to the part that matters:

```vue
<!-- teleportRoot.vue -->
<script setup>const color = 'red'</script>
<template><Teleport to="body"><div class="modal">hi</div></Teleport></template>
<style scoped>.modal { color: v-bind(color) }</style>

<!-- keepAliveRoot.vue: same style, root is <KeepAlive><div class="tab">tab</div></KeepAlive> -->
<!-- vForRoot.vue:      same style, root is <div v-for="item in items" :key="item" class="item"> -->
```

The harness uses only public pieces: `parse`, `compileScript` and `compileTemplate` from `@vue/compiler-sfc` (with `ssr: true` and `ssrCssVars`), then `renderToString` from `@vue/server-renderer`. Teleport content is not part of the returned string, so the harness also prints `ctx.teleports`, which is where Vue puts it.

```js
const { descriptor } = parse(src, { filename })
const script = compileScript(descriptor, { id })
const tpl = compileTemplate({
  source: descriptor.template.content, filename, id,
  scoped: descriptor.styles.some((s) => s.scoped),
  ssr: true,
  ssrCssVars: descriptor.cssVars,
  compilerOptions: { bindingMetadata: script.bindings },
})
// stitch script + template into one ES module, import it, then:
const ctx = {}
const html = await renderToString(createSSRApp(mod.default), ctx)
console.log(html, ctx.teleports)
```

Here is what came out. The CSS variable is the `--abc12345-color:red;` part; I gave every component the id `abc12345` so the output is easy to compare.

```text
=== vue 3.5.45
teleportRoot   teleports={"body":"<!--teleport start anchor--><div class=\"modal\" data-v-abc12345>hi</div><!--teleport anchor-->"}
keepAliveRoot  html=<div class="tab" data-v-abc12345>tab</div>
vForRoot       html=<!--[--><div class="item" data-v-abc12345>a</div><div class="item" data-v-abc12345>b</div><!--]-->

=== vue 3.5.46
teleportRoot   teleports={"body":"<!--teleport start anchor--><div class=\"modal\" style=\"--abc12345-color:red;\" data-v-abc12345>hi</div><!--teleport anchor-->"}
keepAliveRoot  html=<div class="tab" style="--abc12345-color:red;" data-v-abc12345>tab</div>
vForRoot       html=<!--[--><div class="item" style="--abc12345-color:red;" data-v-abc12345>a</div><div class="item" style="--abc12345-color:red;" data-v-abc12345>b</div><!--]-->
```

All three differ in the way the changelog says. In 3.5.45 the server HTML has no `style="--abc12345-color:red;"`, so `color: var(--abc12345-color)` resolves to nothing until the browser version of the component runs and sets it. In 3.5.46 the variable is in the server HTML on the modal, on the keep-alive child, and on each `v-for` item.

What this means for a real page: before hydration, that modal, tab or list row can render with the browser's default colour, width or spacing, then jump when JavaScript starts. It is a short flash that is easy to dismiss as "slow JavaScript". If the `v-bind()` value controls a panel width, the jump is visible.

The comparison above is the whole claim. I rendered the HTML string. I did not open it in a browser, and I did not check any real app.

One tip from the Vue server-rendering guide is easy to miss: avoid targeting `body` with Teleports when you also use SSR, because `body` usually holds other server-rendered content, which "makes it impossible for Teleports to determine the correct starting location for hydration". It recommends a dedicated container such as `<div id="teleported"></div>`. The scanner prints `[to=body]` for that reason. A hydration fix does not turn `to="body"` into a good idea.

![Server HTML for three components, Vue 3.5.45 versus 3.5.46: the CSS variable is missing on the Teleport, KeepAlive and v-for roots in 3.5.45 and present in 3.5.46.](/img/vue-patch-teleport-transition-ssr-retest-1.png)

## Test 2: the class that never left

The Transition fixes are easier to read from the pull requests than from the changelog. The first describes a hover tooltip, where the mouse just passes over the trigger. The element is shown with `v-show` and hidden again before the first animation frame of its enter. The pull request says `*-enter-to` then stays on the element, and if your CSS styles that class, the next show does not animate. The second pull request covers the leave side: a cancelled leave whose timer fires later and removes a class the next enter also needed, which is normal when utility CSS uses one class string for both.

I tried the first one in jsdom, a simulated browser for Node, with `pretendToBeVisual` so animation frames run. The component is a `<Transition>` with a `v-show` element and `duration: 300`. The script shows it, hides it again right away, waits 120 ms, then reads the element's classes.

```js
const visible = ref(false)
const App = {
  setup() {
    return () =>
      h(Transition, { name: 'v', duration: 300 }, {
        default: () => withDirectives(h('div', { id: 't' }, 'tip'), [[vShow, visible.value]]),
      })
  },
}
createApp(App).mount('#app')
await nextTick()
const el = document.getElementById('t')

visible.value = true;  await nextTick()
visible.value = false; await nextTick()   // hidden before the enter's first frame
await sleep(120)
console.log('classes after 120 ms:', JSON.stringify(el.className))
await sleep(500)
console.log('classes after 620 ms:', JSON.stringify(el.className))
```

```text
=== vue 3.5.45
A) classes after 120 ms: "v-leave-active v-enter-to v-leave-to"
A) classes after 620 ms: "v-enter-to"

=== vue 3.5.46
A) classes after 120 ms: "v-leave-active v-leave-to"
A) classes after 620 ms: ""
```

In 3.5.45 the element still carries `v-enter-to` more than half a second after it was hidden, long after both transitions should be over. In 3.5.46 the class is gone, and the element ends with no transition classes. That is the symptom the pull request describes. If your CSS puts an `opacity` or `transform` on `.v-enter-to`, a stuck class is a stuck style.

![Classes left on a tooltip element after show-then-hide: Vue 3.5.45 keeps v-enter-to after 620 ms, Vue 3.5.46 leaves none.](/img/vue-patch-teleport-transition-ssr-retest-2.png)

I also wrote a second case for the leave side: hide, show again before the leave timer fires, then watch the classes. Both versions gave the same classes at every step I looked at, so I did not reproduce the leave bug. That does not make the leave fix empty; my timings and CSS-free setup can simply miss the path the pull request describes. jsdom has no layout and no real transitions, which is why I set an explicit `duration`.

## One small one: `looseEqual` on a prototype-less object

The `shared` fix is one function, so it is easy to check. Vue uses `looseEqual` to compare values for radio and checkbox `v-model`.

```js
const { looseEqual } = require('@vue/shared')
looseEqual(Object.create(null), Object.create(null))
```

```text
vue 3.5.45  looseEqual(null-proto, null-proto) THROWS: Cannot convert object to primitive value
vue 3.5.46  looseEqual(null-proto, null-proto) = true
```

Objects with no prototype are rare in app code. If you do not use them as `v-model` values, this line is not for you.

## What I could not reproduce here

Three things in the list need a real browser or a real app. I did not run them:

- **Teleport hydration anchors.** The pull request explains the failure well. In its words, server rendering writes the outer teleport's empty anchors into the target before the nested block, while hydration "hydrated its children first and only then" claimed the anchors, so the nested teleport took the outer one's. It also says that when the nested content is a `v-if` comment, this is "silent misbinding in production". To see it you need server HTML, a browser and a page with the nesting. I did not build that.
- **Suspense with an out-in transition.** The changelog says mounted hooks now run once. I did not test it.
- **The SFC compiler lines** (tsconfig matching, generic types, `onWarn`). Your type-check run is the test.

Also, the server-render alias fix. I compiled `<label className="field" htmlFor="email">` with both versions and both printed `class="field"` and `for="email"`. My sample did not show the difference the pull request describes, so I have no before-and-after for that line.

## How to bump without guessing

1. **Bump in a branch.** Pin the exact version, not a range. A framework patch is the kind of change that should not slide in with an unrelated `npm update`.
2. **Rebuild the server bundle.** The CSS-variable fix is in the template compiler. If you run a separate SSR build, such as Inertia SSR or a Nuxt build, it has to be rebuilt to pick the fix up. A running server process does not change by itself.
3. **Open the pages the scanner listed with the browser console open.** Vue prints a warning in development when the server markup does not match what the client builds. Any warning on a Teleport page is the thing to read first.
4. **Reload each modal with throttled CPU.** The flash is short on a fast laptop. In the browser's performance panel, 4x or 6x CPU slowdown makes a missing variable easy to see.
5. **Open and close each tooltip fast.** Hover on and off the trigger a few times, then inspect the element. After the transition ends it should carry no `*-enter-to` or `*-leave-to` class.
6. **Look at the diff of your lockfile.** `vue`, `@vue/compiler-sfc`, `@vue/server-renderer` and the other `@vue/*` packages should all move to the same version. A mix is a finding.
7. **Write the result next to the bump.** One line: which pages you opened and what you saw.

![Five checks in order: list the pages, bump in a branch, rebuild the server bundle, open with the console, hover tooltips fast.](/img/vue-patch-teleport-transition-ssr-retest-3.png)

{{< field-note title="Field note" >}}
On a Laravel and Vue project the server render usually comes from Inertia SSR or a Node process next to PHP, and it is the part nobody opens during a normal review. The expensive part of a framework patch is not installing it. It is knowing which five pages to open afterwards, and a modal that is teleported once and forgotten is exactly the kind of page that never makes the list. That is why the scanner comes first. I did not check any Modoo project for this post, so I cannot say which of its pages use these features.
{{< /field-note >}}

## What this does not say

- It does not say every Vue app is affected. Each fix needs a feature you use.
- It does not say 3.5.45 is broken in general. It says the specific cases shown above behave differently.
- It does not say Vue 3.6 is stable. The npm `rc` tag is 3.6.0-rc.16.
- It does not say any app of mine hit these bugs. I checked a harness, not a production page.

## What I did and did not verify

On Nov 22 at about 08:00 Jakarta time I read the Vue `CHANGELOG.md` from `main`, the GitHub release objects for `v3.5.46` and `v3.5.45`, and the npm dist-tags for `vue`. I read the issue and pull request text, through the GitHub API, for the fixes in the table, and the relevant parts of four Vue docs pages: Teleport, SFC CSS features, Server-Side Rendering and Transition.

I ran everything shown above on Node 26.12.1 with `vue`, `@vue/compiler-sfc` and `@vue/server-renderer` pinned at 3.5.45 in one folder and 3.5.46 in another, plus jsdom 31.0.1 for the Transition case. The scanner ran on a fixture, an empty folder, a missing path and this site's repository. I did not run any real application, any browser, the Teleport hydration case, the Suspense case or the SFC compiler cases.

## What you should do Monday morning

1. **Run the scanner on every repo with a `.vue` file.** Save the output. It is your list of pages to open.
2. **Read the `pair` lines first.** A `v-bind()` in a file with a Teleport or KeepAlive is the case the compiler fix is about.
3. **Read the `[to=body]` lines next.** Move them to a dedicated container if you server-render, as the Vue docs recommend.
4. **Bump `vue` in a branch,** pin it exactly, and rebuild the server bundle.
5. **Open each listed page** with the console open, once with the CPU throttled, and hover every tooltip.
6. **Check that all `@vue/*` packages in the lockfile moved together.**
7. **Write down the result,** one line per page, in the pull request.

## What this connects to

It is the same habit as [A UI kit lockfile bump is change control, not cosmetics](/blog/ui-kit-bump-is-change-control/): a bump is a decision that needs a list of places and an owner. [Vite Fixed a Critical Dev Server Bug](/blog/vite-dev-server-bug-check-host-flag/) used a scanner and a version check the same way. If you are watching Vue 3.6, [Vue 3.6 Vapor Mode: Build a Pilot Harness Before You Change a Rendering Path](/blog/vue-3-6-vapor-mode-no-virtual-dom-no-rewrite/) covers the pilot side.

More on Laravel and Vue projects is in the [Laravel and Vue SaaS hub](/laravel-vue-saas/) and the [developer tools hub](/developer-tools/).

## Further reading

- {{< source href="https://github.com/vuejs/core/blob/main/CHANGELOG.md" label="Vue core CHANGELOG.md (the 3.5.46 entry)" >}}
- {{< source href="https://vuejs.org/api/sfc-css-features" label="Vue docs: SFC CSS features (v-bind() in CSS)" >}}
- {{< source href="https://vuejs.org/guide/scaling-up/ssr" label="Vue docs: Server-Side Rendering (Teleports in SSR)" >}}
- {{< source href="https://vuejs.org/guide/built-ins/teleport" label="Vue docs: Teleport" >}}
- {{< source href="https://vuejs.org/guide/built-ins/transition" label="Vue docs: Transition" >}}
