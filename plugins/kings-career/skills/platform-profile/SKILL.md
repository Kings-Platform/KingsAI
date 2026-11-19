---
name: platform-profile
description: Creates or completes the candidate's profile on a talent platform or job board — the kind where a profile, not a single form, is what recruiters see (Revelo, Uplers, Welcome to the Jungle, Turing, Lemon.io, Arc, GeekHunter, AI-training "expert" pools, an ATS candidate portal). Use when the user says "fill my profile on X", "I created the account, do the rest", "complete my Revelo profile", "cadastra meu perfil", "faz o cadastro na plataforma", or when an application needs a platform profile before it can be sent. Resolves every section from the profile's facts and answers, hands the editor to the profile-filler agent, fixes what the platform's CV parser broke, and records what the site taught. Account creation, passwords, CAPTCHAs and terms stay with the user.
---

# Platform profile

A platform profile is many forms behind one login: personal data, experiences, education,
skills, languages, rate, links — each saved on its own. The **values** come from the profile at
`CAREER_PROFILE`; this skill decides them all before the `profile-filler` agent types anything.
**Complete, not minimal:** every section the platform has gets filled, optional ones included.

## 1. Load

From `CAREER_PROFILE`: the index (CV paths per language, the **site notes**, the LinkedIn URL),
`facts.md`, `answers.md` (rate, salary, availability, work authorization, notice) and `rules.md`
(Never say, autonomy). Read the site notes' section for this platform, if any, and the
"talent platforms" notes.

## 2. Account — the user's

The agent never creates an account or logs in. When there is no account yet: open the sign-up,
pre-fill the non-secret fields if the profile's rules allow it (name, email, country), and hand
over the password, the terms, the CAPTCHA and the e-mail confirmation. Continue when the user
says the editor is open.

## 3. Map

`profile-filler` with `MODE: map`: it walks the editor and returns every section, its fields,
the control type of each (text, select, chips, date picker, rate range) and what is already
there — including what the platform **imported** from the CV or LinkedIn.

## 4. Resolve every value

Build one value list, section by section, from the map:

| Section | Source |
|---|---|
| Personal, contact, location, links | `facts.md` |
| Experiences (title, company, dates, location, contract, description, stack) | `facts.md` → experience; the description is the CV's text for that role, cut to the field's limit |
| Education, certificates | `facts.md` |
| Skills | `facts.md` → skills, written with the **platform's own labels** (the option text, not a synonym); respect the platform's limit, most relevant to the target role first |
| Languages and levels | `facts.md`; map the levels to the platform's scale and say the mapping |
| Rate, salary, availability, notice, work authorization | `answers.md`, converted to the field's currency and unit (hourly vs monthly vs yearly) |
| Headline, bio, "about" | the profile's approved text when it has one; otherwise a draft from `facts.md` → summary, **shown to the user** before it is saved |
| Anything with no basis in the profile | stays empty and goes to the user's list |

**Imported items** are checked against `facts.md`: a role, school or skill the facts don't
support, or one the Never-say list covers, is marked for removal.

## 5. Fill

`profile-filler` with `MODE: fill`, the value list, the removal list, the CV file, the site
notes and `SAVE: sections` — it saves each section with the section's own button and reads it
back. Removals are listed by the agent, not done: the classifier treats a delete in an external
system as destructive when a subagent does it. **Delete here, in the main session**, each item
by name, after the user agreed to the removal list.

The final **"submit profile" / "apply" / "send for review"** — the click that puts the profile in
front of recruiters or starts a vetting process — is made here too, after the user saw the
summary, as `ats-apply` does with an application's last click.

## 6. Record and learn

- The agent's `notes` → the profile's **site notes**, under the platform's heading (controls,
  traps, limits, what the parser breaks). A reusable mechanic shared by many sites (a chips
  widget, a date picker family) goes to the plugin's
  [generic playbook](../ats-apply/playbooks/generic.md).
- The platform is a job source too: when the sources page has no row for it, hand it to
  `source-check`.
- Something left for the user (photo, video intro, a skills test, ID verification) → the
  pipeline queue, through `pipeline-keeper` with `EVENT: queue`.

## Output

```
<Platform>: profile <complete | partial> — <n> sections saved; removed: <items>
Left for you: <photo, test, verification…>
Texts written in your name: <headline / bio, verbatim>
```
