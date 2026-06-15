import os
import asyncio
import sys
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# --- BOT CONFIGURATION MATRIX ---
API_ID = 38138069
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"
BOT_TOKEN = "8852295639:AAE3rkvcRSjPZy1t8MykcoDhaqUmpD6Ffwo"
BOT_USERNAME = "Ban_X_All_bot"
OWNER_ID = 8237368993  
LOG_GROUP = -1003947649552  
START_IMG = "https://files.catbox.moe/srmw3t.mp4"

# --- FORCE JOIN CONFIGURATION ---
FSUB_CHANNELS = ["Ban_All_Update", "Genu_Bot_Support"]

# --- MONGO DB SETUP ---
MONGO_URL = "mongodb+srv://misssqn_db_user:Nova01@cluster0.6xxsrwq.mongodb.net/?retryWrites=true&w=majority"
db_client = MongoClient(MONGO_URL)
db = db_client["BanXAllBot_DB"]
users_col = db["users"]
groups_col = db["groups"]

# --- FLASK WEB SERVER ---
app = Flask('')

@app.route('/')
def home(): 
    return "⚡ Ban X All Bot Engine Status: ULTRA ACTIVE ⚡"

# --- PYROGRAM CLIENT ENGINE ---
bot = Client("BanXAllBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- INTERACTIVE BUTTON MATRICES (SMALL CAPS + EMOJIS) ---
START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [
        InlineKeyboardButton("👤 ᴏᴡɴᴇʀ", url="https://t.me/CoderNova"),
        InlineKeyboardButton("🎧 sᴜᴘᴘᴏʀᴛ", url="https://t.me/Genu_Bot_Support/119")
    ],
    [
        InlineKeyboardButton("🛠 ʜᴇʟᴘ & ᴄᴍᴅs", callback_data="help_data"),
        InlineKeyboardButton("📖 ᴅᴇᴘʟᴏʏ ɢᴜɪᴅᴇ", callback_data="guide_data")
    ]
])

BACK_BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴍᴇɴᴜ", callback_data="start_data")]])

FSUB_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📢 ʙᴀɴ ᴀʟʟ ᴜᴘᴅᴀᴛᴇ", url="https://t.me/Ban_All_Update")],
    [InlineKeyboardButton("🎧 ɢᴇɴᴜ ʙᴏᴛ sᴜᴘᴘᴏʀᴛ", url="https://t.me/Genu_Bot_Support")],
    [InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/+S0l_wstPbWwzMDUx")],
    [InlineKeyboardButton("🔄 ᴠᴇʀɪғɪᴇᴅ & ᴄᴏɴᴛɪɴᴜᴇ", callback_data="verify_fsub")]
])

# --- STYLISH CAPTION GENERATORS ---
def get_start_caption(name):
    return (
        f"╔═════════════════════════╗\n"
        f"   ✨ **wᴇʟᴄᴏᴍᴇ {name.upper()}** ✨\n"
        f"╚═════════════════════════╝\n\n"
        f"🚀 **Welcome to the Ultimate Ban X All Bot Engine!**\n\n"
        f"⚡ High-speed multi-threaded concurrency panel engineered to maintain, "
        f"secure, or wipe redundant group assets at cyclone speeds.\n\n"
        f"📊 **System Status:** `Operational [Active]`\n"
        f"👑 **Maintained By:** @CoderNova\n\n"
        f"👉 *Click the buttons below to interact with my internal subsystems.*"
    )

def get_fsub_caption():
    return (
        f"╔═════════════════════════╗\n"
        f"   ⛔ **ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ / Locked** ⛔\n"
        f"╚═════════════════════════╝\n\n"
        f"👋 **Hey there! Safety protocols activated.**\n\n"
        f"📢 You must join our official update channels and support grid "
        f"before using this high-performance clearance tool.\n\n"
        f"👉 *Join all networks below and click 'Verified & Continue'!*"
    )

def get_help_caption():
    return (
        f"╔═════════════════════════╗\n"
        f"    🛠 **ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs ᴄᴇɴᴛᴇʀ** \n"
        f"╚═════════════════════════╝\n\n"
        f"⚙️ **Group Management Unit:**\n"
        f"🔹 `/banall` — Sweeps all non-admin members immediately via parallel threads.\n\n"
        f"👑 **Administrative Master Matrix:**\n"
        f"🔹 `/broadcast` — Sends replied message to all users & groups (No Pin).\n"
        f"🔹 `/broadcast_all` — Sends broadcast + **Auto Pins** the message globally."
    )

