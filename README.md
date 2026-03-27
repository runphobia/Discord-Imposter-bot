# 🎮 Discord Imposter Game Bot

A multiplayer social deduction game bot for Discord where players try to identify the hidden imposter. Inspired by games like *Among Us*, this bot handles player management, role assignment, private messaging, and voting — all within your Discord server.

---

## 📌 Overview

This bot creates a simple but engaging party game experience:

- One player is secretly assigned as the **Imposter**
- All other players are **Crewmates** who receive a shared word
- Players discuss and try to expose the imposter
- A built-in poll system handles voting
- Results are calculated automatically

Perfect for friend groups, small communities, or casual Discord servers.

---

## 🚀 Features

### 🎮 Gameplay
- Slash command-based system (`/commands`)
- Automatic role assignment (Imposter vs Crewmates)
- Random category and word selection
- Private DM role delivery
- Built-in voting poll system
- Automatic win/loss detection

### 👥 Player Management
- Join/leave system
- Player list display (with embed UI)
- Max 5 players per game
- Minimum 2 players required

### 🧠 Game Logic
- Random imposter selection
- Category-based word generation
- Vote counting using Discord polls
- Full game state reset after each round

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **discord.py (v2+)**
- **python-dotenv**
- Native Discord features (slash commands, polls, embeds)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-project-folder>
