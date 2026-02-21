# menu.py
MENU_TEXT = """
🎲 **SBDB Dice Bot Help** 🎲

**Basic Rolls:**
`[[2d6]]` - Roll two 6-sided dice
`[[1d20]]` - Roll one 20-sided die

**Advanced Modifiers:**
`[[5d6kh3]]` - Keep Highest 3
`[[4d20kl2]]` - Keep Lowest 2
`[[6d8dh2]]` - Drop Highest 2
`[[7d10dl3]]` - Drop Lowest 3

**Multiple Rolls:**
`[[10x3d6]]` - Roll 3d6 ten times
`[[5x2d20kh1]]` - Roll 2d20 five times, keep highest

**Combining with Math:**
`[[5d6kh3+2]]` - Keep highest 3, then add 2
`[[4*2d20kl1]]` - Keep lowest 1, then multiply by 4

*Note: Use `[[help]]` to see this again.*
❓Want to add this bot to another server? Type [[install]] for instructions.
❓See also [[about]].
*Use `[[bug]]` to log the error message entered here.*
"""
