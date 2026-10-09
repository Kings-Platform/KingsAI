# Keka

`<tenant>.keka.com/careers/jobdetails/<id>` (posting) → "Apply for this job" →
`/careers/applyjob/<id>` (form). No account or login.

**It can't be fully autonomous:** every submit has an image CAPTCHA, so the form always ends
with the user (CAPTCHA, consent checkbox, "Apply Now").

## Fields

- Text: native value setter + `input`/`change`/`blur`. Native `<select>`: value + `change`.
  No custom dropdowns.
- Names: `firstName`, `middleName`, `lastName`, `email`, `mobilePhone.countryCode` (select; codes
  repeat, match the exact text "+55"), `mobilePhone.number`, `gender`,
  `standardFields.nationality.answer`, `standardFields.dateOfBirth.answer` (read-only datepicker),
  `workExperience.years` + `workExperience.months`, `currentSalary.currency` +
  `currentSalary.amount`, `expectedSalary.currency` (read-only, USD) + `expectedSalary.amount`,
  `standardFields.availability.answer` (days), `standardFields.locationPreference.answer`,
  `standardFields.currentLocation.answer`, `skills` (chip input), `candidateConsent`, `captcha`.
- Company questions: `standardFields.<uuid>.answer`; read the label from the closest wrapper.
- **Current salary is required** — "prefer not to say" doesn't fit; it's a user decision.

## Files

- **Don't upload the CV first.** Both resume inputs (`#resume-upload` and the one inside "Upload
  Resume/CV") start a resume parser that froze the page for good on a 2.5 MB PDF (3 attempts),
  and a working parse can overwrite filled fields. Fill everything, then leave the CV to the user
  (or try it last and re-check every field).
- "Additional Documents" has its own file input and uploads fine (cover letter goes there).

## Traps

- JS output truncates around 900 characters: stash in `window.__k` and read in slices.
- Fields vary by tenant (some have no nationality, LinkedIn or company questions). `expectedSalary.currency` follows
  the tenant (read-only USD or INR) and the amount has **no period label**: Indian tenants mean annual CTC.
- "Apply for this job" can look disabled while the page loads; a coordinate click a few seconds later works.
- `locationPreference` lists only the tenant's job cities.
- "+ Add Experience/Education Details" only respond to JS: `addNewExperienceDetail()` / `addNewEducationDetail()`
  (rows load by ajax in 1–2 s). Experience ids `companyName_n`, `designation_n`, `isCurrentlyWorking_n`,
  `experienceDateOfJoining_n`, `dateOfRelieving_n`, `experienceLocation_n` (n from 1) — no description field.
  Education ids `degree_n`, `branch_n`, `educationDateOfJoining_n`, `dateOfCompletion_n`, `university_n`,
  `educationLocation_n` (n from 0). Dates are read-only jQuery UI pickers ("MM yy"):
  `jQuery('#id').datepicker('setDate', new Date(y, m, 1)).trigger('change')`, joining date first.
- Skills chips: real click, type, Enter (doesn't submit).
- On some tenants the resume upload rejects a valid 2.5 MB PDF as "corrupted". Try a lighter file (DOCX or a compressed PDF); if it still fails, the user submits without it.
