---
name: code-review-analysis
description: Runs a round of code review analysis on a PR — gathers the new comments (Copilot or human, including suppressed ones), records them in the PR's review notes file, pre-analyzes each against the code, and drafts replies. Use when the user asks to go through a "new round" of review comments, to check suppressed comments, to "analisar o review do PR", or when starting the review notes of a new PR.
---

# Code review rounds

A PR's review lives in **one notes file**, accumulating every round. This skill is the fixed order
of a round, so no step gets lost in the rush.

## 1. Find (or create) the notes file

`CR-<PR number>-<short title>.md`, **inside the folder of the demand** the PR belongs to (the
project's `CLAUDE.md` or index of work says where demands live). Creating it is part of the flow —
no need to ask.

```markdown
# CR-123 — <PR title>

| PR | Review decision | Rounds | Open points |
|---|---|---|---|
| [#123](<url>) | CHANGES_REQUESTED | 2 | 3 |

## Round 1 — 29/09/2026 (Copilot)

| ID | GitHub ID | Comment | Reviewer | Difficulty | Status |
|---|---|---|---|---|---|
| 1 | 4082098880 | Add regression coverage for… | Copilot | Low | Fixed (a1b2c3d) |

### Analysis
**1** — what the comment claims, what the code shows, the call and why.

### Replies — ready to post
**1** — "Done in a1b2c3d."
```

A project can define its own format in its docs — then it wins.

## 2. The round, in this order

1. **Update the file if needed** — e.g. a reply from the previous round that was posted
2. **Gather the new points:**
   - Review comments: `kings git-prreview <PR>` (the table skeleton) or
     `gh api repos/<owner>/<repo>/pulls/<PR>/comments --paginate`
   - **Suppressed comments — always check, never skip:**
     `gh api repos/<owner>/<repo>/pulls/<PR>/reviews -q '.[] | select(.user.login | test("opilot")) | .body'`,
     looking for `<details><summary>Suppressed comments</summary>`. Separate duplicates from
     genuinely new points
   - Human reviewers: the **whole thread** (root and replies), not just the top comment
3. **The round's table**, IDs continuing from the last round
4. **Pre-analyze right away** — don't wait to be asked. Validate against the real code: open the
   cited file, count what must be counted. A confident comment is not a correct one
5. **Update the status table** at the top
6. **Project extra steps** — the project's `CLAUDE.md` may define more (e.g. a ticket field that
   follows the review state)
7. **Summary to the user:** how many points, which hold, the most serious one, what's decided and
   what still needs their call

## 3. Copilot before humans

Before the **first** human review request, check whether Copilot reviewed the current code. Once
human review is underway, a commit newer than Copilot's last review is **not** a pending item.

## 4. Human reviewer vs. Copilot

| Reviewer | Treatment |
|---|---|
| **Human** | Implement as asked, no debate. Reply: `Done because required (<commit>)` |
| **Copilot** | Full analysis — it may be right, partly right or wrong; pushing back is fine |

**In both cases, check against the style guide.** A comment that conflicts with a documented rule
is recorded in the round's table with a link to the rule — and for a human reviewer it's still
implemented as asked.

A project may define a different policy in its docs — then it wins.

## 5. Implement and reply

- Implement only what the pre-analysis (or the user's decision) confirmed
- Replies are **written in the notes file first**. Nothing is posted without the user having seen
  the text
- After posting: update the line's status (`Fixed (<commit>)` / `Declined — reason`) and move the
  reply from "ready to post" to "posted"
