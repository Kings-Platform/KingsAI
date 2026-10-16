---
name: site-icon
description: Saves the icon a website shows in the browser tab (its favicon) as a transparent PNG, using `kings site-icon`. Use when the user passes a site and asks for "the tab icon", "the favicon", "the site's logo as PNG", "an icon for this page/card", or needs a company's logo for a page icon. Several sites → several in parallel. Hands each site to the site-icon-fetcher agent, which runs the command and looks at the result.
---

# Site icon

This skill holds the **order**: what to resolve before running and what to report. The command
does the work — discovery, download, SVG rendering — and its options are in
[KingsScript](https://github.com/Kings-Platform/KingsScript) (`kings help`).

| Step | Who |
|---|---|
| Resolve site, destination, size | This session |
| Run, look at the PNG, try the other candidates when the first is poor | `site-icon-fetcher` agent (Haiku) |

## 1. Resolve

- **Site:** the URL the user gave. Only a company name → the official site from a quick search;
  unsure between two domains → ask, never guess.
- **Destination:** what the user said; otherwise the command's default (the Desktop, or
  `KINGS_ICON_DIR`). A file with the same name already there → pass a `--name` that doesn't
  overwrite it.
- **Size:** 512 unless the user asks. A raster icon is never upscaled — the PNG comes out at the
  largest size the site publishes.

`kings` not installed (`command -v kings` fails) → stop and say so; don't download by hand.

## 2. Hand off

One `site-icon-fetcher` call per site, with `URL`, `OUT` (folder), `NAME` (only when needed) and
`SIZE`. Several sites → the calls in parallel, in one message.

## 3. Report

One line per site: the path, the size and where the icon came from. Then, when the agent flagged
it, what the user should know:

- **Small** (under 128 px): it's all the site publishes for the tab; say which larger candidate
  exists (e.g. the touch icon), if any.
- **Plain shape or a platform's default icon**: the tab really shows that — say so, and offer
  the alternative the agent found.

Show the image only when the user asks; the file is on disk.

## What this skill never does

- Upscale a small icon to fake a bigger one
- Pick another site's icon, or a generic logo from an image search, in place of the site's own
- Overwrite a file the user already had
