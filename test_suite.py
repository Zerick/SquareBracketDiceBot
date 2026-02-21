#!/usr/bin/env python3
import sys
from dice_engine import roll_dice

TEST_DATA = [
    ("2d6", "2", "12"),
    ("1d20", "1", "20"),
    ("5d6kh3", "3", "18"),
    ("10x3d6", "30", "180"),
    ("4t3d6", "3, 3, 3, 3", "18, 18, 18, 18")
]

def run_suite(verbose=False):
    print("🧪 --- SBDB OFFLINE TEST SUITE --- 🧪\n")
    
    for query, exp_min, exp_max in TEST_DATA:
        print(f"Testing: [[{query}]]")
        
        # Min Test
        act_min, br_min = roll_dice(query, mode="min")
        status_min = "✅ PASS" if str(act_min) == exp_min else "❌ FAIL"
        print(f"{status_min}      [MIN] Expected: {exp_min} | Got: {act_min}")
        
        # Max Test
        act_max, br_max = roll_dice(query, mode="max")
        status_max = "✅ PASS" if str(act_max) == exp_max else "❌ FAIL"
        print(f"{status_max}      [MAX] Expected: {exp_max} | Got: {act_max}")

        if verbose:
            print(f"           Breakdown Min: {br_min}")
            print(f"           Breakdown Max: {br_max}")
            
        print("-" * 40)

if __name__ == "__main__":
    run_suite(verbose="-v" in sys.argv)
