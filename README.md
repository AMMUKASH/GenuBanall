# 🚀 BAN X ALL BOT (ULTRA CYCLONE PURGE)

An ultra-fast, multi-threaded Telegram group cleaner bot built using the **Pyrogram** framework. Powered by **MongoDB** for persistent storage, integrated with a secure **Force Join (FSub) System**, and armed with an advanced **Parallel Concurrency Architecture** capable of purging thousands of members within seconds without triggering standard API freezes.

---

## 🚀 One-Click Deployment

Aap niche diye gaye button par click karke is bot ko direct **Render** par host kar sakte hain:

[![Deploy to Render](https://render.com/images/deploy-to-render.svg)](https://render.com/deploy?repo=https://github.com/YourUsername/YourRepoName)

> ⚠️ **Important:** Button use karne se pehle URL me `YourUsername/YourRepoName` ko apni GitHub repository ke username aur repo name se replace zaroor kar lein.

---

## ⚡ Key Features

* 🌪 **Cyclone Purge Logic:** Uses `asyncio.gather` parallelism to execute hundreds of ban requests simultaneously, sweeping 5k+ groups in under 25 seconds.
* 🗄 **MongoDB Backend:** Automatically tracks and saves user bases and added groups securely across server restarts.
* 🎯 **Dual Broadcast Matrix:** * `/broadcast`: Standard notification delivery to all registered users and channels.
    * `/broadcast_all`: Advanced mega-delivery that automatically pins the message across all chats.
* 🔒 **3-Tier Force Join (FSub):** Restricts bot access in PM until users join your designated network channels and support chats.
* 📊 **DM Attack History:** Sends a detailed performance report directly to the administrator's private inbox after completing a group sweep.
* 🎛 **Stylish Interactive UI:** Fully customizable text layout headers with inline dynamic command guides.

---

## 🛠 Configuration Variables (Environment Variables on Render)

Jab aap Render par deploy karenge, toh aapko **Environment Variables** me ye saari fields fill karni hongi:

| Variable | Description |
| :--- | :--- |
| `API_ID` | Your Telegram App API ID obtained from my.telegram.org. |
| `API_HASH` | Your Telegram App API Hash configuration string. |
| `BOT_TOKEN` | Bot API Token generated via Telegram's @BotFather. |
| `MONGO_URL` | Complete MongoDB Atlas connection URI string. |
| `LOG_GROUP` | Numeric Telegram Channel/Group ID for monitoring logs. |
| `START_IMG` | Direct URL link to the startup video panel animation (.mp4). |

---

## 🕹 Commands & Usage Matrix

### 👥 Public / Group Commands
* `/start` - Initializes the bot interaction in Private (Triggers Force Join & Media Menu Panels).
* `/banall` - Triggers the automated structural multi-threaded sweep inside groups.

### 👑 Owner Commands (Restricted to OWNER_ID)
* `/broadcast` - Copies the replied message to all users and channels inside the database.
* `/broadcast_all` - Copies and globally forces a PIN notification for the replied message across all targets.

---

## ⚙️ Render Web Service Settings (If doing Manual Setup)
Agar aap Render par web service manually create kar rahe hain, toh ye settings use karein:
* **Runtime:** `Python`
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `python main.py` (Ya aapki file ka jo bhi naam ho, jaise `python bot.py`)

---

## 📜 License & Disclaimers
This utility is intended for group administrative cleanups, migration, and stress testing scenarios. Please deploy ethically and comply with Telegram's Terms of Service. Maintained by [@CoderNova](https://t.me/CoderNova).
