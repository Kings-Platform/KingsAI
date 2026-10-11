# Google Forms

`docs.google.com/forms/d/e/<id>/viewform` (often behind `forms.gle` or a `bit.ly` preview page —
navigate straight to the destination it shows). Single page or a few sections.

**Check first:** a form with a file field forces a Google sign-in, and the response (plus the
uploaded file) is tied to whichever Google account the browser is signed into — which may not be
the application email. Report the account before filling; switching accounts is the user's.

## Fields

- Each question is a `[role=listitem]` with a `[role=heading]` title.
- Text: `input[type=text]` / `textarea` with the native value setter + `input`/`change`/`blur`.
- Radios: `[role=radio]` with `data-value` = option text; JS `.click()` works. "Outro"/"Other" is
  `data-value="__other_option__"` and enables its own text input.
- "Collect email" checkbox records the signed-in account's address — user decision when it differs
  from the application email.

## Files

- Upload is a Google Drive picker in a cross-origin iframe; `file_upload` can't reach it and
  "Procurar" opens the native file dialog. Always the user's.

## Submit

- "Enviar"/"Submit" at the bottom. The user may want "send me a copy" off.
