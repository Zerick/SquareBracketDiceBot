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
from dice_engine import roll_dice
from stats import get_stats
from version import VERSION
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

# --- STATS TESTS ---
print("\n🧪 --- STATS MODULE TESTS --- 🧪")
print("-" * 40)
stats_passed = 0
stats_failed = 0

stats_tests = [
    ("1d6",      True),   # Valid — should return a dict
    ("2d6",      True),
    ("1d20",     True),
    ("5d6kh3",   True),
    ("1d20a",    True),
    ("1d20d",    True),
    ("monkies",  False),  # Invalid — should return None
    ("d",        False),
    ("4d",       False),
]

for expr, expect_valid in stats_tests:
    result = get_stats(expr)
    is_valid = result is not None
    if is_valid == expect_valid:
        status = "✅ PASS"
        stats_passed += 1
    else:
        status = "❌ FAIL"
        stats_failed += 1
    label = "valid" if expect_valid else "invalid"
    print(f"{status}  [[stats {expr}]] — expected {label}, got {'valid' if is_valid else 'invalid'}")

print("-" * 40)
print(f"PASSED: {stats_passed} ✅")
print(f"FAILED: {stats_failed} ❌")
if stats_failed == 0:
    print("\n✨ STATS MODULE: All good! ✨")
else:
    print(f"\n⚠️ WARNING: {stats_failed} stats tests failed.")
