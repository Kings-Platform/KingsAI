#!/usr/bin/env python3
"""Discovery log for source-discovery: who was read, which companies were seen, where each one stopped.

The log is a folder with two TSV files, kept between runs so no recruiter is read twice and no
company page is opened twice:

  recruiters.tsv  slug, name, headline, found_on, read_on, status
  companies.tsv   company_id, name, website, industry, size, from_recruiters, first_seen, stage, note

Stages of a company: new (link saved) -> site (website read) -> a verdict from source-check
(source, no-listing, not-tech, login, dead), or known (already on the sources page) or
excluded (the profile's exclusion list).

Commands (every one prints a short summary; JSON goes to the file given):

  people   LOG SEARCH_JSON... --out FILE      people from linkedin-reader `search` not read yet
  roles    LOG EXP_JSON... --sources PAGE [--exclude NAMES] --out FILE
           records recruiters and their employers, dedupes across profiles and against the log
           and the sources page; FILE = the new companies whose page still has to be read
  sites    LOG COMPANY_JSON... --sources PAGE --out FILE
           records websites; a domain already on the sources page -> known; FILE = the leads
           for source-check (name, website, linkedin)
  verdicts LOG VALIDATOR_JSON...              records each lead's verdict
  stats    LOG
"""
import argparse
import csv
import datetime
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

RECRUITER_COLS = ["slug", "name", "headline", "found_on", "read_on", "status"]
COMPANY_COLS = ["company_id", "name", "website", "industry", "size", "from_recruiters",
                "first_seen", "stage", "note"]
SUFFIXES = r"\b(inc|llc|ltd|ltda|s\.?a\.?|sa|gmbh|corp|corporation|co|company|group|grupo|plc|ag|bv|srl|sas)\b\.?"
TODAY = datetime.date.today().isoformat()


def load(path, cols, key):
    rows = {}
    if path.exists():
        with path.open(newline="") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                rows[row[key]] = {c: row.get(c, "") for c in cols}
    return rows


