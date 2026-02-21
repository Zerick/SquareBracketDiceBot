import re
import d20

def translate_query(query):
    """Translates dh/dl into kh/kl for d20 library support."""
    clean_q = query.replace(" ", "").lower()
    drop_match = re.search(r'(\d+)d(\d+)(d[hl])(\d+)', clean_q)
    if drop_match:
        total, size, dtype, num = drop_match.groups()
        num_to_keep = max(0, int(total) - int(num))
        return f"{total}d{size}{'kl' if dtype == 'dh' else 'kh'}{num_to_keep}"
    return clean_q

def format_breakdown(res):
    """Scrubs stars and replaces strikethroughs with parentheses."""
    raw_str = str(res)
    inner_match = re.search(r'\((.*?)\)', raw_str)
    if inner_match:
        dice_part = inner_match.group(1)
        # Replace strikethrough with parentheses
        dice_part = re.sub(r'~~(.*?)~~', r'(\1)', dice_part)
        # Remove asterisks (crits)
        dice_part = dice_part.replace('*', '')
        return f"{dice_part} = {res.total}"
    return str(res.total).replace('*', '')

def roll_dice(query):
    """Handles both single rolls and Nx multipliers."""
    clean_q = translate_query(query)
    multiplier_match = re.match(r'^(\d+)x(.+)', clean_q)
    
    if multiplier_match:
        count = int(multiplier_match.group(1))
        expr = multiplier_match.group(2)
        rolls = [d20.roll(expr) for _ in range(count)]
        total_score = sum(r.total for r in rolls)
        breakdown = " | ".join([format_breakdown(r) for r in rolls])
        return total_score, breakdown
    else:
        result = d20.roll(clean_q)
        return result.total, format_breakdown(result)
