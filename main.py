import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# --- CONFIGURATION ---
API_ID = 38138069
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"
BOT_TOKEN = "8852295639:AAGgw7gPVj5TjmrTNKmOLWfDtHaaP3V2XYA"
BOT_USERNAME = "Ban_X_All_bot"
OWNER_ID = 8237368993  
LOG_GROUP = -1003947649552  
START_IMG = "https://files.catbox.moe/srmw3t.mp4"

# --- FORCE JOIN CONFIG ---
FSUB_CHANNELS = ["Ban_All_Update", "Genu_Bot_Support"]

# --- MONGO DB SETUP ---
MONGO_URL = "mongodb+srv://misssqn_db_user:Nova01@cluster0.6xxsrwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db_client = MongoClient(MONGO_URL)
db = db_client["BanXAllBot_DB"]
users_col = db["users"]
groups_col = db["groups"]

# --- WEB SERVER (FOR HIBERNATION BYPASS ON RENDER) ---
app = Flask('')
@app.route('/')
def home(): return "⚡ Ban X All Bot Is Ultra Flying Online ⚡"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.daemon = True  # Thread safe exit handle karne ke liye
    t.start()

# Bot Initialization
bot = Client("BanXAllBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- UTILS ---
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
        except Exception:
            pass
    return not_joined

# --- BUTTONS ---
START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Add Me To Your Group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [
        InlineKeyboardButton("👤 Owner", url="https://t.me/CoderNova"),
        InlineKeyboardButton("🎧 All Bot Support", url="https://t.me/Genu_Bot_Support/119")
    ],
    [
        InlineKeyboardButton("🛠 Help & Commands", callback_data="help_data"),
        InlineKeyboardButton("📖 Guide", callback_data="guide_data")
    ]
])

BACK_BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="start_data")]])

def get_start_caption(name):
    return (
        f"╔═════════════════════════╗\n"
        f"   ✨ **WELCOME {name.upper()}** ✨\n"
        f"╚═════════════════════════╝\n\n"
        f"🚀 **Welcome to the Ultimate Ban X All Bot!**\n\n"
        f"⚡ I am engineered to clean up groups at lightning-fast speed. "
        f"Give me rights, use the power, and clear unwanted users instantly.\n\n"
        f"🏷 **Status:** Active & Ready\n"
        f"👑 **Maintained By:** @CoderNova"
    )

# --- HANDLERS ---

@bot.on_message(filters.new_chat_members)
async def on_new_chat(client, message):
    if any(m.id == (await client.get_me()).id for m in message.new_chat_members):
        if not groups_col.find_one({"chat_id": message.chat.id}):
            groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})
            
        log_text = (
            f"📥 **ADDED TO NEW GROUP**\n\n"
            f"👥 **Group Name:** {message.chat.title}\n"
            f"🆔 **Group ID:** `{message.chat.id}`\n"
            f"👤 **Added By:** {message.from_user.mention if message.from_user else 'Unknown'}"
        )
        await send_log(client, log_text)

@bot.on_message(filters.incoming)
async def main_handler(client, message):
    if not message.from_user: return
    user_id = message.from_user.id
    
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id, "name": message.from_user.first_name})
        await send_log(client, f"👤 **New User Registered:** {message.from_user.mention}\n🆔 **ID:** `{user_id}`")

    if message.chat.type != message.chat.type.PRIVATE:
        if not groups_col.find_one({"chat_id": message.chat.id}):
            groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})

    if message.chat.type == message.chat.type.PRIVATE and message.text and message.text.startswith("/start"):
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
                "Niche diye gaye saare buttons par click karke join karein aur verify karein!",
                reply_markup=InlineKeyboardMarkup(fsub_buttons)
            )

        caption = get_start_caption(message.from_user.first_name)
        try:
            await message.reply_video(video=START_IMG, caption=caption, reply_markup=START_BUTTONS)
        except Exception:
            await message.reply_text(text=caption, reply_markup=START_BUTTONS)

@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def standard_broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ **Reply to a message to initiate standard broadcast (No Pin).**")
    
    progress = await message.reply_text("⚡ **Initiating Standard Broadcast...**")
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
            
    await progress.edit(f"📢 **Broadcast Complete!**\n\n✅ **Delivered:** `{success}`\n❌ **Failed/Blocked:** `{failed}`")

