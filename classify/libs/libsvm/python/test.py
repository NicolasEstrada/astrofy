"""This script execute a test on libsvm python module
"""

__author__ = "Matias, Nicolas"
__version__ = "0.1"

from svmutil import svm_train
from svmutil import svm_read_problem
from svmutil import svm_predict

if __name__ == '__main__':

	y, x = svm_read_problem('datasets/url_combined')
	m = svm_train(y[:200], x[:200], '-c 4')
	p_label, p_acc, p_val = svm_predict(y[200:400], x[200:400], m)
