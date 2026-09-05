#!/usr/bin/env python3
"""v2.3 fixture -> v1 renderer adapter. Never invents facts: absent fields stay absent."""
import json

PRESET_CHIP = {
    "P1": "PROFILE P1 - BRANCH MULTIVERSE",
    "waif": "PROFILE P1 - BRANCH MULTIVERSE (HOUSE: WAIF)",
    "P2": "PROFILE P2 - SINGLE MUTABLE TIMELINE",
    "P3": "PROFILE P3 - CLOSED LOOP, MIND PERSISTS",
    "P4": "P4 - ONTOLOGY UNDECLARED",
    "tenet": "PROFILE TENET - PER-TRAVELLER DIRECTION, FATED LOOP",
    "memento": "PROFILE MEMENTO - DUAL AXIS (STORY/VIEW)",
    "dark": "PROFILE DARK - KNOT TOPOLOGY, FATED LOOP",
    "steins-gate": "PROFILE STEINS;GATE - WORLDLINES WITH DIVERGENCE METRIC",
    "looper": "PROFILE LOOPER - REVISION LADDER WITH BODY LINKAGE",
}

def _beat(text, cite=None):
    b = {"beat": text}
    if cite:
        parts = []
        if cite.get("page"): parts.append("p" + str(cite["page"]))
        if cite.get("scene"): parts.append("#" + str(cite["scene"]))
        if parts: b["cite"] = " ".join(parts)
        if cite.get("status") == "unresolved": b["certainty"] = "unseen"
    return b

def _origin_star(u):
    o = u.get("origin", {})
    return "*" if o.get("kind") in ("preexisting", "unknown") else ""

def adapt_p1(g23, graph):
    universes = {u["id"]: u for u in graph["universes"]}
    lane_order = [x for x in graph.get("layout", {}).get("lane_order", []) if x in universes]
    for uid in universes:
        if uid not in lane_order:
            lane_order.append(uid)
    events = {e["id"]: e for e in graph.get("events", [])}
    insts = {i["id"]: i for i in graph.get("instances", [])}

    out = {
        "lanes": lane_order,
        "lane_labels": {uid: _origin_star(universes[uid]) + uid + " - " + universes[uid]["label"] for uid in lane_order},
        "lanes_content": {uid: [] for uid in lane_order},
        "nodes": [], "splits": {}, "joins": {}, "stubs": {}, "arcs": {}, "legend": [],
    }

    for s in graph.get("splits", []):
        ev = events.get(s["event"])
        if not ev:
            continue
        lane = ev["universe"]
        letter = s["event"][2:] if s["event"].startswith("e-") else s["event"]
        letter = letter[:2].upper() if len(letter) > 2 else letter
        cite_l = (ev.get("cite") or {}).get("locator", "")
        cap = letter + " - " + ev["label"]
        if cite_l:
            cap += "\n" + cite_l
        out["splits"][s["event"]] = {"caption": cap, "letter": letter}
        if lane in out["lanes_content"]:
            out["lanes_content"][lane].append({"split": s["event"]})
        for tine in ("+", "-"):
            o = s["outcomes"].get(tine, {})
            u = universes.get(o.get("universe"), {})
            if u.get("origin", {}).get("kind") == "born" and o["universe"] != lane:
                if not any(isinstance(it, dict) and it.get("laneborn") for it in out["lanes_content"].get(o["universe"], [])):
                    out["lanes_content"][o["universe"]].append(
                        {"laneborn": {"from_split": s["event"],
                                       "chip": _origin_star(u) + o["universe"] + " - " + u.get("label", ""),
                                       "note": ""}})

    for t in graph.get("transfers", []):
        dest = t["to"]["universe"]
        src = t["from"]["universe"]
        from_split = None
        for s in graph.get("splits", []):
            se = events.get(s["event"], {})
            if se.get("universe") == src:
                from_split = s["event"]
        entry_ev = events.get(t["to"].get("entry"), {})
        out["joins"][t["id"]] = {"from_split": from_split, "to_lane": dest, "label": t["id"]}
        if dest in out["lanes_content"]:
            out["lanes_content"][dest].append(
                {"join": t["id"], "label": t["id"] + " - " + entry_ev.get("label", "") + " (from " + _origin_star(universes.get(src, {})) + src + " down)"})

    # preexisting lanes: origin header chip (the * marker the aesthetic review demanded)
    for uid in lane_order:
        u = universes[uid]
        if u.get("origin", {}).get("kind") == "preexisting":
            out["lanes_content"][uid].insert(0, {"chip": "* " + uid + " - already running (ancestry off-chart)", "dim": True})
        elif u.get("origin", {}).get("kind") == "unknown":
            out["lanes_content"][uid].insert(0, {"chip": "? " + uid + " - origin undeclared", "dim": True})

    join_entries = {t["to"]["entry"] for t in graph.get("transfers", [])}
    for e in graph.get("events", []):
        if e["id"] in join_entries or e["kind"] in ("split", "outcome", "start"):
            continue
        lane = e["universe"]
        if lane in out["lanes_content"]:
            out["lanes_content"][lane].append(_beat(e["label"], e.get("cite")))

    for sg in graph.get("segments", []):
        lane = sg["universe"]
        if lane in out["lanes_content"]:
            out["lanes_content"][lane].append({"segment": sg["label"]})

    for b23 in graph.get("beats", []):
        seg = next((s for s in graph.get("segments", []) if s["id"] == b23["segment"]), None)
        lane = seg["universe"] if seg else None
        if lane in out["lanes_content"]:
            out["lanes_content"][lane].append(_beat(b23["text"], b23.get("cite")))

    for f in graph.get("fates", []):
        lane = f["universe"]
        inst = insts.get(f["instance"], {})
        if f["status"] == "dead" and lane in out["lanes_content"]:
            out["stubs"][f["id"]] = {"title": lane, "sub": inst.get("label", f["instance"]) + " dies",
                                      "cite": (f.get("cite") or {}).get("locator", "")}
            out["lanes_content"][lane].append({"stub": f["id"]})
        elif f["status"] == "alive" and lane in out["lanes_content"]:
            out["lanes_content"][lane].append({"chip": inst.get("label", f["instance"]) + ": alive at cutoff", "dim": True})

    return out

