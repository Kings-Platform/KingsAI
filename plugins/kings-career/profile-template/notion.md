# Notion — Opportunities and Applications

<!-- Only when the index says "Pipeline format: notion". Fill the ids, keep the rules you want, delete the rest. -->

Where the applications pipeline lives: two databases, one shareable, one private, linked to each
other. Read by the `opportunity-log` skill and its agents (`opportunity-analyst`,
`opportunity-writer`), and by `inbox-triage` / `reply-drafter` for status updates. Writing to these
two databases is authorized here; everything else in Notion stays read-only unless the index says
otherwise.

| Database | Data source | Who sees it |
|---|---|---|
| Opportunities (`https://www.notion.so/<page-id>`) | `collection://<data-source-id>` | Shareable: the posting itself, nothing about you |
| Applications (`https://www.notion.so/<page-id>`) | `collection://<data-source-id>` | Private: what you sent and how it's going |
| Processes (optional, an existing database) | `collection://<data-source-id>` | The selection process, once an application advances (`Process` relation) |

A posting without an Application is one saved for someone else — that's how the two kinds are told
apart.

Page language: `<language of the Overview and section titles>`. Page icons: `<none | emoji | …>`.

## Opportunities — properties

Property keys are the database's names as-is. Values are plain text: no markdown escaping.

| Property | Rule |
|---|---|
| Title | `<Company> → <Role as the posting writes it>`. A company name that is a domain is written without the TLD (Notion turns domains into links). A talent pool, not a posting: `<Company> → Talent pool — <area>` |
| Company | Company name; a staffing agency adds `(staffing; client not named)` or the client |
| Link | The posting URL (ATS, careers page or `linkedin.com/jobs/view/<id>`). Empty when there's only a post |
| Post | The LinkedIn post the role came from, when there is one |
| E-mail | Contact e-mail for applying, published in the posting or the post. Not accessibility or support addresses |
| Posted on | The posting's publish date; otherwise the post's date. Never later than the application date — a later date is the page's "updated" stamp: leave it empty |
| Contract | Only what the posting states (e.g. `CLT / PJ / Freelance / Contractor`) |
| Model | Remote / Hybrid / On-site |
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

Blank line between blocks; the Contact section only when an official contact is tied to the
posting.

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
  block write only the "posting closed" callout (`fetch_posting.py --unavailable` writes it),
  dated in the Overview. The Overview then comes from the screener's card.

## Applications — properties

| Property | Rule |
|---|---|
| Title | Same as the Opportunity title |
| Opportunity | Relation to the Opportunities page |
| Status | Applied / Confirmed / In progress / Rejected / No return / Closed — the latest event wins. A confirmation from the company (auto-reply, confirmation page, an ATS's default label right after sending) → Confirmed; an e-mail you sent with no reply → Applied; In progress only when a person engaged (a reply, a test, an interview) |
| Sent on | Date the application was sent |
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

<quote>
<answer as sent>
</quote>
```

E-mail applications: recipient, subject, attachment and the gap sentence, quoted.

## Applications — status updates

A new event about an application already in Notion (an e-mail, a reply, an interview) changes the
existing page; nothing is created. Two edits:

1. `Status` by the rule above. Vocabulary from the other skills: `confirmed` → Confirmed,
   `in-process` → In progress, `rejected` → Rejected, `closed` → Closed. Never downgrade on a
   weaker event (a confirmation doesn't undo In progress).
2. One line appended at the end of the body, dated, with the source:
   `**Return DD/MM/YYYY (e-mail, <sender>):** <what happened, the deadline when there is one>`.

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
- **Status:** Applied, Confirmed, In progress, Rejected, No return, Closed · **Channel:** ATS, Easy Apply, E-mail, DM, Site · **Language:** `<…>`
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
- `application` (or `null`); the writer adds the relation to the opportunity itself.
- `processo`: the URL of the process page when the application became a process, else `null`.
