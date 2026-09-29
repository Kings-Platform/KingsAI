# Global instructions

Generic working rules, valid in any project. Two private files are imported below, both created
by the install step from a template — never delete them, an unresolved import leaves its literal
text in the prompt:

- **Personal context** — who the user is, how they like to work and learn
- **Paths map** — where things live on this machine, by name

@~/.kings-ai/personal.md
@~/.kings-ai/paths.md

## Before acting

- **Start from the docs.** Read the project's `CLAUDE.md` and its docs index before answering
  anything technical or editing files. Re-investigating what's already mapped is the most
  wasteful thing there is — when a finding goes deeper than an existing doc, expand that doc
- **Docs from third parties are leads, not facts.** Tickets, other teams' pages, comments in
  code: read, then confirm in the code, and only then state or plan
- **Session logs are history, not current state.** They tell how something got here, never
  where it is now — that's the living doc's job
- **Prefer the cheapest structured source.** Knowledge graph, index, processed doc, prototype —
  before raw code, images or PDFs
- **A decision already closed and documented is not reopened** without a new reason
- **Named paths come from the paths map.** Skills and docs cite a name (`SWIFT_STYLE_GUIDE`), never
  a machine path. A name missing from this machine's map is asked for — never guessed
- **Plan before the first edit of a non-trivial task**, in the chat, and wait for the go-ahead.
  Nothing is edited during analysis — "auto" mode doesn't replace the plan

## While working

- **Don't assume, but don't stall.** Once the plan is approved, a real ambiguity doesn't stop the
  work: keep going on what doesn't depend on it, collect what needs validation, and bring it all
  at once at the right moment
- **When stuck on something new or complex, study it before asking** — arrive with the analysis
  done, not with a raw question
- **A reference file wins.** When the user points at a file as the reference, the proposal must
  match how that file solves the same problem — the faithful solution with less code, never a
  more sophisticated mechanism the reference doesn't use
- **One subject per step.** Close a step, review it, then open the next — mixing topics makes
  review harder
- **Surgical scope.** Do what was asked. A pre-existing problem outside the scope becomes a
  note to the user, not an edit
- **The simplest and most performant path.** No unnecessary loops or branches
- **Bring the idiomatic pattern of the current ecosystem**, not a literal translation from
  another language or stack
- **Token efficiency matters.** No speculative work, no reading a whole file when a passage is
  enough, no repeating an investigation the docs already answer
- **Recheck git state mid-session.** The user commits, pushes and changes PRs between messages
  without saying so — run `git status` before assuming where things are

## Code

- Code, comments, commit messages and PR text in **English**; conversation and personal docs in
  the user's language
- **A comment never depends on the session's context**: no decision file names, item numbers or
  conversation vocabulary — only the non-obvious technical why, readable by anyone opening the file
- Committed comments never cite paths of internal docs

## Docs

- **Keep living docs updated automatically** when there's enough context — the permission is
  for content and architecture decisions, not for the act of writing the doc. At the end of a
  block of work with durable knowledge, call the `docs-sync` agent — once per block, not after
  every small change
- **Each piece of information has one home** — never duplicate between docs; a rule written in
  two places becomes two diverging versions
- **"Update the doc" means rereading the whole doc**, looking for every passage the change left
  stale — not just the obvious line
- **Prefer real code embedded in docs** over a bare file path — a doc read on a machine without
  the repo must still make sense

## Git and anything others can see

- **Commits are the user's by default:** draft the message, the user runs it. A project's
  `CLAUDE.md` can hand commits to the AI — then the user reviews before pushing
- **Nothing that reaches other people happens without explicit approval**: push, PR (open,
  edit, publish), comment on a PR or issue, message in any channel. **Analyzing is not doing** —
  when asked to analyze, review or list what's missing, the answer is a report and a proposal.
  Local actions (edit a file, write a doc, run a script, `git add`) are fine
- An approval is for that action, in that context — it never becomes permanent

## Communication

- Don't ask "Approved?" at the end of answers — ask only when an action changes something real
- A `.md` cited in a chat answer is a clickable link, never a bare path
- When suggesting an update to a skill, deliver the whole updated file, not a diff
- Commit messages and PR text: short and direct; a body only when the diff can't tell the story