def get_guide_caption():
    return (
        f"╔═════════════════════════╗\n"
        f"     📖 **ᴏᴘᴇʀᴀᴛɪᴏɴᴀʟ ᴅᴇᴘʟᴏʏ ɢᴜɪᴅᴇ** \n"
        f"╚═════════════════════════╝\n\n"
        f"📝 **Follow these guidelines to deploy and fire the core:**\n\n"
        f"1️⃣ Tap **Add Me To Your Group** to invite the asset.\n"
        f"2️⃣ Promote the instance into an **Administrator** role.\n"
        f"3️⃣ Ensure the **Ban Users** structural permission flag is ON.\n"
        f"4️⃣ Send `/banall` inside target group to trigger execution protocols.\n\n"
        f"🚫 *Note: Group creators and administrators are securely skipped.*"
    )

# --- UTILITY INTEGRATIONS ---
async def send_log(client, text):
    try: await client.send_message(LOG_GROUP, f"🛰 **[ LOG SYSTEM ]**\n\n{text}")
    except: pass

async def check_force_join(client, user_id):
    not_joined = []
    for channel in FSUB_CHANNELS:
        try: await client.get_chat_member(channel, user_id)
        except UserNotParticipant: not_joined.append(channel)
        except: pass
    return not_joined

# --- STRUCTURAL ENGINE LOGIC FLOORS ---
@bot.on_message(filters.new_chat_members)
async def on_new_chat(client, message):
    if any(m.id == (await client.get_me()).id for m in message.new_chat_members):
        if not groups_col.find_one({"chat_id": message.chat.id}):
            groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})
        await send_log(client, f"📥 **ADDED TO NEW GROUP**\n\n👥 **Group:** {message.chat.title}")

@bot.on_message(filters.private & (filters.command("start") | filters.command("help")))
async def start_and_help_handler(client, message):
    if not message.from_user: return
    user_id = message.from_user.id
    
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id, "name": message.from_user.first_name})
        await send_log(client, f"👤 **New User Registered:** {message.from_user.mention}")

    unsubscribed = await check_force_join(client, user_id)
    if unsubscribed:
        try: return await message.reply_video(video=START_IMG, caption=get_fsub_caption(), reply_markup=FSUB_BUTTONS)
        except: return await message.reply_text(text=get_fsub_caption(), reply_markup=FSUB_BUTTONS)

    if message.text.startswith("/help"):
        try: await message.reply_video(video=START_IMG, caption=get_help_caption(), reply_markup=BACK_BUTTONS)
        except: await message.reply_text(text=get_help_caption(), reply_markup=BACK_BUTTONS)
    else:
        try: await message.reply_video(video=START_IMG, caption=get_start_caption(message.from_user.first_name), reply_markup=START_BUTTONS)
        except: await message.reply_text(text=get_start_caption(message.from_user.first_name), reply_markup=START_BUTTONS)

@bot.on_message(filters.group, group=1)
async def database_group_tracker(client, message):
    if message.chat and message.chat.type != message.chat.type.PRIVATE:
        if not groups_col.find_one({"chat_id": message.chat.id}):
            groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})

# --- HIGH-PERFORMANCE ASYNC DISPATCHER ENGINE FOR BROADCAST ---
@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def standard_broadcast(client, message):
    if not message.reply_to_message: 
        return await message.reply_text("❌ **Please reply to a message you want to broadcast!**")
    
    progress = await message.reply_text("⚡ `Fetching network data routing...`")
    
    # Non-blocking async fetch from MongoDB mapping
    loop = asyncio.get_event_loop()
    user_ids = await loop.run_in_executor(None, lambda: [u["user_id"] for u in users_col.find()])
    group_ids = await loop.run_in_executor(None, lambda: [g["chat_id"] for g in groups_col.find()])
    targets = list(set(user_ids + group_ids))
    
    if not targets:
        return await progress.edit("❌ **Database registration matrix is empty!**")
        
    await progress.edit(f"🚀 `Broadcasting to {len(targets)} channels over safe queue...`")
    success = 0
    
    for target in targets:
        try:
            await message.reply_to_message.copy(target)
            success += 1
            await asyncio.sleep(0.3) # Avoid triggering structural TG spam blocks
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            try:
                await message.reply_to_message.copy(target)
                success += 1
            except: pass
        except Exception:
            pass
            
    await progress.edit(f"📢 **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!**\n\n✅ **Successfully sent to:** `{success}` chats.")

