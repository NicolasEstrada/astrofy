""" This is a module have the necesary Features conversion """

__author__ = "Nicolas, Matias"
__version__ = "0.1"


class LinealFeatures(object):
	"""Lineal features id representation
	
	This class have the lineal features.
	"""

	def get(self, name):
		"""getter helper"""

		return self.__getattribute__(name)

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

class PolinomialFeatures(object):
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
	
	def get(self, name):
		"""getter helper"""

		return self.__getattribute__(name)

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
