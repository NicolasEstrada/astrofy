#!/usr/bin/env python
""" This is a module that generates a training set with the required
libsvm format
"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import os

import simplejson as json

from utils import logger
from features import LinealFeatures
from features import PolinomialFeatures

TRAINING_SET_FILE_NAME = 'trainnig.set'

if 'ASTROFY_HOME' in os.environ:
    SOURCE_PATH = os.environ['ASTROFY_HOME'] + 'data/'
    DESTINATION_PATH = os.environ['ASTROFY_HOME'] + 'set/'
else:
    SOURCE_PATH = './data/'
    DESTINATION_PATH = './set/'


def get_file_names():
    """inspect the source folder and return all the available file paths."""
    logger.info("Getting the files names")

    files = set()
    for file_name in os.listdir(SOURCE_PATH):
        if file_name.endswith(".json"):
            files.add(SOURCE_PATH + file_name)
    return files


def extract(file_path):
    """Extracts the (json) raw content of a given file"""
    logger.info("Extracting the data")

    with open(file_path, 'r') as file_object:
        content = file_object.read()

    yield json.loads(content)


def generate(stream):
    logger.info("Generating the data set")
    with open(DESTINATION_PATH + TRAINING_SET_FILE_NAME, 'w'):
        for j_obj in enumerate(stream, start=1):
            # TODO generate training set using the features ids
            LinealFeatures.score
            PolinomialFeatures.colc
            pass

if __name__ == '__main__':
    logger.info("Generating the training set")
    for path in get_file_names():
        # extract(path)
        pass
