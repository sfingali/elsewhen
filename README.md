# film-universe-timelines-engine

The **engine** for Primer-style multi-universe timeline charts. Its job is one
thing: to hold the story's universe structure as a **pure, presentation-agnostic
abstract model** — *what* happens, not *how* it's drawn.

- **Abstract core** (`abstract_model.py`, `abstract.schema.json`): worlds and
  their origins, events, splits (both tines + character fates), transfers, the
  protagonist's route, fates, and citations. Structurally semantic, no glyphs,
  colours, lanes, dash-styles, density, timescale, or layout ordering.
- **Projections** (`projections.py`): render that model into *any* form —
  graphviz DOT, mermaid, markdown, plain text are built in. The PIL chart and
  Studio GUI are just more projections; they live with the visual repo and read
  the same abstract model. Swap the renderer, never touch the model.
- **Import** (`to_abstract.py`): convert a legacy `schema_v2` document (or the
  compiled story JSON) into the abstract model.

The coupling boundary is the **abstract model**, not any drawing. The engine
publishes it; every visual is a downstream projection of it.

## The abstract representation

The model is a plain structure — worlds, events, splits, transfers, route,
fates — all cited. It is the thing a chart is *about*. You can read it directly
as text, or feed it to any projector.

```
THE WAIF — Ben's Story
profile: interpretation=P1 · rules=waif · validation=evidence_pending

# Graph BEN — Ben's Story
Worlds:
  U1   The initial timeline                [initial]
  J+   Jack lives — the line we follow     [born @e-J (U1 +)]
  *2   THE TIMELINE WITH HER               [preexisting · off-chart]
Events (story order):
    0  U1  start  The initial timeline            [cite: canon · Opening state]
   10  U1  split  J — the car crash              [cite: canon · Jack dies in car]
   30  *2  entry  He enters *2 — already running  [cite: canon · First arrival]
Splits:
  e-J  (branch) -> +=Jack lives — the line we follow | -=Jack dies — runs on
Transfers:
  tr-2  Jack lives -> THE TIMELINE WITH HER   (consciousness_transfer)
Route (ben-mind):  U1 → J+ → *2 → J- → *F
Fates:  waif-u1 in U1 @ e-J  dead
```

## Usage

```bash
# Convert a schema_v2 fixture into the abstract model
python3 to_abstract.py fixtures/bens_story.json                 # -> abstract JSON
python3 to_abstract.py fixtures/bens_story.json --text          # -> abstract text
python3 to_abstract.py fixtures/bens_story.json --dot           # -> graphviz DOT
python3 to_abstract.py fixtures/bens_story.json --mermaid       # -> mermaid
python3 to_abstract.py fixtures/bens_story.json --markdown      # -> markdown

# Validate + read any abstract model
python3 abstract_model.py build/abstract/bens_story.json

# Verify every fixture converts + renders all projections
python3 verify_abstract.py
```

## Layout

```
abstract_model.py     the AbstractStory model: load, validate, to_text
abstract.schema.json  JSON Schema for the abstract model
projections.py        dot / mermaid / markdown projectors (+ dispatcher)
to_abstract.py        schema_v2 -> abstract model importer + CLI
verify_abstract.py    convert+validate+render harness for all fixtures

schema_v2.json        legacy frozen data contract (import source)
semantic_validate.py  legacy two-phase E-code validator
timeline_compile.py   legacy allocation-txt -> story JSON authoring
v23_adapter.py        legacy fixture -> v1 renderer doc
fixtures/             6 film fixtures (the import corpus)
tests/                12 negative E-code fixtures
references/           chart-language, json-schema, method, redesign docs
SPEC_v23.md           the v2.3 spec; REPORT/CHANGELOG/OPEN_ISSUES
```

## Provenance

Spec by Astra (gpt-6-astra) via Experiential Labs; JSON schema by Claude Code
(Pro). Committed on `sfingali`. The abstract core + projections are the
presentation-agnostic layer on top.
