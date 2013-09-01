#!/usr/bin/env python
""" This is a module that generates a training set with the required
libsvm format
"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import os

import simplejson as json

from utils import logger

if 'ASTROFY_HOME' in os.environ:
    SOURCE_PATH = os.environ['ASTROFY_HOME'] + '/data/'
else:
    SOURCE_PATH = './data'


def get_file_names():
	"""inspect the source folder and return all the available file paths."""
	return []


def extract(file_path):
	"""Extracts the (json) raw content of a given file"""

	with open(file_path, 'r') as file_object:
		content = file_object.read()

	return json.loads(content)


if __name__ == '__main__':
	logger.info("Generating the training set")
	for path in get_file_names():
		extract(path)
