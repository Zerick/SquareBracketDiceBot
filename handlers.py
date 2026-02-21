import discord
import re
import logging
import asyncio
from dice_engine import roll_dice
from config import WEBHOOK_NAME, EMBED_COLOR
from menu import MENU_TEXT
from installation import INSTALL_TEXT
from about import ABOUT_TEXT
from gatekeeper import get_context

# State management for Verbose mode
VERBOSE_MODE = True

def toggle_verbose():
    global VERBOSE_MODE
    VERBOSE_MODE = not VERBOSE_MODE
    return "ON" if VERBOSE_MODE else "OFF"

def get_verbose():
    return VERBOSE_MODE

async def handle_dice_logic(message, matches):
    """Processes the dice strings and returns the updated text."""
    output_text = message.content
    dice_rolled = False
    
    for m in matches:
        try:
            score, breakdown = roll_dice(m)
            dice_rolled = True
            if get_verbose():
                print(f"{message.author.display_name} - [[{m}]] - {score} ({breakdown})")
            
            # Hover tooltip logic
            tooltip = f"[[{m}]] = {breakdown}"
            replacement = f"[{score}](http://hover.roll '{tooltip}')"
            output_text = output_text.replace(f"[[{m}]]", replacement, 1)
        except:
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
