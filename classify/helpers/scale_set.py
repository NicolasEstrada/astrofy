#!/usr/bin/env python
""" This is a module that scale the set usin svm-scale
"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import os

from utils import logger

LIBSVM_RELATIVE = 'classify/libs/libsvm/'

if 'ASTROFY_HOME' in os.environ:
    TRAINING_SET_PATH = os.environ['ASTROFY_HOME'] + 'set/training.set'
    SCALED_TRAINING_SET_PATH = os.environ['ASTROFY_HOME'] + 'set/training_scale.set'
    LIBSVM_PATH = os.environ['ASTROFY_HOME'] + LIBSVM_RELATIVE
else:
    TRAINING_SET_PATH = 'set/training.set'
    SCALED_TRAINING_SET_PATH = 'set/training_scale.set'
    LIBSVM_PATH = LIBSVM_RELATIVE


def scale(
    input_path=TRAINING_SET_PATH,
    output_path=SCALED_TRAINING_SET_PATH,
    svm_scale='svm-scale'):

    COMMAND = "{svm_scale_path} {input_path} > {output_path}"

    logger.info("Scaling the training set")
    logger.info("Input: {}".format(input_path))
    logger.info("Output: {}".format(output_path))

    command = COMMAND.format(
        svm_scale_path=LIBSVM_PATH + svm_scale,
        input_path=input_path,
        output_path=output_path)

    logger.info("Executing command:  " + command)

    os.system(command)

    logger.info("Scaling process finished.")


if __name__ == '__main__':

    scale()
