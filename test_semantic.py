#!/usr/bin/env python3
"""Negative test runner: every bad fixture must exit 2 with its expected E-code. No tracebacks accepted."""
import subprocess, sys, glob, os

VENVPY = sys.executable
HERE = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.join(HERE, "semantic_validate.py")

EXPECTED = {
    "E240_multi_world_P2": "E240",
    "E241_multi_world_P3": "E241",
    "E201_waif_needs_P1": "E201",
    "E082_bad_outcome_universe": "E082",
    "E143_link_transfer_mismatch": "E143",
    "E146_incomplete_chain": "E146",
    "E040_event_universe": "E040",
    "E210_fate_instance": "E210",
    "E112_same_universe_relation": "E112",
    "E086_continues_mismatch": "E086",
    "E084_born_mismatch": "E084",
    "E118_leap_not_memory": "E118",
}

fails = 0
for path in sorted(glob.glob(os.path.join(HERE, "tests", "*.json"))):
    name = os.path.basename(path)[:-5]
    want = EXPECTED.get(name)
    r = subprocess.run([VENVPY, VAL, path], capture_output=True, text=True, timeout=60)
    out = r.stdout
    ok = (r.returncode == 2) and (want is not None) and (want in out) and ("Traceback" not in r.stderr)
    status = "PASS" if ok else "FAIL"
    if not ok:
        fails += 1
        print(f"{status} {name}: rc={r.returncode} want={want}")
        print("  stdout:", out[:300])
        if r.stderr:
            print("  stderr:", r.stderr[:200])
    else:
        code_line = [l for l in out.splitlines() if l.startswith(want)][0]
        print(f"{status} {name}: {code_line[:100]}")

# positive: Ben's Story must pass clean
r = subprocess.run([VENVPY, VAL, os.path.join(HERE, "fixtures", "bens_story.json")], capture_output=True, text=True, timeout=60)
pos_ok = r.returncode == 0 and "Traceback" not in r.stderr
print(("PASS" if pos_ok else "FAIL") + f" POSITIVE bens_story: rc={r.returncode}")
if not pos_ok:
    print(r.stdout[:400]); fails += 1

print(f"\n{sum(1 for _ in EXPECTED) + 1 - fails}/{len(EXPECTED) + 1} tests passed")
sys.exit(1 if fails else 0)
