#!/usr/bin/env python3
"""List the open jobs of one ATS board, normalized, so a sweeper reads every board the same way.

  ats_list.py <board URL or the source's method text> [--terms "ios,swift"] [--since YYYY-MM-DD]

The first argument is the source's URL (job-boards.greenhouse.io/<slug>, jobs.lever.co/<slug>,
<slug>.gupy.io, <tenant>.inhire.app…) or, when that is a company page, its method text ("Como
buscar"), where the API URL or the tenant header is written. Prints one JSON object:

  {"ats": "...", "board": "...", "total": <jobs on the board>,
   "jobs": [{"title", "link", "location", "remote", "date"}]}   # only the jobs whose title matches a term
   or {"error": "..."} — an unknown URL, or a board that didn't answer.

--terms matches whole words in the title, case-insensitive ("ios" never matches "Bios"); without it
every job is listed. --since drops jobs whose date is older; a job without a date is kept (Gupy and
InHire lists carry none: the posting's own page has it).
"""
import argparse
import datetime
import json
import re
import subprocess
import sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"


def get(url, *extra):
    out = subprocess.run(["curl", "-s", "-m", "25", "-A", UA, *extra, url], capture_output=True, text=True).stdout
    return out


def get_json(url, *extra):
    try:
        return json.loads(get(url, *extra))
    except json.JSONDecodeError:
        return None


def day(value):
    """ISO date from an ISO string or an epoch in milliseconds."""
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return datetime.datetime.fromtimestamp(value / 1000, datetime.timezone.utc).date().isoformat()
    return str(value)[:10]


def job(title, link, location=None, remote=None, date=None):
    return {"title": (title or "").strip(), "link": link, "location": location, "remote": remote, "date": day(date)}


def greenhouse(slug):
    d = get_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
    if not d or "jobs" not in d:
        return None
    # first_published is the posting's age; updated_at moves with every edit of an old posting.
    return [job(j["title"], j["absolute_url"], (j.get("location") or {}).get("name"), None,
                j.get("first_published") or j.get("updated_at")) for j in d["jobs"]]


