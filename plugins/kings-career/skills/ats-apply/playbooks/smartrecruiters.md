# SmartRecruiters

`jobs.smartrecruiters.com/<company>/<id>`. Custom elements with **shadow DOM**: querying
`document` misses the fields; `find` / `read_page` see them.

- "Apply with LinkedIn" (user's login) prefills name, experiences and the CV. Then fix: an
  agency name imported from LinkedIn that the facts page says to replace, the current job's end
  date, job titles with extra separators.
- Fields work with a **real click and keyboard type** by ref.
- **Experience title** is an autocomplete: type, then click the suggestion, or the value is
  dropped.
- The free "message / cover letter" field **rejects `;`** — rewrite the sentence.
- CV: when the LinkedIn import brought it, it's attached; otherwise `file_upload` on the file
  input.
- Custom radios never report checked: verify on screen.
- Submit button at the end; confirmation page in the same tab.

## "oneclick-ui" variant

Every input lives in shadow DOM.

- **Resume:** add a light-DOM proxy `<input type=file>`, `file_upload` into it, then copy the
  file to the shadow input with a `DataTransfer` and dispatch `change` with `composed: true`.
- `#spl-dropzone-file-input-2` is the parse dropzone: avoid it.
