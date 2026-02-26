#!/usr/bin/env python3
# =============================================================================
# SquareBracketDiceBot (SBDB) — stress_test.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Stress tests the dice engine under rapid random rolling conditions.
# Unlike test_suite.py which checks correctness with deterministic min/max,
# this script fires random rolls as fast as possible and looks for crashes,
# unexpected errors, and malformed output.
#
# Run with: ./stress_test.py
# Run harder: ./stress_test.py --rolls 5000
# =============================================================================

import sys
import time
import random
from dice_engine import roll_dice
from version import VERSION

# --- Configuration ---
DEFAULT_ROLLS = 1000
PRINT_EVERY = 100       # Print progress every N rolls
SHOW_FAILURES = True    # Print details on any failure

# --- Expression pool ---
# A wide variety of valid expressions to hammer on
EXPRESSIONS = [
    # Basic
    "1d4", "1d6", "1d8", "1d10", "1d12", "1d20", "1d100",
    # Multi-die
    "2d6", "3d6", "4d6", "5d6", "8d6", "10d6",
    "2d8", "3d8", "4d8",
    "2d10", "3d10",
    "2d12", "3d12",
    "2d20", "3d20",
    # Modifiers
    "1d20+5", "1d20-3", "2d6+10", "1d4-1", "1d6+0",
    "1d20+2d4+5", "3d6+3d6",
    "2*1d6", "3*1d4",
    # Keep/Drop
    "4d6kh3", "5d6kh3", "5d6kh4",
    "4d6kl1", "4d6kl2",
    "4d6dh1", "6d8dh2",
    "6d8dl2", "7d10dl3",
    # Advantage/Disadvantage
    "1d20a", "1d20d",
    "1d8a", "1d8d",
    "1d12a", "1d12d",
    # Batch x (summing)
    "2x1d6", "5x2d6", "10x3d6", "20x1d20",
    "5x1d20+5", "10x2d6+3",
    # Batch t/b/# (individual)
    "4t1d6", "6b2d6", "8#1d20",
    "4t3d6", "5b2d8",
    # Combined keep + batch
    "5x2d20kh1", "10t4d6kh3",
    # Verbose flag (should strip and roll normally)
    "1d20v", "2d6v", "5d6kh3v",
    "1d20av", "1d20dv",
    "10x3d6v", "5t2d6v",
    # Math combinations
    "5d6kh3+2", "4d6kh3-1", "2d20kl1+10",
    # Large dice
    "1d1000", "3d100", "2d1000",
    # Edge cases
    "1d1", "10d1", "20d1",
    "1d2", "1d3",
]

# --- Invalid expressions (should return Error gracefully, never crash) ---
INVALID_EXPRESSIONS = [
    "d", "4d", "d+d", "d20", "monkies", "bug", "help",
    "install", "version", "about", "verbose",
    "1d", "1d+5", "kh3", "dh2",
    "", "   ", "1d20+",
]

def run_stress_test(total_rolls):
    print(f"🔨 --- SBDB STRESS TEST --- 🔨")
    print(f"📦 Engine Version: {VERSION}")
    print(f"🎯 Target: {total_rolls:,} random rolls")
    print(f"📋 Expression pool: {len(EXPRESSIONS)} valid + {len(INVALID_EXPRESSIONS)} invalid")
    print("-" * 50)

    errors = []
    crashes = []
    passed = 0
    start_time = time.time()

    all_expressions = (
        [(e, True) for e in EXPRESSIONS] +
        [(e, False) for e in INVALID_EXPRESSIONS]
    )

    for i in range(1, total_rolls + 1):
        expr, should_succeed = random.choice(all_expressions)

        try:
            score, breakdown, verbose = roll_dice(expr)

            if score == "Error":
                if should_succeed:
                    errors.append(f"[[{expr}]] returned Error unexpectedly: {breakdown}")
                # Invalid expressions returning Error is correct — not a failure
            else:
                # Sanity check the output
                if score is None or breakdown is None:
                    errors.append(f"[[{expr}]] returned None: score={score} breakdown={breakdown}")
                elif str(score).strip() == "":
                    errors.append(f"[[{expr}]] returned empty score")
                else:
                    passed += 1

        except Exception as e:
            crashes.append(f"[[{expr}]] CRASHED: {type(e).__name__}: {e}")

        if i % PRINT_EVERY == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed
            print(f"  {i:,} rolls completed — {rate:.0f} rolls/sec — {len(errors)} errors — {len(crashes)} crashes")

    elapsed = time.time() - start_time
    rate = total_rolls / elapsed

    print("-" * 50)
    print(f"\n📊 STRESS TEST SUMMARY")
    print(f"Total rolls:   {total_rolls:,}")
    print(f"Passed:        {passed:,} ✅")
    print(f"Errors:        {len(errors)} {'✅' if not errors else '❌'}")
    print(f"Crashes:       {len(crashes)} {'✅' if not crashes else '💥'}")
    print(f"Elapsed:       {elapsed:.2f}s")
    print(f"Roll rate:     {rate:.0f} rolls/sec")

    if SHOW_FAILURES and errors:
        print(f"\n⚠️ ERRORS:")
        for e in errors[:20]:  # cap at 20
            print(f"  {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors)-20} more")

    if SHOW_FAILURES and crashes:
        print(f"\n💥 CRASHES:")
        for c in crashes[:20]:
            print(f"  {c}")

    if not errors and not crashes:
        print(f"\n✨ ALL CLEAR: Engine is rock solid under stress! ✨")
    else:
        print(f"\n⚠️ ISSUES FOUND: Review errors and crashes above.")

if __name__ == "__main__":
    rolls = DEFAULT_ROLLS
    if "--rolls" in sys.argv:
        try:
            rolls = int(sys.argv[sys.argv.index("--rolls") + 1])
        except (IndexError, ValueError):
            print("Usage: ./stress_test.py --rolls 5000")
            sys.exit(1)
    run_stress_test(rolls)
