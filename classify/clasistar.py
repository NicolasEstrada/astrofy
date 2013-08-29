# This is a module that classify the incoming objects
# This module requires libsvm-3.17 package

__author__ = "Nicolas, Matias"
__version__ = "0.1"


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

	def __init__(self, arg):
		"""initiaze object parameters.

		Args:
			uri: direction(s) (absolute or relative) to fetch the file(s)
			id: object id i.e sdss.274.51913.93.26 (or some local id def)
		 	objid: sdss3 api object id 1237654669203079226
		"""
		super(ClassiStar, self).__init__()

	def _get_object(self, arg):
		""" Get the object
		
		Retrieves the objects related to the provided uri and id
		from the Objects Store or the SDSS api

		Args:
			uri: direction(s) (absolute or relative) to fetch the file(s)

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

	def __del__(self, arg):
		# Get rid of all temp objects and files (if is required)
		pass
