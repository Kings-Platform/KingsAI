---
name: opportunity-log
description: Saves job postings to the candidate's Notion pipeline — the shareable Opportunities page with the posting's own text, and the private Applications page when there was an application. Use when the user says "save this job to Notion", "add this posting for a friend", "log this application in Notion", "migrate my old applications to Notion", or when job-intake records an application and the profile's pipeline is in Notion. Hands each posting to the opportunity-writer agent and reports the pages.
---

# Opportunity log

The pages are written by the `opportunity-writer` agent, one posting per call. The agent gets the
posting's text itself (script, then its own browser tab), reads the application record it's
pointed at, and adds select options when needed. This skill decides **what** to send and in what
batches.

## 1. Load

`CAREER_PROFILE` → index: the Notion page (database ids, page model, fill rules) and the
applications log. No Notion page in the profile → stop: this profile keeps its pipeline elsewhere.

## 2. Per posting, resolve

| Input | Where it comes from |
|---|---|
| `LINK`, `POST` | The user's link, the job-screener card, or the applications log's Link column. A LinkedIn post that links to the real posting: `LINK` is the posting, `POST` the post |
| `CARD` | The job-screener card when job-intake ran; otherwise company, role, sector and anything the log says that the posting won't (a client name, a contact the log identified as the recruiter) |
| `DESCRIPTION_FILE` | Only when the caller already holds the text (a post's body read earlier, a saved copy) |
| `APPLICATION` | The run that just applied, or a pointer into the applications log: the Índice row and its detail section. None when the user saves a posting for someone else |

Check the Opportunities data source for the company first: a posting already there is sent with
`MODE: migrate` (or skipped), never created twice.

## 3. Hand off

Call `opportunity-writer` with `NOTION`, `SCRIPT` (this skill's `scripts/fetch_posting.py`),
`LINK`, `POST`, `CARD`, `DESCRIPTION_FILE`, `APPLICATION`, `MODE`. Several postings → parallel
calls in batches of 5–10, run in the background and watched as the session's own rules say.

- `PARTIAL` → write the pending page yourself with the values the agent returned, once.
- `NEEDS_TEXT` → the posting is gone and there was no application: tell the user, don't retry.
- `ERROR` → report, don't retry.

## 4. Migrating the old log

Count first (rows, how many have a Link, how many will need the browser) and agree the batch size
with the user. Rows that are summaries of several events (returns, "profile completed") aren't
postings: skip them. Each posting row → `APPLICATION` pointing at its row and detail section; the
latest event about it in the log (a rejection, a return) sets the status. The log is retired by
the user, not by this skill.

## Output

One line per posting: `<Company> — <role>: <created | updated | migrated | partial | needs text> <url>`,
then the properties left empty that the user may want to fill by hand, and any rule the agents
flagged as missing from the profile.
