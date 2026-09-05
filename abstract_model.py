#!/usr/bin/env python3
"""Pure abstract, presentation-agnostic model of a multi-universe timeline.

This is the engine's core. It describes WHAT the story's universe structure is
— worlds and their origins, splits, transfers, the protagonist's route, fates,
and citations — with NO opinion about HOW it is drawn. It carries no visual
vocabulary: no glyphs, colours, lanes, dash-styles, density, timescale, or
layout ordering. Any visual form (PIL chart, SVG, HTML, graphviz, mermaid,
plain text, even video) is a *projection* of this model — see projections.py.

Canonical input is the abstract JSON document (see abstract.schema.json), or a
legacy schema_v2 fixture via to_abstract.py.
"""

import json
import sys

MODEL = "universe-timeline/1.0"

# Semantic only. origin kinds are story facts, not drawing instructions.
ORIGIN_KINDS = ("initial", "born", "preexisting", "unknown")
EVENT_KINDS = ("start", "split", "outcome", "entry", "exit", "anchor", "cutoff", "gate_entry", "gate_exit")
FATE_STATUSES = ("alive", "dead", "unknown", "nonexistent")


class AbstractStory:
    """A validated, projection-ready timeline model."""

    def __init__(self, doc):
        self.doc = doc

    # ---- construction -------------------------------------------------
    @classmethod
    def from_dict(cls, doc):
        return cls(doc)

    @classmethod
    def from_file(cls, path):
        with open(path) as fh:
            return cls(json.load(fh))

    # ---- validation ---------------------------------------------------
    def validate(self):
        """Return a list of human-readable problems ([] == clean)."""
        errs = []
        doc = self.doc
        if doc.get("abstract_model") != MODEL:
            errs.append(f"abstract_model must be '{MODEL}', got {doc.get('abstract_model')!r}")
        seen_graph_ids = set()
        for g in doc.get("graphs", []):
            gid = g.get("namespace", "<no-namespace>")
            if gid in seen_graph_ids:
                errs.append(f"duplicate namespace {gid!r}")
            seen_graph_ids.add(gid)
            worlds = {w["id"] for w in g.get("worlds", [])}
            for w in g.get("worlds", []):
                if w.get("origin") not in ORIGIN_KINDS:
                    errs.append(f"[{gid}] world {w['id']}: unknown origin {w.get('origin')!r}")
            for ev in g.get("events", []):
                if ev.get("kind") not in EVENT_KINDS:
                    errs.append(f"[{gid}] event {ev['id']}: unknown kind {ev.get('kind')!r}")
                if ev.get("universe") not in worlds:
                    errs.append(f"[{gid}] event {ev['id']} cites unknown universe {ev.get('universe')!r}")
            for sp in g.get("splits", []):
                if sp.get("event") not in {e["id"] for e in g.get("events", [])}:
                    errs.append(f"[{gid}] split {sp.get('event')} references unknown event")
                for sign, out in (sp.get("outcomes") or {}).items():
                    if sign not in ("+", "-"):
                        errs.append(f"[{gid}] split {sp.get('event')}: outcome sign {sign!r} invalid")
                    if out.get("universe") not in worlds:
                        errs.append(f"[{gid}] split {sp.get('event')} outcome {sign}: unknown universe {out.get('universe')!r}")
            for tr in g.get("transfers", []):
                if tr.get("from", {}).get("universe") not in worlds or \
                   tr.get("to", {}).get("universe") not in worlds:
                    errs.append(f"[{gid}] transfer {tr.get('id')}: endpoint universe unknown")
            route = g.get("route") or {}
            for v in route.get("visits", []):
                if v.get("universe") not in worlds:
                    errs.append(f"[{gid}] route visit {v.get('id')} cites unknown universe {v.get('universe')!r}")
            for f in g.get("fates", []):
                if f.get("status") not in FATE_STATUSES:
                    errs.append(f"[{gid}] fate {f.get('id')}: unknown status {f.get('status')!r}")
        return errs

    # ---- helpers ------------------------------------------------------
    def graph(self, namespace=None):
        gs = self.doc.get("graphs", [])
        if namespace:
            return next((g for g in gs if g["namespace"] == namespace), None)
        return gs[0] if gs else None

    def world_label(self, g, wid):
        w = next((x for x in g.get("worlds", []) if x["id"] == wid), None)
        return w["label"] if w else wid

    def origin_text(self, w):
        kind = w.get("origin", "unknown")
        if kind == "born" and w.get("born"):
            b = w["born"]
            return f"born @{b.get('event')} ({b.get('parent')} {b.get('tine')})"
        return kind + (" · off-chart" if w.get("ancestry") == "off_chart" else "")

    # ---- the abstract TEXTUAL representation --------------------------
    def to_text(self):
        """Render the model as clean, human-readable abstract text.

        This is the canonical 'abstract textual representation' — pure
        structure, no drawing. It is not a chart; it is the thing a chart is
        a projection of.
        """
        doc = self.doc
        L = []
        L.append(doc.get("title", "(untitled)"))
        if doc.get("subtitle"):
            L.append(doc.get("subtitle"))
        prof = doc.get("profile", {})
        prof_s = " · ".join(f"{k}={v}" for k, v in prof.items() if v)
        if prof_s:
            L.append("profile: " + prof_s)
        if doc.get("footer"):
            L.append("note: " + doc["footer"])
        L.append("")
        for g in doc.get("graphs", []):
            L.append(f"# Graph {g['namespace']} — {g.get('title','')}".strip())
            L.append("")
            L.append("Worlds:")
            for w in g.get("worlds", []):
                L.append(f"  {w['id']:<8} {w.get('label',''):<40} [{self.origin_text(w)}]")
            L.append("")
            L.append("Events (story order):")
            for e in sorted(g.get("events", []), key=lambda x: x.get("order", 0)):
                cite = self._cite_text(e.get("cite"))
                L.append(f"  {e.get('order',0):>3}  {e.get('universe',''):<7} {e.get('kind',''):<8} {e.get('label','')}{('  ' + cite) if cite else ''}")
            L.append("")
            L.append("Splits:")
            for sp in g.get("splits", []):
                out_txt = []
                for sign in ("+", "-"):
                    o = (sp.get("outcomes") or {}).get(sign)
                    if o:
                        out_txt.append(f"{sign}={self.world_label(g, o['universe'])}")
                L.append(f"  {sp.get('event'):<8} ({sp.get('cause','branch')}) -> " + " | ".join(out_txt))
            L.append("")
            L.append("Transfers:")
            for tr in g.get("transfers", []):
                L.append(f"  {tr.get('id','?'):<8} {self.world_label(g, tr.get('from',{}).get('universe'))} -> {self.world_label(g, tr.get('to',{}).get('universe'))}   ({tr.get('mechanism','')})")
            route = g.get("route") or {}
            L.append("")
            L.append(f"Route ({route.get('traveller','?')}):")
            vis = route.get("visits", [])
            for i, v in enumerate(vis):
                L.append(f"  {i+1}. {self.world_label(g, v.get('universe'))}  entry={v.get('entry')} exit={v.get('exit')}")
            L.append("")
            L.append("Fates:")
            for f in g.get("fates", []):
                L.append(f"  {f.get('id','?'):<20} {self.world_label(g, f.get('universe'))} @ {f.get('event')}  {f.get('status')}")
            if g.get("assumptions"):
                L.append("")
                L.append("Assumptions:")
                for a in g["assumptions"]:
                    L.append("  * " + a)
            L.append("")
        return "\n".join(L).rstrip()

    @staticmethod
    def _cite_text(cite):
        if not cite:
            return ""
        src = cite.get("source", "")
        loc = cite.get("locator") or cite.get("page") or cite.get("scene") or ""
        st = cite.get("status", "")
        parts = [p for p in (src, loc) if p]
        out = "[cite: " + " · ".join(parts)
        if st and st != "resolved":
            out += f" · {st}"
        return out + "]"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: abstract_model.py FILE.json [namespace]", file=sys.stderr)
        sys.exit(2)
    story = AbstractStory.from_file(sys.argv[1])
    errs = story.validate()
    if errs:
        for e in errs:
            print("ERR " + e, file=sys.stderr)
        sys.exit(2)
    print(story.to_text())
