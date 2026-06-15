import os
import asyncio

# --- RENDER EVENT LOOP INITIALIZATION WRAPPER ---
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

# --- CONFIGURATION MAPPING ---
API_ID = 38138069
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"
BOT_TOKEN = "8852295639:AAGgw7gPVj5TjmrTNKmOLWfDtHaaP3V2XYA"
BOT_USERNAME = "Ban_X_All_bot"
OWNER_ID = 8237368993  
LOG_GROUP = -1003947649552  
START_IMG = "https://files.catbox.moe/srmw3t.mp4"

# --- FORCE JOIN CONFIGURATION (FSUB) ---
FSUB_CHANNELS = ["Ban_All_Update", "Genu_Bot_Support"]

# --- MONGO DB SETUP ---
MONGO_URL = "mongodb+srv://misssqn_db_user:Nova01@cluster0.6xxsrwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# srv_service_lookup hata diya taaki ConfigurationError permanently fix ho jaye
db_client = MongoClient(MONGO_URL)
db = db_client["BanXAllBot_DB"]
users_col = db["users"]
groups_col = db["groups"]

# --- WEB SERVER (RENDER KEEP ALIVE) ---
app = Flask('')
@app.route('/')
def home(): return "⚡ Ban X All Bot Is Ultra Flying Online ⚡"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- BUTTONS & PANELS MATRIX ---
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

# --- CAPTIONS GENERATOR ---
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

# --- UTILITY INTEGRATIONS ---
async def send_log(client, text):
    try:
        await client.send_message(LOG_GROUP, f"🛰 **[ LOG SYSTEM ]**\n\n{text}")
    except Exception as e:
        print(f"Logging Error: {e}")

async def check_force_join(client, user_id):
    not_joined = []
    for channel in FSUB_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception: pass
    return not_joined

# --- STRUCTURAL EVENT FLOWS ---
async def on_new_chat(client, message):
    if any(m.id == (await client.get_me()).id for m in message.new_chat_members):
        if not groups_col.find_one({"chat_id": message.chat.id}):
            groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})
        log_text = f"📥 **ADDED TO NEW GROUP**\n\n👥 **Group:** {message.chat.title}\n🆔 **ID:** `{message.chat.id}`"
        await send_log(client, log_text)

async def main_handler(client, message):
    if not message.from_user: return
    user_id = message.from_user.id
    
    # User / Group tracking database registration
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id, "name": message.from_user.first_name})
        await send_log(client, f"👤 **New User Registered:** {message.from_user.mention}\n🆔 **ID:** `{user_id}`")

    if message.chat.type != message.chat.type.PRIVATE:
        if not groups_col.find_one({"chat_id": message.chat.id}):
            groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})

    # Routing engine commands
    if message.chat.type == message.chat.type.PRIVATE and message.text and (message.text.startswith("/start") or message.text.startswith("/help")):
        # 🔒 FORCE JOIN CHECK SUBSYSTEM (FSUB)
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
                "Bot ko use karne ke liye aapko hamare official channels aur support group ko join karna hoga. "
                "Join karne ke baad **Verified & Continue** par click karein!",
                reply_markup=InlineKeyboardMarkup(fsub_buttons)
            )

        if message.text.startswith("/help"):
            caption = get_help_caption()
            markup = BACK_BUTTONS
        else:
            caption = get_start_caption(message.from_user.first_name)
            markup = START_BUTTONS

        try:
            await message.reply_video(video=START_IMG, caption=caption, reply_markup=markup)
        except Exception:
            await message.reply_text(text=caption, reply_markup=markup)

# --- BROADCAST SYSTEM (USER & GROUPS - NO PIN) ---
async def standard_broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ **Reply to a message to initiate standard broadcast (No Pin).**")
        
    progress = await message.reply_text("⚡ **Initiating Standard Global Broadcast (Users + Groups)...**")
    
    all_users = [user["user_id"] for user in users_col.find()]
    all_groups = [group["chat_id"] for group in groups_col.find()]
    targets = list(set(all_users + all_groups))
    
    success, failed = 0, 0
    for target in targets:
        try:
            await message.reply_to_message.copy(target)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(target)
            success += 1
        except Exception: 
            failed += 1
            
    await progress.edit(f"📢 **Standard Broadcast Complete!**\n\n✅ **Delivered Chats:** `{success}`\n❌ **Failed/Blocked:** `{failed}`")

