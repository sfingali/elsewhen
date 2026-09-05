#!/usr/bin/env python3
"""Interpretation profiles as explicit parameter sets.

A profile is a named bundle of *semantic* interpretation parameters — how this
film's ontology behaves (branching vs overwrite, universes vs revisions vs
iterations, time mechanics, joined-world backpropagation, etc.). The name is
only a convenience handle; the parameters are the real contract. To build a
custom profile, take a preset bundle and override any one parameter — no new
magic string required.

Every parameter here is semantic. None describe how anything is drawn.
"""

# The full vocabulary of interpretation levers.
DEFAULTS = {
    "history_model": "universes",        # universes | revisions | iterations
    "branching": "branch",               # branch | overwrite | undeclared
    "coexistence": "coexisting",         # coexisting | single_active | undeclared
    "time_mechanics": ["body", "consciousness"],  # subset of body|memory|consciousness|signal
    "joined_worlds": "preexist",         # preexist | not_preexist | undeclared
    "turnstiles": "none",                # both_signs | single_sign | none
    "protagonist_scope": "singular",     # singular | multiple
    "axis": "story_order",               # story_order | world_time
    "validation": "evidence_pending",    # evidence_pending | resolved | observation_only
    "merges": "forbidden",               # forbidden | apparent_reset | siblings
    "genealogy": "acyclic",              # acyclic | bootstrap_cycles
}

# Named profile parameter sets. Each is a full expansion of DEFAULTS semantics
# (a convenient bundle, not a hidden dictionary). Grounded in the ontology:
# THE WAIF branches parallel universes; BTTF2 supersedes revisions of one world;
# Groundhog loops one world with memory; Dark ties era lanes + genealogy cycles;
# Steins;Gate rewrites divergence lines; Tenet runs inverted strands + turnstiles.
PROFILES = {
    "P1": dict(DEFAULTS, history_model="universes", branching="branch",
               coexistence="coexisting", time_mechanics=["body", "consciousness"],
               joined_worlds="preexist", turnstiles="none",
               protagonist_scope="singular", axis="story_order",
               validation="evidence_pending", merges="forbidden", genealogy="acyclic"),
    "P2": dict(DEFAULTS, history_model="revisions", branching="overwrite",
               coexistence="single_active", time_mechanics=["body"],
               joined_worlds="preexist", turnstiles="none",
               protagonist_scope="singular", axis="story_order",
               validation="evidence_pending", merges="forbidden", genealogy="acyclic"),
    "P3": dict(DEFAULTS, history_model="iterations", branching="overwrite",
               coexistence="single_active", time_mechanics=["memory"],
               joined_worlds="not_preexist", turnstiles="none",
               protagonist_scope="singular", axis="story_order",
               validation="evidence_pending", merges="forbidden", genealogy="acyclic"),
    "P4": dict(DEFAULTS, history_model="universes", branching="undeclared",
               coexistence="undeclared", time_mechanics=["body"],
               joined_worlds="undeclared", turnstiles="both_signs",
               protagonist_scope="singular", axis="story_order",
               validation="observation_only", merges="forbidden", genealogy="acyclic"),
    "tenet": dict(DEFAULTS, history_model="universes", branching="branch",
                  coexistence="coexisting", time_mechanics=["body", "memory"],
                  joined_worlds="preexist", turnstiles="both_signs",
                  protagonist_scope="singular", axis="story_order",
                  validation="evidence_pending", merges="forbidden", genealogy="acyclic"),
    "dark": dict(DEFAULTS, history_model="universes", branching="branch",
                 coexistence="coexisting", time_mechanics=["body"],
                 joined_worlds="preexist", turnstiles="none",
                 protagonist_scope="multiple", axis="story_order",
                 validation="evidence_pending", merges="forbidden", genealogy="bootstrap_cycles"),
    "steins-gate": dict(DEFAULTS, history_model="revisions", branching="overwrite",
                        coexistence="single_active", time_mechanics=["memory"],
                        joined_worlds="preexist", turnstiles="none",
                        protagonist_scope="singular", axis="story_order",
                        validation="evidence_pending", merges="forbidden", genealogy="acyclic"),
}

# Aliases for the rules/canon refinements that pick a preset + extra rules.
RULES = {
    "waif": "P1",   # THE WAIF canonical branch model = P1 parameters + waif canon.
}


def resolve(profile_block):
    """Resolve a profile block to a fully-expanded parameter dict.

    Accepts either a string name ('P1') or a block
    {'base': 'P1', 'rules': 'waif', 'params': {'axis': 'world_time'}}.
    Returns a merged dict of concrete parameter values. Unknown names raise.
    """
    if isinstance(profile_block, str):
        name = profile_block
        base = PROFILES.get(name)
        if base is None:
            raise ValueError(f"unknown profile {name!r}")
        return dict(base)

    name = profile_block.get("name") or profile_block.get("base")
    base = PROFILES.get(name)
    if base is None:
        raise ValueError(f"unknown profile {name!r}")
    params = dict(base)
    overrides = profile_block.get("params") or {}
    for k, v in overrides.items():
        if k not in DEFAULTS:
            raise ValueError(f"unknown parameter {k!r} in profile {name!r}")
        params[k] = v
    return params
