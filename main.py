import discord
import re
import logging
import asyncio
from config import TOKEN, WEBHOOK_NAME, EMBED_COLOR
from menu import MENU_TEXT
from installation import INSTALL_TEXT
from about import ABOUT_TEXT
from dice_engine import roll_dice
from whitelist import AUTHORIZED_GUILDS, AUTHORIZED_USERS
from logger_config import setup_logging
from gatekeeper import is_authorized, get_context

try:
    import config
except ImportError:
    print("Error: config.py not found.")
    print("Please copy config.py.example to config.py and add your token.")
    exit(1)

# Initialize self-cleaning logs (discord noise is silenced in logger_config)
setup_logging()

# Global Verbose Toggle (True = Console shows every roll)
VERBOSE_MODE = True

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

active_webhook = None

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    global active_webhook, VERBOSE_MODE

    # 1. BASIC FILTERS
    if message.author == client.user:
        return
    if message.webhook_id and message.author.name == WEBHOOK_NAME:
        return

    # 2. HANDLE DIRECT MESSAGES
    if message.guild is None:
        matches = re.findall(r'\[\[(.*?)\]\]', message.content)

        if matches:
            # SECURITY CHECK: Only whitelisted users can toggle verbose
            if any(m.lower() == "verbose" for m in matches):
                if message.author.id in AUTHORIZED_USERS:
                    VERBOSE_MODE = not VERBOSE_MODE
                    status = "ON" if VERBOSE_MODE else "OFF"
                    await message.author.send(f"Terminal Verbose Mode: **{status}**")
                else:
                    logging.warning(f"Unauthorized verbose toggle attempt by {message.author} (ID: {message.author.id})")
                return

            if any(m.lower() in ["help", "menu"] for m in matches):
                await message.author.send(MENU_TEXT)
                return
            if any(m.lower() == "install" for m in matches):
                await message.author.send(INSTALL_TEXT)
                return
            if any(m.lower() == "about" for m in matches):
                await message.author.send(ABOUT_TEXT)
                return

            # Handle dice rolls in DMs
            output_text = message.content
            for m in matches:
                try:
                    score, breakdown = roll_dice(m)
                    if VERBOSE_MODE:
                        print(f"[DM] {message.author.display_name} - [[{m}]] - {score} ({breakdown})")
                    output_text = output_text.replace(f"[[{m}]]", f"**{score}** ({breakdown})", 1)
                except:
                    continue

            if output_text != message.content:
                await message.author.send(output_text)
                return

        await message.author.send(f"Hello! I am the Dice Proxy bot. Here is how you can use me:\n{MENU_TEXT}")
        return

    # 3. SERVER MESSAGES (Standard Gatekeeper/Whitelist check)
    if not is_authorized(message, AUTHORIZED_GUILDS, AUTHORIZED_USERS):
        return

    # 4. SERVER COMMANDS & DICE PROCESSING
    matches = re.findall(r'\[\[(.*?)\]\]', message.content)
    if not matches:
        return

    # SECURITY CHECK: Even in a server, only YOU can toggle verbose
    if any(m.lower() == "verbose" for m in matches):
        if message.author.id in AUTHORIZED_USERS:
            VERBOSE_MODE = not VERBOSE_MODE
            status = "ON" if VERBOSE_MODE else "OFF"
            await message.channel.send(f"Terminal Verbose Mode: **{status}**")
        else:
            logging.warning(f"Unauthorized verbose toggle attempt in {message.guild.name} by {message.author} (ID: {message.author.id})")
        return

    # Help / Menu command
    if any(m.lower() in ["help", "menu"] for m in matches):
        await message.channel.send(MENU_TEXT)
        return

    # Installation command
    if any(m.lower() == "install" for m in matches):
        await message.channel.send(INSTALL_TEXT)
        return

    # About command
    if any(m.lower() == "about" for m in matches):
        await message.channel.send(ABOUT_TEXT)
        return

    # Diagnostic Permission command
    if any(m.lower() == "check_perms" for m in matches):
        perms = message.channel.permissions_for(message.guild.me)
        checks = [
            ("View Channel", perms.view_channel, "Critical: Bot is blind without this."),
            ("Send Messages", perms.send_messages, "Critical: Used for Help/Install menus."),
            ("Manage Messages", perms.manage_messages, "Critical: Required to hide [[brackets]] and Tupper triggers."),
            ("Manage Webhooks", perms.manage_webhooks, "Critical: Required to post dice results as the user."),
            ("Embed Links", perms.embed_links, "Recommended: Ensures Help menus format correctly.")
        ]
        output = f"### 🛡️ Permissions Checklist for #{message.channel.name}\n"
        for name, has_perm, note in checks:
            emoji = "✅" if has_perm else "❌"
            output += f"{emoji} **{name}** — {note}\n"
        try:
            await message.author.send(output)
        except discord.Forbidden:
            await message.channel.send("⚠️ I couldn't DM you! Please open your DMs to receive the report.")
        return

    # Bug Reporting
    if message.content.lower().startswith('[[bug]]'):
        bug_content = message.content[7:].strip()
        logging.error(f"BUG REPORT from {message.author} (ID: {message.author.id}) {get_context(message)}: {bug_content}")
        await message.channel.send("Bug logged, thank you!")
        return

    # Dice Rolling Engine
    output_text = message.content
    for m in matches:
        try:
            score, breakdown = roll_dice(m)
            
            if VERBOSE_MODE:
                # Format: Player - Roll String - Result (Breakdown)
                print(f"{message.author.display_name} - [[{m}]] - {score} ({breakdown})")
            
            tooltip = f"[[{m}]] = {breakdown}"
            replacement = f"[{score}](http://hover.roll '{tooltip}')"
            output_text = output_text.replace(f"[[{m}]]", replacement, 1)
        except Exception as e:
            logging.error(f"DICE ERROR from {message.author} (ID: {message.author.id}) {get_context(message)} on [[{m}]]: {e}")
            continue

    # 5. SERVER WEBHOOK DELIVERY
    if output_text != message.content:
        if active_webhook is None:
            webhooks = await message.channel.webhooks()
            active_webhook = discord.utils.get(webhooks, name=WEBHOOK_NAME)
            if not active_webhook:
                active_webhook = await message.channel.create_webhook(name=WEBHOOK_NAME)

        try:
            try:
                await message.delete()
            except:
                pass

            embed = discord.Embed(description=output_text, color=EMBED_COLOR)
            await active_webhook.send(
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                embed=embed,
                wait=True
            )
        except Exception as e:
            logging.error(f"WEBHOOK ERROR for {message.author.id}: {e}")
            active_webhook = None

client.run(TOKEN)
