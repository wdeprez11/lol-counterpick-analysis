import numpy as np
import pandas as pd
from src.data_loader import load_matches
from src.data_cleaning import clean_draft_data
from src.features import get_champion_list
from src.features import build_champion_index

df = pd.read_csv("data/raw/LeagueofLegends.csv")

def main():
    raw_df = load_matches()
    clean_df = clean_draft_data(raw_df)
    
    # Print clean df to ensure we are reading data appropriately and cleaning for the correct columns
    print(clean_df.head())
    print(clean_df.shape)

    # Formulate Champions list and print list of champions present in clean_df
    champions = get_champion_list(clean_df)
    print(f"There are {len(champions)} champions present in the dataset.")
    print(champions)

    # Build champion indices
    champions_dict = build_champion_index(champions)
    print(champions_dict)

if __name__ == "__main__":
    main()
