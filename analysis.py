from geochem_table import GeochemResultSet
from confusion_matrix import ConfusionMatrix

def create_threshold_column(data_frame, source_column, destination_column, threshold):
    data_frame[destination_column] = data_frame[source_column].ge(threshold)

def evaluate_performance(y_actual, y_predict, threshold, verbose=1):
    actual_column = "Actual"
    predicted_column = "Predicted"
    actual_threshold_column = "Actual_Threshold"
    predicted_threshold_column = "Predicted_Threshold"

    import pandas

    data_frame = pandas.DataFrame()

    data_frame[actual_column] = y_actual
    data_frame[predicted_column] = y_predict
    create_threshold_column(data_frame, actual_column, actual_threshold_column, threshold)
    create_threshold_column(data_frame, predicted_column, predicted_threshold_column, threshold)

    tp = fp = tn = fn = float(0)

    for index, row in data_frame.iterrows():
        predicted = row[predicted_threshold_column]
        actual = row[actual_threshold_column]

        if predicted:
            if actual:
                tp = tp + 1
            else:
                fp = fp + 1
        else:
            if actual:
                fn = fn + 1
            else:
                tn = tn + 1

    confusion_matrix = ConfusionMatrix(y_actual, y_predict, true_positives=tp, false_positives=fp, false_negatives=fn, true_negatives=tn)

    geochem_result_set = GeochemResultSet(**{
        "n_samples": {"value": int(len(data_frame)), "label": "Number of samples"}, 
        "positive_samples": {"value": int(confusion_matrix.true_positives + confusion_matrix.false_negatives), "label": "Positive samples"},
        "negative_samples": {"value": int(len(data_frame) - confusion_matrix.true_positives - confusion_matrix.false_negatives), "label": "Negative samples"},
        "true_positives": {"value": int(confusion_matrix.true_positives), "label": "True Positives"}, 
        "false_positives": {"value": int(confusion_matrix.false_positives), "label": "False Positives"},
        "true_negatives": {"value": int(confusion_matrix.true_negatives), "label": "True Negatives"},
        "false_negatives": {"value": int(confusion_matrix.false_negatives), "label": "False Negatives"},
        "accuracy": {"value": round(confusion_matrix.accuracy, 2), "label": "Accuracy"}, 
        "precision": {"value": round(confusion_matrix.precision, 2), "label": "Precision"},
        "recall": {"value": round(confusion_matrix.recall, 2), "label": "Recall"},
        "f1": {"value": round(confusion_matrix.f1_score, 2), "label":  "F1"},
        "r2": {"value": round(confusion_matrix.r2, 2), "label": "R2"},
        "rmse": {"value": round(confusion_matrix.rmse, 2),"label": 'RMSE'}
    })
    
    if verbose >= 1:
        geochem_result_set.print_results()

    return data_frame, confusion_matrix, geochem_result_set

def update_scores(confusion_matrix, scores, seed, running_total, metric, verbose = 1):

    if(metric == "f1"):
        current = confusion_matrix.f1_score
    if(metric == "precision"):
        current = confusion_matrix.precision
    if(metric == "recall"):
        current = confusion_matrix.recall
    if(metric == "r2"):
        current = confusion_matrix.r2
    if(metric == "rmse"):
        current = confusion_matrix.rmse

    if(current):
        running_total+=current
        if(current > scores['max'] ):
            scores['max'] = current
            scores['max_seed'] = seed
            
    #uncomment the following if you want 0 scores to reduce the average, not sure what the best way to process these is yet:
    #else: running_total += scores.average

    scores["average"] = running_total/(seed+1)

    if verbose >= 1:
        print(f"Max {metric} = {scores['max']} for seed = {scores['max_seed']}")
        print(f"Average {metric} = {scores['average']}")
    
    return scores


__all__ = ["create_threshold_column", "evaluate_performance", "update_scores"]
