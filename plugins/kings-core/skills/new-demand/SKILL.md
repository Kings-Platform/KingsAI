---
name: new-demand
description: Opens a new demand (task, feature, epic stage) the same way every time — from the inputs to the demand's doc with its Timeline and the approved plan. Use when the user says "let's start the demand X", "vamos iniciar a demanda", "nova demanda", "pega o card …", or opens a new stage of an existing epic. Not for resuming a demand that's already in the index of work — then just read its doc.
---

# New demand

This skill holds **no rules** — they live in the global instructions, the project's `CLAUDE.md`
and its docs standard. Here is only the **order** in which they apply when a demand is born.

> Every demand starts the same way, and its doc — with the **Timeline** — is born on day one, not
> at the end. That doc is what a future session reads to resume, and what `docs-sync` later checks
> the delivery against.

## Where things live

The project's `CLAUDE.md` says where the index of work and the demand docs are. When it doesn't,
the default standard is:

| Content | Home |
|---|---|
| Index of work — roadmap, in progress, done (with the release), backlog | `demandas/README.md` |
| A demand that lasts several sessions | `demandas/<name>/README.md` + `implementation/` (one doc per subject) |
| Provisional decisions during the demand | `demandas/<name>/decisoes/` — exported to `style-guide/` when it closes |
| Studies and prototypes | `pocs/` |

All inside the project's docs folder (`.ai/`, or `docs/` where that's the convention). The full
version of this default is the named path `DOCUMENTATION_STANDARD`, when it resolves on this
machine.

## 0. What counts as starting

The day the user says "let's start demand X" **is the kickoff** — first Timeline line, with
today's date. Same for a new stage of an existing epic (the Timeline is the stage's, and the
epic's README gets its line).

Not a kickoff: resuming a demand that already has a doc and a line in the index — read the doc and
continue. Unsure? Check the index (including the backlog, which may hold prior study) before asking.

## 1. Inputs — ask for everything at once

Check what already came and ask **in a single message** for what's missing. Never start digging
into code with an input missing, only to come back with one more question.

| Input | Notes |
|---|---|
| **Ticket / card** | A lead, not a fact — scope and behavior are validated in the code and with the user |
| **Design** | `.fig` file (skill `fig-layout`) or link |
| **Reference file** | The proposal must match how it solves the same problem, with less code |
| **Epic stage?** | The epic's README gives context and previous stages |
| **Other systems touched** (backend, third parties) | Their docs, if the project keeps them |

## 2. Context — before giving an opinion

1. The docs index → the topic's living doc. Architecture already mapped comes before any grep
2. A code graph, if the project has one (`kings graph deps`/`impact`) — a starting point, confirmed
   in the code
3. Before proposing a new type, model or component: look for an existing one with the same
   meaning, and at the style guide's index

## 3. Where the code runs

Propose the repo (or clone), the branch name and its **base**, following the project's branching
rules — never assume the base. Who creates the branch follows the project's git rules (by default,
the user). The base goes into the demand's doc at the same moment.

## 4. Initial record — before coding

The request to start the demand **is** the go-ahead for its doc. Create, in this order:

1. **The demand's doc**, following the project's template (or the default above): context, ticket,
   branch + base, status, **`## Timeline` already with the kickoff line**, then the sections
2. **Its line in the index of work**, "in progress", with the initial status
3. **Any other place the project tracks status** (a module summary, a docs index)
4. `kings docs-check`, when available

Status must match across every place it lives.

## 5. Action plan

Investigate the code, write the plan in steps in the chat, wait for the go-ahead, only then edit.
**The approved plan goes into the demand's doc** — it's against it that `docs-sync` later records
"plan A → decision B". A plan that stays in the chat is lost.

Scope is the one validated with the user, nothing more. A decision taken for future testability is
stated as such.

## 6. Along the demand

| Moment | What happens | Recorded in |
|---|---|---|
| PR opened (draft, as early as possible) | Title and description drafted in English | Index + Timeline |
| Before leaving draft | Skill `pre-review` | — |
| Each review round | Skill `code-review-analysis` → `CR-<PR>.md` in the demand's folder | Timeline (who, date, how many points) |
| End of a block with durable knowledge | Agent `docs-sync` — once per block, not per small fix | Demand doc + index |
| Design or QA validation, hold, resume | **Only the user knows** — ask when closing a block and pass it to `docs-sync` | Timeline |
| Delivery | Status in every place; provisional decisions exported to the style guide | — |

## 7. What this skill doesn't do

Create branches, commit or touch PRs (unless the project's git rules say so), widen the scope
beyond what was validated, or create convention docs — that's the delivery flow, not the opening.
