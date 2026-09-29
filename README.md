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
- [Structure](#structure)
- [Adding to a plugin](#adding-to-a-plugin)
- [Author](#author)

## Plugins

| Plugin | Scope | Contents |
|---|---|---|
| [`kings-core`](plugins/kings-core/) | Any project | `docs-sync` agent, `readme-style` skill |

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

> [!NOTE]
> From a local clone (`claude plugin marketplace add ./Kings-AI-Platform`), edits take effect on
> the next session or with `/reload-plugins` — no reinstall. From GitHub, updates arrive with
> `claude plugin marketplace update kings-ai-platform`.

## Global instructions

Plugins can't carry always-on instructions, so [`claude-md/global.md`](claude-md/global.md) is
linked as the user's `CLAUDE.md`:

```bash
# Back up the current one, then link
mv ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak
ln -s "$PWD/Kings-AI-Platform/claude-md/global.md" ~/.claude/CLAUDE.md
```

It imports `~/.kings-ai/personal.md` — a private file with personal context, kept outside this
repo.

## Structure

| Path | What it is |
|---|---|
| [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) | The marketplace — lists every plugin |
| `plugins/<name>/.claude-plugin/plugin.json` | A plugin's manifest |
| `plugins/<name>/agents/` | Subagents, one `.md` each |
| `plugins/<name>/skills/<skill>/SKILL.md` | Skills |
| [`claude-md/`](claude-md/) | Always-on instructions, linked into `~/.claude/` |

## Adding to a plugin

- **Skill:** `plugins/<plugin>/skills/<name>/SKILL.md`, with `name` and a `description` that says
  when to use it — the description is what triggers it
- **Agent:** `plugins/<plugin>/agents/<name>.md`, with `name`, `description` and `tools`
- **Plugin:** a folder under `plugins/` with `.claude-plugin/plugin.json`, plus its entry in
  `marketplace.json`
- Check before committing: `claude plugin validate .`
- Nothing that names a company, client or person — that goes to a private marketplace

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
