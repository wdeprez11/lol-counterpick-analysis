# This file loads the data using pandas and declares the load_matches() function which returns the data from LeagueofLegends.csv
import pandas as pd

def load_matches() -> pd.DataFrame:
    return pd.read_csv("data/raw/LeagueofLegends.csv")