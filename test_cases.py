# test_cases.py

# Format: (Raw Input, Expected Min Total, Expected Max Total)
DICE_TESTS = [
    # --- Basic Functionality ---
    ("2d6", "2", "12"),
    ("1d20", "1", "20"),
    ("10x3d6", "30", "180"),
    ("4t3d6", "3, 3, 3, 3", "18, 18, 18, 18"),

    # --- Math & Modifiers ---
    ("2d6+5", "7", "17"),
    ("2d6-2", "0", "10"),
    ("1d20 + 2d4 + 10", "13", "38"),

    # --- Drop/Keep Translation ---
    ("5d6kh3", "3", "18"),      # Keep Highest 3
    ("4d6dh1", "3", "18"),      # Drop Highest 1 (Translates to kl3)
    ("10d10kl1", "1", "10"),    # Keep Lowest 1
    ("6d8dl2", "4", "32"),      # Drop Lowest 2 (Translates to kh4)

    # --- Shorthand (Explicitly checking our rejection of 'headless' dice) ---
    ("d", "Error", "Error"),    
    ("4d", "Error", "Error"),   
    ("d+d", "Error", "Error"),  

    # --- Limits & Stress ---
    # Using join to generate the string "1, 1, 1..." 20 times to match engine output
    ("20x1d1", "20", "20"),
    ("20#1d1", ", ".join(["1"]*20), ", ".join(["1"]*20))
]

