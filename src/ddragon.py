import requests

_VERSION = None
_CHAMPIONS = None
_ITEMS = None
_RUNES = None
_ITEM_NAME_MAP = None

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

def get_item_id_by_name(name: str) -> int | None:
    global _ITEM_NAME_MAP
    if _ITEM_NAME_MAP is None:
        items = get_items_data()
        _ITEM_NAME_MAP = {v["name"].lower(): int(k) for k, v in items.items()}
    return _ITEM_NAME_MAP.get(name.lower())

def get_rune_data() -> list:
    global _RUNES
    if _RUNES is not None:
        return _RUNES
    v = get_latest_version()
    try:
        r = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{v}/data/en_US/runesReforged.json", timeout=10)
        _RUNES = r.json()
    except Exception:
        _RUNES = []
    return _RUNES

def get_rune_by_key(key: str) -> dict | None:
    for tree in get_rune_data():
        if tree.get("key") == key:
            return {"name": tree["name"], "icon": tree["icon"], "is_tree": True}
        for slot in tree.get("slots", []):
            for rune in slot.get("runes", []):
                if rune.get("key") == key:
                    return rune
    return None

def rune_img_url(icon_path: str) -> str:
    return f"https://ddragon.leagueoflegends.com/cdn/img/{icon_path}"

def get_all_champion_names() -> list[str]:
    data = get_champion_data()
    return sorted(data.keys())

def get_champion_tags(champion_name: str) -> list[str]:
    data = get_champion_data()
    champ = data.get(champion_name, {})
    return champ.get("tags", [])
