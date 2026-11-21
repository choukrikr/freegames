import json, os, requests

TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]
SEEN_FILE = "seen.json"

seen = set(json.load(open(SEEN_FILE))) if os.path.exists(SEEN_FILE) else set()

def notify(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": text})

def epic():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    r = requests.get(url, params={"locale": "en-US", "country": "DZ"}, timeout=20).json()
    for g in r["data"]["Catalog"]["searchStore"]["elements"]:
        offers = (g.get("promotions") or {}).get("promotionalOffers") or []
        if not offers:
            continue  # not free right now (upcoming offers are in a different field)
        slug = g.get("productSlug") or (g.get("offerMappings") or [{}])[0].get("pageSlug") or g.get("urlSlug")
        yield f"epic:{g['id']}", f"🎮 Epic free: {g['title']}\nhttps://store.epicgames.com/p/{slug}"

def steam():
    r = requests.get("https://www.gamerpower.com/api/giveaways",
                     params={"platform": "steam", "type": "game"}, timeout=20).json()
    if isinstance(r, list):
        for g in r:
            yield f"steam:{g['id']}", f"🎮 Steam free: {g['title']} (worth {g['worth']})\n{g['open_giveaway_url']}"

for source in (epic, steam):
    try:
        for key, msg in source():
            if key not in seen:
                notify(msg)
                seen.add(key)
    except Exception as e:
        print(source.__name__, "failed:", e)

json.dump(sorted(seen), open(SEEN_FILE, "w"))