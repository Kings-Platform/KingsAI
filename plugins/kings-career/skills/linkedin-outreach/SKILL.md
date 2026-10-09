---
name: linkedin-outreach
description: Sends a LinkedIn invitation with a note, or a DM to an existing connection, using the profile's templates. Use when job-intake asks to invite the author of a posting, when the user shares profile links ("connect with these", "send the note to"), when a recruiter accepted and a DM is due, or when a batch of recruiters needs the standard message. Respects the weekly invitation budget from the profile, queues what doesn't fit, and records every send in the pipeline. Never opens a profile page or a conversation that it doesn't need to.
---

# LinkedIn outreach

Two actions, both from the profile's templates: an **invitation with a note** (not yet
connected) and a **DM** (already connected). The texts are the profile's; this skill holds the
mechanics and the limits.

## 1. Load

From `CAREER_PROFILE`: the index (languages, invitation budget), `rules.md` → Outreach and Red
flags, the `invite` and `dm` texts from where `templates/README.md` says they live (unreadable →
stop and say so; never write the note from memory), and the Outreach table (the index names
its file).

## 2. Vet the list — before the first send

For each person: name, headline, degree. Get them **without opening the profile** (the
`/preload/custom-invite/?vanityName=<slug>` modal shows the name; the search or the post shows
the headline and degree).

| Finding | Action |
|---|---|
| Headline isn't recruiting / talent / hiring, and the person didn't post a role | Skip, say why — `rules.md` says who gets a note |
| Company or person on the profile's exclusion list | Skip |
| Already `1st` | DM route, never an invitation |
| Already in the pipeline's Outreach table | Skip (no second invitation; a DM only if the rule allows a follow-up) |

Show the vetted list only when the profile asks for it (`rules.md` → Autonomy); otherwise send.

## 3. Budget

Count the Outreach rows of kind `invite` in the **last 7 days**. Remaining = budget − count.
Send up to the remaining; the rest goes to the pipeline Queue as `queued: quota`, with the
slug, language and the date it can go.

LinkedIn's own limit is unpublished (~100 per rolling week, lower for accounts with many pending
or ignored invitations). When LinkedIn says the limit was reached: **stop**, queue everything
left, don't try again that day, don't work around it.

## 4. Send an invitation

Procedure and the tested script: [`scripts/invite.md`](scripts/invite.md). In short: open the
custom-invite preload URL for the slug, click "Add a note", insert the filled template with
`insertText`, send, read back the name from the dialog. **The "Connect" button next to a post's
author sends without a note** — never use it.

Language: from the person's headline language, or the posting's; default from the profile.
Note length: the profile's LinkedIn tier (300 characters with Premium, 200 without) — a longer
note fails silently.

## 5. Send a DM

Procedure: [`scripts/dm.md`](scripts/dm.md). From `/messaging/`, "New message", type the name,
pick the `• 1st` option, insert the template paragraph by paragraph. Reading the thread list is
fine; **opening a conversation marks it read** — only open the one you're writing in.

A reply to a recruiter is **not** this skill: that's `reply-drafter`, with approval.

## 6. Verify and record

After a batch, open `/mynetwork/invitation-manager/sent/` once and confirm the names are there
(the list paginates by scroll; load until every name of the batch appears). Then one
`pipeline-keeper` call per person, `EVENT: outreach`.

## Output

```
Invites: <n> sent, <n> queued (quota resets ~<date>), <n> skipped (<why>)
DMs: <n> sent
```

Plus the names, grouped by language.
