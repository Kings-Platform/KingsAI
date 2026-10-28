# Cornerstone (CSOD)

`<tenant>.csod.com/ux/ats/careersite/<site>/home/requisition/<id>?c=<tenant>` (posting) →
"Candidatar-se" / "Apply" → a **guest wizard** of several steps (6 on the tenant tested,
28/10/2026). No account, no CAPTCHA. The URL hash is the step (`#1`…`#6`; the next number after the
last step means submitted). Creating a profile with a password is optional and the user's.

**The session expires when idle.** A step that waits on the user (document numbers, questions the
profile can't answer) can lose everything typed so far: ask for those answers up front, and keep
each step moving.

## Step 1 — contact, CV, experience, education

- Upload the CV with `file_upload` on `#resumeFileUpload`. A parser then pre-fills contact data and
  creates experience and education rows — and gets them wrong in a predictable way: it **drops
  jobs**, invents a row from the CV's summary, guesses months (January), turns non-degree programs
  into education, and leaves wrapping junk in the descriptions and the course name. Rewrite **every**
  row from the facts; delete extra rows with "Excluir …" / "Delete …" (no confirmation).
- Target fields by their id suffix — experience `[id$="_0_<row>_<field>"]`, education
  `_1_<row>_<field>` (fields: 0 company, 1 title, 2 employment-type select, 3 start, 4 end,
  5 description, max 8000) — **never by position**: the file input disappears after the upload and
  every index shifts.
- Native setter + `input`/`change`/`blur` sticks on text, date and textarea; native `<select>` with
  `.value` + `change` sticks. Dates: D/M/YYYY for jobs, MM/YYYY for graduation.
- Brazilian tenants ask the **full surname**, the **employment type per job** (CLT / PJ / estágio /
  outros…) and the **course period** (matutino…): resolve them from the answer bank before starting.
- The data-processing consent (`[id^=user-agreement]`) needs a real click.

## Later steps

- Radios are invisible to `read_page`; `input.labels[0]` holds the option text and a JS
  `r.click()` registers.
- Typical Brazilian bank tenant: document numbers and birth date (the user's), diversity,
  education, marital status, politically exposed person, salary expectation and last salary,
  non-compete, equity in a company, former employee, anti-money-laundering declaration, LinkedIn URL,
  how you heard about the role, and an opt-in to be considered for other roles.
- No cover-letter field on the tenant tested.

## Reading the board without a browser

The careers page carries a guest JWT (`"token":"…"`, about 2 h) and the API host (`"cloud"`, e.g.
`https://us.api.csod.com/`). Then:

```
POST <cloud>rec-job-search/external/jobs
Authorization: Bearer <token>
{"careerSiteId":<site>,"careerSitePageId":<site>,"pageNumber":1,"pageSize":100,
 "cultureId":<cultureID from the page>,"searchText":"<query>","cultureName":"<cultureName>",
 "states":[],"countryCodes":[],"cities":[],"placeID":"","radius":null,"postingsWithinDays":null,
 "customFieldCheckboxKeys":[],"customFieldDropdowns":[],"customFieldRadios":[]}
```

→ `data.totalCount`, `data.requisitions[]` (`requisitionId`, `displayJobTitle`, `locations[].city`,
`postingEffectiveDate`). `searchText` matches the whole text, not only the title. Fetch a fresh
token on every run.
