import numpy as np
import pandas as pd
from src.data_loader import load_matches
from src.data_cleaning import clean_draft_data
from src.features import get_champion_list
from src.features import build_champion_index
from src.features import vectorize_match
from src.features import extract_label
from src.utils import sanity_check_dataset
from src.features import train_logistic_regression

def main():
    raw_df = load_matches("data/raw/LeagueofLegends.csv")
    clean_df = clean_draft_data(raw_df)
    
    # Print clean df to ensure we are reading data appropriately and cleaning for the correct columns
    print(clean_df.head())
    print(clean_df.shape)

    # Formulate Champions list and print list of champions present in clean_df
    champions = get_champion_list(clean_df)
    print(f"There are {len(champions)} champions present in the dataset.")
    # print(champions)

    # Build champion indices
    champions_dict = build_champion_index(champions)
    # print(champions_dict)

    match_results = [] # y
    vectorized_matches = [] # X
    for _, row in clean_df.iterrows():
        vector = vectorize_match(row, champions_dict)
        result = extract_label(row)
        vectorized_matches.append(vector)
        match_results.append(result)

    print(vectorized_matches[0])
    print(match_results[0])

    X = np.array(vectorized_matches)
    y = np.array(match_results)
    sanity_check_dataset(X, y, len(champions))

    log_reg = train_logistic_regression(X, y)

if __name__ == "__main__":
    main()
