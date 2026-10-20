# iCIMS

`<careers-site>.icims.com/jobs/<id>/…`. **No guest apply:** step 1 creates a profile with login and
password behind an hCaptcha, so the form starts as `pending: login` for the user.

- The form lives in a **same-origin iframe**: query its `contentDocument`, not the page. The
  accessibility tree (`read_page`, `find`, `file_upload`) stops at "iCIMS Content iFrame" and
  can't reach the controls inside.
- Stable field names: `PersonProfileFields.*` for the profile and `rcfNNNN` for the company's
  questions.
- An SMS opt-in comes as a select: answer it from the profile's rules.
- `from=login` in the URL doesn't mean the user is logged in; check the page. A
  `mode=prepopulate&social=1` page (profile filled from a connected account under "Create a
  login") isn't a login either, and the hCaptcha still guards the submit: the click is the user's.
- Multi-step: diversity questions often come as a separate step that only appears after
  "Submit Profile".

## Uploading files

`file_upload` can't target an input inside the iframe. What works: add a temporary
`<input type=file>` to the top document, run `file_upload` on it, then in the iframe's realm build a
`DataTransfer`, assign `iframeInput.files = dt.files`, dispatch `input` and `change`, and remove the
temporary input. The file must be in a directory shared with the session; otherwise the upload is
rejected and the attachment stays with the user.

## Resume parser — upload first, then fix everything

Attaching the resume reloads the form (`uploadResume=1`), and the parser replaces existing data.
Upload it first, then re-read every field. Seen so far:

- Employer filled with the work mode ("On-site", "Hybrid") instead of the company.
- The current job gets this month as its end date.
- Descriptions replaced by the parser's own rewrites.
- Extra rows (an old internship), and rows in the wrong order.
- The address City overwritten.

Experience rows are removed with the anchor `#rcf3211Button2_<rowId>` (it runs `hideGroup`); the
first row has no remove anchor.

## Field mechanics

- Text inputs, textareas and the native Month/Day selects take a native value setter plus `input`,
  `change` and `blur`. Year is a text input. The blank Month/Day option has value `"0"`: clear it
  with `selectedIndex = 0`.
- Selects with a `<name>_icimsDropdown` combobox (pronouns, state, school, country, Yes/No
  questions) load their options lazily and need real clicks: `scrollIntoView`, add the iframe's
  rect to the element's rect to get screen coordinates, click. Long lists have a search box (type,
  wait ~2 s, Down, Return); search without accents fails ("Paulo" works, "Sao Paulo" doesn't).
  Short lists have no search box: click the option itself — typing leaks into the last focused
  dropdown, and a select filled earlier can silently change. Read every dropdown back at the end.
- Required status sits in `aria-required` on the combobox anchor, not on the `<select>`.
- Degree lists may offer a single bachelor option ("Bachelors").
