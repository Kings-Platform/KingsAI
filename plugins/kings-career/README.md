# kings-career

Job search as an **operation**: a posting link comes in, a screened, applied and recorded
result comes out, with the human only where the human is needed.

Everything personal lives **outside** the plugin, in the candidate's profile, found through the
named path `CAREER_PROFILE` (default `~/.kings-ai/career/README.md`). The plugin holds the
procedures; the profile holds the facts, the rules, the texts and the pipeline.

Flow, autonomy, requirements and setup: [wiki](https://github.com/Kings-Platform/KingsAI/wiki/kings-career).

## Components

| Component | Type | What it does |
|---|---|---|
| [`job-intake`](skills/job-intake/SKILL.md) | Skill | Entry point for a posting link: screens, checks the pipeline for duplicates, measures fit against the rules, picks the route |
| [`ats-apply`](skills/ats-apply/SKILL.md) | Skill | Applies through an ATS form with a [playbook per platform](skills/ats-apply/playbooks/) and the profile's answer bank |
| [`application-email`](skills/application-email/SKILL.md) | Skill | Applies by email: template, CV attached, sent through the profile's send command |
| [`linkedin-outreach`](skills/linkedin-outreach/SKILL.md) | Skill | Invitation with note or DM, from the templates, within the weekly budget |
| [`reply-drafter`](skills/reply-drafter/SKILL.md) | Skill | Drafts a reply to a recruiter in the profile's tone — sent only after approval |
| [`inbox-triage`](skills/inbox-triage/SKILL.md) | Skill | Reads recent email, classifies it, updates the pipeline |
| [`interview-prep`](skills/interview-prep/SKILL.md) | Skill | Topics, STAR stories, audio scripts — prepares, never impersonates |
| [`job-screener`](agents/job-screener.md) | Agent | Reads a posting and returns a structured card — read-only browser |
| [`form-filler`](agents/form-filler.md) | Agent | Fills and submits one ATS form from a playbook and resolved answers |
| [`pipeline-keeper`](agents/pipeline-keeper.md) | Agent | The only writer of the pipeline: one row per action |

## The profile

The contract every skill depends on. The template ships here:
[`profile-template/`](profile-template/README.md) — copy it to where `CAREER_PROFILE` points
and fill it. Skills **read** the profile and **never** copy its content into themselves: a rule
lives in one place.
