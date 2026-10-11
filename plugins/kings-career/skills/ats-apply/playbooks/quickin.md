# Quickin

`jobs.quickin.io/<tenant>/jobs/<id>` (posting) → "Apply" → `/<tenant>/apply?job_id=…` (form).
Single public page, no account ("Login" / "Rescue profile" in the header are optional), no
CAPTCHA seen. Final button: "Finish".

## Fields

- Text inputs (`#name`, `#salary`, `#email`, `#input-questio-job_question_<id>`): native value
  setter + `input`/`change`/`blur`.
- `#salary` has a currency mask: type the plain amount; it shows as "$20,000.00" whatever the
  currency. The amount is what counts.
- Radios — screening `radio-yes-questio-job_question_<id>` / `radio-no-questio-job_question_<id>`,
  gender (`#male`…), diversity `diversity-<race|sexual_orientation|gender_identity>-option-<n>`:
  JS `el.click()` registers them. To read a screening question's text, walk up from the radio to
  the first ancestor whose `innerText` is longer than the "Yes No" labels.
- Diversity labels carry long definitions after a colon: strip them when reading.
- Only `consent` is marked required in the HTML; the other asterisks are checked by JS at submit.

## Phone

No `name`. The country is a flag button defaulting to "+1": real click → click the "Buscar
código" search input (it doesn't take focus by itself) → type the country → click its row
("Brasil - BR (+55)"). Then real-click the number input, type the digits, Tab. The search box
keeps its text; harmless, but it shows up in a read-back of all text inputs. Filter the country
list out of `find` results — it inflates the output.

## Files

- Resume: `file_upload` on `#validatedCustomFile` (PDF/DOC, 5 MB max). After the upload the input
  is replaced by a filename label: verify from the page text after "Resume (file)", not with
  `input[type=file]`.
- Photo (`photo`): optional. No cover-letter field.

## Before submit

- `#consent` (privacy notice): real click. Screenshot coordinates differ from CSS pixels
  (scale the `getBoundingClientRect` values by screenshot width / viewport width) — a click at
  raw CSS coordinates misses.
