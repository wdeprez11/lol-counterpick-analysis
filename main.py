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
from pathlib import Path
from src.features import count_champion_role_frequency
from src.features import role_to_index
output_path = Path("data/output")

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

    raw_coefficients_list = extract_champion_coefficients(log_reg, champions_dict)
    # print(*coefficients_list, sep="\n")
    coefficients_list = combine_champion_coefficients(raw_coefficients_list)
    coefficients_list = sorted(coefficients_list, key=lambda x: x[1])

    """
    print("Top 10")
    print(*coefficients_list[-10:][::-1], sep="\n")

    neutral_10 = sorted(coefficients_list, key=lambda x: abs(x[1]))[:10]
    print("Neutral 10")
    print(*neutral_10, sep="\n")

    print("Bottom 10")
    print(*coefficients_list[0:10], sep="\n")
    """

    champion_counts = count_champion_frequency(clean_df)
    champion_role_counts = count_champion_role_frequency(clean_df)

    output_path.mkdir(parents=True, exist_ok=True)
    write_champ_summary(champion_counts, coefficients_list)
    write_champ_role_summary(champion_role_counts, raw_coefficients_list)

def write_champ_summary(champion_counts: list[tuple[str, int]], champion_coefficients: list[tuple[str, float]]) -> None:
    """
    Write output file reports for champions counts, and their respective beta coefficients
    
    :param champions_count: List of champions' counts
    :type champions_count: list[tuple[str, int]]
    :param champion_coefficients: List of champions' beta coefficients
    :type champion_coefficients: list[tuple[str, float]]
    :param output_path: Path object with file directory for outputs
    :type output_path: Path
    """
    champ_dict = {champion: [float(count)] for champion, count in champion_counts}
    for champion, beta_coef in champion_coefficients:
        champ_dict[champion].append(beta_coef)

    for champion, values in champ_dict.items():
        assert len(values) == 2, f"length of data corresponding to {champion} is {len(values)}"

    rows = [
        (champion, values[0], values[1], abs(values[1]))
        for champion, values in champ_dict.items()
    ]

    pd.DataFrame(rows, columns=["Champion", "Count", "AvgBeta", "AbsAvgBeta"]).to_csv(output_path / "champion_summary.csv", index=False)

def write_champ_role_summary(champion_role_counts: list[tuple[str, str, int]], raw_coefficients: list[tuple[str, str, str, float]]) -> None:
    grouped = {}
    for champion, _, role, beta_coef in raw_coefficients:
        key = (champion, role)
        grouped.setdefault(key, []).append(beta_coef)

    avg_betas = {
        (champion, role): sum(betas) / len(betas)
        for (champion, role), betas in grouped.items()
    }

    rows = []
    for champion, role, count in champion_role_counts:
        avg_beta = avg_betas.get((champion, role), 0.0)
        rows.append((champion, role, count, avg_beta, abs(avg_beta)))

    rows.sort(key=lambda x: (x[0], role_to_index[x[1]]))

    pd.DataFrame(rows, columns=["Champion", "Role", "Count", "AvgBeta", "AbsAvgBeta"]) \
    .to_csv(output_path / "champion_role_summary.csv", index=False)

if __name__ == "__main__":
    main()
