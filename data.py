import numpy
import pandas
import pathlib
import reproducibility
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def split_train_test(data_frame: pandas.DataFrame, x_labels, y_labels, frac=0.8, seed=None):
    if seed is not None:
        reproducibility.seed_random(seed)

    data_frame_train = data_frame.sample(frac=frac, random_state=seed)
    data_frame_test = data_frame.drop(data_frame_train.index)

    x_train = data_frame_train[x_labels].to_numpy(numpy.float32)
    y_train = data_frame_train[y_labels].to_numpy(numpy.float32).ravel()
    x_test = data_frame_test[x_labels].to_numpy(numpy.float32)
    y_test = data_frame_test[y_labels].to_numpy(numpy.float32).ravel()

    return x_train, y_train, x_test, y_test


def plot_confusion_matrix(comparison, ppm_threshold, target_element, dataset, unit="m", color="#df474f"):
    xmin = 1
    xmax = 6400
    ymin = 1
    ymax = 6400

    plt.scatter(comparison["Actual"].to_list(), comparison["Predicted"].to_list(), color=color)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])

    axes = plt.gca()
    axes.get_xaxis().set_major_formatter(ScalarFormatter())
    axes.get_yaxis().set_major_formatter(ScalarFormatter())

    title = f"Output/Predicted vs Actual {target_element} Concentrations {ppm_threshold} pp{unit} {dataset}"
    plt.hlines(y=ppm_threshold, xmin=xmin, xmax=xmax, colors="black", ls=":", lw=2)
    plt.vlines(x=ppm_threshold, ymin=ymin, ymax=ymax, colors="black", ls=":", lw=2)
    plt.text(1.4, 3000, "False Positive")
    plt.text(800, 3000, "True Positive")
    plt.text(1.4, 40, "True Negative")
    plt.text(800, 40, "False Negative")
    plt.title(title)

    pathlib.Path("Output").mkdir(parents=True, exist_ok=True)

    plt.savefig(title + ".png")