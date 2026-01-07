import pandas as pd


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
    vector = [0] * (2 * N)
    for column_name, c_value in match_row.items():
        # Guarantee column_name is of type str
        column_name = str(column_name).lower()
        # Skip bResult column
        if "champ" not in column_name:
            continue

        # Normalize c_value
        c_value = str(c_value).strip().lower()
        # Update vector values according to champion index dictionary
        if "blue" in column_name:
            vector[champion_to_index[c_value]] = 1
        elif "red" in column_name:
            vector[N + champion_to_index[c_value]] = 1

    return vector