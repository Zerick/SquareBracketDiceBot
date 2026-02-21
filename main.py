import discord
import re
import logging
import asyncio
from config import TOKEN, WEBHOOK_NAME, EMBED_COLOR
from menu import MENU_TEXT
from installation import INSTALL_TEXT
from dice_engine import roll_dice
from whitelist import AUTHORIZED_GUILDS, AUTHORIZED_USERS
from logger_config import setup_logging
from gatekeeper import is_authorized, get_context

# Initialize self-cleaning logs (5MB x 5 backups)
setup_logging()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

active_webhook = None

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    global active_webhook

    # 1. BASIC FILTERS
    # Ignore our own bot user and our own proxy webhooks
    if message.author == client.user:
        return
    if message.webhook_id and message.author.name == WEBHOOK_NAME:
        return

    # 2. HANDLE DIRECT MESSAGES (Bypassing whitelist for help/rolls)
    if message.guild is None:
        # Log if a non-whitelisted user is interacting via DM
        if message.author.id not in AUTHORIZED_USERS:
            logging.info(f"DM Interaction from non-whitelisted user: {message.author} (ID: {message.author.id})")

        matches = re.findall(r'\[\[(.*?)\]\]', message.content)
        
        if matches:
            # Handle recognized commands in DMs
            if any(m.lower() in ["help", "menu"] for m in matches):
                await message.author.send(MENU_TEXT)
                return
            if any(m.lower() == "install" for m in matches):
                await message.author.send(INSTALL_TEXT)
                return
            if any(m.lower() == "check_perms" for m in matches):
                await message.author.send("To check permissions, please use this command inside a server channel! I can't check permissions for a private DM.")
                return
            
            # Handle dice rolls in DMs (Simple text reply, no webhooks/deletions)
            output_text = message.content
            for m in matches:
                try:
                    score, breakdown = roll_dice(m)
                    output_text = output_text.replace(f"[[{m}]]", f"**{score}** ({breakdown})", 1)
                except:
                    continue
            
            if output_text != message.content:
                await message.author.send(output_text)
                return

        # Default DM Response: If no brackets or recognized strings were found
        await message.author.send(f"Hello! I am the Dice Proxy bot. Here is how you can use me:\n{MENU_TEXT}")
        return

    # 3. SERVER MESSAGES (Standard Gatekeeper/Whitelist check)
    # The gatekeeper also handles ignoring 'cc ' prompts so we can catch the Tupper webhook later.
    if not is_authorized(message, AUTHORIZED_GUILDS, AUTHORIZED_USERS):
        return

    # 4. SERVER COMMANDS & DICE PROCESSING
    matches = re.findall(r'\[\[(.*?)\]\]', message.content)
    if not matches:
        return

    # Help / Menu command
    if any(m.lower() in ["help", "menu"] for m in matches):
        await message.channel.send(MENU_TEXT)
        return

    # Installation command
    if any(m.lower() == "install" for m in matches):
        await message.channel.send(INSTALL_TEXT)
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
            try:
                await message.channel.send("⚠️ I couldn't DM you! Please open your DMs to receive the diagnostic report.")
            except:
                pass
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
            # Delete original trigger (Human or Tupper webhook)
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
