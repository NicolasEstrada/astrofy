""" This is a module have the necesary Features conversion """

__author__ = "Nicolas, Matias"
__version__ = "0.1"



class Feature(object):
	"""Feature class

	Generic Feature class"""

	FEATURE = "{feature}:{value}"

	def __init__(self):
		super(Feature, self).__init__()

	def _getattr(self, name):
		try:
			return object.__getattribute__(self, name)
		except AttributeError:
			return None

	def get(self, name, value):
		"""getter helper"""

		attr = self._getattr(name)

		if attr != None:
			return self.convert(attr, value)

		return []

	def convert(self):
		raise NotImplementedError


class LinealFeatures(Feature):
	"""Lineal features id representation
	
	This class have the lineal features.
	"""

	def __init__(self):
		super(LinealFeatures, self).__init__()

	score     = 0
	wavemax   = 1
	elodie_bv = 2
	rchi2     = 3
	rchi2diff = 4
	colvdeg   = 5
	chi68p    = 6
	sn_median = 7
	vdispdof  = 8
	score     = 9
	objc_colc = 10
	z         = 11
	wavemin   = 12
	wavemax   = 13
	vdisp     = 14
	b 		  = 15
	vdispchi2 = 16
	vdispnpix = 17
	objc_rowc = 18
	objc_flags= 19
	dof       = 20

	def convert(self, attr, value):
		"""Convert the feature in a svm valid feature string"""

		# We return a iterable to extend the final features list
		if not isinstance(value, dict):
			return (self.FEATURE.format(feature=attr, value=value), )
		return ()


class PolinomialFeatures(Feature):
	"""Polinomial or multi-dimension features

	Band Order:
		i = 1
		r = 2
		u = 3
		z = 4
		g = 5

	Example
	astrobj['cmodelmag'] = 
	{
	'i': 16.569,
	'r': 17.058,
	'u': 19.5772,
	'z': 16.2163,
	'g': 18.3169}
	
	cmodelmag base code = 400
	cmodelmag -> i = 401

	"""

	def __init__(self):
		super(PolinomialFeatures, self).__init__()

	indexes = {
		"i" : 1,
		"r" : 2,
		"u" : 3,
		"z" : 4,
		"g" : 5
	}

	def band(self, name):
		"""Band index getter helper"""

		return self.indexes[name]

	def convert(self, attr, values):
		"""Convert the feature in a svm valid feature string

		Example of values:
		astrobj['cmodelmag'] = 
		{
		'i': 16.569,
		'r': 17.058,
		'u': 19.5772,
		'z': 16.2163,
		'g': 18.3169}
		"""
		# We return a iterable to extend the final features list
		features = []

		for band, value in values.items():	
			features.append(self.FEATURE.format(
				feature=attr + self.band(band),
				value=value)
			)


		return features

	spectrosynflux 		= 30
	offsetdec 			= 40
	modelflux_ivar 		= 50
	colc 				= 60
	spectroflux_ivar 	= 70
	flags2 				= 80
	m_cr4 				= 90
	fracdev 			= 100
	rowc 				= 110
	aperflux 			= 120
	star_lnl 			= 130
	petroflux 			= 140
	petroth50 			= 150
	nmgypercount 		= 160
	spectrosynflux_ivar = 170
	expflux 			= 180
	petromag 			= 190
	theta_exp 			= 200
	psfflux_ivar 		= 210
	dev_lnl 			= 220
	m_e2 				= 230
	m_e1 				= 240
	psfmag 				= 250
	airmass 			= 260
	modelflux 			= 270
	m_rr_cc_psf 		= 280
	spec2 				= 290
	fiberflux 			= 300
	spec1 				= 310
	spectroflux 		= 320
	skyflux 			= 330
	offsetra 			= 340
	ab_dev 				= 350
	psf_fwhm 			= 360
	petrotheta 			= 370
	phi_offset 			= 380
	modelmag 			= 390
	cmodelmag 			= 400
	m_e2_psf 			= 410
	ab_exp 				= 420
	devflux_ivar 		= 430
	fiber2flux 			= 440
	m_e1_psf 			= 450
	spectroskyflux 		= 460
	petroth9 			= 470
	expmag 				= 480
	phi_exp_deg 		= 490
	phi_dev_deg 		= 500
	extinction 			= 510
	cmodelflux 			= 520
	fiber2mag 			= 530
	m_cr4_psf 			= 540
	profmean_nmgy 		= 550
	exp_lnl 			= 560
	theta_dev 			= 570
	m_rr_cc 			= 580
	devflux 			= 590
	q 					= 600
	u 					= 610


class SDSSObjectTypes(object):
	"""docstring for SDSSObjectTypes"""
	def __init__(self):
		super(SDSSObjectTypes, self).__init__()

	indexes = {
		0: "Unknown",
		1: "Cosmic Ray",
		2: "Defect",
		3: "Galaxy",
		4: "Ghost",
		5: "Known object",
		6: "Star",
		7: "Star trail",
		8: "Sky"}

	# We have 2 classes (Star and Galaxy) for the SVM
	svm_classes = {
		3: -1,
		6: 1}

	def get_svm_class(self, obj_type):
		"""Getter helper to get the svm class"""
		return self.svm_classes.get(int(obj_type))


LF_FIELDS = [
	'score',
	'wavemax',
	'elodie_bv',
	'rchi2',
	'rchi2diff',
	'colvdeg',
	'chi68p',
	'sn_median',
	'vdispdof',
	'score',
	'objc_colc',
	'z',
	'wavemin',
	'wavemax',
	'vdisp',
	'b',
	'vdispchi2',
	'vdispnpix',
	'objc_rowc',
	'objc_flags',
	'dof']

PF_FIELDS =[
	'spectrosynflux',
	'offsetdec',
	'modelflux_ivar',
	'colc',
	'spectroflux_ivar',
	'flags2',
	'm_cr4',
	'fracdev',
	'rowc',
	'aperflux',
	'star_lnl',
	'petroflux',
	'petroth50',
	'nmgypercount',
	'spectrosynflux_ivar',
	'expflux',
	'petromag',
	'theta_exp',
	'psfflux_ivar',
	'dev_lnl',
	'm_e2',
	'm_e1',
	'psfmag',
	'airmass',
	'modelflux',
	'm_rr_cc_psf',
	'spec2',
	'fiberflux',
	'spec1',
	'spectroflux',
	'skyflux',
	'offsetra',
	'ab_dev',
	'psf_fwhm',
	'petrotheta',
	'phi_offset',
	'modelmag',
	'cmodelmag',
	'm_e2_psf',
	'ab_exp',
	'devflux_ivar',
	'fiber2flux',
	'm_e1_psf',
	'spectroskyflux',
	'petroth9',
	'expmag',
	'phi_exp_deg',
	'phi_dev_deg',
	'extinction',
	'cmodelflux',
	'fiber2mag',
	'm_cr4_psf',
	'profmean_nmgy',
	'exp_lnl',
	'theta_dev',
	'm_rr_cc',
	'devflux',
	'q',
	'u']
