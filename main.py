import discord
import re
import logging
import asyncio
import handlers

# From config.py (The basics)
from config import TOKEN, WEBHOOK_NAME

# From whitelist.py (The IDs)
from whitelist import AUTHORIZED_USERS, AUTHORIZED_GUILDS

# From their individual files
from menu import MENU_TEXT
from installation import INSTALL_TEXT
from about import ABOUT_TEXT

# From your utility files
from logger_config import setup_logging
from gatekeeper import is_authorized, get_context

setup_logging()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.webhook_id and message.author.name == WEBHOOK_NAME: return

    matches = re.findall(r'\[\[(.*?)\]\]', message.content)

    # --- DM HANDLING ---
    if message.guild is None:
        if not matches:
            await message.author.send(f"Hello! I am the Dice Proxy bot.\n{MENU_TEXT}")
            return
            
        if any(m.lower() == "verbose" for m in matches):
            if message.author.id in AUTHORIZED_USERS:
                status = handlers.toggle_verbose()
                await message.author.send(f"Terminal Verbose Mode: **{status}**")
            return

        # Regular DM processing
        output_text, rolled = await handlers.handle_dice_logic(message, matches)
        if rolled: await message.author.send(output_text)
        return

    # --- SERVER HANDLING ---
    if not is_authorized(message, AUTHORIZED_GUILDS, AUTHORIZED_USERS):
        return

    if not matches: return

    # Admin Toggles
    if any(m.lower() == "verbose" for m in matches):
        if message.author.id in AUTHORIZED_USERS:
            status = handlers.toggle_verbose()
            try: await message.delete()
            except: pass
            try: await message.author.send(f"Terminal Verbose Mode: **{status}**")
            except: pass
        return

    # Static Commands
    cmd = matches[0].lower()
    if cmd in ["help", "menu"]: await message.channel.send(MENU_TEXT); return
    if cmd == "install": await message.channel.send(INSTALL_TEXT); return
    if cmd == "about": await message.channel.send(ABOUT_TEXT); return

    # Permissions Check
    if cmd == "check_perms":
        p = message.channel.permissions_for(message.guild.me)
        report = f"### 🛡️ Perms for #{message.channel.name}\n"
        report += f"{'✅' if p.manage_webhooks else '❌'} Manage Webhooks\n"
        report += f"{'✅' if p.manage_messages else '❌'} Manage Messages"
        await message.author.send(report)
        return

    # Dice Processing
    output_text, rolled = await handlers.handle_dice_logic(message, matches)
    if rolled:
        await handlers.send_via_webhook(message, output_text)

client.run(TOKEN)
