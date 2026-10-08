# Zoho Recruit

`<company>.zohorecruit.com/jobs/Careers/<id>/…`.

- Decline non-essential cookies first; the form appears after **"I'm interested"**.
- Two steps: **Application**, then **Assessment** (the company's questions). Step 1 has an
  **image CAPTCHA** ("Type below image text") — the user's.
- Fields: first/last name, email, mobile (country code preset), address (City autocomplete
  fills postal code and state), LinkedIn (required), Resume and Cover Letter **as files**.
  `form_input` for texts, `file_upload` for both files. A cover letter in Markdown can be
  converted with `textutil -convert docx` when the field wants a document.
- **Skill set:** a tag field. Type, wait for the suggestions (`li` under "Relevant skills"),
  click the suggestion with a **real click** — Enter adds the first suggestion, not necessarily
  the typed one. Level radios (`name=skillTags`: Master / Intermediate / Beginner): read the
  state first; clicking an already-selected radio clears it and the tag turns red (no level).
  A level can't be changed later: remove the tag and add it again.
- **Education and experience:** "Add" / "Add More" blocks with Title, Company, Summary
  (`form_input`), and dates in custom lists (not `<select>`): click the field, type to filter
  ("Feb", "2023"), **click the option** (Enter doesn't select). "I currently work here"
  disables the end date.
- Confirmation: "Success!".
