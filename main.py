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
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from src.features import extract_champion_coefficients
from src.features import combine_champion_coefficients
from src.features import count_champion_frequency

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

    # print(vectorized_matches[0])
    # print(match_results[0])

    X = np.array(vectorized_matches)
    y = np.array(match_results)
    sanity_check_dataset(X, y, len(champions))

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=11)
    log_reg = train_logistic_regression(X_train, y_train) # Create a function f(x) = 1 / 1 + e^-(mx+b)
    y_pred = log_reg.predict(X_test) # Make a prediction
    log_reg.score(X_test, y_test)
    print(confusion_matrix(y_test, y_pred))

#  |                     | Predicted Loss (0) | Predicted Win (1) |
#  | ------------------- | ------------------ | ----------------- |
#  | **Actual Loss (0)** |     (TN)           |     (FP)          |
#  | **Actual Win (1)**  |     (FN)           |     (TP)          |

    print(classification_report(y_test, y_pred))

    coefficients_list = extract_champion_coefficients(log_reg, champions_dict)
    # print(*coefficients_list, sep="\n")
    coefficients_list = combine_champion_coefficients(coefficients_list)

    log_reg.intercept_[0]

    coefficients_list = sorted(coefficients_list, key=lambda x: x[1])

    print("Top 10")
    print(*coefficients_list[-10:][::-1], sep="\n")

    neutral_10 = sorted(coefficients_list, key=lambda x: abs(x[1]))[:10]
    print("Neutral 10")
    print(*neutral_10, sep="\n")

    print("Bottom 10")
    print(*coefficients_list[0:10], sep="\n")

    champions_count = count_champion_frequency(clean_df)
    print(*champions_count, sep="\n")

if __name__ == "__main__":
    main()
