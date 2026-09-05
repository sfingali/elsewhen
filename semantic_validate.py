#!/usr/bin/env python3
"""Semantic validator for film-universe-timelines v2.3 (spec E-series + AMEND-5 guards + R-repairs).

Usage: python3 semantic_validate.py DOC.json [--schema build/schema_v2.json]
Exit 0 = clean, exit 2 = diagnostics (matches repo convention). Tracebacks are bugs, not diagnostics.
"""
import json, sys, os

DIAG = []

def err(code, path, message):
    DIAG.append({"code": code, "path": path, "message": message})

def E(code, path, message):
    """Raise-and-collect helper: record and continue where safe."""
    err(code, path, message)

# ---------- helpers ----------

def index_by(items, key="id"):
    out = {}
    dups = []
    for it in items:
        k = it.get(key)
        if k in out:
            dups.append(k)
        else:
            out[k] = it
    return out, dups

PROFILE_ONE_WORLD = {"P2", "P3"}
PRESETS = {"P1", "P2", "P3", "P4", "waif", "tenet", "memento", "dark", "steins-gate", "looper",
           "eot", "darko", "azkaban", "predestination", "timecrimes", "interstellar"}

def profile(doc):
    p = doc.get("interpretation_profile")
    if isinstance(p, str):
        return p, {"declaration": "declared" if p != "P4" else "undeclared"}
    if isinstance(p, dict):
        return None, p
    return None, {}

def validate_semantics(doc):
    global DIAG
    DIAG = []
    prof_name, prof = profile(doc)
    declaration = prof.get("declaration", "declared" if prof_name != "P4" else "undeclared")

    # E200: profile must be declared
    p = doc.get("interpretation_profile")
    if p is None:
        err("E200", "/interpretation_profile", "canonical document must declare interpretation_profile.")
        return DIAG
    if isinstance(p, str) and p not in PRESETS:
        err("E012", "/interpretation_profile", f"unsupported interpretation_profile '{p}'.")
    if isinstance(p, dict):
        if p.get("declaration") == "undeclared":
            for k in ("direction", "presentation", "branching", "revision", "loop", "metric"):
                if p.get(k) is not None:
                    err("E248", f"/interpretation_profile/{k}",
                        "P4 must leave world relationships undeclared; all other parameters must be null.")
                    break

    rules = doc.get("interpretation_rules", "none")
    if rules == "waif":
        pn = prof_name or p if isinstance(p, str) else None
        if isinstance(p, dict) or p != "P1":
            err("E201", "/interpretation_rules", "'waif' requires interpretation_profile 'P1'.")

    graphs = doc.get("graphs", [])
    all_universe_ids = set()
    for gi, g in enumerate(graphs):
        gp = f"/graphs/{gi}"
        validate_graph(g, gp, doc, prof_name, declaration)
        for u in g.get("universes", []):
            all_universe_ids.add(u.get("id"))

    # E249: P2/P3 graphs must share one world identity
    if prof_name in PROFILE_ONE_WORLD:
        worlds = [tuple(sorted(u.get("id") for u in g.get("universes", []))) for g in graphs]
        if len(set(worlds)) > 1:
            err("E249", "/graphs", "graphs must share one world identity and identical revision declarations.")

    # P4: every graph must carry the undeclared marking (render obligation; validator enforces declaration shape only)
    return DIAG

