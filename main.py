import os
import asyncio
import sys

# --- RENDER/LINUX CONCURRENCY PROTECTION ---
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# --- BOT CONFIGURATION MATRIX ---
API_ID = 38138069
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"
BOT_TOKEN = "8852295639:AAGgw7gPVj5TjmrTNKmOLWfDtHaaP3V2XYA"
BOT_USERNAME = "Ban_X_All_bot"
OWNER_ID = 8237368993  
LOG_GROUP = -1003947649552  
START_IMG = "https://files.catbox.moe/srmw3t.mp4"

# --- FORCE JOIN CONFIGURATION ---
FSUB_CHANNELS = ["Ban_All_Update", "Genu_Bot_Support"]

# --- MONGO DB CONNECTION (FULLY REPAIR PARAMETERS) ---
# Yahan se '&appName=Cluster0' ko clear hata diya hai taaki pymongo module crash na ho.
MONGO_URL = "mongodb+srv://misssqn_db_user:Nova01@cluster0.6xxsrwq.mongodb.net/?retryWrites=true&w=majority"
db_client = MongoClient(MONGO_URL)
db = db_client["BanXAllBot_DB"]
users_col = db["users"]
groups_col = db["groups"]

# --- FLASK WEB SERVER (RENDER ALIVE AGENT) ---
app = Flask('')
@app.route('/')
def home(): 
    return "⚡ Ban X All Bot Is Ultra Flying Online ⚡"

def run(): 
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- INTERACTIVE BUTTON MATRICES ---
START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Add Me To Your Group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [
        InlineKeyboardButton("👤 Owner", url="https://t.me/CoderNova"),
        InlineKeyboardButton("🎧 Support Chat", url="https://t.me/Genu_Bot_Support/119")
    ],
    [
        InlineKeyboardButton("🛠 Help & Commands", callback_data="help_data"),
        InlineKeyboardButton("📖 Deploy Guide", callback_data="guide_data")
    ]
])

BACK_BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="start_data")]])

# --- DYNAMIC CAPTION GENERATORS ---
def get_start_caption(name):
    return (
        f"╔═════════════════════════╗\n"
        f"   ✨ **WELCOME {name.upper()}** ✨\n"
        f"╚═════════════════════════╝\n\n"
        f"🚀 **Welcome to the Ultimate Ban X All Bot Engine!**\n\n"
        f"⚡ High-speed multi-threaded concurrency panel engineered to maintain, "
        f"secure, or wipe redundant group assets at cyclone speeds.\n\n"
        f"📊 **System Status:** `Operational [Active]`\n"
        f"👑 **Maintained By:** @CoderNova\n\n"
        f"👉 *Click the buttons below to interact with my internal subsystems.*"
    )

def get_help_caption():
    return (
        f"╔═════════════════════════╗\n"
        f"      🛠 **HELP & COMMANDS CENTER** \n"
        f"╚═════════════════════════╝\n\n"
        f"⚡ **Group Infrastructure Commands:**\n"
        f"🔹 `/banall` — Sweeps all non-admin members immediately via parallel threads.\n\n"
        f"👑 **Administrative Owner Matrix:**\n"
        f"🔹 `/broadcast` — Sends replied message to all users & groups (No Pin).\n"
        f"🔹 `/broadcast_all` — Sends replied message to all users & groups + **Auto Pins** the message globally."
    )

def get_guide_caption():
    return (
        f"╔═════════════════════════╗\n"
        f"       📖 **OPERATIONAL DEPLOY GUIDE** \n"
        f"╚═════════════════════════╝\n\n"
        f"📝 **How to correctly configure and fire the Ban All engine:**\n\n"
        f"1️⃣ Click **Add Me To Your Group** button to invite the bot instance.\n"
        f"2️⃣ Promote the bot directly into an **Administrator** role.\n"
        f"3️⃣ Ensure the **Ban Users** structural control flag is enabled.\n"
        f"4️⃣ Type `/banall` in the target group to activate cleanup protocols.\n\n"
        f"🚫 **Safety Note:** Group creators and administrators are automatically skipped."
    )

# --- SYSTEM LOGGER & FSUB CHECKS ---
async def send_log(client, text):
    try: 
        await client.send_message(LOG_GROUP, f"🛰 **[ LOG SYSTEM ]**\n\n{text}")
    except: 
        pass

async def check_force_join(client, user_id):
    not_joined = []
    for channel in FSUB_CHANNELS:
        try: 
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant: 
            not_joined.append(channel)
        except: 
            pass
    return not_joined

# --- STRUCTURAL INTERCEPTORS & HANDLERS ---
async def on_new_chat(client, message):
    if any(m.id == (await client.get_me()).id for m in message.new_chat_members):
        if not groups_col.find_one({"chat_id": message.chat.id}):
            groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})
        await send_log(client, f"📥 **ADDED TO NEW GROUP**\n\n👥 **Group:** {message.chat.title}")