def lever(slug):
    d = get_json(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    if not isinstance(d, list):
        return None
    return [job(j["text"], j["hostedUrl"], (j.get("categories") or {}).get("location"),
                j.get("workplaceType") == "remote", j.get("createdAt")) for j in d]


def ashby(slug):
    d = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
    if not d or "jobs" not in d:
        return None
    return [job(j["title"], j["jobUrl"], j.get("location"), j.get("isRemote"), j.get("publishedAt")) for j in d["jobs"]]


def workable(slug):
    d = get_json(f"https://apply.workable.com/api/v1/widget/accounts/{slug}?details=false")
    if not d or "jobs" not in d:
        return None
    return [job(j["title"], j["url"], ", ".join(x for x in (j.get("city"), j.get("country")) if x),
                j.get("telecommuting"), j.get("published_on") or j.get("created_at")) for j in d["jobs"]]


def inhire(tenant):
    d = get_json("https://api.inhire.app/job-posts/public/pages", "-H", f"X-Tenant: {tenant}")
    if not d or "jobsPage" not in d:
        return None
    return [job(j["displayName"], f"https://{tenant}.inhire.app/vagas/{j['jobId']}", j.get("location"),
                j.get("workplaceType") == "Remote") for j in d["jobsPage"]]


def gupy(slug):
    m = re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>', get(f"https://{slug}.gupy.io/"), re.S)
    if not m:
        return None
    jobs = json.loads(m.group(1))["props"]["pageProps"].get("jobs") or []
    out = []
    for j in jobs:
        w = j.get("workplace") or {}
        a = w.get("address") or {}
        out.append(job(j["title"], f"https://{slug}.gupy.io/jobs/{j['id']}",
                       ", ".join(x for x in (a.get("city"), a.get("state"), a.get("country")) if x) or None,
                       w.get("workplaceType") == "remote"))
    return out


def smartrecruiters(slug):
    out, offset = [], 0
    while True:
        d = get_json(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=100&offset={offset}")
        if not d or "content" not in d:
            return out or None
        for j in d["content"]:
            loc = j.get("location") or {}
            out.append(job(j["name"], f"https://jobs.smartrecruiters.com/{slug}/{j['id']}",
                           ", ".join(x for x in (loc.get("city"), loc.get("country")) if x), loc.get("remote"), j.get("releasedDate")))
        offset += 100
        if offset >= d.get("totalFound", 0):
            return out


def recrutei(label):
    d = get_json(f"https://api.recrutei.com.br/api/v2/vacancies/per-departments/{label}",
                 "-X", "POST", "-H", "Content-Type: application/json", "-d", "{}")
    if not d or "data" not in d:
        return None
    return [job(i["title"], i.get("public_link"), i.get("location"), bool(i.get("remote")))
            for v in d["data"].get("vacancies", []) for i in v.get("items", [])]


def solides(slug):
    out, page = [], 1
    while True:
        d = get_json(f"https://apigw.solides.com.br/jobs/v3/companies/{slug}/vacancies?take=25&page={page}")
        if not d or "data" not in d:
            return out or None
        for j in d["data"]:
            place = ", ".join(x for x in ((j.get("city") or {}).get("name"), (j.get("state") or {}).get("code")) if x)
            out.append(job(j.get("title"), f"https://{slug}.vagas.solides.com.br/vaga/{j['id']}", place or None,
                           j.get("homeOffice"), j.get("publishedAt") or j.get("createdAt")))
        if page >= (d.get("totalPages") or 1):
            return out
        page += 1


def quickin(slug):
    out, page = [], 1
    while True:
        d = get_json(f"https://api.quickin.io/public/careersites/{slug}/jobs?page={page}")
        if not d or "docs" not in d:
            return out or None
        out += [job(j["title"], j.get("career_url") or f"https://jobs.quickin.io/{slug}/jobs/{j['_id']}", j.get("city"),
                    j.get("workplace_type") == "remote", j.get("createdAt")) for j in d["docs"]]
        if page >= (d.get("pages") or d.get("totalPages") or 1):
            return out
        page += 1


def bamboohr(slug):
    d = get_json(f"https://{slug}.bamboohr.com/careers/list", "-H", "Accept: application/json")
    if not d or "result" not in d:
        return None
    return [job(j["jobOpeningName"], f"https://{slug}.bamboohr.com/careers/{j['id']}",
                ", ".join(x for x in ((j.get("location") or {}).get("city"), (j.get("location") or {}).get("state")) if x),
                bool(j.get("isRemote"))) for j in d["result"]]


def rippling(slug):
    d = get_json(f"https://api.rippling.com/platform/api/ats/v1/board/{slug}/jobs")
    if not isinstance(d, list):
        return None
    return [job(j["name"], j.get("url"), (j.get("workLocation") or {}).get("label")) for j in d]


def recruitee(slug):
    d = get_json(f"https://{slug}.recruitee.com/api/offers/")
    if not d or "offers" not in d:
        return None
    return [job(j["title"], j.get("careers_url"), j.get("location"), j.get("remote"), j.get("published_at")) for j in d["offers"]]


def teamtailor(host):
    d = get_json(f"https://{host}/jobs.json")  # a JSON Feed
    if not isinstance(d, dict) or "items" not in d:
        return None
    return [job(j.get("title"), j.get("url"), None, None, j.get("date_published")) for j in d["items"]]


# URL pattern → (ATS, reader). The group is the slug, tenant or host.
BOARDS = [
    # The public API URLs, as a source's method text writes them
    (r"boards-api\.greenhouse\.io/v1/boards/([\w-]+)", "Greenhouse", greenhouse),
    (r"api\.lever\.co/v0/postings/([\w.-]+)", "Lever", lever),
    (r"api\.ashbyhq\.com/posting-api/job-board/([\w.%-]+)", "Ashby", ashby),
    (r"apply\.workable\.com/api/v\d/(?:widget/)?accounts/([\w-]+)", "Workable", workable),
    (r"X-Tenant:\s*([\w-]+)", "InHire", inhire),
    (r"api\.smartrecruiters\.com/v1/companies/([\w-]+)", "SmartRecruiters", smartrecruiters),
    (r"per-departments/([\w-]+)", "Recrutei", recrutei),
    (r"apigw\.solides\.com\.br/jobs/v3/companies/([\w-]+)", "Sólides", solides),
    (r"api\.quickin\.io/public/careersites/([\w-]+)", "Quickin", quickin),
    (r"api\.rippling\.com/platform/api/ats/v1/board/([\w-]+)", "Rippling", rippling),
    # The board URLs
    (r"(?:job-boards|boards)(?:\.eu)?\.greenhouse\.io/(?:embed/job_board\?for=)?([\w-]+)", "Greenhouse", greenhouse),
    (r"jobs\.lever\.co/([\w.-]+)", "Lever", lever),
    (r"jobs\.ashbyhq\.com/([\w.%-]+)", "Ashby", ashby),
    (r"apply\.workable\.com/([\w-]+)", "Workable", workable),
    (r"([\w-]+)\.workable\.com", "Workable", workable),
    (r"([\w-]+)\.inhire\.app", "InHire", inhire),
    (r"([\w-]+)\.gupy\.io", "Gupy", gupy),
    (r"(?:jobs|careers)\.smartrecruiters\.com/([\w-]+)", "SmartRecruiters", smartrecruiters),
    (r"jobs\.recrutei\.com\.br/([\w-]+)", "Recrutei", recrutei),
    (r"([\w-]+)\.vagas\.solides\.com\.br", "Sólides", solides),
    (r"jobs\.quickin\.io/([\w-]+)", "Quickin", quickin),
    (r"([\w-]+)\.bamboohr\.com", "BambooHR", bamboohr),
    (r"ats\.rippling\.com/([\w-]+)", "Rippling", rippling),
    (r"([\w-]+)\.recruitee\.com", "Recruitee", recruitee),
    (r"([\w.-]+\.teamtailor\.com)", "Teamtailor", teamtailor),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="board URL or method text")
    ap.add_argument("--terms", default="")
    ap.add_argument("--since")
    a = ap.parse_args()
    for pattern, ats, reader in BOARDS:
        m = re.search(pattern, a.url, re.I)
        if m and m.group(1).lower() not in ("www", "jobs", "careers", "apply"):
            board = m.group(1)
            break
    else:
        print(json.dumps({"error": "no reader for this source: follow its own method"}))
        return 2
    jobs = reader(board)
    if jobs is None:
        print(json.dumps({"ats": ats, "board": board, "error": "the board didn't answer (wrong slug, board gone or blocked)"}))
        return 1
    total = len(jobs)
    terms = [t.strip() for t in a.terms.split(",") if t.strip()]
    if terms:
        rx = re.compile(r"(?<![\w])(" + "|".join(re.escape(t) for t in terms) + r")(?![\w])", re.I)
        jobs = [j for j in jobs if rx.search(j["title"])]
    if a.since:
        jobs = [j for j in jobs if not j["date"] or j["date"] >= a.since]
    print(json.dumps({"ats": ats, "board": board, "total": total, "jobs": jobs}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
