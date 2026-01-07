import numpy as np
import pandas as pd
from src.data_loader import load_matches
from src.data_cleaning import clean_draft_data
from src.features import get_champion_list
from src.features import build_champion_index
from src.features import vectorize_match

def main():
    raw_df = load_matches("data/raw/LeagueofLegends.csv")
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

    vectorized_matches = []
    for _, row in clean_df.iterrows():
        vector = vectorize_match(row, champions_dict)
        vectorized_matches.append(vector)

    print(vectorized_matches[0])

if __name__ == "__main__":
    main()
