---
name: remote-session
description: Starts a new Claude Code session that keeps running in the background (tmux) with Remote Control on, so the user can drive it from claude.ai or the phone — or reopens an existing conversation that way. Use when the user says "create a new session", "open another remote session", "start a session called X", "spin up a session for <subject>", "resume that session remotely". Runs `kings ai-session`.
---

# Remote session

The command does the work — tmux, `claude --remote-control`, the duplicate check and the
confirmation that it stayed up. Its options are in
[KingsScript](https://github.com/Kings-Platform/KingsScript) (`kings help`). This skill resolves
the three inputs and reports how to get in.

## 1. Resolve

| Input | From |
|---|---|
| **Name** | What the user called it. Short and lowercase-friendly; it is both the tmux session and the title shown in claude.ai. No name given → propose one from the subject ("carreira-2", "kingsai-pr") and use it unless the user objects |
| **Folder** | What the user said; otherwise the folder this session is working in. A project session starts at its repo root |
| **New or resumed** | New by default. "Resume", "continue that one", a session id → `--resume <id>`. Without the id, list the recent ones (`claude --resume` picker is interactive, so look in `~/.claude/projects/<folder-slug>/` for the newest `.jsonl` and confirm which with the user) |

`kings` not installed (`command -v kings` fails) → stop and say so; don't type the tmux command
by hand.

## 2. Run

```bash
kings ai-session "<name>" --dir "<folder>" [--resume <session-id>]
```

- Exit 1 with "already exists" → a session by that name is running. Offer the attach command or
  a different name; never kill the existing one.
- Exit 1 with "stopped right after starting" → Claude refused the flags or the id. Say so with the
  folder, so the user can run it by hand and see the error.

## 3. Report

One line: the name, the folder, and how to reach it — `tmux attach -t <name>` locally, or the
session titled `<name>` in claude.ai / the mobile app.

## What this skill never does

- Kill or replace a running session
- Start a session in a folder the user didn't name or isn't already working in
- Create a session to do work the user asked for here — it only opens the session
