# iCIMS

`<careers-site>.icims.com/jobs/<id>/…`. **No guest apply:** step 1 creates a profile with login and
password behind an hCaptcha, so the form starts as `pending: login` for the user.

- The form lives in a **same-origin iframe**: query its `contentDocument`, not the page.
- Stable field names: `PersonProfileFields.*` for the profile and `rcfNNNN` for the company's
  questions.
- An SMS opt-in comes as a select: answer it from the profile's rules.
- `from=login` in the URL doesn't mean the user is logged in; check the page.
