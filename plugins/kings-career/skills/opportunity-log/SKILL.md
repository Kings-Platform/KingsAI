---
name: opportunity-log
description: Saves job postings to the candidate's Notion pipeline — the shareable Opportunities page with the posting's own text, and the private Applications page when there was an application. Use when the user says "save this job to Notion", "add this posting for a friend", "log this application in Notion", "migrate my old applications to Notion", or when job-intake records an application and the profile's pipeline is in Notion. Fetches the literal posting text, hands each posting to the opportunity-writer agent, and reports the pages.
---

# Opportunity log

The pages are written by the `opportunity-writer` agent, one posting per call. This skill gathers
what the agent needs, so the agent never has to browse or guess.

## 1. Load

`CAREER_PROFILE` → index: the Notion page (database ids, page model, fill rules) and the
applications log. No Notion page in the profile → stop: this profile keeps its pipeline elsewhere.

## 2. Per posting, resolve

| Input | Where it comes from |
|---|---|
| `LINK`, `POST` | The user's link, the job-screener card, or the applications log's Link column |
| `CARD` | The job-screener card when job-intake ran; otherwise the applications log's row and detail section |
| Literal text | `scripts/fetch_posting.py <LINK>` covers Greenhouse, Lever, Ashby and LinkedIn job pages. Anything else (a LinkedIn post, another ATS, a careers page) → read the page in the browser **in a new tab**, save the posting text to a scratch file, pass it as `DESCRIPTION_FILE` |
| `APPLICATION` | From the applications log (status, date, channel, answers sent) or from the run that just applied. None when the user saves a posting for someone else |

A LinkedIn post that links to the real posting: `LINK` is the posting, `POST` the post, and the
literal text is the posting's — the post's text only when there's no posting behind it.

## 3. Hand off

Call `opportunity-writer` with `NOTION`, `SCRIPT` (this skill's `scripts/fetch_posting.py`),
`LINK`, `POST`, `CARD`, `DESCRIPTION_FILE`, `APPLICATION`, `MODE`. Several postings → parallel
calls in batches of 3–4; watch long runs as the session's own rules say.

`NEEDS_TEXT` → get the text in the browser and call again once. `ERROR` → report, don't retry.

## 4. Migrating the old log

`MODE: migrate` for pages that already exist; `create` for log rows with no page yet. Work in
batches the user approves (count first: rows, how many need the browser). Mark each migrated row
in the log only if the profile says how; the log is retired by the user, not by this skill.

## Output

One line per posting: `<Company> — <role>: <created | updated | migrated | needs text> <url>`,
then the properties left empty that the user may want to fill by hand.
