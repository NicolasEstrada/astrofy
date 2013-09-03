#!/usr/bin/env python
""" This is a module that download some sample datafrom
SDSS api (http://api.sdss3.org/) and store it"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import os
import random
import requests

from helpers import download
from helpers.utils import wait
from helpers.utils import logger

RETRIES = 10
THRESHOLD = 100

if __name__ == '__main__':
	while(True):
		if download.db.objects.find({"classified": 0}).count() < THRESHOLD:
			for retry in xrange(0, RETRIES):
				logger.info("Start progress ... Attemp: {0}".format(retry))
				# wait(logger)
				qty = download.download_files(limit=5)
				if qty:
					break
		else:
			wait(logger, 10, False)
