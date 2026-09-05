#!/usr/bin/env python3
"""Import a legacy schema_v2 story document into the pure abstract model.

The abstract model carries the story's structure with no presentation: worlds
and their origins, events, splits (both tines + character fates), transfers,
the route, fates, and citations. Presentation-only fields are deliberately
dropped — `meta.timescale`, `layout.lane_order`, `layout.collapsed_universes`,
and traveller `color` are not story facts, so they do not survive the import.

Usage:
  python3 to_abstract.py FIXTURE.json [--out abstract.json] [--text|--dot|--mermaid|--markdown]
Without --out, prints the abstract JSON (or the abstract text with --text).
"""

import copy
import json
import sys


def convert(doc):
    """schema_v2 document -> abstract-model dict."""
    meta = doc.get("meta", {})
    out = {
        "abstract_model": "universe-timeline/1.0",
        "title": meta.get("title", "(untitled)"),
        "subtitle": meta.get("subtitle", ""),
        "footer": meta.get("footer", ""),
        "profile": _profile(doc),
        "sources": copy.deepcopy(doc.get("sources", [])),
        "characters": copy.deepcopy(_pluck(doc.get("characters", []), ("id", "label"))),
        # travellers: identity only; colour is presentation and is dropped
        "travellers": _pluck(doc.get("travellers", []), ("id", "character")),
        "namespaces": _pluck(doc.get("namespaces", []), ("id", "label")),
        "graphs": [_graph(g) for g in doc.get("graphs", [])],
    }
    return out


def _profile(doc):
    """Build the profile as an explicit parameter set (name + expanded params)."""
    name = doc.get("interpretation_profile")
    if not name:
        return {}
    try:
        from profiles import resolve as _res
        params = _res(name)
    except Exception:
        params = {}
    if doc.get("validation_profile"):
        params["validation"] = doc["validation_profile"]
    prof = {"name": name, "params": params}
    if doc.get("interpretation_rules"):
        prof["rules"] = doc["interpretation_rules"]
    return prof


def _pluck(items, keys):
    out = []
    for it in items:
        out.append({k: it.get(k) for k in keys if k in it})
    return out


