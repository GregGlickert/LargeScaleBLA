:Interneuron Cells to Pyramidal Cells GABA with local Ca2+ pool and read public soma Ca2+ pool

NEURON {
	POINT_PROCESS interD2pyrD_STFD
	USEION ca READ eca,ica
	NONSPECIFIC_CURRENT igaba
	RANGE initW
	RANGE Cdur_gaba, AlphaTmax_gaba, Beta_gaba, Erev_gaba, gbar_gaba, W, on_gaba, g_gaba
	RANGE eca, tauCa, Icatotal
	RANGE ICag, P0g, fCag
	RANGE Cainf, pooldiam, z
	RANGE lambda1, lambda2, threshold1, threshold2
	RANGE fmax, fmin, Wmax, Wmin, maxChange, normW, scaleW, srcid, destid
	RANGE pregid,postgid, thr_rp
	RANGE F, f, tauF, D1, d1, tauD1, D2, d2, tauD2
	RANGE facfactor
}

UNITS {
	(mV) = (millivolt)
        (nA) = (nanoamp)
	(uS) = (microsiemens)
	FARADAY = 96485 (coul)
	pi = 3.141592 (1)
}

PARAMETER {

	srcid = -1 (1)
	destid = -1 (1)
	
	Cdur_gaba = 0.7254 (ms)
	AlphaTmax_gaba = 7.2609 (/ms)
	Beta_gaba = 0.2667 (/ms)
	Erev_gaba = -75 (mV)
	gbar_gaba = 0.6e-3 (uS)

	Cainf = 50e-6 (mM)
	pooldiam =  1.8172 (micrometer)
	z = 2

	k = 0.01	
	
	tauCa = 50 (ms)
	
	P0g = .01
	fCag = .024
	
	lambda1 = 4 : 3 : 2 : 3.0 : 2.0
	lambda2 = .01
	threshold1 = 0.47 :  0.48 : 0.45 : 0.4 : 0.85 : 1.45 : 0.75 : 0.9 : 0.60 : 0.55 (uM)
	threshold2 = 0.52 :  0.53 : 0.5 : 0.45 : 0.9 : 1.5 : 0.8 : 1.0 : 0.70 (uM)

	:GABA Weight
	initW = 4.5 :  :  3 :  2.5 : 3 : 5 : 6.25 : 5
	fmax = 4.2
	fmin = .8
	
	GAPstart1 = 96000
	GAPstop1 = 196000
	
	thr_rp = 1 : .7
	
	facfactor = 1
	: the (1) is needed for the range limits to be effective
        f = 0 (1) < 0, 1e9 > : 1.3 (1) < 0, 1e9 >    : facilitation
        tauF = 20 (ms) < 1e-9, 1e9 >
        d1 = 0.95 (1) < 0, 1 >     : fast depression
        tauD1 = 40 (ms) < 1e-9, 1e9 >
        d2 = 0.9 (1) < 0, 1 >     : slow depression
        tauD2 = 70 (ms) < 1e-9, 1e9 >	
	
}

ASSIGNED {
	v (mV)
	eca (mV)
	ica (nA)
	
	igaba (nA)
	g_gaba (uS)
	on_gaba
	W

	t0 (ms)

	ICan (mA)
	ICag (mA)
	Afactor	(mM/ms/nA)
	Icatotal (mA)

	dW_gaba
	Wmax
	Wmin
	maxChange
	normW
	scaleW
	
	pregid
	postgid

	rp
	tsyn
	
	fa
	F
	D1
	D2	
}

STATE { r_nmda r_gaba capoolcon }

INITIAL {

	on_gaba = 0
	r_gaba = 0
	W = initW

	t0 = -1

	Wmax = fmax*initW
	Wmin = fmin*initW
	maxChange = (Wmax-Wmin)/10
	dW_gaba = 0

	capoolcon = Cainf
	Afactor	= 1/(z*FARADAY*4/3*pi*(pooldiam/2)^3)*(1e6)

	fa =0
	F = 1
	D1 = 1
	D2 = 1	
}

BREAKPOINT {
	SOLVE release METHOD cnexp
}

