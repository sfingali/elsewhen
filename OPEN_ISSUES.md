# OPEN ISSUES — v2.3 implementation

Honest gaps found while executing fixtures. Nothing here was silently weakened.
Each item names the diagnostic that exposed it.

## From the adversarial pass (carried forward)

- **E257 boundary double-count (Tenet):** a turnstile crossing charts both an exit and an
  entry event; interval counts can double-count the traveller during overlap windows.
  Fixture `tenet.json` records both events; counting semantics remain open.
- **E258 pincer coordination under-check (Tenet):** red/blue team coordination is charted
  as narrative beats; the validator cannot prove participants actually connect. Threads in
  the fixture are narrative, not semantically proven.
- **E214 revision continuity (BTTF2 P2):** the P2 reading of alt-1985 works, but costs remain:
  Marty is present in 1955 across both rA and rB simultaneously; Old Biff's return leg
  (2015 -> unchanged 2015) is unexplained in the film and uncharted. Recorded in fixture
  assumptions; a full account needs R4/R5 (route vs world-state separation, honest gaps).

## Found during fixture execution

- **Genealogy-cycle render:** Dark's Charlotte<->Elisabeth bootstrap validates as
  `genealogy_cycles` (kind: bootstrap) but the D3 renderer has no cycle glyph; the pair
  renders only as beats + fates. Cycle visualization is unimplemented.
- **Single-lane header:** P2/P3/P4 charts render one lane without a visible lane-ID header
  (the 8-lane P1 charts have IDs via lane labels). Cosmetic; flagged by vision check on
  groundhog/bttf2/steinsgate renders.
- **E244 guard asymmetry:** P1 forbids revision machinery, but presets (`tenet`, `dark`,
  `steins-gate`) use BOTH branching lanes and revision semantics where their films demand it
  (Steins;Gate has one world + revisions; Tenet has lanes + per-strand direction). The
  validator currently permits this for presets only; the rule should be profile-parameterized,
  not preset-blessed.
- **Divergence metric not validated:** revision `divergence` values (Steins;Gate) are
  charted but unconstrained - the validator does not check monotonicity or the 1% barrier
  crossing; attractor-field semantics live in canon prose only.
- **`transfers[].traversal` for time_travel:** Tenet inversions use mechanism time_travel
  with NO traversal field (consciousness stays with the body, both move). E118 only constrains
  time_leap. A `gated-inversion` traversal arm from v2.2 (R6) is not yet wired in the frozen
  schema enum (schema has body|memory|signal|object).

## Renderer legacy (v1 engine)

- Lane header boxes for P1 charts reuse lane labels (with origin stars) rather than the
  spec's dedicated header primitive - acceptable but not spec-exact (R1 capability table).
- Loop rectangles (`interval`) ignore `timescale` in adapted fixtures (v1 limitation carried
  through the adapter; no fixture currently exercises it).
