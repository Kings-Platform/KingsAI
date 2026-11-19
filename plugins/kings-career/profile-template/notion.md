# Notion — Opportunities, Applications and Processes

<!-- Only when the index says "Pipeline format: notion". Fill the ids and the Names table, keep the rules you want, delete the rest. -->

Where the applications pipeline lives: two databases, one shareable, one private, linked to each
other — plus, optionally, a processes database for the applications that move forward. Read by the
`opportunity-log` skill and its agents (`opportunity-analyst`, `opportunity-writer`), by
`process-log` and its agents (`process-analyst`, `history-keeper`), and by `inbox-triage` /
`reply-drafter` for status updates. Writing to the databases listed here is authorized by this
page; everything else in Notion stays read-only unless the index says otherwise.

| Database | Data source | Who sees it |
|---|---|---|
| Opportunities (`https://www.notion.so/<page-id>`) | `collection://<data-source-id>` | Shareable: the posting itself, nothing about you |
| Applications (`https://www.notion.so/<page-id>`) | `collection://<data-source-id>` | Private: what you sent and how it's going |
| Processes (optional) | `collection://<data-source-id>` | The selection process, once an application advances |
| Meetings (optional, with Processes) | `collection://<data-source-id>` | Interview notes and transcripts |
| Contacts (optional, with Processes) | `collection://<data-source-id>` | Recruiters and interviewers |

A posting without an Application is one saved for someone else — that's how the two kinds are told
apart.

Page language: `<language of the Overview, section titles and notes>`. Page icons: `<none | emoji | …>`.

## Names

The agents never assume a property or section name: they read it here. Rename the right column to
your databases' real names (in any language); the rules below use the left column.

| Role | Name in your Notion |
|---|---|
| Opportunity title | `Title` |
| Opportunity posted date | `Posted on` |
| Opportunity status · checked date | `Status` · `Checked on` |
| Opportunity → Application relation | `Application` |
| Application title | `Title` |
| Application → Opportunity relation | `Opportunity` |
| Application → Process relation | `Process` |
| Application sent date (a date range) | `Sent on` |
| Overview section · must-haves label | `Overview` · `Must-haves` |
| Contact section | `Contact` |
| Description section | `Job description` |
| Answers section (Applications body) | `Answers sent` |
| Taken-down line in the Overview | `Posting taken down on DD/MM/YYYY` |
| Taken-down callout (inside the description) | `Posting closed — the original text is no longer available.` |
| Value not in the record | `not recorded` |
| Status-update line (Applications body) | `**Return DD/MM/YYYY (<channel>, <sender>):** <what happened>` |
| Talent pool title | `<Company> → Talent pool — <area>` |

## Opportunities — properties

Property keys are the database's names as-is. Values are plain text: no markdown escaping. Fill
only what the posting or post says — a field is never filled just to have a value; hashtags are not
evidence.

| Property | Rule |
|---|---|
| Title | `<Company> → <Role as the posting writes it>`. A company name that is a domain is written without the TLD (Notion turns domains into links). Two postings with the same title keep the same title; the properties tell them apart |
| Company | Company name; a staffing agency adds `(staffing; client not named)` or the client. A post that names no company → the author's current company when it can be read; otherwise `Not named` |
| Link | The posting URL (ATS, careers page or `linkedin.com/jobs/view/<id>`). Empty when there's only a post |
| Post | The LinkedIn post the role came from, when there is one |
| E-mail | Contact e-mail for applying, published in the posting or the post. Not accessibility or support addresses |
| Posted on | The posting's publish date; otherwise the post's date. Never later than the application date — a later date is the page's "updated" stamp: leave it empty |
| Status | Active / Closed / Expired / Not checked. **Active** only when this run saw the posting open; **Closed** only with evidence (404/410, "no longer accepting", removed from the ATS list); **Expired** = a post with no posting link, 3+ weeks after its date; otherwise **Not checked**. Never guess |
| Checked on | Date of the check that set Status (fill together with it) |
| Contract | Only what the posting states (e.g. `Employee / Contractor / Freelance`, or your country's contract types) |
| Model | Remote / Hybrid / On-site. **Remote only when the employer's text says the role is fully remote**; any office requirement is Hybrid or On-site; an aggregator's "Remote" label or a silent text → empty |
| Location | `City, Country`; several cities in one country → `A / B, Country`; no city → the country alone; several countries and no city → empty (the country tags carry them). Never the work mode: that is Model |
| Country | Tags: every country the posting names as where the job is or who it accepts. A region only when no country is named (e.g. Americas, Global). Unknown → empty |
| Currency | The currency of the published range; no range → the currency of the job's country |
| Pay | **Only when the posting publishes pay** — a range or a single value; otherwise empty. Never your expectation, never a figure from your own form answers |
| Seniority | From the title, else from the years asked (`≤2 → Junior, 3–4 → Mid, 5+ → Senior`; none → empty) |
| Technologies | What the posting asks for, from the existing options; add an option only for a recurring relevant skill |
| Sector | The company's industry, only with evidence (the posting, the company's own description); otherwise empty |
| Application | Relation, set from the Applications side |