def validate_graph(g, gp, doc, prof_name, declaration):
    universes, dup_u = index_by(g.get("universes", []))
    for d in dup_u:
        err("E030", f"{gp}/universes", f"duplicate universe id '{d}'.")
    events, dup_e = index_by(g.get("events", []))
    for d in dup_e:
        err("E031", f"{gp}/events", f"duplicate event id '{d}'.")
    instances, dup_i = index_by(g.get("instances", []))
    for d in dup_i:
        err("E032", f"{gp}/instances", f"duplicate instance id '{d}'.")

    uids = set(universes.keys())
    eids = set(events.keys())

    # --- universes: origins ---
    born_events = set()
    for uid, u in universes.items():
        o = u.get("origin", {})
        kind = o.get("kind")
        if kind == "born":
            parent = o.get("parent")
            if parent not in uids:
                err("E060", f"{gp}/universes/{uid}/origin/parent", f"born universe '{uid}' cites unknown parent '{parent}'.")
            ev = o.get("event")
            born_events.add(uid)
            # parent must exist BEFORE the child's birth event (existence-before-entry, R-repair)
            if ev not in eids:
                err("E061", f"{gp}/universes/{uid}/origin/event", f"born universe '{uid}' cites unknown birth event '{ev}'.")
        # preexisting universes carry '*' by convention in id (chart-language); warn-level not error
    # P1: every born universe's parent must NOT be born-with-tine-from-itself etc. (cycles)
    for uid, u in universes.items():
        seen = set()
        cur = uid
        while True:
            o = universes.get(cur, {}).get("origin", {})
            if o.get("kind") != "born":
                break
            if cur in seen:
                err("E063", f"{gp}/universes/{uid}", "origin ancestry cycle.")
                break
            seen.add(cur)
            cur = o.get("parent")
            if cur is None or cur not in uids:
                break

    # --- events reference their universe ---
    for eid, e in events.items():
        if e.get("universe") not in uids:
            err("E040", f"{gp}/events/{eid}/universe", f"event '{eid}' cites unknown universe '{e.get('universe')}'.")

    # --- splits: outcome coverage and identity ---
    split_events = set()
    for s_i, s in enumerate(g.get("splits", [])):
        sp = f"{gp}/splits/{s_i}"
        ev = s.get("event")
        split_events.add(ev)
        if ev not in eids:
            err("E080", f"{sp}/event", f"split cites unknown event '{ev}'.")
            continue
        outcomes = s.get("outcomes", {})
        for tine in ("+", "-"):
            o = outcomes.get(tine)
            if not o:
                err("E081", f"{sp}/outcomes/{tine}", "split is missing an outcome tine; every pull must declare both tines.")
                continue
            if o.get("universe") not in uids:
                err("E082", f"{sp}/outcomes/{tine}/universe", f"outcome tine '{tine}' cites unknown universe '{o.get('universe')}'.")
            if o.get("entry") not in eids:
                err("E083", f"{sp}/outcomes/{tine}/entry", f"outcome tine '{tine}' cites unknown entry event '{o.get('entry')}'.")
            # born outcome must correspond to a born universe with that parent/tine (E084)
            if o.get("universe_outcome") == "born":
                u = universes.get(o.get("universe"), {})
                org = u.get("origin", {})
                if org.get("kind") != "born":
                    err("E084", f"{sp}/outcomes/{tine}", f"outcome declares 'born' but universe '{o.get('universe')}' is not a born universe.")
                elif org.get("parent") != (events.get(ev, {}).get("universe")) or org.get("event") != ev:
                    err("E085", f"{sp}/outcomes/{tine}", f"universe '{o.get('universe')}' birth origin does not match split '{ev}'.")
        # source_disposition continues => '+' outcome universe must be the source universe
        if s.get("source_disposition") == "continues":
            src = events.get(ev, {}).get("universe")
            if outcomes.get("+", {}).get("universe") != src:
                err("E086", f"{sp}/outcomes/+", f"source_disposition 'continues' requires '+' tine to continue the source universe '{src}'.")
        # traveller must exist
        if s.get("traveller") and s.get("traveller") not in {t.get("id") for t in doc.get("travellers", [])}:
            err("E087", f"{sp}/traveller", f"split cites unknown traveller '{s.get('traveller')}'.")

    # --- transfers: endpoints resolve; entry/exit events exist ---
    transfer_ids = set()
    for t_i, t in enumerate(g.get("transfers", [])):
        tp = f"{gp}/transfers/{t_i}"
        tid = t.get("id")
        transfer_ids.add(tid)
        frm, to = t.get("from", {}), t.get("to", {})
        for side, ref in (("from", frm), ("to", to)):
            u = ref.get("universe")
            if u is not None and u not in uids:
                err("E110", f"{tp}/{side}/universe", f"transfer '{tid}' {side} cites unknown universe '{u}'.")
            for k in ("exit", "entry", "event"):
                if ref.get(k) is not None and ref[k] not in eids:
                    err("E111", f"{tp}/{side}/{k}", f"transfer '{tid}' {side} cites unknown event '{ref[k]}'.")
        if frm.get("universe") and to.get("universe") and frm["universe"] == to["universe"]:
            rel = (t.get("relation") or {}).get("kind")
            if rel not in ("same_world", "unknown"):
                err("E112", f"{tp}", f"transfer '{tid}' is same-universe but relation is '{rel}'.")
        # R6: traversal/mechanism coherence
        mech = t.get("mechanism")
        trav = t.get("traversal")
        if mech in ("time_leap",) and trav != "memory":
            err("E118", f"{tp}/traversal", f"time_leap transfer '{tid}' must use traversal 'memory'.")
        if mech == "consciousness_transfer" and trav not in (None,):
            err("E119", f"{tp}/traversal", f"consciousness_transfer '{tid}' carries no traversal payload field; leave traversal unset.")

    # --- thread: authoritative route (E130-E145) ---
    thread = g.get("thread", {})
    visits = thread.get("visits", [])
    traveller_ids = {t.get("id") for t in doc.get("travellers", [])}
    visit_ids, dup_v = index_by(visits)
    for d in dup_v:
        err("E131", f"{gp}/thread/visits", f"duplicate visit id '{d}'.")
    if visits:
        tv = thread.get("traveller")
        if tv not in traveller_ids:
            err("E130", f"{gp}/thread/traveller", f"thread cites unknown traveller '{tv}'.")
        for v_i, v in enumerate(visits):
            vp = f"{gp}/thread/visits/{v_i}"
            if v.get("universe") not in uids:
                err("E132", f"{vp}/universe", f"visit '{v.get('id')}' cites unknown universe '{v.get('universe')}'.")
            if v.get("entry") not in eids:
                err("E133", f"{vp}/entry", f"visit '{v.get('id')}' cites unknown entry event '{v.get('entry')}'.")
            if v.get("exit") not in eids:
                err("E134", f"{vp}/exit", f"visit '{v.get('id')}' cites unknown exit event '{v.get('exit')}'.")
            if v.get("traveller") != tv:
                err("E136", f"{vp}/traveller", f"visit '{v.get('id')}' traveller does not match thread traveller.")
        # continuity: links must chain visits in order; exit of vN connects to entry of vN+1 via the link's mechanism
        links = thread.get("links", [])
        seen_pairs = set()
        for l_i, l in enumerate(links):
            lp = f"{gp}/thread/links/{l_i}"
            a, b = l.get("from_visit"), l.get("to_visit")
            if a not in visit_ids or b not in visit_ids:
                err("E135", lp, f"link cites unknown visit(s) '{a}'->'{b}'.")
                continue
            if (a, b) in seen_pairs:
                err("E137", lp, f"duplicate link {a}->{b}.")
            seen_pairs.add((a, b))
            kind = l.get("kind")
            # chain order check: visits are an ordered route
            order = [v.get("id") for v in visits]
            if a in order and b in order and order.index(b) != order.index(a) + 1:
                err("E138", lp, f"link {a}->{b} skips visits; thread must be a continuous route.")
            va, vb = visit_ids.get(a, {}), visit_ids.get(b, {})
            if kind == "split":
                sp_id = l.get("split")
                if not sp_id:
                    err("E139", lp, "split link missing split reference.")
                else:
                    sp = next((s for s in g.get("splits", []) if s.get("event") == sp_id), None)
                    if sp is None:
                        err("E139", lp, f"split link cites unknown split '{sp_id}'.")
                    else:
                        tine = l.get("tine")
                        out = sp.get("outcomes", {}).get(tine, {})
                        # the destination visit's universe must match the tine outcome
                        if out.get("universe") != vb.get("universe"):
                            err("E140", lp, f"split link tine '{tine}' outcome universe '{out.get('universe')}' does not match visit '{b}' universe '{vb.get('universe')}'.")
                        if va.get("exit") != sp_id:
                            err("E141", lp, f"split link requires visit '{a}' to exit at the split event '{sp_id}'.")
            elif kind == "transfer":
                tid = l.get("transfer")
                t = next((x for x in g.get("transfers", []) if x.get("id") == tid), None)
                if t is None:
                    err("E142", lp, f"transfer link cites unknown transfer '{tid}'.")
                else:
                    if t["from"].get("universe") != va.get("universe") or t["to"].get("universe") != vb.get("universe"):
                        err("E143", lp, f"transfer link '{tid}' endpoints do not match the visits it connects.")
                    if va.get("exit") != t["from"].get("exit"):
                        err("E144", lp, f"transfer link '{tid}' requires visit '{a}' to exit at '{t['from'].get('exit')}'.")
                    if vb.get("entry") != t["to"].get("entry"):
                        err("E145", lp, f"transfer link '{tid}' requires visit '{b}' to enter at '{t['to'].get('entry')}'.")
        # the route must form a single connected chain covering all visits
        if len(links) and len(links) != len(visits) - 1:
            err("E146", f"{gp}/thread/links", f"thread has {len(visits)} visits but {len(links)} links; a single route needs exactly len-1.")
        # split-birth check for split links: the thread enters the '+' tine by default only if declared
    # E210: fates reference instances and events
    inst_ids = set(instances.keys())
    for f_i, f in enumerate(g.get("fates", [])):
        fp = f"{gp}/fates/{f_i}"
        if f.get("instance") not in inst_ids:
            err("E210", f"{fp}/instance", f"fate '{f.get('id')}' cites unknown instance '{f.get('instance')}'.")
        if f.get("event") not in eids:
            err("E211", f"{fp}/event", f"fate '{f.get('id')}' cites unknown event '{f.get('event')}'.")

    # --- segments: endpoints in same universe ---
    seg_ids, dup_s = index_by(g.get("segments", []))
    for d in dup_s:
        err("E033", f"{gp}/segments", f"duplicate segment id '{d}'.")
    for sid, sg in seg_ids.items():
        eu = events.get(sg.get("from"), {}).get("universe")
        eu2 = events.get(sg.get("to"), {}).get("universe")
        if sg.get("universe") not in uids:
            err("E150", f"{gp}/segments/{sid}/universe", f"segment cites unknown universe '{sg.get('universe')}'.")
        if eu != sg.get("universe") or eu2 != sg.get("universe"):
            err("E151", f"{gp}/segments/{sid}", f"segment '{sid}' endpoints are not both in its universe.")

    # --- beats reference segments ---
    for b_i, b in enumerate(g.get("beats", [])):
        bp = f"{gp}/beats/{b_i}"
        if b.get("segment") not in seg_ids:
            err("E152", f"{bp}/segment", f"beat '{b.get('id')}' cites unknown segment '{b.get('segment')}'.")
        c = b.get("cite", {})
        if not c.get("locator"):
            err("E160", f"{bp}/cite", f"beat '{b.get('id')}' lacks a citation locator.")

    # --- instances: universe resolves ---
    for iid, inst in instances.items():
        if inst.get("universe") not in uids:
            err("E042", f"{gp}/instances/{iid}/universe", f"instance '{iid}' cites unknown universe '{inst.get('universe')}'.")

    # --- PROFILE GUARDS (AMEND-5 / E240-E250) ---
    born_count = sum(1 for u in universes.values() if u.get("origin", {}).get("kind") == "born")
    has_revision_machinery = bool(g.get("revisions") or g.get("revision_ladders"))
    has_splits = bool(g.get("splits"))
    has_transfers = bool(g.get("transfers"))
    if prof_name == "P2":
        if len(universes) != 1:
            err("E240", f"{gp}/universes", "P2 requires exactly one world; revisions are not universes.")
        if has_splits or has_transfers:
            err("E243", gp, "P2 forbids P1 branching or cross-universe routing machinery.")
        if not g.get("revisions"):
            err("E245", gp, "P2 requires a nonempty ordered revision history.")
    elif prof_name == "P3":
        if len(universes) != 1:
            err("E241", f"{gp}/universes", "P3 requires exactly one loop world; iterations are not universes.")
        if has_splits or has_transfers:
            err("E243", gp, "P3 forbids P1 branching or cross-universe routing machinery.")
        if not g.get("revisions"):
            err("E245", gp, "P3 requires a nonempty ordered revision history.")
    elif prof_name == "P1" or prof_name == "waif":
        if has_revision_machinery:
            err("E244", gp, "P1 forbids same-world revision machinery and supersession fates.")
    elif declaration == "undeclared":
        if has_splits or has_transfers:
            err("E248", gp, "P4 must leave world relationships undeclared (no split/transfer machinery).")

    # loops
    for l_i, loop in enumerate(g.get("loops", [])):
        if prof_name == "P2" and loop.get("kind") == "memory-reset":
            err("E247", f"{gp}/loops/{l_i}", "transition kind 'memory-reset' is incompatible with P2.")
    return DIAG

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: semantic_validate.py DOC.json [--schema build/schema_v2.json]")
        return 2
    doc = json.load(open(args[0]))
    # Phase 1: JSON Schema (if available)
    schema_path = None
    argv = sys.argv[1:]
    if "--schema" in argv:
        schema_path = argv[argv.index("--schema") + 1]
    else:
        cand = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema_v2.json")
        if os.path.exists(cand):
            schema_path = cand
    if schema_path and os.path.exists(schema_path):
        try:
            import jsonschema
            schema = json.load(open(schema_path))
            v = jsonschema.Draft202012Validator(schema)
            sch_errs = sorted(v.iter_errors(doc), key=lambda e: str(list(e.absolute_path)))
            for e in sch_errs:
                err("E001", "/" + "/".join(str(x) for x in list(e.absolute_path)), e.message[:200])
        except ImportError:
            print("WARNING: jsonschema not installed; skipping structural phase", file=sys.stderr)
    # Phase 2: semantics
    validate_semantics(doc)
    for d in DIAG:
        print(f"{d['code']} {d['path']}: {d['message']}")
    print(f"-- {len(DIAG)} diagnostic(s)")
    return 2 if DIAG else 0

if __name__ == "__main__":
    sys.exit(main())
