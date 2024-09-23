import math
import numpy
from sklearn.metrics import r2_score

class ConfusionMatrix:
    def __init__(self, y_actual, y_predict, true_positives=0, false_positives=0, false_negatives=0, true_negatives=0):
        self.y_actual = y_actual
        self.y_predict = y_predict
        self.true_positives = true_positives
        self.false_positives = false_positives
        self.false_negatives = false_negatives
        self.true_negatives = true_negatives

    @property
    def count(self):
        return (self.true_positives + self.false_positives + self.false_negatives + self.true_negatives)

    @property
    def accuracy(self):
        if self.count == 0:
            return math.nan
        return (self.true_negatives + self.true_positives) / self.count

    @property
    def precision(self):
        if (self.true_positives + self.false_positives) == 0:
            return math.nan
        return self.true_positives / (self.true_positives + self.false_positives)
    
    @property
    def recall(self):
        if (self.true_positives + self.false_negatives) == 0:
            return math.nan
        return self.true_positives / (self.true_positives + self.false_negatives)

    @property
    def f1_score(self):
        if math.isnan(self.precision) or math.isnan(self.recall) or self.precision + self.recall == 0:
            return math.nan
        return 2 * (self.precision * self.recall) / (self.precision + self.recall)

    @property
    def r2(self):
        return r2_score(self.y_actual, self.y_predict)
    
    @property
    def rmse(self):
        mse = numpy.square(numpy.subtract(self.y_actual, self.y_predict)).mean()
        return math.sqrt(mse)

    def __add__(self, other):
        true_positives = self.true_positives + other.true_positives
        false_positives = self.false_positives + other.false_positives
        false_negatives = self.false_negatives + other.false_negatives
        true_negatives = self.true_negatives + other.true_negatives

        return ConfusionMatrix(true_positives=true_positives, false_positives=false_positives, false_negatives=false_negatives, true_negatives=true_negatives)