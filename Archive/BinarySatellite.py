import datasets
import numpy

lithium_threshold = 10

satellite_analysis = datasets.satellite_analysis()

import reproducibility

seed = 2
reproducibility.seed_random(seed)

lithium_column = "AvLIROUND"

x_labels = satellite_analysis.x_labels()
y_labels = satellite_analysis.y_labels()

#set all values above threshold to 1 all else to 0

lithium_column_array = satellite_analysis[lithium_column].to_numpy()

lithium_column_array[lithium_column_array<lithium_threshold] = 0    
lithium_column_array[lithium_column_array>=lithium_threshold] = 1

satellite_analysis[lithium_column] = lithium_column_array

from sklearn.ensemble import RandomForestClassifier

reproducibility.seed_random(seed)

satellite_analysis_train = satellite_analysis.sample(frac=0.8, random_state=seed)
satellite_analysis_test = satellite_analysis.drop(satellite_analysis_train.index)

x_train = satellite_analysis_train[x_labels].to_numpy(numpy.float32)
y_train = satellite_analysis_train[y_labels].to_numpy(numpy.float32).ravel()
x_test = satellite_analysis_test[x_labels].to_numpy(numpy.float32)
y_test = satellite_analysis_test[y_labels].to_numpy(numpy.float32).ravel()

model = RandomForestClassifier(n_estimators = 500, max_depth = 4, max_features = 3, bootstrap = True, random_state = seed).fit(x_train, y_train)

print("Training Score", model.score(x_train, y_train))
print("Test Score", model.score(x_test, y_test))

prediction = model.predict(x_test)

from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_score

print(f"confusion matrix: {confusion_matrix(y_test, prediction)}")
print(f"accuracy: {accuracy_score(y_test, prediction)}")
print(f"precision: {precision_score(y_test, prediction)}")
print(f"f1 score: {f1_score(y_test,prediction)}")




