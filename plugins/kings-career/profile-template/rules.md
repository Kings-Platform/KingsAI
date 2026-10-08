# Rules

<!-- The plugin's skills read this page BEFORE any action. Keep it short and explicit. -->
<!-- One rule, one line, one place: a rule written twice diverges at the first change. -->

## Presentation

How any text about you is written (email, note, DM, form answer, cover letter):

- Tone:
- Never claim:
- Don't lead with:
- Name the current employer in outreach? `yes / no`
- Relocation: `never` / `conditional` (the exact sentence lives in `templates/`) / `open`
- When the posting language differs from the recruiter's, write in:

## Never say

Facts the outside must not see, phrased as rules the skills can check:

-

## Targeting

What a posting must be, or must not be, for the plugin to act on it:

| Criterion | Rule |
|---|---|
| Role focus | |
| Stacks to skip | |
| Industries to skip | |
| Work mode | `remote` / `hybrid in <city>` / `relocation ok` |
| Countries that require a local permit you don't have | `apply with "sponsorship: yes"` / `skip` |
| Seniority mismatch (posting asks for more years than you have) | `apply anyway` / `ask first` / `skip` |

## Outreach

| Rule | Value |
|---|---|
| Who gets an invitation note | `tech recruiters and the person who posted a role` |
| Who never gets a message | companies or people to exclude |
| Already connected | `DM, never a second invitation` |
| A posting link always means | `apply + invite the author (nothing if already connected)` |
| Mention the posting in the note or email? | `no — the note only presents you; the role goes in the email subject` |
| Follow-up on an unanswered message | `no` / `after N days` |

## Red flags — stop and show the user before sending

- Recruiter writes from a personal mailbox (Gmail, Hotmail…) for a company role
- The posting names no company, or the "disclaimer" says it represents none
- The role and the company don't match
- "Comment your email" / "DM me your resume" posts with dozens of replies
- A platform you decided not to use:

## Autonomy overrides

The plugin's defaults are in its README. Override here only what differs for you.

| Action | Your setting |
|---|---|
| Submit applications (forms and emails) without per-item approval | `yes` / `no` |
| Send invitation notes with the standard text | `yes` / `no` |
| Reply to a recruiter | `always show first` |
| Salary outside the bank in `answers.md` | `ask` |
