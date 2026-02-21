#!/usr/bin/env python3
import re
import d20

def translate_query(query):
    """Translates shorthand into d20-compliant syntax."""
    clean_q = query.replace(" ", "").lower()
    
    # 1. Convert 'x' to '*' for single-sum math
    clean_q = clean_q.replace('x', '*')

    # 2. Assume d6 if no size is specified: [[4d]] -> [[4d6]]
    clean_q = re.sub(r'd(?=[+-]|kh|kl|dh|dl|[*#tb]|$)', 'd6', clean_q)

    # 3. DROP TO KEEP TRANSLATION: [[6d8dh2]] -> [[6d8kl4]]
    # This regex looks for 'dh' or 'dl' and converts them to 'kl' or 'kh'
    drop_match = re.search(r'(\d+)d(\d+)(d[hl])(\d+)', clean_q)
    if drop_match:
        total, size, dtype, num = drop_match.groups()
        num_to_keep = max(0, int(total) - int(num))
        new_type = 'kl' if dtype == 'dh' else 'kh'
        return f"{total}d{size}{new_type}{num_to_keep}"

    return clean_q

def force_deterministic(query, mode):
    """
    Replaces dice notation with 'stable' dice that return min or max.
    This allows modifiers like kh/kl to still function during tests.
    """
    def replace_dice(match):
        count = int(match.group(1))
        size = int(match.group(2))
        if mode == "min":
            die_val = "1d1" # Always rolls 1
        else:
            die_val = f"(1d1+{size-1})" # Always rolls the max size
            
        return "(" + "+".join([die_val] * count) + ")"

    # Replaces '2d6' with '(1d1+1d1)' or '(1d1+5+1d1+5)'
    return re.sub(r'(\d+)d(\d+)', replace_dice, query)

def format_breakdown(res):
    """Scrubs formatting and extracts the dice math vs total."""
    raw_str = str(res)
    # Use regex to find the part inside parentheses: (1 + 6) = 7
    inner_match = re.search(r'\((.*?)\)', raw_str)
    if inner_match:
        dice_part = inner_match.group(1)
        # Clean up d20's default markdown
        dice_part = re.sub(r'~~(.*?)~~', r'(\1)', dice_part)
        dice_part = dice_part.replace('*', '')
        
        # Safely get total whether res is an object or string
        total = getattr(res, 'total', res)
        return f"{dice_part} = {total}"
    
    return str(getattr(res, 'total', res))

def roll_dice(query, mode=None):
    """
    Main entry point for both Discord and the Test Suite.
    mode: 'min' or 'max' forces deterministic results for testing.
    """
    query = query.lower().replace(' ', '')
    
    try:
        # 1. BATCH/REPEAT HANDLING (#, t, or b)
        batch_match = re.split(r'[#tb]', query, maxsplit=1)
        if len(batch_match) == 2:
            times_str, expr = batch_match
            count = max(1, min(int(times_str), 20))
            
            # Translate and/or Force Determinism
            expr = translate_query(expr)
            if mode:
                expr = force_deterministic(expr, mode)
                
            rolls = [d20.roll(expr) for _ in range(count)]
            totals = [str(getattr(r, 'total', r)) for r in rolls]
            breakdowns = [format_breakdown(r) for r in rolls]
            
            return ", ".join(totals), " | ".join(breakdowns)

        # 2. STANDARD SINGLE ROLLS
        processed_q = translate_query(query)
        if mode:
            processed_q = force_deterministic(processed_q, mode)
            
        result = d20.roll(processed_q)
        total = getattr(result, 'total', result)
        return total, format_breakdown(result)
        
    except Exception as e:
        return "Error", f"Engine Error: {e}"