async def start_and_help_handler(client, message):
    if not message.from_user: return
    user_id = message.from_user.id
    
    # Auto-Registration Flow
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id, "name": message.from_user.first_name})
        await send_log(client, f"👤 **New User Registered:** {message.from_user.mention}")

    # Force Join Restriction Validation
    unsubscribed = await check_force_join(client, user_id)
    if unsubscribed:
        fsub_buttons = [
            [InlineKeyboardButton("📢 Ban All Update", url="https://t.me/Ban_All_Update")],
            [InlineKeyboardButton("🎧 Genu Bot Support", url="https://t.me/Genu_Bot_Support")],
            [InlineKeyboardButton("💬 Support Chat (Join Req)", url="https://t.me/+S0l_wstPbWwzMDUx")],
            [InlineKeyboardButton("🔄 Verified & Continue", callback_data="verify_fsub")]
        ]
        return await message.reply_text(
            "❌ **Access Denied! / Access Restricted**\n\n"
            "Bot ko use karne ke liye aapko hamare channels ko join karna hoga. Join karke confirm karein!", 
            reply_markup=InlineKeyboardMarkup(fsub_buttons)
        )

    if message.text.startswith("/help"):
        await message.reply_text(text=get_help_caption(), reply_markup=BACK_BUTTONS)
    else:
        try: 
            await message.reply_video(video=START_IMG, caption=get_start_caption(message.from_user.first_name), reply_markup=START_BUTTONS)
        except: 
            await message.reply_text(text=get_start_caption(message.from_user.first_name), reply_markup=START_BUTTONS)

async def database_group_tracker(client, message):
    if message.chat and message.chat.type != message.chat.type.PRIVATE:
        if not groups_col.find_one({"chat_id": message.chat.id}):
            groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})

# --- BROADCAST SYSTEM PANEL ---
async def standard_broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ **Reply to a message to broadcast.**")
    progress = await message.reply_text("⚡ **Standard Global Broadcast Running...**")
    targets = list(set([u["user_id"] for u in users_col.find()] + [g["chat_id"] for g in groups_col.find()]))
    success = 0
    for target in targets:
        try:
            await message.reply_to_message.copy(target)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(target)
            success += 1
        except: pass
    await progress.edit(f"📢 **Broadcast Complete! Sent to `{success}` chats.**")

async def broadcast_all_and_pin(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ **Reply to a message to broadcast with Pin.**")
    progress = await message.reply_text("💥 **Mega Broadcast & Auto-Pin Matrix Running...**")
    targets = list(set([u["user_id"] for u in users_col.find()] + [g["chat_id"] for g in groups_col.find()]))
    success = 0
    for target in targets:
        try:
            copied = await message.reply_to_message.copy(target)
            success += 1
            try: await copied.pin(both_sides=True)
            except: pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            copied = await message.reply_to_message.copy(target)
            success += 1
            try: await copied.pin(both_sides=True)
            except: pass
        except: pass
    await progress.edit(f"🔥 **Mega Broadcast Completed! Sent & Pinned in `{success}` targets.**")

# --- CALLBACK INTERACTIONS ROUTER ---
async def cb_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    if query.data == "verify_fsub":
        unsubscribed = await check_force_join(client, user_id)
        if unsubscribed: 
            return await query.answer("⚠️ Aapne abhi tak saare channels join nahi kiye hain!", show_alert=True)
        await query.answer("✅ Verification Successful!")
        await query.message.delete()
        await client.send_message(chat_id=user_id, text=get_start_caption(query.from_user.first_name), reply_markup=START_BUTTONS)
    elif query.data == "help_data":
        await query.edit_message_text(text=get_help_caption(), reply_markup=BACK_BUTTONS)
    elif query.data == "guide_data":
        await query.edit_message_text(text=get_guide_caption(), reply_markup=BACK_BUTTONS)
    elif query.data == "start_data":
        await query.edit_message_text(text=get_start_caption(query.from_user.first_name), reply_markup=START_BUTTONS)

# --- LIGHTNING PURGE ENGINE ---
async def ban_all(client, message):
    if message.chat.type == message.chat.type.PRIVATE: return
    bot_member = await client.get_chat_member(message.chat.id, "me")
    if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
        return await message.reply_text("❌ Mujhe admin banao aur 'Ban Users' permission allow karo!")
    
    msg = await message.reply_text("🚀 **Spawning structural deletion threads...**")
    me = await client.get_me()
    count = 0
    
    async for member in client.get_chat_members(message.chat.id):
        if member.status in ["administrator", "creator"] or member.user.id == me.id: 
            continue
        try:
            await client.ban_chat_member(message.chat.id, member.user.id)
            count += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except: 
            pass
            
    await msg.edit(f"⚡ **Purge Completed! Total Banned:** `{count}`\n🚪 Leaving group automatically...")
    await client.leave_chat(message.chat.id)

# --- MAIN ASYNC CORE ENGINE RUNNER (WITH AUTOMATIC RETRY LAUNCH) ---
async def main():
    keep_alive()  
    print("Pre-loading Structural Pipeline Routing...")
    bot = Client("BanXAllBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    
    # ROUTING SYSTEM SPECIFICATION
    bot.add_handler(Client.on_message(filters.new_chat_members)(on_new_chat))
    bot.add_handler(Client.on_message(filters.private & (filters.command("start") | filters.command("help")))(start_and_help_handler))
    bot.add_handler(Client.on_message(filters.group)(database_group_tracker), group=1)
    bot.add_handler(Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))(standard_broadcast))
    bot.add_handler(Client.on_message(filters.command("broadcast_all") & filters.user(OWNER_ID))(broadcast_all_and_pin))
    bot.add_handler(Client.on_message(filters.command("banall"))(ban_all))
    bot.add_handler(Client.on_callback_query()(cb_handler))
    
    print("Bot launch system sequence initiated...")
    
    while True:
        try:
            await bot.start()
            print("🚀 BOT IS LIVE, SECURE AND RUNNING ON RENDER ENGINE!")
            break
        except FloodWait as tg_cooldown:
            print(f"⚠️ Launch Protection Triggered! Telegram launch cooldown active. Retrying in {tg_cooldown.value}s...")
            await asyncio.sleep(tg_cooldown.value)
            
    while True: 
        await asyncio.sleep(3600)

if __name__ == "__main__":
    loop.run_until_complete(main())
