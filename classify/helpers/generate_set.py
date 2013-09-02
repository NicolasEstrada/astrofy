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
from features import SDSSObjectTypes
from features import PolinomialFeatures
from features import LF_FIELDS, PF_FIELDS

lf = LinealFeatures()
sot = SDSSObjectTypes()
pf = PolinomialFeatures()

DELIMITER = ' '
BASE = "{obj_type}{delimiter}{features}"
TRAINING_SET_FILE_NAME = 'training.set'

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


def extract(file_path_list):
    """Extracts the (json) raw content of a given file"""
    logger.info("Extracting the data")

    for file_path in file_path_list:
        with open(file_path, 'r') as file_object:
            content = file_object.read()

        # We get the payload dict from the main key
        # i.e: {"sdss.2312...": {CONTENT}}
        yield json.loads(content).values()[0]


def generate(stream, total):
    logger.info("Generating the data set")

    # We open the training file in 'a' mode to append the data to the file
    # And also to avoid overwrite the file an lose data
    with open(DESTINATION_PATH + TRAINING_SET_FILE_NAME, 'a') as dest_file:
        for n, j_obj in enumerate(stream, start=1):
            # Create an empty features list
            features_list = []

            # Get object type (objc_type) and evaluate for be used as a 
            # training set element.
            obj_type =sot.get_svm_class(j_obj['objc_type'])

            if obj_type != None:
                for key, value in j_obj.items():
                    if key in PF_FIELDS:
                        features_list.extend(pf.get(key, obj_type, value))
                    elif key in LF_FIELDS:
                        features_list.extend(lf.get(key, obj_type, value))

                line_to_write = BASE.format(
                    obj_type=obj_type,
                    delimiter=DELIMITER,
                    features=DELIMITER.join(features_list)
                )

                # Writing a valid line into the training file
                dest_file.writeline(line_to_write)

            else:
                # Logging unknown objects
                unknown_type = j_obj['objc_type']
                logger.info("Unknown object id {}:{}".format(
                    unknown_type,
                    sot.indexes[unknown_type])
                )

        if n % 10 == 0:
            logger.info("Processing object {}/{}".format(n, total))

if __name__ == '__main__':
    logger.info("Generating the training set")

    file_names = get_file_names()
    total = len(file_names)

    generate(extract(file_names), total)
