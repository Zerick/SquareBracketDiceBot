# =============================================================================
# SquareBracketDiceBot (SBDB) — stats.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Provides statistical analysis for dice expressions via the [[stats]] command.
# Uses Monte Carlo simulation (50,000 rolls) to accurately handle any
# expression the dice engine supports, including keep/drop and advantage.
#
# Stats provided:
#   Min    — the lowest possible result
#   Max    — the highest possible result
#   Mean   — the average result over infinite rolls
#   Median — the middle value; half of all rolls land above, half below
#   Std Dev — how spread out rolls are; low = clusters near mean, high = wide variance
# =============================================================================

import statistics
from dice_engine import roll_dice

SIMULATION_RUNS = 50000

def get_stats(query):
    """
    Runs a Monte Carlo simulation for the given dice expression and returns
    a dict of statistical results plus elapsed time, or None if invalid.
    """
    import time
    start = time.time()

    results = []
    for _ in range(SIMULATION_RUNS):
        score, _, _ = roll_dice(query)
        if score == "Error":
            return None
        try:
            results.append(int(score))
        except (ValueError, TypeError):
            return None

    elapsed = round(time.time() - start, 2)

    return {
        "min":     min(results),
        "max":     max(results),
        "mean":    round(sum(results) / len(results), 2),
        "median":  statistics.median(results),
        "stdev":   round(statistics.stdev(results), 2),
        "elapsed": elapsed,
    }

def format_stats(query, stats):
    """Formats the stats dict into a Discord-ready message."""
    return (
        f"📊 **Stats for [[{query}]]** *(based on {SIMULATION_RUNS:,} simulated rolls)*\n"
        f"```\n"
        f"Min:     {stats['min']}\n"
        f"Max:     {stats['max']}\n"
        f"Mean:    {stats['mean']}  (average over many rolls)\n"
        f"Median:  {stats['median']}  (half of rolls land above this, half below)\n"
        f"Std Dev: {stats['stdev']}  (spread — low means results cluster near the mean)\n"
        f"```"
    )
