---
name: readme-style
description: The owner's README standard, extracted from their repositories. Use ALWAYS when creating, rewriting or reviewing a README.md, or any human-facing .md documentation inside a repo, in any project. Covers skeleton per repo type (app, tool, library, index), badges, index, tables, code blocks, callouts and the author block.
---

# README standard

Good documentation here is **precise and visual**: the reader scans and finds what they need.
Tables, bullets and code carry the *what* and the *how*. Prose only explains the *why* and the
*when* (reason, trade-off, what **not** to do), in 1–3 sentences.

Live reference of the current style, public: the
[KingsScript README](https://github.com/Kings-Platform/KingsScript#readme) (tool, English).

## General rules

- **Language:** Portuguese (pt-BR) for Brazilian or personal-business projects; English for
  portfolio, libraries, public tools and international work. Badge labels always in English
- **Structure over prose:** ~60–70% of a README is tables, lists or code. A paragraph that lists
  things becomes a table or bullets
- **Short sentences, neutral technical tone.** No exclamation marks, no marketing, **no emoji**
- **Em dash (—)** to add the reason or the contrast inside a sentence: "Scripts never live inline
  in the YAML — always in a separate file."
- **Bold** only for the key constraint of a section (one per block, two at most)
- Headings in *sentence case* (`How to run`, `Quick usage`), never Title Case
- Wrap paragraphs and long bullets at ~100 columns
- Portuguese bullets without a final period; English library bullets with one
- Sections chosen by the repo's purpose, named after tasks ("How to run", "Build", "Usage") — no
  fixed template with empty sections
- Never mention a company, client or private context in a repo that may become public

## Skeleton

```
# Name — Subpart               ← single H1; em dash for a subpart
badges (one per line)
</br>                          ← optional spacing before the index
intro: 1–2 sentences
index                          ← only with 4+ sections
## sections...
</br> + --- + ## Author        ← apps and personal repos; tools and libraries don't have it
```

### Badges (shields.io, default flat style)

Fixed colors:

| Badge | Color | Example |
|---|---|---|
| version | `orange`, linked to the release tag | `[![Version](https://img.shields.io/badge/version-5.2.0-orange)](.../releases/tag/5.2.0)` |
| language / language version | `blue` + `?logo=` | `![Language](https://img.shields.io/badge/language-Python-blue?logo=python)` |
| platform | `lightgrey` | `![Platform](https://img.shields.io/badge/platform-iOS-lightgrey?logo=ios)` |
| framework | `red` | `![Framework](https://img.shields.io/badge/framework-UIKit-red)` |
| license | `brightgreen`, linked to `LICENSE` | `[![License](https://img.shields.io/badge/license-GPL--3.0-brightgreen)](./LICENSE)` |
| OS / tool | brand color + `?logo=X&logoColor=white` | `![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)` |

Internal library/module: **no badges**. No release yet: no version badge.

### Intro

- App/tool: one factual sentence, sometimes ending in a colon that leads into a list
- Library: one sentence on what it is + 2 bullets starting with "Improve…"/"Reduce…"

### Index

- Portuguese (app/tool): a list of links, **no numbers and no heading**, right after badges/intro
- English (library/tool): `#### Index` + bullets, nesting subsections
- Short README (~3 sections or fewer): no index

## Content blocks

**Tables are the default for any listing.** Separator `|---|---|`. First column with a path or
type in backticks, linked when the file exists:

| Content | Columns |
|---|---|
| Requirements | `\| Tool \| Version \|` (badge in the first cell) or `\| **File** \| **Description** \|` |
| Folder structure | `\| Folder \| What it is \|` — purpose after an em dash |
| Commands / API | `\| Command \| What it does \|`, `\| Handler \| Purpose \|` |
| Convention | `\| Language \| When to use \|` |

- **Long catalog with link + description** (workflows, actions): HTML `<table>`, `<code>` in cells,
  descriptions starting with a third-person verb ("Validates…", "Builds…") and ending in a period
- **Code:** always with a language on the fence (`bash`, `yaml`, `swift`, `mermaid`). In `bash`,
  one `#` comment above each step, or comments aligned at the end of the line:

  ```bash
  # Run the setup (creates the venv and installs the dependencies)
  ./scripts/build.sh

  act -l              # lists the available jobs
  act -j <job>        # runs one job
  ```

- Steps per OS: bold label (`**macOS:**`) + one code block + an optional `>` tip
- Process (release, deploy): bullets with a verb in the infinitive, the result after a colon
- **Callout:** only `> [!NOTE]` (exact syntax; `> ![NOTE]` is a bug). A one-off tip after a code
  block: plain `>`
- **Architecture:** `mermaid` (`classDiagram` for libraries). Simple flow: ASCII diagram
  (`│ ▼ ←`) in a fence without language
- **Image/GIF:** `<p align="center"><img width=32% src="..."/></p>`; several side by side at 24%
- No `<details>`
- Link to another repo by its name in backticks: `` [`Other-Repo`](https://github.com/...) ``
- One-time setup at the end, under `### Setup`

## Skeleton per repo type

| Type | Sections |
|---|---|
| App (PT) | Plataforma e Requisitos → Como rodar → Gerar executável/Release → Autor |
| App (EN) | Platform & Requirements → Architecture → Modules → Demo → How to run → Author |
| Tool (PT/EN) | Requirements → Structure → Conventions → Usage → Versioning → Validation → catalog |
| Library (EN) | Architectures (mermaid) → Quick usage → `<Type>s available` (table) → Features (`### Name` + `#### How to use`) → Maintenance |
| Index/portfolio (EN) | intro → `> [!NOTE]` → About → one table per category → Author |

## Author

Always the same, 100px avatar. `Autor` (PT) / `Author` (EN); `Autores`/`Time` for a team, one
`<td>` per person. Preceded by `</br>` + `---`.

```html
## Author

<table>
    <tr>
        <td align="center">
            <a href="https://github.com/Gui25Reis">
                <img src="https://avatars1.githubusercontent.com/u/48360732" width="100px;" alt="Gui Reis's profile picture at GitHub"/><br>
                <sub>
                    <b>Gui Reis</b>
                </sub>
            </a>
        </td>
    </tr>
</table>
```

Portuguese: `alt="Foto do Gui Reis no GitHub"`, heading `## Autor`.

## Checklist before delivering

- [ ] A paragraph that lists things? → table or bullets
- [ ] A paragraph longer than 3 sentences? → cut or structure it
- [ ] Index present with 4+ sections
- [ ] Every code block has a language, and `bash` commands are commented
- [ ] `> [!NOTE]` with the right syntax
- [ ] No emoji, no exclamation marks, headings in sentence case
- [ ] Author block at the end (apps/personal repos), with `</table>` closed
