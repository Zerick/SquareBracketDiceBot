import time
import logging
import re

log_cooldowns = {}
COOLDOWN_SECONDS = 60

def get_context(message):
    guild = f"Guild: {message.guild.name} ({message.guild.id})" if message.guild else "Direct Message"
    channel = f"Channel: {message.channel.name} ({message.channel.id})" if hasattr(message.channel, 'name') else f"DM Channel ({message.channel.id})"
    return f"[{guild} | {channel}]"

def is_authorized(message, authorized_guilds, authorized_users):
    # 1. IGNORE PATTERN FILTER (Tupperbox & Character Prefixes)
    if not message.webhook_id:
        clean_content = message.content.strip().lower()
        
        # Pattern A: Two identical letters followed by a space (e.g., 'cc ', 'aa ')
        if re.match(r'^([a-z])\1\s', clean_content):
            return False
            
        # Pattern B: Specific Name Prefixes followed by a colon (e.g., 'amy:', 'kat: ')
        ignored_names = [
            "amy", "dawn", "jan", "jen", "kat", "bots", "shay", "so", 
            "tina", "tro", "zara", "kay", "mori", "elsie", "lexi", 
            "lexih", "ah", "quynh", "hexi"
        ]
        
        # Matches any name in the list followed immediately by a colon
        name_pattern = r'^(' + '|'.join(ignored_names) + r'):'
        if re.match(name_pattern, clean_content):
            return False

    # 2. STANDARD WHITELIST CHECK
    is_whitelisted_guild = message.guild and message.guild.id in authorized_guilds
    is_whitelisted_user = message.author.id in authorized_users

    if not (is_whitelisted_guild or is_whitelisted_user):
        current_time = time.time()
        user_id = message.author.id

        last_logged = log_cooldowns.get(user_id, 0)
        if current_time - last_logged > COOLDOWN_SECONDS:
            log_cooldowns[user_id] = current_time
            logging.warning(f"UNAUTHORIZED ATTEMPT: {message.author} (ID: {user_id}) {get_context(message)}")
        return False

    return True
