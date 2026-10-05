---
name: unit-tests
description: Writes or reviews Swift unit tests following the unit test standard (SWIFT_UNIT_TESTS) and, only where it's silent, the project's complementary conventions. Use when the user asks for unit tests, when editing a *Tests.swift file or anything in a test folder, when creating a mock, spy or stub factory, or when reviewing an existing test. Covers the scenario map, handing the writing to the unit-tests-write agent, the double check and when to run.
paths:
  - "**/*Tests.swift"
  - "**/*Tests/**"
---

# Unit tests

This skill holds **no rules**. The rules live in the unit test standard and its complementary
conventions. Here is the **order**: what to read at each step, who does what, and what not to
decide alone.

> Why the split: a rule written in two places diverges at the first fix. When a rule changes,
> this skill doesn't.

**Who does what:**

| Step | Who |
|---|---|
| Context, scenario map, production seams, double check | This session, with the user |
| Writing mocks, spies, stubs and suites | The `unit-tests-write` agent, from the approved map |
| Running the tests | The `unit-tests-run` agent — **only when the user asked for it** |

## Where the rules are — and which one wins

`SWIFT_UNIT_TESTS`, resolved by the "Named paths" order of the global instructions:

1. **The standard** — this machine's override, or the default when there's none. **It always
   wins** — it's what code review enforces
2. **Complementary conventions** the project's `CLAUDE.md` points to — only where the standard is
   silent
3. **The default**, when an override is the standard — only where both are silent

A lower source that contradicts a higher one is not applied: follow the higher one and mention the
conflict. Nothing resolves on this machine? **Stop and ask** — never write tests against your own
taste.

## 1. Before anything — load the right context

**Always, in the order above:** the standard's index and every page of it that the case
touches; then the complementary conventions and, for what's still open, the default — each from
its index and its base pages (the process and the structure of a test). Within each, every
specific page (mocks, language, architecture) **complements** the base, never replaces it.

**Depending on the case**, open the other pages using the index's **"how to use" routing tree**
(new mock? triggered by a button? testing an enum?) instead of guessing.

**Then the reference suite.** When the project lists a reference suite per kind of test (a real,
reviewed file for a tracker, a mock, a controller…), open the one for this case. Real code that
passed review beats an example in a doc: docs age, and when the two disagree **stop and ask** —
the answer usually fixes the doc. No list? Pick the closest existing suite and say which.

**Then read the production code under test — whole, not just the signature.** That's where the
real scenarios are.

## 2. The map — approved before the first line

A test validates **a business rule**, not a function. Build the map as a table and show it to the
user; nothing is written before it's approved. The map is also **what the writing agent
receives**, so it has to stand on its own.

One block per unit (usually one class under test):

- **Scenarios** — each path the rule opens (`if`/`switch`/`guard`, state that changes behavior),
  including those inside private functions: the test name, how it's triggered, and the
  observable effect with the **exact expected value**, traced in the production code
- **Doubles** — which dependencies need a mock, spy or stub, which already exist, and **which
  existing ones the change leaves stale** (a mock that discards a new argument, a stub missing
  a new field)
- **Production seams** — every change the tests need outside the test target (widened access,
  an injectable dependency, a removed `final`). Listed one by one, each with its reason
- **Shared state** (`static`, singletons, `UserDefaults`) — it decides the suite's shape
- **Stub construction** — can each model be built directly, or does its `init` need something
  heavy? Read every `init` now, not in a broken build

Before designing a protocol for a mock, survey the **other consumers** of the concrete type — or
the contract is born too narrow and gets redone.

No branching at all? Probably one scenario — don't invent variations to "cover more".

## 3. Write — handed to the `unit-tests-write` agent

**One unit per call.** The agent writes the doubles first, then the suite, then the tests, and
returns a `STATUS`.

Before calling it:

1. **Apply the approved production seams yourself.** The agent never edits production code
2. Resolve every path it needs — it doesn't know the project

What goes in the prompt:

| Field | What |
|---|---|
| `REPO` | The clone's folder |
| `PAGES` | The standard and convention pages for this unit, as file paths — the ones from step 1, including the line-length and naming rules |
| `REFERENCE` | The reference suite (and reference double) to copy the shape from |
| `PRODUCTION` | The file(s) under test |
| `TARGETS` | Every file to create or change, with its full path |
| `MAP` | This unit's block of the approved map, complete |
| `DECISIONS` | What the user already decided that the pages don't say |

What comes back:

| `STATUS` | What to do |
|---|---|
| `OK` | Step 4 on what it wrote |
| `NEEDS_DECISION` | It hit something the map doesn't answer (a missing seam, a value that doesn't match the production code). Settle it with the user, fix the map, call it again |
| `ERROR` | Read why. Don't retry blindly |

The agent unavailable, or a unit it returned twice without finishing: write it in this session,
in the same order (doubles → suite → tests), never all at once.

### Stop for approval at each unit

**Close a unit → wait for the go-ahead → next.** A unit is a cohesive, reviewable piece — usually
one class. **Never a whole module.** Changing context (done with class A, starting B)? Pause and
report first, including what was changed in production.

## 4. Double check — before saying it's done

Neither is optional, and neither is done from memory. The agent's `STATUS: OK` is not a check.

**(a) Against the rules.** Reopen the pages from step 1 and check what the agent wrote **item by
item**, in the same order — the standard first. At the end of the whole block, when the project
has a style review step (a `pre-review` cycle), run it **before** any test run: it catches the
mechanical misses reading doesn't, and fixing them after a run means running twice.

**(b) Against the production code.** Trace **line by line** the path each assertion exercises:
which overload is called, what reaches the mock, where each expected value comes from. Never
deduce from a parameter or field name.

**A green build is not (a).** Passing tests confirm it compiles and behaves as asserted — not
naming, how the test body is laid out, or which assertion form is used.

## 5. Running — only when the user asked

**No request to run, no run.** Writing tests is not a request to run them. When the work is
closed and nothing was run, say exactly that — "written, not run" — and stop.

When the user did ask:

- **At the very end, once.** Everything written, steps 1–4 done, the style review applied. Never
  after each file or each unit, never "to see if it's on track", never to answer something
  reading the code answers
- **Batch.** All the suites of the block in one command
- **Hand it to the `unit-tests-run` agent**, with `REPO`, the full `COMMAND` (scheme, simulator
  and flags come from the project's docs — missing? Ask, don't rediscover by trial) and `LOG`
- A failure comes back with the test, the message and the line. Fixing a real failure and
  running again is legitimate. Using the build as a probe isn't

## 6. What not to decide alone

Points the rules mark as **judgement, not rule**: ask, don't pick silently — and when
reviewing someone else's test, never flag them as errors.

Also never decide alone: **a change in production code** beyond the cases the rules already
list. It goes in the map, with its reason, and waits for the go-ahead.

## 7. When neither the standard nor the conventions cover the case

Expected — they grow by demand. **Ask**, solve it together, and at the end record the decision
on the right page — usually the complementary conventions, since the standard belongs to whoever
owns it — with the reason and the discarded alternative. Never invent a convention silently.

## Tests not requested

When a task doesn't ask for tests, **don't add them** — but write the code testable anyway
(injected dependencies, no hidden state, composition). A design decision taken only for future
testability is **said explicitly** to the user.
