#!/usr/bin/env python3
import sys
import dice_engine  # Import the module to get metadata AND the roll function

# Format: (Raw Input, Expected Min Total, Expected Max Total)
TEST_DATA = [
    ("2d6", "2", "12"),
    ("1d20", "1", "20"),
    ("5d6kh3", "3", "18"),
    ("10x3d6", "30", "180"),
    ("4t3d6", "3, 3, 3, 3", "18, 18, 18, 18")
]

def run_suite(verbose=False):
    # 1. Pull metadata directly from the engine
    engine_ver = getattr(dice_engine, 'VERSION', 'UNKNOWN')
    engine_date = getattr(dice_engine, 'LAST_UPDATED', 'UNKNOWN')

    print(f"🧪 --- SBDB OFFLINE TEST SUITE --- 🧪")
    print(f"📦 Engine Version: {engine_ver}")
    print(f"📅 Last Updated:  {engine_date}\n")
    print("-" * 40)

    for query, exp_min, exp_max in TEST_DATA:
        print(f"Testing: [[{query}]]")

        # Use the function from the imported module
        act_min, br_min = dice_engine.roll_dice(query, mode="min")
        act_max, br_max = dice_engine.roll_dice(query, mode="max")

        # Check Results
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
