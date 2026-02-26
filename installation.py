# =============================================================================
# SquareBracketDiceBot (SBDB) — installation.py
# =============================================================================
# Author:   Simonious A.K.A. Zerick
# Contact:  simonious@gmail.com
# GitHub:   https://github.com/Zerick/SquareBracketDiceBot
# License:  MIT
# -----------------------------------------------------------------------------
# Contains all installation help text displayed via [[install]] commands.
# =============================================================================

INSTALL_TEXT = """
### 🛠️ SBDB Installation Guide

Use these subcommands for step-by-step help:
**[[install setup]]** — Clone the repo, set up Python environment and config files
**[[install bot]]** — Create your Discord bot, set intents, get your token
**[[install service]]** — Run SBDB as a systemd service so it starts on boot
**[[install permissions]]** — Set channel permissions and get whitelisted

📖 Full documentation: <https://github.com/Zerick/SquareBracketDiceBot>
❓ Contact: <simonious@gmail.com>
"""

INSTALL_SETUP_TEXT = """
### ⚙️ Step 1 — Environment Setup

**Prerequisites**
* Python 3.8 or higher
* A Linux host (Raspberry Pi or any 24/7 server)

**Clone the repository**
```
git clone https://github.com/Zerick/SquareBracketDiceBot.git
cd SquareBracketDiceBot
```

**Create and activate a virtual environment**
```
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies**
```
pip install -r requirements.txt
```

**Set up config files**
```
cp config.py.example config.py
cp whitelist.py.example whitelist.py
```
* Edit `config.py` and paste in your Bot Token
* Edit `whitelist.py` and add your server ID to `AUTHORIZED_GUILDS` and your user ID to `AUTHORIZED_USERS`

Next: **[[install bot]]**
"""

INSTALL_BOT_TEXT = """
### 🤖 Step 2 — Discord Bot Setup

**Create your bot**
* Go to <https://discord.com/developers/applications>
* Click **New Application** and give it a name
* Go to the **Bot** tab
* Click **Reset Token**, copy it and paste it into `config.py`

**Enable required intents**
* On the **Bot** tab scroll down to **Privileged Gateway Intents**
* Enable **Message Content Intent** ← this is critical, the bot won't work without it

**Invite the bot to your server**
* Go to **OAuth2 → URL Generator**
* **Scopes:** `bot`
* **Bot Permissions:** `Manage Messages`, `Manage Webhooks`, `View Channels`, `Send Messages`, `Embed Links`
* Copy the generated URL and open it in your browser to invite the bot

Next: **[[install service]]**
"""

INSTALL_SERVICE_TEXT = """
### ⚡ Step 3 — Running as a System Service

Running SBDB as a systemd service means it starts automatically on boot and restarts if it crashes.

**Copy the service file**
```
sudo cp sbdb.service /etc/systemd/system/
```

**Edit the service file** to match your install path
```
sudo nano /etc/systemd/system/sbdb.service
```

**Enable and start the service**
```
sudo systemctl daemon-reload
sudo systemctl enable sbdb
sudo systemctl start sbdb
```

**Check it's running**
```
sudo systemctl status sbdb
```

**View live logs**
```
journalctl -u sbdb -f
```

Next: **[[install permissions]]**
"""

INSTALL_PERMISSIONS_TEXT = """
### 🛡️ Step 4 — Permissions and Whitelist

**Channel permissions**
Ensure the bot has these permissions in every channel you want it active:
* View Channel
* Send Messages
* Manage Messages
* Manage Webhooks
* Read Message History
* Embed Links

**Get whitelisted**
* The bot ignores all servers not on its whitelist by default
* Once your bot is running and in your server, try typing `[[1d20]]`
* If it doesn't respond, your server ID needs to be added to `whitelist.py`
* Add it yourself under `AUTHORIZED_GUILDS`, or contact **Simonious** if using the hosted version

**Test your setup**
```
[[1d20]]        — basic roll
[[check_perms]] — verify bot permissions in this channel
[[version]]     — confirm the bot is running and check its version
[[help]]        — see all available commands
```
"""
