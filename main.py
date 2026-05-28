import requests
import time

# =========================
# TELEGRAM AYARLARI
# =========================

BOT_TOKEN = "8910671972:AAELwXlRHp_Y6uBVKCwn09L8qewNabwTMRo"
CHAT_ID = "8325310989"

# Aynı maç tekrar gönderilmesin
gonderilen = set()

# =========================
# TELEGRAM MESAJ
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
# CANLI MAÇLAR
# =========================

def canli_maclar():

    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/all/scoreboard"

    try:

        r = requests.get(url, timeout=10)

        print("Durum:", r.status_code)

        data = r.json()

        events = data.get("events", [])

        print("Canlı maç:", len(events))

        return events

    except Exception as e:

        print("API hata:", e)

        return []

# =========================
# AI HESAPLA
# =========================

def iy_ai(home, away, dakika):

    puan = 0

    # Dakika bonusları
    if 10 <= dakika <= 20:
        puan += 20

    if 20 <= dakika <= 35:
        puan += 30

    if 35 <= dakika <= 45:
        puan += 20

    # Büyük takım bonusları
    buyukler = [

        "Manchester",
        "Liverpool",
        "Arsenal",
        "Chelsea",

        "Barcelona",
        "Real Madrid",

        "Bayern",
        "Dortmund",

        "PSG",

        "Inter",
        "Milan",
        "Juventus",

        "Ajax",

        "Galatasaray",
        "Fenerbahce",
        "Besiktas"
    ]

    for takim in buyukler:

        if takim.lower() in home.lower():
            puan += 15

        if takim.lower() in away.lower():
            puan += 15

    # Max limit
    if puan > 95:
        puan = 95

    return puan

# =========================
# ANALİZ
# =========================

def analiz():

    maclar = canli_maclar()

    for mac in maclar:

        try:

            competition = mac["competitions"][0]

            dakika_text = competition["status"]["displayClock"]

            

            dakika = 0

            try:
                dakika = int(
                    ''.join(
                        filter(str.isdigit, dakika_text)
                    )
                )

            except:
                dakika = 0
            if dakika == 0:
                 continue

            # İlk yarı dışı alma
            if dakika > 45:
                continue

            competitors = competition["competitors"]

            home = competitors[0]["team"]["displayName"]
            away = competitors[1]["team"]["displayName"]

            skor1 = int(competitors[0]["score"])
            skor2 = int(competitors[1]["score"])

            # Sadece 0-0 maçlar
            if skor1 + skor2 >= 1:
                continue

            # Lig adı
            lig = "Canlı Maç"

            try:
                lig = competition["competition"]["displayName"]

            except:
                pass

            ai = iy_ai(home, away, dakika)

            print(
                home,
                "-",
                away,
                "| Dakika:",
                dakika,
                "| AI:",
                ai
            )

            # Filtre
            if ai < 40:
                continue

            # Aynı maçı tekrar atma
            unique_id = f"{home}_{away}"

            if unique_id in gonderilen:
                continue

            mesaj = f"""
🔥 CANLI İY GOL AI

🏆 Lig: {lig}

⚽ {home} vs {away}

⏱ Dakika: {dakika}

📊 Skor:
{skor1} - {skor2}

🤖 AI Gücü: {ai}/100

━━━━━━━━━━━━━━━

📊 CANLI ANALİZ

• İlk yarı tempo yüksek
• Baskılı oyun tespit edildi
• Gol ihtimali güçlü
• Hücum eğilimi pozitif

━━━━━━━━━━━━━━━

✅ SİNYAL:
İLK YARI GOL Bekleniyor
"""

            telegram_gonder(mesaj)

            gonderilen.add(unique_id)

            print("Sinyal gönderildi")

            time.sleep(2)

        except Exception as e:

            print("Maç hata:", e)

# =========================
# BAŞLAT
# =========================

print("🤖 CANLI İY GOL AI BAŞLADI")

telegram_gonder("🤖 CANLI İY GOL AI AKTİF")

while True:

    try:

        analiz()

    except Exception as e:

        print("Genel hata:", e)

    # 2 dakika bekle
    time.sleep(120)