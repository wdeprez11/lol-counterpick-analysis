import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
side_to_index = {
    "blue": 0,
    "red": 1
}
role_to_index = {
    "top": 0,
    "jungle": 1,
    "mid": 2,
    "adc": 3,
    "support": 4
}

def get_champion_list(df: pd.DataFrame) -> list[str]:
    """
    Extracts the list of unique champion names from a draft DataFrame.
    
    :param df: Cleaned DataFrame containing champion columns and game results.
    :type df: pd.DataFrame
    :return: Returns a list of str, all unique champion names
    :rtype: list[str]
    """
    # Declare champions set
    champions = set()
    # Iterate through each column name 
    for col in [column for column in df.columns if "Champ" in column]:
        champions.update(df[col].str.lower().unique())

    # Return champions sorted alphebetically
    return sorted(champions)

def build_champion_index(champions: list[str]) -> dict[str, int]:
    """
    Uses list of champions created by get_champions_list() and uses a dictionary comprehension along with enumerate to create a vale->index pair
    
    :param champions: List of champions created by get_champions_list()
    :type champions: list[str]
    :return: Returns an indexed dictionary of champions
    :rtype: dict[str, int]
    """
    return {champ: i for i, champ in enumerate(champions)}

def vectorize_match(match_row: pd.Series, champion_to_index: dict[str, int]) -> list[int]:
    """
    Docstring for vectorize_match
    
    :param match_row: A single match row from clean_df 
    :type match_row: pd.Series
    :param champion_to_index: Champion dictionary 
    :type champion_to_index: dict[str, int]
    :return: Returns a vector of indexed champions using champion_to_index dictionary
    :rtype: list[int]
    """
    N = len(champion_to_index)
    num_roles = len(role_to_index)
    vector = [0] * (2 * num_roles * N)
    for column_name, c_value in match_row.items():
        # Guarantee column_name is of type str
        column_name = str(column_name).lower()
        # Skip bResult column
        if "champ" not in column_name:
            continue

        # Normalize c_value
        c_value = str(c_value).strip().lower()
        # Update vector values according to champion index dictionary
        side = next(side for side in side_to_index if side in column_name)
        assert side is not None
        role = next(role for role in role_to_index if role in column_name)
        assert role is not None
        side_index = side_to_index[side]
        role_index = role_to_index[role]
        champ_index = champion_to_index[c_value]

        # Vector is 10 blocks. Each block is a length of number of champions. 
        # Multiply the side index {0, 1} by the number of roles (5), and add the role index. 
        # Multiply this value by N - the length of champions. 
        # Finally within that block find the correct champion slot and set it to 1.
        index = (side_index * num_roles + role_index) * N + champ_index 
        vector[index] = 1

    return vector

def extract_label(match_row: pd.Series) -> int:
    """
    Returns match result from match_row
    
    :param match_row: A single match row from clean_df
    :type match_row: pd.Series
    :return: Returns game result - 0 or 1 for match_row
    :rtype: int
    """
    value = int(match_row["bResult"])
    assert value in (0, 1)
    return value

def train_logistic_regression(X: np.ndarray, y: np.ndarray) -> LogisticRegression:
    """
    Using scikit-learn, form a logistic regression using X (vectorized matches) and y (known results)
    
    :param X: Vectorized matches from vectorize_match()
    :type X: np.ndarray
    :param y: Known results from bResult column of clean_df using extract_label()
    :type y: np.ndarray
    :return: Returns a LogisticRegression model, iterating 1000 times and using lbfgs solver
    :rtype: LogisticRegression
    """
    return LogisticRegression(solver="lbfgs", max_iter=1000, C=2).fit(X, y)

def extract_champion_coefficients(log_reg: LogisticRegression, champions_to_index: dict[str, int]) -> list[tuple[str, str, str, float]]:
    """
    Docstring for extract_champion_coefficients
    
    :param log_reg: The logistic regression object created and trained by train_logistic_regression()
    :type log_reg: LogisticRegression
    :param champions_to_index: The dictionary created by build_champion_index()
    :type champions_to_index: dict[str, int]
    :return: Returns the list of coefficients as organized tuples of champion names, team sides, and their regression (beta) coefficients
    :rtype: list[tuple[str, str, float]]
    """
    weights = log_reg.coef_[0]
    N = len(champions_to_index)
    num_roles = len(role_to_index)
    coefficients_list = []

    for side, side_index in side_to_index.items():
        for role, role_index in role_to_index.items():
            for champion, champ_index in champions_to_index.items():
                index = (side_index * num_roles + role_index) * N + champ_index
                beta_coef = weights[index]
                coefficients_list.append((champion, side, role, beta_coef))
        
    return coefficients_list

def combine_champion_coefficients(coefficients_list: list[tuple[str, str, str, float]]) -> list[tuple[str, float]]:
    """
    Docstring for combine_champion_coefficients
    
    :param coefficients_list: The coefficients_list created from the LogisticRegression in train_logistic_regression() and extract_champion_coefficients()
    :type coefficients_list: list[tuple[str, str, str, float]]
    :return: Returns a list of champions with their associated regression coefficients
    :rtype: list[tuple[str, float]]
    """
    grouped_coef: dict[str, list[float]] = {}

    for champion, _, _, beta_coef in coefficients_list:
        grouped_coef.setdefault(champion, []).append(beta_coef)

    combined_coefficients = []
    for champion, beta_coefs in grouped_coef.items():
        combined_coefficients.append((champion, sum(beta_coefs) / len(beta_coefs)))

    return combined_coefficients

def count_champion_frequency(clean_df: pd.DataFrame) -> list[tuple[str, int]]:
    """
    Counts the number of instances of each champion within the dataset
    
    :param clean_df: The clean DataFrame from clean_draft_data())
    :type clean_df: pd.DataFrame
    :return: Returns a list of tuples (champion_name, champion_count)
    :rtype: list[tuple[str, int]]
    """
    return [
        (str(champ), int(count))
        for champ, count in (
            clean_df[[col for col in clean_df.columns if "Champ" in col]]
            .stack()
            .astype(str)
            .str.lower()
            .value_counts()
            .sort_index()
            .items()
        )
    ]