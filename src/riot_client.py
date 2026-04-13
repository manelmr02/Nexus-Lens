import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NexusClient:
    def __init__(self):
        self.api_key = os.getenv("RIOT_API_KEY")
        if not self.api_key:
            raise ValueError("RIOT_API_KEY no encontrada en el archivo .env")
        
        self.headers = {"X-Riot-Token": self.api_key}
        self.routing_region = "europe" 

    def get_puuid_by_riot_id(self, game_name: str, tag_line: str) -> str:
        url = f"https://{self.routing_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["puuid"]

    def get_match_ids(self, puuid: str, count: int = 1) -> list:
        url = f"https://{self.routing_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_match_details(self, match_id: str) -> dict:
        url = f"https://{self.routing_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_match_timeline(self, match_id: str) -> dict:
        url = f"https://{self.routing_region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return {}
        return response.json()
