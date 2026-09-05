# Output redesign — Pass 1 decisions (Claude, 2026-09-05)
Source: subscription design pass over .claude/brief-pass1.md. Implementation split:
pass 2a = additive schema fields (#2-#7) + density flag (#8); pass 2b = horizontal
orientation (#1, largest architectural item, touches shared layout core).

# Timeline engine output redesign — Pass 1 decisions

Read: reference README (8 lessons), schema, chart-language, `universe_graph.py`, 3 reference images, demo-classic.png, `primer.universes.json`. No code touched.

## Decisions

**1. Orientation — engine mode (a), vertical stays canonical default.**
`--orientation horizontal|vertical` (default `vertical`). Rationale: rotation is a *reading choice* per audience, not a story fact — the same JSON should support both, which is the brief's whole premise. Risk to fixed-point restack: nearly everything in `build()` is hardcoded to the Y-axis (`lane_y` cursor, `JOIN_DROP`, `q_extent*`, self-lane loop bulge direction, stub `cx+92` offset, text-wrap width keyed to `LANE_W`). Horizontal mode isn't a small flag — it needs layout expressed in lane-relative coordinates (position-along-lane, offset-across-lane) with a single transpose at draw time, not a parallel code path. Flag for pass 2 as the largest architectural item. The 4 test JSONs need zero changes; they simply gain a second render mode.

**2. Loop-rectangle primitive — schema field (b), opt-in per arc.**
Add optional `interval: [depart, arrive]` to an arc definition. When present, engine draws the Clawz114 staple-rectangle (enter at depart, box encloses duration, re-emerge earlier) instead of the elbow arc; when absent, current elbow-arc rendering is unchanged — **zero risk to existing films**, none of which set `interval` today. Geometric duration needs a shared scale, so this drags in `meta.timescale` (a unit-per-pixel or start/end range) — without it, `[depart, arrive]` numbers have nothing to measure against. Decide the timescale is also opt-in: no `meta.timescale` → `interval` is rejected at validation (exit 2), forcing stories to declare their time axis before claiming duration-as-geometry.

**3. Screen-presence — schema field (b) on beats, `screen: "film"|"flashback"|"deduced"`.**
Renders as a small yellow chip (UnrealityMag device). Default absent = no chip, no layout change → existing films unaffected. Carried by all four styles: it's content (an evidentiary claim about the beat), not a style device, so hiding it in `dash`/`tape` would be lying by omission, which the canon forbids ("uncertainty gets its own row/label").

**4. Epistemic colour — schema field (b) on beats, `certainty: "seen"|"flashback"|"seen-later"|"never-shown"`.**
Default absent = current grey dot (unchanged). Maps to Clawz114's grey/blue/green/red. Which styles carry it: `classic`/`weight` render full colour (they're already colour-forward); `dash`/`tape` are deliberately reduced-palette/line-art styles, so carry it as a letter glyph (S/F/L/N) next to the dot instead of colour — decide this now so pass 2 doesn't silently drop the signal in two of four styles.

**5. Version counters — schema field + opt-in engine behavior (b), `meta.versioning: "crossing-count"`.**
This needs identity, not just a flag: introduce `meta.travellers: {"Aaron": "#color"}` (also serves BTTF2/ClickHole per-traveller colour) and a `traveller: "Aaron"` field on beats/arcs. When `versioning: "crossing-count"` is set, the engine auto-suffixes that traveller's label with `(n)` = ordinal count of their arc departures/marks seen so far in story order — replacing hand-typed `Aaron(2)` with a computed one. Default off; absent `meta.travellers` → no change to the 4 existing films (none declare travellers today).

**6. Honesty devices — mostly default/no-op (c), one schema field.**
- Compressed "11+" row and runtime-as-cite: already expressible with existing `segment`/`lane` labels and the free-text `cite` string — no engine change, just a convention note added to `chart-language.md` in pass 2 (cite runtime `"46:32"` where no scene number exists).
- "?" terminal row: needs one new flag, `{"ending": {..., "uncertain": true}}` (schema field, b) — renders the ending box dashed/grey with "?" instead of green, so uncertainty gets its own visually distinct terminal state rather than reusing the confident-green ending box. Default false, unchanged rendering.

**7. Survivor census — engine feature (a), computed and auto-appended.**
Only meaningful once `meta.travellers` exists (needs identity to count copies). When present, `build()`/`validate()` computes "2× Abe, 3× Aaron alive at the ending" from traveller occupancy at the thread's terminal point and appends it as an auto-generated legend line after the author's own lines. If `meta.travellers` is absent, skip silently — the 4 existing films define no travellers, so this is inert for them, not a regression. Output form deliberately chosen as legend text, not a separate UI element — it's cheap, matches the existing "Index / How to Read" box, and needs no new drawing code.

**8. Density/white space — engine mode (a), NOT a default change.**
The reference charts are denser because of tighter vertical rhythm, smaller lane gaps, and closer stub anchoring — but `B` (breathing factor), `LANE_GAP`, and `SLOTS` are global constants shared by all styles today. Changing them in place would silently re-flow the 4 existing test films' pixel output, violating "must still render unchanged." Decide: add `--density compact|normal` (default `normal` = current constants, byte-identical output); `compact` scales `B` down, shrinks `LANE_GAP`, and pulls the stub offset in, as a second tuning profile pass 2 can dial in against the references without touching the approved look.

## Schema delta (additive only — nothing existing changes shape)

```jsonc
"meta": {
  "timescale": { "unit": "hour", "start": 0 },      // required IF any arc uses interval
  "versioning": "crossing-count",                    // opt-in
  "travellers": { "Aaron": [79,140,214] }            // name -> color; enables #5, #7
}
"arcs": {
  "run1": {
    "interval": [15, 9],          // [depart, arrive] on meta.timescale units -> loop-rectangle (#2)
    "traveller": "Aaron"          // ties arc to a travellers[] entry (#5)
  }
}
// beat item, extended:
{"beat": "...", "cite": "#16", "screen": "film|flashback|deduced",   // #3
 "certainty": "seen|flashback|seen-later|never-shown",                // #4
 "traveller": "Aaron"}                                                 // #5
// ending item, extended:
{"ending": {"title": "...", "body": "...", "cite": "#277", "uncertain": true}}  // #6
```

CLI: `--orientation horizontal|vertical` (default `vertical`, #1), `--density compact|normal` (default `normal`, #8). Both flags, both backward-compatible no-ops when unset.

**Breakage check against the four test films:** none of them set `interval`, `screen`, `certainty`, `meta.versioning`, `meta.travellers`, or `ending.uncertain`, and default CLI flags reproduce current constants exactly — all four should render pixel-identical until pass 2 opts a story into a new field. The one item that needs care in implementation, not design, is #1 (orientation): it's the only decision that touches the shared layout core rather than adding a new opt-in leaf field.
