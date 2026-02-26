#!/usr/bin/env python3
# =============================================================================
# SquareBracketDiceBot (SBDB) — main.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Entry point. Connects to Discord, routes all incoming messages to the
# appropriate handler — DM vs server, dice rolls vs commands vs bug reports.
# =============================================================================
import discord
import re
import logging
import asyncio
import handlers

# From config.py (The basics)
from config import TOKEN, WEBHOOK_NAME
from version import VERSION, LAST_UPDATED

# From whitelist.py (The IDs)
from whitelist import AUTHORIZED_USERS, AUTHORIZED_GUILDS

# From their individual files
from menu import MENU_TEXT
from installation import INSTALL_TEXT, INSTALL_SETUP_TEXT, INSTALL_BOT_TEXT, INSTALL_SERVICE_TEXT, INSTALL_PERMISSIONS_TEXT
from about import ABOUT_TEXT

# From your utility files
from logger_config import setup_logging
from gatekeeper import is_authorized, get_context, check_rate_limit
from stats import get_stats, format_stats

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

    # --- BUG REPORT (works everywhere, checked before guild/DM split) ---
    if any(m.lower() == "bug" for m in matches):
        bug_text_match = re.search(r'\[\[bug\]\]\s*(.*)', message.content, re.IGNORECASE)
        bug_text = bug_text_match.group(1).strip() if bug_text_match else ""
        await handlers.handle_bug_report(message, bug_text)
        return

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

        # Version command in DM
        if any(m.lower() == "version" for m in matches):
            await message.author.send(f"🎲 **SBDB** version **{VERSION}** — last updated {LAST_UPDATED}")
            return

        # Stats command in DM
        if any(m.lower().startswith("stats ") for m in matches):
            expr = next(m[6:].strip() for m in matches if m.lower().startswith("stats "))
            calculating_msg = await message.author.send(f"⏳ Calculating stats for `{expr}`...")
            stats = get_stats(expr)
            if stats:
                elapsed = stats["elapsed"]
                print(f"{message.author.display_name} - [[stats {expr}]] - completed in {elapsed}s")
                await calculating_msg.edit(content=format_stats(expr, stats))
            else:
                print(f"{message.author.display_name} - [[stats {expr}]] - invalid expression")
                await calculating_msg.edit(content=f"❌ Could not compute stats for `{expr}` — is that a valid dice expression?")
            return

        # Rate limit check for DM dice rolls
        if not await check_rate_limit(message, AUTHORIZED_USERS):
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

    # Rate limit check — applies to all commands and dice rolls
    if not await check_rate_limit(message, AUTHORIZED_USERS):
        return

    # Static Commands
    cmd = matches[0].lower()
    if cmd in ["help", "menu"]: await message.channel.send(MENU_TEXT); return
    if cmd == "install": await message.channel.send(INSTALL_TEXT); return
    if cmd == "install setup": await message.channel.send(INSTALL_SETUP_TEXT); return
    if cmd == "install bot": await message.channel.send(INSTALL_BOT_TEXT); return
    if cmd == "install service": await message.channel.send(INSTALL_SERVICE_TEXT); return
    if cmd == "install permissions": await message.channel.send(INSTALL_PERMISSIONS_TEXT); return
    if cmd == "about": await message.channel.send(ABOUT_TEXT + f"\n**Version:** {VERSION} — last updated {LAST_UPDATED}"); return
    if cmd == "version":
        await message.channel.send(f"🎲 **SBDB** version **{VERSION}** — last updated {LAST_UPDATED}")
        return
    if cmd.startswith("stats "):
        expr = cmd[6:].strip()
        calculating_msg = await message.channel.send(f"⏳ Calculating stats for `{expr}`...")
        stats = get_stats(expr)
        if stats:
            elapsed = stats["elapsed"]
            print(f"{message.author.display_name} - [[stats {expr}]] - completed in {elapsed}s")
            await calculating_msg.edit(content=format_stats(expr, stats))
        else:
            print(f"{message.author.display_name} - [[stats {expr}]] - invalid expression")
            await calculating_msg.edit(content=f"❌ Could not compute stats for `{expr}` — is that a valid dice expression?")
        return

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
