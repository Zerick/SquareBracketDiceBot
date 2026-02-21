#!/usr/bin/env python3
import sys
import dice_engine
from test_cases import DICE_TESTS  # Import the data from our new file

def run_suite(verbose=False):
    engine_ver = getattr(dice_engine, 'VERSION', 'UNKNOWN')
    engine_date = getattr(dice_engine, 'LAST_UPDATED', 'UNKNOWN')

    print(f"🧪 --- SBDB OFFLINE TEST SUITE --- 🧪")
    print(f"📦 Engine Version: {engine_ver}")
    print(f"📅 Last Updated:  {engine_date}\n")
    print("-" * 40)

    for query, exp_min, exp_max in DICE_TESTS:
        print(f"Testing: [[{query}]]")

        act_min, br_min = dice_engine.roll_dice(query, mode="min")
        act_max, br_max = dice_engine.roll_dice(query, mode="max")

        status_min = "✅ PASS" if str(act_min) == exp_min else "❌ FAIL"
        status_max = "✅ PASS" if str(act_max) == exp_max else "❌ FAIL"

        print(f"{status_min}      [MIN] Expected: {exp_min} | Got: {act_min}")
        print(f"{status_max}      [MAX] Expected: {exp_max} | Got: {act_max}")

        if verbose:
            print(f"           Breakdown Min: {br_min}")
            print(f"           Breakdown Max: {br_max}")

        print("-" * 40)

if __name__ == "__main__":
    run_suite(verbose="-v" in sys.argv)
