#!/usr/bin/env python3
# =============================================================================
# SquareBracketDiceBot (SBDB) — test_suite.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Offline test suite. Runs all cases in test_cases.py against the dice engine
# using deterministic min/max modes to verify correctness without randomness.
# Run with: ./test_suite.py
# =============================================================================

from dice_engine import roll_dice, VERSION
from test_cases import DICE_TESTS

# Initialize counters
passed = 0
failed = 0
total = len(DICE_TESTS)

print("🧪 --- SBDB OFFLINE TEST SUITE --- 🧪")
print(f"📦 Engine Version: {VERSION}")
print("-" * 40)

for query, expected_min, expected_max in DICE_TESTS:
    print(f"Testing: [[{query}]]")
    
    res_min, _, _v = roll_dice(query, mode="min")
    res_max, _, _v = roll_dice(query, mode="max")
    
    min_pass = str(res_min) == expected_min
    max_pass = str(res_max) == expected_max
    
    if min_pass and max_pass:
        print(f"✅ PASS     [MIN] Got: {res_min}")
        print(f"✅ PASS     [MAX] Got: {res_max}")
        passed += 1
    else:
        if not min_pass:
            print(f"❌ FAIL     [MIN] Expected: {expected_min} | Got: {res_min}")
        if not max_pass:
            print(f"❌ FAIL     [MAX] Expected: {expected_max} | Got: {res_max}")
        failed += 1
    print("-" * 40)

# --- THE ROLL-UP SUMMARY ---
print("\n📊 TEST SUMMARY")
print(f"TOTAL:  {total}")
print(f"PASSED: {passed} ✅")
print(f"FAILED: {failed} ❌")

if failed == 0:
    print("\n✨ ALL SYSTEMS GO: Vibe check 100% passed! ✨")
else:
    print(f"\n⚠️ WARNING: {failed} tests failed. Check your logic!")
