#!/usr/bin/env python3
"""timeline_compile.py — compile a human-owned scene-allocation file into the
JSON that universe_graph.py renders. Adds NOTHING of its own except plumbing.

Film-agnostic: every string that was movie-specific in the original project is
a flag here. Edit YOUR allocation file; never hand-edit the compiled JSON.

SYNTAX (in the allocation file, '#' starts a comment):
  lanes: FAM, WHERED, HER, OPEN     lane order LEFT to RIGHT (thread flows RIGHT -> LEFT)
  label <id>: <pretty name>         name shown on the lane
  already-running: HER, FAM         worlds that exist before the protagonist arrives
  <id>: <ranges>                    protagonist's scenes in that world, e.g.  HER: 78-114
  pulls: 78, 114, 184               the crossing scenes, in STORY ORDER. Crossing i goes
                                    from the (i+1)th-last lane into the (i)th-last lane:
                                    with 4 lanes: 78: OPEN->HER, 114: HER->WHERED, 184: WHERED->FAM
  split: 10                         a split that is NOT a crossing, drawn in its lane
  key: <id>: <n>, <n>               beat dots at those scenes (labelled 'scene N')
  beats: key | all | <number>       beat mode (default: 4 evenly spread)
  thread: <text>                    the route line under the title

Usage:
  python3 timeline_compile.py allocations.txt -o story.universes.json \
      --title "MY FILM — One Man's Story" \
      --split-name 10:"The crash — the worlds split" \
      && python3 tools/universe_graph.py story.universes.json -o story.png
"""
import json, re, sys, argparse
from pathlib import Path


def parse_alloc(path):
    g = {"lanes": [], "labels": {}, "running": [], "ranges": {}, "splits": [],
         "pulls": [], "beats": "4", "thread": "", "keys": {}}
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        keep = s.lower().startswith(("label ", "thread:"))
        line = s if keep else s.split("#")[0].strip()
        if not line:
            continue
        if line.startswith("lanes:"):
            g["lanes"] = [x.strip() for x in line.split(":", 1)[1].split(",") if x.strip()]
        elif line.startswith("label "):
            _, lid, txt = line.split(" ", 2)
            g["labels"][lid.strip()] = txt.strip()
        elif line.startswith("already-running:"):
            g["running"] = [x.strip() for x in line.split(":", 1)[1].split(",") if x.strip()]
        elif line.startswith("pulls:"):
            g["pulls"] = [int(x) for x in re.findall(r"\d+", line.split(":", 1)[1])]
        elif line.startswith("split:"):
            g["splits"].append(int(line.split(":", 1)[1].strip()))
        elif line.startswith("beats:"):
            g["beats"] = line.split(":", 1)[1].strip()
        elif line.startswith("thread:"):
            g["thread"] = line.split(":", 1)[1].strip()
        elif line.startswith("key:"):
            body = line.split(":", 1)[1]
            lid = line.split(":", 1)[0].replace("key", "").strip()
            g["keys"][lid] = [int(x) for x in re.findall(r"\d+", body)]
        else:
            m = re.match(r"^([A-Za-z0-9_*]+)\s*:\s*([\d\-, ]+)$", line)
            if m:
                rng = []
                for part in m.group(2).split(","):
                    part = part.strip()
                    if "-" in part:
                        lo, hi = part.split("-"); rng += [int(lo), int(hi)]
                    elif part:
                        n = int(part); rng += [n, n]
                g["ranges"][m.group(1)] = rng
    return g


