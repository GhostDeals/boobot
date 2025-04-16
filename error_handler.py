from pathlib import Path
import traceback
import requests
import datetime
import os
from dotenv import load_dotenv

# Load .env to grab webhook URL
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def send_error_to_webhook(error_message: str):
    if not WEBHOOK_URL:
        print("? No webhook URL configured.")
        return

    timestamp = datetime.datetime.utcnow().isoformat()
    data = {
        "username": "BooBot Logger",
        "embeds": [
            {
                "title": "?? BooBot Error Logged",
                "description": f"```{error_message}```",
                "color": 16711680,
                "footer": {"text": f"Timestamp: {timestamp} UTC"}
            }
        ]
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"? Failed to send error to Discord: {e}")

async def handle_error(error: Exception):
    error_trace = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    send_error_to_webhook(error_trace[:1900])
