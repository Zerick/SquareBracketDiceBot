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
    # 1. TUPPERBOX TRIGGER FILTER
    # Matches 2-3 of the same letter followed by a space (e.g., 'cc ', 'ttt ')
    # If it matches, we return False so the bot ignores the human's message
    if not message.webhook_id:
        if re.match(r'^([a-zA-Z])\1{1,2}\s', message.content):
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
