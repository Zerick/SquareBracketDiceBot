# 🎲 SquareBracketDiceBot (SBDB)

A specialized Discord bot designed for seamless, inline dice rolling. Inspired by the square-bracket mechanics of Roll20 and Foundry VTT, this bot allows users to trigger rolls naturally within their roleplay sentences without command prefixes.

---

## ✨ Features

* **Inline Rolling:** Trigger rolls mid-sentence using `[[1d20+5]]`.
* **Discord Proxying:** Uses webhooks to delete your bracketed message and repost it as "you" with the result included.
* **Hover Tooltips:** In-channel results show the total; hover over the result to see the full dice breakdown.
* **Stealth Mode:** Matches Discord's dark theme background to minimize the "embed box" look.
* **Gatekeeper Logic:** Includes a "cc " ignore rule to prevent interference with other bots like Tupperbox.
* **Admin Controls:** Toggle terminal `[[verbose]]` mode via private message to monitor rolls in real-time.

---

## 🚀 Installation

### Prerequisites
* **Python 3.8+**
* **Linux any 24/7 host**
* **Discord Bot Token** (with `Message Content` and `Server Members` Intents enabled)

### Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Zerick/SquareBracketDiceBot.git](https://github.com/Zerick/SquareBracketDiceBot.git)
   cd SquareBracketDiceBot
