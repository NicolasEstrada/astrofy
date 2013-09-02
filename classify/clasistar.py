#!/usr/bin/env python

# This is a module that classify the incoming objects
# This module requires libsvm-3.17 package

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import os
import json

from  tempfile import NamedTemporaryFile

from model import load_model
from model import svm_predict
from model import svm_read_problem

from helpers.scale_set import scale
from helpers.utils import get_file_names
from helpers.features import LinealFeatures
from helpers.features import SDSSObjectTypes
from helpers.features import PolinomialFeatures
from helpers.features import LF_FIELDS, PF_FIELDS

DELIMITER = ' '

lf = LinealFeatures()
sot = SDSSObjectTypes()
pf = PolinomialFeatures()


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

    def __init__(self, obj_path, model_path=None):
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

        self.uri = obj_path
        self.id = "sdss.274.51913.93.26"
        self.objid = "1237654669203079226"

        self.obj_json = None
        self.model = None

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
        with open(self.uri, 'r') as test_file:
            content = test_file.read()
            j_obj = json.loads(content)
            self.obj_json = j_obj.values()[0]

        # Somehow a Json will be delivered
        # load on self.obj_json
        return True

    def _convert(self):
        # Create an empty features list        
        features_list = []

        for key, value in self.obj_json.items():
            if key in PF_FIELDS:
                features_list.extend(pf.get(key, value))
            elif key in LF_FIELDS:  
                features_list.extend(lf.get(key, value))

        # Formating the features as valid libvsm strings
        # {N_feature}:{value}
        # i.e: 3:-0.753235 4:1.0235252 6:-1.074325
        libvsm_str = '0' + DELIMITER
        # We are using 0 default label
        # libvsm_str = str(sot.get_svm_class(self.obj_json['objc_type'])) + DELIMITER

        libvsm_str += DELIMITER.join(features_list)

        return libvsm_str


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

        features = self._convert()
        correct = False

        with NamedTemporaryFile() as scaled_buffer:
            # Store the features in a file buffer
            # To be used as a filehandler by svm_read_problem

            with NamedTemporaryFile() as f_buffer:
                f_buffer.write(features)
                f_buffer.seek(0)


                # Scaling the generated features temp file
                scale(
                    input_path=f_buffer.name,
                    output_path=scaled_buffer.name)

            # Loading the svm problem, in this case the features file
            # to be classified.
            y, x = svm_read_problem(scaled_buffer.name)

            # Predict the value of the object
            p_label, p_acc, p_val = svm_predict(
                [y[-1]], [x[-1]], self.model, "-q")

            print 'Predict: ', sot.get_sdss_class(p_label[0])
            print 'SDSS type: ', self.obj_json['objc_type']
            print 'Value: ', p_val[0][0]

            if sot.get_sdss_class(p_label[0]) == self.obj_json['objc_type']:
                correct = True

        if correct:
            return 1
        else:
            return 0


    def __del__(self, **arg):
        # Get rid of all temp objects and files (if is required)
        pass

if __name__ == '__main__':

    results = []

    if 'ASTROFY_HOME' in os.environ:
        TEST_PATH = os.environ['ASTROFY_HOME'] + 'test/'
    else:
        TEST_PATH = 'test/'

    for n, file_path in enumerate(get_file_names(TEST_PATH), start=1):
        cs = ClassiStar(file_path)

        results.append(cs.classify())

        if n % 5 == 0:
            try:
                # raw_input("Press any key to continue or ctrl+D to quit")
                pass
            except EOFError:
                exit(0)

    print "Successful {}/{}".format(results.count(1), len(results))
