NEURON {
	POINT_PROCESS SpikeOut
	GLOBAL thresh, refrac, vrefrac, grefrac
	RANGE bias
	NONSPECIFIC_CURRENT i
}

PARAMETER {
	thresh = 1 (millivolt)
	refrac = 5 (ms)
	vrefrac = 0 (millivolt)
	grefrac = 100 (microsiemens) :clamp to vrefrac
	bias = 0 (nanoamp)
}

ASSIGNED {
	i (nanoamp)
	v (millivolt)
	g (microsiemens)
	i_bias (nanoamp)
}

INITIAL {
	net_send(0, 3)
	g = 0
	i_bias = bias
}

BREAKPOINT {
	i = g*(v - vrefrac) - i_bias
}

NET_RECEIVE(w) {
	if (flag == 1) {
		net_event(t)
		net_send(refrac, 2)
		v = vrefrac
		g = grefrac
		i_bias = 0
	}else if (flag == 2) {
		g = 0
		i_bias = bias
	}else if (flag == 3) {
		WATCH (v > thresh) 1
	}
}
