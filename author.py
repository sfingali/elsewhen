#!/usr/bin/env python3
"""Author an abstract universe-timeline model programmatically.

The abstract representation is a plain structure — worlds, events, splits,
transfers, route, fates, citations — with no visual vocabulary. This builder
lets you construct one directly and emit it as JSON or abstract text, without
hand-writing a legacy schema_v2 document. (To import an existing document, use
to_abstract.py.)

Every method is a fluent no-op on missing data and validates on emit() via the
AbstractStory validator.
"""

import json
import sys

from abstract_model import AbstractStory
from profiles import DEFAULTS, resolve


class Author:
    """A fluent builder for the abstract timeline model."""

    def __init__(self, title, subtitle="", footer="", profile=None):
        self.doc = {
            "abstract_model": "universe-timeline/1.0",
            "title": title,
            "subtitle": subtitle,
            "footer": footer,
            "profile": {},
            "characters": [],
            "travellers": [],
            "namespaces": [],
            "sources": [],
            "graphs": [],
        }
        if profile:
            self.set_profile(profile)
        self._g = None

    # ---- document / profile ------------------------------------------
    def set_profile(self, profile):
        """profile: a preset name ('P1') or a block {name, rules, params}."""
        if isinstance(profile, dict):
            prof = dict(profile)
            prof.setdefault("params", resolve(prof.get("name") or prof.get("base")))
            self.doc["profile"] = prof
        else:
            self.doc["profile"] = {"name": profile, "params": resolve(profile)}
        return self

    def set_params(self, **overrides):
        """Tune the profile's parameter set (preset + overrides)."""
        prof = self.doc.get("profile", {})
        base = prof.get("name")
        if base:
            merged = dict(prof.get("params", {}))
            merged.update(overrides)
            prof["params"] = resolve({"name": base, "params": merged})
            self.doc["profile"] = prof
        return self

    def add_character(self, cid, label):
        self.doc["characters"].append({"id": cid, "label": label})
        return self

    def add_traveller(self, tid, character):
        self.doc["travellers"].append({"id": tid, "character": character})
        return self

    def add_namespace(self, nid, label):
        self.doc["namespaces"].append({"id": nid, "label": label})
        return self

    def add_source(self, sid, title, kind="canon_statement", text=""):
        self.doc["sources"].append({"id": sid, "title": title, "kind": kind, "text": text})
        return self

    # ---- graph --------------------------------------------------------
    def graph(self, namespace, title="", ensure=False):
        """Create (or return) a graph with the given namespace."""
        if ensure:
            for g in self.doc["graphs"]:
                if g["namespace"] == namespace:
                    self._g = g
                    return self
        g = {"namespace": namespace, "title": title, "worlds": [], "events": [],
             "segments": [], "beats": [], "splits": [], "transfers": [], "merges": 0,
             "route": {"traveller": None, "visits": [], "links": []},
             "fates": [], "assumptions": [], "evidence": []}
        self.doc["graphs"].append(g)
        self._g = g
        return self

    def _g_or(self):
        if self._g is None:
            self.graph("G")
        return self._g

    def add_world(self, wid, label, origin="initial", born=None, ancestry=None):
        w = {"id": wid, "label": label, "origin": origin}
        if origin == "born" and born:
            w["born"] = born
        if ancestry:
            w["ancestry"] = ancestry
        self._g_or()["worlds"].append(w)
        return self

    def add_event(self, eid, kind, universe, order, label, cite=None):
        ev = {"id": eid, "kind": kind, "universe": universe, "order": order, "label": label}
        if cite:
            ev["cite"] = cite
        self._g_or()["events"].append(ev)
        return self

    def add_split(self, event, cause, traveller, source_universe, source_disposition, plus, minus):
        sp = {"event": event, "cause": cause, "automatic": True, "traveller": traveller,
              "source_disposition": source_disposition, "source_universe": source_universe,
              "outcomes": {"+": plus, "-": minus}}
        self._g_or()["splits"].append(sp)
        return self

    def add_outcome(self, universe, entry, universe_outcome, instances=None):
        return {"universe": universe, "entry": entry, "universe_outcome": universe_outcome,
                "instances": [{"instance": i, "outcome": o, "fate": f} for (i, o, f) in instances or []]}

    def add_transfer(self, tid, traveller, from_u, exit_ev, to_u, entry_ev, mechanism, relation="different_universes"):
        self._g_or()["transfers"].append({
            "id": tid, "traveller": traveller,
            "from": {"universe": from_u, "exit": exit_ev},
            "to": {"universe": to_u, "entry": entry_ev},
            "mechanism": mechanism, "relation": {"kind": relation}})
        return self

    def add_visit(self, vid, traveller, universe, entry, exit, passes=None):
        self._g_or()["route"]["visits"].append(
            {"id": vid, "traveller": traveller, "universe": universe, "entry": entry,
             "exit": exit, "passes": passes or []})
        return self

    def add_link(self, fr, to, kind, via=None, tine=None):
        d = {"from": fr, "to": to, "kind": kind}
        if via:
            d["via"] = via
        if tine:
            d["tine"] = tine
        self._g_or()["route"]["links"].append(d)
        return self

    def set_route(self, traveller, visits, links):
        self._g_or()["route"] = {"traveller": traveller, "visits": visits, "links": links}
        return self

    def add_fate(self, fid, universe, instance, event, status, cite=None):
        f = {"id": fid, "universe": universe, "instance": instance, "event": event, "status": status}
        if cite:
            f["cite"] = cite
        self._g_or()["fates"].append(f)
        return self

    def add_assumption(self, text):
        self._g_or()["assumptions"].append(text)
        return self

    # ---- output -------------------------------------------------------
    def emit(self):
        return self.doc

    def validate(self):
        return AbstractStory.from_dict(self.emit()).validate()

    def warnings(self):
        return AbstractStory.from_dict(self.emit()).warnings()

    def to_text(self):
        return AbstractStory.from_dict(self.emit()).to_text()

    def to_file(self, path):
        with open(path, "w") as fh:
            json.dump(self.emit(), fh, indent=2)
            fh.write("\n")
        return path


if __name__ == "__main__":
    print("""author: programmatic builder for the abstract timeline model.

  from author import Author
  st = Author("MY FILM", profile="P1")
  st.graph("G", "My story")
  st.add_world("U1", "The initial timeline", "initial")
  st.add_event("e-start", "start", "U1", 0, "It begins")
  st.set_profile("P1").set_params(axis="world_time")
  print(st.to_text())
""")
