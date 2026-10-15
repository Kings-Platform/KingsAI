# Career profile

<!-- Copy this folder to the path CAREER_PROFILE resolves to (default: ~/.kings-ai/career/). -->
<!-- Private: it holds your personal data. Never commit it to a public repo. -->

This is the **index** of your career profile. The `kings-career` plugin reads it first, then the
page it needs for the task. Every skill and agent of the plugin takes its facts, rules and texts
**from here, never from its own memory** — so when something changes, change it here, once.

## Pages

| Page | What it holds | Read by |
|---|---|---|
| [facts.md](facts.md) | Who you are **as the outside should see it**: experiences, education, links, application contacts, CV paths | Everything that writes about you |
| [rules.md](rules.md) | How to present you, what never to say, who not to contact, red flags, and where you override the plugin's default autonomy | Everything, before acting |
| [answers.md](answers.md) | Your answer bank for application forms: salary, work authorization, relocation, start date, degree… | `ats-apply`, `form-filler` |
| [templates/](templates/) | Your approved texts — invitation note, DM, application email, cover letter, relocation sentence — in each language; its README says where each one lives (a file here, or another source) | `linkedin-outreach`, `application-email` |
| [pipeline.md](pipeline.md) | Outreach and queue, one row each — and the applications too, unless the pipeline format is `notion` | `job-intake`, `pipeline-keeper`, `linkedin-outreach` |
| [sources.md](sources.md) | The job sources you sweep: search terms, frequency, the catalog sources you use, your own sources (company boards, people's lists) and companies to watch | `job-sweep` |
| [notion.md](notion.md) | Only with `Pipeline format: notion`: the two databases (ids), property and mapping rules, page model, status updates, the options in use, the plan-file shape | `opportunity-log`, `opportunity-analyst`, `opportunity-writer`, `inbox-triage`, `reply-drafter` |

## Settings

Fill the right column. A skill that finds a setting empty **asks you** — it never guesses.

| Setting | Value |
|---|---|
| Languages you apply in, in order of preference | `en, pt` |
| Default language when the posting doesn't say | `en` |
| Target roles (what a posting must be about to be worth screening) | `iOS / mobile engineer` |
| Where you live, as written in forms | `City, Country` |
| Time zone | `UTC-3` |
| Email account used for applications | `you@example.com` |
| How to send an application email with an attachment | `~/path/to/send-email --to <addr> --subject <s> --body <html> --attach <pdf>` |
| Email reading tool (connector or client), read-only | `Gmail connector` |
| CV files, one per language | `en: ~/Documents/CV/CV-en.pdf` · `pt: ~/Documents/CV/CV-pt.pdf` |
| LinkedIn profile URL (public link, for the blind review) | `https://www.linkedin.com/in/<slug>/` |
| Blind reviews folder (where blind-review saves its reports) | `~/Documents/career/reviews/` |
| Blind review target (the job the reviewer hires for, when the user names none) | `Senior iOS engineer, remote` |
| Cover letter files, one per language | `en: ~/Documents/CV/CoverLetter-en.pdf` |
| Public link to the CV (for messages that can't attach) | `https://…/CV-en.pdf` |
| Pipeline format | `markdown table` (or `csv`, `notion`) |
| Applications table | `pipeline.md` (or a pre-existing log; the keeper appends in its columns) — with `notion`: the Notion page below |
| Notion page (with `Pipeline format: notion`) | `notion.md` |
| Outreach table (the weekly budget is counted here) | `pipeline.md` |
| Queue table | `pipeline.md` |
| LinkedIn weekly invitation budget you want to respect | `80` |
| Sources page (job sources to sweep and how often) | `sources.md` |
| Site notes (selectors, traps and quirks of specific job sites and company careers pages) | `sites.md` (or any notes file) |

## How the plugin uses this profile

```
posting link ─► job-screener ─► job-intake ─┬─► ats-apply (form-filler)
                                              ├─► application-email
                                              ├─► linkedin-outreach
                                              └─► discard, with the reason
                                                        │
                                   ┌────────────────────┴────────────────────┐
                                   │ markdown                                │ notion
                        pipeline-keeper ─► one row in pipeline.md    opportunity-log ─► opportunity page
                                                                                     + application page
```

Each skill reads **rules.md first**, then only the page it needs. Nothing is sent that the
rules forbid, and nothing in the "always you" column of the autonomy table is done for you.
