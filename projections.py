#!/usr/bin/env python3
"""Projections of the abstract model.

Every function here takes an AbstractStory (the pure semantic core) and returns
TEXT. None of them mutate the model, and none of them are the model — they are
downstream *renderings*, swappable and one-of-many. The visual grammar of a
particular chart (the PIL renderer / studio) is just one more projection and
lives with it; here we keep only pure, dependency-free projections so the
engine never needs PIL.

targets: dot (graphviz), mermaid, markdown, text (see AbstractStory.to_text).
"""

import binascii

# graphviz / mermaid only need an id-safe token; labels are arbitrary text.
def _id(token):
    return "n_" + binascii.hexlify(token.encode()).decode()[:12]


def _world_node_id(wid):
    return "W_" + _id(wid)


def to_dot(story):
    """Graphviz DOT — the pure structural graph. Feed to dot/neato/circo. Any style."""
    lines = ["digraph timeline {", "  rankdir=TB;", "  node [shape=box, style=\"rounded, filled\"];"]
    for g in story.doc.get("graphs", []):
        ns = _id(g["namespace"])
        lines.append(f"  subgraph cluster_{ns} {{")
        lines.append(f"    label=\"{g['namespace']} — {g.get('title','')}\";")
        # world nodes
        for w in g.get("worlds", []):
            o = story.origin_text(w)
            fill = {'initial': '#e8f0fe', 'born': '#fdf3d0', 'preexisting': '#e6f4ea', 'unknown': '#f5f5f5'}.get(w.get("origin"), '#f5f5f5')
            lines.append(f"    {_world_node_id(w['id'])} [label=\"{w['id']}: {w.get('label','')}\\n[{o}]\", fillcolor=\"{fill}\"];")
        # splits: edges parent universe -> outcome universe
        for sp in g.get("splits", []):
            ev = sp.get("event", "?")
            for sign in ("+", "-"):
                out = (sp.get("outcomes") or {}).get(sign)
                if out and out.get("universe"):
                    lines.append(f"    {_world_node_id(sp.get('source_universe',''))} -> {_world_node_id(out['universe'])} "
                                 f"[label=\"{sign} ({ev})\", style=\"{'solid' if sign=='+' else 'dashed'}\", color=\"#a05050\"];")
        # transfers: source universe -> target universe
        for tr in g.get("transfers", []):
            f = (tr.get("from") or {}).get("universe")
            t = (tr.get("to") or {}).get("universe")
            if f and t:
                lines.append(f"    {_world_node_id(f)} -> {_world_node_id(t)} "
                             f"[label=\"{tr.get('traveller','?')} [{tr.get('mechanism','')}]\", color=\"#2f7d4f\", style=\"bold\"];")
        lines.append("  }")
    lines.append("}")
    return "\n".join(lines)


def to_mermaid(story):
    """Mermaid flowchart. Paste into mermaid.live / GitHub. Any style target."""
    lines = ["flowchart TD"]
    for g in story.doc.get("graphs", []):
        lines.append(f"  subgraph {_id(g['namespace'])}[\"{g['namespace']} — {g.get('title','')}\"]")
        for w in g.get("worlds", []):
            lines.append(f"    {_world_node_id(w['id'])}[\"{w['id']}: {w.get('label','')}\"]")
        for sp in g.get("splits", []):
            ev = sp.get("event", "?")
            for sign in ("+", "-"):
                out = (sp.get("outcomes") or {}).get(sign)
                if out and out.get("universe"):
                    style = "|." if sign == "-" else "|>"
                    lines.append(f"    {_world_node_id(sp.get('source_universe',''))} {style} {_world_node_id(out['universe'])}|{sign} {ev}|")
        for tr in g.get("transfers", []):
            f = (tr.get("from") or {}).get("universe")
            t = (tr.get("to") or {}).get("universe")
            if f and t:
                lines.append(f"    {_world_node_id(f)} == \"{tr.get('traveller','?')} [{tr.get('mechanism','')}]\" ==> {_world_node_id(t)}")
        lines.append("  end")
    return "\n".join(lines)


def to_markdown(story):
    """Markdown narrative of the structure — readable, cite-aware, no drawing."""
    L = ["# " + story.doc.get("title", "(untitled)")]
    if story.doc.get("subtitle"):
        L.append("\n> " + story.doc["subtitle"])
    prof = story.doc.get("profile", {})
    if prof:
        L.append("\n*Profile:* " + ", ".join(f"`{k}={v}`" for k, v in prof.items() if v))
    for g in story.doc.get("graphs", []):
        L.append(f"\n## {g['namespace']} — {g.get('title','')}")
        L.append("\n### Worlds")
        L.append("| id | world | origin |")
        L.append("|----|-------|--------|")
        for w in g.get("worlds", []):
            L.append(f"| {w['id']} | {w.get('label','')} | {story.origin_text(w)} |")
        L.append("\n### Splits")
        for sp in g.get("splits", []):
            outs = "; ".join(f"{sign}: {story.world_label(g, o['universe'])}" for sign, o in (sp.get("outcomes") or {}).items())
            L.append(f"- `{sp.get('event')}` ({sp.get('cause','branch')}) — " + outs)
        L.append("\n### Transfers")
        for tr in g.get("transfers", []):
            L.append(f"- {tr.get('traveller','?')}: {story.world_label(g, (tr.get('from') or {}).get('universe'))} → {story.world_label(g, (tr.get('to') or {}).get('universe'))} (`{tr.get('mechanism','')}`)")
        route = g.get("route") or {}
        L.append(f"\n### Route — {route.get('traveller','?')}")
        for i, v in enumerate(route.get("visits", []), 1):
            L.append(f"{i}. **{story.world_label(g, v.get('universe'))}** (in `{v.get('entry')}`, out `{v.get('exit')}`)")
        L.append("\n### Fates")
        for f in g.get("fates", []):
            L.append(f"- {f.get('id','?')} — {story.world_label(g, f.get('universe'))} @ `{f.get('event')}` → **{f.get('status')}**")
        if g.get("assumptions"):
            L.append("\n### Assumptions")
            for a in g["assumptions"]:
                L.append(f"- {a}")
        L.append("")
    return "\n".join(L).rstrip()


# Dispatch table. Add a projector here to get another output form.
PROJECTORS = {
    "dot": to_dot,
    "mermaid": to_mermaid,
    "markdown": to_markdown,
}


def render(story, target):
    """Render an AbstractStory into the named projection. Returns text or None."""
    if target == "text":
        return story.to_text()
    fn = PROJECTORS.get(target)
    return fn(story) if fn else None


ALL_TARGETS = list(PROJECTORS) + ["text"]
