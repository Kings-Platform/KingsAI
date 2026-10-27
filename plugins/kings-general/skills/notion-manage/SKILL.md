---
name: notion-manage
description: How to handle Notion pages and databases correctly — creating and editing pages, writing content in the connector's Markdown, setting properties (select, status, relations, dates), adding select options, attaching files, removing pages, and checking that what was written rendered as real blocks. Use before ANY write to Notion, in any workflow (career pipeline, docs, reports), and when the user says "the Notion page is badly formatted", "it shows {color=…} / <synced_block> as text", "fix the page", "create a page in Notion", "update the database". Holds the tested syntax, the API gotchas and a checker script; workflow skills keep only their own page models and point here.
---

# Notion manage

Two ways to write, and the job decides which:

| Job | Tool |
|---|---|
| Page **content** written as Markdown (a new page, a section, a whole body) | Notion connector: `notion-create-pages`, `notion-update-page` |
| Exact block edits (fix one heading, append blocks, a table built in code), properties in bulk, file uploads, trash, queries by date | Notion API through the `ntn` CLI (`ntn api <path>`) |

Whatever wrote it, **read the page back** before reporting success (§4). A call that returns
without error has not proven anything: the connector stores unsupported syntax as literal text,
silently.

## 1. Connector Markdown — the only syntax that renders (tested 26/10/2026)

The connector moved to "Markdown vNext". The authority is its spec: fetch
`notion://docs/notion-flavored-markdown-spec` with `notion-fetch` when something here doesn't
cover the case — never guess syntax.

| Want | Write | Never write (stored as literal text, or deprecated) |
|---|---|---|
| Heading with background color | `<h2 color="blue_bg">` ⏎ `Title` ⏎ `</h2>` | `## Title {color="blue_bg"}` — the `{color=…}` ends up in the title |
| Plain heading | `## Title` | |
| Synced block (original) | `<synced-block>` ⏎ children ⏎ `</synced-block>`, children **not** indented | `<synced_block>` with tab-indented children |
| Reference to an existing synced block | `<synced-block-reference url="…"></synced-block-reference>` (url copied from a fetched `<synced-block>`; never a page url) | |
| Callout | `<callout icon="🚫" color="gray_bg">` ⏎ `text` ⏎ `</callout>` | |
| Toggle heading with children | `<toggle heading="h2">` ⏎ `Title` ⏎ blank line ⏎ children ⏎ `</toggle>` | |
| Table | Pipe table (`\| a \| b \|` + `\| --- \| --- \|`); `<br />` for a line break inside a cell; `\|` for a literal pipe | mixing pipe rows and `<table>` |
| Styled table (colors, widths) | `<table header-row="true">` with `<tr>` / `<td>` | |
| Bold / italic | `**text**` / `*text*`; `<b>text</b>` when the styled text has edge spaces | |
| Separate blocks | A **blank line** between paragraphs | consecutive lines with no blank line — they merge into one paragraph |
| Empty paragraph | `<p />` | `<empty-block/>` |
| Link / page mention | `[text](https://…)` / `<mention url="https://app.notion.com/p/…" />` | |
| Date | `<date start="2026-10-26" />` | |

Escape literal characters in text with a backslash: `\< \> \{ \} \[ \] \$ \|` (and backtick).
Tags never written: `<div>`, `<details>`, `<small>`, `<sup>`, `<mark>` and any other HTML — they
are saved as text.

A `markdown_parser_warning` in the response (e.g. `deprecated_tag`, "was automatically
converted") means this section is out of date for that tag: fix the caller to the new form and
update this table.

## 2. API through `ntn`

Always wrap the call — a hung request otherwise blocks the session:

```bash
perl -e 'alarm 60; exec @ARGV' ntn api /v1/pages/<id> </dev/null
echo '<json>' | perl -e 'alarm 60; exec @ARGV' ntn api /v1/pages/<id> -X PATCH -d @-
```

| Need | How |
|---|---|
| Read a page's blocks | `GET /v1/blocks/<id>/children?page_size=100` (recurse on `has_children`) |
| Fix one block | `PATCH /v1/blocks/<block id>` with `{"heading_2": {"rich_text": [...], "color": "blue_background"}}` |
| Append blocks | `PATCH /v1/blocks/<id>/children` with `{"children": [...]}` — at most 100 per call |
| Create a page under a page | `POST /v1/pages` with `{"parent": {"page_id": …}, "properties": {"title": …}, "children": [...]}` |
| Query a database by date | `POST /v1/data_sources/<collection id>/query` with `{"filter": {"timestamp": "created_time", "created_time": {"on_or_after": "2026-10-26T00:00:00-03:00"}}}` |
| Remove a page | `PATCH /v1/pages/<id>` with `{"in_trash": true}` (recoverable for 30 days) |
| Upload a file | `ntn files create` → a `file_upload` id → a `pdf` / `file` block or a Files property |

Property gotchas:

- A **Status** property is written `{"status": {"name": "…"}}`, not `select` — the API answers
  "Status is expected to be status".
- A **new select option** is added by updating the data source with **every existing option plus
  the new one** (fetch first). Two writers adding options in parallel erase each other's: add
  options once, before the parallel writers run.
- Text values: at most 2000 characters per `rich_text` item; split longer text.
- Bulk writes: pause ~0.35 s between calls and retry with backoff on 429 / 5xx.
- Through the connector, dates are split: `date:<Prop>:start`, `date:<Prop>:is_datetime` (0/1).

## 3. Before writing

- Fetch the target first (page or data source): exact property names, existing options, current
  body. A database destination needs its `collection://` id, never the database page id.
- Read the workspace's own rules for that page (a workflow's page model, who may write where).
  This skill is mechanics only; it never authorizes a write the workspace's rules don't.

## 4. After writing — read back

Run the checker on every page you wrote:

```bash
python3 scripts/check_markup.py <page id> [<page id> …]
python3 scripts/check_markup.py --since 2026-10-26 <collection id> [<collection id> …]
python3 scripts/check_markup.py --tree <page id>          # the block tree, to eyeball a page
```

No shell (an agent with only the connector): `notion-fetch` the page instead — escaped syntax in the
result (`\{color=`, `\<synced`, `\<table`, a heading that ends in `{color="…"}`) means it rendered
as text.

The script lists blocks whose text still carries markup (`{color=`, `<synced`, `<table`, `<h2`, a
leading backslash…). `--fix` rewrites the commonest case in place — a heading with a literal
`{color="…"}` becomes a real colored heading. Anything else it finds: rewrite that section with
the syntax of §1 and check again. Report a write as done only when the checker comes back clean.

## What this skill never does

- Write to a page or database the workspace's rules keep read-only
- Delete permanently (trash only, and only what the task said to remove)
- Change a database schema to work around a property error without saying so
