import asyncio
import time
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from rich.console import Console

from Music.config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    MONGO_DB_URI,
    SESSION_NAME,
    SUDO_USERS,
    OWNER_ID,
    LOG_GROUP_ID,
    CHANNEL,
    GROUP,
    UPSTREAM_BRANCH,
    UPSTREAM_REPO
)
from Music.converter.cli import app, userbot
from Music.MusicUtilities.helpers.tasks import install_requirements

console = Console()
boottime = time.time()

# Global variabel
db = AsyncIOMotorClient(MONGO_DB_URI).wbb
SUDOERS = SUDO_USERS
OWNER = OWNER_ID
aiohttpsession = None
BOT_ID = 0
BOT_NAME = ""
BOT_USERNAME = ""
ASSID = 0
ASSNAME = ""
ASSUSERNAME = ""
ASSMENTION = ""

# Fungsi untuk load sudoers
async def load_sudoers():
    global SUDOERS
    print("[INFO]: LOADING SUDO USERS")
    sudoersdb = db.sudoers
    sudoers_data = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers_list = sudoers_data["sudoers"] if sudoers_data else []
    for user_id in SUDO_USERS:
        if user_id not in sudoers_list:
            sudoers_list.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"}, {"$set": {"sudoers": sudoers_list}}, upsert=True
            )
    SUDOERS = list(set(SUDO_USERS + sudoers_list))
    print("[INFO]: LOADED SUDO USERS")

# Fungsi untuk info bot & userbot
async def all_info(app, client):
    global BOT_ID, BOT_NAME, BOT_USERNAME
    global ASSID, ASSNAME, ASSMENTION, ASSUSERNAME
    getme = await app.get_me()
    getme1 = await client.get_me()
    BOT_ID = getme.id
    ASSID = getme1.id
    BOT_NAME = f"{getme.first_name} {getme.last_name or ''}".strip()
    BOT_USERNAME = getme.username
    ASSNAME = f"{getme1.first_name} {getme1.last_name or ''}".strip()
    ASSUSERNAME = getme1.username
    ASSMENTION = getme1.mention

# Fungsi update dari Git
async def check_git_updates():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        console.print("[red] Git repo tidak valid, menginisialisasi ulang...")
        repo = Repo.init()
        origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(UPSTREAM_BRANCH, origin.refs[UPSTREAM_BRANCH])
        repo.heads[UPSTREAM_BRANCH].set_tracking_branch(origin.refs[UPSTREAM_BRANCH])
        repo.heads[UPSTREAM_BRANCH].checkout(True)
    except GitCommandError:
        console.print("[red] Git command error.")
        return

    origin = repo.remote("origin")
    origin.fetch(UPSTREAM_BRANCH)
    try:
        origin.pull(UPSTREAM_BRANCH)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    
    await install_requirements("pip3 install --no-cache-dir -r requirements.txt")
    console.print("[green] Git client update completed.")

# Fungsi utama
async def main():
    global aiohttpsession
    print("[INFO]: STARTING BOT")
    await load_sudoers()
    await check_git_updates()

    print("[INFO]: STARTING BOT CLIENT")
    await app.start()

    print("[INFO]: STARTING ASSISTANT CLIENT")
    await userbot.start()

    print("[INFO]: LOADING BOT & ASSISTANT INFO")
    await all_info(app, userbot)

    aiohttpsession = ClientSession()
    print("[INFO]: BOT IS UP AND RUNNING!")

# Eksekusi
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
