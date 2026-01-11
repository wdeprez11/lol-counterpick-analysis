import os, requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("RIOT_API_KEY")

url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/wild/iwnl"
headers = {"X-Riot-Token": api_key}

# print(requests.get(url, headers=headers).json())

data = requests.get(url, headers=headers).json()
puuid = data["puuid"]

match_url = ("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"f"{puuid}/ids?start=0&count=20")

print(requests.get(match_url, headers=headers).json())