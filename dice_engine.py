#!/usr/bin/env python3
import re
import d20

# VERSION TRACKER
VERSION = "1.2.2-STABLE"
LAST_UPDATED = "2026-02-21"

def translate_query(query):
    clean_q = query.replace(" ", "").lower()
    clean_q = clean_q.replace('x', '*')
    clean_q = re.sub(r'd(?=[+-]|kh|kl|dh|dl|[*#tb]|$)', 'd6', clean_q)

    # Drop/Keep logic translation
    drop_match = re.search(r'(\d+)d(\d+)(d[hl])(\d+)', clean_q)
    if drop_match:
        total, size, dtype, num = drop_match.groups()
        num_to_keep = max(0, int(total) - int(num))
        new_type = 'kl' if dtype == 'dh' else 'kh'
        return f"{total}d{size}{new_type}{num_to_keep}"
    return clean_q

def force_deterministic(query, mode):
    """
    Replaces dice with 'fixed' dice that d20 treats as individual rolls.
    '5d6kh3' -> '(1d1+5,1d1+5,1d1+5,1d1+5,1d1+5)kh3'
    """
    def replace_dice(match):
        count = int(match.group(1))
        size = int(match.group(2))
        
        if mode == "min":
            # 1d1 is always 1
            die_str = "1d1"
        else:
            # 1d1 + (size-1) is always the max (e.g., 1d1+19 for a d20)
            die_str = f"(1d1+{size-1})"
            
        # Join with commas and wrap in parentheses to create a 'set' 
        # that kh/kl can actually operate on.
        return "(" + ",".join([die_str] * count) + ")"

    return re.sub(r'(\d+)d(\d+)', replace_dice, query)

def format_breakdown(res):
    raw_str = str(res)
    # Look for anything inside brackets or parens
    inner_match = re.search(r'[\({](.*?)[\)}]', raw_str)
    if inner_match:
        dice_part = inner_match.group(1)
        dice_part = re.sub(r'~~(.*?)~~', r'(\1)', dice_part)
        dice_part = dice_part.replace('*', '')
        total = getattr(res, 'total', res)
        return f"{dice_part} = {total}"
    return str(getattr(res, 'total', res))

def roll_dice(query, mode=None):
    query = query.lower().replace(' ', '')
    try:
        # 1. BATCH HANDLING
        batch_match = re.split(r'[#tb]', query, maxsplit=1)
        if len(batch_match) == 2:
            times_str, expr = batch_match
            count = max(1, min(int(times_str), 20))
            expr = translate_query(expr)
            if mode:
                expr = force_deterministic(expr, mode)
            rolls = [d20.roll(expr) for _ in range(count)]
            totals = [str(getattr(r, 'total', r)) for r in rolls]
            return ", ".join(totals), " | ".join([format_breakdown(r) for r in rolls])

        # 2. STANDARD ROLLS
        processed_q = translate_query(query)
        if mode:
            processed_q = force_deterministic(processed_q, mode)
        result = d20.roll(processed_q)
        return getattr(result, 'total', result), format_breakdown(result)
        
    except Exception as e:
        # If it fails, we want to know WHY
        return "Error", f"{e}"
