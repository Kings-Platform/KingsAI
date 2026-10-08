# kings-career

Job search as an **operation**, not a conversation: a posting link comes in, a screened, applied
and recorded result comes out — with the human only where the human is needed.

Everything personal lives **outside** the plugin, in the candidate's profile, found through the
named path `CAREER_PROFILE` (default `~/.kings-ai/career/README.md`). The plugin holds the
procedures; the profile holds the facts, the rules, the texts and the pipeline.

#### Index

- [Components](#components)
- [Flow](#flow)
- [Autonomy](#autonomy)
- [The profile](#the-profile)
- [Setup](#setup)

## Components

| Component | Type | What it does |
|---|---|---|
| [`job-intake`](skills/job-intake/SKILL.md) | Skill | Entry point for a posting link: screens, checks the pipeline for duplicates, measures fit against the rules, picks the route |
| [`ats-apply`](skills/ats-apply/SKILL.md) | Skill | Applies through an ATS form (Greenhouse, Lever, Ashby, Workday…) with a playbook per platform and the profile's answer bank |
| [`application-email`](skills/application-email/SKILL.md) | Skill | Applies by email: template, CV attached, sent through the profile's send command |
| [`linkedin-outreach`](skills/linkedin-outreach/SKILL.md) | Skill | Invitation with note or DM, from the templates, within the weekly budget |
| [`reply-drafter`](skills/reply-drafter/SKILL.md) | Skill | Drafts a reply to a recruiter in the profile's tone — sent only after approval |
| [`inbox-triage`](skills/inbox-triage/SKILL.md) | Skill | Reads recent email, classifies (rejection, confirmation, action for the user), updates the pipeline |
| [`interview-prep`](skills/interview-prep/SKILL.md) | Skill | Likely topics, STAR stories with numbers, audio scripts — for a test, an AI screening or an interview |
| [`job-screener`](agents/job-screener.md) | Agent | Reads a posting or post (follows the redirect) and returns a structured card — read-only browser |
| [`form-filler`](agents/form-filler.md) | Agent | Fills and submits one ATS form from a playbook and the answer bank; returns "sent" or "pending: X" |
| [`pipeline-keeper`](agents/pipeline-keeper.md) | Agent | The only writer of the pipeline: one row per action, always the same shape |

## Flow

```
posting link
    │
    ▼
job-screener (agent) ──► card: company, role, location, mode, requirements, contact, channel, flags
    │
    ▼
job-intake (skill) ──► already in the pipeline? fit by the rules? route?
    │
    ├──► ats-apply ──► form-filler (agent) ──► sent / pending-user
    ├──► application-email ──► email with CV, through the profile's command
    ├──► linkedin-outreach ──► invite the author (or nothing, if already connected)
    └──► discard, with the reason
    │
    ▼
pipeline-keeper (agent) ──► one row in the profile's pipeline
```

The user sees **one line per link**, plus what only they can do.

## Autonomy

Defaults. The profile's `rules.md` overrides them per candidate.

| Action | Default |
|---|---|
| Read a posting, decide the route, record it | Automatic |
| Submit an application (form or email) | Automatic once the profile grants it; otherwise show first |
| Invitation with the standard note | Automatic, within the weekly budget |
| Reply to a recruiter | Draft shown first, always |
| Create an account, log in, solve a CAPTCHA, type a document number | Always the user |
| Technical test, audio, video, interview | Always the user — the plugin prepares, never impersonates |
| Salary outside the answer bank | Ask |
| Posting with a red flag | Stop and show |
| Work around a blocked tool or a platform limit | Never — report and queue |

## The profile

The contract every skill depends on. The template ships with the plugin:
[`profile-template/`](profile-template/README.md).

| Page | Holds |
|---|---|
| `README.md` | Index + settings: languages, CV paths, send-email command, pipeline format, invitation budget |
| `facts.md` | The external version of who the candidate is; an "Internal" section for what must never leak |
| `rules.md` | Presentation, never-say, targeting, outreach, red flags, autonomy overrides |
| `answers.md` | The form answer bank |
| `templates/` | Approved texts per language, with placeholders |
| `pipeline.md` | Applications, outreach and the queue of blocked items |

Skills **read** the profile and **never** copy its content into themselves. A rule lives in one
place; when it changes, the skills don't.

## Setup

```bash
# 1. Install the plugin (see the marketplace README)
claude plugin install kings-career@kingsai --scope user

# 2. Create your private profile from the template
cp -r <KingsAI>/plugins/kings-career/profile-template ~/.kings-ai/career

# 3. Point CAREER_PROFILE elsewhere only if you keep the profile in another place
#    (~/.kings-ai/paths.md, one row: | `CAREER_PROFILE` | `~/other/place/README.md` |)
```

Then fill the profile. A skill that hits an empty setting asks for it; it never guesses.

Browser work (LinkedIn, ATS forms) needs a browser tool the user is logged into, such as Claude
in Chrome. Sending email needs a local command that can attach a file (the profile index names it).
