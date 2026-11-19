# Job sources

Read by the `job-sweep` skill. It says **what to search for**, **where**, and **how often**. The
mechanics and the public sources live in the plugin's
sources catalog (`kings-career` → `skills/job-sweep/sources-catalog.md`) — list here only what you use and what
the catalog can't hold.

## Search

| Setting | Value |
|---|---|
| Search terms (`{query}`) | `iOS`, `Swift`, `Senior iOS` |
| Target rule (which titles count, which to drop even when they mention a term) | Empty → `job-sweep` asks you. e.g. `keep native iOS (Swift, UIKit, SwiftUI; "iOS and Android" native) · drop another platform only (Android-only, React Native, Flutter) and QA, support, sales, design or management titles that merely mention it` |
| Freshness (oldest posting worth recording) | `60 days` |
| Location terms (`{location}`) | `remote`, `LATAM`, `Brazil` |
| Frequency (default for every source) | `weekly` (or `daily 09:00`, `every 2 days`) |

## Catalog sources in use

One row per catalog source you sweep. `Frequency` empty = the default above.

| Source | Frequency | Last run | Notes |
|---|---|---|---|
| remotar.com.br | | | |
| vagaslume.tech | | | |
| Himalayas | | | |

## Catalog sources turned off

| Source | Why |
|---|---|
| | |

## Your own sources

Company boards, recruiters' lists, communities — anything the catalog doesn't name.

| Source | URL | Access (API, page, browser, members-only) | Category (ATS or feed, for batching) | Frequency | Last run | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

## Companies to watch

Companies that hire your target remotely, even with nothing open today. The sweep reads their
board in full each run.

| Company | Board (ATS + id) | Why |
|---|---|---|
| | | |
