---
name: unit-tests
description: Writes or reviews Swift unit tests following the unit test standard (SWIFT_UNIT_TESTS) and, only where it's silent, the project's complementary conventions. Use when the user asks for unit tests, when editing a *Tests.swift file or anything in a test folder, when creating a mock, spy or stub factory, or when reviewing an existing test. Covers suite structure, naming, mocks, UI action triggers and when to run the tests.
paths:
  - "**/*Tests.swift"
  - "**/*Tests/**"
---

# Unit tests

This skill holds **no rules**. The rules live in the unit test standard and its complementary
conventions. Here is the **order**: what to read at each step, and what not to decide alone.

> Why the split: a rule written in two places diverges at the first fix. When a rule changes,
> this skill doesn't.

## Where the rules are — and which one wins

1. **The standard: `SWIFT_UNIT_TESTS`** (named path — this machine's override, or the default).
   Its value is the standard's index. **It always wins** — it's what code review enforces
2. **Complementary conventions** — the ones the project's `CLAUDE.md` points to. They apply
   **only where the standard is silent**. A convention that contradicts the standard is not
   applied: follow the standard and mention the conflict

The standard doesn't resolve on this machine? **Stop and ask** — never write tests against your
own taste.

## 1. Before writing — load the right context

**Always, in this order:** the standard's index and every page of it that the case touches;
then the complementary conventions' index and its base pages (the process and the structure of a
test). Within each, every specific page (mocks, language, architecture) **complements** the base,
never replaces it.

**Depending on the case**, open the other pages using the README's **"how to use" routing tree**
(new mock? triggered by a button? testing an enum?) instead of guessing — it follows the pages
when they're added or moved, so this skill doesn't have to list them.

**Then read the production code under test — whole, not just the signature.** That's where the
real scenarios are.

A rule that cites a real file as its example: **open the file and check it matches the rule**
before applying the rule in bulk. A rule can be stale while its example is right — when they
disagree, stop and ask.

## 2. Map before the first line

A test validates **a business rule**, not a function:

- Which paths does the rule open (`if`/`switch`/`guard`, state that changes behavior)? Each is a
  scenario, including those inside private functions
- What is the observable effect of each path?
- Is shared state involved (`static`, singletons, `UserDefaults`)? It decides the suite's shape
- Which dependencies need a mock, and **which other consumers** use the same concrete type? Survey
  them before designing a protocol — or the contract is born too narrow and gets redone
- **Can each model that becomes a stub be built directly**, or does its `init` need something
  heavy (a macro-generated `Decodable`, no memberwise `init`, JSON)? Read every `init` before
  writing the stub — not in a broken build halfway through

No branching at all? Probably one scenario — don't invent variations to "cover more".

## 3. Write — in three separate steps

**Never all three at once:**

1. **Mocks** — create what's missing (mock, spy, stub factory)
2. **The test class** — suite, `sut`, `init`, `deinit` when there's state, using step 1's mocks
3. **The tests** — the scenarios from the map

Each step fails differently (compile / runtime / assertion); together, diagnosis gets expensive
and review can't be sliced. Two things often forgotten, both in the rules: **assertion
messages** and **extracting a private helper when a block repeats**.

> Creating mocks is mechanical once the contract is known — it can run while the deep analysis of
> **another** case goes on. The three steps **within one case** never run in parallel.

### Stop for approval at each unit

**Close a unit → wait for the go-ahead → next.** A unit is a cohesive, reviewable piece — usually
one class, or one of the steps above when the case is big. **Never a whole module.** Changing
context (done with class A, starting B)? Pause and report first.

## 4. Double check — before saying it's done

Neither is optional, and neither is done from memory:

**(a) Against the rules.** Reopen the pages from step 1 and check **item by item** — the
standard first, then the complementary conventions.

**(b) Against the production code.** Trace **line by line** the path each assertion exercises:
which overload is called, what reaches the mock, where each expected value comes from. Never
deduce from a parameter or field name.

**A green build is not (a).** Passing tests confirm it compiles and behaves as asserted — not
naming, how the test body is laid out, `#require` vs `#expect`, or "never compare a raw string".
The feeling of "all green, done" is exactly the trigger to run (a) on purpose. Closing a unit
means running (a) and (b) again on what it added, even when green.

## 5. Running — only when needed, only at the end

Building tests is slow. Running is the final step, not a routine check — and an earlier
permission approval is not a license to run whenever.

**Run only when both hold:**

1. The work is closed — everything written, steps 1–4 done
2. There's a question only running answers — does it compile, pass, exercise the intended path?

**Never run** after each file or small fix, "to see if it's on track", to answer something reading
the code answers (that's step 4), or as a substitute for the review.

**How:**
- **Batch, don't iterate.** Three suites written: verify the three, run **once**
- **Say beforehand what will run and why** — the user may prefer to run it in Xcode
- The command (scheme, simulator, flags) comes from the project's docs; missing? Ask — don't
  rediscover it by trial
- Fixing a real failure and running again is legitimate. Using the build as a probe isn't
- A failure the `xcodebuild` log doesn't explain: read the **xcresult** — the log swallows the
  cause, and reading it needs no new build

## 6. What not to decide alone

Points the rules mark as **judgement, not rule**: ask, don't pick silently — and when
reviewing someone else's test, never flag them as errors.

Also never decide alone: **widening access in production code** (`private` → `private(set)`,
exposing an outlet) beyond the cases the rules already list. That's production scope.

## 7. When neither the standard nor the conventions cover the case

Expected — they grow by demand. **Ask**, solve it together, and at the end record the decision
on the right page — usually the complementary conventions, since the standard belongs to whoever
owns it — with the reason and the discarded alternative. Never invent a convention silently.

## Tests not requested

When a task doesn't ask for tests, **don't add them** — but write the code testable anyway
(injected dependencies, no hidden state, composition). A design decision taken only for future
testability is **said explicitly** to the user.