def adapt_single_lane(g23, graph):
    u = graph["universes"][0]
    lane = u["id"]
    out = {
        "lanes": [lane],
        "lane_labels": {lane: lane + " - " + u["label"]},
        "lanes_content": {lane: []},
        "nodes": [], "splits": {}, "joins": {}, "stubs": {}, "arcs": {}, "legend": [],
    }
    for r in graph.get("revisions", []):
        out["lanes_content"][lane].append({"segment": r["id"] + " - " + r.get("label", r["id"])})
    for e in graph.get("events", []):
        if e["universe"] != lane:
            continue
        rev = e.get("revision")
        prefix = "[" + rev + "] " if rev else ""
        out["lanes_content"][lane].append(_beat(prefix + e["label"], e.get("cite")))
    for t in graph.get("transfers", []):
        if t.get("mechanism") == "time_travel" and t.get("traversal") == "body":
            out["arcs"][t["id"]] = {"traveller": t.get("traveller") or "",
                                     "depart": t["from"].get("exit", ""), "arrive": t["to"].get("entry", "")}
            out["lanes_content"][lane].append({"arc": t["id"]})
            out["lanes_content"][lane].append({"mark": t["id"]})
        elif t.get("mechanism") == "time_leap":
            out["lanes_content"][lane].append({"chip": t["id"] + ": memory leap (body retained)", "dim": True})
    for b23 in graph.get("beats", []):
        out["lanes_content"][lane].append(_beat(b23["text"], b23.get("cite")))
    return out

def adapt(doc):
    profile = doc.get("interpretation_profile", "P4")
    prof_name = profile if isinstance(profile, str) else None
    if prof_name is None:
        decl = profile.get("declaration", "undeclared") if isinstance(profile, dict) else "undeclared"
        chip_text = "P4 - ONTOLOGY UNDECLARED" if decl == "undeclared" else "PROFILE - PARAMETRIC"
    else:
        chip_text = PRESET_CHIP.get(prof_name, "PROFILE " + prof_name.upper())
    single_lane_profile = (isinstance(profile, str) and profile in ("P2", "P3", "P4")) or \
                          (isinstance(profile, dict) and profile.get("declaration") == "undeclared")
    results = []
    for graph in doc.get("graphs", []):
        if single_lane_profile:
            v1 = adapt_single_lane(doc, graph)
        else:
            v1 = adapt_p1(doc, graph)
        m = v1.setdefault("meta", {})
        m["_profile_chip"] = chip_text
        m["_graph_ns"] = graph.get("namespace", "")
        th = graph.get("thread", {})
        vs = th.get("visits", [])
        if vs:
            route = " -> ".join(v["universe"] for v in vs)
            m["_thread_route"] = "THE THREAD: " + route
        v1["legend"] = v1.get("legend", []) + [chip_text]
        results.append(v1)
    return results

if __name__ == "__main__":
    import sys
    doc = json.load(open(sys.argv[1]))
    outs = adapt(doc)
    for i, o in enumerate(outs):
        print("graph", i, "lanes:", o["lanes"], "items:", sum(len(v) for v in o["lanes_content"].values()))
