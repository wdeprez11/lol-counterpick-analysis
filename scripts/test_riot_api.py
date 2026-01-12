import os, requests, time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("RIOT_API_KEY")

url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/wild/iwnl"
headers = {"X-Riot-Token": api_key}

# print(requests.get(url, headers=headers).json())

data = requests.get(url, headers=headers).json()
puuid = data["puuid"]

matches_url = ("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"f"{puuid}/ids?start=0&count=1")
matches_id_list = requests.get(matches_url, headers=headers).json()
matches_list = []
for match_id in matches_id_list:
    match_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(match_url, headers=headers)

    if response.status_code == 200:
        matches_list.append(response.json())
    else:
        print(f"Error {response.status_code} on match {match_id}")

    time.sleep(1)

match = matches_list[0]
# print(match.keys())
# print(match["info"].keys())
# print(match["info"]["participants"][0].keys())

participants = match["info"]["participants"]

player = next(p for p in participants if p["puuid"] == puuid)
# print(player["championName"], player["teamPosition"], player["win"])

ROLE_TO_COL = {
    ("TOP", 100): "blueTopChamp",
    ("JUNGLE", 100): "blueJungleChamp",
    ("MIDDLE", 100): "blueMiddleChamp",
    ("BOTTOM", 100): "blueADCChamp",
    ("UTILITY", 100): "blueSupportChamp",

    ("TOP", 200): "redTopChamp",
    ("JUNGLE", 200): "redJungleChamp",
    ("MIDDLE", 200): "redMiddleChamp",
    ("BOTTOM", 200): "redADCChamp",
    ("UTILITY", 200): "redSupportChamp",
}


rows = []

for match in matches_list:
    row = {
        "blueTopChamp": None,
        "blueJungleChamp": None,
        "blueMiddleChamp": None,
        "blueADCChamp": None,
        "blueSupportChamp": None,
        "redTopChamp": None,
        "redJungleChamp": None,
        "redMiddleChamp": None,
        "redADCChamp": None,
        "redSupportChamp": None,
        "bResult": None
    }

    for participant in match["info"]["participants"]:
        key = (participant["teamPosition"], participant["teamId"])
        if key in ROLE_TO_COL:
            col = ROLE_TO_COL[key]
            row[col] = participant["championName"]

            if participant["teamId"] == 100:
                row["bResult"] = participant["win"]

    rows.append(row)



print(rows)
