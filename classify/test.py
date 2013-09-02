#!/usr/bin/env python

from clasistar import ClassiStar
from features import LinealFeatures, PolinomialFeatures

if __name__ == '__main__':
	cs = ClassiStar()
	lf = LinealFeatures()
	print 'score', lf.get('score')
	pf = PolinomialFeatures()
	print 'petromag', pf.get('petromag') + pf.band('u')
