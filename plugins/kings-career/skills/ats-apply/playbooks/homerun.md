# Homerun

`<company>.homerun.co/<slug>/<lang>` (posting) and `…/apply` (form). No account, no CAPTCHA seen. A
cookie banner (Decline / Accept) shows on the posting: **Decline** by a plain click.

## Flow

Four steps, one URL each (`?&step=N`): **1** personal information and the resume, **2** the
company's questions, **3** a preview that lists every value and answer, **4** "Submit your
application" at the bottom of the preview. "Next: Questions" and "Next: Preview" validate and advance;
one read of the preview's page text verifies the whole application. A tenant may add a consent
checkbox on the preview or EEO questions; the one seen had neither, and no cover-letter field.

## Fields

- Inputs have stable ids: `first_name`, `last_name`, `email`, `city`, `country`, `phone_number`,
  `linkedin`; the optional photo is `photo_file`. City and country are **free text** (no select), the
  phone a plain `tel` input with no country picker.
- Required fields carry only a `*` in the label — the `required` attribute is not set. Hidden honeypot
  inputs (`homerun_required*`, `valid_from`) are to be left alone.
- The native value setter plus `input` / `change` / `blur` works on text inputs **and textareas**
  (`HTMLTextAreaElement.prototype`). Custom questions are textareas named `questions[<id>]`.
- Resume: `input#resume_files`; `find` returns it as a button ref and `file_upload` on that ref works
  (a 150 KB PDF). The page shows the file name with a spinner, then a chevron once attached.

## Questions

Postings are often tailored with **three free-text technical questions** (architecture designed,
a performance issue solved, a modernization led) that are never in the answer bank. Write them from
the profile's stories **before** the agent opens the form, get them approved, and keep the approved
text in the answer bank for the next form of the same kind. A question with no approved answer stays
empty and goes to the user as pending.

## Submit

The final click is the user's: the browser tool's permission check blocks submitting an application
on the user's behalf, and the playbook never works around it. Leave the tab on the preview, with
everything read back, and report.
