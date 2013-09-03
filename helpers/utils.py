"""This is a module contains some helpful utilities"""

from __future__ import division

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import time
import random
import logging

FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

flhdl = logging.FileHandler('log/fetch_ids.log')
logger = logging.getLogger('Astrofy_downloader')
logger.setLevel(logging.INFO)
logger.addHandler(flhdl)

MAX_WAIT = 4


def wait(logger=None, max_wait=MAX_WAIT, rand=True):
    secs =  max_wait / random.uniform(1, max_wait) if rand else max_wait

    if logger:
        logger.debug("Waiting for {0:.2f} seconds".format(secs))
    else:
    	print "Waiting for {0:.2f} seconds".format(secs)

    time.sleep(secs)

