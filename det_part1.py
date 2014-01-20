# Written by Andrej Prsa
# Comments added by Meredith Rawls
# This creates a fake light curve and bins it to give an approximation
# of the desired signal. The binning can then be used to detrend it.

import numpy as np

# time and lc go together (unfolded data)
# phase and flux go together (folded data)

class Data:
    def __init__(self, period, timespan=2*np.pi):
        self.period = period
        self.time = None
        self.phase = None
        self.lc = None
        self.timespan = timespan
        return
        
    def generate(self, sigma, freq1, amp=1, y0=0, N=2000, freq2=0, amp2=0):
        self.time = np.linspace(0, self.timespan, N)
        self.phase = (self.time % self.period) / self.period
        self.lc = y0+amp*np.sin(freq1*self.time)+np.random.normal(scale=sigma, size=N)+amp2*np.cos(freq2*self.time)
        self.pts = zip(self.phase, self.lc)
        self.pts.sort()
        return

    def __str__(self):
        out = ""
        for i in range(len(self.time)):
            out += "%f\t%f\n" % (self.time[i], self.lc[i])
        return out

class Signal:
    def __init__(self, bins, period, data, flux=None):
        self.bins = bins
        self.period = period
        self.phase = np.linspace(0, 1, bins)
        self.data = data
        if flux != None:
            self.flux = flux
        else:
            self.flux = np.histogram(self.data.phase, self.bins, weights=self.data.lc)[0]/np.histogram(self.data.phase, self.bins)[0]
        return

    def clc(self):
        self.lc = [self.flux[int(self.bins*ph)] for ph in self.data.phase]


d = Data(2*np.pi/5, timespan=10.)
d.generate(sigma=0.02, freq1=5.0, amp=0.1, y0=1.0, amp2=0.1, freq2=1./np.sqrt(2))

s = Signal(201, 2*np.pi/5, d)
s.clc()

from pylab import *
#~ plot(d.phase, d.flux, 'b.')
#~ bar(s.phase, s.flux, 1./s.bins)
subplot(211)
plot(d.time, d.lc, 'b-')
subplot(212)
plot(d.time, d.lc-s.lc, 'r-')
show()
