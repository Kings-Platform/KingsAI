# Sources catalog

Public job sources anyone can sweep, with how to reach them **without guessing**. `{query}` is a
search term from the profile (`iOS`, `Swift`, `Android`, `React`…), `{location}` a location term
(`Brazil`, `LATAM`, `remote`). The profile picks which of these it uses and adds its own.

Each entry: **access** (how the sweeper reads it), **login**, **cost**, **open check** (how to be
sure a role is still open) and **notes** (what it tends to return, traps).

Observed state is dated; a source that changed gets its entry updated, not a note elsewhere.

## Aggregators with an API or a predictable search URL

| Source | Access | Login / cost | Open check | Notes |
|---|---|---|---|---|
| remotar.com.br | `https://api.remotar.com.br/jobs?search={query}` | no / free | Follow the job's apply link | Brazilian market, few USD roles |
| vagaslume.tech | `https://www.vagaslume.tech/api/vagas?search={query}` | no / free | Follow the original link (often LinkedIn or Telegram) | Aggregates ~24 sources. Since 10/2026: redirects to `www.`, filter is `search=` (`q=` ignored), some terms fail after page 1 |
| trulyremotework.com | Sitemap `https://trulyremotework.com/sitemap-jobs/1.xml`, then each job page | no / free | The page links the ATS — check there | Small, filters worldwide eligibility, links the ATS directly |
| Working Nomads | `https://www.workingnomads.com/jobsapi/_search?q=title:{query}` | no / free | ATS link | Mostly US/EU |
| Himalayas | `https://himalayas.app/jobs/api/search?q={query}&sort=recent&page=N` | no / free | ATS link | Job pages sit behind Cloudflare; the API carries the description. Location tags can be wrong — read the text |
| Jobgether | HTML of `https://jobgether.com/remote-jobs/{query}` lists offers; each offer's JSON-LD has company and ATS link | no / free | ATS link | Offer date = first 8 hex chars of the offer id (Unix time) |
| DailyRemote | Public listing for `{query}` | no / company and link behind Premium | Find the role on the company's ATS | High volume; use as a lead only |
| Remote.co | Listing | Paid for details | — | Title and location only without a plan |
| UnlockCareer | Public company pages `https://unlockcareer.ai/jobs/<company>`; list via `https://unlockcareer.ai/sitemap.xml` | Search is paid | ATS link | US→LATAM; check the sitemap for new companies |
| WordPress job blogs | `https://<site>/wp-json/wp/v2/<post-type>?search={query}` | no / free | Follow the "apply" link | Many reposts of old roles — check the date at the destination |

## Talent platforms (profile-based; the user is logged in)

Checked in the user's browser, in their own tab. The sweeper reads the role list; it never edits
the profile and never applies.

| Source | Where the roles are | Notes |
|---|---|---|
| Wellfound | `https://wellfound.com/jobs` (filters: role, remote, location) | Mostly US/India; recruiters also message here |
| Arc.dev | `https://arc.dev/dashboard/d/full-time-jobs/browse` and the freelance list | Shows fit and pay band |
| Lemon.io | `https://me.lemon.io/open-projects` | Projects, not postings |
| Revelo | `https://app.careers.revelo.com/home` → Jobs | US companies hiring in LATAM |
| Turing, Strider, Flexiple | Each platform's dashboard | Mostly inbound matching; check for invitations |

## ATS-domain search

Search for `{query}` roles **inside an ATS's domain** to discover companies, then read the
company's board through the ATS's public API.

- **How:** a web search restricted to the ATS domain. If the search tool ignores `site:`, use its
  domain filter (e.g. `allowed_domains`).
- **Freshness (tested 10/2026):** the search index lags. Ashby and SmartRecruiters returned mostly
  live roles. Lever, Gupy and Greenhouse returned mostly closed ones. Workable, Breezy and
  Recruitee were mixed. Teamtailor and Personio returned little. **Always** confirm each hit with
  the API below before reporting it.
- **Best use:** the company list. A company hiring the target remotely is worth reading in full
  through its board API, even when the hit itself is closed.

| ATS | Domain | Open check / full board |
|---|---|---|
| Greenhouse | `job-boards.greenhouse.io`, `boards.greenhouse.io` | `https://boards-api.greenhouse.io/v1/boards/<board>/jobs/<id>` (404 = closed); board: `/v1/boards/<board>/jobs?content=true` |
| Lever | `jobs.lever.co` | `https://api.lever.co/v0/postings/<company>/<id>`; board: `/v0/postings/<company>` |
| Ashby | `jobs.ashbyhq.com` | `https://api.ashbyhq.com/posting-api/job-board/<company>` (id listed = open) |
| Workable | `apply.workable.com` | `https://apply.workable.com/api/v1/widget/accounts/<account>` |
| SmartRecruiters | `jobs.smartrecruiters.com` | The posting page (closed shows "no longer available"); old roles can stay listed — check the date |
| Recruitee | `<company>.recruitee.com` | `https://<company>.recruitee.com/api/offers/` |
| Teamtailor | `<company>.teamtailor.com` | `https://<company>.teamtailor.com/jobs` |
| Breezy | `<company>.breezy.hr` | The posting page |
| Gupy | `<company>.gupy.io` | The posting page (status shown); mostly Brazil |
| InHire | `<tenant>.inhire.app` | `https://api.inhire.app/job-posts/public/pages` with header `X-Tenant: <tenant>` |

## Lists from people (curated, posted on LinkedIn or a blog)

People who post roles regularly for a stack — a hiring newsletter, a recruiter's weekly list, a
community board — are often the earliest source. They are **profile-only** (the catalog doesn't
name people): list them in the profile with the URL and how to read them (public page, API,
members-only).
