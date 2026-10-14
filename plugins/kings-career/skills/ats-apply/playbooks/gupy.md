# Gupy

`<company>.gupy.io/jobs/<id>` (Brazil). Account required — the user logs in; the CV and the
base data come from the Gupy profile, which the user maintains.

- Review the profile first when the posting matters: current employer, experiences, skills
  (some common skills don't exist in Gupy's catalog), language level. The phone lives in the
  account settings, not in the form.
- The posting's own questions (additional data, disability, institution) from the answer bank.
- **"Finalizar candidatura"** is the submit: with autonomy granted, the agent clicks it; the
  dashboard then shows the stage (e.g. "Currículo 1/5").
- Each application sends a confirmation email.

## Steps and traps

- **Closed check first:** a job page with the "Candidaturas encerradas" badge / "Inscrições encerradas" and a greyed "Candidatar-se" is closed — return closed before checking login.
- **Finding the job:** the company page loads only ~10 jobs; use the "Digite o nome da vaga"
  search (real click, type, Enter). On some company pages the search doesn't filter (and `?jobName=` does nothing): page through with a real click on the page buttons (10 per page, alphabetical) and read `a[href*="/job"]`. "Candidatar-se" → `/candidates/jobs/<id>/apply`, which
  redirects to `/candidates/applications/<appId>/steps/<stepId>/curriculum`.
- **Order:** "vamos continuar sua candidatura?" → Continuar → "Dados adicionais" → "Perguntas
  criadas pela empresa" ("Responder agora") → the questions → the optional "Apresente-se!" modal,
  whose "Finalizar candidatura" button is the submit.
- **"Dados adicionais":** the referral and employee radios come pre-set to Não
  (`radioGroupIsIndicatedTitle`, `radioGroupIsCompanyEmployeeTitle`). The source field
  (`input[name=howDidYouHearAboutUs]`) is a typeahead: a JS click closes the menu; use a real
  click on the field, type, then a real click on the suggestion.
- **An empty questions screen** (only the title and "Salvar e continuar") can be real: check
  `private-api.gupy.io/form-step-activity/candidate/form/<appId>/<formId>` (the form id shows in
  `performance.getEntriesByType('resource')`) before saving. Answers can't be edited after
  saving, so never save blanks when the endpoint lists questions.
- Reloading a step returns to the "continuar" screen and keeps what was saved.
