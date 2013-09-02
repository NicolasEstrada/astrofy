# This is a module that classify the incoming objects
# This module requires libsvm-3.17 package

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import json

from model import load_model


class ClassiStar(object):
	"""docstring for ClassiStar

	This class do an automatic classification using libsvm.

	Attributes
		uri: A str representing the object location.
		id: An unique identifier from the OS.
		objid: An unique identifier from SDDS API
		.
		.
		.
	"""

	def __init__(self, model_path=None):
		"""initiaze object parameters.

		Args:
			uri: direction(s) (absolute or relative) to fetch the file(s)
			id: object id i.e sdss.274.51913.93.26 (or some local id def)
		 	objid: sdss3 api object id 1237654669203079226

		"""
		super(ClassiStar, self).__init__()

		self._version = __version__
		self.authors = __author__
		self._description = "Astronomical object clasification"

		self.uri = "protocol://some/location/somewhere"
		self.id = "sdss.274.51913.93.26"
		self.objid = "1237654669203079226"

		self._get_object()
		self._load_model(model_path)

	def _load_model(self, file_path):
		"""Loads the model

		Loads the svm model generated with the training set.

		Args:
			file_path: absolute or relative path to the model file
		
		Returns:
			A bool representing if the operation was successful or not.
		
		Raise:
			Exception: Uncaught exception.
		"""

		self.model = load_model()
		return True


	def _get_object(self, **arg):
		""" Get the object
		
		Retrieves the objects related to the provided uri and id
		from the Objects Store or the SDSS api

		Args:
			uri: direction(s) (absolute or relative) to fetch the file(s)

		Returns:
			A bool representing if the operation was successful or not.
		
		Raise:
			Exception: Uncaught exception.
		"""

		# Get object
		test_file_path = '/home/mestrada/devel/ili136/samples/sdss.274.51913.93.26.json'
		with open(test_file_path, 'r') as test_file:
			content = test_file.read()
			j_obj = json.loads(content)
			self.obj_json = j_obj.values()[0]

		print self.obj_json['objc_type']
		# Somehow a Json will be delivered
		# load on self.obj_json
		return True

	def classify(self, **arg):
		""" Classify the loaded object.

		Classify the object with a SVM (external library) based on the
		extracted features.

		Returns:
			A dict mapping representing the classification result.
			Example:
			{'objid': 1237654669203079226,
			 'sdds_type': 'star',
			 'class_type': 'star',
			 'elapsed_time': 2.12,
			 .
			 .
			 .
			}

		Raise:
			Exception: Uncaught exception.
		"""
		pass

	def __del__(self, **arg):
		# Get rid of all temp objects and files (if is required)
		pass