def main():
    ap = argparse.ArgumentParser(description="Compile a scene-allocation file into universe-chart JSON.")
    ap.add_argument("alloc", help="scene-allocation .txt (see syntax in this file's docstring)")
    ap.add_argument("-o", "--out", default="story.universes.json")
    ap.add_argument("--title", default="UNIVERSE TIMELINE")
    ap.add_argument("--subtitle", default="Split circles carry the scene number of the split · * = already running, ancestry off-chart")
    ap.add_argument("--footer", default="Compiled from a scene-allocation file — edit that file, then recompile.")
    ap.add_argument("--canvas", default="2800x3600", help="WxH, e.g. 2800x3600")
    ap.add_argument("--split-name", action="append", default=[],
                    metavar="N:TEXT", help="caption for split N (repeatable)")
    ap.add_argument("--stub-template", default="{scene}B — HE DIES",
                    help="death-stub title; {scene} placeholder")
    ap.add_argument("--stub-sub-template", default="the tine where he dies at split #{scene}",
                    help="death-stub subtitle; {scene} placeholder")
    ap.add_argument("--join-label-template", default="he enters {lane}",
                    help="join label; {lane} placeholder")
    ap.add_argument("--opening-title", default="OPENING — THE OPENING UNIVERSE")
    ap.add_argument("--opening-body", default="Where the story begins.")
    ap.add_argument("--opening-cite", default="")
    ap.add_argument("--legend", action="append", default=[],
                    help="legend line under the chart (repeatable)")
    a = ap.parse_args()

    g = parse_alloc(Path(a.alloc))
    errs = []
    lanes = g["lanes"]
    if not lanes:
        errs.append("no lanes: line")
    for lid in lanes:
        if lid not in g["ranges"]:
            errs.append(f"no scene range for lane '{lid}'")
    k = len(lanes) - 1
    if len(g["pulls"]) != k:
        errs.append(f"pulls: needs exactly {k} scenes for {len(lanes)} lanes (one per crossing), got {len(g['pulls'])}")
    if errs:
        print("ALLOCATION ERRORS:")
        for e in errs:
            print("  -", e)
        sys.exit(2)

    split_names = {}
    for part in a.split_name:
        if ":" in part:
            kk, vv = part.split(":", 1)
            split_names[int(kk)] = vv.strip()

    w, h = (int(x) for x in a.canvas.lower().split("x"))

    # thread flows RIGHT -> LEFT: crossing i (story order) = lanes[n-1-i] -> lanes[n-2-i]
    n = len(lanes)
    bounds = []
    for i, pull in enumerate(g["pulls"]):
        bounds.append((pull, lanes[n - 1 - i], lanes[n - 2 - i]))

    out = {
        "_doc": "COMPILED from %s via timeline_compile.py. Do not hand-edit; edit the allocation file and recompile." % Path(a.alloc).name,
        "meta": {
            "title": a.title,
            "subtitle": a.subtitle,
            "thread_label": g["thread"] or "THE THREAD",
            "footer": a.footer,
            "canvas": [w, h],
        },
        "lanes": [{"id": lid, "label": g["labels"].get(lid, lid)} for lid in lanes],
        "nodes": [{"id": "U1", "lane": lanes[-1], "title": a.opening_title,
                   "body": a.opening_body, "cite": a.opening_cite}],
        "lanes_content": {}, "splits": {}, "stubs": {}, "joins": {}, "thread": [], "legend": [],
    }
    if a.opening_cite == "":
        del out["nodes"][0]["cite"]

    for (pull, src, tgt) in bounds:
        out["splits"][str(pull)] = {"letter": str(pull), "caption": split_names.get(pull, f"SPLIT AT #{pull}")}
        out["joins"][f"join-{pull}"] = {"from_split": str(pull), "to_lane": tgt, "side": "left",
                                        "label": a.join_label_template.replace("{lane}", g["labels"].get(tgt, tgt))}
    for s in g["splits"]:
        out["splits"][str(s)] = {"letter": str(s), "caption": split_names.get(s, f"SPLIT AT #{s}")}

    for lid in lanes:
        rng = g["ranges"][lid]; lo, hi = rng[0], rng[-1]
        star = "*" if lid in g["running"] else ""
        content = []
        if lid == lanes[-1]:
            content.append({"node": "U1"})
        if star:
            content.append({"laneborn": {"from_split": None,
                "chip": f"{g['labels'].get(lid, lid)} — ALREADY RUNNING",
                "note": "this world began long before the chart"}})
        outgoing = [(p, s, t) for (p, s, t) in bounds if s == lid]
        incoming = [(p, s, t) for (p, s, t) in bounds if t == lid]
        nsplits = [s for s in g["splits"] if lo <= s <= hi]
        nsset = set(nsplits)
        if g["beats"] == "key" and g["keys"].get(lid):
            beats = [x for x in g["keys"][lid]
                     if lo <= x <= hi and x not in nsset and x not in [p for p, _, _ in outgoing]]
        elif g["beats"].isdigit():
            nb = int(g["beats"]); step = max(1, (hi - lo) // (nb + 1))
            beats = list(range(lo + step, hi, step))[:nb]
            for p, s, t in outgoing:
                if lo <= p <= hi:
                    beats = [b for b in beats if b < p]
        else:
            beats = []
        events = []
        for p, s, t in incoming: events.append((p, "join", p))
        for p, s, t in outgoing: events.append((p, "split", p))
        for s in nsplits:        events.append((s, "nsplit", s))
        for b in beats:          events.append((b, "beat", b))
        for pos, kind, val in sorted(events):
            if kind == "join":     content.append({"join": f"join-{val}"})
            elif kind == "split":  content.append({"split": str(val)})
            elif kind == "nsplit": content.append({"split": str(val)})
            else:                  content.append({"beat": f"scene {val}", "cite": f"#{val}"})
        if outgoing:
            content.append({"stub": f"stub-{outgoing[0][0]}"})
            content.append({"chip": f"{g['labels'].get(lid, lid)} — RUNS ON", "dim": True})
            content.append({"abandon": 140})
        out["lanes_content"][lid] = content

    for (pull, src, tgt) in bounds:
        out["stubs"][f"stub-{pull}"] = {
            "title": a.stub_template.replace("{scene}", str(pull)),
            "sub": a.stub_sub_template.replace("{scene}", str(pull)),
        }

    out["thread"] = ["U1"] + [f"join-{p}" for p, _, _ in bounds] + ["ENDING"]
    out["legend"] = list(a.legend)

    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"compiled {a.out}")
    for (pull, src, tgt) in bounds:
        print(f"  split #{pull}: {g['labels'].get(src, src)}  ->  {g['labels'].get(tgt, tgt)}")


if __name__ == "__main__":
    main()
