# =============================================================================
# SquareBracketDiceBot (SBDB) — gatekeeper.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Filters incoming messages before any processing occurs. Enforces the
# server/user whitelist, ignores Tupperbox-style prefixes, and rate limits
# users to prevent abuse.
# =============================================================================
import time
import logging
import re

log_cooldowns = {}
COOLDOWN_SECONDS = 60

# --- Rate Limiting ---
RATE_LIMIT_MAX = 20       # Max rolls allowed per window
RATE_LIMIT_WINDOW = 60    # Window size in seconds
rate_limit_buckets = {}   # {user_id: [timestamp, timestamp, ...]}
rate_limit_warned = {}    # {user_id: last_warned_timestamp} — prevents DM spam

def get_context(message):
    guild = f"Guild: {message.guild.name} ({message.guild.id})" if message.guild else "Direct Message"
    channel = f"Channel: {message.channel.name} ({message.channel.id})" if hasattr(message.channel, 'name') else f"DM Channel ({message.channel.id})"
    return f"[{guild} | {channel}]"

async def check_rate_limit(message, authorized_users):
    """
    Returns True if the user is within their rate limit (OK to proceed).
    Returns False if they've exceeded it, and sends them a one-time DM warning.
    Authorized users are always exempt.
    """
    user_id = message.author.id

    # Admins are exempt
    if user_id in authorized_users:
        return True

    current_time = time.time()

    # Get or create the user's timestamp bucket
    timestamps = rate_limit_buckets.get(user_id, [])

    # Drop timestamps outside the current window
    timestamps = [t for t in timestamps if current_time - t < RATE_LIMIT_WINDOW]

    if len(timestamps) >= RATE_LIMIT_MAX:
        # Rate limit exceeded — warn the user once per window
        last_warned = rate_limit_warned.get(user_id, 0)
        if current_time - last_warned > RATE_LIMIT_WINDOW:
            rate_limit_warned[user_id] = current_time
            logging.warning(f"RATE LIMITED: {message.author} (ID: {user_id}) {get_context(message)}")
            try:
                await message.author.send(
                    f"⚠️ You're rolling too fast! You can make up to **{RATE_LIMIT_MAX} rolls "
                    f"per {RATE_LIMIT_WINDOW} seconds**. Please slow down and try again shortly."
                )
            except Exception:
                pass  # If we can't DM them, fail silently
        return False

    # Under the limit — record this roll and allow it
    timestamps.append(current_time)
    rate_limit_buckets[user_id] = timestamps
    return True

def is_authorized(message, authorized_guilds, authorized_users):
    # 1. IGNORE PATTERN FILTER (Tupperbox & Short Name Prefixes)
    if not message.webhook_id:
        clean_content = message.content.strip()

        # Rule A: Two identical letters followed by a space (e.g., 'cc ', 'aa ')
        if re.match(r'^([a-zA-Z])\1\s', clean_content):
            return False

        # Rule B: Any 1-5 letter word followed by a colon at the start of the line
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
