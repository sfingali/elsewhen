# Chart JSON schema

The JSON is the story. The engine validates then renders. Version: v4 engine.

```jsonc
{
  "_doc": "optional note; ignored",
  "meta": {
    "title": "THE FILM — One Man's Story",
    "subtitle": "one line under the title",
    "thread_label": "THE THREAD: OPEN → WORLD B → WORLD C — THE LAST PULL",
    "footer": "small grey line at the very bottom",
    "canvas": [2800, 3600],            // width clamped to >= 2400
    "node_types": {                    // OPTIONAL per-film palette
      "death":  {"color": [150,74,74]},   // stub edge; fill+text derived
      "ending": {"color": [38,118,62]},   // ending box edge
      "split":  {"color": [255,232,122], "edge": [185,168,95], "text": [60,48,8]},
      "thread": {"color": [38,118,62], "weight": 10},
      "lane":   {"color": [150,148,142], "weight": 4},
      "join":   {"color": [38,118,62], "weight": 10}
    }
  },
  "lanes": [ {"id": "FAM", "label": "FAM"}, ... ],   // LEFT to RIGHT
                                                     // opening universe RIGHTMOST;
                                                     // thread flows right -> left
  "nodes": [ {                        // story-start box, in the opening lane
    "id": "U1", "lane": "OPEN",
    "title": "OPEN — The Opening Universe",
    "body": "Where the story begins.",
    "cite": "p1 #1–3"                 // optional
  } ],
  "lanes_content": {                  // per lane, TOP to BOTTOM, in draw order
    "OPEN": [
      {"node": "U1"},
      {"split": "10"},                // must exist in splits{}
      {"beat": "scene 16", "cite": "#16"},          // optional: tone death|good, side left
      {"segment": "THE TIMELINE WITH HER (from the join down)"} // green chip
      {"stub": "stub-10"},            // the death tine box (forks right)
      {"chip": "OPEN — Runs On", "dim": true},
      {"abandon": 140}                // px of faded 'runs on' tail (60..320)
    ],
    "HER": [
      {"laneborn": {"from_split": null,              // null = already running
        "chip": "HER — Already Running",
        "note": "this world began long before the chart"}},
      {"join": "join-78"}             // join item lives ONLY in to_lane's list
    ]
  },
  "splits": { "10": {"letter": "10", "caption": "The crash — the worlds split"} },
  "stubs":  { "stub-10": {"title": "10B — He Dies", "sub": "the tine where he dies at split #10"} },
  "joins":  { "join-78": {"from_split": "10", "to_lane": "HER",
                           "side": "left", "label": "he enters HER"} },
  "arcs":   {                            // TIME-TRAVEL ARCS: a trip within/into worlds,
    "trip1": {                           // NOT a new universe. Use for films whose
      "from_lane": "OPEN",               // grammar is overwrites, loops, channels.
      "to_lane": "M1985",
      "kind": "travel",                  // travel (thread-colour) | return (grey) | loop (lane-colour)
      "label": "to 2015 and back",
      "side": "right",                   // which way the elbow bulges (auto-defaulted)
      "color": [120,120,126],            // optional per-arc colour (e.g. another traveller)
      "carry_through": false,            // false = another character's trip: the thread IGNORES it
      "arrive_thread": false             // false = its arrival doesn't resume the thread
    }
  },
  // lanes_content items for arcs:
  //   {"arc": "trip1"}  = the DEPARTURE dot (place in from_lane, at its story position)
  //   {"mark": "trip1"} = the ARRIVAL dot (place in to_lane, at its story position)
  // each arc needs exactly one of each; validator enforces it.
  "thread": ["U1", "join-78", "ENDING"],   // ordered route; ids must resolve;
                                           // 'ENDING' is a literal
  "legend": ["line one", "line two"]       // 'The Index / How to Read' box
}
```

## Output-flexibility fields (pass 2a — all opt-in; absent = unchanged rendering)

| field | where | values | effect |
|---|---|---|---|
| `interval` | arc | `[depart, arrive]` | loop-rectangle (Clawz114 staple shape): duration becomes geometry. **Requires `meta.timescale`** — validation refuses otherwise (exit 2) |
| `meta.timescale` | meta | `{"unit": "hour", "start": 0}` | the time axis `interval` measures against |
| `screen` | beat | `film` \| `flashback` \| `deduced` | yellow presence chip (UnrealityMag device) — is this beat shown in the film? |
| `certainty` | beat | `seen` \| `flashback` \| `seen-later` \| `never-shown` | epistemic colour (Clawz114 code): how you know. `classic`/`weight` render full colour; `dash`/`tape` carry letter glyphs S/F/L/N — never silently dropped |
| `traveller` | beat or arc | name in `meta.travellers` | ties the item to a traveller identity |
| `meta.travellers` | meta | `{"Name": [r,g,b]}` | per-traveller colours; enables versioning + survivor census |
| `meta.versioning` | meta | `"crossing-count"` | engine auto-suffixes traveller labels `(n)` = ordinal count of their departures in story order (`Aaron(0)`, `Aaron(1)`…) — no hand-typed version numbers |
| `uncertain` | ending | `true` | dashed/grey "?" terminal box instead of the confident green ending — uncertainty gets its own terminal state |

`meta.travellers` also appends a **survivor census** line to the legend — engine-computed occupancy at the ending, e.g. `2× Abe, 3× Aaron alive at the ending` (Clawz114's closing note, made computable). Absent travellers → no census, no change.

CLI: `--density compact|normal` (default `normal` — byte-identical to the v4 look; `compact` tightens rhythm/lane-gap/stub offset toward the reference-chart density) and `--orientation vertical|horizontal` (default `vertical`; horizontal = time flows left→right, universes as rows stacked top→bottom — the native form of the fan-made Primer charts).

## Validation rules (enforced, exit 2)

- every `split`/`stub`/`node`/`join` reference in `lanes_content` must resolve
- a `join` item may be listed in **only one** lane, and it must be the join's
  `to_lane`
- `joins.*.from_split` must exist; `to_lane` must be a real lane
- every `thread` element must be a known node/split/join id or `ENDING`
- each arc: exactly one `arc` item in from_lane + one `mark` item in to_lane;
  kind travel|return|loop; color [r,g,b]; carry_through/arrive_thread boolean
- `interval` on an arc without `meta.timescale` is refused; `traveller` names
  must exist in `meta.travellers`; `screen`/`certainty` values are enum-checked
- unknown lanes in `lanes_content` fail

## Optional items

- `{"ending": {"title": "...", "body": "...", "cite": "#277–278"}}` in a lane's
  content — green final-image box (hmm: see `universe_graph.py` measure()).
- `{"tone": "death"|"good"}` on beats colours the dot.
- `{"side": "left"}` on beats/joins flips the label to the other side of the
  lane line; join labels auto-flip if they would clip the canvas edge.
