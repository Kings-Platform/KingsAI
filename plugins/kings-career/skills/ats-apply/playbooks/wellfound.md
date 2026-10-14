# Wellfound

URL shape: `https://wellfound.com/jobs/<id>-<slug>`. Requires the user's logged-in session;
the CV comes from the Wellfound profile (no file field). Never edit the profile.

## Before applying

The job page's left panel shows "Hires remotely in", Visa sponsorship and Relocation. A warning
icon next to Location ("This job requires you to relocate") or Visa sponsorship predicts a hard
block (below).

## Apply modal

- Click **Apply** and wait ~3 s for the modal to finish loading (it's greyed out until then).
- Query the whole document for `textarea` — `[role=dialog]` can come back empty.
- One free-text box per posting:
  - a recruiter question: `textarea[name="customQuestionAnswers[<id>][answer]"]`, or
  - the generic note: `textarea[name=userNote]`, placeholder "Write a note to <Company>."
  Both are new free text → show the draft to the user before sending.
- Native value setter + `input`/`change`/`blur` enables **Send application**.
- Navigating away from a filled modal loses the text with no warning.

## Hard block

"<Company> does not offer visa sponsorship and requires all remote workers to be in-country.
Your profile indicates you require sponsorship." — the textarea and Send are disabled. Return
`BLOCKED` with the message; changing the profile's sponsorship answer is not an option.

## Confirmation

Same modal: "SUCCESS! YOUR APPLICATION HAS BEEN SENT." (URL unchanged), followed by an
AI-interview upsell — ignore it.
