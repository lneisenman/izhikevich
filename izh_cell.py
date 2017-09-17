# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

from neuron import h


h.nrn_load_dll("./mod_files/nrnmech.dll")    # load the model dll files


class IzhCell():
    """
    A python version of the icell template from Ted's Izhmodel with the synapse
    model from Brette et al 2007
    """
    def __init__(self):
        self.soma = h.Section(name="soma")
        h.pt3dclear()
        h.pt3dadd(0, 0, 0, 1)
        h.pt3dadd(15, 0, 0, 1)
        self.x = self.y = self.z = 0
        self.soma.L = 10
        self.soma.diam = 3.1831
        self.soma.Ra = 100
        self.soma.cm = 1
        self.soma.insert('pas')
        self.soma.g_pas = 5e-5
        self.soma.e_pas = -70
        self.izh = h.Izh(0.5, sec=self.soma)
        self.izh.amp = 0
        self.all = h.SectionList()
        self.all.append()
        self.make_synapses()

    def position(self, x, y, z):
        for i in range(h.n3d()):
            h.pt3dchange(i, x+self.x+h.x3d(i), y+self.y+h.y3d(i),
                         z+self.z+h.z3d(i), h.diam3d(i))
            self.x = x
            self.y = y
            self.z = z

    def is_art(self):
        return 0

    def make_synapses(self):
        self.synlist = list()
        syn = h.ExpSyn(0.5, sec=self.soma)
        syn.tau = 5
        self.synlist.append(syn)

        syn = h.ExpSyn(0.5, sec=self.soma)
        syn.tau = 10
        syn.e = -80
        self.synlist.append(syn)

    def connect2target(self, target):
        self.soma.push()
        nc = h.NetCon(self.soma(0.5)._ref_v, target)
        h.pop_section()
        return nc

    def set_params(self, a=0.02, b=0.2, c=-65, d=8):
        ''' set a, b, c and d to achieve different behaviors

        The defaults set the parameters to those of a regular spiking (RS)
        cell assuming the equation coefficients are the defaults of
        0.04, 5 and 140 (v' = 0.04v**2 + 5v + 140) '''

        self.izh.a = a
        self.izh.b = b
        self.izh.c = c
        self.izh.d = d

    def set_coeffs(self, e=0.04, f=5, g=140):
        ''' set the coefficents of the equation v' = e*v**2 + f*v +g

        The defaults set the coefficients to the standard values for the
        published cell types '''

        self.izh.e = e
        self.izh.f = f
        self.izh.g = g

    def RS(self):
        ''' set params for regular spiking (RS) behavior '''
        self.set_params(a=0.02, b=0.2, c=-65, d=8)
        self.set_coeffs(e=0.04, f=5, g=140)

    def IB(self):
        ''' set params for intrinsically bursting (IB) behavior '''
        self.set_params(a=0.02, b=0.2, c=-55, d=4)
        self.set_coeffs(e=0.04, f=5, g=140)

    def CH(self):
        ''' set params for chattering (CH) behavior '''
        self.set_params(a=0.02, b=0.2, c=-50, d=2)
        self.set_coeffs(e=0.04, f=5, g=140)

    def FS(self):
        ''' set params for fast spiking (FS) behavior '''
        self.set_params(a=0.1, b=0.2, c=-65, d=2)
        self.set_coeffs(e=0.04, f=5, g=140)

    def class1(self):
        ''' set params for class 1 behavior '''
        self.set_params(a=0.02, b=-0.1, c=-55, d=6)
        self.set_coeffs(e=0.04, f=4.1, g=108)

    def class2(self):
        ''' set params for class 2 behavior '''
        self.set_params(a=0.2, b=0.26, c=-65, d=0)
        self.set_coeffs(e=0.04, f=5, g=140)

if __name__ == '__main__':
    print('hello')
    cell = IzhCell()
    print(cell.soma.diam, cell.soma.cm)
    h.psection()
