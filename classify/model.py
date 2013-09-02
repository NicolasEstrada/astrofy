#!/usr/bin/env python
""" This is a module that generates model from a training set to be
used as a base model for galaxy/star clasification
"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import os


from helpers.utils import logger

from libs.libsvm.python.svmutil import svm_train
from libs.libsvm.python.svmutil import svm_predict
from libs.libsvm.python.svmutil import svm_load_model
from libs.libsvm.python.svmutil import svm_save_model
from libs.libsvm.python.svmutil import svm_read_problem

TRAINING_OFFSET = 1000

if 'ASTROFY_HOME' in os.environ:
    TRAINING_SET_PATH = os.environ['ASTROFY_HOME'] + 'set/training_scale.set'
    MODEL_PATH = os.environ['ASTROFY_HOME'] + 'model/model.svm'
else:
    TRAINING_SET_PATH = './set/training_scale.set'
    MODEL_PATH = './model/model.svm'


def generate_model(training_path=TRAINING_SET_PATH, model_path=MODEL_PATH):
    """Generate the base model for clasification

    Save the generated model into the destination path

    Args:
        training_path: absolute or relative path to the training set
        model_path: absolute or relative path to the model file
    
    Returns:
        None
    
    Raise:
        Exception: Uncaught exception.
    """

    logger.info("Generating the svm model")
    y, x = svm_read_problem(training_path)
    model = svm_train(y[:TRAINING_OFFSET], x[:TRAINING_OFFSET], '-c 4 -q')
    svm_save_model(model_path, model)


def load_model(model_path=MODEL_PATH):
    """Loads the model

    Loads the svm model generated with the training set.

    Args:
        model_path: absolute or relative path to the model file
    
    Returns:
        SVM model object
    
    Raise:
        Exception: Uncaught exception.
    """

    logger.info("Loading the svm model")

    return svm_load_model(model_path)


if __name__ == '__main__':
    generate_model()

    model = load_model()
    y, x = svm_read_problem(TRAINING_SET_PATH)
    p_label, p_acc, p_val = svm_predict(
        [y[-1]], [x[-1]], model, options="-q")

    print p_label, p_acc, p_val
