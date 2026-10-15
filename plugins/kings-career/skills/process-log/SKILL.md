---
name: process-log
description: Keeps each selection process page in the candidate's Notion pipeline (the processes database) true and complete — creates the page when an interview gets scheduled, and after each interview or recruiter email reads the meeting transcript and the mail thread to update properties (offer, expectation, contract, phases, progress, status), the overview, the contacts and the history table. Use when the user says "an interview was scheduled", "the interview is over, read the transcript", "update my processes", "check if anyone replied", or after inbox-triage finds a process email. Hands each process to the process-analyst agent (decides and writes the page) and then the history-keeper agent (writes the history rows).
---

# Process log

A selection process has one page in the processes database, and it must always tell the truth:
what phase, what was said about money and contract, what the user still owes, what happened when.

| Step | Agent | Model | Does |
|---|---|---|---|
| Decide + page | `process-analyst` | Sonnet | Reads every source for one process (application page, process page, meeting notes with transcript, mail threads), decides properties, overview, contacts and the new history rows; writes the page, the contacts and the meeting's database fields → `plan.json` |
| History | `history-keeper` | Haiku | Adds the plan's rows to the page's history table (creates the table when missing), newest first, no duplicates |

The page model, the database ids and the fill rules live in the profile's Notion page
(`CAREER_PROFILE` → index → Notion), in its processes section. Read it; don't
decide the layout from memory.

## 1. Load

`CAREER_PROFILE` → index → the Notion page: the processes, applications, opportunities, meetings
and contacts data source ids, the page pattern, the rule "interview scheduled → process page".
No Notion page in the profile → stop.

## 2. Pick the processes

| Request | Processes |
|---|---|
| "Interview scheduled with X" | X — create the page if it doesn't exist (the rule is absolute: a scheduled interview always has its page) |
| "The interview is over" / "read the transcript" | The process of that interview |
| "Update my processes" / "check for replies" | Every page whose status is in the profile's in-progress or to-do groups |

For each, resolve what the analyst needs:
- `PROCESS`: the process page url (or `none` → create).
- `APPLICATION` / `OPPORTUNITY`: the application and opportunity pages (the application's
  relation to the process, or search by company).
- `MEETINGS`: meeting-note pages about this process since the last history row — the meetings
  database and, since the recorder can drop notes at workspace level, a search by company name
  limited to recent days.
- `MAIL_QUERY`: a Gmail query for the process (recruiter's address or domain, company name),
  `newer_than` the last history date minus one day.

## 3. Hand off

Per process, a scratch directory `OUT` of its own.

1. **Analysts in parallel** (batches of up to 5): `process-analyst` with `NOTION` (the profile's
   Notion page path), `FACTS`, the ids above, `PROCESS`, `APPLICATION`, `OPPORTUNITY`, `MEETINGS`,
   `MAIL_QUERY`, `OUT`.
2. **History keepers in parallel**: `history-keeper` with `PAGE` (the process url from the
   analyst's output), `FORMAT` (the profile's Notion page) and `ROWS` (`OUT/plan.json` → `history_rows`). A plan with no new rows needs
   no keeper.
3. Once the last report is in, finish in the same turn.

`NOTHING_NEW` from an analyst → the process had no event since its last history row; report it
in one line, no keeper.

## Output

One line per process: `<Company>: <created | updated | nothing new> — phase <n>/<total>, status
<s>; <what changed>` and its url. Then, separately, the **user's pending items** collected from
all plans (references to send, forms, tests with deadlines) — those are the user's to do.

## What this skill never does

- Reply to a recruiter or send anything (that's `reply-drafter`, with approval)
- Delete a page, a contact or a meeting
- Invent a number: an offer, a range or a phase count goes in only when a source says it
