---
title: "An AI-Written Form That Submits Is Not an Accessible Form"
date: 2026-11-05T06:00:00+07:00
draft: false
slug: "ai-written-form-that-submits-is-not-accessible"
description: "The agent's form saved the record, so the PR looked done. Here is the four-check review and the Playwright plus axe test I run on every AI-written Vue form before it ships, especially in the error state."
topics: ["frontend"]
tags: ["accessibility", "vue", "laravel", "playwright", "axe-core", "forms", "vibe-coding", "code-review"]
cover: /covers/ai-written-form-that-submits-is-not-accessible.png
seo:
  primaryQuery: "AI generated form accessibility"
  secondaryQueries:
    - "vue form accessibility checklist label aria-describedby"
    - "playwright axe test form error state"
    - "vibe coding accessibility review"
---

The pull request had a GIF. A coding agent built a profile settings form in Vue. You type an email, you click Save, the toast says "Saved." The record changed in the database. The reviewer approved it in four minutes.

Then I pressed Tab.

Focus jumped straight past the Save "button", because it was a `<div>` with a click handler. The email field had no label, only a grey placeholder that vanished the moment you typed. When I entered a bad email, a small red line appeared under the field. A screen reader said nothing. Nothing tied that red line to the input. The form worked for the person who recorded the GIF. It did not work for a keyboard user, a screen reader user, or the next developer who had to change it.

A form that submits is not an accessible form. The happy path is the part an agent demos best. The error path is the part your users actually live in.

<!--more-->

