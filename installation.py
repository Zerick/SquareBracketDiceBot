# =============================================================================
# SquareBracketDiceBot (SBDB) — installation.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Contains the installation instructions displayed when a user types [[install]].
# =============================================================================


INSTALL_TEXT = """
### 🛠️ Bot Installation Checklist

**[ 1 ] Invite the Bot**
* Go to the [Discord Developer Portal](<https://discord.com/developers/applications>).
* Navigate to **OAuth2 -> URL Generator**.
* **Scopes:** `bot`, `webhook.incoming`.
* **Permissions:** `Manage Messages`, `Manage Webhooks`, `View Channels`, `Send Messages`, `Embed Links`.
* Use the generated link to add the bot to your server.

**[ 2 ] Request Whitelist**
* **The Lock:** The bot is locked by default and ignores unlisted servers.
* **The Key:** Once the bot is in your server, try to roll with `[[1d20]]`, then ask **Simonious** to whitelist the server. 

**[ 3 ] Channel Setup**
* **Permissions:** Ensure the bot has **View Channel** & **Read Message History**.
"""
