---
name: blind-review
description: Gets a cold, honest read from a recruiter's point of view — of the candidate's LinkedIn profile and CV, or of the messages they send (connection note, DM, reply to a recruiter, application email, and the templates behind them). A reviewer agent that knows nothing about the candidate beyond what's in front of it scores the artifact against the target role and lists red flags, questionable claims and fixes by impact. Use when the user says "review my LinkedIn", "what would a recruiter think of my CV", "review my templates", "would a recruiter answer this?", "blind review", or after a profile, CV or template rewrite. Hands each artifact to the blind-reviewer agent; never edits anything itself.
---

# Blind review

The value of this review is that the reviewer is **blind**: it sees the profile the way a
stranger does. Everything this skill hands it must keep it that way.

| Step | Who |
|---|---|
| Resolve what to review and for which role | This session |
| Read and judge, one artifact per call | `blind-reviewer` agent (Opus) |
| Reconcile the findings with the facts, build the plan | This session |

## 1. Load

From `CAREER_PROFILE` → index: `Target roles`, `LinkedIn profile URL`, `CV files` and
`Blind reviews folder` (and `Blind review target`, when set). The user may narrow it ("only the LinkedIn", "the pt CV").

- `TARGET`: the user's words when they name a role; otherwise one line built from `Target
  roles` plus the seniority and market the index states (e.g. "Senior iOS engineer, remote,
  international"). It describes the **job**, never the candidate.
- Missing URL or CV path → ask; never guess one.

## 2. Hand off — blind by construction

The agent gets exactly four things: `TARGET`, `SOURCES`, `REPORT_LANG` (the user's language) and
`OUT` (`<Blind reviews folder>/blind-review-<artifact>-<yyyy-mm-dd>.md`; no folder set → the
session's scratchpad). **Never** pass the candidate's facts, rules, previous reviews, notes about
what changed, or what the user hopes to hear — that would teach the reviewer what to look for.

A profile URL goes with `?locale=<code>` for the language a recruiter of `TARGET` reads
(international → `en_US`; a local market → its language, e.g. `pt_BR`). The browser is logged in
as the owner, and without it LinkedIn renders the owner's language, not the recruiter's. A target
covering two markets → one review per locale.

Calls, in parallel:
- one per artifact (the profile URL; each CV file);
- one cross-check with the profile URL **and** the main CV together, when both are in scope.

## 3. Reconcile — here, not in the agent

Now, with the profile's `facts.md` open, read each report and sort every finding:

| Kind | Meaning | Becomes |
|---|---|---|
| Real problem | The page shows something wrong or confusing | A fix |
| True but not shown | The facts support it; the page doesn't make it visible | A fix: show it |
| Reviewer misread | The page is right; the reviewer read it wrong | Nothing — but note it: a recruiter may misread the same way |
| Asks for something the candidate lacks | A keyword or claim the facts don't support | Never a fix — the profile doesn't claim what isn't true |

Compare with the previous review in the same folder, when there is one: score moved, what was
fixed, what's new.

## Messages

Same blindness, a different artifact: what a recruiter **receives**.

**Which messages:** the profile's templates (`templates/README.md` → each text and language, read
the way its row says), or one message the user or another skill hands over (a reply drafted by
`reply-drafter`, an email about to go out).

**Make it arrive as it would.** Fill every placeholder with a plausible value — a first name, a
role, a company, the CV link the profile index gives — so the reviewer reads a message, not a
template. Drop the optional paragraphs a real send would drop (a relocation paragraph only for a
posting abroad). Say in the report which values were invented.

**Hand-off** — one `blind-reviewer` call per message, in parallel, with `KIND: message`, the
message as `SOURCES`, `CHANNEL`, and a `CONTEXT` that holds only what the recipient has:
- `invite` / `dm`: the recipient's title (a tech recruiter, unless the user says otherwise);
- `reply`: the recipient's own message the text answers;
- `email`: the posting (a real recent one from the pipeline, or a sample of the target role) and
  which attachments go with it;
- optionally the candidate's profile URL with the locale of the message's language.

`TARGET`, `REPORT_LANG` and `OUT` as above; `OUT` is `blind-review-<text>-<lang>-<date>.md`.

**Reconcile** the same way (real problem · true but not shown · misread · not a fit). A fix to a
template goes to the user as a proposal: the templates are the user's to edit.

## Output

Per artifact: score and verdict (and the change since the last review). Then **one** plan for
all artifacts, ordered by impact: what, where, who decides. The reports' paths for the detail.

## What this skill never does

- Give the reviewer anything but the four inputs
- Edit the profile or the CV — the plan goes to the user first
- Turn a gap the facts don't support into a claim
