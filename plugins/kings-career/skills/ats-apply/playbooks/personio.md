# Personio

`<company>.jobs.personio.com/job/<id>` (posting) → `/job/<id>/apply` (form, on the page itself —
no iframe, no login, no resume autofill).

## Fields

- `input[name]` with id `field-<name>`. Standard: `first_name`, `last_name`, `email`, `phone`,
  `salary_expectations`, `available_from`. Company fields are `custom_attribute_<n>` (LinkedIn,
  GitHub…): map them by label or placeholder.
- **"Expected salary" and "Available from" are plain text inputs** even when they look like a
  number and a date (no picker): write the period and currency ("EUR 48,000 per year") and the
  availability in words.
- `form_input` by ref holds after blur. The phone accepts a foreign number as free text, though
  the placeholder shows the company's country format.

## Files

- `#doc-input-cv`, `#doc-input-other`, `#doc-input-cover-letter` (names `documents.cv`,
  `documents.other`, `documents.cover-letter`); `file_upload` works and each file shows as a chip
  with "×".
- After the upload the input's `.files` reads empty (the app moves the file into its own state):
  verify the file name in the form's text, not the input.

## Submit

- `button[type=submit]` "Submit Application" → "Application submitted! Thank you for applying to
  <company>." on the same URL, plus a confirmation e-mail.
- Some forms have no consent checkbox — only footer links to the privacy statement.
