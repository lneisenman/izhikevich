# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

import matplotlib.pyplot as plt
from neuron import h
import numpy as np
import pandas as pd
import scipy.stats as stats

import netutils as nu

from izh_cell import IzhCell


def run(end_time):
    sc = nu.SimulationController()
    sc.set_fixed_dt(0.1)
    sc.set_v_init(-60)
    sc.set_celsius(36)
    sc.stdrun(end_time)


def single():
    cell = IzhCell()
    cell.class1()
#    cell.izh.amp = 0
#    cell.izh.delay = 0
#    cell.izh.dur = 1e9

    tvec = h.Vector()
    tvec.record(h._ref_t)
    vvec = h.Vector()
    vvec.record(cell.soma(0.5)._ref_v)

    recording = nu.SpikeRecorder([cell])
    run(30*60000)

    times = recording.tvec.as_numpy()
    deltas = np.diff(times)
    plt.hist(deltas, bins=50, normed=True)
    x = np.linspace(1, 10000, 10000)
    mu, std = stats.norm.fit(deltas)
    norm = stats.norm.pdf(x, mu, std)
    plt.plot(x, norm, 'r')
    print(stats.kstest(deltas, 'norm', args=stats.norm.fit(deltas)))
    a, b = stats.expon.fit(deltas)
    print(a, b)
    exp = stats.expon.pdf(x, a, b)
    plt.plot(x, exp, 'g')
    print(stats.kstest(deltas, 'expon', args=stats.norm.fit(deltas)))
    plt.figure()
#    plt.plot(tvec, vvec)


def pair():
    cell1 = IzhCell()
    cell1.class1()
    cell2 = IzhCell()
    cell2.class1()

    tvec = h.Vector()
    tvec.record(h._ref_t)
    vvec1 = h.Vector()
    vvec2 = h.Vector()
    vvec1.record(cell1.soma(0.5)._ref_v)
    vvec2.record(cell2.soma(0.5)._ref_v)

    recording = nu.SpikeRecorder([cell1, cell2])
    run(20000)

    plt.plot(tvec, vvec1)
    plt.plot(tvec, vvec2)

    nu.draw_raster_plot(recording)
    spike_times = nu.separate_cells(recording)
    print(spike_times.keys())
    print(spike_times[1])


if __name__ == '__main__':
    plt.style.use({'axes.spines.top': False, 'axes.spines.right': False})
    h.load_file("stdrun.hoc")       # load the standard run libraries
#    single()
    pair()
