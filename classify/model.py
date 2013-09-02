#!/usr/bin/env python
""" This is a module that generates model from a training set to be
used as a base model for galaxy/star clasification
"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import os


from helpers.utils import logger

from libs.libsvm.python.svmutil import *

if 'ASTROFY_HOME' in os.environ:
    TRAINING_SET_PATH = os.environ['ASTROFY_HOME'] + 'set/training.set'
    MODEL_PATH = os.environ['ASTROFY_HOME'] + 'model/model.svm'
else:
    TRAINING_SET_PATH = './set/training.set'
    MODEL_PATH = './model/model.svm'

def generate_model():
    logger.info("Generating the svm model")
    y, x = svm_read_problem(TRAINING_SET_PATH)
    model = svm_train(y[:200], x[:200], '-c 4')
    svm_save_model(MODEL_PATH, model)

def load_model():
    logger.info("Generating the svm model")
    return svm_load_model(MODEL_PATH)

if __name__ == '__main__':
    generate_model()

    model = load_model()
    y, x = svm_read_problem(TRAINING_SET_PATH)
    p_label, p_acc, p_val = svm_predict(y[230:400], x[230:400], model)
