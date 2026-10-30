# Tracker RMS

URL shape: `https://<host>.tracker-rms.com/<Db>/apply?jobcode=<N>`.

## Gate — the user's

The apply URL redirects to `/Resource/Register/?db=<Db>&jobcode=<N>` and shows a MotionCAPTCHA
("draw over the shape you see", `canvas#mc-canvas`) before any field. Return `PENDING: captcha`
and leave the tab open; once the user solves it the URL becomes `/Resource/Register` and the
agent continues in that tab.

## Form

One page with "Next" steps: Contact → Employment History (3 collapsible rows) → Supporting
Documents (up to 3 files) → "Your Application is ready to submit!" → **Submit Application**.
No account or password. Required: first name, surname, email, mobile phone.

- Field names: `Resource.*`, `History[i].*`, `References[i].*`. The LinkedIn field is
  `Resource.otherphone`.
- Text fields: native value setter + `input`/`change`/`blur`. Selects: plain `.value` + `change`.
- Dates are read-only flatpickr inputs (`d M Y`): `el._flatpickr.setDate('01 Feb 2023', true, 'd M Y')`.
  Month/year only in the profile → day `01`.
- Only 3 employment rows: list the most relevant roles; say which one was left out.
- Uploads use Dropzone with 3 hidden `input[type=file]`, one file per input. The inputs read
  0 files afterwards — check `Dropzone.instances[i].files[j].status === 'success'` instead.
- A hidden timesheet-approval modal has `approveTimesheets*` checkboxes ticked by default; it is
  not part of the application — ignore it when reading checkboxes back.

## Confirmation

Path `/Resource/SaveRegistration`, title "Thank You", text "Thank You <name> — Your Application
has been successfully received".
