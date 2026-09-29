# Kings AI Platform

![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?logo=claude&logoColor=white)
[![License](https://img.shields.io/badge/license-GPL--3.0-brightgreen)](./LICENSE)

</br>

A [Claude Code](https://code.claude.com) marketplace with reusable agents and skills, one
**plugin** per context — the same idea as [KingsScript](https://github.com/Kings-Platform/KingsScript)
layers, using Claude Code's own plugin system.

- Improve reuse: agents and skills written once, installed on every machine.
- Improve focus: each context (generic, a stack, a company) is a plugin enabled only where it applies.

#### Index

- [Plugins](#plugins)
- [Install](#install)
- [Global instructions](#global-instructions)
- [Project conventions](#project-conventions)
- [Structure](#structure)
- [Adding to a plugin](#adding-to-a-plugin)
- [Validating](#validating)
- [Author](#author)

## Plugins

| Plugin | Scope | Contents |
|---|---|---|
| [`kings-core`](plugins/kings-core/) | Any project | See below |
| [`kings-swift`](plugins/kings-swift/) | Swift and iOS projects | See below |

**`kings-core`:**

| Component | Type | What it does |
|---|---|---|
| [`docs-sync`](plugins/kings-core/agents/docs-sync.md) | Agent | Keeps the project's living docs in sync with what a session delivered |
| [`style-review`](plugins/kings-core/agents/style-review.md) | Agent | Reviews the diff against the written standard — reports, never edits |
| [`pre-review`](plugins/kings-core/skills/pre-review/SKILL.md) | Skill | The cycle around `style-review` before human review |
| [`code-review-analysis`](plugins/kings-core/skills/code-review-analysis/SKILL.md) | Skill | A round of PR review comments, recorded in `CR-<PR>.md` |
| [`new-demand`](plugins/kings-core/skills/new-demand/SKILL.md) | Skill | Opens a demand: inputs, context, doc with Timeline, plan |
| [`readme-style`](plugins/kings-core/skills/readme-style/SKILL.md) | Skill | README standard |
| [`fig-layout`](plugins/kings-core/skills/fig-layout/SKILL.md) | Skill | Reads a Figma `.fig` with [`kings fig-parse`](https://github.com/Kings-Platform/KingsScript) |

**`kings-swift`** — reads the style guide named `SWIFT_STYLE_GUIDE` in the paths map, unless the
project has its own:

| Component | Type | What it does |
|---|---|---|
| [`unit-tests`](plugins/kings-swift/skills/unit-tests/SKILL.md) | Skill | Writes and reviews unit tests: map, three steps, double check, when to run |
| [`swift-code-style`](plugins/kings-swift/skills/swift-code-style/SKILL.md) | Skill | Applies the code style and screen structure while writing Swift |

Company-specific plugins live in their own private marketplaces, installed next to this one.

## Install

```bash
# Add the marketplace (or a local clone, to edit plugins in place)
claude plugin marketplace add Kings-Platform/Kings-AI-Platform

# Install a plugin — user scope: every project on this machine
claude plugin install kings-core@kings-ai-platform --scope user
```

| Scope | Where it applies | Setting |
|---|---|---|
| `user` | Every project on the machine | `~/.claude/settings.json` |
| `project` | Everyone in a repo | `<repo>/.claude/settings.json` |
| `local` | Only you, in a repo | `<repo>/.claude/settings.local.json` |

Components are namespaced by plugin: the agent is `kings-core:docs-sync`.

Installed plugins are **copied to a cache, pinned to a commit** — editing the source changes
nothing until an update:

```bash
# From GitHub: fetch the marketplace, then update the plugin
claude plugin marketplace update kings-ai-platform
claude plugin update kings-core@kings-ai-platform

# From a local clone: commit, then update — it takes the commit checked out, even on a branch
claude plugin update kings-core@kings-ai-platform
```

With [KingsScript](https://github.com/Kings-Platform/KingsScript), `kings ai-update` does all of it,
and its daily checkup runs it by itself — skipping a local clone that isn't clean and on its
default branch.

> [!NOTE]
> An update applies to new sessions — restart the running ones.

## Global instructions

Plugins can't carry always-on instructions, so [`claude-md/global.md`](claude-md/global.md) is
linked as the user's `CLAUDE.md`. It imports two private files, kept outside this repo:

| File | What it holds |
|---|---|
| `~/.kings-ai/personal.md` | Personal context — who you are, how you like to work |
| `~/.kings-ai/paths.md` | Where things live **on this machine**, by name — skills cite the name, each machine sets the path |

```bash
# Links ~/.claude/CLAUDE.md to global.md (the previous one is kept as .bak) and creates the two
# private files from their templates, if missing
./Kings-AI-Platform/install/install.sh
```

Move what's personal from the `.bak` into `personal.md` — the template says what goes where.

## Project conventions

Skills and agents carry no project paths. They read the project's `CLAUDE.md` for what they need,
and fall back to a default when it's silent:

| The skills need to know | Default when `CLAUDE.md` doesn't say |
|---|---|
| Docs folder | `.ai/`, or `docs/` when that's already the convention |
| Index of work (demands and their status) | `demandas/README.md` in the docs folder |
| Where a demand's docs live | `demandas/<name>/` |
| Style guide and conventions | `style-guide/` and `conventions/` in the docs folder |
| Branching model and a branch's base | Never assumed — asked |
| Who commits and opens PRs | The user; the AI drafts |
| Building or running the app | Not allowed — static checks only |
| Extra steps (ticket fields, notifications) | None |
| A shared guide outside the repo | A **name** from the paths map (`SWIFT_STYLE_GUIDE`) — never a machine path |

A company or project plugin adds its own specifics on top — never by editing `kings-core`.

## Structure

| Path | What it is |
|---|---|
| [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) | The marketplace — lists every plugin |
| `plugins/<name>/.claude-plugin/plugin.json` | A plugin's manifest |
| `plugins/<name>/agents/` | Subagents, one `.md` each |
| `plugins/<name>/skills/<skill>/SKILL.md` | Skills |
| [`claude-md/`](claude-md/) | Always-on instructions, linked into `~/.claude/` |
| [`install/`](install/) | Links the instructions and creates the personal file from [`personal.example.md`](install/personal.example.md) |

## Adding to a plugin

- **Skill:** `plugins/<plugin>/skills/<name>/SKILL.md`, with `name` and a `description` that says
  when to use it — the description is what triggers it
- **Agent:** `plugins/<plugin>/agents/<name>.md`, with `name`, `description` and `tools`
- **Plugin:** a folder under `plugins/` with `.claude-plugin/plugin.json`, plus its entry in
  `marketplace.json`
- Nothing that names a company, client or person — that goes to a private marketplace

## Validating

```bash
# Manifests
claude plugin validate .
claude plugin validate plugins/kings-core

# Install in a throwaway config, so the real ~/.claude stays untouched
export CLAUDE_CONFIG_DIR="$(mktemp -d)"
claude plugin marketplace add ./Kings-AI-Platform
claude plugin install kings-core@kings-ai-platform --scope user
claude plugin list
```

</br>

---

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
