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
    SCALE_PATH = os.environ['ASTROFY_HOME'] + 'set/'
    SCALED_TRAINING_SET_PATH = SCALE_PATH + 'training_scale.set'
    LIBSVM_PATH = os.environ['ASTROFY_HOME'] + LIBSVM_RELATIVE
else:
    SCALE_PATH = 'set/'
    TRAINING_SET_PATH = 'set/training.set'
    SCALED_TRAINING_SET_PATH = 'set/training_scale.set'
    LIBSVM_PATH = LIBSVM_RELATIVE


def scale(
    input_path=TRAINING_SET_PATH,
    output_path=SCALED_TRAINING_SET_PATH,
    scale_params_path=SCALE_PATH + 'scale.params',
    svm_scale='svm-scale',
    scale_mode='r'):

    COMMAND = "{svm_scale_path} -{scale_mode} {scale_params_path} {input_path} > {output_path}"

    logger.debug("Scaling the training set")
    logger.debug("Input: {}".format(input_path))
    logger.debug("Output: {}".format(output_path))
    logger.debug("Storing scale params in: {}".format(scale_params_path))

    command = COMMAND.format(
        svm_scale_path=LIBSVM_PATH + svm_scale,
        input_path=input_path,
        output_path=output_path,
        scale_params_path=scale_params_path,
        scale_mode=scale_mode)

    logger.debug("Executing command:  " + command)

    os.system(command)

    logger.debug("Scaling process finished.")


if __name__ == '__main__':

    scale(scale_mode='s')
