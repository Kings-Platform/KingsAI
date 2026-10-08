# Lever

`jobs.lever.co/<company>/<id>/apply`. Plain HTML, no React: the easiest platform.

- **Fill by JS:** `el.value = …` plus `input`/`change` events works; radios with
  `radio.click()`. Stable `name`s: `name`, `email`, `phone`, `location`, `org`,
  `urls[LinkedIn]`, `urls[GitHub]`, `opportunityLocationId` (select), and the company's
  questions as `cards[<uuid>][fieldN]`.
- **Radio by text:** match the value exactly (`value.trim() === 'Advanced'`), not by prefix —
  options often share a prefix.
- **Resume:** `file_upload` on the input behind "ATTACH RESUME/CV". Lever parses it
  ("Analyzing resume…" → "Success!") and may fill fields on its own — re-read them.
- **Cookie banner** covers the submit button: the first "Submit application" does nothing.
  Click "Deny" and submit again.
- **Confirmation:** URL `/thanks`, "Application submitted!".
- The sentence "File exceeds the maximum upload size…" is a hidden template always present in
  the DOM — not an error.
- Scanning without a browser: `api.lever.co/v0/postings/<company>?mode=json`.