### Mapping rules (evidence, not guesses)

| Posting says | Property |
|---|---|
| A named contract type of your country | Contract = that type |
| Abroad: "permanent", "full-time employee" | Contract empty (a local contract type doesn't apply) |
| "Contract", "6-month contract", "right-to-hire" | Contract = Contractor |
| "Freelance", "per project", paid per hour/task | Contract = Freelance |
| "Full-time" alone | Contract empty (a schedule, not a contract type) |
| Junior / Mid / Senior / Staff / Lead / Principal in the title | Seniority from the title |
| A level number in the title ("Engineer II") | Seniority from the number; it wins over the years rule |

## Opportunities — page body

```
<h2 color="blue_bg">
Overview
</h2>

<2–3 sentences: what the product/team is, mode and place>

**Must-haves**

- <the 3–5 must-haves, short>

<h2 color="blue_bg">
Contact
</h2>

- <Name> — <role: recruiter / hiring manager / post author> — [LinkedIn](<url>) · <email>

<h2 color="blue_bg">
Job description
</h2>

<synced-block>
#### **<Title — location · type, as the posting header shows>**

<the posting's own text, literal, in its own language: bold section titles, "- " bullets>
</synced-block>
```

Headings use the names of the Names table. Blank line between blocks; the Contact section only
when an official contact is tied to the posting.

- **Description is literal.** Copy the posting's text; don't summarize, translate or reorder. Drop
  only page chrome (Apply buttons, cookie notes, duplicated footers) and lines made only of
  hashtags. A post-only role uses the post's text.
- **Contact:** someone who can be reached to talk about the role directly — the recruiter or hiring
  manager, the "job poster" a job page shows, or the post's author when the post offers to answer.
  Not people who only reacted to, commented on or reshared it. A post by a company page has no
  Contact section: its e-mail goes to the E-mail property. Always with the profile link when one
  exists.
- No line repeating the posting or post link: those live in properties.
- **Talent pool** (no specific opening): the description holds only text the company published;
  nothing published → no description section, and the Overview says so. Your own notes (interviews,
  what you were told, pay discussed) never go on the Opportunities page: they belong on the
  Applications page, which is private.
- **Posting taken down** and there was an application: keep the section, and inside the synced
  block write only the taken-down callout (`fetch_posting.py --unavailable --unavailable-text
  "<the callout text from the Names table>"` writes it), dated in the Overview with the taken-down
  line. The Overview then comes from the screener's card.

## Applications — properties

| Property | Rule |
|---|---|
| Title | Same as the Opportunity title |
| Opportunity | Relation to the Opportunities page |
| Status | Applied / Confirmed / In progress / Rejected / No return / Closed — the latest event wins. A confirmation from the company (auto-reply, confirmation page, an ATS's default label right after sending) → Confirmed; an e-mail you sent with no reply → Applied; In progress only when a person engaged (a reply, a test, an interview) |
| Sent on | Date range: **start** = the day the application was sent; **end** = the day the process ended (the rejection's date for Rejected, the closing date for Closed / No return). Empty end = still open |
| Channel | ATS / Easy Apply / E-mail / DM / Site |
| Platform | Where it was submitted (Greenhouse, Lever, Gupy, LinkedIn for Easy Apply, Gmail, the company's own form…) — add the option when new |
| Language | The language the application was **sent** in (CV and answers), not the posting's |
| Expectation sent | What you asked, as sent; empty when none was asked |
| Gaps | One line: the posting's must-haves that `facts.md` doesn't support (or supports weakly). Always a missing work authorization or residence when the posting requires one. Only gaps — never logistics you meet |
| Process | Relation to the processes database, when the application becomes a process |

## Applications — page body

```
<h2 color="blue_bg">
Answers sent
</h2>

<confirmation text in one line>

| Field | Answer |                                  ← form answers as sent
| --- | --- |

**<free-text question>**

> <answer as sent>
```

E-mail applications: recipient, subject, attachment and the gap sentence, quoted.

## Applications — status updates

A new event about an application already in Notion (an e-mail, a reply, an interview) changes the
existing page; nothing is created. Two edits:

1. `Status` by the rule above. Vocabulary from the other skills: `confirmed` → Confirmed,
   `in-process` → In progress, `rejected` → Rejected, `closed` → Closed. Never downgrade on a
   weaker event (a confirmation doesn't undo In progress). Rejected or Closed also sets the end of
   `Sent on` to the event's date (the e-mail's, not today's).
2. One line appended at the end of the body, dated, with the source — the status-update line of the
   Names table, with the deadline when there is one.

No page found → the application is missing: run `opportunity-log` for it rather than inventing a
page here.

## Select options in use

<!-- Keep this list equal to the databases' options; the agents use these names exactly. -->

Only **Platform**, **Currency**, **Country** and **Sector** may get a new option; everything else
stays within the list — a technology that isn't here is simply not tagged.

- **Technologies:** `<…>`
- **Sector:** `<…>`
- **Currency:** `<…>` · **Country:** `<…>`
- **Contract:** `<…>` · **Model:** `<…>` · **Seniority:** `<…>`
- **Opportunity status:** Active, Closed, Expired, Not checked
- **Application status:** Applied, Confirmed, In progress, Rejected, No return, Closed · **Channel:** ATS, Easy Apply, E-mail, DM, Site · **Language:** `<…>`
- **Platform:** `<…>`

## Notion syntax

The syntax every page here uses — colored headings, synced blocks, callouts, tables, escapes — and
the read-back check after each write live in the `kings-general:notion-manage` skill. Load it
before writing; the page models above are written in that syntax.

The description section never needs hand-written syntax: `fetch_posting.py --body-out` (or
`--wrap` / `--unavailable`) writes it ready to paste.

## The plan file (analyst → writer)

The analyst decides everything and writes the Opportunities page itself (it holds the posting's
text, so the copy stays faithful). The writer only writes the Applications page. The plan is a
JSON file:

```json
{
  "opportunity": {"page_id": "…", "url": "https://www.notion.so/…"},
  "deferred_properties": {"Currency": "JPY"},
  "relations": {"opportunity": "Opportunity", "process": "Process"},
  "application": {"properties": {"Title": "…", "Status": "Applied", "date:Sent on:start": "2026-10-07", "date:Sent on:is_datetime": 0, "…": "…"}, "body": "<h2 color=\"blue_bg\">\nAnswers sent\n</h2>\n\n…"},
  "processo": null,
  "new_options": [{"database": "applications", "column": "Platform", "option": "Recruitee"}],
  "replace_body": false
}
```

- `properties` use the exact keys of the data source (dates split into `date:<name>:start` /
  `:is_datetime`; multi-selects as JSON arrays; plain-text values, no escaping).
- `deferred_properties`: opportunity properties whose select option doesn't exist yet — the caller
  creates the option, then the writer sets them.
- `relations`: the Application's relation property names, from the Names table — the writer sets
  them with these keys.
- `application` (or `null`); the writer adds the relation to the opportunity itself.
- `processo`: the URL of the process page when the application became a process, else `null`.

## Processes (optional)

Only with a Processes database. Read by `process-log`, `process-analyst` and `history-keeper`.

**Rule:** as soon as an interview with a person is scheduled (any phase, a first recruiter call
included), the process page exists and the application links to it. An automated screening (an AI
audio or chat, a recorded self-intro, a test platform) does not count.

**Page pattern**, top to bottom:
1. Two callouts side by side (`<columns>`): the posting link and the company site.
2. A **History** toggle heading (h2) with the history table inside it — newest first, written only
   by the `history-keeper` agent.
3. `<h2 color="blue_bg">` **Overview** — one fact per bullet: company, where the role came from,
   contract, model and currency, client (for an agency), expectation or offer, the main gap, the
   **phases** as a numbered list (✔ on the done ones), and **your pending items**. Rewritten after
   every event; no timeline here.
4. `<h2 color="blue_bg">` **About** — a synced-block reference to the Opportunity's description block
   (`<synced-block-reference url="<opportunity>#<block id>"></synced-block-reference>`), never a
   pasted copy.

- Name: the company. An agency or consultancy placing you at a client: `<Agency> → <Client>` (the
  agency alone while the client is unknown).
- Contacts: every recruiter or interviewer gets a Contacts page (name, e-mail, LinkedIn, role),
  related to the process and the meetings; the page body stays blank.
- Properties (rename to yours): Status, Current phase, Total phases, Progress (done / total),
  Expectation/Offer, Gross, Currency, Period, Contract, First contact, Contacts, Meetings. **Current
  phase** counts only phases confirmed (scheduled) or done.
- Sections or toggles you add by hand stay — the agents never remove them.

**History table — exact markdown** (heading, column names and date format are yours to rename):

```
<toggle heading="h2">
History

<table header-row="true">
<tr>
<th>Date</th>
<th>Description</th>
</tr>
<tr>
<td>15/10/2026</td>
<td>Fact.<br />  • topic<br />  • topic</td>
</tr>
</table>
</toggle>
```

A single fact stays plain text; two or more become `  • …` lines joined with `<br />`. Interview
rows: a bold title (phase, who, time, channel, outcome) and 2–3 bullets.

**Meeting pages:** title `<Company> - <Phase>` (the first call: `<Company> - Intro call`); date,
relation to the process and participants set; the note's own content stays as the recorder wrote
it.
