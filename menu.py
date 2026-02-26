# =============================================================================
# SquareBracketDiceBot (SBDB) — menu.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Contains the help/menu text displayed when a user types [[help]] or [[menu]].
# =============================================================================

MENU_TEXT = """
🎲 **SBDB Dice Bot Help** 🎲

**Basic Rolls:**
[[2d6]] - Roll two 6-sided dice
[[1d20]] - Roll one 20-sided die

**Advanced Modifiers:**
[[1d20a]] - Advantage (roll twice, keep highest)
[[1d20d]] - Disadvantage (roll twice, keep lowest)
[[5d6kh3]] - Keep Highest 3
[[4d20kl2]] - Keep Lowest 2
[[6d8dh2]] - Drop Highest 2
[[7d10dl3]] - Drop Lowest 3

**Multiple Rolls:**
[[10x3d6]] - Roll 3d6 ten times and sum the results
[[5x2d20kh1]] - Roll 2d20 five times keeping highest, sum the results
[[10t3d6]] - Roll 3d6 ten times and show individual results
use t, b, or # for individual results

**Combining with Math:**
[[5d6kh3+2]] - Keep highest 3, then add 2
[[4*2d20kl1]] - Keep lowest 1, then multiply by 4

**Verbose Mode:**
Add a v to any roll to see the full breakdown inline:
[[1d20v]], [[5d6kh3v]], [[10x3d6v]]

Note: Use [[help]] to see this again
❓See also [[about]] ❓
"""
