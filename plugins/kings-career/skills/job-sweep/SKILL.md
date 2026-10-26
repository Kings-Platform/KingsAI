---
name: job-sweep
description: Sweeps the candidate's job sources — aggregators, curated lists, talent platforms, company boards, ATS-domain searches — for open roles that match the profile, drops what is closed or already in the pipeline, and reports the new ones. Use when the user says "run the job search", "sweep the job sites", "any new roles this week", "faz a busca de vagas", or when the profile's sweep frequency says a run is due. Never applies: the user picks, and each pick goes to job-intake.
---

# Job sweep

The **sources** and the **search terms** are the profile's; this skill holds the order and the
[catalog](sources-catalog.md) of public sources anyone can use. Nothing here is specific to a
stack: the terms come from the profile.

## 1. Load

From `CAREER_PROFILE`: the index (target roles), `rules.md` (Targeting, Red flags, Outreach
exclusions) and the **sources page** the index names (`Sources`; usually `sources.md`). No sources
page → offer to create one from the catalog and stop.

From the sources page take:

- **Search terms** — the words a source's search URL is filled with (`{query}`), and the
  location terms (`{location}`).
- **Frequency** and each source's **last run** — or an **activation** column (on / off per source):
  when the page has one, it replaces both (see step 2).
- **Enabled catalog sources**, **disabled** ones, and the **profile-only sources** (company
  boards, recruiters' lists, anything the catalog can't name).

## 2. Pick what is due

**With an activation column** (a source is on or off): every source that is **on** runs, on every
run; frequency and last run gate nothing, and an off source is skipped without a mention. This is
what a scheduled run wants: the page decides what is swept, and a daily run that finds nothing
"due" because a person already swept by hand is not a sweep.

**Without one**, a source is due when `today − last run ≥ its frequency` (the source's own, else
the page's).

Either way the user can override: "all sources", "only the aggregators", "only <name>". Say in one
line what will run and what is skipped.

## 3. Sweep — in parallel

Group the due sources (4–6 per group, similar access method together) and call
`source-sweeper` once per group, **in parallel**. **Browser agents that only read run in parallel**, each in its own tab (tested 25/10/2026). Before the batch, open an anchor tab (`tabs_context_mcp` with `createIfEmpty`) and keep it open until the last agent returns: the tab group belongs to the session and Chrome removes it as soon as it is empty, so without the anchor the first agent to close its tab dissolves the group under the others. Agents that click or type (`form-filler`, Easy Apply) work on the window's active tab and run one at a time. Then call each with:

```
SOURCES:   <the rows of this group, with URL templates already filled>
TERMS:     <search terms>
TARGET:    <target roles + Targeting rules summarized: seniority, stack exclusions, eligibility>
SINCE:     <date of the previous run, or 8 days ago>
```

Sources that need the user's logged-in browser (talent platforms, paid lists) go in a group of
their own, so a login problem doesn't stall the rest.

## 4. Merge and dedupe

1. Merge the cards; the same role reached through two sources is one role (keep both sources).
2. Check every card against the pipeline — Notion opportunities when the pipeline format is
   `notion`, the markdown applications otherwise — and against the Outreach table. Match by the
   **posting's own id** (the job id inside the link, tracking stripped) or by role + country + city,
   **never by the company name alone**: aggregators and recruiters republish the same role under
   another company name. Prefer a script over a search for this, one lookup per card. Already there →
   "already in the pipeline", not new.
3. Apply `rules.md` once more: a card the sweeper marked "for the user" stays that way; anything
   on the exclusion list goes.

## 5. Report

```
New and relevant: <n>
  <company> — <role> | <location / eligibility> | <pay> | <posted> | <source> | <link>
For you to decide: <n>      (one line each, with the doubt: stack mix, eligibility, seniority)
Already in the pipeline: <n> (names only)
Discarded: <n> by reason   (US-only, other country, junior, stack, closed)
Sources: <name> — ok | nothing new | down (<why>) | needs login
Companies worth watching: <name> — <why> (hire the target remotely, no open role today)
```

Then update each swept source's **last run** on the sources page, and note sources whose access
changed (a URL that moved, an API that started failing) right there — the next run depends on it.

## 6. Hand off

The user picks. Each pick goes to `job-intake` (or straight to `ats-apply` /
`application-email` when the card already has the channel). Roles to keep only as a record go to
`opportunity-log` as opportunity-only.

## What this skill never does

- Apply, message, create an account or log in
- Report a role without checking it is still open
- Count a role as new without the pipeline check
- Keep a source's quirks in its own memory — they go to the sources page or the catalog
