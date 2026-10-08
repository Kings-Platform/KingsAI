---
name: reply-drafter
description: Drafts a reply to a recruiter or hiring manager — a LinkedIn message, an email, a WhatsApp text — in the candidate's tone, from the profile's rules and facts. Use when the user says "X replied, prepare an answer", "how do I respond to this", or pastes a recruiter's message. Always shows the draft and sends only after the user approves; then records the exchange in the pipeline.
---

# Reply drafter

A reply is the one message the plugin **never sends on its own**. Draft, show, wait, send.

## 1. Read the whole thread

Not just the last message. Pull the thread from where it lives (the LinkedIn conversation, the
email thread through the read-only connector, the pasted text). Note: what they asked, what the
candidate already said, which role and which application id are involved (the pipeline has the
id — quote it in the reply when it helps the recruiter find the application).

## 2. Load the rules

`CAREER_PROFILE` → `rules.md` (Presentation, Never say), `facts.md` (Internal section: what
must not leak), `answers.md` (if they ask salary, availability, authorization).

## 3. Draft

- Same language as their message.
- Short: answer what was asked, add at most one useful fact (an application id, that relocation
  is on the table, a date), close warmly. No paragraph of self-presentation — they already have
  it.
- Honest about constraints that affect them **now** (location, visa, availability) — better
  said here than discovered by the recruiter later.
- Never: the Never-say list; a claim the facts don't support; "I saw your post".
- Offer **one** draft, with one line on why it's written that way (what it discloses and why).

## 4. Approval

Show the draft. The user may rewrite it entirely — send **their** text, verbatim, no
"improvements".

## 5. Send and record

LinkedIn: the DM procedure in `linkedin-outreach/scripts/dm.md`, in the existing thread. Email:
the profile's send command (or a reply through the connector **only** when no attachment is
needed and the profile allows it). Read the sent message back and quote its time.

`pipeline-keeper`, `EVENT: status` on the application row (`in-process`, with the next step), or
`EVENT: outreach` kind `reply` — each with the file the profile index names for that table.
