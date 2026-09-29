---
name: fig-layout
description: Reads a Figma .fig file (the layout designers export) without the Figma MCP, using `kings fig-parse`. Use when the user passes a .fig path, points to a folder of extracts, or asks to "look at the Figma" of a demand. Extracts hierarchy, size, auto-layout, color, typography and text of each screen.
---

# Reading a `.fig`

This skill holds the **order**: what to run, what to open, and what not to do. The format's
details and traps are in the [`kings fig-parse` README](https://github.com/Kings-Platform/KingsScript/tree/main/Scripts/Design/Figma).

> **Nothing here renders an image.** You read the screen through the node tree and its
> properties, not a PNG. When a visual reference is essential, ask the user for an export — never
> invent what isn't in the tree.

> **Don't export icons on your own.** `--svg` works, but run it **only when the user explicitly
> asks for the icon** — never as a bonus to a layout analysis.

## 1. Find the `.fig` and extract the catalog

Files already received live in `$KINGS_FIG_DIR/figmas/` (default `~/Documents/FigExtracts/figmas/`).
When the user mentions a Figma without a path, look there before asking. New files usually land
in `~/Downloads`.

```bash
kings fig-parse <path/to/file.fig>
```

It writes to `$KINGS_FIG_DIR/<fig-name>_<date_time>/`. **Every run creates a new folder** — an
older extraction is never overwritten, so check the date before reading a folder that already
existed. Without a filter, only `index.md` (the catalog) and `thumbnail.png` come out: cheap, and
always the first step.

## 2. Read `index.md` and find the screen

It lists the pages and, per page, the top-level containers with **size and `id`**.

- **Mobile screen size** (`412x…`, `375x812`, `390x…`) is the most reliable signal — a real file
  has hundreds of top-level nodes that are annotations, arrows, test prints and library components
- **Names repeat a lot** — that's why the `id` exists: extract by `--id` whenever there's more than one
- **The page tells the intent:** `Handoff` is what was delivered to dev; `Exploration`/`Sandbox`
  are drafts; `UAT` is usually prints. **Unsure which page counts? Ask** — implementing a discarded
  exploration is the expensive mistake here

## 3. Extract the screen

```bash
kings fig-parse <file.fig> --id 209:4463                  # one screen
kings fig-parse <file.fig> --page Handoff --all-frames    # a whole page
```

| Flag | Use |
|---|---|
| `--include-hidden` | Hidden nodes — useful for alternative states |
| `--no-expand` | Don't resolve components — debugging only |
| `--images used\|all\|none` | Default `used`; `all` can copy more than 100 MB |

### SVG icon — only when asked

```bash
kings fig-parse <file.fig> --id 209:4463 --svg "Wifi"   # by name, inside the extracted screen
kings fig-parse <file.fig> --svg 182:11442              # exact id, anywhere in the file
```

Written to `icons/<name>--<sid>-<lid>.svg`. A name not found in the extracted screens falls back to the
whole page and may hit hundreds of nodes — the output lists the candidates with ids; repeat with
the id. The SVG carries comments where something was approximated (gradient reduced to its first
color, stroke alignment SVG can't express) — **read them before handing the file over**.

## 4. Read the artifacts, in this order

1. **`.tree.txt`** — the main read. One line per node: type, name, text, size, position,
   auto-layout, radius, fill, stroke, effect, font
2. **`.json`** — only for a value the tree doesn't show (font postscript, `letterSpacing`, gradient
   stops, `autoResize`). **Never dump the whole `.json` into the chat** — it passes 500 KB per screen
3. **`images/`** — the rasters referenced as `fill:image(<hash>)`; the file name is the hash

## 5. What the tree tells you, and what it doesn't

| Mark on the line | Meaning |
|---|---|
| `~` before the type | The node comes from inside a component — changing it in code means changing the component |
| `component:external-library` | Component from a library not embedded in the `.fig`. **Its content isn't in the file** — don't conclude the screen is empty there |
| `vectorPath: "unavailable"` (in the `.json`) | An icon of that size and fill exists, but its shape wasn't converted — `--svg` can convert it |
| `[truncated: maxDepth]` | The tree hit the depth limit — run again with a higher `--depth` |
| `WARNING: TRUNCATED by --max-nodes` | Screens are missing — raise `--max-nodes` |

## 6. Mistakes this skill exists to prevent

- **Assuming the first frame with the right name is the screen** — check the page and the size
- **Reading an old extraction folder as if it were current** — the folder name has date and time
- **Treating absence as fact** — `external-library` and `vectorPath: unavailable` are extractor
  limits, not missing design. Tell the user instead of guessing

## 7. When the extraction looks wrong

Run `kings fig-check`. It compares the file against a recorded baseline (node count, expanded
instances, applied overrides) and catches this format's typical silent failure: parsing on and
returning less. A divergence with no change to the extractor means Figma changed the format — tell
the user, don't work around it.
