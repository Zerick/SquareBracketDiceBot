INSTALL_TEXT = """
### 🛠️ Bot Installation Checklist

**1. Invite the Bot**
* Go to the [Discord Developer Portal](https://discord.com/developers/applications).
* **OAuth2 -> URL Generator**.
* **Scopes:** `bot`, `webhook.incoming`.
* **Permissions:** `Manage Messages`, `Manage Webhooks`, `Read Message History`, `Send Messages`, `Embed Links`.
* Use the generated link to add the bot to your server.

**2. Authorize (Whitelist)**
* The bot is locked by default. To unlock it:
* 🎲 Type `[[1d20]]` in the new server.
* 📋 Contact bot owner and ask them to whitelist you for use of this bot

**3. Channel Setup**
* Ensure the bot has 'View Channel' permissions.
* The bot creates its own Webhook automatically on the first roll.
"""
