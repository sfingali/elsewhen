# elsewhen

The **abstract engine** for multi-universe / time-travel timeline charts. Its
whole job is one thing: to hold a film's universe structure as a **pure,
presentation-agnostic model** — *what* happens, never *how* it's drawn.

- **Abstract core** (`abstract_model.py`, `abstract.schema.json`): worlds and
  their origins, events, splits (both tines + character fates), transfers, the
  protagonist's route, fates, and citations. Structurally semantic — no glyphs,
  colours, lanes, dash-styles, density, timescale, or layout ordering.
- **Projections** (`projections.py`): render that model into *any* form —
  graphviz DOT, mermaid, markdown, plain text are built in. The PIL chart and
  Studio GUI are just more projections, reading the same model. Swap the
  renderer, never touch the model.
- **Import** (`to_abstract.py`): convert a legacy `schema_v2` document (or a
  compiled story JSON) into the abstract model.

The coupling boundary is the **abstract model**, not any drawing.

## The abstract representation

The model is a plain structure — worlds, events, splits, transfers, route,
fates — all cited. It is the thing a chart is *about*. Read it as text, or feed
it to any projector.

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
# Convert a legacy schema_v2 fixture into the abstract model
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

fixtures/             6 film fixtures (the import corpus)
references/           chart-language.md + method.md (the ontology + method)
```

This is intentionally lean: abstract core + import corpus + the two ontology
docs. The legacy v2.3 machinery (schema_v2.json, the E-code validator, the
allocation compiler, the full SPEC) has been pruned from this repo — it lives on
in the sibling visual repo `film-universe-timelines`, which owns the PIL renderer
and Studio GUI.
