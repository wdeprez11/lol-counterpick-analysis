import numpy as np
import pandas as pd
from src.data_loader import load_matches
from src.data_cleaning import clean_draft_data

df = pd.read_csv("data/raw/LeagueofLegends.csv")

def main():
    raw_df = load_matches()
    clean_df = clean_draft_data(raw_df)

    print(clean_df.head())
    print(clean_df.shape)

if __name__ == "__main__":
    main()
