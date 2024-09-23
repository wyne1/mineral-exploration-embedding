# from tensorflow import keras
from sklearn.ensemble import HistGradientBoostingRegressor
from pandas import DataFrame
import numpy as np

# def neural_network(input_length, hidden_layer_count=10) -> keras.Model:
#     inputs = keras.Input(shape=(input_length,))
#     layer = inputs
#     for i in range(0, hidden_layer_count):
#         layer = keras.layers.Dense(64, activation="relu", use_bias=True)(layer)
#     outputs = keras.layers.Dense(1, activation="linear")(layer)
#     model = keras.Model(inputs=inputs, outputs=outputs, name="LithiumPPM")

#     model.compile(
#         loss = keras.losses.MeanSquaredError(),
#         optimizer = keras.optimizers.Adam(),
#         metrics = [
#             keras.metrics.MeanAbsoluteError(),
#             keras.metrics.MeanSquaredError(),
#             keras.metrics.RootMeanSquaredError()
#         ]
#     )

#     return model

def hist_gradient_boosting_regressor_geochem(target_element: str, seed: int, geochemical_analysis: "function", country=None) -> tuple[np.array, np.array, np.array, np.array, DataFrame, DataFrame, HistGradientBoostingRegressor]:
    geochemical_analysis = geochemical_analysis(target_element)

    x_labels = geochemical_analysis.x_labels()
    y_labels = geochemical_analysis.y_labels()

    if country != None:
        geochemical_analysis = geochemical_analysis[geochemical_analysis["COUNTRY"] == country][x_labels + y_labels].dropna(subset=y_labels)

    geochemical_analysis_measured = geochemical_analysis[x_labels + y_labels].dropna(subset=y_labels)
    geochemical_analysis_train = geochemical_analysis_measured.sample(frac=0.8, random_state=seed)
    geochemical_analysis_test = geochemical_analysis_measured.drop(geochemical_analysis_train.index)
    
    x_train = geochemical_analysis_train[x_labels].to_numpy(np.float32)
    y_train = geochemical_analysis_train[y_labels].to_numpy(np.float32).ravel()
    x_test = geochemical_analysis_test[x_labels].to_numpy(np.float32)
    y_test = geochemical_analysis_test[y_labels].to_numpy(np.float32).ravel()    
    
    model = HistGradientBoostingRegressor(loss="squared_error", validation_fraction=0.2, min_samples_leaf=5, random_state=seed).fit(x_train, y_train)
    
    return x_train, y_train, x_test, y_test, x_labels, y_labels, geochemical_analysis, geochemical_analysis_measured, model

__all__ = ["neural_network", "hist_gradient_boosting_regressor_geochem"]