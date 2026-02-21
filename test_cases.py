# test_cases.py

# Format: (Raw Input, Expected Min Total, Expected Max Total)
DICE_TESTS = [
    ("2d6", "2", "12"),
    ("1d20", "1", "20"),
    ("5d6kh3", "3", "18"),
    ("10x3d6", "30", "180"),
    ("4t3d6", "3, 3, 3, 3", "18, 18, 18, 18"),
    # Adding a few more to test our engine's versatility:
    ("2d6+5", "7", "17"),
    ("4d6dh1", "3", "18"),  # Tests our Drop High -> Keep Low translation
]