# --- BROADCAST ALL SYSTEM (USER & GROUPS + AUTO PIN) ---
async def broadcast_all_and_pin(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ **Reply to a message to initiate advanced broadcast (With Auto-Pin).**")
        
    progress = await message.reply_text("💥 **Initiating Mega Broadcast & Global Auto-Pin Matrix...**")
    
    all_users = [user["user_id"] for user in users_col.find()]
    all_groups = [group["chat_id"] for group in groups_col.find()]
    targets = list(set(all_users + all_groups))
    
    success, failed = 0, 0
    for target in targets:
        try:
            copied_msg = await message.reply_to_message.copy(target)
            success += 1
            try: 
                await copied_msg.pin(both_sides=True)
            except: 
                pass  
        except FloodWait as e:
            await asyncio.sleep(e.value)
            copied_msg = await message.reply_to_message.copy(target)
            success += 1
            try: 
                await copied_msg.pin(both_sides=True)
            except: 
                pass
        except Exception: 
            failed += 1
            
    await progress.edit(f"🔥 **Mega Broadcast All Completed!**\n\n✅ **Total Sent & Pinned:** `{success}`\n❌ **Failed Destinations:** `{failed}`")

# --- CALLBACK INTERACTION ROUTER ---
async def cb_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    if query.data == "verify_fsub":
        unsubscribed = await check_force_join(client, user_id)
        if unsubscribed:
            return await query.answer("⚠️ Aapne abhi tak saare channels join nahi kiye hain! Join karke check karein.", show_alert=True)
        await query.answer("✅ Verification Successful!", show_alert=True)
        caption = get_start_caption(query.from_user.first_name)
        try:
            await query.message.delete()
            await client.send_video(chat_id=user_id, video=START_IMG, caption=caption, reply_markup=START_BUTTONS)
        except Exception:
            await client.send_message(chat_id=user_id, text=caption, reply_markup=START_BUTTONS)
            
    elif query.data == "help_data":
        caption = get_help_caption()
        try: await query.edit_message_caption(caption=caption, reply_markup=BACK_BUTTONS)
        except Exception: await query.edit_message_text(text=caption, reply_markup=BACK_BUTTONS)
        
    elif query.data == "guide_data":
        caption = get_guide_caption()
        try: await query.edit_message_caption(caption=caption, reply_markup=BACK_BUTTONS)
        except Exception: await query.edit_message_text(text=caption, reply_markup=BACK_BUTTONS)
        
    elif query.data == "start_data":
        caption = get_start_caption(query.from_user.first_name)
        try: await query.edit_message_caption(caption=caption, reply_markup=START_BUTTONS)
        except Exception: await query.edit_message_text(text=caption, reply_markup=START_BUTTONS)

# --- CORE LIGHTNING BANALL PROTOCOL ---
async def ban_all(client, message):
    if message.chat.type == message.chat.type.PRIVATE:
        return await message.reply_text("❌ This command can only be executed within groups!")
    bot_member = await client.get_chat_member(message.chat.id, "me")
    if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
        return await message.reply_text("❌ Admin Access Denied! Please grant me 'Ban Users' permissions.")

    user_who_fired = message.from_user
    user_id = user_who_fired.id if user_who_fired else None
    await send_log(client, f"🚨 **CYCLONE PURGE INITIATED**\n**Group:** {message.chat.title}")
    msg = await message.reply_text("🚀 **Spawning parallel processing threads...**")

    async def fast_ban(user_id_to_ban):
        try:
            await client.ban_chat_member(message.chat.id, user_id_to_ban)
            return True
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.ban_chat_member(message.chat.id, user_id_to_ban)
                return True
            except: return False
        except Exception: return False

    tasks = []
    me = await client.get_me()
    async for member in client.get_chat_members(message.chat.id):
        if member.status in ["administrator", "creator"] or member.user.id == me.id:
            continue
        tasks.append(fast_ban(member.user.id))

    if not tasks: return await msg.edit("❌ **No non-admin members found to clear!**")
    await msg.edit(f"🔥 **Purging `{len(tasks)}` members instantly...**")
    results = await asyncio.gather(*tasks)
    count = sum(1 for r in results if r is True)
    await msg.edit(f"⚡ **Purge Completed! Banned:** `{count}`\n🚪 Leaving group automatically...")
    
    if user_id:
        try: await client.send_message(chat_id=user_id, text=f"📊 **HISTORY REPORT**\n\nGroup: {message.chat.title}\nBanned: `{count}`")
        except: pass
    await asyncio.sleep(1)
    await client.leave_chat(message.chat.id)

# --- MAIN ASYNC CORE ENGINE RUNNER ---
async def main():
    keep_alive()  # Activates local web service for Render uptime
    print("Initializing Pyrogram Core Async Engine...")
    bot = Client("BanXAllBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    
    # Injecting event handler structures dynamically
    bot.add_handler(Client.on_message(filters.new_chat_members)(on_new_chat))
    bot.add_handler(Client.on_message(filters.incoming)(main_handler))
    bot.add_handler(Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))(standard_broadcast))
    bot.add_handler(Client.on_message(filters.command("broadcast_all") & filters.user(OWNER_ID))(broadcast_all_and_pin))
    bot.add_handler(Client.on_message(filters.command("banall"))(ban_all))
    bot.add_handler(Client.on_callback_query()(cb_handler))
    
    await bot.start()
    print("Bot is fully live, verified, and stable on Render! 🚀")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    loop.run_until_complete(main())