This is not a niche complaint. WebAIM scanned the top one million home pages again in February 2026. 95.9% had detectable WCAG 2 failures, up from 94.8% in 2025. That reversed six straight years of small improvements. Missing form labels showed up on 51% of those pages, and one third (33.1%) of all form inputs they found were not properly labeled. [Source: https://webaim.org/projects/million/]

WebAIM is careful about cause. Its report says these trends "likely reflect broader shifts in web development including increased reliance on 3rd party frameworks and libraries and automated or AI-assisted coding practices ('vibe coding')." [Source: https://webaim.org/projects/million/] I would not pin the whole number on AI either. But the pattern is familiar to anyone reviewing generated UI this year: the code renders, the request succeeds, and the semantics are missing. I wrote about the general version of this in [Code That Renders Is Not Code You Can Trust](/blog/code-that-renders-is-not-code-you-can-trust/). This post is the narrow, practical version for one component every SaaS has: the form.

The question is not whether the form demos well. The question is whether it still works when the user is wrong, the mouse is gone, and someone else maintains it next quarter.

![Same form, two users: works with a mouse, fails with a keyboard because focus skips the div button](/img/ai-written-form-that-submits-is-not-accessible-1.png)

## What the agent actually shipped

Here is a cleaned-up version of the form from that PR. If you have reviewed generated Vue code this year, you have seen this shape.

```vue
<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const errors = ref<Record<string, string>>({})

async function submit() {
  try {
    await axios.post('/settings/profile', { email: email.value })
    errors.value = {}
  } catch (e: any) {
    errors.value = { email: e.response?.data?.errors?.email?.[0] ?? 'Error' }
  }
}
</script>

<template>
  <div class="card">
    <input v-model="email" placeholder="Email" class="input" />
    <span v-if="errors.email" class="text-xs text-red-500">{{ errors.email }}</span>

    <div class="btn btn-primary" @click="submit">Save</div>
  </div>
</template>
```

Nothing here throws. Nothing fails a type check. The Laravel endpoint returns 422 with a proper `errors` object, and the component shows it. A unit test that clicks the div and checks the database would pass.

Now read it as a user who does not use a mouse:

- **There is no form.** There is a `div`. Pressing Enter in the field does nothing, because the browser's implicit submission only works inside a real `<form>`.
- **The button is not a button.** A `div` with `@click` is not in the tab order and has no button role. Keyboard users cannot reach it. Screen readers do not announce it as something you can press.
- **The placeholder is pretending to be a label.** Once you type, the hint disappears. There is no programmatic label, and that is exactly the "missing labels" failure WebAIM counts.
- **The error is a floating red line.** It is not linked to the input. The input does not say it is invalid. Focus stays wherever it was. A screen reader user hears silence after pressing Save.
- **Colour carries the meaning.** Extra-small red text on a white card is the kind of thing that ends up in the low contrast bucket, which WebAIM found on 83.9% of home pages in 2026.

None of these are exotic. They map to some of the oldest Level A and AA criteria in WCAG: 1.3.1 Info and Relationships, 2.1.1 Keyboard, 3.3.1 Error Identification, 3.3.2 Labels or Instructions, 4.1.2 Name, Role, Value, and 1.4.3 Contrast (Minimum). [Source: https://www.w3.org/WAI/WCAG22/quickref/]

{{< note type="warning" title="The happy-path demo hides all of this" >}}
Every problem above is invisible in a GIF recorded with a mouse and valid input. If your review is "watch the video, check the database row", you are reviewing the part of the form that rarely breaks.
{{< /note >}}

## Why generated forms fail in the same places

I do not think the models are lazy. I think they are trained on what the web looks like, and the web looks like the WebAIM numbers. The most common way to write a form on the public internet is the slightly broken way.

There are three habits I see over and over in agent output:

1. **Styled `div` instead of native element.** Design-system class names like `btn btn-primary` push the model toward "this is a button because it looks like one". The native `<button>` gives you focus, Enter and Space activation, and the button role for free.
2. **Placeholder as the only text.** Placeholders make screenshots look clean. Labels make forms usable. The agent optimises for the screenshot, because the prompt usually describes how it should look.
3. **Error text as decoration.** The agent renders the server error near the field. It does not wire it to the field, because "show the error under the input" is a visual instruction, not a semantic one.

There is a fourth habit that looks like a fix: **ARIA sprinkled on top.** You ask the agent to "make it accessible" and you get `role="button" tabindex="0" aria-label="Save"` on the same `div`, with no keyboard handler for Space or Enter. Now it is focusable but still cannot be activated by keyboard. WebAIM's 2026 data notes that pages with more ARIA had significantly more detected errors. They are careful to say this does not prove ARIA caused the errors, because those pages were also more complex. [Source: https://webaim.org/projects/million/] My review rule is simpler: if a native element does the job, ARIA on a `div` is a smell, not a fix.

![Four checks before approving a generated form: reach it, name it, error finds you, status is spoken](/img/ai-written-form-that-submits-is-not-accessible-2.png)

## The four checks I run before approving a generated form

I do not ask juniors to memorise WCAG. I ask them to do four things with the keyboard and the browser's accessibility panel. It takes about three minutes per form.

| Check | How to test it in 30 seconds | What failure looks like |
|---|---|---|
| 1. Can I reach it? | Tab from the address bar to Submit | Focus skips a field or the button |
| 2. Does it have a name? | Inspect each input in the DevTools Accessibility pane | Name is empty or comes only from the placeholder |
| 3. Does the error find me? | Submit bad input, press nothing else | Focus stays put, nothing is announced |
| 4. Does it say what changed? | Submit valid input with a screen reader on | Toast appears, nothing is read out |

Check 3 is the one generated code fails most in my reviews. It is also the one a happy-path demo never touches. So I start there.

The rule for check 3 is: after a failed submit, focus goes to the first invalid field, that field says it is invalid, and its error text is its description. When focus lands, a screen reader reads the label, the invalid state, and the message in one go. The user does not have to hunt.

The rule for check 4 is: one polite status region per form. "Saved" or "Could not save, try again" goes there. A toast that is just a styled `div` sliding in from the corner is check 4 failing. WCAG calls this 4.1.3 Status Messages, a Level AA criterion.

## The fixed component, line by line

Here is the same form after review. It is not longer because of accessibility theatre. Almost every added line is a native attribute.

```vue
<script setup lang="ts">
import { ref, nextTick } from 'vue'
import axios from 'axios'

const email = ref('')
const errors = ref<Record<string, string>>({})
const status = ref('')
const emailInput = ref<HTMLInputElement | null>(null)

async function submit() {
  errors.value = {}
  status.value = ''
  try {
    await axios.post('/settings/profile', { email: email.value })
    status.value = 'Profile saved.'
  } catch (e: any) {
    if (e.response?.status !== 422) {
      status.value = 'Could not save. Please try again.'
      return
    }
    const fieldErrors = e.response.data.errors as Record<string, string[]>
    errors.value = Object.fromEntries(
      Object.entries(fieldErrors).map(([field, messages]) => [field, messages[0]])
    )
    const count = Object.keys(errors.value).length
    status.value = `Please fix ${count} field${count === 1 ? '' : 's'}.`
    await nextTick()
    if (errors.value.email) {
      emailInput.value?.focus()
    }
  }
}
</script>

<template>
  <form novalidate @submit.prevent="submit">
    <div class="field">
      <label for="email">Email</label>
      <input
        id="email"
        ref="emailInput"
        v-model="email"
        type="email"
        autocomplete="email"
        :aria-invalid="errors.email ? 'true' : 'false'"
        :aria-describedby="errors.email ? 'email-error' : undefined"
      />
      <p v-if="errors.email" id="email-error" class="field-error">{{ errors.email }}</p>
    </div>

    <button type="submit" class="btn btn-primary">Save</button>

    <p role="status" class="sr-status">{{ status }}</p>
  </form>
</template>
```

What changed, and why each line matters:

- **`<form>` and `<button type="submit">`.** Enter now submits. Tab reaches the button. The button role is native. `@submit.prevent` keeps the SPA behaviour.
- **`novalidate`.** I let Laravel be the single source of truth for validation messages. Browser bubbles and server messages disagreeing is its own bug.
- **`<label for="email">`.** A visible, permanent name. Clicking the label focuses the field, which is a small win for touch users too.
- **`type="email"` and `autocomplete="email"`.** Mobile keyboards show `@`, and browsers can autofill. Autofill also helps with the spirit of 3.3.7 Redundant Entry, one of the 9 success criteria added in WCAG 2.2. [Source: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/]
- **`aria-invalid` and `aria-describedby`.** These are the only ARIA attributes in the component. They connect the native input to its error message. That is ARIA doing the one job HTML cannot do alone.
- **Focus after `nextTick()`.** The error paragraph must exist in the DOM before focus moves, or the description is empty when the screen reader reads it. This line is the one agents almost never write.
- **`role="status"`.** One polite live region for "saved" and "please fix". The status role already implies `aria-live="polite"`, so there is no need to add both.

For a form with many fields, replace the single `emailInput` ref with a lookup: find the first field name in `errors`, then `document.getElementById(name)?.focus()`. Keep the ID convention strict (`email` and `email-error`) so this stays boring.

{{< note type="success" title="Native first, ARIA second" >}}
The fixed component uses two ARIA attributes and one role. Everything else is plain HTML that has worked in every major browser for over a decade. If an agent's "accessible" version has more ARIA than this for a single field, read it twice.
{{< /note >}}

## Make the server side carry readable messages

The other half of check 3 lives in Laravel. If your validation messages are "The email field must be a valid email address", that is fine for a developer and vague for a user. When the error becomes the input's accessible description, the message is the instruction. Write it like one.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateProfileRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user() !== null;
    }

    public function rules(): array
    {
        return [
            'email' => ['required', 'email', 'max:255'],
        ];
    }

    public function messages(): array
    {
        return [
            'email.required' => 'Enter your email address.',
            'email.email' => 'Enter an email address like name@example.com.',
            'email.max' => 'Use an email address under 255 characters.',
        ];
    }
}
```

When the request expects JSON, Laravel answers a failed FormRequest with HTTP 422 and an `errors` object keyed by field name. [Source: https://laravel.com/docs/validation] That shape is exactly what the Vue component maps into `errors.value`. The field name in Laravel, the `id` on the input, and the key in `errors` should be the same string. Agents drift here. One file says `email`, another says `emailAddress`, and the focus code silently does nothing.

I make that naming rule part of the review, not a style preference. On a Laravel plus Vue codebase, the contract between FormRequest keys and input IDs is as real as a database column name. My notes on that stack live under [/laravel-vue-saas/](/laravel-vue-saas/).

![One field name across the stack: Laravel FormRequest key email, Vue input id email, error text id email-error](/img/ai-written-form-that-submits-is-not-accessible-3.png)

## Put the error path in a test, not in your memory

Review catches the form you are looking at today. A test catches the regression an agent introduces next month when it "refactors" the component. Playwright's accessibility guide uses `@axe-core/playwright` to run the axe engine inside a normal test. [Source: https://playwright.dev/docs/accessibility-testing]

The important detail from that guide: `analyze()` scans the page in its current state. If you scan right after `page.goto()`, you scan the empty form. The error message does not exist yet, so the broken error wiring is invisible. Interact first, then scan.

```ts
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('profile form', () => {
  test('works by keyboard and announces errors', async ({ page }) => {
    await page.goto('/settings/profile')

    // Check 2: the field has a real label, not just a placeholder
    const email = page.getByLabel('Email')
    await expect(email).toBeVisible()

    // Check 1: the submit control is a real button
    await expect(page.getByRole('button', { name: 'Save' })).toBeVisible()

    // Check 3: submit bad input with the keyboard only
    await email.fill('not-an-email')
    await email.press('Enter')

    await expect(email).toHaveAttribute('aria-invalid', 'true')
    await expect(email).toHaveAccessibleDescription(/name@example\.com/)
    await expect(email).toBeFocused()

    // Check 4: the status region says what happened
    await expect(page.getByRole('status')).toContainText('Please fix 1 field')

    // Scan the form in its error state, not its empty state
    const results = await new AxeBuilder({ page })
      .include('form')
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze()

    expect(results.violations.map((v) => `${v.id}: ${v.help}`)).toEqual([])
  })
})
```

A few notes so this runs on the first try:

- Set `baseURL` in `playwright.config.ts` so `page.goto('/settings/profile')` resolves, and log in through a setup project or saved storage state if the page is behind auth.
- The tags follow the Playwright guide's WCAG A and AA set, plus `wcag22aa`, which the axe-core API docs list as "WCAG 2.2 Level AA". [Source: https://github.com/dequelabs/axe-core/blob/develop/doc/API.md]
- I map violations to `id: help` strings instead of comparing the raw objects. When the test fails in CI, the junior sees a rule name and a one-line explanation instead of a wall of HTML snippets.
- On 5 November 2026, npm lists `@playwright/test` 1.64.1 and `@axe-core/playwright` 4.14.0 as latest. Pin whatever you install, and let your normal dependency review move them.

The `getByLabel`, `getByRole`, and `toHaveAccessibleDescription` assertions do as much work as axe here. They fail if the label, role, or error wiring is missing, in plain language, without any rule IDs. That is why I keep both. Axe catches the long tail. The explicit assertions document the contract.

## Teach the agent the contract once

You can fix forms one PR at a time, or you can write the contract down where the agent reads it. Most coding agents read a repository instruction file. Whatever yours is called, put form rules in it in short, checkable lines.

```markdown
## Forms (rules for any change to *.vue files)

- Every input has a visible <label for="id">. A placeholder is never the label.
- Submit is <button type="submit"> inside a <form>. Never a clickable <div> or <span>.
- Field IDs match the Laravel FormRequest keys exactly (email -> id="email").
- Error text uses id="<field>-error". The input gets aria-invalid and aria-describedby.
- After a failed submit, wait for nextTick, then focus the first invalid field.
- Each form has one role="status" element for saved / failed / please-fix messages.
- Do not add ARIA to a native element that already has the role you need.
- Every new or changed form ships with a Playwright test that submits bad input
  by keyboard and runs AxeBuilder in the error state.
```

This does not make the agent perfect. It makes the agent's mistakes reviewable. When the output breaks a rule, you can point at the line instead of arguing taste. That matters when the reviewer is a junior and the author is a model that sounds confident.

{{< field-note title="Field note" >}}
On the Laravel plus Vue SaaS projects I maintain, the forms that hurt were never the login page. They were the admin screens nobody demos: supplier edit, invoice correction, user role changes. Those get generated fast and reviewed fast, because "it is only internal". Then a staff member who navigates by keyboard, or who zooms to 200%, files a ticket that the Save button "does nothing". The fix is never hard. The cost is that by then three other screens copied the same broken component. My rule now: the first generated form in a module gets the full four-check review and a Playwright test, and every later form in that module reuses that component instead of getting a fresh one from the agent. One reviewed pattern beats ten fast ones.
{{< /field-note >}}

## What automation will not catch

I want to be honest about the ceiling. Playwright's own guide says automated accessibility tests detect some common problems, but many problems can only be discovered through manual testing, and it recommends combining automated tests, manual assessments, and inclusive user testing. [Source: https://playwright.dev/docs/accessibility-testing]

Things the test above will not tell you:

- **Whether the error message makes sense.** Axe checks that a description exists. It does not check that "Invalid input" is useless.
- **Whether focus order matches visual order** in a complex two-column layout.
- **Whether a custom date picker or combobox** generated by the agent is actually operable. For those, I prefer a well-tested component library over agent-written widgets, every time.
- **Whether the form still works at 200% zoom** on a small laptop, where a sticky footer can cover the focused field. WCAG 2.2 added 2.4.11 Focus Not Obscured (Minimum) for exactly that kind of problem.

So the test is a floor, not a certificate. Once a release, someone on the team should tab through the main forms with a screen reader on. NVDA on Windows and VoiceOver on macOS are both free. Ten minutes is enough to find the thing your test did not think of.

If you like this style of "prove the boring path" review, the same thinking runs through [The JavaScript I Deleted With CSS](/blog/the-javascript-i-deleted-with-css-a-2026-survival-guide/), where native browser features replaced code an agent would happily have written. More tooling notes live under [/developer-tools/](/developer-tools/), and if you are new here, [/start-here/](/start-here/) is the map.

## What you should do Monday morning

1. **Pick your three most-used forms.** Login does not count. Choose the ones staff or customers fill in every day.
2. **Run the four checks by hand.** Tab to Submit, inspect each input's accessible name, submit bad input, submit good input with a screen reader on. Write down every failure.
3. **Fix the error path first.** Native `<form>` and `<button>`, real labels, `aria-invalid` plus `aria-describedby`, focus the first invalid field after `nextTick()`, one `role="status"`.
4. **Align names across the stack.** Make FormRequest keys, input IDs, and error keys the same string. Rewrite validation messages as instructions.
5. **Add one Playwright test per form** that submits bad input by keyboard and runs `AxeBuilder` with WCAG A and AA tags in the error state. Make it block the merge.
6. **Write the form rules into your agent instruction file.** Eight short lines. Point to them in every review comment instead of re-explaining.
7. **Book ten minutes of screen reader testing** into your release checklist. The automated test is the floor. A human is the ceiling.

## Further reading

{{< source href="https://webaim.org/projects/million/" label="WebAIM — The WebAIM Million: 2026 report on the accessibility of the top 1,000,000 home pages" >}}

{{< source href="https://playwright.dev/docs/accessibility-testing" label="Playwright — Accessibility testing with @axe-core/playwright" >}}

{{< source href="https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/" label="W3C WAI — What's New in WCAG 2.2" >}}
