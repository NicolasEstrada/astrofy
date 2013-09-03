#!/usr/bin/env python
""" This is a module that download some sample datafrom
SDSS api (http://api.sdss3.org/)"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import os
import random
import requests

import pymongo
import simplejson as json

from utils import wait
from utils import logger

EXT = '.json'

if 'ASTROFY_HOME' in os.environ:
    DOWNLOAD_PATH = os.environ['ASTROFY_HOME'] + 'data/'
else:
    DOWNLOAD_PATH = './data/'

if 'ASTROFY_HOME' in os.environ:
    IMAGE_PATH = os.environ['ASTROFY_HOME'] + 'images/'
else:
    IMAGE_PATH = './images/'

SpectrumQueryUrl = "http://api.sdss3.org/spectrumQuery"
IDQueryUrl = "http://api.sdss3.org/spectrum"
IDGetImageUrl = "http://dr10.sdss3.org/sas/dr10/boss/photoObj/frames/{rerun}/{run}/{camcol}/frame-{format}-{lrun}-{camcol}-{lfield}.{ext}"

RETRIES = 10

RA_range = (0.0, 360.0)
DEC_range = (-90.0, 90.0)
RADIUS_range = (900, 1800)

IGNORE_KEYS = [
	'wavelengths',
	'fracnsighi',
	'or_mask',
	'and_mask',
	'wavelength_dispersion',
	'sky_flux',
	'best_fit',
	'inv_var',
	'flux'
]

_get_ra = lambda *x: random.uniform(*RA_range)
_get_dec = lambda *x: random.uniform(*DEC_range)
_get_radius = lambda *x: random.uniform(*RADIUS_range)


client = pymongo.MongoClient("localhost", 27017)
db = client.test
db.objects.ensure_index([('id', 1)])


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


def save_and_get_files(ids, format='json'):
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

		yield sdss_id, payload  # yields the object id and the json info
		wait(logger, 1)

	logger.info("Download finished")


# http://dr10.sdss3.org/sas/dr10/boss/photoObj/frames/301/4570/4/frame-irg-004570-4-0135.jpg
# http://dr10.sdss3.org/sas/dr10/boss/photoObj/frames/301/4570/4/frame-u-004570-4-0135.fits.bz2
# http://dr10.sdss3.org/sas/dr10/boss/photoObj/frames/301/4570/4/frame-g-004570-4-0135.fits.bz2
# http://dr10.sdss3.org/sas/dr10/boss/photoObj/frames/301/4570/4/frame-r-004570-4-0135.fits.bz2
# http://dr10.sdss3.org/sas/dr10/boss/photoObj/frames/301/4570/4/frame-i-004570-4-0135.fits.bz2
# http://dr10.sdss3.org/sas/dr10/boss/photoObj/frames/301/4570/4/frame-z-004570-4-0135.fits.bz2

def download_files(format='irg', limit=3):
	"""Download the files in json format"""

	logger.info("Starting download process")

	logger.info("Downloading files ...")

	ext = 'jpg' if format == 'irg' else 'fits.bz2'

	# import pdb
	# pdb.set_trace()

	download_count = 0

	for sdss_id, sdss_object in save_and_get_files(
							     get_ids(_get_ra(),
							     		 _get_dec(),
							     		 _get_radius(), limit)):

		params = {
		    'ext': ext,
		    'format': format,
		    'lrun': str(sdss_object[sdss_id]['run']).zfill(6),
		    'lfield': str(sdss_object[sdss_id]['field']).zfill(4)
		}

		sdss_object[sdss_id].update(params)

		# Cleaning SDSS objects
		for key in IGNORE_KEYS:
			if key in sdss_object[sdss_id]:
				del sdss_object[sdss_id][key]

		# import pdb
		# pdb.set_trace()
		# print sdss_object[sdss_id]['rerun']

		url = IDGetImageUrl.format(**sdss_object[sdss_id])
		result = requests.get(url)

		# print result.headers

		# **********************************************************
		# **********************************************************
		# **********************************************************

		# TODO: mkdir (if folder doesn't exists), if filexists, omit
		# TODO: store it in MongoDB. Use spectrumID key within sdss_object[sdss_id]

		# **********************************************************
		# **********************************************************
		# **********************************************************

		# Storing the image locally
		if result.status_code == 200:
			# payload = result.json()
			file_path = IMAGE_PATH + sdss_id + '.' + ext
			with open(file_path, 'w') as out_file:
				out_file.write(result.content)		

			logger.info("Progress ... SDSS object ID: {0} - stored in --> {1}".format(
				sdss_id, file_path))

			# Storing the sdss_object document in Mongo with astrofy application data

			astrofy_data = {
				'id': sdss_id,
				'source': url,
				'object_path': DOWNLOAD_PATH + sdss_id + EXT,
				'path': file_path,
				'object_data': sdss_object[sdss_id],
				'classified': 0,
				'event': 0,
				'clientid': None
			}

			db.objects.save(astrofy_data)

			download_count += 1
			# TODO: -> mongo: objects, results

		wait(logger, 1)

	if download_count:
		logger.info("{0} files downloaded".format(download_count))
	else:
		logger.info("No files downloaded")

	return download_count



if __name__ == '__main__':
	# for retry in xrange(0, RETRIES):
		# logger.info("Attempt {0}".format(retry))
	# 	ids = get_ids(_get_ra(), _get_dec(), _get_radius(), 50)
	# 	wait(logger)
	# 	download_files(ids)

	while(True):

		if True:
			for retry in xrange(0, RETRIES):
				logger.info("Start progress ... Attemp: {0}".format(retry))
				wait(logger)
				qty = download_files(limit=2)
				if qty:
					break
		else:
			wait(logger, 10, False)


