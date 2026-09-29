---
name: pre-review
description: Runs the style-review agent on the current diff before the PR goes to human code review, then drives the fix cycle. Use when the user asks for a "style review", "pre-review", "check it against the style guide before sending", "revisão de estilo", or when closing a unit of work before taking a PR out of draft or asking for review.
---

# Pre-review

This skill holds **no rules** — they live in the project's style guide and conventions, which the
`style-review` agent knows how to load. Here is only the **cycle**: find the base, call the agent,
and what to do with the report.

> The point: keep coding as usual, and right before human review, fix what's already documented —
> no review comment about something the style guide covers.

## 1. Find the diff's base

1. The user gave it? Use it
2. No? The project's `CLAUDE.md` or its index of work (branch → base) may have it, or state the
   branching model (trunk-based from `main`)
3. Still unknown? **Stop and ask.** Never assume a base

## 2. Call the `style-review` agent

Pass the base. It loads the standard, reports findings by severity and **edits nothing**.

## 3. Deliver the report and wait

Show the report as it comes — findings, questions, what was left out on purpose. **Apply nothing
yet**: the user reviews it first.

## 4. Apply only what the user approves

When the user says which points to apply (by number, "all of them"…), edit **only those**, in the
main session. An approved finding is the finding as reported — not an invitation to improve
anything around it. A rejected or postponed point is decided: don't insist.

## 5. End of the cycle

Done when the approved points are edited. No commit, no push, no PR change, no remote comment —
those follow the project's git rules.
