import os

BOT_LOG_LEVEL = int(os.environ.get("BOT_LOG_LEVEL", 25))
LOG_LEVEL = int(os.environ.get("LOG_LEVEL", 25))

_MONGO_URI = os.environ.get("MONGO_URI")

TOKEN = os.environ.get("TOKEN")