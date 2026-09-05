# Film Universe Timelines — Data Model SPEC v2.3
# Order: PART 1 = v2 base spec. PART 2 = v2.1 amendments (interpretation profiles). PART 3 = v2.2 parametric integration (supersedes conflicting v2.1 text). PART 4 = v2.3 adversarial repairs R1-R11 (most recent, supersedes all).

===== PART 1: v2 BASE SPEC =====
# Film Universe Timelines — Data Model SPEC v2.1
# = v2 SPEC (below, part 1) + AMENDMENT LIST (below, part 2). The amendments SUPERSEDE any v2 text they contradict.
# interpretation_profile: P1 branch-multiverse | P2 single mutable timeline | P3 loop w/ mind persistence | P4 undeclared (authoring default).
# THE WAIF canon = house profile ("interpretation_rules": "waif", requires P1), not universal physics.

===== PART 1: v2 SPEC =====
# Film Universe Timelines — Data Model v2 Specification

**Status:** implementable specification  
**Schema version:** `2` — independent of the current renderer’s “v4” implementation name  
**Canonical ontology:** THE WAIF / Ben’s Story

## 0. Binding decisions

1. **A trigger pull is an automatic split.** Its two outcomes include a surviving traveller counterpart and a dead traveller counterpart. The author supplies the identities and evidence; the compiler does not guess them.
2. **There is no reset or overwrite operation.** An apparent reset is a consciousness transfer into a different universe. A sibling relationship must be recorded if known; otherwise its ancestry remains explicitly unknown.
3. **Universe existence, character survival, and consciousness movement are separate facts.** A character’s death does not terminate a universe.
4. **Pre-existing universes begin at the chart’s top.** Arrival is not their birth.
5. **The thread is authoritative.** It is an ordered sequence of visits, not an interpretation of lane placement.
6. **Lane order is presentation only.** Repeated visits, skipped lanes, and crossings in either direction are legal.
7. **Birth identity is immutable.** A universe born on split `J`’s negative tine is `J-`, even if someone later enters it alive.
8. **Evidence is retained through normalization, validation, rendering, editing, and export.**

### Evidence limitation of the supplied material

The prompt supplies canon statements, but **no screenplay pages or scene numbers**. This specification therefore distinguishes:

- `production`: every citation has resolved page and scene values;
- `evidence_pending`: citation objects are mandatory, but explicitly unavailable locators are permitted and visibly flagged.

The Ben fixture below is a complete, structurally valid `evidence_pending` document. It does **not** invent screenplay citations. Promoting it to `production` requires the actual script locators.

This is an evidence limitation, not an inability to express the ontology.

---

# A. SCHEMA v2

## A1. Document structure

All objects reject undeclared fields, except `extensions`, which may contain application-specific data. All arrays shown below are required, although some may be empty.

```json
{
  "schema_version": 2,
  "validation_profile": "production",
  "meta": {
    "title": "Schema fixture",
    "subtitle": "Synthetic test data, not screenplay evidence",
    "footer": "",
    "axis": "story_order"
  },
  "sources": [],
  "characters": [],
  "travellers": [],
  "namespaces": [],
  "graphs": [],
  "graph_links": [],
  "extensions": {}
}
```

### Root fields

| Field | Type / rule |
|---|---|
| `schema_version` | Integer, exactly `2`. |
| `validation_profile` | `production` or `evidence_pending`. |
| `meta.title`, `subtitle`, `footer` | Strings. Authored spelling and casing are preserved. |
| `meta.axis` | Exactly `story_order` in v2. Down means **schematic narrative progression**, not elapsed world time. |
| `sources` | Evidence sources, each with globally unique `id`, `title`, `kind`, `text`. `kind`: `screenplay`, `canon_statement`, `test_fixture`. |
| `characters` | Globally unique `{id, label}` records. Character identity is not body-instance identity. |
| `travellers` | Globally unique `{id, character, label, color}` consciousness records. `color` is three integers, each `0..255`. |
| `namespaces` | Globally unique `{id, label}` records. |
| `graphs` | At most one graph per namespace. A namespace may be reserved without a graph. |
| `graph_links` | Non-routing cross-references between graphs. |
| `extensions` | Object; never interpreted as story facts. |

A graph has:

```json
{
  "namespace": "BEN",
  "title": "Ben's Story",
  "universes": [],
  "instances": [],
  "events": [],
  "splits": [],
  "transfers": [],
  "merges": [],
  "segments": [],
  "beats": [],
  "fates": [],
  "thread": {
    "traveller": "ben-mind",
    "visits": [],
    "links": []
  },
  "layout": {
    "lane_order": [],
    "collapsed_universes": []
  },
  "assumptions": []
}
```

Identifiers are unique **within their collection and namespace**. References are typed: an event reference cannot resolve to a similarly named universe.

Local references are plain strings. Cross-graph references are:

```json
{"namespace": "W", "id": "W1"}
```

Cross-graph references are allowed only in `graph_links` in v2. A graph never silently acquires another graph’s lanes or route.

---

## A2. Universes and immutable birth identities

Every universe has `id`, `label`, and `origin`.

The four origin forms are:

```json
{"kind": "initial"}
```

```json
{"kind": "preexisting", "ancestry": "off_chart"}
```

```json
{
  "kind": "born",
  "event": "J",
  "parent": "U1",
  "tine": "+"
}
```

```json
{
  "kind": "unknown",
  "exists_by": "observed-Q"
}
```

Rules:

- `initial`: root of this chart, not a claim about the universe’s cosmological beginning.
- `preexisting`: already running before its first depicted entry; header ID starts with `*`.
- `born`: ID must be exactly `origin.event + origin.tine`.
- `unknown`: no backpropagation claim. `exists_by` is a required local event proving its existence by that point. Its earlier lane is drawn with uncertainty, not as established prehistory.

`exists_by` may be the first entry event. For an earlier entry to be accepted, an earlier existence witness must be supplied.

### Continuation versus birth

At a split, a tine may:

- preserve the source universe’s identity: `universe_outcome: "continues"`;
- create a new identity with ancestry: `universe_outcome: "born"`;
- enter an outcome whose relationship is unresolved: `universe_outcome: "unknown"`.

A continuing tine does **not** rename its universe. Thus a later `T+` outcome may explicitly say **“continues J+”**. `T+` is then a tine label, not a new universe ID.

This permits Ben’s route to remain:

> `U1 → J+ → *2 → J- → *F`

even though other splits occur during those visits.

---

## A3. Events and event coordinates

Events are the only placement authority.

```json
{
  "id": "leave-2",
  "kind": "exit",
  "universe": "*2",
  "story_order": 50,
  "world_time": null,
  "label": "Ben leaves",
  "cite": {
    "source": "script",
    "page": "42",
    "scene": "78",
    "locator": "p42 #78",
    "status": "resolved"
  }
}
```

Required event fields:

- `id`
- `kind`: `start`, `split`, `outcome`, `entry`, `exit`, `anchor`, `cutoff`
- `universe`
- `story_order`: finite number
- `world_time`: `null` or `{clock, value, unit}`
- `label`
- `cite`

`world_time.value` is numeric. World-time values are comparable only when `clock` and `unit` match. They are metadata in v2, not layout distances.

Events may share `story_order` when they are ports of the same split. Ordering at a split is:

1. source event;
2. outgoing tines;
3. their outcome ports.

Array order is never a chronology rule.

`cutoff` means “the chart stops here.” It means neither character death nor universe destruction.

---

## A4. Splits and explicit per-tine outcomes

```json
{
  "event": "J",
  "cause": "trigger_pull",
  "automatic": true,
  "traveller": "ben-mind",
  "source_disposition": "ancestry_prefix",
  "outcomes": {
    "+": {
      "universe": "J+",
      "entry": "J.plus",
      "universe_outcome": "born",
      "character_outcomes": [
        {
          "instance": "ben-Jplus",
          "outcome": "continues",
          "fate": "ben-Jplus-alive"
        }
      ]
    },
    "-": {
      "universe": "J-",
      "entry": "J.minus",
      "universe_outcome": "born",
      "character_outcomes": [
        {
          "instance": "ben-Jminus",
          "outcome": "dies",
          "fate": "ben-Jminus-dead"
        }
      ]
    }
  }
}
```

### Split fields

| Field | Rule |
|---|---|
| `event` | References exactly one `kind: split` event. Its universe is the source. |
| `cause` | `trigger_pull`, `branch`, or `unknown`. |
| `automatic` | Boolean. Must be `true` for `trigger_pull`. |
| `traveller` | The consciousness whose survival alternatives this split records. |
| `source_disposition` | `continues` or `ancestry_prefix`. |
| `outcomes` | Exactly two keys: `+` and `-`. |
| `outcomes.*.entry` | Explicit `outcome` event in the result universe. |
| `universe_outcome` | `continues`, `born`, or `unknown`. |
| `character_outcomes[].outcome` | `continues`, `born`, `dies`, or `unknown`. |
| `character_outcomes[].fate` | Required fate record supporting that outcome. |

**Why two outcome fields?** `born` and `continues` can describe universe identity; `dies` describes a character instance. A single untyped enum would again confuse a dead traveller with a dead universe.

For `trigger_pull`:

- `+` contains a `continues` outcome for an instance of the named traveller’s character;
- `-` contains a `dies` outcome for an instance of that character;
- both records have explicit fate references.

Other characters’ outcomes may be included independently.

### Source disposition

- `continues`: exactly one tine preserves the source identity.
- `ancestry_prefix`: neither tine preserves it; the parent lane ends **as a shared ancestry segment** at the fork. This is not destruction of a universe.

A negative tine’s **character track** forks right and ends in a death cap. The universe remains available for later events and visits.

---

## A5. Instances and per-universe fates

```json
{
  "id": "waif-in-2",
  "character": "waif",
  "universe": "*2",
  "native_to_universe": false,
  "provenance": "unknown"
}
```

Instance fields:

- `id`
- `character`
- `universe`
- `native_to_universe`: `true`, `false`, or `null`
- `provenance`: `native`, `split_counterpart`, `arrival`, or `unknown`

An instance is local to one universe. Consciousness identity is separate.

```json
{
  "id": "waif-U1-death",
  "universe": "U1",
  "instance": "waif-U1",
  "event": "J",
  "status": "dead",
  "cite": {
    "source": "canon",
    "page": null,
    "scene": null,
    "locator": "CANON 4",
    "status": "unavailable"
  }
}
```

Fate statuses are `alive`, `dead`, `unknown`.

A fate is a state **at an event**, not a globally propagated character status. No record saying “Waif dead” may kill all Waif instances.

For one instance, a confirmed `dead` record is terminal. A later living traveller in that universe needs a distinct instance, or explicitly unknown embodiment. A transfer does not resurrect the dead instance by implication.

---

## A6. Consciousness transfers

```json
{
  "id": "to-2",
  "traveller": "ben-mind",
  "from": {
    "universe": "J+",
    "exit": "leave-Jplus"
  },
  "to": {
    "universe": "*2",
    "entry": "enter-2"
  },
  "mechanism": "consciousness_transfer",
  "relation": {
    "kind": "unknown"
  },
  "embodiment": {
    "mode": "unknown",
    "from_instance": "ben-Jplus",
    "to_instance": "ben-2"
  }
}
```

`mechanism`:

- `consciousness_transfer`
- `apparent_reset`

`relation`:

```json
{"kind": "unknown"}
```

```json
{"kind": "different_universes"}
```

```json
{"kind": "siblings", "parent": "U1", "split": "J"}
```

```json
{"kind": "siblings_off_chart"}
```

A known `siblings` relationship must agree with both declared origins. `siblings_off_chart` is an explicit authored claim, not inferred from similar scenery.

`embodiment.mode`:

- `unknown`
- `occupies_host`
- `coexists`
- `displaces`
- `fusion`

`from_instance` and `to_instance` are required keys, each an instance ID or `null`. Non-unknown modes require both identities. The latter three modes also require `other_travellers`, an array of declared traveller IDs.

**Transfer semantics:**

- source and destination universes must differ;
- source and destination universe lines continue independently;
- source instance survival is not inferred;
- destination native-character survival is not inferred;
- no split is required immediately before a transfer.

For `apparent_reset`, `relation.kind` must be `siblings` or `siblings_off_chart`.

**Groundhog Day mapping:** different universe per represented iteration; each apparent reset is a directed transfer to its sibling. Repeated calendar dates go in `world_time`, not into a same-universe rewind.

---

## A7. Actual merges

**Actual universe merging is deliberately not expressible in v2.**

```json
"merges": []
```

The field is reserved and must remain empty. A nonempty value fails validation.

This is preferable to drawing a consciousness transfer as a merger or inventing unspecified dispositions of converging histories. No accepted canon point requires actual merging.

The words *join* and *joined universe* in THE WAIF map to **transfer**, never to `merges`.

---

## A8. Segments, beats, and citations

Segments are named intervals on a universe, not labels attached only to a junction.

```json
{
  "id": "with-her",
  "universe": "*2",
  "from": "enter-2",
  "to": "M",
  "label": "THE TIMELINE WITH HER (from the join down)"
}
```

A beat belongs to exactly one segment:

```json
{
  "id": "meeting",
  "segment": "with-her",
  "story_order": 35,
  "text": "Ben meets a Waif who is not native to this universe.",
  "cite": {
    "source": "script",
    "page": "37",
    "scene": "64",
    "locator": "p37 #64",
    "status": "resolved"
  },
  "screen": "film",
  "certainty": "seen",
  "tone": "neutral",
  "side": "right",
  "traveller": "ben-mind"
}
```

Beat requirements:

- `id`, `segment`, `story_order`, `text`, `cite` required.
- Optional: `screen`, `certainty`, `tone`, `side`, `traveller`.
- `screen`: `film`, `flashback`, `deduced`.
- `certainty`: `seen`, `flashback`, `seen-later`, `never-shown`.
- `tone`: `neutral`, `death`, `good`.
- `side`: `left`, `right`.

The beat’s universe is derived from its segment. There is no duplicate `lane` field to disagree.

A segment may not straddle an interior split. Split-adjacent segments use the source split port on the incoming side and the appropriate outcome port on the outgoing side.

### Citation type

Every event, beat, and fate has:

```json
{
  "source": "script",
  "page": "37–38",
  "scene": "64, 66",
  "locator": "p37–38 #64, #66",
  "status": "resolved"
}
```

All five keys are mandatory.

- `resolved`: `page` and `scene` are nonempty strings.
- `unavailable`: missing values are `null`; `locator` still identifies the actual available evidence.
- `source` must resolve.
- Citations are never converted to generated scene ranges.
- Discontiguous locators remain discontiguous.

Production requires `resolved`. Pending evidence is visibly rendered, for example:

> `CANON 4 · page unavailable · scene unavailable`

---

## A9. Thread as ordered visits

```json
{
  "traveller": "ben-mind",
  "visits": [
    {
      "id": "v1",
      "traveller": "ben-mind",
      "universe": "U1",
      "entry": "opening",
      "exit": "J",
      "passes": []
    },
    {
      "id": "v2",
      "traveller": "ben-mind",
      "universe": "J+",
      "entry": "J.plus",
      "exit": "leave-Jplus",
      "passes": [
        {"split": "T", "tine": "+"}
      ]
    }
  ],
  "links": [
    {
      "from_visit": "v1",
      "to_visit": "v2",
      "kind": "split",
      "split": "J",
      "tine": "+"
    }
  ]
}
```

Rules:

- Every visit has `id`, `traveller`, `universe`, `entry`, `exit`, `passes`.
- `passes` records splits traversed **within** that visit without changing universe identity.
- One link exists between each adjacent pair of visits.
- Link kinds:
  - `split`: fields `split`, `tine`;
  - `transfer`: field `transfer`.
- Visits are not deduplicated by universe.
- The first entry is a `start` event.
- The final exit is a `cutoff` event.
- A thread need not occupy every declared universe.
- Unvisited negative worlds remain real universe entities.

Header text is generated from the visits. `meta.thread_label` is not an independent v2 field.

---

## A10. Complete minimal production example

This is intentionally synthetic. Its page and scene citation refers to the inline test source, not THE WAIF.

It exercises an initial world, a born death world, an already-running destination, an unknown-origin declaration, an in-universe continuing tine, a transfer, a cited beat, and explicit fates.

```json
{
  "schema_version": 2,
  "validation_profile": "production",
  "meta": {
    "title": "v2 mechanism fixture",
    "subtitle": "Synthetic evidence",
    "footer": "",
    "axis": "story_order"
  },
  "sources": [
    {
      "id": "fixture",
      "title": "Inline fixture ledger",
      "kind": "test_fixture",
      "text": "Page 1, scene 1: Ada starts in A. A trigger pull splits A: Ada continues in A and dies in K-. Ada then enters the already-running *X. Q is observed with unknown ancestry. The chart cuts off."
    }
  ],
  "characters": [
    {"id": "ada", "label": "Ada"}
  ],
  "travellers": [
    {"id": "ada-mind", "character": "ada", "label": "Ada", "color": [38, 118, 62]}
  ],
  "namespaces": [
    {"id": "TEST", "label": "Mechanism fixture"}
  ],
  "graphs": [
    {
      "namespace": "TEST",
      "title": "Ada",
      "universes": [
        {"id": "A", "label": "Opening world", "origin": {"kind": "initial"}},
        {"id": "K-", "label": "Death world", "origin": {"kind": "born", "event": "K", "parent": "A", "tine": "-"}},
        {"id": "*X", "label": "Destination", "origin": {"kind": "preexisting", "ancestry": "off_chart"}},
        {"id": "Q", "label": "Unknown ancestry", "origin": {"kind": "unknown", "exists_by": "observe-Q"}}
      ],
      "instances": [
        {"id": "ada-A", "character": "ada", "universe": "A", "native_to_universe": true, "provenance": "native"},
        {"id": "ada-Kminus", "character": "ada", "universe": "K-", "native_to_universe": true, "provenance": "split_counterpart"}
      ],
      "events": [
        {"id": "start", "kind": "start", "universe": "A", "story_order": 0, "world_time": null, "label": "Opening", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}},
        {"id": "K", "kind": "split", "universe": "A", "story_order": 10, "world_time": null, "label": "Trigger pull", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}},
        {"id": "K.plus", "kind": "outcome", "universe": "A", "story_order": 10, "world_time": null, "label": "K+ continues A", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}},
        {"id": "K.minus", "kind": "outcome", "universe": "K-", "story_order": 10, "world_time": null, "label": "K-: Ada dies", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}},
        {"id": "leave", "kind": "exit", "universe": "A", "story_order": 20, "world_time": null, "label": "Departure", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}},
        {"id": "arrive", "kind": "entry", "universe": "*X", "story_order": 21, "world_time": null, "label": "Arrival", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}},
        {"id": "observe-Q", "kind": "anchor", "universe": "Q", "story_order": 22, "world_time": null, "label": "Existence observed", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}},
        {"id": "end", "kind": "cutoff", "universe": "*X", "story_order": 30, "world_time": null, "label": "Chart cutoff", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}}
      ],
      "splits": [
        {
          "event": "K",
          "cause": "trigger_pull",
          "automatic": true,
          "traveller": "ada-mind",
          "source_disposition": "continues",
          "outcomes": {
            "+": {"universe": "A", "entry": "K.plus", "universe_outcome": "continues", "character_outcomes": [{"instance": "ada-A", "outcome": "continues", "fate": "ada-survives"}]},
            "-": {"universe": "K-", "entry": "K.minus", "universe_outcome": "born", "character_outcomes": [{"instance": "ada-Kminus", "outcome": "dies", "fate": "ada-dies"}]}
          }
        }
      ],
      "transfers": [
        {
          "id": "cross",
          "traveller": "ada-mind",
          "from": {"universe": "A", "exit": "leave"},
          "to": {"universe": "*X", "entry": "arrive"},
          "mechanism": "consciousness_transfer",
          "relation": {"kind": "different_universes"},
          "embodiment": {"mode": "unknown", "from_instance": "ada-A", "to_instance": null}
        }
      ],
      "merges": [],
      "segments": [
        {"id": "after-K", "universe": "A", "from": "K.plus", "to": "leave", "label": "After the surviving pull"},
        {"id": "destination", "universe": "*X", "from": "arrive", "to": "end", "label": "The destination visit"}
      ],
      "beats": [
        {"id": "continues", "segment": "after-K", "story_order": 15, "text": "Ada continues before crossing.", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}}
      ],
      "fates": [
        {"id": "ada-survives", "universe": "A", "instance": "ada-A", "event": "K.plus", "status": "alive", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}},
        {"id": "ada-dies", "universe": "K-", "instance": "ada-Kminus", "event": "K.minus", "status": "dead", "cite": {"source": "fixture", "page": "1", "scene": "1", "locator": "p1 #1", "status": "resolved"}}
      ],
      "thread": {
        "traveller": "ada-mind",
        "visits": [
          {"id": "v1", "traveller": "ada-mind", "universe": "A", "entry": "start", "exit": "leave", "passes": [{"split": "K", "tine": "+"}]},
          {"id": "v2", "traveller": "ada-mind", "universe": "*X", "entry": "arrive", "exit": "end", "passes": []}
        ],
        "links": [
          {"from_visit": "v1", "to_visit": "v2", "kind": "transfer", "transfer": "cross"}
        ]
      },
      "layout": {
        "lane_order": ["*X", "A", "K-", "Q"],
        "collapsed_universes": ["K-"]
      },
      "assumptions": []
    }
  ],
  "graph_links": [],
  "extensions": {}
}
```

## A11. Backward compatibility

Compatibility means **preserving recoverable content**, not preserving incorrect pixels or inventing missing semantics.

| Old field | v2 destination / behavior |
|---|---|
| `lanes[]` | `universes[]`; original order becomes `layout.lane_order`. |
| `lanes[].label` | `universes[].label`, rendered persistently. |
| `nodes[]` | `start` or `anchor` events; titles, bodies, and citations preserved. |
| `lanes_content` | Normalized to events, segments, beats and explicit endpoint references. Removed from canonical v2 output. |
| `splits.{id}.letter` | Event ID, if suitable; otherwise an explicit migration ID map is required. Scene citations do not become birth letters automatically. |
| `splits.*.caption` | Split event `label`. |
| `laneborn.from_split` | `origin.kind: born` only after parent and tine are supplied. |
| Explicit “already running” declaration | `origin.kind: preexisting`; starred ID assigned through an explicit migration map. |
| Missing `laneborn` | Does **not** imply pre-existence. Migration requires origin annotation. |
| `stubs` | Identified universe + instance + fate + `collapsed_universes` entry. Parent split must be supplied explicitly. |
| `joins` | `transfers`; old placement becomes an entry event. `from_split` alone is insufficient to determine the actual departure universe. |
| `arcs` | Transfers only when their endpoints are different universes and their semantics are explicitly supplied. |
| Same-lane `loop` or reset arc | Migration error until distinct sibling universes and transfers are authored. |
| `thread[]` | Ordered visits and links. Ambiguous token lists require author annotation. |
| `meta.thread_label` | Retained in migration report; replaced by generated route header. |
| Flat or nested beat | One v2 beat object; retain citation, tone, side, screen, certainty and traveller. |
| `segment` string | Explicit segment with `from` and `to` anchors. |
| `chip.dim`, `abandon` | Presentation data only; never proof of survival or pre-existence. |
| `ending` | `cutoff` event plus preserved label/citation. A death needs a separate fate. |
| `meta.travellers` | `characters` and `travellers`; identity mapping must be reviewed. |
| `meta.versioning` | Optional displayed transfer ordinal derived from thread order; never a survivor count. |
| `interval`, `timescale` | Explicit endpoint `world_time`; no clamped duration rectangle. |
| `legend` | Preserved explanatory text in `extensions.legacy_legend`; structural symbol key is generated. |
| Unparseable citation string | Retained verbatim as `locator`, status `unavailable`; never discarded. |

---

# B. VALIDATOR INVARIANTS

## Diagnostic protocol

- `validate()` never crashes on malformed input.
- CLI validation failure returns **exit code 2**.
- `build()` calls the same validator before layout.
- Errors are sorted by JSON Pointer, then code.
- The messages below are exact templates; braces denote substituted values.
- Structural errors stop semantic checks for that malformed subtree.
- JSON parsing rejects duplicate object keys.

