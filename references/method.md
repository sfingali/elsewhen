# Production method

How to take a time-travel screenplay from zero to a finished universe chart.
This is the process used on THE WAIF; it generalises.

## Stage 1 — ground truth

1. Get the screenplay in text form (fountain ideal). If scenes aren't numbered,
   insert `#N#` markers at every slugline so every future claim can cite.
2. Watch/read for the **splitting acts**: every moment the world forks (a death
   cheated, a jump, a trigger pull). List them in story order with scene
   numbers. In most films these are 3–6 events, not one per time-travel beat —
   count *world forks*, not effects shots.
3. Decide the **ontology** with the director before drawing anything:
   - Do splits branch or overwrite? (This tool assumes: branch. If the film
     truly resets, this is the wrong tool.)
   - Do joined worlds pre-exist? (Assumed: yes — "backpropagation".)
   - Who is the chart ABOUT? One protagonist per chart. Other characters'
     jumps are separate graphs.
   - Where does the chart END? Ending on the final split is often stronger
     than drawing the final world out.

## Stage 2 — the allocation file

4. One lane per universe the protagonist occupies. Order so each crossing hops
   exactly one lane left, opening universe rightmost.
5. Write the allocation file (syntax in `tools/timeline_compile.py`): lane
   ranges in scene numbers, `pulls:` = crossing scenes in story order,
   `split:` = non-crossing forks, `key:` beats for anything that must appear.
6. Compile; fix allocation errors (missing ranges, wrong pull count) — the
   compiler refuses to guess.

## Stage 3 — scene allocation discipline

7. Allocate EVERY scene of the protagonist's thread to exactly one lane:
   - framed present-action scenes → the lane where they happen;
   - a story told to the protagonist (porch stories, interviews) → the lane
     where they LISTEN, not the flashback content;
   - flashbacks with no protagonist present → NOT on this chart at all (they
     belong to another character's graph);
   - keep a flagged list of ambiguous scenes and settle each with the
     director — never guess into the chart.
8. Record the allocation in a plain-text file the director can read and edit.
   It is the source of truth; the JSON is compiled from it.

## Stage 4 — render + QA

9. Render all four styles from the one JSON. Pick the style that matches the
   use: `classic` for reference, `dash` when pre-history must be visible,
   `tape` for pitch decks, `weight` for print.
10. QA loop (automate the boring half):
    - vision pass: collisions, clipped labels, joins dodging text, stub boxes
      not overlapping captions;
    - pixel checks: dashed pre-history actually dashed (paint-duty fraction
      < 0.75), thread solid (> 0.85) — eyeballs lie about strokes;
    - validator negative tests: feed the engine a join in the wrong lane, an
      unknown id, a duplicate join listing — demand exit 2 every time.
11. Iterate with the director on ONTOLOGY corrections (lane order, numbering,
    what ends the chart), not on drawing. All changes flow: allocation →
    compile → render. A PNG is never edited.

## Stage 5 — companions

12. Keep the event ledger JSON (every beat: scene cite, universe, event) next
    to the chart. Charts show structure; ledgers prove it.
13. If the film has a second graph (another character's jumps, before-lives),
    give it its own allocation file and chart. Cross-reference by name, never
    by merging lanes.
