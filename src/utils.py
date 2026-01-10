# Helper file for validations and helper functions
import numpy as np
import pandas as pd

def sanity_check_dataset(X: np.ndarray, y: np.ndarray, num_champions: int) -> None:
    """
    Short sanity check to verify size of X and y are correct. Validation function.
    
    :param X: Vectorized matches from vectorize_match()
    :type X: np.ndarray
    :param y: Match results from extract_label()
    :type y: np.ndarray
    :param num_of_champions: Number of champions present in dataset - len(champions)
    :type num_of_champions: int
    """
    num_roles = 5
    num_matches = X.shape[0]
    assert X.shape == (num_matches, 2 * num_roles * num_champions), f"X has wrong shape: {X.shape}"
    assert y.shape == (num_matches,), f"y has wrong shape: {y.shape}"

    for i in range(num_matches):
        assert X[i].sum() == 10, f"Match {i} has {int(X[i].sum())} champions instead of 10" # Verify there are no more than 10 champions per match