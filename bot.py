import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest

# ================== CONFIG (HARDCODED) ==================
BOT_TOKEN = "8374406264:AAE19EeB7ZiXo71YYXFXcet2UDFZsTNaZrQ"
CHANNEL_ID = -1003636897874
SUPPORT_USERNAME = "@KILL4R_UR"
# ========================================================

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ------------------ STORAGE ------------------
users = {}        # user_id: {"points": int, "refs": int}
redeemed = {}     # user_id: set()

def get_user(uid: int):
    if uid not in users:
        users[uid] = {"points": 0, "refs": 0}
        redeemed[uid] = set()
    return users[uid]

# ------------------ FORCE SUBSCRIBE ------------------
async def is_member(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

# ------------------ SAFE EDIT ------------------
async def safe_edit(call: CallbackQuery, text, kb=None):
    try:
        await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except TelegramBadRequest:
        pass

# ------------------ KEYBOARDS ------------------
def join_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ JOIN CHANNEL", url="https://t.me/KILL4R_OSINT")],
        [InlineKeyboardButton(text="🔐 VERIFY MEMBERSHIP", callback_data="verify")]
    ])

def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 REWARD VAULT", callback_data="vault")],
        [
            InlineKeyboardButton(text="👤 PROFILE", callback_data="profile"),
            InlineKeyboardButton(text="🔗 REFERRALS", callback_data="referral")
        ],
        [InlineKeyboardButton(text="🛠 SUPPORT", callback_data="support")]
    ])

# ------------------ START ------------------
@dp.message(CommandStart())
async def start(message: Message):
    uid = message.from_user.id
    get_user(uid)

    if not await is_member(uid):
        await message.answer(
            "🛡️ **Welcome to KILL4R Private Access**\n\n"
            "_This bot is a restricted access system._\n\n"
            "⚡ **Join the official channel to unlock access.**",
            reply_markup=join_kb(),
            parse_mode="Markdown"
        )
        return

    await message.answer(
        "🛡️ **KILL4R PRIVATE ACCESS PANEL**\n\n"
        "_Welcome to the KILL4R vault._\n\n"
        "🧠 **Private methods & tools**\n"
        "🎁 **Exclusive rewards**\n"
        "🔗 **Referral-based progression**\n\n"
        "_Use the controls below to navigate the vault._",
        reply_markup=main_kb(),
        parse_mode="Markdown"
    )

# ------------------ VERIFY ------------------
@dp.callback_query(F.data == "verify")
async def verify(call: CallbackQuery):
    if await is_member(call.from_user.id):
        await safe_edit(
            call,
            "✅ **Access Verified**\n\n"
            "_You can now earn points and redeem rewards._",
            main_kb()
        )
    else:
        await call.answer("Join the channel first.", show_alert=True)

# ------------------ PROFILE ------------------
@dp.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    u = get_user(call.from_user.id)
    await safe_edit(
        call,
        f"👤 **USER PROFILE**\n\n"
        f"🆔 **User ID:** `{call.from_user.id}`\n"
        f"👤 **Handle:** @{call.from_user.username}\n\n"
        f"💎 **Points Available:** **{u['points']}**\n"
        f"🔗 **Referrals:** **{u['refs']}**\n\n"
        "_Invite users to unlock premium rewards._",
        InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅️ RETURN", callback_data="back")]]
        )
    )

# ------------------ REFERRAL ------------------
@dp.callback_query(F.data == "referral")
async def referral(call: CallbackQuery):
    bot_username = (await bot.me()).username
    uid = call.from_user.id
    await safe_edit(
        call,
        "🔗 **REFERRAL SYSTEM**\n\n"
        "⚡ **+5 Points per verified referral**\n\n"
        f"🎯 **Your referral link:**\n"
        f"`https://t.me/{bot_username}?start={uid}`",
        InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅️ RETURN", callback_data="back")]]
        )
    )

# ------------------ VAULT ------------------
@dp.callback_query(F.data == "vault")
async def vault(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1️⃣ Insta → Gmail / Number (20)", callback_data="noop")],
        [InlineKeyboardButton(text="2️⃣ Telegram ID Tracker (15)", callback_data="noop")],
        [InlineKeyboardButton(text="3️⃣ Private Methods (30)", callback_data="noop")],
        [InlineKeyboardButton(text="4️⃣ Netflix Premium (30)", callback_data="noop")],
        [InlineKeyboardButton(text="5️⃣ Crunchyroll Premium (25)", callback_data="noop")],
        [InlineKeyboardButton(text="6️⃣ Prime Video (20)", callback_data="noop")],
        [InlineKeyboardButton(text="7️⃣ Advanced AI Prompt (20)", callback_data="noop")],
        [InlineKeyboardButton(text="⬅️ RETURN", callback_data="back")]
    ])
    await safe_edit(
        call,
        "🎁 **REWARD VAULT**\n\n"
        "_Select a reward to view details._",
        kb
    )

# ------------------ SUPPORT ------------------
@dp.callback_query(F.data == "support")
async def support(call: CallbackQuery):
    await safe_edit(
        call,
        f"🛠️ **SUPPORT CENTER**\n\n"
        f"📩 **Contact:** {SUPPORT_USERNAME}",
        InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅️ RETURN", callback_data="back")]]
        )
    )

# ------------------ BACK ------------------
@dp.callback_query(F.data == "back")
async def back(call: CallbackQuery):
    await safe_edit(
        call,
        "🛡️ **KILL4R PRIVATE ACCESS PANEL**",
        main_kb()
    )

# ------------------ RUN ------------------
async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
