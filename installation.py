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

**[ 1 ] Prerequisites**
* Python 3.8 or higher
* A Linux host (Raspberry Pi or any 24/7 server works great)
* A Discord account with access to the [Developer Portal](<https://discord.com/developers/applications>)

**[ 2 ] Clone the Repository**
```
git clone https://github.com/Zerick/SquareBracketDiceBot.git
cd SquareBracketDiceBot
```

**[ 3 ] Set Up the Environment**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**[ 4 ] Configure the Bot**
* Copy `config.py.example` to `config.py`
* Fill in your **Bot Token** in `config.py`
* Copy `whitelist.py.example` to `whitelist.py`
* Add your server ID to `AUTHORIZED_GUILDS` and your user ID to `AUTHORIZED_USERS`

**[ 5 ] Create Your Discord Bot**
* Go to the [Discord Developer Portal](<https://discord.com/developers/applications>)
* Create a **New Application**, then go to the **Bot** tab
* Enable **Message Content Intent** under Privileged Gateway Intents
* Copy your **Bot Token** and paste it into `config.py`

**[ 6 ] Invite the Bot to Your Server**
* In the Developer Portal go to **OAuth2 -> URL Generator**
* **Scopes:** `bot`
* **Permissions:** `Manage Messages`, `Manage Webhooks`, `View Channels`, `Send Messages`, `Embed Links`
* Use the generated URL to invite the bot to your server

**[ 7 ] Request Whitelist**
* **The Lock:** The bot ignores unlisted servers by default
* **The Key:** Once the bot is in your server, try `[[1d20]]`, then ask **Simonious** to whitelist your server ID

**[ 8 ] Run the Bot**
```
source venv/bin/activate
./main.py
```

**[ 9 ] Channel Permissions**
* Ensure the bot has **View Channel**, **Send Messages**, **Manage Messages**, **Manage Webhooks**, and **Read Message History** in any channel you want it active in

❓Need help? Contact <simonious@gmail.com> or open an issue on GitHub.
"""
