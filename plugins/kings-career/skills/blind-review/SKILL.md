---
name: blind-review
description: Gets a cold, honest read of the candidate's LinkedIn profile and/or CV from a recruiter's point of view — a reviewer agent that knows nothing about the candidate beyond the page, scores it against the target role and lists red flags, questionable claims and fixes by impact. Use when the user says "review my LinkedIn", "what would a recruiter think of my CV", "blind review", "run the blind analysis again", or after a profile or CV rewrite. Hands each artifact to the blind-reviewer agent; never edits the profile itself.
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

## Output

Per artifact: score and verdict (and the change since the last review). Then **one** plan for
all artifacts, ordered by impact: what, where, who decides. The reports' paths for the detail.

## What this skill never does

- Give the reviewer anything but the four inputs
- Edit the profile or the CV — the plan goes to the user first
- Turn a gap the facts don't support into a claim
