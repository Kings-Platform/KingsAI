# LinkedIn Easy Apply

`linkedin.com/jobs/view/<id>/` with the "Candidatura simplificada" / "Easy Apply" button. A modal,
not a page; some employers feed it from their ATS (`applicantTrackingSystemName=Lever` in the URL,
"Candidatura alimentada por Lever"), which brings all their custom questions in, one group per page.

## Opening and finding the modal

- **Before anything**, read the job page for "Candidatura enviada" under "Status da candidatura"
  (already applied) or "Não aceita mais candidaturas" / "Não aceita candidaturas agora" (closed — match "Não aceita" + "candidaturas"). Either one: stop and report.

- A ref click on "Candidatura simplificada" sometimes doesn't open it; a **coordinate click** does.
- `[role=dialog]` and `.jobs-easy-apply-modal` don't match (hashed classes). Find the root by
  walking up from the text "Candidate-se à empresa" to the first ancestor holding a button
  "Avançar" / "Revisar" / "Avaliar" / "Enviar candidatura". **Re-find it on every page**: a root
  stashed before "Avançar" goes stale, and setters on detached nodes "succeed" silently.
- Page counter: "N de M páginas". The button on the last questions page is often "Avaliar".

## Fields

- Text inputs and native `<select>`: native value setter + `input`/`change`/`blur`; options by
  text `startsWith` (option texts are long). Clicking "Avançar" from JS works.
- Labels are often empty (`label[for]` with no text): the question is in the input's `aria-label`.
- **Numeric fields take digits only** (years, salary without a currency label). "Valor inválido"
  appears only after "Avançar". A salary field with no currency from a local employer is a
  currency decision: answers.md → Compensation, not a guess.
- Radios: `find` + real click by ref. `input.value` is "on" and `closest('div')` reads the wrong
  text — confirm answers from the review-page text or a screenshot. LinkedIn **pre-fills radios**
  from earlier applications: always read the checked state.
- Checkboxes need a real click; labels may show raw HTML entities from the ATS config.

## Contact page

- LinkedIn pre-fills the phone from the member profile, which may not be the number the profile's
  facts allow in forms. Always read the phone and overwrite it with the application number.
- Some forms are a **single page**: contact, resume and "Enviar candidatura" with no "Avançar" or
  review step — the "Siga a empresa" checkbox is on that page.

## Resume

- No `input[type=file]` until "Carregar currículo", which opens the system picker (not usable).
  Saved CVs are radios with name and date; the newest is pre-selected. Pick the language by
  clicking the radio; check which is selected by walking up from `input:checked` to the ancestor
  whose text contains "pdf". A new file has to be uploaded once by hand.

## Before submit

- Skip "Marcar vaga como preferencial" (monthly quota).
- "Siga a empresa …" on the review page is ticked by default when present: untick it with a click
  at the label's left edge (+8 px) after `scrollIntoView` and a 1 s wait; it survives "Editar".
- Optional diversity questions: blank. Lever data-consent selects: the recruitment consent only,
  never the marketing one.
- Confirmation: "Candidatura enviada" under "Status da candidatura" on the job page.

## Tooling traps

- JS results truncate around 1,000 characters and are blocked when they contain `?`, `=`, `&` or
  `#`: stash text in `window.__k` and read it in slices; reduce the 250-option country select to a
  count.
