# Comeet (Spark Hire Recruit)

`www.comeet.com/jobs/<company>/<companyUID>/<slug>/<positionUID>` (posting). The form is **not**
in that page's DOM: it's an iframe `iframe[src*="/apply"]` pointing to
`www.comeet.co/jobs/<companyUID>/<positionUID>/apply?token=…&embedded=true…`. No account.

- **Reach the form:** on the comeet.com page, open the iframe's `src` as a top-level page
  (`location.href = document.querySelector('iframe[src*="/apply"]').src`). Its title reads
  "Spark Hire Recruit Jobs".
- On `www.comeet.co` the browser tool may **deny JavaScript**: use `read_page` (filter
  `interactive`) for refs, `form_input` by ref for text, `find` + `file_upload` for the file
  buttons ("Attach Resume / Cover Letter / Portfolio"); the filename shows next to the field.
- Usual fields: first and last name, e-mail, phone (a mask strips spaces; keep the country code),
  resume (required), personal website, cover letter, portfolio, personal note. Company questions
  may follow.
- The position also has an apply-by-e-mail address (`<company>.<positionUID>@comeetapply.com`):
  use the form.
- **Submit:** "Submit application" → "Submitting…" → "Thank you <name>! Your application has been
  submitted." in the same frame.
