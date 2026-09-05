#!/usr/bin/env python3
"""Unit tests for the abstract engine: authoring, validation, profiles, import.

Dependency-free (plain asserts). Run:  python3 tests/test_abstract.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from abstract_model import AbstractStory  # noqa: E402
from author import Author  # noqa: E402
from profiles import resolve  # noqa: E402
from to_abstract import convert  # noqa: E402

_fails = 0


def check(name, cond, detail=""):
    global _fails
    if cond:
        print(f"PASS {name}")
    else:
        _fails += 1
        print(f"FAIL {name} {detail}")


def doc_from(profile, worlds=1, merges=0, extra_params=None):
    a = Author("Test film", profile=profile if isinstance(profile, str) else "P1")
    if isinstance(profile, dict) and extra_params:
        pass
    a.graph("G", "Test graph")
    a.add_world("U1", "The initial timeline", "initial")
    if worlds > 1:
        a.add_world("U2", "A second world", "preexisting", ancestry="off_chart")
    a.add_event("e-start", "start", "U1", 0, "It begins")
    d = a.emit()
    d["graphs"][0]["merges"] = merges
    return d


def test_author_valid():
    a = Author("MY FILM — Test", profile="P1")
    a.graph("G", "Test story", ensure=True)
    a.add_world("U1", "The initial timeline", "initial")
    a.add_world("J-", "The dying tine", "born", born={"event": "e-split", "parent": "U1", "tine": "-"})
    a.add_event("e-start", "start", "U1", 0, "It begins", cite={"source": "s", "locator": "1", "status": "unavailable"})
    a.add_event("e-split", "split", "U1", 5, "The split")
    a.add_split("e-split", "branch", "ben-mind", "U1", "continues",
                a.add_outcome("U1", "e-start", "continues", [("i1", "continues", "survives")]),
                a.add_outcome("J-", "e-start", "born", [("i2", "dies", "dies")]))
    a.add_traveller("ben-mind", "ben")
    a.set_route("ben-mind",
                [{"id": "v1", "traveller": "ben-mind", "universe": "U1", "entry": "e-start", "exit": "e-start", "passes": []}],
                [])
    a.add_fate("f-i2", "J-", "i2", "e-split", "dead")
    d = a.emit()
    errs = AbstractStory.from_dict(d).validate()
    check("author valid model → clean", errs == [], str(errs))
    check("author emits text with title", "MY FILM" in a.to_text())


def test_unknown_profile_rejected():
    d = doc_from("P1")
    d["profile"] = {"name": "bogus", "params": {}}
    errs = AbstractStory.from_dict(d).validate()
    check("unknown profile rejected", any("unknown profile 'bogus'" in e for e in errs), str(errs))


def test_unknown_param_rejected():
    d = doc_from("P1")
    d["profile"] = {"name": "P1", "params": {"not_a_param": "x"}}
    errs = AbstractStory.from_dict(d).validate()
    check("unknown parameter rejected", any("unknown parameter 'not_a_param'" in e for e in errs), str(errs))


def test_merge_forbidden():
    d = doc_from("P1", merges=1)
    errs = AbstractStory.from_dict(d).validate()
    check("merge forbidden (merges>0) rejected", any("forbids actual merge" in e for e in errs), str(errs))


def test_revisions_not_coexisting():
    d = doc_from("P1")
    d["profile"] = {"name": "P1", "params": resolve({"name": "P1", "params": {"history_model": "revisions", "coexistence": "coexisting"}})}
    errs = AbstractStory.from_dict(d).validate()
    check("revisions+coexisting contradiction rejected", any("revisions cannot be coexistence" in e for e in errs), str(errs))


def test_iterations_single_world():
    d = doc_from("edge-of-tomorrow", worlds=2)
    errs = AbstractStory.from_dict(d).validate()
    check("iterations with multiple worlds rejected", any("iterations but 2 worlds" in e for e in errs), str(errs))


def test_custom_profile_resolution():
    p = resolve({"name": "P1", "params": {"axis": "world_time", "turnstiles": "both_signs"}})
    check("custom profile = preset + overrides", p["axis"] == "world_time" and p["turnstiles"] == "both_signs" and p["history_model"] == "universes", str(p))


def test_warnings_signal_bootstrap():
    a = Author("W", profile="interstellar")
    a.graph("G", "g").add_world("E", "The timeline", "initial")
    a.add_event("e-start", "start", "E", 0, "start")
    notes = AbstractStory.from_dict(a.emit()).warnings()
    check("signal warning surfaced", any("signal transports no body" in n for n in notes), str(notes))


def test_import_fixture_clean():
    path = os.path.join(ROOT, "fixtures", "bens_story.json")
    doc = json.load(open(path))
    abstract = convert(doc)
    errs = AbstractStory.from_dict(abstract).validate()
    check("import bens_story fixture → clean", errs == [], str(errs))
    check("imported profile has expanded params", "universes" in abstract["profile"]["params"].get("history_model", ""), str(abstract.get("profile")))


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        try:
            t()
        except Exception as exc:  # noqa: BLE001
            global _fails
            _fails += 1
            print(f"FAIL {t.__name__} threw: {exc!r}")
    print(f"\n{len(tests) - _fails}/{len(tests)} tests passed")
    sys.exit(1 if _fails else 0)


if __name__ == "__main__":
    main()
