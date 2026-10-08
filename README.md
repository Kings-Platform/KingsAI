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
| [`kings-career`](plugins/kings-career/) | Job search | See below |

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

**`kings-swift`** — reads the named paths `SWIFT_STYLE_GUIDE` and `SWIFT_UNIT_TESTS`, in the
[named path order](#named-paths): the machine's override is the standard, the project's
conventions complement it, the default fills what's left:

| Component | Type | What it does |
|---|---|---|
| [`unit-tests`](plugins/kings-swift/skills/unit-tests/SKILL.md) | Skill | The order of a unit test task: context, approved scenario map, writing handed to the agent, double check, when to run |
| [`unit-tests-write`](plugins/kings-swift/agents/unit-tests-write.md) | Agent | Writes the doubles and the suite of one unit from the approved map — never touches production code, never runs |
| [`unit-tests-run`](plugins/kings-swift/agents/unit-tests-run.md) | Agent | Runs an assembled test command and reports per test — only when the user asked for a run |
| [`swift-code-style`](plugins/kings-swift/skills/swift-code-style/SKILL.md) | Skill | Applies the code style and screen structure while writing Swift |

**`kings-career`** — job search as an operation. Reads the candidate's private profile through
the named path `CAREER_PROFILE` (facts, rules, form answers, templates, pipeline); the plugin
holds only the procedures. Details, flow and the autonomy table in its
[README](plugins/kings-career/README.md):

| Component | Type | What it does |
|---|---|---|
| [`job-intake`](plugins/kings-career/skills/job-intake/SKILL.md) | Skill | Entry point for a posting link: screen, duplicate check, fit by the rules, route |
| [`ats-apply`](plugins/kings-career/skills/ats-apply/SKILL.md) | Skill | Applies through an ATS form, with a playbook per platform and the answer bank |
| [`application-email`](plugins/kings-career/skills/application-email/SKILL.md) | Skill | Applies by email, CV attached, through the profile's send command |
| [`linkedin-outreach`](plugins/kings-career/skills/linkedin-outreach/SKILL.md) | Skill | Invitation with note or DM, from the templates, within the weekly budget |
| [`reply-drafter`](plugins/kings-career/skills/reply-drafter/SKILL.md) | Skill | Drafts a reply to a recruiter — sent only after approval |
| [`inbox-triage`](plugins/kings-career/skills/inbox-triage/SKILL.md) | Skill | Sorts recent email and updates the pipeline |
| [`interview-prep`](plugins/kings-career/skills/interview-prep/SKILL.md) | Skill | Topics, STAR stories, audio scripts, platform rules — prepares, never impersonates |
| [`job-screener`](plugins/kings-career/agents/job-screener.md) | Agent | Reads a posting and returns a structured card — read-only |
| [`form-filler`](plugins/kings-career/agents/form-filler.md) | Agent | Fills and submits one ATS form from a playbook and resolved answers |
| [`pipeline-keeper`](plugins/kings-career/agents/pipeline-keeper.md) | Agent | The only writer of the pipeline, one row per action |

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
| A shared guide outside the repo | A [named path](#named-paths) (`SWIFT_STYLE_GUIDE`) — never a machine path |

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
