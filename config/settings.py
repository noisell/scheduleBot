"""Local configuration. Never commit real values to this module."""
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
OWNER_USER_ID = int(os.getenv("OWNER_USER_ID", "0"))
YOOMONEY_RECEIVER = os.getenv("YOOMONEY_RECEIVER", "")
