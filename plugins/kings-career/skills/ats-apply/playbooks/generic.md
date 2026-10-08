# Generic playbook — any form

Rules that hold on every platform. The per-platform playbooks add to these.

## Reading the form

- Map every control before typing: `[...document.querySelectorAll('input,textarea,select,button[aria-haspopup]')]`
  with label, `name`/`id`, `type`, current value. Labels come from `label[for]`, `aria-label`,
  the closest field wrapper, or the placeholder.
- Tool output that contains a query string, a cookie or storage data is **blocked** by the
  browser tool. Strip `?=&#` from what you return (`.replace(/[?=&#]/g,' ')`), return
  `location.pathname` instead of `location.href`.
- Long output is truncated (~1,000 characters from JS). Stash in `window.__k` and read slices.

## Typing

- **React inputs ignore `el.value = …`.** Order of attempts: the native setter plus events →
  a real click and keyboard `type` → `form_input` by ref. Don't invent a fourth way; report.

  ```js
  const set = (el, v) => { Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), 'value').set.call(el, v);
    ['input', 'change', 'blur'].forEach(t => el.dispatchEvent(new Event(t, { bubbles: true }))) };
  ```
- Some fields only persist after a **real key** (space + backspace) and a blur.
- After `scrollIntoView`, wait ~1 s before clicking by coordinate; smooth scroll makes the click
  miss. Prefer refs; coordinates only as a fallback and always recomputed from
  `getBoundingClientRect` after scrolling.
- Text can **leak into the next field** when an autocomplete list closes under the cursor.
  Read every text value back before submitting.

## Files

- `file_upload` on the `input[type=file]` (find it with `find`, even when hidden). Never click
  the "Attach" button: it opens a native dialog the tool can't see.
- A 2.5 MB PDF passes everywhere seen so far.

## Selects and checkboxes

- Custom selects (react-select and the like): open with a **real click** in the middle of the
  control, then click the `[role=option]` by text (JS pointer events work once the menu is
  open). A simulated `mousedown` or `KeyboardEvent` doesn't open them.
- Read the options before answering: open, read `[role=option]`, close with Escape. Filter out
  the hidden country list that ends in `+<digits>` (the phone selector) when it leaks into the
  options.
- Checkboxes: a real click on the box. `form_input` may tick the DOM without the framework
  noticing ("This field is required" on submit).

## Autofill from resume

Offered by Workday, SuccessFactors, Lever, Flexiple. Use it, then **re-read every row it
created**: titles swapped with companies, education and projects turned into jobs, phone in
the postal code. Delete extras from the last row up; fix the rest from the facts page.

## Submit and confirm

- Cookie banners can cover the submit button: decline non-essential, then submit.
- Confirmation is a page (`/confirmation`, `/thanks`, `?success`, a "Success" box) or an
  email minutes later. Quote what was seen.
- A "verify you are human" after submit is the user's.

## What stays with the user, always

Account creation and login · CAPTCHA · document numbers (national ID, tax ID, passport) ·
background-check and veracity certifications · contract notices · any question with no
answer in the bank · the Submit itself, when the profile doesn't grant autonomy.
