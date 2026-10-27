#!/usr/bin/env python3
"""Finds Notion blocks whose text still carries Markdown/XML markup, i.e. syntax the connector saved
as literal text instead of rendering it.

Usage:
  check_markup.py [--fix] <page id> [<page id> ...]
  check_markup.py [--fix] --since YYYY-MM-DD <collection id> [<collection id> ...]
  check_markup.py --tree <page id>

--since checks every page created on or after that day in the given data sources. --fix rewrites
headings that end in a literal {color="…"} as real colored headings; other findings are only
listed. Exit 1 when something is still wrong. Needs the `ntn` CLI, authenticated.
"""
import json
import re
import subprocess
import sys
import time

MARKUP = re.compile(r'\{color=|</?synced[-_]block|</?table|<h[1-4]\b|</?callout|</?toggle|<empty-block|^\\')
COLOR = re.compile(r'\s*\\?\{color=\\?"([a-z]+)(_bg)?\\?"\\?\}\s*$')


def ntn(path, body=None, method="GET"):
    args = ["perl", "-e", "alarm 90; exec @ARGV", "ntn", "api", path]
    if body is not None:
        args += ["-X", method, "-d", "@-"]
    run = subprocess.run(args, input=json.dumps(body) if body is not None else None,
                         stdin=None if body is not None else subprocess.DEVNULL, capture_output=True, text=True)
    return json.loads(run.stdout) if run.stdout.strip().startswith("{") else {}


def children(block_id):
    found, cursor = [], None
    while True:
        query = f"?page_size=100&start_cursor={cursor}" if cursor else "?page_size=100"
        page = ntn(f"/v1/blocks/{block_id}/children{query}")
        found += page.get("results", [])
        if not page.get("has_more"):
            return found
        cursor = page["next_cursor"]


def text(block):
    data = block.get(block["type"], {})
    if block["type"] == "table_row":
        return " | ".join("".join(r.get("plain_text", "") for r in cell) for cell in data.get("cells", []))
    return "".join(r.get("plain_text", "") for r in data.get("rich_text", []))


def walk(block_id, depth=0):
    for block in children(block_id):
        yield block, depth
        # Synced-block references and child pages hold content that lives elsewhere.
        if block["has_children"] and block["type"] not in ("child_page", "child_database"):
            yield from walk(block["id"], depth + 1)


def fix_heading(block):
    kind, value = block["type"], text(block)
    match = COLOR.search(value)
    if not kind.startswith("heading_") or not match:
        return False
    color = match.group(1) + ("_background" if match.group(2) else "")
    title = COLOR.sub("", value).replace("\\", "").strip()
    body = {kind: {"rich_text": [{"type": "text", "text": {"content": title}}], "color": color}}
    return bool(ntn(f"/v1/blocks/{block['id']}", body, "PATCH").get("id"))


def check(page_id, fix):
    problems = 0
    for block, _ in walk(page_id):
        value = text(block)
        if not MARKUP.search(value):
            continue
        if fix and fix_heading(block):
            print(f"  fixed  {block['type']}: {value[:70]}")
            time.sleep(0.35)
            continue
        problems += 1
        print(f"  markup {block['type']} {block['id']}: {value[:70]}")
    return problems


def pages_since(day, collections):
    for collection in collections:
        cursor = None
        while True:
            body = {"page_size": 100, "filter": {"timestamp": "created_time",
                                                  "created_time": {"on_or_after": day + "T00:00:00Z"}}}
            if cursor:
                body["start_cursor"] = cursor
            result = ntn(f"/v1/data_sources/{collection}/query", body, "POST")
            yield from result.get("results", [])
            if not result.get("has_more"):
                break
            cursor = result["next_cursor"]


def title(page):
    return "".join(t["plain_text"] for v in page.get("properties", {}).values() if v["type"] == "title" for t in v["title"])


def main():
    args = [a for a in sys.argv[1:] if a != "--fix"]
    fix = "--fix" in sys.argv
    if not args:
        sys.exit(__doc__)
    if args[0] == "--tree":
        for block, depth in walk(args[1]):
            color = block.get(block["type"], {}).get("color", "")
            print("  " * depth + f"{block['type']} {color} {text(block)[:80]!r}")
        return
    if args[0] == "--since":
        targets = [(p["id"], title(p)) for p in pages_since(args[1], args[2:])]
    else:
        targets = [(a, title(ntn(f"/v1/pages/{a}"))) for a in args]
    bad = 0
    for page_id, name in targets:
        found = check(page_id, fix)
        if found:
            print(f"{name or page_id}: {found} block(s) with markup")
        bad += bool(found)
    print(f"{len(targets)} page(s) checked, {bad} with markup left")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
