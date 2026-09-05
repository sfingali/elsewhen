# CHANGELOG — v2.3 implementation

## Removed / replaced (v1 -> v2.3)

- No v1 code paths deleted yet: `tools/universe_graph.py` retains its v1 `validate()` and
  example charts (byte-exact per house rule). The v2.3 stack lives beside it:
  `build/schema_v2.json` (frozen contract), `build/semantic_validate.py` (E-series),
  `build/v23_adapter.py` (fixture -> engine).
- v1's implicit "universe = lane" convention is superseded for fixtures: lanes now come
  from explicit `layout.lane_order`, origins from `origin` kinds, threads from authoritative
  `thread.visits` (adapter), not lane heuristics.
- Survivor census (v1 `meta.travellers` auto-count) is NOT used by any v2.3 fixture
  (fabricated counts prohibited); the census code path remains for legacy charts only.

## Added

- D1 `build/schema_v2.json` + verifier: draft 2020-12, 69 defs, closed object types,
  envelope enforcement (schema_version 2, specification_revision 2.3, interpretation_profile).
- D2 `build/semantic_validate.py`: two-phase (schema -> semantics) validator, exit-2
  convention; E030-E251 coverage incl. split outcome coverage (E080-E087), transfer/traversal
  coherence (E110-E119), authoritative thread continuity (E130-E146), profile guards
  (E201, E240-E249), genealogy bootstrap cycles.
- D2 `build/test_semantic.py` + 12 negative fixtures: 13/13 pass (each bad doc exits 2 with
  its exact code; no tracebacks; positive Ben's Story exits 0).
- D3 `build/v23_adapter.py` + `--fixture` CLI: fixture -> renderer adaptation with profile
  chips, thread-route chrome, origin stars/chips for preexisting lanes, letter-capped split
  circles; P4 would get the mandatory ONTOLOGY UNDECLARED chip (no P4 fixture yet).
- D4 fixtures + renders: bens_story (P1+waif), groundhog (P3), bttf2 (P2), tenet (tenet),
  dark (dark), steinsgate (steins-gate) - all validate rc=0, all render PNGs in build/render/.

## Verification

- `build/test_semantic.py`: 13/13.
- `build/semantic_validate.py build/fixtures/*.json`: rc=0 for all six.
- Vision checks on all rendered PNGs (profile chip, thread route, segments, fates, footer).
