---
name: source-discovery
description: Discovers new job sources through the recruiters in the user's LinkedIn network — reads every company each recruiter has worked at, saves all those companies, removes the ones already seen or already sources, reads each new company's website, then hands them to source-check, which finds the careers listing and records the cheapest way to read it (public API first). Use when the user says "find new sources", "discover new companies", "look at the companies my recruiters worked at", "descobrir novas fontes", "pega mais recrutadores", "next batch of recruiters".
---

# Source discovery

A recruiter's experience list is a map of companies that hire tech people. This skill turns the
user's recruiter connections into **new sources**, in stages that each finish before the next
starts, so nothing is opened twice:

```
recruiters (connections) ─► every employer ─► dedupe (profiles, log, sources page)
                         ─► website of each new company ─► source-check (listing → API first)
```

| Stage | Who | Cost |
|---|---|---|
| Find recruiters, read their experience, read company pages | `linkedin-reader` (Sonnet, read-only browser, own tab) | One page load per recruiter or company |
| Dedupe and keep the log | `scripts/discovery_log.py` — never by hand | None |
| Careers listing and access method | `source-check` → `source-validator` in batches | `curl` only |

## 1. Load

From `CAREER_PROFILE`: the index (Sources page, Sources command, **Discovery log**), `rules.md`
(the exclusion list: companies whose people the user never contacts and that are never recorded).
No Discovery log setting → ask the user for a folder and save it in the index before starting.

`LOG` = that folder; `run stats` shows what earlier rounds left:

```bash
python3 -I scripts/discovery_log.py stats "$LOG"
```

## 2. Recruiters

**Default: the user's own connections.** One `linkedin-reader` call, `MODE: search`, with people
searches filtered to first-degree connections:

```
https://www.linkedin.com/search/results/people/?keywords=<terms>&network=%5B%22F%22%5D&origin=FACETED_SEARCH&page=<n>
```

Terms: `tech recruiter`, `technical recruiter`, `talent acquisition`, `IT recruiter`,
`technical sourcer`, plus the profile's location terms (e.g. `latam`, `nearshore`) and the
interface language's word for recruiter. Up to ~10 pages per term while results keep coming.
A list the user already keeps (names or slugs of recruiter connections) can seed or replace the
search — ask for it when the profile points to one.

```bash
python3 -I scripts/discovery_log.py people "$LOG" search-*.json --out pending.json
```

`pending.json` holds everyone not read yet. A batch is **50 recruiters** unless the user says
otherwise; prefer headlines about tech recruiting and the user's target regions, and vary the
employers (five people from the same company read the same companies).

## 3. Experience — every employer

Groups of ~13 slugs, one `linkedin-reader` per group, `MODE: experience`, in parallel. Each reader
records **every** employer of the recruiter (not only the current one), with role, dates and
whether the role was recruiting. Opens nothing but the experience pages.

Before the batch, open an **anchor tab** (`tabs_context_mcp` with `createIfEmpty`) and keep it until
the last reader returns: Chrome removes an empty tab group, and with it the readers' tabs. Watch
the readers as the session's own rules say (done files, an idle alert). A reader that reports a
LinkedIn warning → stop every reader and open no LinkedIn page again that day (the web route in §5
still runs).

## 4. Dedupe

```bash
python3 -I scripts/discovery_log.py roles "$LOG" exp-*.json --sources <sources page> \
  --exclude "<excluded companies, comma-separated>" --out companies-new.json
```

It keeps employers where the person worked in recruiting, drops schools, freelance and the
person's own business, merges the same company found through several profiles, drops what the log
already has and what the sources page names, and saves **every** company link in the log. Report
the counts it prints.

## 5. Websites

Groups of ~25 links from `companies-new.json`, one `linkedin-reader` per group, `MODE: company`,
**at most 4 readers at a time** (same anchor-tab rule): nine company readers in parallel got HTTP 429
from LinkedIn after two pages each (13/11/2026). Then:

```bash
python3 -I scripts/discovery_log.py sites "$LOG" comp-*.json --sources <sources page> --out leads.json
```

**When LinkedIn stops the stage** (a 429 or any warning): don't read company pages again that day.
The companies left can still go on without LinkedIn — hand them to `source-check` as leads with only
the name and the company link (`website: null`): the validator finds the official site on the web,
confirming the homepage names the company, and goes on from rung 0. Search engines also throttle
bursts, so expect `no-site` for small companies whose domain can't be guessed.

A company whose domain is already on the sources page becomes `known`. `leads.json` is the list of
new companies with their website.

## 6. Careers and access → source-check

Hand `leads.json` to `source-check` as company leads (batches of ~20 per validator, `curl` only).
It finds each company's listing, climbs the access ladder — **the public API first**, then a feed
or embedded data, plain HTML, the browser last — and records the new sources with the sources
command. Then:

```bash
python3 -I scripts/discovery_log.py verdicts "$LOG" <validator output files>
```

Any company that hires tech people is worth a source, even with no opening for the user's target
today: the system serves other stacks and other people too.

## Output

```
Recruiters read: <n> (<n> waiting for the next batch)
Companies: <n> links saved · <n> duplicates across profiles · <n> already in the log · <n> already sources · <n> new
Websites: <n> read · <n> without a website
Sources: <n> created (<n> API · <n> page · <n> browser) · <n> no listing · <n> not tech · <n> down
```

Then the openings matching the profile's target that the validators saw (not recorded — that's
`job-sweep` and `opportunity-log`), the leads that need a browser, and one status table: done,
waiting for the user, not started.

## What this skill never does

- Click Connect, Follow or Message, send an invitation, type on LinkedIn — reading only
- Retry around a LinkedIn warning, a login wall, a CAPTCHA or a paywall
- Open a company page the log or the sources page already covers
- Record a role, or a source whose method nobody ran