DERIVATIVE release {
	if (t0>0) {
		if (rp < thr_rp) {
			if (t-t0 < Cdur_gaba) {
				on_gaba = 1
			} else {
				on_gaba = 0
			}
		} else {
			on_gaba = 0
		}
	}
	if (t0>0) {
		if (rp < thr_rp) {
			if (t-t0 < Cdur_gaba) {
				on_gaba = 1
			} else {
				on_gaba = 0
			}
		} else {
			on_gaba = 0
		}
	}

	r_gaba' = AlphaTmax_gaba*on_gaba*(1-r_gaba)-Beta_gaba*r_gaba

	dW_gaba = eta(capoolcon)*(lambda1*omega(capoolcon, threshold1, threshold2)-lambda2*GAP1(GAPstart1, GAPstop1)*W)*dt

	: Limit for extreme large weight changes
	if (fabs(dW_gaba) > maxChange) {
		if (dW_gaba < 0) {
			dW_gaba = -1*maxChange
		} else {
			dW_gaba = maxChange
		}
	}

	:Normalize the weight change
	normW = (W-Wmin)/(Wmax-Wmin)
	if (dW_gaba < 0) {
		scaleW = sqrt(fabs(normW))
	} else {
		scaleW = sqrt(fabs(1.0-normW))
	}

	W = W + dW_gaba*scaleW
	
	:Weight value limits
	if (W > Wmax) { 
		W = Wmax
	} else if (W < Wmin) {
 		W = Wmin
	}


	g_gaba = gbar_gaba*r_gaba*facfactor
	igaba = W*g_gaba*(v - Erev_gaba)

	ICag = P0g*g_gaba*(v - eca)	
	Icatotal = ICag + k*ica*4*pi*((15/2)^2)*(0.01)    :  icag+k*ica*Area of soma*unit change
	capoolcon'= -fCag*Afactor*Icatotal + (Cainf-capoolcon)/tauCa
}

NET_RECEIVE(dummy_weight) {
	t0 = t
	rp = unirand()	
	
	:F  = 1 + (F-1)* exp(-(t - tsyn)/tauF)
	D1 = 1 - (1-D1)*exp(-(t - tsyn)/tauD1)
	D2 = 1 - (1-D2)*exp(-(t - tsyn)/tauD2)
 :printf("%g\t%g\t%g\t%g\t%g\t%g\n", t, t-tsyn, F, D1, D2, facfactor)
	:printf("%g\t%g\t%g\t%g\n", F, D1, D2, facfactor)
	tsyn = t
	
	facfactor = F * D1 * D2

	::F = F+f  :F * f
	
	if (F > 3) { 
	F=3	}	
	if (facfactor < 0.7) { 
	facfactor=0.7
	}
	D1 = D1 * d1
	D2 = D2 * d2
:printf("\t%g\t%g\t%g\n", F, D1, D2)
}

:::::::::::: FUNCTIONs and PROCEDUREs ::::::::::::

FUNCTION eta(Cani (mM)) {
	LOCAL taulearn, P1, P2, P4, Cacon
	P1 = 0.1
	P2 = P1*1e-4
	P4 = 1
	Cacon = Cani*1e3
	taulearn = P1/(P2+Cacon*Cacon*Cacon)+P4
	eta = 1/taulearn*0.001
}

FUNCTION omega(Cani (mM), threshold1 (uM), threshold2 (uM)) {
	LOCAL r, mid, Cacon
	Cacon = Cani*1e3
	r = (threshold2-threshold1)/2
	mid = (threshold1+threshold2)/2
	if (Cacon <= threshold1) { omega = 0}
	else if (Cacon >= threshold2) {	omega = 1/(1+50*exp(-50*(Cacon-threshold2)))}
	else {omega = -sqrt(r*r-(Cacon-mid)*(Cacon-mid))}
}
FUNCTION GAP1(GAPstart1 (ms), GAPstop1 (ms)) {
	LOCAL s
	if (t <= GAPstart1) { GAP1 = 1}
	else if (t >= GAPstart1 && t <= GAPstop1) {GAP1 = 30}					: During the Gap, apply lamda2*2
	else  {	GAP1 = 1}
}
FUNCTION unirand() {    : uniform random numbers between 0 and 1
        unirand = scop_random()
}