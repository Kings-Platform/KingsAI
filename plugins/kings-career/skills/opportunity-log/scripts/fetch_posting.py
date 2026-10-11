#!/usr/bin/env python3
"""Fetch a job posting's original text from public endpoints, without a browser.

Usage: fetch_posting.py <posting-url>

Prints JSON: {source, title, location, posted_at, poster, emails, text}. `text` is the posting
body as Notion-flavored markdown (bold section titles, "- " bullets). Exit code 2 when the URL
belongs to no supported source: the caller falls back to reading the page in a browser.

Supported: Greenhouse (boards and company pages that carry the gh job id), Lever, Ashby and
LinkedIn job pages (the logged-out jobs-guest endpoint). LinkedIn posts need a session and are
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


def to_markdown(markup):
    text = html.unescape(markup)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<(h[1-6])[^>]*>\s*(.*?)\s*</\1>", r"\n**\2**\n", text, flags=re.S)
    text = re.sub(r"<(strong|b)>\s*(.*?)\s*</\1>", r"**\2**", text, flags=re.S)
    text = re.sub(r"<li[^>]*>", "- ", text)
    text = re.sub(r"</(p|li|h\d|div|ul|ol)>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\xa0", " ")
    lines = [line.strip() for line in text.splitlines()]
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
        host = re.search(r"https?://(?:www\.)?([a-z0-9-]+)\.", url)
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


def approximate_date(relative):
    """Turns LinkedIn's '3 days ago' into a date; the result is approximate by nature."""
    match = re.match(r"(\d+)\s+(minute|hour|day|week|month)", relative)
    if not match:
        return None
    amount, unit = int(match.group(1)), match.group(2)
    days = {"minute": 0, "hour": 0, "day": 1, "week": 7, "month": 30}[unit] * amount
    return (datetime.date.today() - datetime.timedelta(days=days)).isoformat()


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: fetch_posting.py <posting-url>")
    url = sys.argv[1]
    for fetcher in (lever, ashby, linkedin_job, greenhouse):
        try:
            result = fetcher(url)
        except Exception as error:  # a dead posting or a changed endpoint: try the next source
            print(f"{fetcher.__name__}: {error}", file=sys.stderr)
            continue
        if result:
            result["url"] = url
            print(json.dumps(result, ensure_ascii=False, indent=1))
            return
    print(json.dumps({"url": url, "error": "unsupported source"}))
    sys.exit(2)


if __name__ == "__main__":
    main()
