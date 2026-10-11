# Ashby

`jobs.ashbyhq.com/<company>/<id>` (posting) and `/application` (form). React.

- **Focus first:** in a new tab, typing registers nothing until the tab has real focus. Click
  one visible field by screen coordinates, check `document.hasFocus()` and one value, then go.
- **Text fields:** JS `focus()` + keyboard `type` does **not** register — the values read back
  empty. What works: a **real click on the field by ref** (`find` → ref), then `type`. Verify
  with one JS read of all `input[type=text]` values at the end.
- Fields: `_systemfield_name`, `_systemfield_email`, `_systemfield_resume` (file), `phone`,
  `cover_letter` (file), and the company's questions as `question_<n>` or a UUID `name`.
- **Location** is an autocomplete with no `name` (`input[placeholder="Start typing..."]`): type
  the city, wait ~2 s, click the first option.
- **Date fields** are a calendar popover ("Pick date..."): header in the browser locale, → to
  change month, click the day; reads back as MM/DD/YYYY.
- **Radio questions** (relocation, visa, language, privacy consent) can be real
  `input[type=radio]` named `<uuid>_<suffix>`: click by ref, check `input[type=radio]:checked`.
- **Yes/No questions** may also be two `button`s; find them by text with the question as context
  (`find "Yes button for <question>"`) and click by ref. The underlying checkbox reports the
  state: read `input[type=checkbox]` values to confirm.
- **Files:** the CV folder must be shared with the session, or the upload is refused
  ("only files this session is allowed to read"). `file_upload` on the "Resume" / "Cover Letter" file inputs (found by `find`). Both
  names appear in the page text once uploaded.
- "Autofill from resume" exists; not needed — the fields are few.
- **Submit:** "Submit Application" → a green "Success" box with the company's text. A
  confirmation email follows.
- Some companies allow **one application per year**; the posting says so. Check the pipeline.
- Scanning without a browser: `api.ashbyhq.com/posting-api/job-board/<company>?includeCompensation=true`
  (includes the salary range).
