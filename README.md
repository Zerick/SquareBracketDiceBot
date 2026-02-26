# 🎲 SquareBracketDiceBot (SBDB)

A specialized Discord bot designed for seamless, inline dice rolling. Inspired by the square-bracket mechanics of Roll20 and Foundry VTT, SBDB lets users roll dice naturally mid-sentence without command prefixes.

---

## ✨ Features

* **Inline Rolling** — Trigger rolls mid-sentence using `[[1d20+5]]`
* **Discord Proxying** — Deletes your bracketed message and reposts it as you with the result inline
* **Hover Tooltips** — Results show the total; hover to see the full dice breakdown
* **Verbose Mode** — Add `v` to any roll for inline breakdown: `[[5d6kh3v]]`
* **Advantage/Disadvantage** — `[[1d20a]]` and `[[1d20d]]` shorthand
* **Batch Rolling** — `[[10x3d6]]` sums N rolls; `[[10t3d6]]` shows individual results
* **Drop/Keep** — `[[5d6kh3]]`, `[[4d6dh1]]`, `[[6d8dl2]]` and more
* **Dice Statistics** — `[[stats 5d6kh3]]` shows min, max, mean, median and std dev
* **Bug Reporting** — `[[bug]] describe the issue` logs directly to the bot owner
* **Gatekeeper Logic** — Whitelist-based access, Tupperbox-compatible ignore rules
* **Rate Limiting** — 20 rolls per 60 seconds per user, admins exempt
* **Admin Controls** — `[[verbose]]` toggle via DM to monitor rolls in the terminal
* **Systemd Service** — Runs as a background service, restarts on crash

---

## 🎲 Dice Syntax

| Expression | Description |
|---|---|
| `[[2d6]]` | Roll two 6-sided dice |
| `[[1d20+5]]` | Roll with modifier |
| `[[5d6kh3]]` | Keep highest 3 |
| `[[4d6dh1]]` | Drop highest 1 |
| `[[6d8dl2]]` | Drop lowest 2 |
| `[[1d20a]]` | Advantage (roll twice, keep highest) |
| `[[1d20d]]` | Disadvantage (roll twice, keep lowest) |
| `[[10x3d6]]` | Roll 3d6 ten times, sum results |
| `[[10t3d6]]` | Roll 3d6 ten times, show each result |
| `[[5d6kh3v]]` | Verbose — show full breakdown inline |
| `[[stats 1d20]]` | Show statistics for any expression |

---

## 🚀 Installation

### Prerequisites
* Python 3.8+
* Linux host (Raspberry Pi or any 24/7 server)
* Discord Bot Token with **Message Content Intent** enabled

### Quick Setup

**1. Clone and install**
```bash
git clone https://github.com/Zerick/SquareBracketDiceBot.git
cd SquareBracketDiceBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Configure**
```bash
cp config.py.example config.py
cp whitelist.py.example whitelist.py
```
Edit `config.py` with your bot token. Edit `whitelist.py` with your server and user IDs.

**3. Discord Developer Portal**
* Create a bot at <https://discord.com/developers/applications>
* Enable **Message Content Intent** under Privileged Gateway Intents
* Invite with scopes: `bot` and permissions: `Manage Messages`, `Manage Webhooks`, `View Channels`, `Send Messages`, `Embed Links`

**4. Run**
```bash
./main.py
```

### Running as a System Service
```bash
sudo cp sbdb.service /etc/systemd/system/
sudo nano /etc/systemd/system/sbdb.service  # update paths
sudo systemctl daemon-reload
sudo systemctl enable sbdb
sudo systemctl start sbdb
```

For full in-Discord installation help type `[[install]]` after the bot is running.

---

## 📁 File Structure

| File | Description |
|---|---|
| `main.py` | Entry point, message routing |
| `dice_engine.py` | Core dice rolling logic |
| `handlers.py` | Message processing, webhook, bug reporting |
| `gatekeeper.py` | Whitelist, rate limiting, Tupperbox filters |
| `stats.py` | Dice statistics via Monte Carlo simulation |
| `logger_config.py` | Logging setup |
| `version.py` | Single source of truth for bot version |
| `config.py.example` | Template for config.py |
| `whitelist.py.example` | Template for whitelist.py |
| `sbdb.service` | Systemd service file |
| `test_suite.py` | Offline test runner |
| `test_cases.py` | Test case definitions |

---

## 🧪 Running Tests
```bash
source venv/bin/activate
./test_suite.py
```

---

## 📜 License
MIT — see [LICENSE](LICENSE)

**Author:** Simonious A.K.A. Zerick
**Contact:** simonious@gmail.com
**GitHub:** <https://github.com/Zerick/SquareBracketDiceBot>
