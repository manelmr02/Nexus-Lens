import requests

_VERSION = None
_CHAMPIONS = None
_ITEMS = None

def get_latest_version() -> str:
    global _VERSION
    if _VERSION:
        return _VERSION
    try:
        r = requests.get("https://ddragon.leagueoflegends.com/api/versions.json", timeout=5)
        _VERSION = r.json()[0]
    except Exception:
        _VERSION = "14.24.1"
    return _VERSION

def get_champion_data() -> dict:
    global _CHAMPIONS
    if _CHAMPIONS:
        return _CHAMPIONS
    v = get_latest_version()
    try:
        r = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{v}/data/en_US/champion.json", timeout=10)
        _CHAMPIONS = r.json().get("data", {})
    except Exception:
        _CHAMPIONS = {}
    return _CHAMPIONS

def get_items_data() -> dict:
    global _ITEMS
    if _ITEMS:
        return _ITEMS
    v = get_latest_version()
    try:
        r = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{v}/data/en_US/item.json", timeout=10)
        _ITEMS = r.json().get("data", {})
    except Exception:
        _ITEMS = {}
    return _ITEMS

def champion_img_url(champion_name: str) -> str:
    v = get_latest_version()
    return f"https://ddragon.leagueoflegends.com/cdn/{v}/img/champion/{champion_name}.png"

def item_img_url(item_id: int) -> str:
    v = get_latest_version()
    return f"https://ddragon.leagueoflegends.com/cdn/{v}/img/item/{item_id}.png"

def profile_icon_url(icon_id: int) -> str:
    v = get_latest_version()
    return f"https://ddragon.leagueoflegends.com/cdn/{v}/img/profileicon/{icon_id}.png"

def get_item_name(item_id: int) -> str:
    items = get_items_data()
    item = items.get(str(item_id))
    return item["name"] if item else f"Item {item_id}"