def save(path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in rows.values():
            w.writerow({c: str(row.get(c, "")).replace("\t", " ").replace("\n", " ") for c in cols})


def read_json(paths):
    for p in paths:
        try:
            yield json.loads(Path(p).read_text())
        except (OSError, json.JSONDecodeError) as e:
            print(f"skipped {p}: {e}", file=sys.stderr)


def company_id(link):
    m = re.search(r"/company/([^/?#]+)", link or "")
    return m.group(1).lower() if m else None


def norm(name):
    s = re.sub(SUFFIXES, " ", (name or "").lower())
    return re.sub(r"[^\w]+", " ", s).strip()


def on_page(name, page):
    n = norm(name)
    return len(n) >= 3 and re.search(r"(?<!\w)" + re.escape(n) + r"(?!\w)", page) is not None


def domain(url):
    host = urlparse(url if "//" in (url or "") else "//" + (url or "")).hostname or ""
    return host.lower().removeprefix("www.")


def page_text(path):
    return norm(Path(path).read_text()) if path else ""


def cmd_people(a):
    log = Path(a.log)
    recruiters = load(log / "recruiters.tsv", RECRUITER_COLS, "slug")
    fresh, seen = [], set()
    for data in read_json(a.files):
        for p in data.get("people", []):
            slug = p.get("slug")
            if not slug or slug in seen:
                continue
            seen.add(slug)
            if slug in recruiters:
                continue
            recruiters[slug] = {"slug": slug, "name": p.get("name", ""), "headline": p.get("headline", ""),
                                "found_on": TODAY, "read_on": "", "status": "found"}
            fresh.append(p)
    pending = [r for r in recruiters.values() if not r["read_on"]]
    save(log / "recruiters.tsv", RECRUITER_COLS, recruiters)
    Path(a.out).write_text(json.dumps(pending, ensure_ascii=False, indent=1))
    print(f"people: {len(seen)} in the search, {len(fresh)} new to the log, {len(pending)} not read yet -> {a.out}")


def cmd_roles(a):
    log = Path(a.log)
    recruiters = load(log / "recruiters.tsv", RECRUITER_COLS, "slug")
    companies = load(log / "companies.tsv", COMPANY_COLS, "company_id")
    page = page_text(a.sources)
    exclude = [norm(x) for x in (a.exclude or "").split(",") if x.strip()]
    counts = {"roles": 0, "kept": 0, "not_recruiting": 0, "skipped": 0, "no_page": 0,
              "dup_profiles": 0, "dup_log": 0, "known": 0, "excluded": 0, "new": 0}
    new = {}
    for data in read_json(a.files):
        for r in data.get("recruiters", []):
            slug = r.get("slug")
            if not slug:
                continue
            row = recruiters.setdefault(slug, {"slug": slug, "found_on": TODAY})
            row.update(name=r.get("name", row.get("name", "")), headline=r.get("headline", row.get("headline", "")),
                       read_on=TODAY, status=r.get("status", "ok"))
            for role in r.get("roles", []):
                counts["roles"] += 1
                name = role.get("company", "")
                if any(x and x in norm(name) for x in exclude):
                    counts["excluded"] += 1
                    continue
                if role.get("skip"):
                    counts["skipped"] += 1
                    continue
                if role.get("recruiting") is False:
                    counts["not_recruiting"] += 1
                    continue
                cid = company_id(role.get("linkedin"))
                if not cid:
                    counts["no_page"] += 1
                    continue
                counts["kept"] += 1
                if cid in new:
                    counts["dup_profiles"] += 1
                    new[cid]["from"].add(slug)
                    continue
                if cid in companies:
                    counts["dup_log"] += 1
                    froms = set(filter(None, companies[cid]["from_recruiters"].split(",")))
                    companies[cid]["from_recruiters"] = ",".join(sorted(froms | {slug}))
                    continue
                stage = "known" if on_page(name, page) else "new"
                counts["known" if stage == "known" else "new"] += 1
                new[cid] = {"name": name, "stage": stage, "from": {slug}}
    for cid, c in new.items():
        companies[cid] = {"company_id": cid, "name": c["name"], "from_recruiters": ",".join(sorted(c["from"])),
                          "first_seen": TODAY, "stage": c["stage"]}
    save(log / "recruiters.tsv", RECRUITER_COLS, recruiters)
    save(log / "companies.tsv", COMPANY_COLS, companies)
    todo = [{"linkedin": f"https://www.linkedin.com/company/{cid}/", "name": c["name"]}
            for cid, c in new.items() if c["stage"] == "new"]
    Path(a.out).write_text(json.dumps(todo, ensure_ascii=False, indent=1))
    print("roles: " + ", ".join(f"{k} {v}" for k, v in counts.items()) + f" -> {len(todo)} pages to read, {a.out}")


def cmd_sites(a):
    log = Path(a.log)
    companies = load(log / "companies.tsv", COMPANY_COLS, "company_id")
    raw = Path(a.sources).read_text().lower() if a.sources else ""
    leads, known, no_site = [], 0, 0
    for data in read_json(a.files):
        for c in data.get("companies", []):
            cid = company_id(c.get("linkedin"))
            if not cid:
                continue
            row = companies.setdefault(cid, {"company_id": cid, "first_seen": TODAY, "from_recruiters": ""})
            row.update(name=c.get("name") or row.get("name", ""), website=c.get("website") or "",
                       industry=c.get("industry") or "", size=c.get("size") or "",
                       note=c.get("site_doubt") or row.get("note", ""))
            d = domain(row["website"])
            if row.get("stage") not in (None, "", "new", "site", "no-site"):
                continue
            if not d:
                row["stage"], no_site = "no-site", no_site + 1
            elif d in raw:
                row["stage"], known = "known", known + 1
            else:
                row["stage"] = "site"
                leads.append({"name": row["name"], "website": row["website"], "linkedin": c.get("linkedin"),
                              "industry": row["industry"], "size": row["size"], "site_doubt": c.get("site_doubt")})
    save(log / "companies.tsv", COMPANY_COLS, companies)
    Path(a.out).write_text(json.dumps(leads, ensure_ascii=False, indent=1))
    print(f"sites: {len(leads)} leads, {known} known by domain, {no_site} without a website -> {a.out}")


def cmd_verdicts(a):
    log = Path(a.log)
    companies = load(log / "companies.tsv", COMPANY_COLS, "company_id")
    by_site = {domain(c["website"]): c for c in companies.values() if c["website"]}
    tally = {}
    for data in read_json(a.files):
        for v in data if isinstance(data, list) else data.get("sources") or data.get("companies") or [data]:
            # A lead whose website was found by the validator (not on LinkedIn) is matched by its company link
            row = companies.get(company_id(v.get("linkedin"))) or by_site.get(domain(v.get("website") or v.get("url")))
            if not row:
                continue
            if v.get("website") and not row.get("website"):
                row["website"] = v["website"]
            verdict = v.get("verdict", "")
            row["stage"] = "source" if verdict in ("api", "page-ok", "browser-only", "source", "known") else verdict
            row["note"] = (v.get("careers_url") or v.get("url") or row["note"])[:300]
            tally[row["stage"]] = tally.get(row["stage"], 0) + 1
    save(log / "companies.tsv", COMPANY_COLS, companies)
    print("verdicts: " + ", ".join(f"{k} {n}" for k, n in sorted(tally.items())))


def cmd_stats(a):
    log = Path(a.log)
    recruiters = load(log / "recruiters.tsv", RECRUITER_COLS, "slug")
    companies = load(log / "companies.tsv", COMPANY_COLS, "company_id")
    read = sum(1 for r in recruiters.values() if r["read_on"])
    stages = {}
    for c in companies.values():
        stages[c["stage"]] = stages.get(c["stage"], 0) + 1
    print(f"recruiters: {read} read, {len(recruiters) - read} waiting; companies: {len(companies)} — "
          + ", ".join(f"{k} {n}" for k, n in sorted(stages.items())))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("people", cmd_people), ("roles", cmd_roles), ("sites", cmd_sites),
                     ("verdicts", cmd_verdicts), ("stats", cmd_stats)):
        p = sub.add_parser(name)
        p.add_argument("log")
        if name != "stats":
            p.add_argument("files", nargs="+")
        if name in ("people", "roles", "sites"):
            p.add_argument("--out", required=True)
        if name in ("roles", "sites"):
            p.add_argument("--sources")
        if name == "roles":
            p.add_argument("--exclude")
        p.set_defaults(fn=fn)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
