# v2.3 Implementation Report — film-universe-timelines

## What shipped

The v2.3 data model is implemented and executed end-to-end:
**spec (Astra, adversarially survived) -> frozen JSON Schema -> semantic validator ->
fixtures -> rendered charts.**

| Deliverable | Artifact | Status |
|---|---|---|
| D1 Frozen schema (R1) | `build/schema_v2.json` (69 defs, draft 2020-12) | compiles; rejects v1 docs with exact envelope errors |
| D2 Semantic validator | `build/semantic_validate.py` | two-phase; exit-2 + exact E-codes |
| D2 Negative suite | `build/test_semantic.py` + 12 bad docs | **13/13 pass** |
| D3 Renderer bridge | `build/v23_adapter.py` + `--fixture` mode | profile chip, thread chrome, origin stars |
| D4 Fixtures x6 | `build/fixtures/*.json` | **all validate rc=0** |
| D4 Renders x6 | `build/render/*-classic.png` | all vision-verified |

## Fixture coverage (the six-encoding adversarial matrix)

| Film | Profile | Key machinery exercised | Adversarial disposition |
|---|---|---|---|
| Ben's Story | P1 + waif | born/preexisting origins, per-tine outcomes, consciousness transfers, namespace isolation, thread U1->J+->*2->J--->*F | regression control - validates UNCHANGED canon |
| Groundhog Day | P3 | one-world loop, revision ladder r0->r2, memory-persist thread, no P1 machinery | E241/E243 guards hold |
| BTTF2 | P2 | alt-1985 as superseded revision (rA->rB->rC), body-travel as revision navigation | the v2.2 counterexample now encodes |
| Tenet | tenet | inverted strands as lanes, turnstile splits, pincer as narrative | E257/E258 open, honestly logged |
| Dark | dark | era lanes, cave transfers, bootstrap genealogy cycle | cycle render open |
| Steins;Gate | steins-gate | divergence revisions, memory-only traversal, attractor convergence | metric unconstrained (logged) |

## How to use

    # validate any fixture (schema + semantics)
    /tmp/fut/.venv/bin/python build/semantic_validate.py build/fixtures/<film>.json

    # render it
    python3 tools/universe_graph.py build/fixtures/<film>.json --fixture --out build/render

    # run the negative suite
    /tmp/fut/.venv/bin/python build/test_semantic.py

## Open issues

See `build/OPEN_ISSUES.md` (E257/E258, P2 simultaneity costs, genealogy-cycle render,
single-lane headers, preset/parameter guard asymmetry, divergence constraints,
gated-inversion traversal arm). Nothing was silently weakened to make a fixture pass.

## Provenance

- Spec: Astra (gpt-6-astra) via Experiential Labs - design, amendment, integration,
  adversarial break; ~320k input tokens, $0.00.
- D1 schema: Claude Code (Pro) - 24 turns before session wall; recovered and committed.
- D2-D5: executed directly by the orchestrator.
- All work committed on sfingali/film-universe-timelines local clone /tmp/fut.
