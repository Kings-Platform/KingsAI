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
| [templates/](templates/) | Your approved texts: invitation note, DM, application email, cover letter, in each language you apply in | `linkedin-outreach`, `application-email` |
| [pipeline.md](pipeline.md) | Every application and contact, one row each — the single place the plugin checks "did I already apply?" | `job-intake`, `pipeline-keeper`, `linkedin-outreach` |

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
| Cover letter files, one per language | `en: ~/Documents/CV/CoverLetter-en.pdf` |
| Public link to the CV (for messages that can't attach) | `https://…/CV-en.pdf` |
| Pipeline format | `markdown table` (or `csv`, `notion`) |
| LinkedIn weekly invitation budget you want to respect | `80` |

## How the plugin uses this profile

```
posting link ─► job-screener ─► job-intake ─┬─► ats-apply (form-filler)
                                              ├─► application-email
                                              ├─► linkedin-outreach
                                              └─► discard, with the reason
                                                        │
                                              pipeline-keeper ─► one row in pipeline.md
```

Each skill reads **rules.md first**, then only the page it needs. Nothing is sent that the
rules forbid, and nothing in the "always you" column of the autonomy table is done for you.
