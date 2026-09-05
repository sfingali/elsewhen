#!/usr/bin/env python3
"""Verify the abstract engine: convert every fixture to the abstract model,
validate it, and render every projection (text, dot, mermaid, markdown)."""

import glob
import json
import os
import sys

from abstract_model import AbstractStory
from projections import render
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
        for target in ("text", "dot", "mermaid", "markdown"):
            txt = render(story, target)
            ext = {"text": "txt", "dot": "dot", "mermaid": "mmd", "markdown": "md"}[target]
            with open(base + "." + ext, "w") as fh:
                fh.write(txt + "\n")
        if errs:
            fails += 1
            print(f"FAIL {name}: {len(errs)} validation problem(s)")
            for e in errs[:6]:
                print("   " + e)
        else:
            nw = len(abstract.get("worlds", []) or [])
            nw = sum(len(g.get("worlds", [])) for g in abstract.get("graphs", []))
            print(f"PASS {name}: clean · {nw} worlds · wrote json/txt/dot/mmd/md")
    print(f"\n{len(FIXTURES) - fails}/{len(FIXTURES)} fixtures converted cleanly")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
