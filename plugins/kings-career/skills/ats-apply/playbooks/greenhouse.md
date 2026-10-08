# Greenhouse

## Where the form is

- Board: `job-boards.greenhouse.io/<company>`; posting: `/<company>/jobs/<id>`; the form is on
  the posting page.
- A company careers site that embeds Greenhouse (`careers.<company>.com/?gh_jid=<id>`) loads
  an iframe `job-boards.greenhouse.io/embed/job_app`. The browser tool may not run JS on the
  company's domain; open the board URL or the embed directly:
  `boards.greenhouse.io/embed/job_app?for=<company>&token=<id>`.
- **"Already applied?"** `my.greenhouse.io/applications` lists the user's applications when
  they're logged in to MyGreenhouse. Some boards autofill from it ("Autofilled from
  MyGreenhouse") — check nothing was overwritten.
- Public API for scanning without a browser: `boards-api.greenhouse.io/v1/boards/<company>/jobs`.

## Fields

- Ids: `first_name`, `last_name`, `preferred_name`, `email`, `phone`, `candidate-location`,
  and `question_<n>` for the company's questions.
- **Text and textarea: `form_input` by ref** — reliable. Click + `type` on a ref sometimes
  doesn't enter the text.
- Some fields that look like text are react-selects (`form_input` returns empty): treat them as
  selects.

## Selects (react-select)

- Open with a **real click in the middle** of the control (not its left edge); a click by ref
  failed on some boards. Then click the option by JS:

  ```js
  const o = [...document.querySelectorAll('[role=option]')]
    .filter(o => !/\+\d+$/.test(o.innerText.trim()))        // hides the phone-country list
    .find(o => o.innerText.trim().startsWith(TEXT));
  ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click']
    .forEach(e => o.dispatchEvent(new MouseEvent(e, { bubbles: true })));
  ```
  Closes the menu and persists; reliable across many selects in a row.
- Scroll each select to ~300 px from the top (`window.scrollTo({top: scrollY + rect.top - 300,
  behavior: 'instant'})`), compute all coordinates after scrolling, then click. Near the end of
  the page the page can't scroll further and heights vary.
- **Phone country** (combobox next to the phone field) is required even without an asterisk:
  click, type the country, Enter.
- **Location** (`candidate-location`): Google autocomplete — type, wait, click the suggestion.
  The list can open off-screen if the page scrolled; the least stable step. Verify the value.

## Files

`file_upload` on the input behind "Attach" (resume; cover letter where there's a field).

## Checkboxes

Required consent checkboxes: real click. If it already shows ticked but the form says required,
click twice (untick, tick).

## Submit

"Submit application" → `/jobs/<id>/confirmation`. The invisible reCAPTCHA hasn't blocked.
Fields that stay with the user: veracity certification, background-check consent, "business
entity", contract notices.

## Known blocker

The browser extension may deny `job-boards.greenhouse.io` ("Permission denied for reading /
JavaScript on this domain"). Nothing to work around: the user allows the site in the
extension, or fills the form themselves.
