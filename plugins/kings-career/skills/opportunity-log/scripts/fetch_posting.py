#!/usr/bin/env python3
"""Fetch a job posting's original text from public endpoints, without a browser.

Usage:
  fetch_posting.py <posting-url> [--body-out FILE]
  fetch_posting.py --supports <posting-url>       (exit 0 = served without a browser, 2 = needs one)
  fetch_posting.py --post-date <linkedin-post-url> (the post's exact creation date, from its id)
  fetch_posting.py --wrap TEXT_FILE --title "<header>" --body-out FILE
  fetch_posting.py --unavailable --body-out FILE

Prints JSON: {source, title, location, posted_at, poster, emails, text}. `text` is the posting
body as Notion-flavored markdown (bold section titles, "- " bullets). Exit code 2 when the URL
belongs to no supported source: the caller falls back to reading the page in a browser.

--body-out writes the Notion "Descrição da vaga" content, ready to paste: the text escaped and
indented inside a synced block. --wrap does the same for text read elsewhere (a browser, a post);
--unavailable writes the "posting taken down" note in its place.

Supported: Greenhouse (boards and company pages that carry the gh job id), Lever, Ashby, Gupy, Comeet, Personio,
SmartRecruiters, Recruitee, Workday, Oracle Cloud HCM, amazon.jobs, LinkedIn job pages (the logged-out jobs-guest endpoint) and
any page that embeds the posting as schema.org JSON-LD (Teamtailor and many careers sites). LinkedIn posts need a session and are
not supported.
"""

import datetime
import html
import json
import re
import subprocess
import sys

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def get(url):
    # curl uses the system trust store; python.org builds of Python often ship without one.
    result = subprocess.run(
        ["curl", "-sSfL", "--max-time", "20", "-A", USER_AGENT, url],
        capture_output=True,
        check=True,
    )
    return result.stdout.decode("utf-8", errors="replace")


def bold(match):
    # Whitespace inside <b>…</b> moves outside the markers: Notion doesn't render "**A: **B".
    inner = re.sub(r"<[^>]+>", "", match.group(2))
    if not any(char.isalnum() for char in inner):
        return inner
    lead = " " if inner[0].isspace() else ""
    tail = " " if inner[-1].isspace() else ""
    return f"{lead}**{inner.strip()}**{tail}"


