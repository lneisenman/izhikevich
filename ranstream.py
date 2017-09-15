# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

from neuron import h


class RandomStream():
    ''' A python version of the RandomStream in Brette et al 2007 that uses
        Random123

    '''
    def __init__(self, stream):
        self.stream = stream
        self.r = h.Random()
        self.r.Random123(stream, 0, 0)

    def repick(self):
        return self.r.repick()

    def binomial(self, N, p):
        self.r.binomial(N, p)

    def discunif(self, low, high):
        self.r.discunif(low, high)

    def erlang(self, mean, var):
        self.r.erland(mean, var)

    def geometric(self, mean):
        self.r.geometric(mean)

    def hypergeo(self, mean, var):
        self.r.hypergeo(mean, var)

    def lognormal(self, mean, var):
        self.r.lognormal(mean, var)

    def negexp(self, mean):
        self.r.negexp(mean)

    def normal(self, mean, var):
        self.r.normal(mean, var)

    def poisson(self, mean):
        self.r.poisson(mean)

    def uniform(self, low, high):
        self.r.uniform(low, high)

    def weibull(self, alpha, beta):
        self.r.weibull(alpha, beta)


if __name__ == '__main__':
    print('hello')
    rs = RandomStream(1)
    rs.discunif(0, 10)
    for i in range(10):
        print(i, int(rs.repick()))
