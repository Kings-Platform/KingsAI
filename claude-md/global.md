# Global instructions

Generic working rules, valid in any project. Personal context (who the user is, how they like to
work and learn) lives in a private file, imported below — it's optional and may not exist.

@~/.kings-ai/personal.md

## Before acting

- **Start from the docs.** Read the project's `CLAUDE.md` and its docs index before answering
  anything technical or editing files. Re-investigating what's already mapped is the most
  wasteful thing there is — when a finding goes deeper than an existing doc, expand that doc
- **Docs from third parties are leads, not facts.** Tickets, other teams' pages, comments in
  code: read, then confirm in the code, and only then state or plan
- **Prefer the cheapest structured source.** Knowledge graph, index, processed doc, prototype —
  before raw code, images or PDFs
- **A decision already closed and documented is not reopened** without a new reason
- **Bring the idiomatic pattern of the current ecosystem**, not a literal translation from
  another language or stack

## While working

- **Don't assume, but don't stall.** With a real ambiguity, keep going on what doesn't depend on
  it, collect what needs validation, and bring it all at once at the right moment
- **When stuck on something new or complex, study it before asking** — arrive with the analysis
  done, not with a raw question
- **One subject per step.** Close a step, review it, then open the next — mixing topics makes
  review harder
- **Surgical scope.** Do what was asked. A pre-existing problem outside the scope becomes a
  note to the user, not an edit
- **The simplest and most performant path.** No unnecessary loops or branches
- **Token efficiency matters.** No speculative work, no reading a whole file when a passage is
  enough, no repeating an investigation the docs already answer

## Code

- Code, comments, commit messages and PR text in **English**; conversation and personal docs in
  the user's language
- **A comment never depends on the session's context**: no decision file names, item numbers or
  conversation vocabulary — only the non-obvious technical why, readable by anyone opening the file
- Committed comments never cite paths of internal docs

## Docs

- **Keep living docs updated automatically** when there's enough context — the permission is
  for content and architecture decisions, not for the act of writing the doc. At the end of a
  block of work with durable knowledge, call the `docs-sync` agent
- **Each piece of information has one home** — never duplicate between docs; a rule written in
  two places becomes two diverging versions
- **Prefer real code embedded in docs** over a bare file path — a doc read on a machine without
  the repo must still make sense
- A `.md` cited in a chat answer is a clickable link, never a bare path

## Anything others can see

**Nothing that reaches other people happens without the user's explicit approval**: commit,
push, PR (open, edit, publish), comment on a PR or issue, message in any channel. **Analyzing is
not doing** — when asked to analyze, review or list what's missing, the answer is a report and a
proposal. Local actions (edit a file, write a doc, run a script) are fine.

- Don't ask "Approved?" at the end of answers — ask only when an action changes something real
- When suggesting an update to a skill, deliver the whole updated file, not a diff
