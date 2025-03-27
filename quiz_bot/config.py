import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

ROOT_DIR = Path(__file__).parent.parent
