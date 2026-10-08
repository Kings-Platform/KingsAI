# KingsAI

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
- [Structure](#structure)
- [Adding to a plugin](#adding-to-a-plugin)
- [Validating](#validating)
- [Author](#author)

## Plugins

Each plugin has a page in the [wiki](https://github.com/Kings-Platform/KingsAI/wiki) — the source of truth for what it does and how its
pieces fit.

| Plugin | Scope | Documentation |
|---|---|---|
| [`kings-core`](plugins/kings-core/) | Any project: living docs, style review, code review rounds, new demands, README style, Figma files | [wiki](https://github.com/Kings-Platform/KingsAI/wiki/kings-core) |
| [`kings-swift`](plugins/kings-swift/) | Swift and iOS: code style and unit tests, driven by the `SWIFT_STYLE_GUIDE` and `SWIFT_UNIT_TESTS` named paths | [wiki](https://github.com/Kings-Platform/KingsAI/wiki/kings-swift) |
| [`kings-career`](plugins/kings-career/) | Job search as an operation, driven by the `CAREER_PROFILE` named path | [wiki](https://github.com/Kings-Platform/KingsAI/wiki/kings-career) |

Company-specific plugins live in their own private marketplaces, installed next to this one.

## Install

```bash
# Add the marketplace (or a local clone, to edit plugins in place)
claude plugin marketplace add Kings-Platform/KingsAI

# Install a plugin — user scope: every project on this machine
claude plugin install kings-core@kingsai --scope user
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
claude plugin marketplace update kingsai
claude plugin update kings-core@kingsai

# From a local clone: commit, then update — it takes the commit checked out, even on a branch
claude plugin update kings-core@kingsai
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
| `~/.kings-ai/paths.md` | This machine's **path overrides** — see [Named paths](#named-paths) |

```bash
# Links ~/.claude/CLAUDE.md to global.md (the previous one is kept as .bak) and creates the two
# private files from their templates, if missing
./KingsAI/install/install.sh
```

Move what's personal from the `.bak` into `personal.md` — the template says what goes where.

### Named paths

Skills cite a **name** instead of a path. Each value points to an **index** (`README.md` /
`index.md`) that maps the pages behind it.

| File | Role |
|---|---|
| [`claude-md/paths.md`](claude-md/paths.md) | **Defaults** — every name, pre-mapped to its original source. Ships with the repo |
| `~/.kings-ai/paths.md` | **Overrides** — only the names that differ on this machine; each becomes the standard for its name |

**Order, topic by topic:** the override is the standard and wins on what it covers; conventions
the project's `CLAUDE.md` points to fill its gaps; the default fills what's left — and is the
standard when there's no override. `global.md` holds only this rule and imports both files (the
defaults through the link `~/.kings-ai/paths.default.md`, created by the install).

A work machine pointing the Swift skills to the company's own guide:

```markdown
| Name | Path |
|---|---|
| `SWIFT_STYLE_GUIDE` | `~/Repos/docs/StyleGuide/README.md` |
| `SWIFT_UNIT_TESTS` | `~/Repos/docs/StyleGuide/unit-tests/README.md` |
```

A name that resolves to a missing file is asked for, never guessed. New name: add it to
`claude-md/paths.md` with its default.

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
- Document it in the [wiki](https://github.com/Kings-Platform/KingsAI/wiki): the README only lists the plugins

## Validating

```bash
# Manifests
claude plugin validate .
claude plugin validate plugins/kings-core

# Install in a throwaway config, so the real ~/.claude stays untouched
export CLAUDE_CONFIG_DIR="$(mktemp -d)"
claude plugin marketplace add ./KingsAI
claude plugin install kings-core@kingsai --scope user
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
