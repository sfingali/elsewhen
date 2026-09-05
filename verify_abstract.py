#!/usr/bin/env python3
"""Verify the abstract engine: convert every fixture to the abstract model,
validate it, and emit its abstract text representation."""

import glob
import json
import os
import sys

from abstract_model import AbstractStory
from to_abstract import convert

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = sorted(glob.glob(os.path.join(HERE, "fixtures", "*.json")))
OUT = os.path.join(HERE, "build")


def main():
    os.makedirs(os.path.join(OUT, "abstract"), exist_ok=True)
    fails = 0
    for path in FIXTURES:
        name = os.path.splitext(os.path.basename(path))[0]
        with open(path) as fh:
            doc = json.load(fh)
        abstract = convert(doc)
        story = AbstractStory.from_dict(abstract)
        errs = story.validate()
        base = os.path.join(OUT, "abstract", name)
        with open(base + ".json", "w") as fh:
            json.dump(abstract, fh, indent=2)
            fh.write("\n")
        for target in ("text",):
            txt = story.to_text()
            ext = {"text": "txt"}[target]
            with open(base + "." + ext, "w") as fh:
                fh.write(txt + "\n")
        if errs:
            fails += 1
            print(f"FAIL {name}: {len(errs)} validation problem(s)")
            for e in errs[:6]:
                print("   " + e)
        else:
            nw = sum(len(g.get("worlds", [])) for g in abstract.get("graphs", []))
            p = story.profile_params()
            p_s = " ".join(f"{k}={v if not isinstance(v, list) else '/'.join(v)}" for k, v in p.items())
            print(f"PASS {name}: {nw} worlds · params[ {p_s} ]")
            print(f"          -> wrote json/txt")
    print(f"\n{len(FIXTURES) - fails}/{len(FIXTURES)} fixtures converted cleanly")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
