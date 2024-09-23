import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

def min_max_scaling(data):
    """
    Perform Min-Max scaling on the input data.
    """
    scaler = MinMaxScaler()
    return pd.Series(scaler.fit_transform(data.values.reshape(-1, 1)).flatten(), index=data.index)

def standard_scaling(data):
    """
    Perform Standard scaling (z-score normalization) on the input data.
    """
    scaler = StandardScaler()
    return pd.Series(scaler.fit_transform(data.values.reshape(-1, 1)).flatten(), index=data.index)

def robust_scaling(data):
    """
    Perform Robust scaling on the input data.
    """
    scaler = RobustScaler()
    return pd.Series(scaler.fit_transform(data.values.reshape(-1, 1)).flatten(), index=data.index)

def log_transform(data):
    """
    Perform log transformation on the input data.
    Adds a small constant to avoid log(0).
    """
    return np.log(data + 1e-10)

def winsorization(data, limits=(0.05, 0.95)):
    """
    Perform Winsorization on the input data.
    """
    lower_limit = data.quantile(limits[0])
    upper_limit = data.quantile(limits[1])
    return data.clip(lower=lower_limit, upper=upper_limit)

def log_then_min_max(data):
    """
    Perform log transformation followed by Min-Max scaling.
    """
    log_data = log_transform(data)
    return min_max_scaling(log_data)

def winsor_then_min_max(data, limits=(0.05, 0.95)):
    """
    Perform Winsorization followed by Min-Max scaling.
    """
    winsor_data = winsorization(data, limits)
    return min_max_scaling(winsor_data)

    
def calculate_weights(differences, penalty_factor=1):
    # Higher penalty factor will penalize lower differences more
    return penalty_factor / (differences + penalty_factor)

def weighted_f1_score(data_frame, gold_threshold, ore_diff_threshold, penalty_factor=1):
    data_frame["Actual"] = data_frame[GOLD_COLUMN] >= gold_threshold
    data_frame["Predicted"] = data_frame[ORE_DIFFERENCE_COLUMN] <= ore_diff_threshold
    
    data_frame["Weight"] = calculate_weights(data_frame[ORE_DIFFERENCE_COLUMN], penalty_factor)
    
    tp = data_frame[data_frame["Actual"] & data_frame["Predicted"]]
    fp = data_frame[~data_frame["Actual"] & data_frame["Predicted"]]
    fn = data_frame[data_frame["Actual"] & ~data_frame["Predicted"]]
    tn = data_frame[~data_frame["Actual"] & ~data_frame["Predicted"]]
    
    weighted_tp = tp["Weight"].sum()
    weighted_fp = fp["Weight"].sum()
    weighted_fn = fn["Weight"].sum()
    weighted_tn = tn["Weight"].sum()
    
    weighted_accuracy = (weighted_tp + weighted_tn) / (weighted_tp + weighted_tn + weighted_fp + weighted_fn)
    weighted_precision = weighted_tp / (weighted_tp + weighted_fp)
    weighted_recall = weighted_tp / (weighted_tp + weighted_fn)
    
    if weighted_precision + weighted_recall == 0:
        return 0
    
    weighted_f1 = 2 * (weighted_precision * weighted_recall) / (weighted_precision + weighted_recall)
    
    return round(weighted_f1, 4), round(weighted_precision, 4), round(weighted_recall, 4), round(weighted_accuracy, 4), tp, fp, fn, tn

def penalty_function(ore_difference, max_penalty=10):
    return max_penalty / (ore_difference + 0.1)  

def custom_loss(data_frame, gold_threshold, ore_diff_threshold, max_penalty=10):
    data_frame["Actual"] = data_frame[GOLD_COLUMN] >= gold_threshold
    data_frame["Predicted"] = data_frame[ORE_DIFFERENCE_COLUMN] <= ore_diff_threshold
    
    false_positives = data_frame[~data_frame["Actual"] & data_frame["Predicted"]]
    false_negatives = data_frame[data_frame["Actual"] & ~data_frame["Predicted"]]
    
    fp_penalties = false_positives[ORE_DIFFERENCE_COLUMN].apply(penalty_function, max_penalty=max_penalty)
    fn_penalties = false_negatives[ORE_DIFFERENCE_COLUMN].apply(penalty_function, max_penalty=max_penalty)
    
    total_loss = fp_penalties.sum() + fn_penalties.sum()
    
    return total_loss