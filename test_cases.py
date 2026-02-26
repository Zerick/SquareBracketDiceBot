# =============================================================================
# SquareBracketDiceBot (SBDB) — test_cases.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Test case definitions for test_suite.py.
# Format: (Raw Input, Expected Min Total, Expected Max Total)
# =============================================================================

DICE_TESTS = [
    # --- Basic Functionality ---
    ("2d6", "2", "12"),
    ("1d20", "1", "20"),
    ("1d100", "1", "100"),
    ("1d1000", "1", "1000"),

    # --- Verbose Flag (should strip 'v' and roll normally) ---
    ("1d20v", "1", "20"),
    ("5d6kh3v", "3", "18"),

    # --- Math & Modifiers ---
    ("2d6+5", "7", "17"),
    ("2d6-2", "0", "10"),
    ("1d6+0", "1", "6"),
    ("1d4-10", "-9", "-6"),
    ("2*1d6", "2", "12"),
    ("1d20 + 2d4 + 10", "13", "38"),
    ("3d6+3d6", "6", "36"),

    # --- Drop/Keep Translation ---
    ("5d6kh3", "3", "18"),      # Keep Highest 3
    ("4d6dh1", "3", "18"),      # Drop Highest 1 (Translates to kl3)
    ("10d10kl1", "1", "10"),    # Keep Lowest 1
    ("6d8dl2", "4", "32"),      # Drop Lowest 2 (Translates to kh4)

    # --- Summing Batch: x (rolls N times, returns grand total) ---
    ("10x3d6", "30", "180"),
    ("5x1d1+2", "15", "15"),    # 5 rolls of (1d1+2=3) = always 15
    ("20x1d6", "20", "120"),    # Max batch size
    ("21x1d1", "20", "20"),     # Over limit — clamps to 20 rolls

    # --- Individual Batch: t / b / # (rolls N times, returns each result) ---
    ("4t3d6", "3, 3, 3, 3", "18, 18, 18, 18"),
    ("4b1d6", "1, 1, 1, 1", "6, 6, 6, 6"),
    ("4#1d6", "1, 1, 1, 1", "6, 6, 6, 6"),
    ("20t1d6", ", ".join(["1"]*20), ", ".join(["6"]*20)),   # Max batch size
    ("20#1d1", ", ".join(["1"]*20), ", ".join(["1"]*20)),

    # --- Advantage / Disadvantage Shorthand ---
    ("1d20a", "1", "20"),       # Advantage — translates to 2d20kh1
    ("1d20d", "1", "20"),       # Disadvantage — translates to 2d20kl1
    ("1d8a", "1", "8"),         # Advantage on any die size
    ("1d8d", "1", "8"),         # Disadvantage on any die size
    ("1d20av", "1", "20"),      # Advantage verbose — strips v, still rolls correctly
    ("1d20dv", "1", "20"),      # Disadvantage verbose — strips v, still rolls correctly

    # --- Stats Command ---
    # Stats uses simulation so we can't test exact values.
    # These are handled separately in test_suite.py via get_stats() directly.

    # --- Shorthand (Explicitly checking our rejection of 'headless' dice) ---
    ("d", "Error", "Error"),
    ("4d", "Error", "Error"),
    ("d+d", "Error", "Error"),
]
