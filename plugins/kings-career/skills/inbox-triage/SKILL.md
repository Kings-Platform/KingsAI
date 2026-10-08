---
name: inbox-triage
description: Reads the recent email of the candidate's application account and sorts it — rejections, application confirmations, interview or test invitations with deadlines, account activations and other actions only the user can take, and noise — then updates the pipeline. Use when the user says "check my email", "any news", "what came in", "update everything from the inbox", or on a schedule. Read-only on the mailbox; never clicks an activation link, never replies.
---

# Inbox triage

## 1. Load

`CAREER_PROFILE` index: the application email account and the reading tool. The pipeline path.

## 2. Read

Search the last N threads (default: 2 days, or the window the user gives)
with the read-only tool. Subject and snippet are usually enough; open the body only for
invitations, tests and anything with a deadline.

## 3. Classify

| Class | Signals | Pipeline action |
|---|---|---|
| **Rejection** | "not moving forward", "other candidates", "não seguiremos" | `status` → `rejected` |
| **Confirmation** | "application received", "thank you for applying", ATS no-reply | `status` → `confirmed` (only if the row is `sent`) |
| **Process** | interview slot, test link, screening, "next steps" | `status` → `in-process`, next step with the **deadline** |
| **Action for the user** | activate account, verify email, complete profile, sign a form | `queue` row, owner = user |
| **Recruiter message** (a person writing) | a real name, a question | Hand to `reply-drafter`; don't answer here |
| **Noise** | newsletters, platform marketing, "your profile is incomplete" from a platform the user dropped | Nothing |

A confirmation for an application that isn't in the pipeline → say so; it's a missing row, not
a mystery.

## 4. Report

```
Rejections: <company — role> …
Confirmed: …
In process: <company — what, by when> …
Your action: <what, where> …
Noise: <n> skipped
```

Deadlines first. One line each. Nothing is clicked for the user: activation and verification
links are theirs.
