#!/usr/bin/env python3
from dice_engine import roll_dice
from test_cases import DICE_TESTS

# Initialize counters
passed = 0
failed = 0
total = len(DICE_TESTS)

print("🧪 --- SBDB OFFLINE TEST SUITE --- 🧪")
print("📦 Engine Version: 1.2.7-STABLE")
print("-" * 40)

for query, expected_min, expected_max in DICE_TESTS:
    print(f"Testing: [[{query}]]")
    
    # Run Min test
    # (Assuming your engine has a way to force min/max, 
    # or you are checking the logic we built previously)
    res_min, _ = roll_dice(query, mode="min") 
    res_max, _ = roll_dice(query, mode="max")
    
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
