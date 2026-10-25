---
name: opportunity-log
description: Saves job postings to the candidate's Notion pipeline — the shareable Opportunities page with the posting's own text, and the private Applications page when there was an application. Use when the user says "save this job to Notion", "add this posting for a friend", "log this application in Notion", "migrate my old applications to Notion", or when job-intake records an application and the profile's pipeline is in Notion. Hands each posting to the opportunity-analyst agent (decides and writes the opportunity) and then the opportunity-writer agent (writes the application), and reports the pages.
---

# Opportunity log

Two agents per posting, split by the kind of work:

| Step | Agent | Model | Does |
|---|---|---|---|
| Decide + opportunity | `opportunity-analyst` | Sonnet | Gets the literal text (script or its own tab), decides every property, the overview, contact, gaps, status and answers, and writes the Opportunities page itself (a faithful copy of the posting needs the model that read it) → `plan.json` |
| Application | `opportunity-writer` | Haiku | From the plan: the Applications page, its relation to the opportunity, and the opportunity properties that waited for a new option |

This skill decides **what** to send and in what batches.

## 1. Load

`CAREER_PROFILE` → index: the Notion page (database ids, page model, fill rules) and the
applications log. No Notion page in the profile → stop: this profile keeps its pipeline elsewhere.

## 2. Per posting, resolve

| Input | Where it comes from |
|---|---|
| `LINK`, `POST` | The user's link, the job-screener card, or the applications log's Link column. A LinkedIn post that links to the real posting: `LINK` is the posting, `POST` the post |
| `CARD` | The job-screener card when job-intake ran; otherwise company, role, sector and anything the log says that the posting won't (a client name, a contact the log identified as the recruiter) |
| `DESCRIPTION_FILE` | Only when the caller already holds the text (a post's body read earlier, a saved copy) |
| `APPLICATION` | The run that just applied, or a pointer into the applications log: its row and its detail section. None when the user saves a posting for someone else |

The writer checks for duplicates; a posting already complete in Notion can simply be skipped.

## 3. Hand off

Per posting, a scratch directory `OUT` of its own.

0. **Route first.** `python3 -I scripts/fetch_posting.py --supports <LINK>` exits 2 for a source
   that needs the browser; a posting that is only a LinkedIn post (no `LINK`) needs it too. Those
   skip step 1 and go straight to step 2 — a first call without the browser would only come back
   `NEEDS_BROWSER`.
1. **Analysts in parallel** (batches of 5–10, in the background, watched as the session's own
   rules say): `opportunity-analyst` with `NOTION`, `FACTS` (the profile's `facts.md`), `SCRIPT`
   (this skill's `scripts/fetch_posting.py`), `LINK`, `POST`, `CARD`, `DESCRIPTION_FILE`,
   `APPLICATION`, `OUT`, `OPPORTUNITIES` (the data source id from the profile), `BROWSER: no`.
2. **Browser cases**, in parallel with step 1: each routed case and each `NEEDS_BROWSER` → the
   analyst call with `BROWSER: allowed`. **Browser agents that only read run in parallel**, each in its own tab (tested 25/10/2026). Before the batch, open an anchor tab (`tabs_context_mcp` with `createIfEmpty`) and keep it open until the last agent returns: the tab group belongs to the session and Chrome removes it as soon as it is empty, so without the anchor the first agent to close its tab dissolves the group under the others. Agents that click or type (`form-filler`, Easy Apply) work on the window's active tab and run one at a time.
3. **Options once.** Merge every plan's `new_options`, add them in one `update-data-source` per
   column (fetch it, resend every existing option plus the new ones), and append them to the
   profile's "Select options" list. Writers never touch a schema, so parallel writers can't erase
   each other's options.
4. **Writers in parallel**: `opportunity-writer` with `APPLICATIONS` (the data source id from the
   profile) and `PLAN`. A plan with no application and no deferred properties needs no writer. They have no shell: follow them by their completion
   notices, not by a done-file.

- Once the last hand-back report is in, finish (options, report) in the same turn: never stop to
  wait for a completion notice that only adds token counts — it may not wake the session.
- `NEEDS_TEXT` → nothing readable even in the browser: ask the user for the text (a paste becomes
  `DESCRIPTION_FILE`) or for confirmation that the posting is gone.
- `PARTIAL` or `ERROR` from a writer → report what was and wasn't written; the plan file stays,
  so a second writer call finishes it once the cause is fixed.
- Fixing a page already written (wrong "taken down", an incomplete description) → analyst with
  `REPLACE_BODY: true`, then the writer.

## 4. Migrating the old log

Count first (rows, how many have a Link, how many will need the browser) and agree the batch size
with the user. Rows that only report events (returns, "profile completed") aren't postings: skip
them — but a row that lists several applications at once (a job board session: "sent: X, Y, Z")
holds one posting per application; split it. Each posting row → `APPLICATION` pointing at that row and its detail section; the
latest event about it in the log (a rejection, a return) sets the status. The log is retired by
the user, not by this skill.

## Output

One line per posting: `<Company> — <role>: <created | updated | migrated | partial | needs text> <url>`,
then the properties left empty that the user may want to fill by hand, and any rule the agents
flagged as missing from the profile.