### Numbered checks

1. **JSON syntax and duplicate keys**

   `E001 {path}: duplicate JSON key '{key}'.`

   `E002 {path}: invalid JSON: {detail}.`

2. **Structural schema**

   `E010 {path}: required field '{field}' is missing.`

   `E011 {path}: expected {type}.`

   `E012 {path}: unsupported value '{value}'.`

   `E013 {path}: unknown field '{field}'.`

3. **Version**

   `E020 /schema_version: expected 2.`

4. **Identifier uniqueness**

   `E030 {path}: duplicate {entity_type} id '{id}' in namespace '{namespace}'.`

   Global collections use namespace `$global`.

5. **Reference resolution**

   `E040 {path}: unknown {entity_type} '{id}' in namespace '{namespace}'.`

6. **Namespace isolation**

   `E041 {path}: routing references cannot cross namespaces.`

   `E042 {path}: namespace '{namespace}' has more than one graph.`

7. **Layout membership**

   Every universe appears exactly once in `lane_order`.

   `E050 {path}: lane_order must contain every universe exactly once.`

   `E051 {path}: collapsed universe '{universe}' is visited or contains non-collapsible content.`

   Collapsible content is limited to its birth outcome event and corresponding fates. No entry, exit, beat, later split, or visit may be hidden in a stub.

8. **Born identity and parent agreement**

   `E060 {path}: born universe id must be '{event}{tine}'.`

   `E061 {path}: origin does not match split '{event}' tine '{tine}'.`

   `E062 {path}: birth parent must be split source universe '{universe}'.`

9. **Origin presentation**

   `E063 {path}: preexisting universe id must begin with '*'.`

   `E064 {path}: '*' is reserved for preexisting universe ids.`

10. **Existence before use**

    Check events, visits, transfers and segment endpoints.

    `E070 {path}: universe '{universe}' does not exist at event '{event}'.`

    `E071 {path}: existence of universe '{universe}' before event '{event}' is unproven.`

    A born universe exists from its outcome port onward. An `ancestry_prefix` source cannot contain later events. A pre-existing universe exists before first entry. Unknown origins need a witness no later than the referenced event.

11. **Ancestry acyclicity**

    `E072 {path}: universe ancestry contains a cycle involving '{universe}'.`

    Repeated visits and crossing routes do not count as ancestry cycles.

12. **Split definition cardinality**

    Every `split` event has exactly one split definition, and every definition references a `split` event.

    `E080 {path}: split event '{event}' must have exactly one split definition.`

13. **Outcome coverage**

    `E081 {path}: split outcomes must contain exactly '+' and '-'.`

    `E082 {path}: split tines must identify two distinct result universes.`

    `E083 {path}: outcome entry must be an outcome event in universe '{universe}' at split story_order.`

14. **Continuation agreement**

    `E084 {path}: source_disposition 'continues' requires exactly one continuing source-universe tine.`

    `E085 {path}: source_disposition 'ancestry_prefix' forbids a continuing source-universe tine.`

    `E086 {path}: universe_outcome 'born' requires a matching born origin.`

    `E087 {path}: universe_outcome 'unknown' requires an unknown origin.`

15. **Automatic trigger physics**

    `E090 {path}: trigger_pull must set automatic to true.`

    `E091 {path}: trigger_pull '+' must record the traveller character continuing.`

    `E092 {path}: trigger_pull '-' must record the traveller character dying.`

16. **Character-outcome evidence**

    Fate and instance must agree with result universe, event and character.

    `E100 {path}: character outcome and referenced fate disagree.`

    `E101 {path}: instance '{instance}' does not belong to universe '{universe}'.`

    Outcome-to-fate mapping: `continues|born → alive`, `dies → dead`, `unknown → unknown`.

17. **Per-instance mortality**

    `E102 {path}: instance '{instance}' is alive after its recorded death.`

    A different instance of the same character is legal.

18. **Transfer endpoint agreement**

    `E110 {path}: departure event must be an exit event in universe '{universe}'.`

    `E111 {path}: arrival event must be an entry event in universe '{universe}'.`

    `E112 {path}: a consciousness transfer must connect different universes.`

    `E113 {path}: transfer arrival must follow departure in story_order.`

    These checks replace the old arc/mark placement loopholes.

19. **Transfer endpoint uniqueness**

    `E114 {path}: event '{event}' is used by more than one transfer endpoint.`

    Use distinct co-located ports for distinct transfers.

20. **Reset ontology**

    `E120 {path}: apparent_reset requires a sibling-universe relation.`

    `E121 {path}: declared sibling relation does not match universe origins.`

    `E122 {path}: same-universe reset or overwrite is not supported by this ontology.`

21. **Embodiment**

    `E123 {path}: embodiment mode '{mode}' requires both instance identities.`

    `E124 {path}: embodiment instance is in the wrong endpoint universe.`

    `E125 {path}: embodiment mode '{mode}' requires other_travellers.`

22. **Thread cardinality and identity**

    `E130 {path}: thread must contain at least one visit.`

    `E131 {path}: visit traveller must equal thread traveller '{traveller}'.`

    `E132 {path}: thread requires exactly one link between each adjacent pair of visits.`

23. **Visit endpoints and ordering**

    `E133 {path}: visit endpoint '{event}' is outside universe '{universe}'.`

    `E134 {path}: visit exit must not precede entry in story_order.`

    `E135 {path}: first visit must enter at a start event.`

    `E136 {path}: final visit must exit at a cutoff event.`

24. **Thread link continuity**

    `E140 {path}: link does not connect the adjacent visit endpoints.`

    `E141 {path}: transfer traveller differs from thread traveller.`

    `E142 {path}: thread cannot follow a dying traveller outcome.`

    A later visit to a negative universe is legal; following the dead counterpart *through its death* is not.

25. **Within-visit split traversal**

    Every split strictly encountered between entry and exit, including a split whose outcome continues before a later exit, has exactly one matching `passes` record.

    `E143 {path}: visit must select exactly one tine for split '{split}'.`

    `E144 {path}: pass tine does not continue the visit universe.`

    `E145 {path}: pass split lies outside the visit interval.`

26. **Segment endpoints and split boundaries**

    `E150 {path}: segment endpoints must belong to universe '{universe}'.`

    `E151 {path}: segment end must follow segment start.`

    `E152 {path}: segment crosses interior split '{split}'; divide the segment at its ports.`

27. **Beat placement**

    `E153 {path}: beat must lie strictly between its segment endpoints.`

    A beat at a split belongs in the split event’s label/evidence, not ambiguously on both adjacent intervals.

28. **Citation presence and production completeness**

    `E160 {path}: cite requires source, page, scene, locator, and status.`

    `E161 {path}: resolved citation requires nonempty page and scene.`

    `E162 {path}: production requires resolved page and scene citations.`

    In `evidence_pending`, emit:

    `W160 {path}: page or scene citation is unavailable; production certification is blocked.`

29. **Actual merges**

    `E170 {path}: actual universe merges are not supported in schema v2; use an explicit transfer only for consciousness movement.`

30. **Renderer geometry assertions**

    `E180 {path}: rendered endpoint is detached from event port '{event}'.`

    `E181 {path}: split '{split}' has no visible diagonal '{tine}' tine.`

    `E182 {path}: death tine '{split}-' does not fork to the right.`

    `E183 {path}: thread geometry is disconnected or branching.`

    `E184 {path}: connector overlaps an unrelated connector without a crossing bridge.`

    `E185 {path}: rendered citation text is missing.`

31. **Legacy migration refusal**

    `E190 {path}: legacy field '{field}' requires explicit v2 annotation: {requirement}.`

    `E191 {path}: unsupported allocation syntax '{text}'.`

    This is an intentional refusal, not a traceback.

---

# C. RENDER MAPPING

## C1. Semantic primitives

| Concept | Required primitive |
|---|---|
| Universe | Thin neutral baseline with persistent ID and name. |
| Initial universe | Header `U1 — …`; begins at chart top. |
| Pre-existing universe | Header `*2 — … / ALREADY RUNNING`; baseline starts at top, including the pre-entry region. |
| Born universe | Baseline begins at its actual split outcome port, never at an independent lane cursor. |
| Unknown origin | `?` header badge; uncertain dotted prehistory above the existence witness. No “already running” assertion. |
| Split | Yellow event glyph plus **two visible diagonal tines**. Each tine prints its sign, result universe ID and outcome. |
| Continuing tine | Label such as `T+ → J+ · Ben continues`; diagonal fork may return to the source’s lane column. |
| Death tine | Diagonal to the right, named universe, character death cap and fate caption. The cap belongs to the character track, not the universe baseline. |
| Collapsed death universe | Explicit named mini-lane/stub, attached through the declared split/tine; expandable without changing data. |
| Transfer | Hollow exit port → directed connector → filled entry port. **Neither universe baseline terminates.** |
| Apparent reset | Same transfer primitive, with `APPARENT RESET / SIBLING CUT` badge. Never a same-lane loop. |
| Segment | Interval bracket or subdued chip positioned between its anchors; label prefixed with universe ID. |
| Beat | Small point in its segment, prose, then page + scene citation. |
| Fate | Character/instance badge beside the relevant event; death uses `X`, alive uses an open circle, unknown uses `?`. |
| Thread | One continuous foreground route assembled from visits, passes and links. Visit numbers remain visible at repeated entries. |
| Chart cutoff | Open-ended cutoff bar and box. No death cap unless a separate fate says death. |
| Geometric crossing | Bridge or gap on the lower-priority connector. No implied junction. |
| Namespace | Separate panel/chart title. A W graph is never folded into Ben’s lane list. |
| Pending citation | Visible `page unavailable / scene unavailable` annotation. |
| Actual merge | No primitive in v2; validation refuses it. |

### Right-hand death rule and orientation

In canonical vertical mode, the death tine must leave the split with positive screen-X displacement.

Horizontal mode must preserve the same **screen-right diagonal departure** for death tines rather than blindly transposing the split glyph. After that initial diagonal, routing may enter a suitable gutter or negative-world row. Labels and `-` retain the semantics in either orientation.

Global lane ordering cannot override the local right-hand death fork.

### Thread rendering

Construct one ordered route:

1. first visit entry;
2. in-universe path through selected `passes`;
3. visit exit;
4. matching link geometry;
5. next visit entry;
6. repeat through final cutoff.

No green line is inferred from:

- lack of `laneborn`;
- presence of a join;
- first occupied lane;
- a split’s position;
- a traveller declaration;
- an unreferenced arc.

Other travellers’ graph references never interrupt Ben’s thread.

## C2. Changes to current `build()` sections

| Current code section | v2 change |
|---|---|
| Beginning of `build()` | Call normalization and validation. Select one namespace to render. |
| `raw = ... lanes_content` | Build typed placements from `events`, `segments`, `beats`; no `next(iter(item))`. |
| `survivor census` | Delete. No replacement census in v2. |
| `measure()` | Measure all labels, headers, beats and citations, not just three box types. |
| `fixed-point restack` | Retain the placement-list approach, but use dependency constraints from event anchors and split ports. Remove `from_split + JOIN_DROP` as the universal transfer rule. |
| `q_extent()` / `q_extent_any()` | Replace duplicate estimates with one measured screen rectangle per placement. |
| `lane base lines` | Derive start/end from origin and source disposition. Departure and death never terminate a universe baseline. |
| `thread verticals` | Replace entirely with visit/pass/link traversal. No lane-based carry heuristics. |
| `stubs diagonals` | Iterate split outcomes; never search for nearest preceding split. |
| `time-travel arcs` | Reuse corridor-routing helpers for explicit transfers. Append the actual final arrival port after any dodge. |
| `version counters` | If displayed, enumerate transfers along the thread, not `arc_pos` insertion order. |
| `markers / boxes / text` | Render generated identity labels, fates, complete citations, and segment intervals. Do not call `tc()` on authored text. |
| `chrome` | Generate route header from visits; add persistent lane headers and generated symbol key. |
| `legend` | No fabricated `RUNS ON` mortality claims and no survivor arithmetic. |
| `hitboxes` | Use final measured screen rectangles directly; remove reversed logical-coordinate transformation. |
| `seg()` / styles | Add semantic tokens for transfer, fate and uncertainty. Palette and style selection must preserve endpoint shapes and labels. |

### Layout staging

Retain PIL, fonts, existing box drawing, and the `P` placement list. Change the preparation sequence to:

1. derive placements and constraints;
2. measure all text and boxes;
3. solve event positions;
4. freeze the obstacle set;
5. route connectors;
6. assert exact endpoint attachment and nonconnecting crossings;
7. calculate complete canvas extents;
8. draw.

There is no fixed eight-pass substitute for an unsatisfiable dependency graph. Detect a constraint cycle and report a validation/layout diagnostic.

---

# D. MIGRATION — PATCH-SIZED IMPLEMENTATION ORDER

The following sequence changes the current implementation incrementally.

## Patch 1 — immediate correctness fixes in the legacy path

Files: `tools/universe_graph.py`, existing tests.

- Replace both stale arc lookups with `g["arcs"][p["v"]]`.
- Preserve flat and nested beat `cite`, `tone`, `side`, `screen`, `certainty`, `traveller`.
- Preserve `chip.dim`.
- Disable the survivor census.
- Add endpoint tails from dodged routes to the actual arrival dots.
- Make negative CLI tests require `returncode == 2`.

These fixes do not wait for v2.

## Patch 2 — canonical data structures and schema

Add:

- `references/schema-v2.json`
- `tools/universe_model.py`
- `tests/test_schema_v2.py`

Implement:

- strict JSON loading with duplicate-key detection;
- typed document normalization;
- origin, event, split, transfer, segment, fate and visit records;
- `production` and `evidence_pending` profiles;
- exact structural diagnostics.

Keep the legacy loader separate. Do not auto-detect ontology from prose.

## Patch 3 — semantic validator

Implement section B before enabling v2 rendering.

Add positive and negative fixtures for:

- `A → B → A → C`;
- entering a born universe before birth;
- entering a negative universe after its native traveller died;
- wrong transfer endpoint universe;
- omitted split tine;
- duplicate placements represented through duplicate IDs;
- missing page or scene citation;
- unrelated traveller transfer;
- lane-array permutations.

## Patch 4 — first example conversion

**Update `examples/demo-film/demo.universes.json` first.**

Why: it already exercises split, crossing, already-running lanes and the split-2 missing-fork defect.

- Supply explicit universe origins and split outcomes.
- Replace joins with transfers.
- Author visits and links.
- Keep all existing citations.
- Mark unsupported/missing evidence as pending; do not manufacture it.
- Save a legacy fixture under `tests/fixtures/legacy/` before conversion.

Add the Ben fixture from section E as:

`examples/the-waif/bens-story.v2.json`

It becomes the ontology acceptance test, not a substitute for the screenplay ledger.

## Patch 5 — v2 origin and split rendering

Keep current marker/box functions.

Replace only:

- lane baseline generation;
- born-lane anchoring;
- death-stub parent lookup;
- missing fork behavior.

Add persistent lane headers and outcome identities.

At this stage a v2 chart may render neutral universe structure before its thread is enabled.

## Patch 6 — authoritative thread and transfers

Replace the old `thread verticals` section.

- Route from visits, passes and links.
- Reuse the arc corridor code.
- Add exit/entry ports.
- Permit arbitrary lane jumps and revisits.
- Generate the route header.
- Assert single connected thread geometry.

Update **`examples/bttf2/bttf2.universes.json` next**, because another traveller’s departure must not interrupt Marty’s thread. Its universe allocation must be explicitly corrected, not merely re-keyed.

## Patch 7 — cited segment and beat layout

- Anchor segment labels to intervals.
- Measure all citations.
- Use one immutable obstacle set.
- Add rendered-text manifests for citation-presence tests.
- Correct screen-space hitboxes.

Then update **`examples/advanced-demo/advanced-demo.universes.json`** to cover revisits, explicit instances and per-universe deaths. Remove its old survivor census assertions.

## Patch 8 — compiler migration

File: `tools/timeline_compile.py`.

- Remove `lanes - 1` pull-count rule.
- Remove “next lane left” routing.
- `pulls:` still denotes automatic splits, but compilation requires explicit outcomes/identities.
- Add explicit transition declarations identifying departure and arrival events.
- Preserve actual scene sets, not their convex range.
- Fix `OPEN:` parsing and reject unknown syntax.
- Support authored beats with page and scene citations.
- Refuse incomplete production input with `E190`, not inferred mortality or `RUNS ON`.

## Patch 9 — Studio migration

Files: `studio/index.html`, `studio/timeline_studio.py`.

- Edit normalized beat objects only.
- Edit thread visits and links, not token strings.
- Expose origin, tine identity, endpoint and per-universe fate fields.
- Use the shared validator.
- Preserve evidence-pending state and original citation locators.

## Patch 10 — remaining interpretation fixtures and documentation

Update in this order:

1. `examples/groundhog-day/`: distinct sibling universes; apparent-reset transfers.
2. `examples/butterfly-effect/`: explicit branching interpretation under this ontology; no overwrite state primitive.
3. `examples/primer/`: explicit universes, endpoint evidence and acknowledged unknowns; no inferred copy census.

Then replace the conflicting rules in:

- `references/json-schema.md`
- `references/chart-language.md`
- `references/method.md`
- `references/output-redesign-decisions.md`
- `README.md`
- `SKILL.md`

Explicitly supersede the earlier review’s same-universe reset/revision recommendation. It conflicts with the accepted canon.

---

# E. SELF-CHECK — BEN’S STORY

## E1. What this fixture asserts

Canon directly supplies:

- `U1`;
- splits `J`, `T`, `M`, `C`;
- pre-existing `*2` and `*F`;
- Ben’s route `U1 → J+ → *2 → J- → *F`;
- initial-universe Waif death at the jump;
- the encountered Waif’s non-native status;
- separate W and B namespaces.

The prompt does **not** supply the full event ledger. The following are explicit **fixture allocations**, not recovered screenplay facts:

- `J` births both `J+` and `J-`.
- `T` occurs during the `J+` visit.
- `M` occurs during the `*2` visit.
- `C` occurs during the later `J-` visit.
- Their positive tines preserve the occupied universe’s identity.
- W1 and W2 below are separate Waif transfer events with unspecified mechanism beyond consciousness crossing; they are **not asserted to be trigger pulls**.
- The particular W destination identities and schematic order exist to test namespace isolation.

These allocations make the supplied topology executable without pretending to know missing pages, scenes, bodies or jump mechanics.

## E2. Complete JSON

