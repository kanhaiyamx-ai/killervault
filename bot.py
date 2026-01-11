import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest

# ==================================================
# 🔒 TEMPORARY HARDCODED CONFIG (STABLE)
# ==================================================

BOT_TOKEN = "8374406264:AAE19EeB7ZiXo71YYXFXcet2UDFZsTNaZrQ"   # ⚠️ put token here
CHANNEL_ID = -1003636897874                  # your channel id
SUPPORT_USERNAME = "@KILL4R_UR"

# ==================================================
# BOT SETUP
# ==================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==================================================
# DATABASE
# ==================================================

db = sqlite3.connect("users.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    points INTEGER DEFAULT 0,
    referrer INTEGER
)
""")
db.commit()

# ==================================================
# SAFE EDIT (ERROR HANDLING)
# ==================================================

async def safe_edit(message, text, reply_markup=None):
    try:
        await message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise

# ==================================================
# FORCE SUBSCRIBE
# ==================================================

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

def join_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Join Official Channel", url="https://t.me/KILL4R_OSINT")],
        [InlineKeyboardButton(text="✅ Verify Access", callback_data="verify")]
    ])

# ==================================================
# KEYBOARDS
# ==================================================

def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
        [InlineKeyboardButton(text="🎁 Redeem Rewards", callback_data="redeem")],
        [InlineKeyboardButton(text="🔗 Invite & Earn", callback_data="invite")],
        [InlineKeyboardButton(text="🆘 Support", callback_data="support")]
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back", callback_data="back")]
    ])

# ==================================================
# UI TEXT (UNDERGROUND STYLE)
# ==================================================

MAIN_PANEL = (
    "🕶️ **KILL4R Private Access**\n\n"
    "You are inside the system.\n\n"
    "🎯 Earn points via referrals\n"
    "🧠 Unlock private methods & tools\n"
    "🎁 Redeem premium rewards\n\n"
    "Proceed using the controls below."
)

REDEEM_HEADER = (
    "🎁 **Redeem Rewards**\n\n"
    "✨ *Use your points to unlock exclusive methods, tools, and subscriptions.*\n\n"
    "⚡ *Points are deducted instantly after successful redemption.*"
)

# ==================================================
# /start
# ==================================================

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    args = message.text.split()

    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    db.commit()

    if not await is_subscribed(user_id):
        await message.answer(
            "🔒 **Access Restricted**\n\n"
            "Join the official channel to unlock the system.",
            parse_mode="Markdown",
            reply_markup=join_keyboard()
        )
        return

    # Referral
    if len(args) > 1:
        try:
            referrer = int(args[1])
            if referrer != user_id:
                cur.execute("SELECT referrer FROM users WHERE user_id=?", (user_id,))
                if cur.fetchone()[0] is None:
                    cur.execute("UPDATE users SET referrer=? WHERE user_id=?", (referrer, user_id))
                    cur.execute("UPDATE users SET points = points + 5 WHERE user_id=?", (referrer,))
                    db.commit()
        except:
            pass

    await message.answer(
        MAIN_PANEL,
        parse_mode="Markdown",
        reply_markup=main_menu_kb()
    )

# ==================================================
# VERIFY
# ==================================================

@dp.callback_query(F.data == "verify")
async def verify(call: CallbackQuery):
    if await is_subscribed(call.from_user.id):
        await safe_edit(call.message, MAIN_PANEL, main_menu_kb())
    else:
        await call.answer("Join the channel first.", show_alert=True)

# ==================================================
# PROFILE
# ==================================================

@dp.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    cur.execute("SELECT points FROM users WHERE user_id=?", (call.from_user.id,))
    points = cur.fetchone()[0]

    await safe_edit(
        call.message,
        f"👤 **Your Profile**\n\n"
        f"🆔 ID: `{call.from_user.id}`\n"
        f"⭐ Points: **{points}**",
        main_menu_kb()
    )

# ==================================================
# INVITE
# ==================================================

@dp.callback_query(F.data == "invite")
async def invite(call: CallbackQuery):
    bot_username = (await bot.me()).username
    link = f"https://t.me/{bot_username}?start={call.from_user.id}"

    await safe_edit(
        call.message,
        "🔗 **Invite & Earn**\n\n"
        "Earn **5 points** per valid referral.\n\n"
        f"Your referral link:\n`{link}`",
        main_menu_kb()
    )

# ==================================================
# SUPPORT
# ==================================================

@dp.callback_query(F.data == "support")
async def support(call: CallbackQuery):
    await safe_edit(
        call.message,
        f"🆘 **Support & Help**\n\n"
        f"For any issue, contact:\n{SUPPORT_USERNAME}",
        main_menu_kb()
    )

# ==================================================
# REDEEM
# ==================================================

@dp.callback_query(F.data == "redeem")
async def redeem(call: CallbackQuery):
    await safe_edit(
        call.message,
        REDEEM_HEADER,
        InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Insta → Gmail / Number | 20 pts", callback_data="m1")],
            [InlineKeyboardButton(text="Telegram User ID Tracker | 15 pts", callback_data="m2")],
            [InlineKeyboardButton(text="Private Methods & Tools | 30 pts", callback_data="m3")],
            [InlineKeyboardButton(text="Netflix (1 Month) | 30 pts", callback_data="m4")],
            [InlineKeyboardButton(text="AI Jailbreak Prompt | 20 pts", callback_data="m5")],
            [InlineKeyboardButton(text="Crunchyroll (1 Month) | 25 pts", callback_data="m6")],
            [InlineKeyboardButton(text="Prime Video (1 Month) | 20 pts", callback_data="m7")],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="back")]
        ])
    )

# ==================================================
# BACK
# ==================================================

@dp.callback_query(F.data == "back")
async def back(call: CallbackQuery):
    await safe_edit(call.message, MAIN_PANEL, main_menu_kb())

# ==================================================
# RUN
# ==================================================

async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
