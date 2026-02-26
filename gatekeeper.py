# =============================================================================
# SquareBracketDiceBot (SBDB) — gatekeeper.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Filters incoming messages before any processing occurs. Enforces the
# server/user whitelist and ignores messages that match Tupperbox-style
# prefixes to prevent interference with other bots.
# =============================================================================

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
    # 1. IGNORE PATTERN FILTER (Tupperbox & Short Name Prefixes)
    if not message.webhook_id:
        clean_content = message.content.strip()
        
        # Rule A: Two identical letters followed by a space (e.g., 'cc ', 'aa ')
        if re.match(r'^([a-zA-Z])\1\s', clean_content):
            return False
            
        # Rule B: Any 1-5 letter word followed by a colon at the start of the line
        # ^ starts at beginning
        # [a-zA-Z]{1,5} matches any letters, length 1 to 5
        # : matches the colon
        if re.match(r'^[a-zA-Z]{1,5}:', clean_content):
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
