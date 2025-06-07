import asyncio
import pytz
from pyrogram import Client
from pytgcalls import idle
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Music.config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    AUTO_LEAVE,
    LOG_GROUP_ID
)
from Music import app, client, BOT_NAME, ASSNAME
from Music.MusicUtilities.database.functions import clean_restart_stage
from Music.MusicUtilities.database.queue import get_active_chats, remove_active_chat
from Music.MusicUtilities.helpers.autoleave import leave_from_inactive_call
from Music.MusicUtilities.tgcallsrun import run


# Inisialisasi Scheduler
scheduler = AsyncIOScheduler(timezone=pytz.utc)


async def load_start():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[INFO]: Sending restart status...")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**✅ Bot berhasil direstart.**",
            )
        except Exception as e:
            print(f"[WARN]: Tidak bisa kirim pesan restart: {e}")

    try:
        chats = await get_active_chats()
        for chat in chats:
            try:
                await remove_active_chat(int(chat["chat_id"]))
            except Exception as e:
                print(f"[WARN]: Gagal hapus chat aktif {chat}: {e}")
    except Exception as e:
        print(f"[ERROR]: Tidak bisa ambil chat aktif: {e}")

    try:
        await app.send_message(LOG_GROUP_ID, "**✅ Bot berhasil dijalankan.**")
    except Exception as e:
        print(f"[WARN]: Gagal kirim log: {e}")

    if AUTO_LEAVE:
        print("[INFO]: Menjalankan auto-leave scheduler...")
        scheduler.add_job(leave_from_inactive_call, "interval", seconds=AUTO_LEAVE)
        scheduler.start()


async def main():
    print(f"[INFO]: Memulai BOT sebagai {BOT_NAME}")
    await app.start()

    print(f"[INFO]: Memulai Assistant sebagai {ASSNAME}")
    await client.start()

    await load_start()

    print("[INFO]: Memulai panggilan suara...")
    run()

    await idle()

    print("[INFO]: Bot dihentikan.")
    await app.stop()
    await client.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO]: Dihentikan oleh pengguna.")
