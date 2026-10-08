# SAP SuccessFactors

`career<n>.successfactors.eu` / `.com`. Account required (user). The candidate profile is
shared across the company's postings; applications pick it up.

- Profile sections are collapsed: "Expand all sections". "Save" is at the bottom of the page.
- **Upload:** "Upload resume" / "Attach letter" opens a "Select upload source" dialog; the
  `input type=file` is inside it (`find "file input in dialog"`) and `file_upload` works.
- **The CV upload parses and creates experience rows on its own, all wrong** (city as company,
  projects as employers, the current employer swapped). Delete the extras ("Delete row", no
  confirmation) and fix the remaining ones.
- **Texts:** native setter + `input`/`change` persists (ids like `NNN:_txtFld`).
- **Dates** aren't inputs reachable by label: real click, `type` `DD/MM/YYYY`, then click a
  blank area to confirm. **Tab jumps the page to the top** (focus lands on "Log off").
- **Combobox** (`NNN:_input role=combobox`): the first click only focuses. Open with a second
  click on the arrow or `alt+ArrowDown` (sometimes twice), click the option. In long lists,
  type part of the text **then** `alt+ArrowDown` to filter. Typing too little and clicking by
  position picked the wrong entry — verify.
- "Current employer = yes" disables the end date.
- **Final check:** list every value by JS (label via `label[for=id]`) before Save.
