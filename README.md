# KILL4R Access Bot

A professional Telegram referral-based access bot built with **aiogram v3**.

This bot uses a **points & rewards system** combined with **mandatory channel subscription**
to grow Telegram communities organically.

---

## ✨ Features

- 🔒 Force Subscribe (mandatory channel join)
- 👥 Referral system (+ points per referral)
- 🎁 Rewards & redeem system
- ⭐ Points tracking
- 🆘 Support section
- 🚫 Prevents access without joining channel
- ⚡ Optimized for Railway (24/7 uptime)

---

## 🧠 How It Works

1. User starts the bot
2. User must join the official Telegram channel
3. Access is verified
4. User invites others using a referral link
5. Points are earned for each valid referral
6. Points can be redeemed for rewards

---

## 🛠 Tech Stack

- Python 3.10+
- aiogram v3
- SQLite (default, can be upgraded to PostgreSQL)
- Railway hosting

---

## 🚀 Deployment (Railway)

1. Fork or clone this repository
2. Create a Railway project
3. Add environment variables:
   - `BOT_TOKEN`
   - `CHANNEL_ID`
   - `SUPPORT_USERNAME`
4. Set start command:
   ```bash
   python bot.py
