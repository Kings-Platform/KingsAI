---
name: swift-code-style
description: Applies the Swift code style when writing or changing Swift code — enums, extensions, protocols, list model equality, localized strings, view tags, and how screens are structured (ViewCode). Use when writing or editing .swift files, creating a screen or view controller, or when asked whether some Swift code follows the style.
paths:
  - "**/*.swift"
---

# Swift code style

This skill holds **no rules** — only where they are and how to apply them.

## Where the style is

`SWIFT_STYLE_GUIDE`, resolved by the "Named paths" order of the global instructions:

1. **The standard** — this machine's override, or the default when there's none. **It wins** on
   everything it covers
2. **Conventions** the project's `CLAUDE.md` points to — only where the standard is silent
3. **The default**, when an override is the standard — only where both are silent

A lower source that contradicts a higher one is **not** applied — mention the conflict instead.

## How to apply

1. **Start from the index and load only what the change touches.** The index says which page
   covers what: a new enum → the enums page; a protocol conformance → extensions and protocols;
   a string shown to the user → localized strings. Don't read every page for a one-line change
2. **New screen or view controller:** the guide's page on how screens are built, when it has
   one. **The project's existing pattern wins** over the guide's default: follow what's there
3. **Write to the rule, not to the example next to it.** Nearby code may predate the rule — the
   style applies to new code and to code the task touches, never as a license to sweep the file
4. **A rule that cites a real file as its example:** check the file matches before applying the
   rule in bulk; when they disagree, ask

## When reviewing

Reviewing a whole diff against the style is the `kings-core:style-review` agent's job, through
the `kings-core:pre-review` skill — this skill is for writing.
