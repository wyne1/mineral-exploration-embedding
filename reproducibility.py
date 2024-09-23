import numpy
import os
import random
# import tensorflow

def seed_random(seed):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    numpy.random.seed(seed)
    # tensorflow.random.set_seed(seed)
    # tensorflow.compat.v1.set_random_seed(seed)