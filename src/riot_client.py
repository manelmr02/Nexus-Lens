import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

REGION_MAP = {
    "EUW": {"routing": "europe", "platform": "euw1"},
    "EUNE": {"routing": "europe", "platform": "eun1"},
    "NA": {"routing": "americas", "platform": "na1"},
    "KR": {"routing": "asia", "platform": "kr"},
    "BR": {"routing": "americas", "platform": "br1"},
    "JP": {"routing": "asia", "platform": "jp1"},
    "TR": {"routing": "europe", "platform": "tr1"},
    "OCE": {"routing": "sea", "platform": "oc1"},
    "LAN": {"routing": "americas", "platform": "la1"},
    "LAS": {"routing": "americas", "platform": "la2"},
}

class NexusClient:
    def __init__(self, region: str = "EUW"):
        self.api_key = self._load_api_key()
        if not self.api_key:
            raise ValueError("RIOT_API_KEY no encontrada en .env ni en Streamlit secrets")
        self.headers = {"X-Riot-Token": self.api_key}
        self.set_region(region)

    def _load_api_key(self) -> str:
        try:
            import streamlit as st
            return st.secrets.get("RIOT_API_KEY", os.getenv("RIOT_API_KEY", ""))
        except Exception:
            return os.getenv("RIOT_API_KEY", "")

    def set_region(self, region: str):
        r = REGION_MAP.get(region.upper(), REGION_MAP["EUW"])
        self.routing_region = r["routing"]
        self.platform_region = r["platform"]

    def _get(self, url: str, retries: int = 3) -> dict:
        for attempt in range(retries):
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 2))
                time.sleep(wait)
                continue
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code in (404, 400):
                resp.raise_for_status()
            time.sleep(1)
        resp.raise_for_status()
        return {}

    def get_puuid_by_riot_id(self, game_name: str, tag_line: str) -> str:
        url = f"https://{self.routing_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return self._get(url)["puuid"]

    def get_summoner_by_puuid(self, puuid: str) -> dict:
        url = f"https://{self.platform_region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        try:
            return self._get(url)
        except Exception:
            return {}

    def get_rank_by_summoner_id(self, summoner_id: str) -> list:
        url = f"https://{self.platform_region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        try:
            return self._get(url)
        except Exception:
            return []

    def get_champion_mastery(self, puuid: str, count: int = 10) -> list:
        url = f"https://{self.platform_region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count={count}"
        try:
            return self._get(url)
        except Exception:
            return []

    def get_match_ids(self, puuid: str, count: int = 20, queue: int = None) -> list:
        url = f"https://{self.routing_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
        if queue:
            url += f"&queue={queue}"
        return self._get(url)

    def get_match_details(self, match_id: str) -> dict:
        url = f"https://{self.routing_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        return self._get(url)

    def get_match_timeline(self, match_id: str) -> dict:
        url = f"https://{self.routing_region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
        try:
            return self._get(url)
        except Exception:
            return {}
