---
name: ats-apply
description: Applies to a role through its application form (Greenhouse, Lever, Ashby, Workday, Workable, SmartRecruiters, InHire, Gupy, Zoho Recruit, SuccessFactors, Oracle Cloud, or a company's own form). Use when job-intake routes to a form, or when the user says "apply to this one", "fill the form", "submit my application". Resolves every answer from the profile first, hands the form to the form-filler agent with the platform playbook, and records the result. Stops for what only the user can do — account, login, CAPTCHA, document numbers, unanswered questions.
---

# ATS apply

The form is filled by the `form-filler` agent, from a **playbook per platform** and the
profile's **answer bank**. This skill resolves everything the agent will need, so the agent
never has to decide.

## 1. Identify the platform

From the application URL:

| URL contains | Playbook |
|---|---|
| `greenhouse.io` (board or `/embed/job_app`) | [greenhouse](playbooks/greenhouse.md) |
| `lever.co` | [lever](playbooks/lever.md) |
| `ashbyhq.com` | [ashby](playbooks/ashby.md) |
| `myworkdayjobs.com` | [workday](playbooks/workday.md) |
| `workable.com` | [workable](playbooks/workable.md) |
| `smartrecruiters.com` | [smartrecruiters](playbooks/smartrecruiters.md) |
| `inhire.app` | [inhire](playbooks/inhire.md) |
| `gupy.io` | [gupy](playbooks/gupy.md) |
| `zohorecruit.com` | [zoho-recruit](playbooks/zoho-recruit.md) |
| `successfactors` | [successfactors](playbooks/successfactors.md) |
| `oraclecloud.com` | [oracle-cloud](playbooks/oracle-cloud.md) |
| `keka.com/careers` | [keka](playbooks/keka.md) |
| `docs.google.com/forms` / `forms.gle` | [google-forms](playbooks/google-forms.md) |
| `linkedin.com/jobs/view` with Easy Apply (only when the profile's rules allow it) | [linkedin-easy-apply](playbooks/linkedin-easy-apply.md) |
| anything else | the profile's **site notes** (`Site notes` in the index) for that site, if any, plus [generic](playbooks/generic.md) |

A company careers page often **embeds** one of these; the playbook says how to reach the real
form. Pass the agent both sources when they exist: the plugin playbook for the platform and the
profile's site notes for that specific site.

## 2. Resolve the answers — before the agent opens anything

1. `CAREER_PROFILE` → index (CV and cover-letter paths per language), `facts.md`, `answers.md`,
   `rules.md`.
2. **Map the form's questions first** — through the agent, never by reading the page here. Call
   `form-filler` with `SUBMIT: map`: it opens the form, lists every field and question with what
   matched the profile and what didn't, types nothing, and returns. The answers are resolved
   **here**, never improvised there.
3. For each question: the answer from `answers.md`; a free-text question from its "already
   answered" table; a new free-text question → write it from `facts.md` (summary, stories) and
   **show it to the user** before sending, unless the profile's autonomy says otherwise. A
   question with no basis in the profile → it stays pending for the user.
4. Cover letter: the profile's PDF when there's a file field; the `cover-letter` text, from
   where `templates/README.md` says it lives, when it's a text field; always when the field
   exists, even if optional (profile rule).
5. Autofill platforms (Workday, SuccessFactors, Lever): tell the agent which experiences and
   dates are correct, so it can fix what the parser breaks.

## 3. Hand off

**Platforms whose playbook says "account required"** (Workday, Gupy, SuccessFactors, Oracle
Cloud…): ask the user to log in first and tell you when the form is open. The agent never logs
in; called too early it only returns `pending: login`.

Call `form-filler` with `URL`, `PLAYBOOK`, `FACTS`, `ANSWERS` (path + the resolved answers for
this form), `FILES`, and `SUBMIT: no`: the agent fills and verifies everything and stops with the
submit button visible. **The final click is made here, in the main session**, after reading the
agent's report — so the user's approval (the profile's autonomy, or a per-click permission
prompt) applies to that one action. An agent relayed a "submit" by the caller may refuse it, and
it should. `SUBMIT: yes` stays available for runs the user explicitly delegates end to end.

Blocked platform (the browser tool reports "permission denied" on the domain, or a CAPTCHA, or
a login): the agent returns `PENDING`. Don't retry around it; tell the user what to unblock and
hand over the tab with the form filled as far as it went.

## 4. Record and learn

`pipeline-keeper`, `EVENT: application`, channel `<platform>`, status `sent` or
`pending-user: <what>`, external id = the confirmation or requisition id.

The agent's `notes` are kept so the next application is cheaper. Where they go:

- **A reusable mechanic of an ATS family** (Greenhouse, Lever, Keka, Easy Apply…: a selector, a
  widget, a trap every tenant shares) → the plugin playbook.
- **Anything specific to one site or tenant** (a company's own careers page, a job board, a
  question only that employer asks) → the profile's **site notes**. A new site never needs a
  plugin change.

## Output

One line: `<Company> — <role>: sent via <platform> (<confirmation>)` or
`pending with you: <what> (tab open)`. Then the free-text answers that were written for this
form, so the user knows what was said in their name.
