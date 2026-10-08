---
name: application-email
description: Sends an application by email when a posting gives a recruiter address ("send your CV to …"). Use when job-intake routes to email, or when the user says "send an email to this recruiter", "apply by email", "mail my CV to". Builds the body from the profile's email template in the posting's language, attaches the CV through the profile's send command, and records the message id. Never sends through a connector that can't attach the CV.
---

# Application email

The text comes from the profile's templates; the sending goes through the profile's own command.
This skill is the **order** between the two.

## 1. Load

From `CAREER_PROFILE`: the index (send command, CV paths, languages), `rules.md`, `facts.md`
(only for the facts the template needs), and the template `templates/email.<lang>.html`.

**Language:** the posting's language; when the recruiter and the posting differ, the rule in
`rules.md` → Presentation decides. A recruiter in the candidate's own language with an
international project → attach **both** CVs.

## 2. Red flags — before writing

`rules.md` → Red flags. A personal mailbox, no company, a mismatch between role and company →
**show the draft and wait**, even when the profile grants autonomy for applications.

## 3. Build the body

- Fill the placeholders: `{first_name}` (the recruiter's, capitalized; "Hi," with no name when
  the posting gives only an address), `{relocation}` (only when the posting is in another
  country and the rule is `conditional`), `{role}` in the subject.
- **The body never mentions the post** ("I saw your post…"): the role goes in the subject; the
  body is the presentation. This is a rule of the profile, not a style choice.
- When the posting asks for specifics (location, visa status, rate, availability), add **one
  short block** with those answers, taken from `answers.md`. A requirement the candidate lacks
  and the posting marks as mandatory: name it honestly in one sentence, or leave it out — never
  claim it.
- When the posting **dictates a subject line**, use it verbatim.
- Write the HTML to the scratchpad (never inside the profile or a repo).

## 4. Send

Run the send command from the profile index with the HTML and the CV attachment(s). The
command prints the message id; keep it. A transient error (HTTP 5xx) → retry once after a few
seconds; a second failure → report, don't fall back to another sender.

**Never** use an email connector's `send` / `create_draft` for this: it can't carry the PDF, and
a CV sent as a link is a different thing from what the profile promised.

## 5. Record

`pipeline-keeper`, `EVENT: application`, channel `email`, external id = the message id. Then
hand the author to `linkedin-outreach` if `job-intake` hasn't already.

## Output

One line: `Email sent to <addr> (<lang>, CV <langs>) — id <id>`, plus the honest-gap sentence if
one was written, so the user knows what was said.
