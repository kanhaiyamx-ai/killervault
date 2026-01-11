import asyncio
import sqlite3
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
SUPPORT = os.getenv("SUPPORT_USERNAME")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ---------- DATABASE ----------
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

# ---------- FORCE SUBSCRIBE ----------
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

# ---------- START ----------
@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    ref = message.text.split(" ")

    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    db.commit()

    if not await is_subscribed(user_id):
        await message.answer(
            "🔒 **Access Restricted**\n\n"
            "To use this bot, you must join the official channel.",
            reply_markup=join_keyboard(),
            parse_mode="Markdown"
        )
        return

    if len(ref) > 1:
        referrer = int(ref[1])
        if referrer != user_id:
            cur.execute("SELECT referrer FROM users WHERE user_id=?", (user_id,))
            if cur.fetchone()[0] is None:
                cur.execute("UPDATE users SET referrer=? WHERE user_id=?", (referrer, user_id))
                cur.execute("UPDATE users SET points = points + 5 WHERE user_id=?", (referrer,))
                db.commit()

    await main_menu(message)

# ---------- VERIFY ----------
@dp.callback_query(F.data == "verify")
async def verify(call: CallbackQuery):
    if await is_subscribed(call.from_user.id):
        await call.message.edit_text(
            "✅ **Access Verified**\n\n"
            "✨ Access granted successfully.\n\n"
            "🔗 Earn points by inviting users\n"
            "🎁 Redeem premium rewards from the store\n"
            "🔓 Unlock exclusive methods and tools",
            parse_mode="Markdown",
            reply_markup=main_menu_kb()
        )
    else:
        await call.answer("Join the channel first.", show_alert=True)

# ---------- MAIN MENU ----------
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
        [InlineKeyboardButton(text="🎁 Redeem Rewards", callback_data="redeem")],
        [InlineKeyboardButton(text="🔗 Invite & Earn", callback_data="invite")],
        [InlineKeyboardButton(text="🆘 Support", callback_data="support")]
    ])

async def main_menu(message: Message):
    await message.answer(
        "🏠 **Main Menu**",
        reply_markup=main_menu_kb(),
        parse_mode="Markdown"
    )

# ---------- PROFILE ----------
@dp.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    cur.execute("SELECT points FROM users WHERE user_id=?", (call.from_user.id,))
    points = cur.fetchone()[0]
    await call.message.edit_text(
        f"👤 **Your Profile**\n\n"
        f"⭐ Points: {points}",
        parse_mode="Markdown",
        reply_markup=main_menu_kb()
    )

# ---------- INVITE ----------
@dp.callback_query(F.data == "invite")
async def invite(call: CallbackQuery):
    link = f"https://t.me/{(await bot.me()).username}?start={call.from_user.id}"
    await call.message.edit_text(
        f"🔗 **Invite & Earn**\n\n"
        f"Earn **5 points** per referral.\n\n"
        f"Your link:\n{link}",
        parse_mode="Markdown",
        reply_markup=main_menu_kb()
    )

# ---------- SUPPORT ----------
@dp.callback_query(F.data == "support")
async def support(call: CallbackQuery):
    await call.message.edit_text(
        f"🆘 **Support & Help**\n\n"
        f"Contact:\n{SUPPORT}",
        parse_mode="Markdown",
        reply_markup=main_menu_kb()
    )

# ---------- REDEEM ----------
@dp.callback_query(F.data == "redeem")
async def redeem(call: CallbackQuery):
    await call.message.edit_text(
        "🎁 **Redeem Rewards**\n\n"
        "✨ *Use your points to unlock exclusive methods, tools, and subscriptions.*\n\n"
        "⚡ *Points are deducted instantly after successful redemption.*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
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

@dp.callback_query(F.data == "back")
async def back(call: CallbackQuery):
    await call.message.edit_text("🏠 **Main Menu**", reply_markup=main_menu_kb(), parse_mode="Markdown")

# ---------- RUN ----------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
