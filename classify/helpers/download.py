#!/usr/bin/env python
""" This is a module that download some sample datafrom
SDSS api (http://api.sdss3.org/)"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import random
import requests

from utils import wait

SpectrumQueryUrl = "http://api.sdss3.org/spectrumQuery"
IDQueryUrl = "http://api.sdss3.org/spectrum"

RETRIES = 1

RA_range = (0.0, 360.0)
DEC_range = (-90.0, 90.0)
RADIUS_range = (0, 1800)

_get_ra = lambda *x: random.uniform(*RA_range)
_get_dec = lambda *x: random.uniform(*DEC_range)
_get_radius = lambda *x: random.uniform(*RADIUS_range)


def get_ids(ra, dec, radius, limit=None):
	"""Get ids from sdss API"""

	# Example params: ?&limit=5&ra=159.815d&dec=-0.655&radius=900
	params = {
	    'ra': str(ra) + 'd',
	    'dec': dec,
	    'radius': radius,
	    'limit': limit
	}

	result = requests.get(SpectrumQueryUrl, params=params)

	if result.status_code == 200:
		obj_list = result.json()

		if len(obj_list) > 0:
			return obj_list

		else:
			print "No result found for:"
			print " ra: {}; dec: {}; radius: {}; limit: {}".format(
				ra, dec, radius, limit)
	else:
		print "Connection problems... Status code: {}".format(
			result.status_code)

	return []

# TODO: Download json files


if __name__ == '__main__':
	for _ in xrange(0, RETRIES):
		print get_ids(_get_ra(), _get_dec(), _get_radius(), 5)
		wait()
