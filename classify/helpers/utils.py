"""This is a module contains some helpful utilities"""

from __future__ import division

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import time
import random

MAX_WAIT = 4


def wait(logger=None):
    secs =  MAX_WAIT / random.uniform(1, MAX_WAIT)

    if logger:
        logger.debug("Waiting for {0:.2f} seconds".format(secs))
    else:
    	print "Waiting for {0:.2f} seconds".format(secs)

    time.sleep(secs)