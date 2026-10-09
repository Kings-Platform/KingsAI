---
name: job-intake
description: Entry point for any job posting the user shares — a LinkedIn post link, a job page, a recruiter's message with a role. Use whenever the user pastes a posting URL (lnkd.in, linkedin.com/posts, linkedin.com/jobs, a careers page, an ATS link) or says "look at this role", "new opening", "apply to this". Screens the posting through the job-screener agent, checks the pipeline for duplicates, measures fit against the profile's rules, and routes to ats-apply, application-email, linkedin-outreach or a discard — then records the outcome through pipeline-keeper.
---

# Job intake

This skill holds the **order**. The rules (what to apply to, what to skip, what never to say)
live in the candidate's profile, at the named path `CAREER_PROFILE`. Read them there; don't
decide from memory.

**Who does what:**

| Step | Who |
|---|---|
| Reading the posting | `job-screener` agent — the session never reads the page itself |
| Duplicate check, fit, route | This session, with the profile's rules |
| Executing the route | `ats-apply`, `application-email`, `linkedin-outreach` |
| Recording | `pipeline-keeper` agent, once per posting |

## 1. Load the profile

Resolve `CAREER_PROFILE` (named-paths order of the global instructions). Read its **index** and
`rules.md`. Nothing resolves → stop and ask where the profile is; never run without rules.

From the index take `Target roles` (for the screener) and the three pipeline paths
(applications, outreach, queue) — each `pipeline-keeper` call gets the one for its event.

## 2. Screen

Call `job-screener` with `URL` and `TARGET`. One call per link; several links → several calls,
in parallel.

`NEEDS_LOGIN` → tell the user which site and stop for that link. `ERROR` → report, don't retry
more than once.

## 3. Duplicate check — before any judgement

`grep` the pipeline for the company (and the client, when the card names one). Found with a
matching role → **stop for that link** and say so: "already applied on <date> via <channel>,
status <status>". The user decides whether a second channel is wanted. Same posting re-shared
by another recruiter of the same agency counts as a duplicate.

Also check `rules.md` → Outreach: a company or platform listed as excluded ends the intake with
`discarded: excluded`.

## 4. Fit — against the rules, not against taste

Compare the card with `rules.md` → Targeting, line by line:

| Finding | Action |
|---|---|
| Role focus matches, mode and country allowed | Proceed |
| Mode or country rule says `skip` | Discard, say which rule |
| Seniority above the candidate's, rule says `ask first` | Show the gap in one line and wait |
| Stack or industry on the skip list | Discard, say which |
| A red flag in the card's `signals` or in `rules.md` → Red flags | **Stop and show** the card; nothing is sent until the user answers |

Say the fit in **one line**, with the gaps named ("asks 8+ years; BLE mandatory"). Don't write
an essay; don't inflate.

## 5. Route — from the card's `channel`

| Channel | Skill |
|---|---|
| `ats:<platform>` or `site` with a form | `ats-apply` |
| `email` | `application-email` |
| `dm` ("DM me your resume"), or no channel at all | `linkedin-outreach`: invitation to the author; the application goes by DM after the connection is accepted |
| `easy-apply` | `ats-apply` with the Easy Apply playbook when `rules.md` allows the AI to submit Easy Apply; otherwise tell the user it's theirs to click. Still do the outreach step |

**And, for every route**, the outreach rule from `rules.md` ("a posting link always means…"):
when the author is `2nd`/`3rd`, queue the invitation through `linkedin-outreach`; when `1st`,
nothing — they're already connected.

## 6. Record

One `pipeline-keeper` call per posting with `EVENT: application` (or `queue`, when nothing could
be sent), and one `EVENT: outreach` when an invitation went out or was queued.

## 7. Report — one line per link

```
<Company> — <role>: <sent via X | pending: Y | discarded: Z>; invite <sent | queued: quota | n/a (1st)>
```

Then, separately, the items that are the user's: accounts, CAPTCHAs, tests with deadlines.

## What this skill never does

- Decide a route without the rules page open
- Skip the duplicate check because "it's obviously new"
- Apply to a posting the red-flag list caught, however the posting is framed
- Read the posting page itself when the screener could