@bot.on_message(filters.command("broadcast_all") & filters.user(OWNER_ID))
async def broadcast_all_and_pin(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ **Reply to a message to initiate advanced broadcast (With Pin).**")
        
    progress = await message.reply_text("💥 **Initiating Mega Broadcast & Auto-Pin...**")
    all_users = [user["user_id"] for user in users_col.find()]
    all_groups = [group["chat_id"] for group in groups_col.find()]
    targets = list(set(all_users + all_groups))
    
    success, failed = 0, 0
    for target in targets:
        try:
            copied_msg = await message.reply_to_message.copy(target)
            success += 1
            try: await copied_msg.pin(both_sides=True)
            except: pass  
        except FloodWait as e:
            await asyncio.sleep(e.value)
            copied_msg = await message.reply_to_message.copy(target)
            success += 1
            try: await copied_msg.pin(both_sides=True) 
            except: pass
        except Exception:
            failed += 1
            
    await progress.edit(f"🔥 **Mega Broadcast Completed!**\n\n✅ **Total Sent & Pinned:** `{success}`\n❌ **Failed:** `{failed}`")

@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    if query.data == "verify_fsub":
        unsubscribed = await check_force_join(client, user_id)
        if unsubscribed:
            return await query.answer("⚠️ Aapne abhi tak saare channels join nahi kiye hain!", show_alert=True)
        
        await query.answer("✅ Success! Verified.", show_alert=True)
        caption = get_start_caption(query.from_user.first_name)
        try:
            await query.message.delete()
            await client.send_video(chat_id=user_id, video=START_IMG, caption=caption, reply_markup=START_BUTTONS)
        except Exception:
            await client.send_message(chat_id=user_id, text=caption, reply_markup=START_BUTTONS)

    elif query.data == "help_data":
        help_text = (
            f"╔═════════════════════════╗\n"
            f"      🛠 **HELP & COMMANDS** \n"
            f"╚═════════════════════════╝\n\n"
            f"⚡ **Group Commands:**\n"
            f"📍 `/banall` - Bans all non-admin members instantly.\n\n"
            f"⚡ **Owner Commands:**\n"
            f"📍 `/broadcast` - Send message to all users & chats.\n"
            f"📍 `/broadcast_all` - Send, copy, and pin to all users & chats."
        )
        await query.edit_message_caption(caption=help_text, reply_markup=BACK_BUTTONS)
        
    elif query.data == "guide_data":
        guide_text = (
            f"╔═════════════════════════╗\n"
            f"          📖 **BOT GUIDE** \n"
            f"╚═════════════════════════╝\n\n"
            f"1️⃣ **Add me** to your target group.\n"
            f"2️⃣ Promote me to **Administrator** status.\n"
            f"3️⃣ Ensure I have the **Ban Users** permission.\n"
            f"4️⃣ Type `/banall` in the group chat.\n\n"
            f"⚠️ *Note: Admins cannot be banned.*"
        )
        await query.edit_message_caption(caption=guide_text, reply_markup=BACK_BUTTONS)
        
    elif query.data == "start_data":
        caption = get_start_caption(query.from_user.first_name)
        await query.edit_message_caption(caption=caption, reply_markup=START_BUTTONS)

@bot.on_message(filters.command("banall"))
async def ban_all(client, message):
    if message.chat.type == message.chat.type.PRIVATE:
        return await message.reply_text("❌ This command can only be executed within groups!")

    bot_member = await client.get_chat_member(message.chat.id, "me")
    if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
        return await message.reply_text("❌ Admin Access Denied! Please grant me 'Ban Users' permissions.")

    user_who_fired = message.from_user
    user_id = user_who_fired.id if user_who_fired else None
    
    await send_log(client, f"🚨 **CYCLONE PURGE INITIATED**\n**Group:** {message.chat.title}\n**Triggered By:** {user_who_fired.mention if user_who_fired else 'Unknown'}")
    msg = await message.reply_text("🚀 **Gathering target database... Spawning threads!**")

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

    if not tasks:
        return await msg.edit("❌ **No non-admin members found to ban!**")

    await msg.edit(f"🔥 **Purging `{len(tasks)}` members instantly...**")
    results = await asyncio.gather(*tasks)
    count = sum(1 for r in results if r is True)
    
    await msg.edit(f"⚡ **Cyclone Purge Completed!**\n\n✅ **Banned:** `{count}`\n🚪 **Status:** Automatically Leaving Chat...")
    await send_log(client, f"✅ **MEGA PURGE COMPLETE**\n**Group:** {message.chat.title}\n**Total Cleaned:** `{count}`")
    
    if user_id:
        history_caption = (
            f"╔════════════════════════════╗\n"
            f"      📊 **BAN-ALL ATTACK HISTORY** \n"
            f"╚════════════════════════════╝\n\n"
            f"👥 **Group Name:** {message.chat.title}\n"
            f"🆔 **Group ID:** `{message.chat.id}`\n"
            f"🔥 **Total Members Banned:** `{count}`\n\n"
            f"⏱ **Status:** Task Successfully Finished."
        )
        try: await client.send_message(chat_id=user_id, text=history_caption)
        except: pass

    await asyncio.sleep(1)
    await client.leave_chat(message.chat.id)

# --- MAIN ASYNC RUNNER FOR RENDER (CRITICAL ERROR FIX) ---
async def main():
    keep_alive()  # Flask server thread start karega
    print("Starting Pyrogram Client Engine...")
    await bot.start()
    print("Bot is ultra flying online! 🚀")
    await asyncio.Event().wait()  # Client loop ko active rakhega bina crash kiye

if __name__ == "__main__":
    asyncio.run(main())  # Loops handle correctly on Python 3.10+
