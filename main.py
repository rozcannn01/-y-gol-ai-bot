import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def telegram_gonder(mesaj):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }

    requests.post(url, data=data)

print("🤖 CANLI İY GOL AI AKTİF")

telegram_gonder("🤖 CANLI İY GOL AI AKTİF")

while True:

    print("Bot çalışıyor...")

    time.sleep(60)