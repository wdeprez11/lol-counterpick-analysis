### League,Year,Season,Type,blueTeamTag,bResult,rResult,redTeamTag,
# gamelength,golddiff,goldblue,bKills,bTowers,bInhibs,bDragons,bBarons,
# bHeralds,goldred,rKills,rTowers,rInhibs,rDragons,rBarons,rHeralds,
# blueTop,blueTopChamp,goldblueTop,blueJungle,blueJungleChamp,goldblueJungle,blueMiddle,
# blueMiddleChamp,goldblueMiddle,blueADC,blueADCChamp,goldblueADC,blueSupport,
# blueSupportChamp,goldblueSupport,blueBans,redTop,redTopChamp,goldredTop,redJungle,
# redJungleChamp,goldredJungle,redMiddle,redMiddleChamp,goldredMiddle,redADC,
# redADCChamp,goldredADC,redSupport,redSupportChamp,goldredSupport,redBans,Address
###
import pandas as pd
def clean_draft_data(df: pd.DataFrame) -> pd.DataFrame:
    champion_columns = [col for col in df.columns if "Champ" in col]
    clean_df = df[champion_columns + ["bResult"]]
    return clean_df
