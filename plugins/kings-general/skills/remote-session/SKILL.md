---
name: remote-session
description: Starts a new Claude Code session that keeps running in the background (tmux) with Remote Control on, so the user can drive it from claude.ai or the phone — or reopens an existing conversation that way. Use when the user says "create a new session", "open another remote session", "start a session called X", "spin up a session for <subject>", "resume that session remotely" — and brings back the ones that dropped: "resume the remotes", "bring my remote sessions back", "the remote sessions are offline", "retoma os remotes", "volta as sessões remotas". Runs `kings ai-session` / `kings ai-resume`.
---

# Remote session

The command does the work — tmux, `claude --remote-control`, the duplicate check and the
confirmation that it stayed up. Its options are in
[KingsScript](https://github.com/Kings-Platform/KingsScript) (`kings help`). This skill resolves
the three inputs and reports how to get in.

## Bringing sessions back

Every session `kings ai-session` starts is recorded (tmux name, title, folder, conversation id), so
"bring the remote sessions back" needs no input:

```bash
kings ai-resume --restart [name...]
```

- No names → all recorded sessions; names match the tmux name or the title.
- A session that is gone is started again on its conversation. One still running but idle is
  restarted — that's the case after a sign-in expires: the process stays up with Remote Control
  off. A busy one is left alone and reported; say which.
- `claude auth status` says `loggedIn: false` → the restart won't reconnect anything. Stop and ask
  the user to sign in first (`claude auth login`); never sign in for them.
- A name the user mentions that isn't recorded → it wasn't started by `kings ai-session`. Say so;
  don't guess an id.
- A session the user closed for good → `kings ai-resume --forget <name>`, only when they ask.

Report one line per session: back, already running, or left running because it was busy.

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

- Kill or replace a running session — the only restart is `kings ai-resume --restart`, which skips
  busy sessions, and only when the user asked to bring the remote sessions back
- Start a session in a folder the user didn't name or isn't already working in
- Create a session to do work the user asked for here — it only opens the session
