import requests
import time
import os

# =========================
# TELEGRAM
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

gonderilen_canli = set()
gonderilen_over = set()

# =========================
# TELEGRAM SEND
# =========================

def telegram_gonder(mesaj):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }

    try:
        requests.post(url, data=data)
        print("Telegram gönderildi")
    except Exception as e:
        print("Telegram hata:", e)

# =========================
# ESPN DATA
# =========================

def maclari_cek():

    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        return data.get("events", [])
    except:
        return []

# =========================
# CANLI İY GOL AI
# =========================

def canli_ai(home, away, dakika, skor1, skor2):

    puan = 0

    if 10 <= dakika <= 20:
        puan += 20
    if 20 <= dakika <= 35:
        puan += 30
    if 35 <= dakika <= 45:
        puan += 20

    buyukler = ["Manchester","Liverpool","Arsenal","Chelsea",
                "Barcelona","Real Madrid","Bayern","Dortmund",
                "PSG","Inter","Milan","Juventus","Ajax",
                "Galatasaray","Fenerbahce","Besiktas"]

    for t in buyukler:
        if t.lower() in home.lower():
            puan += 15
        if t.lower() in away.lower():
            puan += 15

    if skor1 + skor2 >= 1:
        puan -= 20

    if puan > 95:
        puan = 95

    return puan

# =========================
# 2.5 ÜST AI
# =========================

def over_ai(home, away):

    puan = 50

    buyukler = ["Manchester","Liverpool","Arsenal","Chelsea",
                "Barcelona","Real Madrid","Atletico",
                "Bayern","Dortmund","Leverkusen",
                "PSG","Inter","Milan","Juventus","Napoli",
                "Ajax","Galatasaray","Fenerbahce","Besiktas"]

    for t in buyukler:
        if t.lower() in home.lower():
            puan += 20
        if t.lower() in away.lower():
            puan += 20

    if puan > 99:
        puan = 99

    return puan

# =========================
# CANLI ANALİZ
# =========================

def canli_analiz():

    maclar = maclari_cek()

    for m in maclar:

        try:
            c = m["competitions"][0]
            comp = c["competitors"]

            home = comp[0]["team"]["displayName"]
            away = comp[1]["team"]["displayName"]

            skor1 = int(comp[0]["score"])
            skor2 = int(comp[1]["score"])

            dakika_text = c["status"]["displayClock"]
            dakika = int(''.join(filter(str.isdigit, dakika_text)) or 0)

            if dakika == 0 or dakika > 45:
                continue

            if skor1 + skor2 >= 1:
                continue

            match_id = f"{home}_{away}_canli"

            if match_id in gonderilen_canli:
                continue

            ai = canli_ai(home, away, dakika, skor1, skor2)

            print("CANLI:", home, "-", away, "AI:", ai)

            if ai < 40:
                continue

            mesaj = f"""
🔥 CANLI İY GOL AI

⚽ {home} vs {away}
⏱ Dakika: {dakika}
📊 Skor: {skor1}-{skor2}
🤖 AI: {ai}/100

👉 İLK YARI GOL BEKLENTİSİ
"""

            telegram_gonder(mesaj)
            gonderilen_canli.add(match_id)

        except:
            pass

# =========================
# OVER 2.5 ANALİZ
# =========================

def over_analiz():

    maclar = maclari_cek()

    for m in maclar:

        try:
            c = m["competitions"][0]
            comp = c["competitors"]

            home = comp[0]["team"]["displayName"]
            away = comp[1]["team"]["displayName"]

            match_id = f"{home}_{away}_over"

            if match_id in gonderilen_over:
                continue

            ai = over_ai(home, away)

            print("OVER:", home, "-", away, "AI:", ai)

            if ai < 85:
                continue

            mesaj = f"""
🔥 2.5 ÜST AI

⚽ {home} vs {away}
🤖 AI: %{ai}

👉 2.5 ÜST POTANSİYEL
"""

            telegram_gonder(mesaj)
            gonderilen_over.add(match_id)

        except:
            pass

# =========================
# LOOP
# =========================

print("🤖 MULTI AI BOT AKTİF")

telegram_gonder("🤖 MULTI AI BOT AKTİF")

while True:

    try:
        canli_analiz()
        over_analiz()

    except Exception as e:
        print("Genel hata:", e)

    time.sleep(120)