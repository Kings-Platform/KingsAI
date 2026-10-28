---
name: source-check
description: Validates a job source before it enters the sweep, and re-validates the ones already there — finds whether a script can read its openings through a public API or feed, plain HTML, or only a browser (API first, browser last), tests it, and records the source with that access and the exact method. Use when the user says "add this source", "new job board", "here's a site with jobs", "check if this site has an API", "revalidate the sources", "can we read X without the browser"; when job-intake gets a posting from a site that isn't a source yet; and when job-sweep finds a source it couldn't read.
---

# Source check

Reading a source through an API costs a script; through the browser it costs an agent, a tab and
minutes, every run. So no source enters the sweep — and no source stays on the browser — without
this check. The **sources page and its command are the profile's**; this skill holds the order.

## 1. Load

From `CAREER_PROFILE`: the index (the **Sources page** and the **sources command** that creates and
updates rows, with its keys and the access options), and the sources page itself. No command in the
index → stop and say the profile can't record sources yet.

## 2. Pick what to check

| Trigger | Sources |
|---|---|
| The user names a site or a link | That site. A posting link → its board: the ATS board (`boards.greenhouse.io/<co>`, `jobs.lever.co/<co>`…), the company's careers page, or the aggregator's listing |
| `job-intake` screened a posting | The posting's board, **only when** the sources page has no row for it (match by domain and by company) |
| `job-sweep` couldn't read a source | That source |
| "Revalidate" | Every enabled source whose access is not the API (or the ones the user lists) |

Already a source with an API that works → say so in one line and stop. A source that is only a
social network post or a person's profile is not a board: skip it.

## 3. Validate — in parallel

One `source-validator` agent per source (Sonnet), all in the same turn, with `SOURCE`, `TERMS`
(from the sources page), `OUT` (a scratch file per source) and `LANG` (the profile's). Agents
that open the browser each use their own tab; before the batch, open an **anchor tab**
(`tabs_context_mcp` with `createIfEmpty`) and keep it until the last agent returns — Chrome removes
an empty tab group, and with it the tabs of the agents still running.

## 4. Record

Merge the agents' files into one list for the sources command:

| Verdict | Entry |
|---|---|
| `api`, `page-ok`, `browser-only` | `access`, `how` (the method, verbatim), `notes`; a new source also `create`, `name`, `url`, `type`, `region` |
| `login` | access `Navegador logado`; the user decides whether it stays enabled |
| `dead` | An existing row: status off (the profile's "down" status) with the note. A new one: not created — report it |

Run the command, then the profile's pull (when it keeps a mirror) so the next sweep reads the new
access. A method the agent couldn't test (blocked by a permission, a key it wasn't allowed to use)
stays as it was, with the reason in `notes`.

## Output

```
<Source>: <verdict> — <access> (<evidence>) <created | updated | unchanged>
```

Then, separately: openings matching the terms the agents saw today (the sweep confirms whether
they're new), and what is the user's to decide (a login, a paywall, a test the auto mode blocked).

## What this skill never does

- Log in, create accounts, or get around a CAPTCHA, a challenge or a paywall
- Record a method nobody ran, or move a source to the browser without trying the API first
- Write a role to the pipeline — that's `job-sweep` and `opportunity-log`