@bot.on_message(filters.command("broadcast_all") & filters.user(OWNER_ID))
async def broadcast_all_and_pin(client, message):
    if not message.reply_to_message: 
        return await message.reply_text("❌ **Please reply to a message you want to broadcast & pin!**")
    
    progress = await message.reply_text("⚡ `Fetching pin network deployment...`")
    
    loop = asyncio.get_event_loop()
    user_ids = await loop.run_in_executor(None, lambda: [u["user_id"] for u in users_col.find()])
    group_ids = await loop.run_in_executor(None, lambda: [g["chat_id"] for g in groups_col.find()])
    targets = list(set(user_ids + group_ids))
    
    if not targets:
        return await progress.edit("❌ **Database registration matrix is empty!**")
        
    await progress.edit(f"💥 `Pin Broadcasting to {len(targets)} targets...`")
    success = 0
    
    for target in targets:
        try:
            copied = await message.reply_to_message.copy(target)
            success += 1
            try: await copied.pin(both_sides=True)
            except: pass
            await asyncio.sleep(0.4)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            try:
                copied = await message.reply_to_message.copy(target)
                success += 1
                try: await copied.pin(both_sides=True)
                except: pass
            except: pass
        except Exception:
            pass
            
    await progress.edit(f"🔥 **ɢʟᴏʙᴀʟ ᴘɪɴ ʙʀᴏᴀᴅᴄᴀsᴛ ᴅᴏɴᴇ!**\n\n✅ **Delivered & Pinned in:** `{success}` chats.")

@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    if query.data == "verify_fsub":
        unsubscribed = await check_force_join(client, user_id)
        if unsubscribed: return await query.answer("⚠️ Join channels first!", show_alert=True)
        await query.answer("✅ Verified!")
        await query.message.delete()
        try: await client.send_video(chat_id=user_id, video=START_IMG, caption=get_start_caption(query.from_user.first_name), reply_markup=START_BUTTONS)
        except: await client.send_message(chat_id=user_id, text=get_start_caption(query.from_user.first_name), reply_markup=START_BUTTONS)
    elif query.data == "help_data":
        await query.edit_message_caption(caption=get_help_caption(), reply_markup=BACK_BUTTONS)
    elif query.data == "guide_data":
        await query.edit_message_caption(caption=get_guide_caption(), reply_markup=BACK_BUTTONS)
    elif query.data == "start_data":
        await query.edit_message_caption(caption=get_start_caption(query.from_user.first_name), reply_markup=START_BUTTONS)

@bot.on_message(filters.command("banall"))
async def ban_all(client, message):
    if message.chat.type == message.chat.type.PRIVATE: return
    bot_member = await client.get_chat_member(message.chat.id, "me")
    if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
        return await message.reply_text("❌ Mujhe admin banao aur 'Ban Users' permission allow karo!")
    
    user_who_fired = message.from_user
    user_id = user_who_fired.id if user_who_fired else None
    msg = await message.reply_text("🚀 **Spawning flood-safe deletion workers...**")
    
    sem = asyncio.Semaphore(5)
    me = await client.get_me()
    
    async def fast_ban(user_id_to_ban):
        async with sem:
            try:
                await client.ban_chat_member(message.chat.id, user_id_to_ban)
                return True
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                try:
                    await client.ban_chat_member(message.chat.id, user_id_to_ban)
                    return True
                except: return False
            except: return False

    tasks = []
    async for member in client.get_chat_members(message.chat.id):
        if member.status in ["administrator", "creator"] or member.user.id == me.id: 
            continue
        tasks.append(fast_ban(member.user.id))

    if not tasks: return await msg.edit("❌ No non-admin members found!")
    await msg.edit(f"🔥 **Safely clearing `{len(tasks)}` members...**")
    
    results = await asyncio.gather(*tasks)
    count = sum(1 for r in results if r is True)
    
    await msg.edit(f"⚡ **Purge Completed! Total Banned:** `{count}`\n🚪 Leaving group...")
    if user_id:
        try: await client.send_message(chat_id=user_id, text=f"📊 **REPORT:**\nGroup: {message.chat.title}\nBanned: `{count}`")
        except: pass
    await client.leave_chat(message.chat.id)

# --- WEB DRIVER STABILIZER FOR PYROGRAM INTERNAL LOOP ---
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, use_reloader=False, threaded=True)

flask_thread = Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

if __name__ == "__main__":
    print("🚀 TIMED EXECUTION: INITIATING PYROGRAM ENGINE...")
    bot.run()