def to_markdown(markup):
    # Greenhouse double-encodes its content: one unescape yields tags, a second yields the text.
    text = html.unescape(html.unescape(markup)).replace("\xa0", " ")
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<(h[1-6])[^>]*>(.*?)</\1>", lambda m: "\n" + bold(m) + "\n", text, flags=re.S)
    text = re.sub(r"<(strong|b)\b[^>]*>(.*?)</\1>", bold, text, flags=re.S)
    text = re.sub(r"<li[^>]*>", "- ", text)
    text = re.sub(r"</(p|li|h\d|div|ul|ol)>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    lines = [re.sub(r"[ \t]{2,}", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line and line != "**")


def iso_from_ms(value):
    if not value:
        return None
    return datetime.datetime.fromtimestamp(value / 1000, datetime.UTC).date().isoformat()


def greenhouse(url):
    match = re.search(r"greenhouse\.io/([^/]+)/jobs/(\d+)", url)
    board, job_id = (match.group(1), match.group(2)) if match else (None, None)
    if not match:
        # Company careers pages often end in the Greenhouse job id; the board is the company name.
        tail = re.search(r"/(\d{7,})/?$", url)
        # The company is the label before the TLD: careers.example.com and www.example.com both work.
        host = re.search(r"https?://(?:[a-z0-9-]+\.)*?([a-z0-9-]+)\.[a-z]{2,}(?:\.[a-z]{2})?/", url)
        if not (tail and host):
            return None
        board, job_id = host.group(1), tail.group(1)
    data = json.loads(get(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs/{job_id}"))
    text = to_markdown(data["content"])
    return {
        "source": "greenhouse",
        "title": data["title"],
        "location": data.get("location", {}).get("name"),
        "posted_at": (data.get("first_published") or "")[:10] or None,
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def lever(url):
    match = re.search(r"jobs\.lever\.co/([^/]+)/([0-9a-f-]{36})", url)
    if not match:
        return None
    data = json.loads(get(f"https://api.lever.co/v0/postings/{match.group(1)}/{match.group(2)}"))
    parts = [to_markdown(data.get("description", ""))]
    parts += [f"**{item['text']}**\n{to_markdown(item['content'])}" for item in data.get("lists", [])]
    parts.append(to_markdown(data.get("additional", "")))
    text = "\n".join(part for part in parts if part)
    return {
        "source": "lever",
        "title": data["text"],
        "location": data.get("categories", {}).get("location"),
        "posted_at": iso_from_ms(data.get("createdAt")),
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def ashby(url):
    match = re.search(r"jobs\.ashbyhq\.com/([^/]+)/([0-9a-f-]{36})", url)
    if not match:
        return None
    board, job_id = match.groups()
    jobs = json.loads(get(f"https://api.ashbyhq.com/posting-api/job-board/{board}"))["jobs"]
    job = next((item for item in jobs if job_id in (item.get("id", "") + item.get("jobUrl", ""))), None)
    if not job:
        return None
    text = to_markdown(job.get("descriptionHtml", ""))
    return {
        "source": "ashby",
        "title": job["title"],
        "location": job.get("location"),
        "posted_at": (job.get("publishedAt") or "")[:10] or None,
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def linkedin_job(url):
    match = re.search(r"linkedin\.com/jobs/view/(?:[^/]*-)?(\d+)", url) or re.search(
        r"currentJobId=(\d+)", url
    )
    if not match:
        return None
    page = get(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{match.group(1)}")
    body = re.search(r"show-more-less-html__markup[^>]*>(.*?)</div>", page, re.S)
    if not body:
        return None
    title = re.search(r"top-card-layout__title[^>]*>(.*?)</h2>", page, re.S)
    location = re.search(r"topcard__flavor--bullet[^>]*>(.*?)</span>", page, re.S)
    ago = re.search(r"posted-time-ago__text[^>]*>\s*(.*?)\s*<", page, re.S)
    poster = re.search(r"Direct message the job poster.*?href=\"(https://[a-z.]*linkedin\.com/in/[^\"?]+)", page, re.S)
    text = to_markdown(body.group(1))
    return {
        "source": "linkedin",
        "title": html.unescape(title.group(1)).strip() if title else None,
        "location": html.unescape(location.group(1)).strip() if location else None,
        "posted_at": approximate_date(ago.group(1)) if ago else None,
        "poster": re.sub(r"https://[a-z]+\.linkedin", "https://www.linkedin", poster.group(1)) if poster else None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def gupy(url):
    if not re.search(r"\.gupy\.io/jobs/\d+", url):
        return None
    page = get(url)
    data = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.S)
    if not data:
        return None
    job = json.loads(data.group(1))["props"]["pageProps"]["job"]
    sections = [
        ("", job.get("description")),
        ("Responsabilidades e atribuições", job.get("responsibilities")),
        ("Requisitos e qualificações", job.get("prerequisites")),
        ("Informações adicionais", job.get("relevantExperiences")),
    ]
    text = "\n".join(
        (f"**{title}**\n" if title else "") + to_markdown(body) for title, body in sections if body
    )
    place = ", ".join(part for part in (job.get("addressCity"), job.get("addressStateShortName")) if part)
    return {
        "source": "gupy",
        "title": job.get("name"),
        "location": place or job.get("workplaceType"),
        "posted_at": (job.get("publishedAt") or "")[:10] or None,
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def smartrecruiters(url):
    match = re.search(r"jobs\.smartrecruiters\.com/([^/]+)/(\d+)", url)
    if not match:
        return None
    company, job_id = match.groups()
    data = json.loads(get(f"https://api.smartrecruiters.com/v1/companies/{company}/postings/{job_id}"))
    sections = (data.get("jobAd") or {}).get("sections", {})
    parts = [
        (f"**{section['title']}**\n" if section.get("title") else "") + to_markdown(section.get("text", ""))
        for section in sections.values()
        if section.get("text")
    ]
    text = "\n".join(parts)
    location = data.get("location") or {}
    return {
        "source": "smartrecruiters",
        "title": data.get("name"),
        "location": ", ".join(part for part in (location.get("city"), location.get("country")) if part and part != "xx"),
        "posted_at": (data.get("releasedDate") or "")[:10] or None,
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def recruitee(url):
    match = re.search(r"https?://([^.]+)\.recruitee\.com/o/([^/?#]+)", url)
    if not match:
        return None
    company, slug = match.groups()
    offer = json.loads(get(f"https://{company}.recruitee.com/api/offers/{slug}"))["offer"]
    text = "\n".join(
        part
        for part in (to_markdown(offer.get("description", "")), to_markdown(offer.get("requirements", "")))
        if part
    )
    return {
        "source": "recruitee",
        "title": offer.get("title"),
        "location": offer.get("location"),
        "posted_at": (offer.get("published_at") or "")[:10] or None,
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def workday(url):
    match = re.search(r"https://([^./]+)\.(wd\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/]+)/(?:job|details)/(.+?)/?$", url)
    if not match:
        return None
    tenant, pod, site, path = match.groups()
    data = json.loads(get(f"https://{tenant}.{pod}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/job/{path}"))
    job = data["jobPostingInfo"]
    text = to_markdown(job.get("jobDescription", ""))
    return {
        "source": "workday",
        "title": job.get("title"),
        "location": job.get("location"),
        "posted_at": job.get("startDate"),
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def oracle_hcm(url):
    match = re.search(r"https://([^/]+\.oraclecloud\.com)/hcmUI/CandidateExperience/[a-z-]+/sites/([^/]+)/job/(\d+)", url)
    if not match:
        return None
    host, site, job_id = match.groups()
    endpoint = (
        f"https://{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails"
        f'?expand=all&onlyData=true&finder=ById;Id="{job_id}",siteNumber={site}'
    )
    items = json.loads(get(endpoint)).get("items") or []
    if not items:
        return None  # an empty answer is not proof the posting is gone: the caller checks the page
    job = items[0]
    sections = [
        ("", job.get("ExternalDescriptionStr")),
        ("Responsibilities", job.get("ExternalResponsibilitiesStr")),
        ("Qualifications", job.get("ExternalQualificationsStr")),
    ]
    text = "\n".join((f"**{title}**\n" if title else "") + to_markdown(body) for title, body in sections if body)
    return {
        "source": "oracle-hcm",
        "title": job.get("Title"),
        "location": job.get("PrimaryLocation"),
        "posted_at": (job.get("ExternalPostedStartDate") or "")[:10] or None,
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def amazon_jobs(url):
    match = re.search(r"amazon\.jobs/[a-z-]+/jobs/(\d+)", url)
    if not match:
        return None
    jobs = json.loads(get(f"https://www.amazon.jobs/en/search.json?base_query={match.group(1)}")).get("jobs", [])
    job = next((item for item in jobs if item.get("id_icims") == match.group(1)), None)
    if not job:
        return None
    sections = [
        ("", job.get("description")),
        ("Basic qualifications", job.get("basic_qualifications")),
        ("Preferred qualifications", job.get("preferred_qualifications")),
    ]
    text = "\n".join((f"**{title}**\n" if title else "") + to_markdown(body) for title, body in sections if body)
    posted = None
    if job.get("posted_date"):
        posted = datetime.datetime.strptime(job["posted_date"], "%B %d, %Y").date().isoformat()
    return {
        "source": "amazon-jobs",
        "title": job.get("title"),
        "location": job.get("normalized_location") or job.get("location"),
        "posted_at": posted,
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def comeet(url):
    if "comeet.com/jobs/" not in url:
        return None
    page = get(url)
    data = re.search(r"POSITION_DATA\s*=\s*(\{.*?\});\s*\n", page, re.S)
    if not data:
        return None
    job = json.loads(data.group(1))
    details = (job.get("custom_fields") or {}).get("details") or []
    text = "\n".join(
        (f"**{item['name']}**\n" if item.get("name") else "") + to_markdown(item.get("value") or "")
        for item in details
        if item.get("value")
    )
    place = job.get("location") or {}
    return {
        "source": "comeet",
        "title": job.get("name"),
        "location": ", ".join(part for part in (place.get("city"), place.get("country")) if part) or None,
        "posted_at": None,  # only the last update time is published
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def personio(url):
    match = re.search(r"https://([^./]+)\.jobs\.personio\.(?:com|de)/job/(\d+)", url)
    if not match:
        return None
    page = get(f"https://{match.group(1)}.jobs.personio.com/job/{match.group(2)}?language=en")
    # The page is server-rendered; each section is a jb-description-item with a title and rich text.
    items = re.findall(
        r'jb-description-item">\s*(?:<h2[^>]*>(.*?)</h2>)?\s*<div[^>]*rich-text-content[^>]*>(.*?)</div></div>',
        page,
        re.S,
    )
    if not items:
        return None
    text = "\n".join((f"**{html.unescape(title).strip()}**\n" if title else "") + to_markdown(body) for title, body in items)
    title = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
    return {
        "source": "personio",
        "title": html.unescape(re.sub(r"<[^>]+>", "", title.group(1))).strip() if title else None,
        "location": None,
        "posted_at": None,
        "poster": None,
        "emails": sorted(set(EMAIL.findall(text))),
        "text": text,
    }


def linkedin_post_date(url):
    """A LinkedIn post or activity id carries its creation time in its top 41 bits (ms since epoch)."""
    match = re.search(r"(?:activity[:-]|share-|ugcPost-)(\d{18,20})", url)
    if not match:
        return None
    millis = int(match.group(1)) >> 22
    return datetime.datetime.fromtimestamp(millis / 1000, datetime.UTC).date().isoformat()


def json_ld(url):
    # Many careers pages (Teamtailor and others) embed the posting as schema.org JSON-LD.
    page = get(url)
    for block in re.findall(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", page, re.S):
        try:
            data = json.loads(block, strict=False)
        except ValueError:
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data])
        posting = next((item for item in items if isinstance(item, dict) and item.get("@type") == "JobPosting"), None)
        if not posting or not posting.get("description"):
            continue
        text = to_markdown(posting["description"])
        places = posting.get("jobLocation") or []
        place = (places[0] if isinstance(places, list) and places else places or {}).get("address", {})
        location = ", ".join(
            part for part in (place.get("addressLocality"), place.get("addressCountry")) if isinstance(part, str)
        )
        return {
            "source": "json-ld",
            "title": html.unescape(posting.get("title", "")).strip() or None,
            "location": location or None,
            "posted_at": (posting.get("datePosted") or "")[:10] or None,
            "poster": None,
            "emails": sorted(set(EMAIL.findall(text))),
            "text": text,
        }
    return None


def approximate_date(relative):
    """Turns LinkedIn's '3 days ago' into a date; the result is approximate by nature."""
    match = re.match(r"(\d+)\s+(minute|hour|day|week|month)", relative)
    if not match:
        return None
    amount, unit = int(match.group(1)), match.group(2)
    days = {"minute": 0, "hour": 0, "day": 1, "week": 7, "month": 30}[unit] * amount
    return (datetime.date.today() - datetime.timedelta(days=days)).isoformat()


NOTION_RESERVED = re.compile(r"([\\$\[\]<>{}|^~`])")
UNAVAILABLE = (
    '<callout icon="🚫" color="gray_bg">Vaga encerrada — o texto original não está mais disponível.</callout>'
)


def notion_line(line):
    # Bold markers and "- " bullets are kept; every other reserved character is escaped.
    return NOTION_RESERVED.sub(r"\\\1", line)


def synced_block(title, text):
    lines = [f"#### **{notion_line(title)}**"] if title else []
    lines += [notion_line(line) for line in text.splitlines() if line.strip()]
    return "<synced_block>\n" + "\n".join("\t" + line for line in lines) + "\n</synced_block>\n"


def option(flag):
    if flag not in sys.argv:
        return None
    index = sys.argv.index(flag)
    return sys.argv[index + 1] if index + 1 < len(sys.argv) else None


def write_body(content):
    path = option("--body-out")
    if path:
        with open(path, "w") as body:
            body.write(content)


def main():
    if "--post-date" in sys.argv:
        date = linkedin_post_date(option("--post-date") or "")
        print(date or "")
        sys.exit(0 if date else 2)
    if "--supports" in sys.argv:
        # Preflight for the caller, no tokens spent: exit 0 when some source serves this URL's text.
        target = option("--supports") or ""
        if "linkedin.com/posts/" in target or "linkedin.com/feed/" in target:
            sys.exit(2)
        for fetcher in FETCHERS:
            try:
                if fetcher(target):
                    sys.exit(0)
            except Exception:
                continue
        sys.exit(2)
    if "--unavailable" in sys.argv:
        write_body("<synced_block>\n\t" + UNAVAILABLE + "\n</synced_block>\n")
        return
    if "--wrap" in sys.argv:
        with open(option("--wrap")) as source:
            write_body(synced_block(option("--title"), source.read()))
        return
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        sys.exit("usage: fetch_posting.py <posting-url> [--body-out FILE]")
    url = sys.argv[1]
    for fetcher in FETCHERS:
        try:
            result = fetcher(url)
        except Exception as error:  # a dead posting or a changed endpoint: try the next source
            print(f"{fetcher.__name__}: {error}", file=sys.stderr)
            continue
        if result:
            result["url"] = url
            header = " — ".join(part.strip() for part in (result["title"], result["location"]) if part)
            write_body(synced_block(header, result["text"]))
            print(json.dumps(result, ensure_ascii=False, indent=1))
            return
    print(json.dumps({"url": url, "error": "unsupported source"}))
    sys.exit(2)


FETCHERS = (lever, ashby, linkedin_job, gupy, comeet, personio, smartrecruiters, recruitee, workday, oracle_hcm, amazon_jobs, greenhouse, json_ld)


if __name__ == "__main__":
    main()
