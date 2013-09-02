#!/usr/bin/env python
""" This is a module that download some sample datafrom
SDSS api (http://api.sdss3.org/)"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import os
import random
import argparse
import requests

import simplejson as json

from utils import wait
from utils import logger

EXT = '.json'

if 'ASTROFY_HOME' in os.environ:
    DOWNLOAD_PATH = os.environ['ASTROFY_HOME'] + 'data/'
else:
    DOWNLOAD_PATH = './data/'

SpectrumQueryUrl = "http://api.sdss3.org/spectrumQuery"
IDQueryUrl = "http://api.sdss3.org/spectrum"

RA_range = (0.0, 360.0)
DEC_range = (-90.0, 90.0)
RADIUS_range = (900, 1800)

_get_ra = lambda *x: random.uniform(*RA_range)
_get_dec = lambda *x: random.uniform(*DEC_range)
_get_radius = lambda *x: random.uniform(*RADIUS_range)


def get_ids(ra, dec, radius, limit=None):
	"""Get ids from sdss API"""

	# i.e: ?&limit=5&ra=159.815d&dec=-0.655&radius=900
	params = {
	    'ra': str(ra) + 'd',
	    'dec': dec,
	    'radius': radius,
	    'limit': limit
	}

	logger.info("Getting ids for: ra: {}; dec: {}; radius: {}; limit: {}".format(
		ra, dec, radius, limit))

	result = requests.get(SpectrumQueryUrl, params=params)

	if result.status_code == 200:
		obj_list = result.json()

		if len(obj_list) > 0:
			return obj_list

		else:

			logger.info("No result found for: ra: {}; dec: {}; radius: {}; limit: {}".format(
				ra, dec, radius, limit))
	else:
		logger.critical("Connection problems... Status code: {}".format(
			result.status_code))

	return []


def download_files(ids, format='json'):
	"""Download the files in json format"""

	logger.info("Starting download process")

	logger.info("Downloading {} files".format(len(ids)))

	for n, sdss_id in enumerate(ids, start=1):
		# i.e: ?id=boss.3840.55574.029.v5_4_45&format=json
		params = {
		    'id':sdss_id, 
		    'format': format
		}

		result = requests.get(IDQueryUrl, params=params)

		if result.status_code == 200:
			payload = result.json()
			with open(DOWNLOAD_PATH + sdss_id + EXT, 'w') as out_file:
				out_file.write(json.dumps(payload))		

		if n % 5 == 0:
			logger.info("Progress {}/{}".format(n, len(ids)))

		wait(logger, 1)

	logger.info("Download finished")

if __name__ == '__main__':

	parser = argparse.ArgumentParser(
		prog='./download', description='Download files from sdss')
	parser.add_argument(
		'-a', type=int, default=1,
		help='Number of attempts (default: 1)')
	parser.add_argument('-l', default=10,
        help='Limit of files (default: 10)')

	args = parser.parse_args()

	retries = args.a
	limit = args.l

	for retry in xrange(0, retries):
		logger.info("Attempt {0}".format(retry))
		ids = get_ids(_get_ra(), _get_dec(), _get_radius(), limit)
		wait(logger)
		download_files(ids)