```json
{
  "schema_version": 2,
  "validation_profile": "evidence_pending",
  "meta": {
    "title": "THE WAIF — Ben's Story",
    "subtitle": "Canon topology fixture; screenplay locators pending",
    "footer": "Universe identity is separate from consciousness and character fate.",
    "axis": "story_order"
  },
  "sources": [
    {
      "id": "canon",
      "title": "Author-supplied THE WAIF canon",
      "kind": "canon_statement",
      "text": "Every trigger pull automatically splits. No rewind. Joined worlds already existed. The Waif dies in U1 at the jump. The later Waif is not native to the encountered universe. Ben's route is U1 -> J+ -> *2 -> J- -> *F. Death tines fork right. Beats require page and scene evidence. Other graphs have separate namespaces."
    },
    {
      "id": "allocation",
      "title": "Explicit structural test allocations",
      "kind": "test_fixture",
      "text": "For this topology test: J births J+ and J-. T is in J+; M is in *2; C is in J-. T+, M+, and C+ preserve their source identities. W1 and W2 are separate Waif transfers through WU1, *W2, and *W3. These allocations are not screenplay citations."
    }
  ],
  "characters": [
    {"id": "ben", "label": "Ben"},
    {"id": "waif", "label": "The Waif"}
  ],
  "travellers": [
    {"id": "ben-mind", "character": "ben", "label": "Ben", "color": [38, 118, 62]},
    {"id": "waif-mind", "character": "waif", "label": "The Waif", "color": [70, 90, 150]}
  ],
  "namespaces": [
    {"id": "BEN", "label": "Ben's Story"},
    {"id": "W", "label": "The Waif's jumps"},
    {"id": "B", "label": "Before-lives; reserved for a separate graph"}
  ],
  "graphs": [
    {
      "namespace": "BEN",
      "title": "Ben's Story",
      "universes": [
        {"id": "U1", "label": "The initial timeline", "origin": {"kind": "initial"}},
        {"id": "J+", "label": "The surviving J branch", "origin": {"kind": "born", "event": "J", "parent": "U1", "tine": "+"}},
        {"id": "J-", "label": "The J death branch, later entered", "origin": {"kind": "born", "event": "J", "parent": "U1", "tine": "-"}},
        {"id": "T-", "label": "The T death branch", "origin": {"kind": "born", "event": "T", "parent": "J+", "tine": "-"}},
        {"id": "*2", "label": "The timeline with her", "origin": {"kind": "preexisting", "ancestry": "off_chart"}},
        {"id": "M-", "label": "The M death branch", "origin": {"kind": "born", "event": "M", "parent": "*2", "tine": "-"}},
        {"id": "C-", "label": "The C death branch", "origin": {"kind": "born", "event": "C", "parent": "J-", "tine": "-"}},
        {"id": "*F", "label": "The final joined universe", "origin": {"kind": "preexisting", "ancestry": "off_chart"}}
      ],
      "instances": [
        {"id": "waif-U1", "character": "waif", "universe": "U1", "native_to_universe": true, "provenance": "native"},
        {"id": "waif-2", "character": "waif", "universe": "*2", "native_to_universe": false, "provenance": "unknown"},
        {"id": "ben-Jplus", "character": "ben", "universe": "J+", "native_to_universe": true, "provenance": "split_counterpart"},
        {"id": "ben-Jminus-dead", "character": "ben", "universe": "J-", "native_to_universe": true, "provenance": "split_counterpart"},
        {"id": "ben-Tminus", "character": "ben", "universe": "T-", "native_to_universe": true, "provenance": "split_counterpart"},
        {"id": "ben-2", "character": "ben", "universe": "*2", "native_to_universe": null, "provenance": "unknown"},
        {"id": "ben-Mminus", "character": "ben", "universe": "M-", "native_to_universe": true, "provenance": "split_counterpart"},
        {"id": "ben-Jminus-return", "character": "ben", "universe": "J-", "native_to_universe": null, "provenance": "unknown"},
        {"id": "ben-Cminus", "character": "ben", "universe": "C-", "native_to_universe": true, "provenance": "split_counterpart"}
      ],
      "events": [
        {"id": "opening", "kind": "start", "universe": "U1", "story_order": 0, "world_time": null, "label": "Ben's opening universe", "cite": {"source": "canon", "page": null, "scene": null, "locator": "CANON 5", "status": "unavailable"}},
        {"id": "J", "kind": "split", "universe": "U1", "story_order": 10, "world_time": null, "label": "J — automatic trigger split; the initial Waif dies at the jump", "cite": {"source": "canon", "page": null, "scene": null, "locator": "CANON 1, 4, 5", "status": "unavailable"}},
        {"id": "J.plus", "kind": "outcome", "universe": "J+", "story_order": 10, "world_time": null, "label": "J+ — Ben continues", "cite": {"source": "canon", "page": null, "scene": null, "locator": "CANON 1, 5", "status": "unavailable"}},
        {"id": "J.minus", "kind": "outcome", "universe": "J-", "story_order": 10, "world_time": null, "label": "J- — this Ben dies", "cite": {"source": "canon", "page": null, "scene": null, "locator": "CANON 1, 5", "status": "unavailable"}},
        {"id": "T", "kind": "split", "universe": "J+", "story_order": 20, "world_time": null, "label": "T — automatic trigger split", "cite": {"source": "allocation", "page": null, "scene": null, "locator": "T allocation; mortality rule CANON 1", "status": "unavailable"}},
        {"id": "T.plus", "kind": "outcome", "universe": "J+", "story_order": 20, "world_time": null, "label": "T+ continues J+", "cite": {"source": "allocation", "page": null, "scene": null, "locator": "T positive continuation", "status": "unavailable"}},
        {"id": "T.minus", "kind": "outcome", "universe": "T-", "story_order": 20, "world_time": null, "label": "T- — Ben dies", "cite": {"source": "allocation", "page": null, "scene": null, "locator": "T negative branch", "status": "unavailable"}},
        {"id": "leave-Jplus", "kind": "exit", "universe": "J+", "story_order": 25, "world_time": null, "label": "Ben leaves J+", "cite": {"source": "canon", "page": null, "scene": null, "locator": "CANON 5", "status": "unavailable"}},
        {"id": "enter-2", "kind": "entry", "universe": "*2", "story_order": 30, "world_time": null, "label": "Ben enters an already-running universe", "cite": {"source": "canon", "page": null, "scene": null, "locator": "CANON 3, 5", "status": "unavailable"}},
        {"id": "meet-waif", "kind": "anchor", "universe": "*2", "story_order": 35, "world_time": null, "label": "The encountered Waif is not native to *2", "cite": {"source": "canon", "page": null, "scene": null, "locator": "CANON 4", "status": "unavailable"}},
        {"id": "M", "kind": "split", "universe": "*2", "story_order": 40, "world_time": null, "label": "M — automatic trigger split", "cite": {"source": "allocation", "page": null, "scene": null, "locator": "M allocation; mortality rule CANON 1", "status": "unavailable"}},
        {"id": "M.plus", "kind": "outcome", "universe": "*2", "story_order": 40, "world_time": null, "label": "M+ continues *2", "cite": {"source": "allocation", "page": null, "scene": null, "locator": "M positive continuation", "status": "unavailable"}},
        {"id": "M.minus", "kind": "outcome", "universe": "M-", "story_order": 40, "world_time": null, "label": "M- — Ben dies", "cite": {"source": "allocation", "page": null, "scene": null, "locator": "M negative branch", "status": "unavailable"}},
        {"id": "leave-2", "kind": "exit", "universe": "*2", "story_order": 45, "world_time": null, "label": "Ben leaves *2", "cite": {"source": "canon", "page": null, "scene": null, "locator": "CANON 5", "status": "unavailable"}},
        {"id": "enter-Jminus", "kind": "entry", "universe": "J-", "story_order": 50, "world_time": null, "label": "Ben enters J-; this is not resurrection of its dead Ben instance", "cite": {"source": "canon", "page": null, "scene": null, "locator": "CANON 1, 5", "status": "unavailable"}},
        {"id": "C", "kind": "split", "universe": "J-", "story_order": 60, "world_time": null, "label": "C — automatic trigger split", "cite": {"source": "allocation", "page": null, "scene": null, "locator": "C allocation; mortality rule CANON 1", "status": "unavailable"}},
        {"id": "C.plus", "kind": "outcome", "universe": "J-", "story_order": 60, "world_time": null, "label": "C+ continues J-", "cite": {"source": "allocation", "page": null, "scene": null, "locator": "C positive continuation", "status": "unavailable"}},
        {"id": "C.minus", "kind": "outcome", "universe": "C-", "story_order": 60, "world_time": null, "label": "C- — Ben dies", "cite

===== PART 2: AMENDMENTS v2 -> v2.1 (superseding) =====
## AMEND-1 — PROFILE MECHANISM

**Amends:** title block; §0; A1–A9; B.

Replace the canonical-ontology declaration with:

> **Specification revision:** `2.1`; `schema_version: 2` remains the schema-family identifier.  
> **Core ontology:** neutral. Every canonical document declares one interpretation profile. THE WAIF is the house interpretation, not universal physics. `validation_profile` governs evidence completeness only.

### Document fields

Add:

```json
{
  "interpretation_profile": "P4",
  "interpretation_rules": "none"
}
```

Exact field definitions:

- `interpretation_profile`: `"P1"`, `"P2"`, `"P3"`, or `"P4"`.
- Authoring default: `"P4"`. Normalization writes this explicitly; canonical validation never infers a profile from a title, source text, graph shape, or lane count.
- `interpretation_rules`: `"none"` or `"waif"`; optional, default `"none"`. `"waif"` requires `"P1"`.
- A missing canonical `interpretation_profile` fails:
  
  `E200 /interpretation_profile: canonical document must declare interpretation_profile.`

- An unsupported value uses `E012`.
- Invalid house-rule combination fails:
  
  `E201 /interpretation_rules: 'waif' requires interpretation_profile 'P1'.`

**P4 marking rule:**

> P4 must display `P4 · ONTOLOGY UNDECLARED` persistently on canvas and in exported text. Every depicted connection between distinct history contexts must display `RELATION UNDECLARED`. Such contexts are observations, not asserted coexisting worlds. Neither label may be hidden by styling, cropping, collapsing, or legend suppression.

Failure:

`E202 {path}: required interpretation-profile marking is missing or incorrect.`

### Profile scope

| Entity | P1 — branch-multiverse | P2 — single mutable timeline | P3 — closed loop, mind persistence | P4 — ambiguous/undeclared |
|---|---|---|---|---|
| `graphs` | Branch-world graphs | Views of one revisable world | Views of one iterating world | Observation graphs |
| `namespaces` | Reference isolation, never ancestry | Reference isolation, never additional worlds | Reference isolation, never additional worlds | Reference isolation, never an ontology claim |
| `universes` | Persistent world identities, including ancestry prefixes | Exactly one world ID per graph, plus its ordered revision history | Exactly one world ID per graph, plus its ordered iterations | Identified observation contexts; coexistence undeclared |
| Across graphs | Different IDs may identify different worlds | All rendered graphs use the same world ID and identical world/revision declarations | All rendered graphs use the same world ID and identical world/iteration declarations | No world equivalence inferred |
| `layout.lane_order` | World-column order | Exactly `[world_id]`; revisions are not lanes | Exactly `[world_id]`; iterations are not lanes | Observation-column order, explicitly non-ontological |
| `instances` | Embodiments local to one world | Embodiment identifiers local to the one world; presence and fate are revision-local | Embodiment identifiers local to the one world; presence and fate are iteration-local | Embodiments local to an observed context |
| `fates` | Event-local facts about an instance in a world | Event-and-revision-local facts; superseded facts remain historical records only | Event-and-iteration-local facts; reset carries no bodily fate forward | Observed facts only; no propagation across contexts |
| `thread` | Ordered consciousness visits among worlds | Ordered consciousness visits to particular revisions of one world | Ordered visits through iterations by the retaining consciousness | Ordered observed continuity; mechanism and world relationship undeclared |
| Origin | Existing P1 origins | `initial` or `unknown`; revision creation is not world birth | `initial` or `unknown`; iteration start is not world birth | `initial` or `unknown`; no asserted branch ancestry |

> An event graph consists of authored event identities, evidence, coordinates, causal relations, and ordered route endpoints. Profile encoding binds those events to worlds, revisions, or observation contexts and interprets transition edges. Re-encoding must preserve event IDs, evidence, `story_order`, `world_time`, and the represented route; profile-specific bindings and transition records may change. Changing only the profile chip is not a valid conversion. A film may have multiple separately declared encodings of the same event graph.

### Complete profile-conditional invariant replacement

The following replaces every ontology-dependent invariant in the supplied specification. All other structural, reference, evidence, namespace-isolation, no-inference, and geometry checks remain binding.

| Existing clauses/checks | P1 form | P2 form | P3 form | P4 form |
|---|---|---|---|---|
| §0.1; A4; B15: automatic trigger physics | With `waif`, every authored trigger intervention has an automatic split with explicit surviving/dead counterparts. With `none`, no trigger physics is inferred; an authored `cause:"trigger_pull"` split still explicitly asserts the existing two-outcome contract. | Trigger/intervention may cause an authored revision; no automatic split or death. | Intervention may occur within an iteration; reset requires an authored iteration transition, not a split. | Intervention effect remains undeclared; no automatic split, reset, or death. |
| §0.2; A6; B20: reset/overwrite | Apparent reset is an explicit sibling transfer; no overwrite. | Overwrite advances revision order in the same world; old histories cease to be current worlds. | Reset advances iteration order in the same world; declared mind persists. | Only an observed transition; no sibling, overwrite, or loop assertion. |
| §0.3–4,7; A2; B8–11: existence, birth, ancestry | Existing birth identities, ancestry, witnesses and pre-existing-world rules apply. Death/transfer does not terminate a world. | One world persists through revisions. Revision availability replaces branch-birth checks; no `born`/`preexisting` origin, starred ID, or ancestry edge. | One world persists through iterations. Iteration availability replaces branch-birth checks; no branch origins or ancestry. | Witness bounds apply to observed contexts; no established prehistory or ancestry is inferred. |
| A4; B12–14: split structure | Existing split cardinality, tines, continuation and birth agreement apply. | `splits:[]`; no `split` or `outcome` events. | `splits:[]`; no `split` or `outcome` events. | `splits:[]`; no `split` or `outcome` events. |
| A5; B16–17: fate scope/mortality | Existing world-and-instance agreement; death terminal for that instance. | Fate and instance agree with event world; death terminal only within its revision. | Death terminal only within its iteration; bodily reset is not implicit resurrection within that iteration. | Death terminal within a single observed context; no cross-context inference. |
| A6; B18–21: transitions/embodiment | Existing different-world transfers, sibling-reset constraints and embodiment checks. | No `transfers`; revision transitions have same-world, adjacent-revision endpoints. | No `transfers`; iteration transitions have same-world, adjacent-iteration endpoints and retained mind. | Transfers connect observation contexts with `relation.kind:"unknown"` and `mechanism:"observed_transition"` only. |
| A8; B26: segments | Cannot cross an interior split. | Endpoints must share one revision; cannot span a revision boundary. | Endpoints must share one iteration; cannot span a reset boundary. | Endpoints must share one observed context. |
| A9; B22–25: visits/links | Existing visits, `passes`, split/transfer links; unvisited worlds remain declared worlds. | Visits select one revision; `passes:[]`; links use declared revision transitions. Superseded history is not an unvisited persistent world. | Visits select one iteration; `passes:[]`; links use declared reset transitions. | Visits select observed contexts; `passes:[]`; links reference observed transitions. |
| B7; C1–C2: lanes/collapse | Existing universe lanes and explicit birth stubs. | One baseline; no collapsed universe stubs. | One baseline; no collapsed universe stubs. | Observation columns, never labelled universe lanes; collapsing is forbidden. |
| B30; C1: split/reset geometry | Existing explicit tines. Screen-right death geometry applies only to an authored dying negative tine. | Revision splice and superseded-history treatment; no tines/sibling connectors. | Iteration separators and reset connectors; no parallel universe lanes. | Dashed connectors labelled undeclared; no branch/reset glyph asserting ontology. |
| A11; B31; D: migration | Explicit branch identities/outcomes required. | Explicit same-world revision records required. | Explicit iteration/reset and memory records required. | Preserve observation contexts and mark uncertainty; never manufacture a committed profile. |

**Profile-independent retained invariants:**

> Thread order remains authoritative. Narrative order is not world time. Death, consciousness movement, history supersession, and world existence remain distinct facts. No compiler-generated deaths, survival claims, parentage, body counts, memory retention, or citations. Actual world merging remains unsupported under every profile.

Add `"observed_transition"` to A6 `mechanism`, legal only in P4.

### Causal loops and bootstrap evidence

**Amends A1, A3 and B:** add optional graph arrays, defaulting to `[]`:

```json
{
  "causal_links": [
    {
      "id": "c1",
      "from": "later-observation",
      "to": "earlier-intervention",
      "subject": "remembered-message",
      "cite": {
        "source": "film",
        "page": null,
        "scene": null,
        "locator": "Authored causal interpretation",
        "status": "unavailable"
      }
    }
  ],
  "causal_cycles": [
    {
      "id": "loop1",
      "kind": "bootstrap",
      "links": ["c1", "c2"]
    }
  ]
}
```

> `causal_links` reference events in the same namespace; `subject` is a nonempty authored identity for the transmitted information/object. `causal_cycles.kind` is `closed_loop` or `bootstrap`; listed links must form one directed cycle, with at least one link. Bootstrap links must share `subject`. Every directed cycle must be covered by a declared cycle record. Causal edges may run backward in narrative/world time and never become ancestry or layout-order constraints. A reset arrow alone does not establish a causal cycle. No external origin is invented for a bootstrap subject.

Errors:

- `E203 {path}: causal cycle is undeclared.`
- `E204 {path}: causal cycle links do not form the declared directed cycle.`
- `E205 {path}: bootstrap cycle links must share one subject.`

---

## AMEND-2 — P2 SUPERSESSION

**Amends:** A1, A3, A5, A8–A9; adds revision validation to B.

### Minimal revision records

Add optional graph field `revisions`, default `[]`. It is mandatory and nonempty in P2/P3; forbidden nonempty in P1/P4.

```json
{
  "revisions": [
    {
      "id": "r0",
      "universe": "U",
      "order": 0,
      "transition": null
    },
    {
      "id": "r1",
      "universe": "U",
      "order": 1,
      "transition": {
        "kind": "overwrite",
        "from": "journal-intervention",
        "to": "revised-history-entry",
        "traveller": "evan-mind",
        "memory": "retained"
      }
    }
  ]
}
```

Exact rules:

- Revision IDs are unique within the graph’s `revisions` collection.
- `order` is a nonnegative integer; values are exactly `0..n-1`. Array order is irrelevant.
- All records reference the graph’s sole world.
- Order zero has `transition:null`; every later record has exactly one transition from its immediate predecessor.
- `transition.kind`: `"overwrite"` in P2; `"reset"` in P3.
- `transition.memory`: `"retained"`, `"none"`, or `"unknown"` in P2; exactly `"retained"` in P3.
- `transition.traveller` references a declared traveller. P3 transitions name the graph thread’s traveller.
- `from` and `to` reference events in predecessor and destination revisions respectively.
- Normal transition endpoints are `exit` → `entry`, with increasing `story_order`.
- A terminal P2 overwrite with `memory:"none"` may use `cutoff` → `entry`; the cutoff must be the thread’s final exit and the thread must not visit that successor revision.
- Endpoint citations provide transition evidence. Unsupported interpretation details must also be declared in `assumptions`; no production evidence is generated.
- No revision is a universe, descendant, sibling, instance of world duplication, or lane.

### State attachment

Add required `revision` to **every event in P2/P3**:

```json
{
  "id": "revised-history-entry",
  "kind": "entry",
  "universe": "U",
  "revision": "r1",
  "story_order": 21,
  "world_time": null,
  "label": "Revised history",
  "cite": {
    "source": "film",
    "page": null,
    "scene": null,
    "locator": "Journal revision",
    "status": "unavailable"
  }
}
```

Add required `revision` to **every visit in P2/P3**:

```json
{
  "id": "v1",
  "traveller": "evan-mind",
  "universe": "U",
  "revision": "r1",
  "entry": "revised-history-entry",
  "exit": "next-intervention",
  "passes": []
}
```

Add thread link kind `"revision"`:

```json
{
  "from_visit": "v0",
  "to_visit": "v1",
  "kind": "revision",
  "revision": "r1"
}
```

> The link references the destination revision’s transition. Its `from`/`to` events must equal the adjacent visit endpoints; its traveller must match the thread. Following the link requires `memory:"retained"`. A visit cannot straddle revisions. Segments derive revision from their endpoints; beats derive it from their segment; fates derive it from their event. No duplicate revision field is added to those records.

### Supersession and fate semantics

> Under P2, at revision position `k`, revisions `<k` are superseded, `k` is current, and `>k` are not yet applied. The default final view selects the maximum order. Retained historical records do not assert persistent historical worlds. Superseded fates remain cited facts of their revision; they contribute nothing to the current-state fate display or any census. No fate or bodily state carries forward without an explicit record.

> Under P3, lower-order records are completed iterations, not superseded branch worlds. Reset establishes an authored new iteration of world state; it does not automatically copy any fate record. The same traveller ID and `memory:"retained"` express mind persistence. The last iteration may proceed beyond the repeated date without another reset.

Extend A5 `status` with `"nonexistent"`, legal only in P2:

> `nonexistent` means the named embodiment is absent from that revision’s history; it does not mean death, a dead world, or erasure of the document’s character/traveller identity. An instance ID may designate an embodiment present in an earlier revision but absent in a later one. It may not designate both an absent adult embodiment and a fetus that actually lived and died. Death and nonexistence need separate identities where that distinction matters. No thread visit may occupy an embodiment throughout an interval explicitly recorded as nonexistent.

Add optional visit field:

```json
{"instance": "evan-adult"}
```

> `instance` defaults to `null`, meaning unknown embodiment, not proof of existence. A non-null instance must belong to the visit’s world. An explicit nonexistent fate at a visited event rejects that occupancy. Unknown embodiment may not be used to assert mind survival after an explicitly terminal `memory:"none"` transition.

Exact errors:

- `E210 {path}: revisions must have unique contiguous order values starting at 0.`
- `E211 {path}: revision transition must connect the immediately preceding revision to this revision.`
- `E212 {path}: event revision does not belong to event universe.`
- `E213 {path}: visit endpoints must belong to visit revision '{revision}'.`
- `E214 {path}: revision link does not match adjacent visit endpoints and traveller.`
- `E215 {path}: thread revision link requires retained memory.`
- `E216 {path}: segment endpoints must belong to one revision.`
- `E217 {path}: instance '{instance}' is alive after its recorded death in revision '{revision}'.`
- `E218 {path}: thread occupies nonexistent instance '{instance}'.`
- `E219 {path}: terminal overwrite must end the thread at its source cutoff.`
- `E220 {path}: P3 reset requires retained memory for the thread traveller.`

---

## AMEND-3 — PROOF MINI-ENCODES

**Amends:** A10 and D Patch 10; adds interpretation fixtures.

These are **field projections**, not standalone documents. Merge each into its fixture’s normal A1 envelope; preserve all omitted required arrays. Common envelope: `schema_version:2`, `validation_profile:"evidence_pending"`, `interpretation_rules:"none"`, `meta.axis:"story_order"`, source `film` containing the authored film/edition interpretation ledger, declared namespace `F`. Declare characters `phil`, `rita`, `evan` and travellers `phil-mind`, `evan-mind` as applicable. Unshown graph arrays are empty.

Calendar values below are numeric day-of-month on the declared illustrative clock; they are not elapsed-time layout distances. The Groundhog fixtures depict selected repetitions, not an invented exhaustive iteration count.

### (a) Groundhog Day — P3

```json
{
  "interpretation_profile": "P3",
  "graphs": [{
    "namespace": "F",
    "universes": [{"id":"U","label":"Punxsutawney","origin":{"kind":"initial"}}],
    "instances": [
      {"id":"phil-body","character":"phil","universe":"U","native_to_universe":true,"provenance":"native"},
      {"id":"rita-body","character":"rita","universe":"U","native_to_universe":true,"provenance":"native"}
    ],
    "revisions": [
      {"id":"r0","universe":"U","order":0,"transition":null},
      {"id":"r1","universe":"U","order":1,"transition":{"kind":"reset","from":"x0","to":"s1","traveller":"phil-mind","memory":"retained"}},
      {"id":"r2","universe":"U","order":2,"transition":{"kind":"reset","from":"x1","to":"s2","traveller":"phil-mind","memory":"retained"}}
    ],
    "events": [
      {"id":"s0","kind":"start","universe":"U","revision":"r0","story_order":0,"world_time":{"clock":"local-calendar","value":2,"unit":"February-day"},"label":"February 2; selected iteration","cite":{"source":"film","page":null,"scene":null,"locator":"Repeated February 2","status":"unavailable"}},
      {"id":"x0","kind":"exit","universe":"U","revision":"r0","story_order":1,"world_time":null,"label":"Iteration ends","cite":{"source":"film","page":null,"scene":null,"locator":"Overnight reset","status":"unavailable"}},
      {"id":"s1","kind":"entry","universe":"U","revision":"r1","story_order":2,"world_time":{"clock":"local-calendar","value":2,"unit":"February-day"},"label":"February 2 again; Phil remembers","cite":{"source":"film","page":null,"scene":null,"locator":"Remembered repetition","status":"unavailable"}},
      {"id":"x1","kind":"exit","universe":"U","revision":"r1","story_order":3,"world_time":null,"label":"Another reset","cite":{"source":"film","page":null,"scene":null,"locator":"Repeated awakening","status":"unavailable"}},
      {"id":"s2","kind":"entry","universe":"U","revision":"r2","story_order":4,"world_time":{"clock":"local-calendar","value":2,"unit":"February-day"},"label":"Final represented February 2","cite":{"source":"film","page":null,"scene":null,"locator":"Final repeated day","status":"unavailable"}},
      {"id":"end","kind":"cutoff","universe":"U","revision":"r2","story_order":5,"world_time":{"clock":"local-calendar","value":3,"unit":"February-day"},"label":"February 3; life continues","cite":{"source":"film","page":null,"scene":null,"locator":"Ending awakening","status":"unavailable"}}
    ],
    "fates": [
      {"id":"rita0","universe":"U","instance":"rita-body","event":"s0","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita in represented day","status":"unavailable"}},
      {"id":"rita1","universe":"U","instance":"rita-body","event":"s1","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita restored in repeated day","status":"unavailable"}},
      {"id":"rita2","universe":"U","instance":"rita-body","event":"s2","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita in final repeated day","status":"unavailable"}}
    ],
    "thread": {"traveller":"phil-mind","visits":[
      {"id":"v0","traveller":"phil-mind","universe":"U","revision":"r0","instance":"phil-body","entry":"s0","exit":"x0","passes":[]},
      {"id":"v1","traveller":"phil-mind","universe":"U","revision":"r1","instance":"phil-body","entry":"s1","exit":"x1","passes":[]},
      {"id":"v2","traveller":"phil-mind","universe":"U","revision":"r2","instance":"phil-body","entry":"s2","exit":"end","passes":[]}
    ],"links":[{"from_visit":"v0","to_visit":"v1","kind":"revision","revision":"r1"},{"from_visit":"v1","to_visit":"v2","kind":"revision","revision":"r2"}]},
    "layout":{"lane_order":["U"],"collapsed_universes":[]},
    "assumptions":["P3 interpretation; selected repetitions only. Rita represents explicitly recorded townsfolk state; no population fate census. No townsfolk fate or memory is carried across reset."]
  }]
}
```

### (b) Groundhog Day — P1

Retain event IDs, kinds, coordinates, labels and citations from (a). Remove every event `revision`; bind `s0,x0` to `*d0`, `s1,x1` to `*d1`, and `s2,end` to `*d2`. Replace the remaining divergent fields with:

```json
{
  "interpretation_profile": "P1",
  "graphs": [{
    "namespace": "F",
    "universes": [
      {"id":"*d0","label":"Selected February 2 world","origin":{"kind":"preexisting","ancestry":"off_chart"}},
      {"id":"*d1","label":"Next represented sibling","origin":{"kind":"preexisting","ancestry":"off_chart"}},
      {"id":"*d2","label":"Final represented sibling","origin":{"kind":"preexisting","ancestry":"off_chart"}}
    ],
    "revisions": [],
    "instances": [
      {"id":"rita0-body","character":"rita","universe":"*d0","native_to_universe":true,"provenance":"native"},
      {"id":"rita1-body","character":"rita","universe":"*d1","native_to_universe":true,"provenance":"native"},
      {"id":"rita2-body","character":"rita","universe":"*d2","native_to_universe":true,"provenance":"native"}
    ],
    "transfers": [
      {"id":"t1","traveller":"phil-mind","from":{"universe":"*d0","exit":"x0"},"to":{"universe":"*d1","entry":"s1"},"mechanism":"apparent_reset","relation":{"kind":"siblings_off_chart"},"embodiment":{"mode":"unknown","from_instance":null,"to_instance":null}},
      {"id":"t2","traveller":"phil-mind","from":{"universe":"*d1","exit":"x1"},"to":{"universe":"*d2","entry":"s2"},"mechanism":"apparent_reset","relation":{"kind":"siblings_off_chart"},"embodiment":{"mode":"unknown","from_instance":null,"to_instance":null}}
    ],
    "fates": [
      {"id":"rita0","universe":"*d0","instance":"rita0-body","event":"s0","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita in represented day","status":"unavailable"}},
      {"id":"rita1","universe":"*d1","instance":"rita1-body","event":"s1","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita restored in repeated day","status":"unavailable"}},
      {"id":"rita2","universe":"*d2","instance":"rita2-body","event":"s2","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita in final repeated day","status":"unavailable"}}
    ],
    "thread": {"traveller":"phil-mind","visits":[
      {"id":"v0","traveller":"phil-mind","universe":"*d0","entry":"s0","exit":"x0","passes":[]},
      {"id":"v1","traveller":"phil-mind","universe":"*d1","entry":"s1","exit":"x1","passes":[]},
      {"id":"v2","traveller":"phil-mind","universe":"*d2","entry":"s2","exit":"end","passes":[]}
    ],"links":[
      {"from_visit":"v0","to_visit":"v1","kind":"transfer","transfer":"t1"},
      {"from_visit":"v1","to_visit":"v2","kind":"transfer","transfer":"t2"}
    ]},
    "layout":{"lane_order":["*d0","*d1","*d2"],"collapsed_universes":[]},
    "assumptions":["P1 alternate interpretation, not a claim that the film establishes multiverse physics. Sibling ancestry is authored off-chart; its parent is not invented."]
  }]
}
```

- P3 satisfies same-world adjacent-iteration transition rules; P1 satisfies different-world sibling-transfer rules.
- P3 reuses revision-scoped body identities; P1 uses independent per-world counterparts. Neither propagates Rita’s fate or invents later survival.
- P3 draws one baseline with iteration separators and `RESET / MEMORY RETAINED`; P1 draws persistent sibling lanes and `APPARENT RESET / SIBLING CUT`.
- The event identities, chronology, repeated dates and ordered consciousness route are unchanged.

### (c) The Butterfly Effect — P2

The protagonist is **Evan Treborn**; “Eikon” is treated as the request’s reference to Evan, not a second character. This fixture explicitly selects the **director’s-cut ending**. Its final prenatal intervention uses a home movie, not a journal. `evan-adult` being nonexistent does not deny that a fetus existed and died.

```json
{
  "interpretation_profile": "P2",
  "graphs": [{
    "namespace": "F",
    "universes": [{"id":"U","label":"One revised world","origin":{"kind":"initial"}}],
    "instances": [{"id":"evan-adult","character":"evan","universe":"U","native_to_universe":true,"provenance":"native"}],
    "revisions": [
      {"id":"r0","universe":"U","order":0,"transition":null},
      {"id":"r1","universe":"U","order":1,"transition":{"kind":"overwrite","from":"journal1","to":"childhood1","traveller":"evan-mind","memory":"retained"}},
      {"id":"r2","universe":"U","order":2,"transition":{"kind":"overwrite","from":"journal2","to":"childhood2","traveller":"evan-mind","memory":"retained"}},
      {"id":"r3","universe":"U","order":3,"transition":{"kind":"overwrite","from":"prenatal","to":"without-adult-evan","traveller":"evan-mind","memory":"none"}}
    ],
    "events": [
      {"id":"start","kind":"start","universe":"U","revision":"r0","story_order":0,"world_time":null,"label":"Initial represented history","cite":{"source":"film","page":null,"scene":null,"locator":"Director's cut; opening history","status":"unavailable"}},
      {"id":"journal1","kind":"exit","universe":"U","revision":"r0","story_order":1,"world_time":null,"label":"Evan reads a journal","cite":{"source":"film","page":null,"scene":null,"locator":"First selected journal intervention","status":"unavailable"}},
      {"id":"childhood1","kind":"entry","universe":"U","revision":"r1","story_order":2,"world_time":null,"label":"Evan's childhood intervention point","cite":{"source":"film","page":null,"scene":null,"locator":"Selected childhood revision","status":"unavailable"}},
      {"id":"journal2","kind":"exit","universe":"U","revision":"r1","story_order":3,"world_time":null,"label":"Evan reads again","cite":{"source":"film","page":null,"scene":null,"locator":"Next selected journal intervention","status":"unavailable"}},
      {"id":"childhood2","kind":"entry","universe":"U","revision":"r2","story_order":4,"world_time":null,"label":"Another childhood intervention point","cite":{"source":"film","page":null,"scene":null,"locator":"Further selected revision","status":"unavailable"}},
      {"id":"prenatal","kind":"cutoff","universe":"U","revision":"r2","story_order":5,"world_time":null,"label":"Home-movie-enabled prenatal intervention; thread ends","cite":{"source":"film","page":null,"scene":null,"locator":"Director's-cut prenatal ending","status":"unavailable"}},
      {"id":"without-adult-evan","kind":"entry","universe":"U","revision":"r3","story_order":6,"world_time":null,"label":"Resulting history: adult Evan never exists","cite":{"source":"film","page":null,"scene":null,"locator":"Director's-cut resulting history","status":"unavailable"}}
    ],
    "fates": [
      {"id":"adult0","universe":"U","instance":"evan-adult","event":"journal1","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Evan before revision","status":"unavailable"}},
      {"id":"adult1","universe":"U","instance":"evan-adult","event":"journal2","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Evan before further revision","status":"unavailable"}},
      {"id":"adult-absent","universe":"U","instance":"evan-adult","event":"without-adult-evan","status":"nonexistent","cite":{"source":"film","page":null,"scene":null,"locator":"Director's cut: no adult Evan in resulting history","status":"unavailable"}}
    ],
    "thread": {"traveller":"evan-mind","visits":[
      {"id":"v0","traveller":"evan-mind","universe":"U","revision":"r0","entry":"start","exit":"journal1","passes":[]},
      {"id":"v1","traveller":"evan-mind","universe":"U","revision":"r1","entry":"childhood1","exit":"journal2","passes":[]},
      {"id":"v2","traveller":"evan-mind","universe":"U","revision":"r2","entry":"childhood2","exit":"prenatal","passes":[]}
    ],"links":[{"from_visit":"v0","to_visit":"v1","kind":"revision","revision":"r1"},{"from_visit":"v1","to_visit":"v2","kind":"revision","revision":"r2"}]},
    "layout":{"lane_order":["U"],"collapsed_universes":[]},
    "assumptions":["Director's-cut P2 interpretation; selected interventions, not a complete scene ledger. r0-r2 are superseded histories, not surviving worlds. No visit or surviving consciousness is asserted in r3. Adult and prenatal embodiment are not conflated."]
  }]
}
```

---

## AMEND-4 — RENDER MAPPING

**Amends:** C1–C2; B30.

Exact persistent profile chips:

| Profile | Canvas text |
|---|---|
| P1, `interpretation_rules:"none"` | `P1 · BRANCH MULTIVERSE` |
| P1, `interpretation_rules:"waif"` | `P1 · BRANCH MULTIVERSE · THE WAIF HOUSE RULES` |
| P2 | `P2 · SINGLE MUTABLE TIMELINE` |
| P3 | `P3 · CLOSED LOOP · MIND PERSISTS` |
| P4 | `P4 · ONTOLOGY UNDECLARED` |

Required rendering invariants:

> **P2:** Draw one world baseline. Stack revision sections serially in revision order, never as parallel world lanes. Label each section `{world} / {revision} · CURRENT` or `{world} / {revision} · SUPERSEDED — NOT A COEXISTING WORLD`. Superseded backgrounds and state badges use grey/dim styling; strike the word `CURRENT` only when showing its replacement. Never strike or obscure authored prose or citations. Historical thread portions remain visible but are marked `HISTORICAL ROUTE`, not surviving consciousness. Revision connectors read `HISTORY OVERWRITE`.

> **P3:** Draw one world baseline with serial iteration sections labelled `{world} / {revision} · ITERATION {order}`. Reset connectors read `RESET / MEMORY RETAINED`; older sections read `COMPLETED ITERATION`. Calendar dates may repeat; narrative position still increases. Continuing beyond the loop’s date stays in the final iteration. No sibling lanes, branch tines, or supersession strike convention.

> **P4:** Draw observation-context columns with headers `OBSERVED CONTEXT {id} · WORLD IDENTITY UNDECLARED`. Connections are dashed and labelled `RELATION UNDECLARED`. No stars, already-running claims, split tines, or reset/overwrite badges.

> **Fates:** P2/P3 badges include revision ID. `nonexistent` uses `∅ · NONEXISTENT IN THIS REVISION`, never an `X` death cap. Superseded badges are excluded from current-state summaries. No profile enables survivor arithmetic.

> **Build:** Normalize and validate the profile before deriving placements. Every placement and connector retains its exact event/world/revision IDs. Layout reads those records, never stale loop variables or nearby lanes. Profile-specific geometry assertions run after routing.

Additional errors:

- `E230 {path}: revision or iteration is rendered as a coexisting universe lane.`
- `E231 {path}: superseded history is missing its non-coexistence marking.`
- `E232 {path}: iteration reset is missing its retained-memory marking.`
- `E233 {path}: undeclared ontology is rendered with an asserted world relationship.`

Replace `E170` with:

`E170 {path}: actual universe merges are not supported in schema v2.1; consciousness movement, overwrite, and reset are distinct operations.`

---

## AMEND-5 — REGRESSION GUARDS

**Amends:** B7–30; E2 header.

Add these exact fail-fast semantic checks:

| Rejected condition | Exact error |
|---|---|
| P2 has anything other than one universe per graph | `E240 {path}: P2 requires exactly one world; revisions are not universes.` |
| P3 has anything other than one universe per graph | `E241 {path}: P3 requires exactly one loop world; iterations are not universes.` |
| P2/P3 layout differs from `[sole_world_id]`, or has collapsed universes | `E242 {path}: {profile} forbids sibling lanes and collapsed universe stubs.` |
| P2/P3 uses `born`/`preexisting`, starred IDs, splits, split/outcome events, transfers, split passes, or split/transfer thread links | `E243 {path}: {profile} forbids P1 branching or cross-universe routing machinery.` |
| P1 contains nonempty revisions, event/visit `revision`, revision links, or `nonexistent` | `E244 {path}: P1 forbids same-world revision machinery and supersession fates.` |
| P2/P3 has missing/empty revisions | `E245 {path}: {profile} requires a nonempty ordered revision history.` |
| P2/P3 event or visit omits revision | `E246 {path}: {profile} requires an explicit revision reference.` |
| P2 uses reset, or P3 uses overwrite | `E247 {path}: transition kind '{kind}' is incompatible with {profile}.` |
| P4 asserts ancestry, siblings, split/reset/overwrite semantics, or uses revision machinery | `E248 {path}: P4 must leave world relationships undeclared.` |
| P2/P3 graphs disagree on world identity or revision declarations | `E249 {path}: {profile} graphs must share one world identity and identical revision declarations.` |
| Non-P1 transfer is not a legal P4 observed transition | `E250 {path}: transfers are supported only by P1 or undeclared P4 observation continuity.` |

Replace B20 `E122` with:

`E122 {path}: P1 does not support same-world reset or overwrite; select P2 or P3 and encode revisions.`

Additional binding regression requirements:

> Test both Groundhog encodings against their declared profiles. Changing only P1→P2 must fail with `E240`, `E242`, or `E243`; changing only P3→P1 must fail with `E244`. Retaining one lane while hiding extra P2 universes must still fail `E240`. Renaming branch lanes to “revisions” must not bypass structural checks. Shuffling universe, revision, event, or transfer arrays must not change ancestry, revision order, thread route, citations, or fate scope. Negative tests require exit code 2 and expected diagnostics, never a crash.

> Retain all v2 reference, endpoint, split-outcome, unknown-origin witness, explicit-fate, citation-manifest, namespace, and connected-thread tests. Add dead→alive within one revision as a rejection and dead→explicitly alive after a P3 reset as an acceptance. No test may rely on inferred embodiment, inferred survival, inferred ancestry, or inferred memory.

**Amended Ben’s Story header; all remaining E2 data stays unchanged:**

```json
{
  "schema_version": 2,
  "interpretation_profile": "P1",
  "interpretation_rules": "waif",
  "validation_profile": "evidence_pending",
  "meta": {
    "title": "THE WAIF — Ben's Story",
    "subtitle": "Canon topology fixture; screenplay locators pending",
    "footer": "Universe identity is separate from consciousness and character fate.",
    "axis": "story_order"
  }
}
```

A10’s existing synthetic fixture receives `"interpretation_profile":"P1"`; its explicitly authored trigger split already satisfies P1 without enabling house-wide trigger physics.

---

## AMEND-6 — CONSISTENCY SWEEP

**Amends:** every supplied section containing hard-coded P1 framing.

| Section | One-line replacement |
|---|---|
| Title/status block | “v2.1 is ontology-neutral; THE WAIF is the declared P1 house interpretation.” |
| §0.1 | “Automatic trigger splitting and paired survival/death are house rules, not core event physics.” |
| §0.2 | “Reset semantics are selected by profile: sibling cut, overwrite, retained-mind iteration, or undeclared transition.” |
| §0.3 | “World existence, embodiment fate, consciousness continuity and history-currentness are separate facts.” |
| §0.4 | “P1 pre-existing worlds backpropagate to chart top; revision/iteration starts do not imply world births.” |
| §0.7 | “Immutable split-birth identity applies to P1 born worlds only.” |
| §0 evidence-limitation conclusion | “Evidence completeness is independent of the document’s explicitly selected ontology.” |
| A1 document/root/graph fields | “Declare interpretation separately from evidence mode; normalize new optional arrays to empty and apply profile-specific graph scope.” |
| A2 universes/origins/continuation | “Origins and branch continuation describe P1 worlds; P2/P3 use one world with ordered states, and P4 uses witnessed observation contexts.” |
| A3 events/coordinates | “Events retain narrative/world-time coordinates; P2/P3 additionally require revision membership, and split ports exist only in P1.” |
| A4 splits/trigger physics/source disposition | “This section defines authored P1 splits; it neither classifies all interventions nor requires other profiles to branch.” |
| A5 instances/fates/mortality | “Fates are world-local in P1, revision-local in P2, iteration-local in P3, and observation-local in P4.” |
| A6 transfers/reset/Groundhog mapping | “P1 transfers cross worlds; P2 overwrites and P3 resets use revisions; P4 records undeclared observed transitions.” |
| A7 actual merges | “Actual merging remains unsupported across profiles; THE WAIF ‘joins’ mean P1 transfers only.” |
| A8 segments/beats | “Segments stay within one world-state context and cannot cross a split, revision, or iteration boundary.” |
| A9 thread/links/unvisited worlds | “Visits and explicit links remain authoritative; their context is a world, revision, iteration, or undeclared observation according to profile.” |
| A10 production example | “Declare P1 on this synthetic mechanism fixture; it tests P1 machinery, not universal film ontology.” |
| A11 lanes/stubs/joins/arcs migration rows | “Interpret legacy geometry only after profile selection and explicit semantic annotation.” |
| A11 same-lane loop/reset row | “Require P2 revision, P3 iteration, P1 sibling-transfer, or P4 undeclared-transition annotation; never force a sibling interpretation.” |
| B7–21, B23–26, B30 | “Apply the profile-conditional invariant matrix and revision guards; retain all unaffected checks.” |
| B29 actual merges | “Use the v2.1 merge diagnostic; overwrite and reset are not merges.” |
| B31 migration | “Missing ontology/state annotations fail migration rather than being inferred from lane shape.” |
| C1 universe/origin/split/transfer/reset/fate primitives | “Select world, revision, iteration, or observation primitives from the declared profile.” |
| C1 right-hand death orientation | “Screen-right death tines apply only to explicitly authored P1 dying negative outcomes.” |
| C1 thread rendering | “Traverse visits and split, transfer, or revision links without inferring a route from lanes.” |
| C2 baselines/arcs/version counters/chrome | “Build profile-specific state baselines and transitions; display profile plus transition ordinals, never world/population counts.” |
| C2 layout staging | “Causal cycles do not create layout precedence; only placement constraints participate in layout-cycle detection.” |
| D Patch 2 | “Implement interpretation profiles separately from evidence profiles, including revision and causal records.” |
| D Patch 3 | “Add cross-profile rejection tests, revision-state checks and explicit causal-cycle tests before rendering.” |
| D Patch 4 | “Convert the existing split demo as P1; Ben is the house-profile acceptance test, not the core ontology test.” |
| D Patch 5 | “Keep P1 origin/split rendering isolated from P2/P3 serial-state and P4 observation rendering.” |
| D Patch 6 | “Route all declared link kinds; convert BTTF2 under explicit P2 revision semantics rather than compulsory universe reallocation.” |
| D Patch 7 | “Scope instances and fates by profile while retaining all cited segment/beat and no-census protections.” |
| D Patch 8 | “`pulls:` implies automatic split only with P1 house rules; otherwise require authored profile-appropriate intervention semantics.” |
| D Patch 9 | “Expose profile selection, revision/iteration membership, memory continuity and profile-scoped fates through the shared validator.” |
| D Patch 10, Groundhog | “Maintain both P3 loop and P1 sibling-cut encodings of the same selected event graph.” |
| D Patch 10, Butterfly | “Use P2 superseded histories with an explicitly selected ending; do not fabricate a surviving final traveller.” |
| D Patch 10, Primer | “Declare P1 as the fixture interpretation, preserving unknown mechanisms and ancestry without inferred copy counts.” |
| D Patch 10, documentation conclusion | “Supersede universal no-rewind framing; same-world revision/reset is valid under P2/P3, not under P1 house rules.” |
| E1 | “These canon assertions and structural allocations apply to the explicitly declared THE WAIF P1 house fixture.” |
| E2 | “Add the P1/waif header; preserve the supplied fixture body and citations unchanged.” |

| Fixture film | Profile(s) used | New fields required | Invariants that changed form |
|---|---|---|---|
| THE WAIF / Ben’s Story | P1 + `waif` | `interpretation_profile`, `interpretation_rules` | Automatic-trigger law becomes house-scoped; existing branch fixture semantics retained |
| Groundhog Day | P3 and alternate P1 | Profile; P3 `revisions`, event/visit `revision`, revision links | World cardinality, reset endpoints, memory, fate terminality, lanes |
| The Butterfly Effect — director’s cut | P2 | Profile, revisions, revision membership/links, terminal `memory:"none"`, `status:"nonexistent"` | Supersession, revision-local mortality, terminal thread, absent embodiment |
| Back to the Future Part II | P2 | Profile, revisions, revision membership/links | One-world identity, overwritten history, fate scope, no sibling lanes |
| Primer | P1; P4 for a separately undeclared reading | Profile; P4 `mechanism:"observed_transition"` where applicable | Branch assertions versus undeclared relationships; no inferred ancestry or copy census |

===== PART 3: v2.2 INTEGRATION (supersedes conflicting PART-2 text) =====
**Design decision.** Replace the flat profile list with parameters, but reject the proposed tuple literally: presentation reversal is not physical inversion; undeclared ontology is not a combination of negative assertions; a primary/tangent pair is not necessarily sibling branching; and divergence and clock shear can coexist. Use the corrected parameter set below: separate `presentation`, explicit `declaration`, an additional `primary-tangent` topology value, and a set-valued `metric`. Retain P1–P4 as backward-compatible named presets. Parameters authorize mechanisms; they never create worlds, transitions, memories, bodies, or causal relations without records.

# v2.2 INTEGRATION AMENDMENT LIST

## 1. IN-1 — PARAMETRIC PROFILE

**Targets:** title; §0; A1; B; AMEND-1, AMEND-4–6.

### Profile JSON and presets

`schema_version` remains `2`; specification revision becomes `2.2`.

`interpretation_profile` accepts a registered preset string or the following exact object shape:

```json
{
  "interpretation_profile": {
    "declaration": "declared",
    "direction": "forward",
    "presentation": "dual",
    "branching": "none",
    "revision": "none",
    "loop": "none",
    "metric": []
  },
  "interpretation_rules": "none"
}
```

Field domains:

| Field | Domain |
|---|---|
| `declaration` | `declared`, `undeclared` |
| `direction` | `forward`, `inverted`, `per-traveller` |
| `presentation` | `story`, `dual` |
| `branching` | `none`, `siblings`, `knot`, `worldlines-with-metric`, `primary-tangent` |
| `revision` | `none`, `supersede`, `ladder-with-body-linkage` |
| `loop` | `none`, `memory-reset`, `fated-closed`, `doomed-collapsing`, `death-reset-external-anchor` |
| `metric` | Duplicate-free array containing `divergence-value` and/or `relativistic-clock-shear` |

For `declaration:"undeclared"`, every other parameter is exactly `null`:

```json
{
  "interpretation_profile": {
    "declaration": "undeclared",
    "direction": null,
    "presentation": null,
    "branching": null,
    "revision": null,
    "loop": null,
    "metric": null
  }
}
```

The following table is the normative preset registry. Tuple columns are literal field values, not inferred film physics.

| Preset | declaration | direction | presentation | branching | revision | loop | metric |
|---|---|---|---|---|---|---|---|
| `P1` | declared | forward | story | siblings | none | none | `[]` |
| `waif` | declared | forward | story | siblings | none | none | `[]` |
| `P2` | declared | forward | story | none | supersede | none | `[]` |
| `P3` | declared | forward | story | none | none | memory-reset | `[]` |
| `P4` | undeclared | null | null | null | null | null | `null` |
| `tenet` | declared | per-traveller | story | none | none | fated-closed | `[]` |
| `memento` | declared | forward | dual | none | none | none | `[]` |
| `dark` | declared | forward | story | knot | none | fated-closed | `[]` |
| `steins-gate` | declared | forward | story | worldlines-with-metric | none | none | `["divergence-value"]` |
| `looper` | declared | forward | story | none | ladder-with-body-linkage | none | `[]` |
| `eot` | declared | forward | story | none | none | death-reset-external-anchor | `[]` |
| `darko` | declared | forward | story | primary-tangent | none | doomed-collapsing | `[]` |
| `azkaban` | declared | forward | story | none | none | fated-closed | `[]` |
| `predestination` | declared | forward | story | none | none | fated-closed | `[]` |
| `timecrimes` | declared | forward | story | none | none | fated-closed | `[]` |
| `interstellar` | declared | forward | story | none | none | none | `["relativistic-clock-shear"]` |

`waif` additionally requires `interpretation_rules:"waif"`. Existing `"P1"` plus `"waif"` remains its exact alias. No other preset enables house rules.

Preset strings remain canonical; expansion is a validator operation, not a mandatory source rewrite. Authoring defaults to `P4`; canonical omission still fails E200.

### Combination rules

> `direction` describes continuous bodily evolution relative to a declared world clock, not the sign of a time-travel displacement. A forward-evolving traveller may jump into the past.

> `branching:"none"` permits exactly one world identity across the document’s rendered graphs. `siblings` permits independently persistent worlds but does not assert that every pair are siblings. `knot`, `worldlines-with-metric`, and `primary-tangent` require their respective topology records.

> `revision != "none"` requires `branching:"none"` and `loop:"none"`. Iterating loops require `branching:"none"` and `revision:"none"`. `fated-closed` permits `none` or `knot`, with `revision:"none"`. `doomed-collapsing` requires `primary-tangent`, and conversely.

> `worldlines-with-metric` requires `divergence-value`; `divergence-value` requires `worldlines-with-metric`. Clock shear is independent of that pairing.

> A profile declaration is document-wide. Contradictory interpretations require separate documents, not silently different namespace physics.

Exact diagnostics:

```text
E201 /interpretation_rules: 'waif' requires the P1 parameter set and the P1 or waif preset.
E251 {path}: undeclared ontology requires null mechanism parameters.
E252 {path}: incompatible profile parameters: {detail}.
E253 {path}: mechanism '{mechanism}' is not enabled by the declared parameters.
E254 {path}: declared topology requires {requirement}.
```

### Re-scoping retained guarantees

Replace profile-name dispatch with mechanism predicates:

| Existing invariant family | v2.2 scope |
|---|---|
| Birth IDs, split ancestry, split cardinality and explicit tines | Every authored `splits` record; splits enabled only by `siblings` |
| Automatic trigger law | `interpretation_rules:"waif"`; an explicitly authored trigger split still carries A4’s contract |
| Revision ordering, endpoint membership, supersession | `revision != "none"` |
| Iteration ordering and reset membership | `loop` is `memory-reset` or `death-reset-external-anchor` |
| P4 restrictions and uncertainty markings | `declaration:"undeclared"` |
| Per-instance mortality | One world/state context, ordered along the instance’s bodily history |
| Namespace isolation, typed references, evidence, no census, exact endpoints | Every parameter combination |
| Ancestry acyclicity | Split-parent ancestry only; never causal, genealogy, or knot edges |

**New-record convention:** JSON below contains field projections, not standalone fixtures. New graph arrays default to `[]`. Every new semantic record carries `evidence_events`, a nonempty array of local event references, unless it already carries `cite`. Referenced event citations undergo E160–E162. Unknown facts require an explicit unknown variant where provided; omission is not an assertion.

Canvas chrome retains the v2.1 P1–P4 chips. New presets show `ONTOLOGY {preset}` plus all expanded parameter values. Custom profiles show `ONTOLOGY CUSTOM` plus those values. P4’s existing mandatory warnings remain unchanged. Missing or incorrect disclosure uses E202.

---

## 2. IN-2 — DIRECTION, GATES, COEXISTENCE, PINCERS

**Targets:** A1, A3, A5–A6, A9; B17–25; C1–C2.

### Bodily direction records

Add graph `motions`, `gates`, and `pincers`. Add optional instance fields `body` and `identity`, referencing IN-8 body and person identities respectively.

```json
{
  "motions": [
    {
      "id": "m-forward",
      "traveller": "protagonist-mind",
      "instance": "protagonist-younger",
      "from": "approach",
      "to": "turnstile-in",
      "proper_order": [0, 1],
      "direction": {"clock": "world-clock", "sign": 1},
      "evidence_events": ["approach", "turnstile-in"]
    },
    {
      "id": "m-inverted",
      "traveller": "protagonist-mind",
      "instance": "protagonist-older",
      "from": "turnstile-out",
      "to": "inverted-departure",
      "proper_order": [1, 2],
      "direction": {"clock": "world-clock", "sign": -1},
      "evidence_events": ["turnstile-out", "inverted-departure"]
    }
  ],
  "gates": [
    {
      "id": "turnstile-1",
      "kind": "turnstile",
      "location": "facility",
      "traveller": "protagonist-mind",
      "entry": "turnstile-in",
      "exit": "turnstile-out",
      "entry_direction": 1,
      "exit_direction": -1,
      "from_motion": "m-forward",
      "to_motion": "m-inverted",
      "evidence_events": ["turnstile-in", "turnstile-out"]
    }
  ],
  "pincers": [
    {
      "id": "operation",
      "motions": ["red-motion", "blue-motion"],
      "coordination_links": ["briefing-link"],
      "evidence_events": ["briefing"]
    }
  ]
}
```

`proper_order` contains two finite numbers with the second greater than the first. It is an authored coordinate within one body biography, not an elapsed-time measurement.

Add event `location`; add event kinds `gate_entry`, `gate_exit`. Add optional visit `motion`. Add thread link:

```json
{
  "from_visit": "v-forward",
  "to_visit": "v-inverted",
  "kind": "gate",
  "gate": "turnstile-1"
}
```

`locations` is defined in IN-7; clocks may be declared without enabling relativistic shear.

Exact invariants:

> Each motion stays within one world/state context and names an instance belonging to that world. Its endpoint world-time values use its declared clock and a common unit. Their nonzero difference has the declared sign. Its proper-order interval increases regardless of sign.

> Under `per-traveller`, every represented bodily visit has an explicit motion. Under `forward` or `inverted`, supplied motions must agree with the profile sign.

> A turnstile connects adjacent motions of the same traveller and body identity, in the same world/state context, at one location and one world-clock value. Entry and exit signs are opposites. A gate does not create a universe, revision, or iteration.

> Two coexisting instances may share a body identity only when their represented proper-order intervals are disjoint. They are different temporal portions of one body, not two native births. Mere character equality never establishes body equality.

> A pincer contains at least one motion of each sign, all in one world, plus explicit causal coordination links. Opposed motion alone does not establish coordination.

```text
E255 {path}: motion direction, endpoints, or bodily proper order disagree.
E256 {path}: turnstile must reverse one body's direction at one world-state location and time.
E257 {path}: same-body coexistence lacks distinct ordered bodily portions.
E258 {path}: temporal pincer requires opposed motions and explicit coordination links.
```

**Rendering:** retain one world baseline. Draw separately labelled instance tracks inside its lane. Arrowheads follow traveller progression; on a displayed world-time axis an inverted track points toward decreasing world time. On story/view axes, arrowheads follow the routed ports and carry `WORLD-TIME −`; do not reverse them merely to obtain an upward arrow. Gates use paired direction ports; pincers use a coordination bracket and explicit information connectors. No second-world lane or compulsory second axis.

---

## 3. IN-3 — STORY/VIEW DUAL COORDINATES

**Targets:** A1 `meta.axis`; A3; A8; B23, B26–27; C2.

Allow `meta.axis:"story_order"` or `"view_order"`. Add `view_order` to events and beats:

```json
{
  "meta": {
    "title": "Memento",
    "subtitle": "",
    "footer": "",
    "axis": "view_order"
  }
}
```

```json
{
  "id": "remembered-action",
  "segment": "earlier-history",
  "story_order": 12,
  "view_order": 87,
  "text": "An earlier action is presented later.",
  "cite": {
    "source": "film",
    "page": null,
    "scene": null,
    "locator": "Selected sequence",
    "status": "unavailable"
  }
}
```

Exact rules:

> `story_order` is authored schematic progression of the represented story, not elapsed time. `view_order` is authored presentation position. Neither is inferred from array order, memory ability, or the other coordinate.

> With `presentation:"dual"`, every event and beat carries both finite coordinates. With `presentation:"story"`, `view_order` is optional; selecting the view axis requires it on every rendered event and beat. P4 may carry either coordinate without asserting temporal physics.

> Segment membership and strict beat containment remain defined by `story_order`, not display order. A view rendering may fragment a segment into labelled visible pieces; every piece retains the same segment ID. It must not fabricate a new history interval.

> Repeated presentation of one event uses graph `presentations` records, not duplicate event identities:

```json
{
  "presentations": [
    {
      "id": "second-view",
      "event": "remembered-action-event",
      "view_order": 95,
      "perspective_instance": "leonard-body",
      "evidence_events": ["remembered-action-event"]
    }
  ]
}
```

`perspective_instance` is an instance ID or `null`. The event’s own `view_order` identifies its first represented presentation.

Mandatory legend:

```text
AXIS: STORY ORDER · SCHEMATIC, NOT ELAPSED TIME
AXIS: VIEW ORDER · PRESENTATION, NOT PHYSICAL TIME
```

Display exactly the applicable line. Dual-coordinate event/beat labels expose both values.

```text
E259 {path}: displayed coordinate '{axis}' is missing or non-finite.
E260 {path}: story/view coordinates or axis legend have been conflated.
```

Memento requires no inverted body, time-travel transfer, loop reset, or inferred memory mechanism.

---

## 4. IN-4 — REVISION LADDERS AND BODY LINKAGE

**Targets:** AMEND-2; A5, A9; B revision checks; C1.

Retain `revisions`. Add graph `revision_ladders`; add revision field `ladder`:

```json
{
  "revision_ladders": [
    {
      "id": "joe-ladder",
      "universe": "U",
      "evidence_events": ["first-intervention"]
    }
  ],
  "revisions": [
    {
      "id": "r0",
      "universe": "U",
      "ladder": "joe-ladder",
      "order": 0,
      "transition": null
    },
    {
      "id": "r1",
      "universe": "U",
      "ladder": "joe-ladder",
      "order": 1,
      "transition": {
        "kind": "overwrite",
        "from": "young-intervention",
        "to": "older-response",
        "traveller": "joe-mind",
        "memory": "retained"
      }
    }
  ]
}
```

For legacy P2/P3 records, missing `ladder` denotes their existing single ordered sequence; no source rewrite is required. With `ladder-with-body-linkage`, ladder declarations and membership are mandatory. Orders are contiguous **within each ladder**. Revision IDs remain graph-wide unique. Events still name exactly one revision.

Add graph `body_linkages`:

```json
{
  "body_linkages": [
    {
      "id": "young-old-joe",
      "from_instance": "young-joe",
      "to_instance": "old-joe",
      "body": "joe-body-history",
      "channels": ["wound", "memory"],
      "updates": [
        {
          "id": "scar-update",
          "channel": "wound",
          "from": "young-scar",
          "to": "old-scar",
          "from_revision": "r0",
          "to_revision": "r1",
          "effect": "replace",
          "state_before": "unscarred",
          "state_after": "scarred"
        },
        {
          "id": "memory-update",
          "channel": "memory",
          "from": "changed-experience",
          "to": "changed-recollection",
          "from_revision": "r1",
          "to_revision": "r2",
          "effect": "replace",
          "state_before": "memory-state-1",
          "state_after": "memory-state-2"
        }
      ],
      "evidence_events": ["young-scar", "old-scar", "changed-recollection"]
    }
  ]
}
```

`channels`: nonempty subset of `wound`, `memory`, `existence`. `effect`: `replace` or `remove`; `state_before`/`state_after`: nonempty authored state identifiers, with `state_after:null` only for `remove`.

Exact invariants:

> A body linkage relates explicit temporal instances of the same declared body identity. Every update names its source and target events and revisions; each event belongs to its stated revision and linkage instance’s world. Revision changes advance the declared ladder; same-revision updates are legal and do not create a revision.

> An update transmits only its named state channel. Wound propagation does not imply memory propagation, death, nonexistence, or world erasure. Memory replacement is not consciousness transfer and does not change traveller identity.

> “Immediate” means the authored target response event, not equal `story_order`, equal age, or an inferred physical propagation rate.

> No state propagates across ladder boundaries without an explicit update identifying both ladders’ revisions. Multiple ladder displays are histories of one world, never parallel world lanes.

> Supersession, E218 occupancy rejection, and terminal `memory:"none"` rules remain binding. A linked removal of existence requires an explicit `nonexistent` fate; a lethal effect requires an explicit `dead` fate.

```text
E261 {path}: revision ladder membership or predecessor order is invalid.
E262 {path}: body-linkage update lacks matching body, event, revision, or state-channel identities.
E263 {path}: body linkage implies an unrecorded fate or propagation.
```

---

## 5. IN-5 — LOOP TYPES

**Targets:** A1, A3, A5–A6, A9; AMEND-2; B; C1.

Add graph `loops`, discriminated by `kind`.

### A. Fated closed history

```json
{
  "id": "time-turner-loop",
  "kind": "fated-closed",
  "universes": ["U"],
  "entry": "return-to-past",
  "closure": "departure-already-observed",
  "cycle": "rescue-cycle",
  "instances": ["harry-younger", "harry-older", "hermione-younger", "hermione-older"],
  "reset_memory": "not-applicable",
  "evidence_events": ["return-to-past", "departure-already-observed"]
}
```

> A fated loop has no reset, overwrite, or iteration records. Its `cycle` is a declared causal cycle. Younger and older selves are distinct instances with explicit body identities and ordered bodily portions. Ordinary autobiographical memory continues; “zero memory persistence” means **no memory carried across a reset**, not amnesia after travel.

> With `branching:"none"`, all loop members occupy the same world. With `knot`, multiple worlds require IN-6 entanglement. No event is overwritten merely because another instance witnesses it.

### B. Doomed collapsing tangent

```json
{
  "id": "tangent-loop",
  "kind": "doomed-collapsing",
  "primary_universe": "P",
  "tangent_universe": "T",
  "opens": "tangent-opening",
  "closes": "tangent-collapse",
  "stability": "unstable",
  "lifetime": {
    "clock": "tangent-clock",
    "start": 0,
    "end": 28,
    "unit": "day"
  },
  "closure_cycle": "artifact-closure",
  "termination": "world-collapse",
  "residues": [
    {
      "object": "engine",
      "from": "engine-in-tangent",
      "to": "engine-in-primary",
      "transfer": "engine-return"
    }
  ],
  "evidence_events": ["tangent-opening", "tangent-collapse", "engine-in-primary"]
}
```

The numbers above are illustrative allocations, not an edition-independent Darko duration assertion.

> Primary and tangent IDs are distinct. This relation asserts neither sibling ancestry nor that primary history is superseded. The tangent has no events after its declared physical lifetime. Its baseline ends with `TANGENT WORLD COLLAPSES`, not a character death cap.

> Closure must be supported by `closure_cycle`; every residue names an object identity and an explicit object transfer joining the named endpoint events. Residue survival does not imply surviving tangent persons.

### C. Death reset with external anchor

Use existing `revisions` as iteration records; `transition.kind:"reset"` remains unchanged. Add:

```json
{
  "id": "omega-loop",
  "kind": "death-reset-external-anchor",
  "universe": "U",
  "owner": "omega",
  "reset_source": "omega-network",
  "subjects": ["cage-mind"],
  "anchors": [
    {
      "id": "a0",
      "event": "initial-anchor",
      "world_time": {"clock": "earth-clock", "value": 100, "unit": "hour"}
    },
    {
      "id": "a1",
      "event": "earlier-anchor",
      "world_time": {"clock": "earth-clock", "value": 90, "unit": "hour"}
    }
  ],
  "resets": [
    {
      "revision": "r1",
      "trigger": "cage-death",
      "trigger_fate": "cage-dead-r0",
      "anchor": "a0",
      "source": "omega-network",
      "memory_subjects": ["cage-mind"]
    },
    {
      "revision": "r2",
      "trigger": "final-death",
      "trigger_fate": "cage-dead-r1",
      "anchor": "a1",
      "source": "omega-network",
      "memory_subjects": ["cage-mind"]
    }
  ],
  "ending": {
    "event": "post-reset-ending",
    "state": "inactive",
    "further_resets": "not-asserted"
  },
  "evidence_events": ["cage-death", "final-death", "post-reset-ending"]
}
```

`owner` and `reset_source` reference IN-8 identities. Anchor times must equal their anchor events’ times. Reset destinations occur at the selected anchor coordinate but belong to the new iteration.

> Every represented reset has exactly one reset record, an explicit dead fate at its trigger, an enabled source identity, a selected anchor, and explicit retaining subjects. Owner, source, victim, and retaining subject are separate roles; equality is permitted only through explicit shared IDs.

> The reset is a world-state operation, not a body/memory transfer. Its revision transition still identifies the thread’s retaining traveller. No fate or non-subject memory is copied.

> Anchor changes are explicit selections, never inferred from an earlier-looking shot. A reset into a final iteration and continuation without another reset are distinct from “no final reset.” An undecided ending belongs in a separately P4 encoding, not a falsely definite anchor.

For `memory-reset`, existing P3 records remain sufficient; optional `loops` records use:

```json
{
  "id": "daily-loop",
  "kind": "memory-reset",
  "universe": "U",
  "subjects": ["phil-mind"],
  "revisions": ["r0", "r1", "r2"],
  "evidence_events": ["s0", "s1", "s2"]
}
```

Exact diagnostics:

```text
E264 {path}: fated-closed loop cannot reset, revise, or duplicate its history.
E265 {path}: collapsing loop lacks a bounded lifetime, causal closure, or explicit residue transfer.
E266 {path}: event lies outside the tangent world's declared lifetime.
E267 {path}: external-anchor reset lacks matching source, death trigger, anchor, or retaining subjects.
E268 {path}: reset destination or terminal state disagrees with the declared anchor sequence.
```

---

## 6. IN-6 — KNOT TOPOLOGY AND BOOTSTRAP GENEALOGY

**Targets:** A1–A3, A5, A7; AMEND-1 causal machinery; B; C1.

Add graph arrays:

```json
{
  "character_versions": [
    {
      "id": "martha-adam",
      "character": "martha",
      "universe": "A",
      "instances": ["martha-A-young", "martha-A-older"],
      "evidence_events": ["martha-A-observed"]
    },
    {
      "id": "martha-eve",
      "character": "martha",
      "universe": "E",
      "instances": ["martha-E-young", "martha-E-older"],
      "evidence_events": ["martha-E-observed"]
    }
  ],
  "correspondences": [
    {
      "id": "martha-counterparts",
      "kind": "counterparts",
      "versions": ["martha-adam", "martha-eve"],
      "evidence_events": ["counterpart-encounter"]
    }
  ],
  "genealogy": [
    {
      "id": "parent-edge",
      "parent": "parent-person",
      "child": "child-person",
      "parent_instance": "parent-at-conception",
      "child_instance": "child-at-birth",
      "causal_link": "conception-to-birth",
      "evidence_events": ["conception", "birth"]
    }
  ],
  "genealogy_cycles": [
    {
      "id": "ancestral-bootstrap",
      "edges": ["parent-edge", "return-parent-edge"],
      "causal_cycle": "genealogy-causality",
      "evidence_events": ["conception", "return-conception"]
    }
  ],
  "knots": [
    {
      "id": "adam-eve-knot",
      "worlds": ["A", "E"],
      "entanglement_links": ["A-causes-E", "E-causes-A"],
      "cycles": ["mutual-world-cycle", "genealogy-causality"],
      "origin_world": "O",
      "dissolution": {
        "intervention": "origin-intervention",
        "targets": ["A", "E"],
        "termination_events": ["A-dissolves", "E-dissolves"],
        "origin_continues_at": "origin-continuation",
        "causal_links": ["origin-prevents-knot"]
      },
      "evidence_events": ["origin-intervention", "A-dissolves", "E-dissolves"]
    }
  ]
}
```

`dissolution` may be `null`; all other shown knot fields are required. A supplied dissolution requires all its shown fields.

Exact invariants:

> Version correspondence is not body identity, shared memory, fusion, or automatic fate propagation. Version instances must belong to the stated character and world.

> Genealogy edges reference person identities and matching instances. A genealogy cycle is a directed closed parent→child path, including a permitted one-edge self-parent cycle. Every genealogical cycle requires a record and supporting causal cycle. It is not universe ancestry.

> A knot has at least two distinct member worlds and causal entanglement connecting them into one strongly connected component. Its origin world is distinct from every member. Namespace names never stand in for world IDs.

> Dissolution explicitly terminates the named member worlds at the named events. No later event may occupy those worlds in that represented history. The origin world continues; member worlds do not merge into it. No deaths or individual disappearance fates are generated.

Predestination’s person identity may occur in multiple genealogy roles and multiple bodily instances. Timecrimes may attach several IN-3 presentations to one event; witnesses do not multiply the event or the bystander biography.

```text
E269 {path}: character-version correspondence has incompatible character, world, or instance membership.
E270 {path}: bootstrap genealogy lacks a declared closed identity path and supporting causal cycle.
E271 {path}: knot declaration lacks connected multi-world entanglement or a distinct origin world.
E272 {path}: knot dissolution is incomplete or is encoded as a universe merge.
```

Render a separate correspondence/genealogy overlay. Only explicit transfer records carry travellers between world lanes. Entanglement connectors are causal, not routing or layout-precedence edges.

---

## 7. IN-7 — METRICS, CLOCK SHEAR, AND TRAVERSAL TYPES

**Targets:** A1–A3, A6, A9; B18–21; C1–C2.

### Worldline metric and attractors

Add universe `divergence`; add graph `worldline_systems` and `attractor_fields`:

```json
{
  "divergence": {
    "system": "meter-system",
    "value": "1.048596",
    "unit": "percent",
    "evidence_events": ["meter-reading"]
  }
}
```

```json
{
  "worldline_systems": [
    {
      "id": "meter-system",
      "worlds": ["alpha-line", "beta-line", "target-line"],
      "existence": "single-active",
      "activation_sequence": ["alpha-line", "beta-line", "target-line"],
      "evidence_events": ["first-reading", "last-reading"]
    }
  ],
  "attractor_fields": [
    {
      "id": "alpha",
      "system": "meter-system",
      "worldlines": ["alpha-line"],
      "fixed_outcomes": [
        {
          "id": "convergence",
          "claim": "Named outcome recurs within the represented basin.",
          "witnesses": ["outcome-observation"]
        }
      ],
      "evidence_events": ["outcome-observation"]
    }
  ]
}
```

`value` is a signed decimal string without exponent; comparisons use exact decimal arithmetic. `existence`: `single-active`, `coexisting`, or `undeclared`. `activation_sequence` is required only for `single-active`, permits revisits, and asserts activity order—not world birth or destruction.

> A divergence number is a coordinate, not a probability, population count, distance in metres, or branch count. Comparison requires the same metric system. Attractor membership and fixed-outcome claims are authored; no missing death, event, or transfer is generated from membership.

> `single-active` histories render as non-coexisting alternatives, with the active selection labelled. `undeclared` existence prints `WORLDLINE COEXISTENCE UNDECLARED`. Neither silently becomes P1 persistent sibling worlds.

### Locations and clock rates

Add graph `clocks`, `locations`, `clock_rates`:

```json
{
  "clocks": [
    {"id": "earth-clock", "unit": "second"},
    {"id": "miller-clock", "unit": "second"}
  ],
  "locations": [
    {
      "id": "miller",
      "universe": "U",
      "clock": "miller-clock",
      "evidence_events": ["landing"]
    }
  ],
  "clock_rates": [
    {
      "id": "miller-rate",
      "location": "miller",
      "from": "landing",
      "to": "departure",
      "relative_to": "earth-clock",
      "rate": {"numerator": 1, "denominator": 61362},
      "synchronization": {
        "local_event": "landing",
        "reference_event": "earth-reference"
      },
      "evidence_events": ["rate-explanation"]
    }
  ]
}
```

This sample uses seconds and a Julian year: one local hour per seven reference years.

> Rates are positive rational local-clock units per reference-clock unit, valid only over the declared interval. Units must match or use an explicitly registered exact conversion. Synchronization provides the correspondence anchor; a rate alone does not synchronize clock zeros.

> Inversion sign and clock-rate magnitude are separate. Clock shear does not move an instance, change its world, or create another iteration.

### Transfer discriminators

Add optional legacy-compatible field:

```json
{"traversal": "memory"}
```

If present, its domain is exactly `body`, `memory`, `signal`. Missing `traversal` on a v2/v2.1 transfer means **legacy traversal detail unspecified**, not an inferred value. New time-travel encodes must supply it.

Extend ordinary transfer `mechanism` with `time_travel`, `time_leap`, `object_transport`; extend relation with:

```json
{"kind": "same_world"}
```

Body traversal retains ordinary transfer endpoints and embodiment. Same-world body travel requires explicit source/destination instances sharing one body identity. Object transport instead carries `object`, has `traveller:null`, and omits `embodiment`.

Memory transfer projection:

```json
{
  "id": "leap",
  "traversal": "memory",
  "traveller": "okabe-mind",
  "from": {"universe": "line-before", "exit": "leap-out"},
  "to": {"universe": "line-after", "entry": "leap-in"},
  "mechanism": "time_leap",
  "relation": {"kind": "different_universes"},
  "embodiment": {
    "mode": "occupies_host",
    "from_instance": "okabe-before",
    "to_instance": "okabe-after"
  },
  "memory_payload": "leap-memories",
  "pre_leap_body": {
    "retained_by": "okabe-before",
    "fate": "body-after-leap"
  }
}
```

> Memory traversal moves the named information/consciousness continuity, not the source body. `pre_leap_body.retained_by` must equal the source embodiment instance. Its referenced fate must concern that instance in the source context at the departure event or an explicitly later bodily event; `unknown` is legal and visibly unresolved. It must never be omitted. Destination embodiment and host disposition remain explicit A6 facts.

Signal arm of the `transfers` discriminated union:

```json
{
  "id": "tesseract-signal",
  "traversal": "signal",
  "mechanism": "temporal_signal",
  "from": {"universe": "U", "event": "send-watch-signal"},
  "to": {"universe": "U", "event": "receive-watch-signal"},
  "sender": "cooper-person",
  "receiver": "murph-person",
  "payload": "quantum-data",
  "channel": "gravity",
  "causal_link": "watch-message",
  "evidence_events": ["send-watch-signal", "receive-watch-signal"]
}
```

> `transfers` is henceforth a transport-record collection. Its `signal` arm is **not traveller transfer**: it carries no traveller, embodiment, body movement, visit, or thread link. It routes emission→reception ports with a dotted `SIGNAL · NO TRAVEL` connector. A6’s exit/entry event-kind requirements apply only to body/memory/legacy traveller transfers.

> `causal_link` must match the signal events and payload identity. A signal into the past does not itself prove a closed loop. The tesseract’s higher-dimensional geometry is not simulated; its asserted observable action is encoded as a signal.

```text
E273 {path}: divergence coordinate or attractor membership has an incompatible metric system.
E274 {path}: clock-rate interval lacks valid units, positive rate, or synchronization.
E275 {path}: memory traversal must identify the instance retaining the pre-leap body and its explicit fate.
E276 {path}: traversal type conflicts with its payload, embodiment, endpoint, or thread semantics.
E277 {path}: signal must match an explicit causal link and cannot transport or route a traveller.
```

---

## 8. IN-8 — OBJECT, PERSON, BODY, AND BOOTSTRAP IDENTITY

**Targets:** A1, A5–A6; AMEND-1 causal records; B.

Add graph `identities`, `object_occurrences`, `identity_roles`:

```json
{
  "identities": [
    {
      "id": "note",
      "kind": "object",
      "label": "Bootstrap note",
      "character": null,
      "provenance": {"kind": "closed", "cycle": "note-cycle"},
      "evidence_events": ["note-received", "note-sent"]
    },
    {
      "id": "jane-person",
      "kind": "person",
      "label": "One biography",
      "character": "jane",
      "provenance": {"kind": "closed", "cycle": "jane-cycle"},
      "evidence_events": ["jane-birth"]
    },
    {
      "id": "jane-body",
      "kind": "body",
      "label": "Jane's bodily history",
      "character": "jane",
      "provenance": {"kind": "origin", "event": "jane-birth"},
      "evidence_events": ["jane-birth"]
    }
  ],
  "object_occurrences": [
    {
      "id": "note-younger",
      "object": "note",
      "event": "note-received",
      "location": "room",
      "evidence_events": ["note-received"]
    }
  ],
  "identity_roles": [
    {
      "id": "jane-mother-role",
      "identity": "jane-person",
      "instance": "jane-at-conception",
      "role": "mother",
      "event": "conception",
      "evidence_events": ["conception"]
    }
  ]
}
```

`identities.kind`: `person`, `body`, `object`, `information`, `entity`. `character` is required and non-null for person/body, otherwise `null`. Entity identities cover non-traveller mechanism owners and sources.

`provenance` has exactly one of these forms:

```json
{"kind": "origin", "event": "manufacture"}
```

```json
{"kind": "closed", "cycle": "bootstrap-cycle"}
```

```json
{"kind": "unknown", "observed_at": "first-observation"}
```

Add optional identity `components`, an array of object identity IDs, for composites such as Algorithm pieces. Composition is not fusion of worlds or people.

Exact invariants:

> A closed object/information provenance references a `bootstrap` causal cycle whose links all have that identity ID as `subject`. Each occurrence claimed to participate in bootstrap provenance must lie on, or be reachable by explicitly recorded same-subject causal links from, that cycle.

> A closed person provenance references a declared causal cycle supported by IN-6 genealogy records. It may include multiple parent identities; therefore it need not use the single-subject object-bootstrap rule. A body birth may be an origin event within that closed person provenance without inventing an external ancestor.

> Causal chains are traversed backward to an explicit origin, an explicit unknown boundary, or a declared closed chain. Only the third qualifies as bootstrap provenance. A closed label cannot terminate at an unknown boundary.

> Object identity does not establish a loop. The Algorithm may have an explicit future manufacture origin; a future origin alone is not bootstrap provenance. An Artifact may survive tangent collapse without having bootstrap manufacture. Encode only the supported distinction.

```text
E278 {path}: bootstrap object '{object}' provenance must terminate in a declared closed chain, never an unexplained origin.
E279 {path}: identity provenance, occurrence, role, or causal subject does not resolve consistently.
```

Existing string-valued causal subjects remain legal; when used by typed provenance or signal records they must resolve to the corresponding identity ID. E203–E205 remain unchanged for existing causal cycles.

---

## 9. IN-9 — REGRESSION AND SUPERSEDED CHECKS

**Targets:** E2; A10; B; AMEND-5.

### Ben header

The complete v2.1 Ben fixture requires **no body changes and no header changes**:

```json
{
  "schema_version": 2,
  "interpretation_profile": "P1",
  "interpretation_rules": "waif",
  "validation_profile": "evidence_pending",
  "meta": {
    "title": "THE WAIF — Ben's Story",
    "subtitle": "Canon topology fixture; screenplay locators pending",
    "footer": "Universe identity is separate from consciousness and character fate.",
    "axis": "story_order"
  }
}
```

The P1 preset expansion preserves its split identities, route, unknown embodiments, citations, namespace isolation, and mortality checks. New arrays are optional; new traversal detail is not retroactively invented.

**Verification boundary:** the E2 JSON supplied here ends inside a citation and is not parseable. The compatibility result applies to the complete v2.1 fixture, not to that truncated excerpt; no executed validation result is claimed.

### Exact replacements and retirements

| Existing check | v2.2 disposition |
|---|---|
| E112 | Replace as below; same-world time travel is permitted, sibling transfers remain cross-world |
| E113, E134 | Apply to legacy narrative-order routing only; motion-linked routes use bodily order |
| E102, E217 | Terminality follows bodily order within one world/revision/iteration, not screen order |
| E120–E122 | Sibling-reset constraints remain for P1 apparent resets; replace E122 below |
| E210–E219 | Retained; sequence scope becomes the declared ladder or iteration sequence |
| E220 | Rename to memory-reset predicate; external-anchor loops use E267 as well |
| E230–E233 | Retained for state histories and undeclared relationships |
| E240–E250 | Retire profile-name capability guards; replace with E252–E254 and mechanism-specific checks |
| E170 | Replace version-specific text below |
| E201 | Replaced in IN-1 |
| E203–E205 | Retained; causal cycles are not birth ancestry |
| E182 | Still only an explicitly dying negative split tine |
| E183 | Per-thread continuity remains mandatory; multiple body tracks or separate threads are not one branching thread |

```text
E112 {path}: transfer world relation disagrees with its endpoint worlds.
E122 {path}: reset or overwrite lacks the iteration or revision machinery required by the declared parameters.
E220 {path}: memory-reset requires retained memory for the thread traveller.
E170 {path}: actual universe merges are not supported in schema v2.2; transfer, signal, overwrite, reset, collapse, and dissolution are distinct operations.
```

Ordering replacement invariant:

> Display coordinates never determine death terminality or physical travel legality. A motion-backed visit uses its declared bodily order. A traveller transfer or gate joins consecutive route visits through exact ports even when its world-time displacement is negative. Legacy visits without motion records retain v2.1 story-order checks. Causal edges impose no route or layout ordering.

Required regressions retain both Groundhog encodings, Butterfly’s terminal overwrite, Ben, A10, namespace isolation, array permutations, evidence manifests, exit code 2, and all no-inference checks. Add negatives for each E251–E279 condition before accepting the new fixtures.

---

## 10. IN-10 — CONSISTENCY SWEEP

**Targets:** every contradictory v2/v2.1 clause.

| Section | Binding one-line replacement |
|---|---|
| Title; AMEND-1 profile declaration | “v2.2 uses declared parameter sets and registered presets; evidence mode remains independent.” |
| §0.1 | “Automatic trigger splitting is exclusively the named WAIF house rule.” |
| §0.2 | “Sibling cut, revision, iteration reset, fated return, signal, collapse and dissolution are distinct explicitly recorded mechanisms.” |
| §0.3 | “World existence, world activity, history currentness, bodily state and consciousness continuity are separate facts.” |
| §0.4, §0.7 | “Pre-existing-lane and immutable birth-ID rules apply to their declared origin records, never to revisions, iterations or temporal body portions.” |
| A1 document/root fields | “Accept preset strings or the exact parametric object; declare new typed arrays and retain strict unknown-field rejection.” |
| A1 graph/namespace scope | “A namespace isolates references; world multiplicity follows topology records, never graph count.” |
| A2 origins and continuation | “Branch births use split origins; knots, worldlines and primary/tangent relations require their own explicit topology rather than invented branch ancestry.” |
| A3 coordinates and equal ports | “Story/view coordinates control presentation; world clocks and bodily order control physical temporal checks.” |
| A3 event kinds | “Add gate entry/exit ports; signal events use ordinary anchor events and their explicit signal role.” |
| A4 splits | “Binary split machinery is enabled by `siblings`; all authored split contracts remain enforced.” |
| A5 instances and mortality | “Instances are world-local temporal embodiments; optional person/body identities relate them without conflating their scoped fates.” |
| A6 section title | “Transport records: body, memory, signal and legacy-unspecified traversal; only traveller-bearing records can route a thread.” |
| A6 different-world restriction | “Endpoint relation determines same-world versus cross-world transport; continuous inversion is represented by motions and gates.” |
| A6 source/destination continuation | “Movement alone does not terminate worlds; explicit collapse or dissolution records may do so independently.” |
| A6 Groundhog mapping | “Retain both P1 sibling-cut and P3 memory-reset encodings; neither is universal reset physics.” |
| A7 merges | “No merge operation is added; knot dissolution and tangent collapse are explicit termination mechanisms.” |
| A8 segments and beats | “Keep semantic story intervals and context membership; fragment their presentation when displaying non-monotone view order.” |
| A9 visits and links | “Support split, traveller-transfer, revision and gate links; signal and causal edges never substitute for thread continuity.” |
| A9 one consciousness rule | “Each thread remains a single ordered route; coexisting instances and pincer participants require explicit motions, not inferred route branching.” |
| A10 | “The synthetic P1 fixture remains valid without new mechanism records.” |
| A11 arcs/loops/joins | “Migration requires explicit transport, gate, revision, reset, causal or undeclared-observation semantics.” |
| A11 interval/timescale | “Preserve clock endpoints; add rate and synchronization records only when authored.” |
| B7–11 | “Apply lane, origin, existence and ancestry checks to the declared topology, including explicit world termination bounds.” |
| B17–25 | “Use context-local bodily chronology and discriminator-specific endpoint checks; retain exact route continuity.” |
| B26–27 | “Validate semantic segment containment independently of the displayed axis.” |
| B29–30 | “Forbid merges; assert mechanism-specific geometry and persistent ontology/axis disclosure.” |
| C1 world lanes | “A lane represents only its declared world or observation context; revisions, iterations and temporal body portions are not extra worlds.” |
| C1 reset/transfer primitives | “Render distinct transport, gate, reset, overwrite, signal, collapse and dissolution symbols.” |
| C1 right-hand death rule | “Keep screen-right departure only for an explicitly dying negative split tine.” |
| C1 thread rendering | “Follow explicit route ports and bodily continuity, not monotonic screen position.” |
| C2 layout constraints | “Causal, genealogy and knot cycles do not create layout-precedence cycles.” |
| C2 chrome/counters | “Show preset expansion, display axis, scoped state labels and transition ordinals; never infer population counts.” |
| D Patches 2–3 | “Implement parameter validation and all new typed mechanisms with positive and negative fixtures before rendering.” |
| D Patches 4–7 | “Preserve existing fixture conversions; add mechanism-specific rendering without changing their declared interpretations.” |
| D Patch 8 | “Compile only explicitly authored mechanism records; prose, lane geometry and film titles never select physics.” |
| D Patch 9 | “Expose parameter presets, motion/body identity, dual coordinates, ladders, loops, knots, metrics and provenance through the shared validator.” |
| D Patch 10 and documentation conclusion | “Maintain separate interpretation encodes where evidence does not establish one ontology; no universal sibling or overwrite conversion.” |
| E1–E2 | “Ben remains the unchanged P1/WAIF acceptance fixture, subject to its existing evidence-pending status.” |
| AMEND-1 scope/invariant matrix | “Replace flat-profile dispatch with IN-1 predicates and explicit topology/state records.” |
| AMEND-2 | “Generalize ordered states to ladders and loop iterations without weakening supersession, memory or absent-embodiment guards.” |
| AMEND-3 | “Existing mini-encodes retain their preset strings, event identities, coordinates, citations and routes.” |
| AMEND-4 | “Retain legacy chips and state markings; add expanded parameter disclosure and new mechanism primitives.” |
| AMEND-5 | “Replace E240–E250 capability guards while preserving their rejection cases under equivalent parameter predicates.” |
| AMEND-6 | “This sweep supersedes its remaining flat-profile restrictions.” |

No cosmological simulator, entropy solver, attractor-outcome generator, biological paradox resolver, or five-dimensional geometry engine is added. Unsupported claims use a **separate P4 observation encoding**, with existing `observed_transition` and `RELATION UNDECLARED` markings; they cannot be hidden inside `extensions` and rendered as facts.

| Corpus film | Parametric preset | New machinery required | Fixtures still needing encodes before trust |
|---|---|---|---|
| Tenet | `tenet` | Motions, turnstiles, same-body temporal portions, pincers, object provenance | Turnstile round trip; opposed-self encounter; pincer information path; Algorithm manufacture versus bootstrap |
| Memento | `memento` | Dual coordinates and repeated presentations | Full selected story/view permutation; fragmented segment; no physical inversion |
| Looper | `looper` | Revision ladders, wound/memory/existence linkage | Successive scars; memory replacement; terminal self-removal; no inferred fate |
| Donnie Darko | `darko` | Primary/tangent relation, bounded collapse, causal closure, residue transport | Edition-specific lifetime; engine identity and return; separate primary/tangent fates |
| Dark | `dark` | Versions, correspondence, genealogy cycles, entanglement, origin dissolution | Three-world ledger; Unknown’s ancestry cycle; version-specific fates; dissolution without merger |
| Steins;Gate | `steins-gate` | Divergence systems, attractors, active-worldline semantics, memory traversal | Meter readings; attractor witnesses; time leap with source-body fate; target-line activation |
| Predestination | `predestination` | One person biography, multiple bodily portions and genealogy roles | Mother/father/child identity cycle; recruitment bootstrap; bodily mortality order |
| Timecrimes | `timecrimes` | Interleaved bodily occupancy and multi-perspective event presentations | Three Héctor portions; nested causal cycles; one consistent bystander history |
| Edge of Tomorrow | `eot` | External reset owner/source, death trigger, anchors, memory subjects | Ordinary reset; loss of reset capability; separately justified final anchor and post-reset continuation |
| Interstellar | `interstellar` | Clock-rate intervals, synchronization, signal-without-travel | Miller/reference clock accounting; watch signal; no fabricated traveller transfer |
| Prisoner of Azkaban | `azkaban` | Same-world body travel, coexisting selves, fated causal closure | Both returning travellers; rescue self-consistency; no iteration and no reset-memory claim |

===== PART 2: v2.1 PROFILE AMENDMENTS (for reference where not superseded) =====
## AMEND-1 — PROFILE MECHANISM

**Amends:** title block; §0; A1–A9; B.

Replace the canonical-ontology declaration with:

> **Specification revision:** `2.1`; `schema_version: 2` remains the schema-family identifier.  
> **Core ontology:** neutral. Every canonical document declares one interpretation profile. THE WAIF is the house interpretation, not universal physics. `validation_profile` governs evidence completeness only.

### Document fields

Add:

```json
{
  "interpretation_profile": "P4",
  "interpretation_rules": "none"
}
```

Exact field definitions:

- `interpretation_profile`: `"P1"`, `"P2"`, `"P3"`, or `"P4"`.
- Authoring default: `"P4"`. Normalization writes this explicitly; canonical validation never infers a profile from a title, source text, graph shape, or lane count.
- `interpretation_rules`: `"none"` or `"waif"`; optional, default `"none"`. `"waif"` requires `"P1"`.
- A missing canonical `interpretation_profile` fails:
  
  `E200 /interpretation_profile: canonical document must declare interpretation_profile.`

- An unsupported value uses `E012`.
- Invalid house-rule combination fails:
  
  `E201 /interpretation_rules: 'waif' requires interpretation_profile 'P1'.`

**P4 marking rule:**

> P4 must display `P4 · ONTOLOGY UNDECLARED` persistently on canvas and in exported text. Every depicted connection between distinct history contexts must display `RELATION UNDECLARED`. Such contexts are observations, not asserted coexisting worlds. Neither label may be hidden by styling, cropping, collapsing, or legend suppression.

Failure:

`E202 {path}: required interpretation-profile marking is missing or incorrect.`

### Profile scope

| Entity | P1 — branch-multiverse | P2 — single mutable timeline | P3 — closed loop, mind persistence | P4 — ambiguous/undeclared |
|---|---|---|---|---|
| `graphs` | Branch-world graphs | Views of one revisable world | Views of one iterating world | Observation graphs |
| `namespaces` | Reference isolation, never ancestry | Reference isolation, never additional worlds | Reference isolation, never additional worlds | Reference isolation, never an ontology claim |
| `universes` | Persistent world identities, including ancestry prefixes | Exactly one world ID per graph, plus its ordered revision history | Exactly one world ID per graph, plus its ordered iterations | Identified observation contexts; coexistence undeclared |
| Across graphs | Different IDs may identify different worlds | All rendered graphs use the same world ID and identical world/revision declarations | All rendered graphs use the same world ID and identical world/iteration declarations | No world equivalence inferred |
| `layout.lane_order` | World-column order | Exactly `[world_id]`; revisions are not lanes | Exactly `[world_id]`; iterations are not lanes | Observation-column order, explicitly non-ontological |
| `instances` | Embodiments local to one world | Embodiment identifiers local to the one world; presence and fate are revision-local | Embodiment identifiers local to the one world; presence and fate are iteration-local | Embodiments local to an observed context |
| `fates` | Event-local facts about an instance in a world | Event-and-revision-local facts; superseded facts remain historical records only | Event-and-iteration-local facts; reset carries no bodily fate forward | Observed facts only; no propagation across contexts |
| `thread` | Ordered consciousness visits among worlds | Ordered consciousness visits to particular revisions of one world | Ordered visits through iterations by the retaining consciousness | Ordered observed continuity; mechanism and world relationship undeclared |
| Origin | Existing P1 origins | `initial` or `unknown`; revision creation is not world birth | `initial` or `unknown`; iteration start is not world birth | `initial` or `unknown`; no asserted branch ancestry |

> An event graph consists of authored event identities, evidence, coordinates, causal relations, and ordered route endpoints. Profile encoding binds those events to worlds, revisions, or observation contexts and interprets transition edges. Re-encoding must preserve event IDs, evidence, `story_order`, `world_time`, and the represented route; profile-specific bindings and transition records may change. Changing only the profile chip is not a valid conversion. A film may have multiple separately declared encodings of the same event graph.

### Complete profile-conditional invariant replacement

The following replaces every ontology-dependent invariant in the supplied specification. All other structural, reference, evidence, namespace-isolation, no-inference, and geometry checks remain binding.

| Existing clauses/checks | P1 form | P2 form | P3 form | P4 form |
|---|---|---|---|---|
| §0.1; A4; B15: automatic trigger physics | With `waif`, every authored trigger intervention has an automatic split with explicit surviving/dead counterparts. With `none`, no trigger physics is inferred; an authored `cause:"trigger_pull"` split still explicitly asserts the existing two-outcome contract. | Trigger/intervention may cause an authored revision; no automatic split or death. | Intervention may occur within an iteration; reset requires an authored iteration transition, not a split. | Intervention effect remains undeclared; no automatic split, reset, or death. |
| §0.2; A6; B20: reset/overwrite | Apparent reset is an explicit sibling transfer; no overwrite. | Overwrite advances revision order in the same world; old histories cease to be current worlds. | Reset advances iteration order in the same world; declared mind persists. | Only an observed transition; no sibling, overwrite, or loop assertion. |
| §0.3–4,7; A2; B8–11: existence, birth, ancestry | Existing birth identities, ancestry, witnesses and pre-existing-world rules apply. Death/transfer does not terminate a world. | One world persists through revisions. Revision availability replaces branch-birth checks; no `born`/`preexisting` origin, starred ID, or ancestry edge. | One world persists through iterations. Iteration availability replaces branch-birth checks; no branch origins or ancestry. | Witness bounds apply to observed contexts; no established prehistory or ancestry is inferred. |
| A4; B12–14: split structure | Existing split cardinality, tines, continuation and birth agreement apply. | `splits:[]`; no `split` or `outcome` events. | `splits:[]`; no `split` or `outcome` events. | `splits:[]`; no `split` or `outcome` events. |
| A5; B16–17: fate scope/mortality | Existing world-and-instance agreement; death terminal for that instance. | Fate and instance agree with event world; death terminal only within its revision. | Death terminal only within its iteration; bodily reset is not implicit resurrection within that iteration. | Death terminal within a single observed context; no cross-context inference. |
| A6; B18–21: transitions/embodiment | Existing different-world transfers, sibling-reset constraints and embodiment checks. | No `transfers`; revision transitions have same-world, adjacent-revision endpoints. | No `transfers`; iteration transitions have same-world, adjacent-iteration endpoints and retained mind. | Transfers connect observation contexts with `relation.kind:"unknown"` and `mechanism:"observed_transition"` only. |
| A8; B26: segments | Cannot cross an interior split. | Endpoints must share one revision; cannot span a revision boundary. | Endpoints must share one iteration; cannot span a reset boundary. | Endpoints must share one observed context. |
| A9; B22–25: visits/links | Existing visits, `passes`, split/transfer links; unvisited worlds remain declared worlds. | Visits select one revision; `passes:[]`; links use declared revision transitions. Superseded history is not an unvisited persistent world. | Visits select one iteration; `passes:[]`; links use declared reset transitions. | Visits select observed contexts; `passes:[]`; links reference observed transitions. |
| B7; C1–C2: lanes/collapse | Existing universe lanes and explicit birth stubs. | One baseline; no collapsed universe stubs. | One baseline; no collapsed universe stubs. | Observation columns, never labelled universe lanes; collapsing is forbidden. |
| B30; C1: split/reset geometry | Existing explicit tines. Screen-right death geometry applies only to an authored dying negative tine. | Revision splice and superseded-history treatment; no tines/sibling connectors. | Iteration separators and reset connectors; no parallel universe lanes. | Dashed connectors labelled undeclared; no branch/reset glyph asserting ontology. |
| A11; B31; D: migration | Explicit branch identities/outcomes required. | Explicit same-world revision records required. | Explicit iteration/reset and memory records required. | Preserve observation contexts and mark uncertainty; never manufacture a committed profile. |

**Profile-independent retained invariants:**

> Thread order remains authoritative. Narrative order is not world time. Death, consciousness movement, history supersession, and world existence remain distinct facts. No compiler-generated deaths, survival claims, parentage, body counts, memory retention, or citations. Actual world merging remains unsupported under every profile.

Add `"observed_transition"` to A6 `mechanism`, legal only in P4.

### Causal loops and bootstrap evidence

**Amends A1, A3 and B:** add optional graph arrays, defaulting to `[]`:

```json
{
  "causal_links": [
    {
      "id": "c1",
      "from": "later-observation",
      "to": "earlier-intervention",
      "subject": "remembered-message",
      "cite": {
        "source": "film",
        "page": null,
        "scene": null,
        "locator": "Authored causal interpretation",
        "status": "unavailable"
      }
    }
  ],
  "causal_cycles": [
    {
      "id": "loop1",
      "kind": "bootstrap",
      "links": ["c1", "c2"]
    }
  ]
}
```

> `causal_links` reference events in the same namespace; `subject` is a nonempty authored identity for the transmitted information/object. `causal_cycles.kind` is `closed_loop` or `bootstrap`; listed links must form one directed cycle, with at least one link. Bootstrap links must share `subject`. Every directed cycle must be covered by a declared cycle record. Causal edges may run backward in narrative/world time and never become ancestry or layout-order constraints. A reset arrow alone does not establish a causal cycle. No external origin is invented for a bootstrap subject.

Errors:

- `E203 {path}: causal cycle is undeclared.`
- `E204 {path}: causal cycle links do not form the declared directed cycle.`
- `E205 {path}: bootstrap cycle links must share one subject.`

---

## AMEND-2 — P2 SUPERSESSION

**Amends:** A1, A3, A5, A8–A9; adds revision validation to B.

### Minimal revision records

Add optional graph field `revisions`, default `[]`. It is mandatory and nonempty in P2/P3; forbidden nonempty in P1/P4.

```json
{
  "revisions": [
    {
      "id": "r0",
      "universe": "U",
      "order": 0,
      "transition": null
    },
    {
      "id": "r1",
      "universe": "U",
      "order": 1,
      "transition": {
        "kind": "overwrite",
        "from": "journal-intervention",
        "to": "revised-history-entry",
        "traveller": "evan-mind",
        "memory": "retained"
      }
    }
  ]
}
```

Exact rules:

- Revision IDs are unique within the graph’s `revisions` collection.
- `order` is a nonnegative integer; values are exactly `0..n-1`. Array order is irrelevant.
- All records reference the graph’s sole world.
- Order zero has `transition:null`; every later record has exactly one transition from its immediate predecessor.
- `transition.kind`: `"overwrite"` in P2; `"reset"` in P3.
- `transition.memory`: `"retained"`, `"none"`, or `"unknown"` in P2; exactly `"retained"` in P3.
- `transition.traveller` references a declared traveller. P3 transitions name the graph thread’s traveller.
- `from` and `to` reference events in predecessor and destination revisions respectively.
- Normal transition endpoints are `exit` → `entry`, with increasing `story_order`.
- A terminal P2 overwrite with `memory:"none"` may use `cutoff` → `entry`; the cutoff must be the thread’s final exit and the thread must not visit that successor revision.
- Endpoint citations provide transition evidence. Unsupported interpretation details must also be declared in `assumptions`; no production evidence is generated.
- No revision is a universe, descendant, sibling, instance of world duplication, or lane.

### State attachment

Add required `revision` to **every event in P2/P3**:

```json
{
  "id": "revised-history-entry",
  "kind": "entry",
  "universe": "U",
  "revision": "r1",
  "story_order": 21,
  "world_time": null,
  "label": "Revised history",
  "cite": {
    "source": "film",
    "page": null,
    "scene": null,
    "locator": "Journal revision",
    "status": "unavailable"
  }
}
```

Add required `revision` to **every visit in P2/P3**:

```json
{
  "id": "v1",
  "traveller": "evan-mind",
  "universe": "U",
  "revision": "r1",
  "entry": "revised-history-entry",
  "exit": "next-intervention",
  "passes": []
}
```

Add thread link kind `"revision"`:

```json
{
  "from_visit": "v0",
  "to_visit": "v1",
  "kind": "revision",
  "revision": "r1"
}
```

> The link references the destination revision’s transition. Its `from`/`to` events must equal the adjacent visit endpoints; its traveller must match the thread. Following the link requires `memory:"retained"`. A visit cannot straddle revisions. Segments derive revision from their endpoints; beats derive it from their segment; fates derive it from their event. No duplicate revision field is added to those records.

### Supersession and fate semantics

> Under P2, at revision position `k`, revisions `<k` are superseded, `k` is current, and `>k` are not yet applied. The default final view selects the maximum order. Retained historical records do not assert persistent historical worlds. Superseded fates remain cited facts of their revision; they contribute nothing to the current-state fate display or any census. No fate or bodily state carries forward without an explicit record.

> Under P3, lower-order records are completed iterations, not superseded branch worlds. Reset establishes an authored new iteration of world state; it does not automatically copy any fate record. The same traveller ID and `memory:"retained"` express mind persistence. The last iteration may proceed beyond the repeated date without another reset.

Extend A5 `status` with `"nonexistent"`, legal only in P2:

> `nonexistent` means the named embodiment is absent from that revision’s history; it does not mean death, a dead world, or erasure of the document’s character/traveller identity. An instance ID may designate an embodiment present in an earlier revision but absent in a later one. It may not designate both an absent adult embodiment and a fetus that actually lived and died. Death and nonexistence need separate identities where that distinction matters. No thread visit may occupy an embodiment throughout an interval explicitly recorded as nonexistent.

Add optional visit field:

```json
{"instance": "evan-adult"}
```

> `instance` defaults to `null`, meaning unknown embodiment, not proof of existence. A non-null instance must belong to the visit’s world. An explicit nonexistent fate at a visited event rejects that occupancy. Unknown embodiment may not be used to assert mind survival after an explicitly terminal `memory:"none"` transition.

Exact errors:

- `E210 {path}: revisions must have unique contiguous order values starting at 0.`
- `E211 {path}: revision transition must connect the immediately preceding revision to this revision.`
- `E212 {path}: event revision does not belong to event universe.`
- `E213 {path}: visit endpoints must belong to visit revision '{revision}'.`
- `E214 {path}: revision link does not match adjacent visit endpoints and traveller.`
- `E215 {path}: thread revision link requires retained memory.`
- `E216 {path}: segment endpoints must belong to one revision.`
- `E217 {path}: instance '{instance}' is alive after its recorded death in revision '{revision}'.`
- `E218 {path}: thread occupies nonexistent instance '{instance}'.`
- `E219 {path}: terminal overwrite must end the thread at its source cutoff.`
- `E220 {path}: P3 reset requires retained memory for the thread traveller.`

---

## AMEND-3 — PROOF MINI-ENCODES

**Amends:** A10 and D Patch 10; adds interpretation fixtures.

These are **field projections**, not standalone documents. Merge each into its fixture’s normal A1 envelope; preserve all omitted required arrays. Common envelope: `schema_version:2`, `validation_profile:"evidence_pending"`, `interpretation_rules:"none"`, `meta.axis:"story_order"`, source `film` containing the authored film/edition interpretation ledger, declared namespace `F`. Declare characters `phil`, `rita`, `evan` and travellers `phil-mind`, `evan-mind` as applicable. Unshown graph arrays are empty.

Calendar values below are numeric day-of-month on the declared illustrative clock; they are not elapsed-time layout distances. The Groundhog fixtures depict selected repetitions, not an invented exhaustive iteration count.

### (a) Groundhog Day — P3

```json
{
  "interpretation_profile": "P3",
  "graphs": [{
    "namespace": "F",
    "universes": [{"id":"U","label":"Punxsutawney","origin":{"kind":"initial"}}],
    "instances": [
      {"id":"phil-body","character":"phil","universe":"U","native_to_universe":true,"provenance":"native"},
      {"id":"rita-body","character":"rita","universe":"U","native_to_universe":true,"provenance":"native"}
    ],
    "revisions": [
      {"id":"r0","universe":"U","order":0,"transition":null},
      {"id":"r1","universe":"U","order":1,"transition":{"kind":"reset","from":"x0","to":"s1","traveller":"phil-mind","memory":"retained"}},
      {"id":"r2","universe":"U","order":2,"transition":{"kind":"reset","from":"x1","to":"s2","traveller":"phil-mind","memory":"retained"}}
    ],
    "events": [
      {"id":"s0","kind":"start","universe":"U","revision":"r0","story_order":0,"world_time":{"clock":"local-calendar","value":2,"unit":"February-day"},"label":"February 2; selected iteration","cite":{"source":"film","page":null,"scene":null,"locator":"Repeated February 2","status":"unavailable"}},
      {"id":"x0","kind":"exit","universe":"U","revision":"r0","story_order":1,"world_time":null,"label":"Iteration ends","cite":{"source":"film","page":null,"scene":null,"locator":"Overnight reset","status":"unavailable"}},
      {"id":"s1","kind":"entry","universe":"U","revision":"r1","story_order":2,"world_time":{"clock":"local-calendar","value":2,"unit":"February-day"},"label":"February 2 again; Phil remembers","cite":{"source":"film","page":null,"scene":null,"locator":"Remembered repetition","status":"unavailable"}},
      {"id":"x1","kind":"exit","universe":"U","revision":"r1","story_order":3,"world_time":null,"label":"Another reset","cite":{"source":"film","page":null,"scene":null,"locator":"Repeated awakening","status":"unavailable"}},
      {"id":"s2","kind":"entry","universe":"U","revision":"r2","story_order":4,"world_time":{"clock":"local-calendar","value":2,"unit":"February-day"},"label":"Final represented February 2","cite":{"source":"film","page":null,"scene":null,"locator":"Final repeated day","status":"unavailable"}},
      {"id":"end","kind":"cutoff","universe":"U","revision":"r2","story_order":5,"world_time":{"clock":"local-calendar","value":3,"unit":"February-day"},"label":"February 3; life continues","cite":{"source":"film","page":null,"scene":null,"locator":"Ending awakening","status":"unavailable"}}
    ],
    "fates": [
      {"id":"rita0","universe":"U","instance":"rita-body","event":"s0","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita in represented day","status":"unavailable"}},
      {"id":"rita1","universe":"U","instance":"rita-body","event":"s1","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita restored in repeated day","status":"unavailable"}},
      {"id":"rita2","universe":"U","instance":"rita-body","event":"s2","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita in final repeated day","status":"unavailable"}}
    ],
    "thread": {"traveller":"phil-mind","visits":[
      {"id":"v0","traveller":"phil-mind","universe":"U","revision":"r0","instance":"phil-body","entry":"s0","exit":"x0","passes":[]},
      {"id":"v1","traveller":"phil-mind","universe":"U","revision":"r1","instance":"phil-body","entry":"s1","exit":"x1","passes":[]},
      {"id":"v2","traveller":"phil-mind","universe":"U","revision":"r2","instance":"phil-body","entry":"s2","exit":"end","passes":[]}
    ],"links":[{"from_visit":"v0","to_visit":"v1","kind":"revision","revision":"r1"},{"from_visit":"v1","to_visit":"v2","kind":"revision","revision":"r2"}]},
    "layout":{"lane_order":["U"],"collapsed_universes":[]},
    "assumptions":["P3 interpretation; selected repetitions only. Rita represents explicitly recorded townsfolk state; no population fate census. No townsfolk fate or memory is carried across reset."]
  }]
}
```

### (b) Groundhog Day — P1

Retain event IDs, kinds, coordinates, labels and citations from (a). Remove every event `revision`; bind `s0,x0` to `*d0`, `s1,x1` to `*d1`, and `s2,end` to `*d2`. Replace the remaining divergent fields with:

```json
{
  "interpretation_profile": "P1",
  "graphs": [{
    "namespace": "F",
    "universes": [
      {"id":"*d0","label":"Selected February 2 world","origin":{"kind":"preexisting","ancestry":"off_chart"}},
      {"id":"*d1","label":"Next represented sibling","origin":{"kind":"preexisting","ancestry":"off_chart"}},
      {"id":"*d2","label":"Final represented sibling","origin":{"kind":"preexisting","ancestry":"off_chart"}}
    ],
    "revisions": [],
    "instances": [
      {"id":"rita0-body","character":"rita","universe":"*d0","native_to_universe":true,"provenance":"native"},
      {"id":"rita1-body","character":"rita","universe":"*d1","native_to_universe":true,"provenance":"native"},
      {"id":"rita2-body","character":"rita","universe":"*d2","native_to_universe":true,"provenance":"native"}
    ],
    "transfers": [
      {"id":"t1","traveller":"phil-mind","from":{"universe":"*d0","exit":"x0"},"to":{"universe":"*d1","entry":"s1"},"mechanism":"apparent_reset","relation":{"kind":"siblings_off_chart"},"embodiment":{"mode":"unknown","from_instance":null,"to_instance":null}},
      {"id":"t2","traveller":"phil-mind","from":{"universe":"*d1","exit":"x1"},"to":{"universe":"*d2","entry":"s2"},"mechanism":"apparent_reset","relation":{"kind":"siblings_off_chart"},"embodiment":{"mode":"unknown","from_instance":null,"to_instance":null}}
    ],
    "fates": [
      {"id":"rita0","universe":"*d0","instance":"rita0-body","event":"s0","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita in represented day","status":"unavailable"}},
      {"id":"rita1","universe":"*d1","instance":"rita1-body","event":"s1","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita restored in repeated day","status":"unavailable"}},
      {"id":"rita2","universe":"*d2","instance":"rita2-body","event":"s2","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Rita in final repeated day","status":"unavailable"}}
    ],
    "thread": {"traveller":"phil-mind","visits":[
      {"id":"v0","traveller":"phil-mind","universe":"*d0","entry":"s0","exit":"x0","passes":[]},
      {"id":"v1","traveller":"phil-mind","universe":"*d1","entry":"s1","exit":"x1","passes":[]},
      {"id":"v2","traveller":"phil-mind","universe":"*d2","entry":"s2","exit":"end","passes":[]}
    ],"links":[
      {"from_visit":"v0","to_visit":"v1","kind":"transfer","transfer":"t1"},
      {"from_visit":"v1","to_visit":"v2","kind":"transfer","transfer":"t2"}
    ]},
    "layout":{"lane_order":["*d0","*d1","*d2"],"collapsed_universes":[]},
    "assumptions":["P1 alternate interpretation, not a claim that the film establishes multiverse physics. Sibling ancestry is authored off-chart; its parent is not invented."]
  }]
}
```

- P3 satisfies same-world adjacent-iteration transition rules; P1 satisfies different-world sibling-transfer rules.
- P3 reuses revision-scoped body identities; P1 uses independent per-world counterparts. Neither propagates Rita’s fate or invents later survival.
- P3 draws one baseline with iteration separators and `RESET / MEMORY RETAINED`; P1 draws persistent sibling lanes and `APPARENT RESET / SIBLING CUT`.
- The event identities, chronology, repeated dates and ordered consciousness route are unchanged.

### (c) The Butterfly Effect — P2

The protagonist is **Evan Treborn**; “Eikon” is treated as the request’s reference to Evan, not a second character. This fixture explicitly selects the **director’s-cut ending**. Its final prenatal intervention uses a home movie, not a journal. `evan-adult` being nonexistent does not deny that a fetus existed and died.

```json
{
  "interpretation_profile": "P2",
  "graphs": [{
    "namespace": "F",
    "universes": [{"id":"U","label":"One revised world","origin":{"kind":"initial"}}],
    "instances": [{"id":"evan-adult","character":"evan","universe":"U","native_to_universe":true,"provenance":"native"}],
    "revisions": [
      {"id":"r0","universe":"U","order":0,"transition":null},
      {"id":"r1","universe":"U","order":1,"transition":{"kind":"overwrite","from":"journal1","to":"childhood1","traveller":"evan-mind","memory":"retained"}},
      {"id":"r2","universe":"U","order":2,"transition":{"kind":"overwrite","from":"journal2","to":"childhood2","traveller":"evan-mind","memory":"retained"}},
      {"id":"r3","universe":"U","order":3,"transition":{"kind":"overwrite","from":"prenatal","to":"without-adult-evan","traveller":"evan-mind","memory":"none"}}
    ],
    "events": [
      {"id":"start","kind":"start","universe":"U","revision":"r0","story_order":0,"world_time":null,"label":"Initial represented history","cite":{"source":"film","page":null,"scene":null,"locator":"Director's cut; opening history","status":"unavailable"}},
      {"id":"journal1","kind":"exit","universe":"U","revision":"r0","story_order":1,"world_time":null,"label":"Evan reads a journal","cite":{"source":"film","page":null,"scene":null,"locator":"First selected journal intervention","status":"unavailable"}},
      {"id":"childhood1","kind":"entry","universe":"U","revision":"r1","story_order":2,"world_time":null,"label":"Evan's childhood intervention point","cite":{"source":"film","page":null,"scene":null,"locator":"Selected childhood revision","status":"unavailable"}},
      {"id":"journal2","kind":"exit","universe":"U","revision":"r1","story_order":3,"world_time":null,"label":"Evan reads again","cite":{"source":"film","page":null,"scene":null,"locator":"Next selected journal intervention","status":"unavailable"}},
      {"id":"childhood2","kind":"entry","universe":"U","revision":"r2","story_order":4,"world_time":null,"label":"Another childhood intervention point","cite":{"source":"film","page":null,"scene":null,"locator":"Further selected revision","status":"unavailable"}},
      {"id":"prenatal","kind":"cutoff","universe":"U","revision":"r2","story_order":5,"world_time":null,"label":"Home-movie-enabled prenatal intervention; thread ends","cite":{"source":"film","page":null,"scene":null,"locator":"Director's-cut prenatal ending","status":"unavailable"}},
      {"id":"without-adult-evan","kind":"entry","universe":"U","revision":"r3","story_order":6,"world_time":null,"label":"Resulting history: adult Evan never exists","cite":{"source":"film","page":null,"scene":null,"locator":"Director's-cut resulting history","status":"unavailable"}}
    ],
    "fates": [
      {"id":"adult0","universe":"U","instance":"evan-adult","event":"journal1","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Evan before revision","status":"unavailable"}},
      {"id":"adult1","universe":"U","instance":"evan-adult","event":"journal2","status":"alive","cite":{"source":"film","page":null,"scene":null,"locator":"Evan before further revision","status":"unavailable"}},
      {"id":"adult-absent","universe":"U","instance":"evan-adult","event":"without-adult-evan","status":"nonexistent","cite":{"source":"film","page":null,"scene":null,"locator":"Director's cut: no adult Evan in resulting history","status":"unavailable"}}
    ],
    "thread": {"traveller":"evan-mind","visits":[
      {"id":"v0","traveller":"evan-mind","universe":"U","revision":"r0","entry":"start","exit":"journal1","passes":[]},
      {"id":"v1","traveller":"evan-mind","universe":"U","revision":"r1","entry":"childhood1","exit":"journal2","passes":[]},
      {"id":"v2","traveller":"evan-mind","universe":"U","revision":"r2","entry":"childhood2","exit":"prenatal","passes":[]}
    ],"links":[{"from_visit":"v0","to_visit":"v1","kind":"revision","revision":"r1"},{"from_visit":"v1","to_visit":"v2","kind":"revision","revision":"r2"}]},
    "layout":{"lane_order":["U"],"collapsed_universes":[]},
    "assumptions":["Director's-cut P2 interpretation; selected interventions, not a complete scene ledger. r0-r2 are superseded histories, not surviving worlds. No visit or surviving consciousness is asserted in r3. Adult and prenatal embodiment are not conflated."]
  }]
}
```

---

## AMEND-4 — RENDER MAPPING

**Amends:** C1–C2; B30.

Exact persistent profile chips:

| Profile | Canvas text |
|---|---|
| P1, `interpretation_rules:"none"` | `P1 · BRANCH MULTIVERSE` |
| P1, `interpretation_rules:"waif"` | `P1 · BRANCH MULTIVERSE · THE WAIF HOUSE RULES` |
| P2 | `P2 · SINGLE MUTABLE TIMELINE` |
| P3 | `P3 · CLOSED LOOP · MIND PERSISTS` |
| P4 | `P4 · ONTOLOGY UNDECLARED` |

Required rendering invariants:

> **P2:** Draw one world baseline. Stack revision sections serially in revision order, never as parallel world lanes. Label each section `{world} / {revision} · CURRENT` or `{world} / {revision} · SUPERSEDED — NOT A COEXISTING WORLD`. Superseded backgrounds and state badges use grey/dim styling; strike the word `CURRENT` only when showing its replacement. Never strike or obscure authored prose or citations. Historical thread portions remain visible but are marked `HISTORICAL ROUTE`, not surviving consciousness. Revision connectors read `HISTORY OVERWRITE`.

> **P3:** Draw one world baseline with serial iteration sections labelled `{world} / {revision} · ITERATION {order}`. Reset connectors read `RESET / MEMORY RETAINED`; older sections read `COMPLETED ITERATION`. Calendar dates may repeat; narrative position still increases. Continuing beyond the loop’s date stays in the final iteration. No sibling lanes, branch tines, or supersession strike convention.

> **P4:** Draw observation-context columns with headers `OBSERVED CONTEXT {id} · WORLD IDENTITY UNDECLARED`. Connections are dashed and labelled `RELATION UNDECLARED`. No stars, already-running claims, split tines, or reset/overwrite badges.

> **Fates:** P2/P3 badges include revision ID. `nonexistent` uses `∅ · NONEXISTENT IN THIS REVISION`, never an `X` death cap. Superseded badges are excluded from current-state summaries. No profile enables survivor arithmetic.

> **Build:** Normalize and validate the profile before deriving placements. Every placement and connector retains its exact event/world/revision IDs. Layout reads those records, never stale loop variables or nearby lanes. Profile-specific geometry assertions run after routing.

Additional errors:

- `E230 {path}: revision or iteration is rendered as a coexisting universe lane.`
- `E231 {path}: superseded history is missing its non-coexistence marking.`
- `E232 {path}: iteration reset is missing its retained-memory marking.`
- `E233 {path}: undeclared ontology is rendered with an asserted world relationship.`

Replace `E170` with:

`E170 {path}: actual universe merges are not supported in schema v2.1; consciousness movement, overwrite, and reset are distinct operations.`

---

## AMEND-5 — REGRESSION GUARDS

**Amends:** B7–30; E2 header.

Add these exact fail-fast semantic checks:

| Rejected condition | Exact error |
|---|---|
| P2 has anything other than one universe per graph | `E240 {path}: P2 requires exactly one world; revisions are not universes.` |
| P3 has anything other than one universe per graph | `E241 {path}: P3 requires exactly one loop world; iterations are not universes.` |
| P2/P3 layout differs from `[sole_world_id]`, or has collapsed universes | `E242 {path}: {profile} forbids sibling lanes and collapsed universe stubs.` |
| P2/P3 uses `born`/`preexisting`, starred IDs, splits, split/outcome events, transfers, split passes, or split/transfer thread links | `E243 {path}: {profile} forbids P1 branching or cross-universe routing machinery.` |
| P1 contains nonempty revisions, event/visit `revision`, revision links, or `nonexistent` | `E244 {path}: P1 forbids same-world revision machinery and supersession fates.` |
| P2/P3 has missing/empty revisions | `E245 {path}: {profile} requires a nonempty ordered revision history.` |
| P2/P3 event or visit omits revision | `E246 {path}: {profile} requires an explicit revision reference.` |
| P2 uses reset, or P3 uses overwrite | `E247 {path}: transition kind '{kind}' is incompatible with {profile}.` |
| P4 asserts ancestry, siblings, split/reset/overwrite semantics, or uses revision machinery | `E248 {path}: P4 must leave world relationships undeclared.` |
| P2/P3 graphs disagree on world identity or revision declarations | `E249 {path}: {profile} graphs must share one world identity and identical revision declarations.` |
| Non-P1 transfer is not a legal P4 observed transition | `E250 {path}: transfers are supported only by P1 or undeclared P4 observation continuity.` |

Replace B20 `E122` with:

`E122 {path}: P1 does not support same-world reset or overwrite; select P2 or P3 and encode revisions.`

Additional binding regression requirements:

> Test both Groundhog encodings against their declared profiles. Changing only P1→P2 must fail with `E240`, `E242`, or `E243`; changing only P3→P1 must fail with `E244`. Retaining one lane while hiding extra P2 universes must still fail `E240`. Renaming branch lanes to “revisions” must not bypass structural checks. Shuffling universe, revision, event, or transfer arrays must not change ancestry, revision order, thread route, citations, or fate scope. Negative tests require exit code 2 and expected diagnostics, never a crash.

> Retain all v2 reference, endpoint, split-outcome, unknown-origin witness, explicit-fate, citation-manifest, namespace, and connected-thread tests. Add dead→alive within one revision as a rejection and dead→explicitly alive after a P3 reset as an acceptance. No test may rely on inferred embodiment, inferred survival, inferred ancestry, or inferred memory.

**Amended Ben’s Story header; all remaining E2 data stays unchanged:**

```json
{
  "schema_version": 2,
  "interpretation_profile": "P1",
  "interpretation_rules": "waif",
  "validation_profile": "evidence_pending",
  "meta": {
    "title": "THE WAIF — Ben's Story",
    "subtitle": "Canon topology fixture; screenplay locators pending",
    "footer": "Universe identity is separate from consciousness and character fate.",
    "axis": "story_order"
  }
}
```

A10’s existing synthetic fixture receives `"interpretation_profile":"P1"`; its explicitly authored trigger split already satisfies P1 without enabling house-wide trigger physics.

---

## AMEND-6 — CONSISTENCY SWEEP

**Amends:** every supplied section containing hard-coded P1 framing.

| Section | One-line replacement |
|---|---|
| Title/status block | “v2.1 is ontology-neutral; THE WAIF is the declared P1 house interpretation.” |
| §0.1 | “Automatic trigger splitting and paired survival/death are house rules, not core event physics.” |
| §0.2 | “Reset semantics are selected by profile: sibling cut, overwrite, retained-mind iteration, or undeclared transition.” |
| §0.3 | “World existence, embodiment fate, consciousness continuity and history-currentness are separate facts.” |
| §0.4 | “P1 pre-existing worlds backpropagate to chart top; revision/iteration starts do not imply world births.” |
| §0.7 | “Immutable split-birth identity applies to P1 born worlds only.” |
| §0 evidence-limitation conclusion | “Evidence completeness is independent of the document’s explicitly selected ontology.” |
| A1 document/root/graph fields | “Declare interpretation separately from evidence mode; normalize new optional arrays to empty and apply profile-specific graph scope.” |
| A2 universes/origins/continuation | “Origins and branch continuation describe P1 worlds; P2/P3 use one world with ordered states, and P4 uses witnessed observation contexts.” |
| A3 events/coordinates | “Events retain narrative/world-time coordinates; P2/P3 additionally require revision membership, and split ports exist only in P1.” |
| A4 splits/trigger physics/source disposition | “This section defines authored P1 splits; it neither classifies all interventions nor requires other profiles to branch.” |
| A5 instances/fates/mortality | “Fates are world-local in P1, revision-local in P2, iteration-local in P3, and observation-local in P4.” |
| A6 transfers/reset/Groundhog mapping | “P1 transfers cross worlds; P2 overwrites and P3 resets use revisions; P4 records undeclared observed transitions.” |
| A7 actual merges | “Actual merging remains unsupported across profiles; THE WAIF ‘joins’ mean P1 transfers only.” |
| A8 segments/beats | “Segments stay within one world-state context and cannot cross a split, revision, or iteration boundary.” |
| A9 thread/links/unvisited worlds | “Visits and explicit links remain authoritative; their context is a world, revision, iteration, or undeclared observation according to profile.” |
| A10 production example | “Declare P1 on this synthetic mechanism fixture; it tests P1 machinery, not universal film ontology.” |
| A11 lanes/stubs/joins/arcs migration rows | “Interpret legacy geometry only after profile selection and explicit semantic annotation.” |
| A11 same-lane loop/reset row | “Require P2 revision, P3 iteration, P1 sibling-transfer, or P4 undeclared-transition annotation; never force a sibling interpretation.” |
| B7–21, B23–26, B30 | “Apply the profile-conditional invariant matrix and revision guards; retain all unaffected checks.” |
| B29 actual merges | “Use the v2.1 merge diagnostic; overwrite and reset are not merges.” |
| B31 migration | “Missing ontology/state annotations fail migration rather than being inferred from lane shape.” |
| C1 universe/origin/split/transfer/reset/fate primitives | “Select world, revision, iteration, or observation primitives from the declared profile.” |
| C1 right-hand death orientation | “Screen-right death tines apply only to explicitly authored P1 dying negative outcomes.” |
| C1 thread rendering | “Traverse visits and split, transfer, or revision links without inferring a route from lanes.” |
| C2 baselines/arcs/version counters/chrome | “Build profile-specific state baselines and transitions; display profile plus transition ordinals, never world/population counts.” |
| C2 layout staging | “Causal cycles do not create layout precedence; only placement constraints participate in layout-cycle detection.” |
| D Patch 2 | “Implement interpretation profiles separately from evidence profiles, including revision and causal records.” |
| D Patch 3 | “Add cross-profile rejection tests, revision-state checks and explicit causal-cycle tests before rendering.” |
| D Patch 4 | “Convert the existing split demo as P1; Ben is the house-profile acceptance test, not the core ontology test.” |
| D Patch 5 | “Keep P1 origin/split rendering isolated from P2/P3 serial-state and P4 observation rendering.” |
| D Patch 6 | “Route all declared link kinds; convert BTTF2 under explicit P2 revision semantics rather than compulsory universe reallocation.” |
| D Patch 7 | “Scope instances and fates by profile while retaining all cited segment/beat and no-census protections.” |
| D Patch 8 | “`pulls:` implies automatic split only with P1 house rules; otherwise require authored profile-appropriate intervention semantics.” |
| D Patch 9 | “Expose profile selection, revision/iteration membership, memory continuity and profile-scoped fates through the shared validator.” |
| D Patch 10, Groundhog | “Maintain both P3 loop and P1 sibling-cut encodings of the same selected event graph.” |
| D Patch 10, Butterfly | “Use P2 superseded histories with an explicitly selected ending; do not fabricate a surviving final traveller.” |
| D Patch 10, Primer | “Declare P1 as the fixture interpretation, preserving unknown mechanisms and ancestry without inferred copy counts.” |
| D Patch 10, documentation conclusion | “Supersede universal no-rewind framing; same-world revision/reset is valid under P2/P3, not under P1 house rules.” |
| E1 | “These canon assertions and structural allocations apply to the explicitly declared THE WAIF P1 house fixture.” |
| E2 | “Add the P1/waif header; preserve the supplied fixture body and citations unchanged.” |

| Fixture film | Profile(s) used | New fields required | Invariants that changed form |
|---|---|---|---|
| THE WAIF / Ben’s Story | P1 + `waif` | `interpretation_profile`, `interpretation_rules` | Automatic-trigger law becomes house-scoped; existing branch fixture semantics retained |
| Groundhog Day | P3 and alternate P1 | Profile; P3 `revisions`, event/visit `revision`, revision links | World cardinality, reset endpoints, memory, fate terminality, lanes |
| The Butterfly Effect — director’s cut | P2 | Profile, revisions, revision membership/links, terminal `memory:"none"`, `status:"nonexistent"` | Supersession, revision-local mortality, terminal thread, absent embodiment |
| Back to the Future Part II | P2 | Profile, revisions, revision membership/links | One-world identity, overwritten history, fate scope, no sibling lanes |
| Primer | P1; P4 for a separately undeclared reading | Profile; P4 `mechanism:"observed_transition"` where applicable | Branch assertions versus undeclared relationships; no inferred ancestry or copy census |

===== PART 4: v2.3 ADVERSARIAL REPAIRS R1-R11 (supersedes all) =====
# PART 3 — Smallest final revision set

These are proposed amendments, **not retroactive claims that the preceding JSON already uses them**.

## R1. Freeze one executable schema and capability table

**Refs:** A1, B2, IN-1, IN-7, IN-9.

Publish one flattened schema; retire contradictory source paragraphs from normative use. Keep `schema_version:2`, but add:

```json
{"specification_revision":"2.3"}
```

New documents require it; legacy documents are validated against an explicitly selected compatibility revision. Do not infer revision from omitted traversal fields.

Exact rule:

> Every object type has one enumerated field set. `evidence_events` is required on top-level new semantic records except clocks; nested records inherit their containing record’s evidence unless they supply their own. The schema explicitly lists those optional nested evidence fields. No prose-wide wildcard adds fields to otherwise closed object types.

```text
E280 {path}: specification revision or canonical object definition is ambiguous.
E281 {path}: record uses a mechanism outside the declared capability table.
```

The capability table must explicitly authorize:

- Body/memory/signal transport independently of world branching.
- Reset/overwrite only with their state machinery.
- Observed transitions only under undeclared ontology.
- Turnstiles only where both motion signs are authorized.
- No `gated-inversion` traversal enum.

This closes the E240–E250 retirement hole without reinstating preset-name dispatch.

## R2. Define body portions, event positions, and boundary equivalence

**Refs:** A5, B17, IN-2, IN-9.

Add graph records:

```json
{
  "body_positions":[
    {"id":"np-death","body":"nb","instance":"n-final","event":"n-death","proper_order":3,"evidence_events":["n-death"]}
  ]
}
```

Exact invariants:

> Motion interiors use open intervals. Consecutive portions may share an endpoint only through a declared gate or transport boundary. That shared boundary denotes one bodily position, not two coexisting bodies.

> Every fate on a body-linked instance requires a matching body position. Within one state context, a dead body position forbids an alive position later in the same body biography, regardless of instance ID.

> Visit traveller, instance, motion, context, and motion endpoints must agree exactly. A body-linked visit cannot use omission of `motion` to evade bodily ordering.

```text
E282 {path}: bodily event position is missing or conflicts with its motion.
E283 {path}: body '{body}' is alive after its terminal bodily position in this state.
E284 {path}: visit, motion, traveller, instance, or boundary ports disagree.
```

**Tenet repair:** `gnr/gnf` may share proper-order boundaries legally; `n-final` cannot be “resurrected” by renaming its next instance.

## R3. Make pincer coordination actually connect participants

**Refs:** IN-2/E258.

Replace the pincer invariant:

> Motion world-time intervals must overlap. The declared coordination subgraph must contain an information path connecting participants of opposite signs; merely referencing a briefing event or an unrelated causal edge is insufficient. Endpoint participation is explicit.

Add:

```json
{
  "participants":[
    {"motion":"mpr","coordination_events":["brief","red0"]},
    {"motion":"mnb","coordination_events":["blue-report"]}
  ]
}
```

```text
E258 {path}: temporal pincer requires overlapping opposed motions connected by participant-bound coordination paths.
```

`stalsk-pincer` as emitted must fail until a blue-side information witness is supplied. Do not invent that witness from the word “pincer.”

## R4. Separate world-state change from each traveller’s route

**Refs:** AMEND-2, A9, E211/E214/E215/E219.

Keep revision transition endpoints as the **state-change evidence**, but stop requiring every affected traveller to use those ports.

Add graph `state_passages`:

```json
{
  "state_passages":[
    {
      "id":"marty-r0-r1",
      "traveller":"mm",
      "from":{"revision":"r0","event":"m-leave"},
      "to":{"revision":"r1","event":"alt85"},
      "memory":"retained",
      "transport":null,
      "evidence_events":["m-leave","alt85"]
    }
  ]
}
```

Add thread link:

```json
{"from_visit":"mv0","to_visit":"mv1","kind":"state_passage","state_passage":"marty-r0-r1"}
```

Exact invariants:

> A passage references an existing authorized revision/iteration sequence and exact route endpoints. It does not create the destination state or identify its intervention agent. `transport:null` asserts no represented physical transport mechanism; it is not permission to draw one.

> Retained memory applies only to the named traveller. A state passage cannot carry an instance marked nonexistent at its destination.

```text
E285 {path}: state passage lacks matching state membership, traveller, memory, or route endpoints.
```

**BTTF repair:** Biff remains the intervention traveller; Marty gets his own passage. Old Biff’s physical return retains a separate body transport. No invented causal role or shared port.

## R5. Add honest route gaps and optional additional threads

**Refs:** A1/A9, IN-9/E183.

Preserve legacy `thread`. Add optional `additional_threads:[]`, whose members use the identical thread schema and have an `id`. Every thread is independently validated.

Add:

```json
{
  "journey_gaps":[
    {
      "id":"unexpanded-origin-journey",
      "traveller":"jm",
      "from":"leave-E",
      "to":"origin-arrival",
      "mechanism":"unexpanded",
      "evidence_events":["leave-E","origin-arrival"]
    }
  ]
}
```

Thread link:

```json
{"from_visit":"jvE","to_visit":"jvO","kind":"journey_gap","journey_gap":"unexpanded-origin-journey"}
```

Exact invariant:

> A gap asserts observed continuity only. It cannot satisfy a transport, gate, physical-trajectory, causal-loop, or body-displacement proof. It renders `INTERVENING JOURNEY NOT ENCODED`, never a direct-travel arrow.

```text
E286 {path}: unexpanded journey is rendered or validated as a specified transport.
```

**Dark/SG repair:** replace compressed `EO`/`rescue` mechanisms with gaps until their actual itineraries are expanded. Other travellers can receive authoritative routes without duplicating world declarations across graphs.

## R6. Repair the transport union instead of using host language for bodies

**Refs:** A6, IN-7/E276.

For body-bearing travellers, replace `embodiment` with:

```json
{
  "body_transport":{
    "body":"bb",
    "from_instance":"b-past",
    "to_instance":"b-return"
  }
}
```

For objects, define a complete arm:

```json
{
  "id":"letter-delivery",
  "traversal":"object",
  "mechanism":"ordinary_transport",
  "object":"letter",
  "from":{"universe":"U","event":"note-written"},
  "to":{"universe":"U","event":"note-delivered"},
  "evidence_events":["note-written","note-delivered"]
}
```

This deliberately extends the traversal enum to `body|memory|signal|object`. It does **not** claim the current schema already allows `"object"`.

For memory traversal add:

```json
{"destination_memory":{"host":"oA2","effect":"replace","prior_state":"unknown"}}
```

Exact invariants:

> Body transport preserves declared body identity and does not occupy or displace a separate host. Object transport has no traveller or thread link. Ordinary transport does not receive a temporal-jump glyph. Memory transport states its destination memory effect independently of bodily fate.

```text
E276 {path}: transport arm conflicts with its payload, identity continuity, endpoint roles, or route semantics.
E287 {path}: body transport is encoded as host occupation, or ordinary custody as temporal displacement.
```

The small extra object arm is preferable to permanently calling an engine, letter, or Algorithm a `body`.

## R7. Bind history activity and sampled state identity to occurrences

**Refs:** AMEND-2, IN-4, IN-7, E210/E273.

Add state-selection metadata:

```json
{
  "representation":{
    "coverage":"selected",
    "omitted_predecessors":"unknown"
  }
}
```

Allowed coverage: `consecutive|selected`. `omitted_predecessors` is a nonnegative integer or `"unknown"`; consecutive requires `0`.

For worldline systems replace naked activity sequencing in new documents with:

```json
{
  "activations":[
    {"id":"act-A","world":"A","order":0,"evidence_events":["a-start"]},
    {"id":"act-G","world":"G","order":1,"evidence_events":["target-meter"]}
  ]
}
```

Events and visits in single-active systems require `activation`. The same world may appear in several activation records.

Exact invariants:

> Represented sequence order is not a count of experienced iterations. A selected-state gap cannot certify immediate physical predecessor relationships.

> Single-active event membership is checked against an activation occurrence, not just a world ID. Activity changes do not create births, deaths, or persistent sibling worlds.

> Multiple ladders require an explicit selected revision per ladder; “maximum order anywhere” is not a world state.

```text
E288 {path}: sampled history is represented as an exhaustive iteration count or immediate predecessor.
E289 {path}: event, visit, or current-state display lacks a matching history activation.
E290 {path}: multiple revision ladders lack an explicit joint state selection.
```

**Groundhog repair:** display `REPRESENTED ITERATION r2`, not literal “third loop.”  
**SG repair:** readings and rescue events acquire exact activation membership.

## R8. Distinguish terminal continuity from memory at transition

**Refs:** AMEND-2/E219, A5/A9.

Retain `memory:"retained"` when Evan enters the prenatal experience. Add thread termination:

```json
{
  "termination":{
    "event":"fetal-death",
    "reason":"embodied_death",
    "instance":"fetus",
    "fate":"fetus-dead"
  }
}
```

Allow a final visit to end at the termination event rather than requiring an unrelated cutoff. The old cutoff-only form remains legal for an incomplete chart.

Exact invariants:

> Death terminates the represented embodied route at the cited fate. No visit follows it. Absence of a resulting adult biography is a separate revision fact.

> `memory:"none"` means no retained-memory continuity across that transition; it must not be used as shorthand for death later in the destination.

Add optional developmental linkage:

```json
{"id":"evan-development","kind":"developmental","instances":["fetus","adult"],"character":"evan","evidence_events":["prenatal","result"]}
```

Its semantics are potential developmental identity across the represented revisions, **not** simultaneous existence or automatic body-state propagation.

```text
E291 {path}: terminal route confuses transition memory, later embodied death, or absent developmental outcome.
```

This fixes the ending without adding a biological-paradox simulator.

## R9. Require genealogy role events; allow unknown occurrence location honestly

**Refs:** IN-6/IN-8, E270/E279.

A genealogy edge must name:

```json
{
  "parent_event":"conception",
  "child_event":"birth",
  "parent_role":"father"
}
```

`parent_role`: `mother|father|parent|unknown`.

Exact invariants:

> Its causal link must connect those exact events. Parent and child identities must match their role instances. A birth-to-birth ancestry dependency may be recorded as a causal link, but cannot masquerade as conception-to-birth support.

For person provenance, permit:

```json
{"kind":"origin","event":null,"evidence_events":["parentage-revelation"]}
```

This means an asserted birth/origin with unplaced occurrence, not an unknown person identity. It is not usable as a world-existence witness.

```text
E292 {path}: genealogy role, conception/birth event, or identity-instance membership disagrees.
E293 {path}: unplaced origin is used as a located occurrence or world-existence witness.
```

**Dark repair:** do not assign the Unknown’s birth to E merely to satisfy required event placement. Do not use `enter-E` as Martha’s conception event.

## R10. Type observation versus fate, and make provenance claims explicit

**Refs:** A5, IN-7 attractors, IN-8.

Add:

```json
{
  "observations":[
    {
      "id":"apparent-kurisu-death",
      "event":"apparent-death",
      "observer":"earlier-okabe",
      "subject_instance":"kG",
      "claim":"appears-dead",
      "evidence_events":["apparent-death"]
    }
  ]
}
```

Observation claims do not create fates.

Add optional occurrence field:

```json
{"bootstrap_participation":true}
```

Exact invariants:

> Only occurrences explicitly marked as participating must satisfy the same-subject closed-chain reachability check. Every rendered bootstrap label must trace to closed provenance, never a future origin or unknown boundary.

> Fixed-outcome text and observed apparent death cannot generate a dead fate.

```text
E294 {path}: observation or attractor claim is rendered as an unrecorded bodily fate.
E295 {path}: rendered bootstrap claim lacks explicit closed provenance and occurrence support.
```

**Algorithm disposition:** retain future manufacture. No new machinery is justified to force a bootstrap claim unsupported by the supplied evidence.

## R11. Make termination and rendering tests executable obligations

**Refs:** B7–11, B30, C2, IN-6/IN-9.

Exact rules:

> Physical termination is compared within the event’s world/history occurrence, using authored physical ordering. Presentation after a termination scene is not physical existence after termination.

> Renderer input is an immutable normalized snapshot. Every primitive carries its source IDs and selected state/activation. Cache keys include all interpretation parameters, axis, active selections, and source-content hashes.

> Every semantic record’s direct citation or inherited evidence-event citations appears in the export manifest and accessible rendered detail. Counts of worlds, bodies, instances, visits, and selected iterations are never relabelled as survivors or total lived iterations.

```text
E296 {path}: physical termination was inferred from presentation order.
E297 {path}: rendered primitive belongs to a stale document, interpretation, axis, or state selection.
E298 {path}: semantic evidence is missing from the rendered or exported evidence manifest.
E299 {path}: rendered count asserts an unauthored population, survival, or iteration total.
```

Required execution matrix:

- Every preset and equivalent custom parameter set produce identical semantic primitives.
- Shuffling every unordered collection changes no semantics.
- Changing only axis changes no fate, body identity, currentness, or causal relation.
- Changing profile/state selection invalidates all affected render caches.
- Each E251–E299 has one minimal rejecting fixture.
- Each claimed closed v1 critical has a positive, negative, and render-manifest regression.
- Negative CLI tests require exit code 2.
- **No corpus “validates” badge before these tests run.**

## Refusal fallback: no invented ontology

Where exact journeys, origin locations, or mechanism claims remain unsupported, use a separate P4 document like (h), not a claimed clean committed fixture. For the Algorithm question, this is the complete minimal observation fallback:

```json
{
  "schema_version":2,"interpretation_profile":"P4","interpretation_rules":"none","validation_profile":"evidence_pending",
  "meta":{"title":"Tenet — Algorithm observations only","subtitle":"No bootstrap ontology asserted","footer":"Future manufacture report does not establish a closed object history.","axis":"story_order"},
  "sources":[{"id":"film","title":"Tenet Algorithm explanation","kind":"canon_statement","text":"Characters describe the Algorithm as a physical construction made by a scientist in the future."}],
  "characters":[{"id":"p","label":"Protagonist"}],"travellers":[{"id":"pm","character":"p","label":"Observed Protagonist","color":[38,118,62]}],"namespaces":[{"id":"O","label":"Observation"}],"graph_links":[],"extensions":{},
  "graphs":[{
    "namespace":"O","title":"Reported provenance","universes":[{"id":"C","label":"Explanation scene","origin":{"kind":"initial"}}],"instances":[],
    "events":[{"id":"hear","kind":"start","universe":"C","story_order":0,"world_time":null,"label":"Protagonist hears the account of future manufacture","cite":{"source":"film","page":null,"scene":null,"locator":"Algorithm explanation","status":"unavailable"}},{"id":"stop","kind":"cutoff","universe":"C","story_order":1,"world_time":null,"label":"Observation ends; closed provenance not established","cite":{"source":"film","page":null,"scene":null,"locator":"Algorithm explanation","status":"unavailable"}}],
    "splits":[],"transfers":[],"merges":[],"segments":[],"beats":[],"fates":[],
    "thread":{"traveller":"pm","visits":[{"id":"v","traveller":"pm","universe":"C","entry":"hear","exit":"stop","passes":[]}],"links":[]},
    "layout":{"lane_order":["C"],"collapsed_universes":[]},"assumptions":["A reported origin is preserved as an observation; no closed object chain is asserted."]
  }]
}
```

# Verdict

“Local pass” below means the named manual checks passed—not executed validation or render certification.

| Fixture | Preset/params | Validates? | False claims still exposed | Open v1 findings | Friction notes |
|---|---|---|---|---|---|
| Tenet | `tenet` | **Not certifiable:** E257 boundary ambiguity; E258 underchecks coordination | Shared boundary counted twice; unrelated pincer coordination; renamed-body resurrection; Algorithm bootstrap if inferred | 1, 5, 6, 8, 11, 12 | Rich body tracks lack exact event-position and route coverage rules |
| BTTF2 | `P2` | **No: E214** at `mv0→mv1` | Marty substituted for Biff; physical travel rendered as possession; letter rendered as time jump | 1, 4, 5, 6, 7, 9, 12 | Other-agent supersession is structurally second-class |
| Groundhog Day | `P3` | **Local pass; sampling semantics unresolved** | Selected index becomes literal loop count; Rita state or memory inferred | 1, 5, 6, 8, 10, 12 | One-world support exists; iteration identity needs explicit gaps |
| Butterfly Effect | `P2` | **Local pass as limited adult-route projection only** | Terminal `none` implies no prenatal continuity; adult absence becomes no fetal existence | 1, 4, 5, 7, 9, 12 | Complete ending forces continuity loss at the wrong boundary |
| Dark | `dark` | **Not a clean film acceptance fixture** | Proxy conception; allocated birth location; compressed direct journey; visitor rendered as native counterpart | 1, 4, 5, 6, 7, 8, 12 | Topology works better than occurrence, genealogy-role, and journey semantics |
| Steins;Gate | `steins-gate` | **Local transport/metric checks pass; full chronology not certified** | Unbound activation; apparent death becomes death; physical rescue becomes host occupation | 1, 4, 5, 6, 7, 9, 12 | Worldline activity and memory effects are weaker than P1 routing |
| THE WAIF | `P1` + `waif` | **Header only; complete body unavailable here** | Any claim of executed compatibility or rendered correctness | 5, 11, 12 require execution | Best-supported legacy path; cannot be the corpus’s sole standard |
| Groundhog observations | Undeclared; all other parameters `null` | **Manual semantic pass; render unverified** | Only if required P4 markings are omitted or traveller identity is overinterpreted | 5, 11, 12 require execution | Honest fallback, not a substitute for repairing committed profiles |
| Algorithm observations | `P4` | **Manual semantic pass; render unverified** | None asserted beyond the reported explanation | 5, 11, 12 require execution | Refuses unsupported bootstrap provenance without discarding evidence |