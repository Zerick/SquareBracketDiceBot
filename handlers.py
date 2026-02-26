import discord
import re
import logging
import asyncio
from logging.handlers import RotatingFileHandler
from dice_engine import roll_dice
from config import WEBHOOK_NAME, EMBED_COLOR
from menu import MENU_TEXT
from installation import INSTALL_TEXT
from about import ABOUT_TEXT
from gatekeeper import get_context
from datetime import datetime

# State management for Verbose mode
VERBOSE_MODE = True

def toggle_verbose():
    global VERBOSE_MODE
    VERBOSE_MODE = not VERBOSE_MODE
    return "ON" if VERBOSE_MODE else "OFF"

def get_verbose():
    return VERBOSE_MODE

def log_bug(text):
    """Writes a bug report entry directly to bugs.log."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('bugs.log', 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} | {text}\n")

async def handle_bug_report(message, bug_text):
    """Logs a bug report to bugs.log and echoes confirmation to the user."""
    user = message.author
    identity = f"{user} (ID: {user.id})"

    if not bug_text:
        # Empty report — console only, no file write
        print(f"[BUG] Empty report from {identity}")
        await message.author.send(
            "Please describe the bug after the tag, for example:\n"
            "`[[bug]] roller crashed on 5d6kh3`"
        )
        return

    # Full report — write to file, print to console, confirm to user
    log_entry = f"{identity} | {bug_text}"
    log_bug(log_entry)
    print(f"[BUG] {log_entry}")
    await message.author.send(f"Thank you! BUG: {bug_text} Logged!")

async def handle_dice_logic(message, matches):
    """Processes the dice strings and returns the updated text."""
    output_text = message.content
    dice_rolled = False
    
    for m in matches:
        try:
            score, breakdown, roll_verbose = roll_dice(m)
            dice_rolled = True
            if get_verbose():
                print(f"{message.author.display_name} - [[{m}]] - {score} ({breakdown})")
            
            if roll_verbose:
                # Verbose mode: show full breakdown inline AND as a hover tooltip
                original_query = m.rstrip('v').rstrip('V')
                tooltip = f"[[{original_query}]] = {breakdown}"
                replacement = f"**{original_query}** → [{breakdown}](http://hover.roll '{tooltip}')"
            else:
                # Normal mode: hover tooltip link
                tooltip = f"[[{m}]] = {breakdown}"
                replacement = f"[{score}](http://hover.roll '{tooltip}')"

            output_text = output_text.replace(f"[[{m}]]", replacement, 1)
        except Exception as e:
            logging.warning(f"Dice error for '{m}': {e}")
            continue
    return output_text, dice_rolled

async def send_via_webhook(message, output_text):
    """FIX: Fetches/Creates webhook per-channel to prevent teleporting."""
    try:
        webhooks = await message.channel.webhooks()
        target_webhook = discord.utils.get(webhooks, name=WEBHOOK_NAME)
        
        if not target_webhook:
            target_webhook = await message.channel.create_webhook(name=WEBHOOK_NAME)

        try:
            await message.delete()
        except:
            pass

        embed = discord.Embed(description=output_text, color=EMBED_COLOR)
        await target_webhook.send(
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
            embed=embed,
            wait=True
        )
    except Exception as e:
        logging.error(f"WEBHOOK ERROR in {message.channel.name}: {e}")
