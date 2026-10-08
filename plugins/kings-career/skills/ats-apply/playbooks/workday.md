# Workday

`<company>.wd<n>.myworkdayjobs.com`. Account required: the **user signs in** (email + password,
or "Sign in with Google"); the agent takes over at the first form step.

## Steps

Autofill with Resume → My Information → My Experience → Application Questions → Voluntary
Disclosures → Self Identify → Review → Submit. "Save and Continue" between steps; errors are
listed at the top of the step.

## Techniques

- **Text and dates:** focus the input by JS (`focus()` + `select()`), then **real keyboard**
  `type`. Dates: focus the month segment and type `MMYYYY` (or `MMDDYYYY`) in one go — the
  cursor advances by itself.
- **Dropdowns** (`button[aria-haspopup=listbox]`): click the button, then click the
  `[role=option]` by text — works by JS. Read the options first (open, list, close).
- **Searchable lists** (phone country, field of study): typing filters; **Enter selects the
  highlighted item, which may be wrong** (a different country). Scroll the list and click the
  exact entry, or find it by text with `find`.
- **Checkboxes** (e.g. the disability form CC-305): JS `click()` doesn't register; real click.

## Autofill traps

"Autofill with Resume" fills My Information and My Experience from the PDF and gets it wrong:
titles and companies swapped, education and projects turned into experiences, the phone number
in the postal code. Map every `workExperience-N--jobTitle/companyName/location/startDate/endDate`,
fix each from the facts page, delete the extras with the row's "Delete" (last row first).
Check My Information (postal code, phone country) before saving.

## Questions

Typical: non-compete, authorized to work in <country>, sponsorship needed, former employee,
open to relocation. All from the answer bank. Voluntary disclosures and self-identification
(gender, ethnicity, veteran, disability) also from the bank — the user's choice to decline is
an answer, not a gap. The self-ID form asks for name and today's date.

## Confirm

"Application Submitted" dialog; the application appears under My Applications; email follows.
