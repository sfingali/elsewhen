# elsewhen

The **abstract engine** for multi-universe / time-travel timeline charts. Its
whole job is one thing: to hold a film's universe structure as a **pure,
presentation-agnostic model** — *what* happens, never *how* it's drawn.

Anything that turns this model into a picture — a PIL chart, an SVG, an HTML
page, a graphviz/mermaid graph, a video — is a **consumer** of the engine, not
part of it. The engine only ever answers "what is the structure"; the rendering
never touches this repo.

- **Abstract core** (`abstract_model.py`, `abstract.schema.json`): worlds and
  their origins, events, splits (both tines + character fates), transfers, the
  protagonist's route, fates, and citations. Structurally semantic — no glyphs,
  colours, lanes, dash-styles, density, timescale, or layout ordering.
- **Profiles** (`profiles.py`): named interpretations as explicit parameter
  sets — nothing hidden in a magic string.
- **Validation** (`abstract_model.validate()` + the schema): structural and
  coherence checks against the declared parameters.
- **Import** (`to_abstract.py`): convert a legacy `schema_v2` document (or a
  compiled story JSON) into the abstract model.

## Profiles are parameter sets

An interpretation **profile is not a magic string** — it is a bundle of semantic
parameters. The name (`P1`, `P2`, `P3`, `P4`, `tenet`, `dark`, `steins-gate`,
plus the diversity presets `eeaao`, `interstellar`, `edge-of-tomorrow`,
`predestination`) is just a convenience handle; the real contract is the
expanded parameter set in `profile.params`.

```json
"profile": {
  "name": "P1",
  "rules": "waif",
  "params": {
    "history_model": "universes",      // universes | revisions | iterations
    "branching": "branch",             // branch | overwrite | undeclared
    "coexistence": "coexisting",       // coexisting | single_active | undeclared
    "time_mechanics": ["body", "consciousness"],
    "joined_worlds": "preexist",       // preexist | not_preexist | undeclared
    "turnstiles": "none",              // both_signs | single_sign | none
    "protagonist_scope": "singular",   // singular | multiple
    "axis": "story_order",             // story_order | world_time
    "validation": "evidence_pending",
    "merges": "forbidden",             // forbidden | apparent_reset | siblings
    "genealogy": "acyclic"             // acyclic | bootstrap_cycles
  }
}
```

A **custom profile** is a preset plus overrides — no new name required:

```python
from profiles import resolve
resolve({"name": "P1", "params": {"axis": "world_time", "turnstiles": "both_signs"}})
```

The validator checks the model is coherent with its declared parameters (e.g. a
film marked `merges: forbidden` cannot carry an actual merge).

## The abstract representation

The model is a plain structure — worlds, events, splits, transfers, route,
fates — all cited. It is the thing a chart is *about*.

```
THE WAIF — Ben's Story
profile: P1 (parameter set — universes · branch · coexisting · body/consciousness)

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

## Author a new film

Use `author.py` to describe a film **directly in the abstract form** — no legacy
JSON required:

```python
from author import Author

st = Author("MY FILM — One Man's Story", profile="P1",
            footer="Universe identity is separate from consciousness and character fate.")
st.graph("G", "One man's story")
st.add_world("U1", "The initial timeline", "initial")
st.add_world("J-", "The dying tine", "born", born={"event": "e-J", "parent": "U1", "tine": "-"})
st.add_event("e-start", "start", "U1", 0, "It begins")
st.add_event("e-J", "split", "U1", 10, "The jump — the worlds split")
st.add_split("e-J", "branch", "ben-mind", "U1", "continues",
             st.add_outcome("U1", "e-start", "continues", [("i1", "continues", "survives")]),
             st.add_outcome("J-", "e-start", "born", [("i2", "dies", "dies")]))
st.set_profile("P1").set_params(axis="world_time")   # preset + override — a custom profile
st.add_assumption("Ground truth: the screenplay with #N# scene markers.")
st.to_file("film.abstract.json")
print(st.validate())   # [] == clean
print(st.to_text())    # the human-readable abstract form
```

`set_params(...)` derives a custom profile from a preset + overrides — no new
magic name. `to_file` writes the abstract JSON; `to_text` the readable form;
`validate()` the coherence problems.

## Usage

```bash
# Convert a legacy schema_v2 fixture into the abstract model
python3 to_abstract.py fixtures/bens_story.json            # -> abstract JSON
python3 to_abstract.py fixtures/bens_story.json --text     # -> abstract text

# Derive a custom profile on import: preset + parameter overrides
python3 to_abstract.py fixtures/tenet.json --base tenet --set axis=world_time --set turnstiles=none --text

# Validate + read any abstract model
python3 abstract_model.py build/abstract/bens_story.json

# Verify every fixture converts + validates, and run the unit tests
python3 verify_abstract.py
python3 tests/test_abstract.py
```

## Layout

```
abstract_model.py     the AbstractStory model: load, validate, to_text
abstract.schema.json  JSON Schema for the abstract model
profiles.py           named profiles as parameter sets (+ resolve/overrides)
author.py             programmatic builder to author an abstract model directly
to_abstract.py        schema_v2 -> abstract model importer + CLI (--base/--set)
verify_abstract.py    convert + validate harness for all fixtures
tests/test_abstract.py  unit tests (validation + authoring + profiles)

fixtures/             10 film fixtures (the import corpus — incl. the 4 diversity films)
references/           chart-language.md + method.md (the ontology + method)
```

This is intentional and lean: **engine only** — abstract model + profiles +
validation + import. No renderer, no projector, no visual vocabulary. Consumers
(the PIL renderer, Studio, graphviz/mermaid projection) live in the sibling
visual repo `film-universe-timelines` and read this model.