def _graph(g):
    events = g.get("events", [])
    ev_by_id = {e["id"]: e for e in events}

    worlds = []
    for u in g.get("universes", []):
        origin = u.get("origin", {})
        w = {
            "id": u["id"],
            "label": u.get("label", ""),
            "origin": origin.get("kind", "unknown"),
        }
        if w["origin"] == "born" and origin.get("event"):
            w["born"] = {"event": origin.get("event"), "parent": origin.get("parent"), "tine": origin.get("tine")}
        if origin.get("ancestry"):
            w["ancestry"] = origin["ancestry"]
        worlds.append(w)

    out_splits = []
    for sp in g.get("splits", []):
        ev = sp.get("event")
        outcomes = {}
        for sign, o in (sp.get("outcomes") or {}).items():
            outcomes[sign] = {
                "universe": o.get("universe"),
                "entry": o.get("entry"),
                "universe_outcome": o.get("universe_outcome"),
                "instances": [
                    {"instance": c.get("instance"), "outcome": c.get("outcome"), "fate": c.get("fate")}
                    for c in o.get("character_outcomes", [])
                ],
            }
        out_splits.append({
            "event": ev,
            "cause": sp.get("cause"),
            "automatic": sp.get("automatic"),
            "traveller": sp.get("traveller"),
            "source_disposition": sp.get("source_disposition"),
            "source_universe": ev_by_id.get(ev, {}).get("universe"),
            "outcomes": outcomes,
        })

    transfers = []
    for tr in g.get("transfers", []):
        transfers.append(copy.deepcopy({
            "id": tr.get("id"),
            "traveller": tr.get("traveller"),
            "from": {"universe": tr.get("from", {}).get("universe"), "exit": tr.get("from", {}).get("exit")},
            "to": {"universe": tr.get("to", {}).get("universe"), "entry": tr.get("to", {}).get("entry")},
            "mechanism": tr.get("mechanism"),
            "relation": copy.deepcopy(tr.get("relation")),
        }))

    thread = g.get("thread", {})
    # collect evidence = every citable record (events, beats, fates) that has a cite
    evidence = []
    for e in events:
        if e.get("cite"):
            evidence.append({"where": e["id"], "note": e.get("label"), "cite": e["cite"]})
    for b in g.get("beats", []):
        if b.get("cite"):
            evidence.append({"where": b["id"], "note": b.get("text"), "cite": b["cite"]})
    for f in g.get("fates", []):
        if f.get("cite"):
            evidence.append({"where": f["id"], "note": f.get("status"), "cite": f["cite"]})

    return {
        "namespace": g.get("namespace"),
        "title": g.get("title", ""),
        "worlds": worlds,
        "events": [
            {"id": e.get("id"), "kind": e.get("kind"), "universe": e.get("universe"),
             "order": e.get("story_order"), "label": e.get("label"), "cite": copy.deepcopy(e.get("cite"))}
            for e in events
        ],
        "segments": [
            {"id": s.get("id"), "universe": s.get("universe"), "from": s.get("from"), "to": s.get("to"), "label": s.get("label")}
            for s in g.get("segments", [])
        ],
        "beats": [
            {"id": b.get("id"), "segment": b.get("segment"), "order": b.get("story_order"), "text": b.get("text"), "cite": b.get("cite")}
            for b in g.get("beats", [])
        ],
        "splits": out_splits,
        "transfers": transfers,
        "route": {
            "traveller": thread.get("traveller"),
            "visits": [
                {"id": v.get("id"), "universe": v.get("universe"), "entry": v.get("entry"), "exit": v.get("exit"), "passes": _pluck(v.get("passes", []), ("split", "tine"))}
                for v in thread.get("visits", [])
            ],
            "links": [
                {"from": l.get("from_visit"), "to": l.get("to_visit"), "kind": l.get("kind"), "via": l.get("split") or l.get("transfer")}
                for l in thread.get("links", [])
            ],
        },
        "fates": [
            {"id": f.get("id"), "universe": f.get("universe"), "instance": f.get("instance"), "event": f.get("event"), "status": f.get("status"), "cite": f.get("cite")}
            for f in g.get("fates", [])
        ],
        "merges": len(g.get("merges") or []),
        "assumptions": copy.deepcopy(g.get("assumptions", [])),
        "evidence": evidence,
    }


def _apply_profile(abstract, base, overrides):
    """Resolve a profile into a base preset + explicit parameter overrides."""
    from profiles import resolve
    prof = abstract.get("profile") or {}
    name = base or prof.get("name") or "P1"
    merged = dict(prof.get("params", {}))
    merged.update(overrides)
    params = resolve({"name": name, "params": merged})
    abstract["profile"] = {"name": name, "params": params}
    if prof.get("rules"):
        abstract["profile"]["rules"] = prof["rules"]
    return abstract


def main(argv):
    if len(argv) < 2:
        print("usage: to_abstract.py FIXTURE.json [--out F] [--text] [--base PROFILE] [--set k=v ...]",
              file=sys.stderr)
        return 2
    path = argv[1]
    with open(path) as fh:
        doc = json.load(fh)
    abstract = convert(doc)

    want_text = "--text" in argv[2:]
    out = None
    base = None
    overrides = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--out="):
            out = a.split("=", 1)[1]
        elif a == "--out":
            out = argv[i + 1]; i += 1
        elif a == "--base":
            base = argv[i + 1]; i += 1
        elif a.startswith("--set="):
            k, _, v = a[len("--set="):].partition("=")
            overrides[k.strip()] = v.strip()
        elif a == "--set":
            k, _, v = argv[i + 1].partition("=")
            overrides[k.strip()] = v.strip(); i += 1
        i += 1

    if base or overrides:
        abstract = _apply_profile(abstract, base, overrides)

    if want_text:
        from abstract_model import AbstractStory
        text = AbstractStory.from_dict(abstract).to_text()
        if out:
            with open(out, "w") as fh:
                fh.write(text + "\n")
        else:
            print(text)
        return 0

    # default: emit the abstract JSON
    dumped = json.dumps(abstract, indent=2)
    if out:
        with open(out, "w") as fh:
            fh.write(dumped + "\n")
    else:
        print(dumped)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
