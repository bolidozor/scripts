#!/usr/bin/env python3

'''
Detector of linearly-frequency-modulated signal segments
========================================================

This script reads samples on its standard input, runs them through
a detector of linearly-frequency-modulated segments and then produces
a series of waterfall plots with the detections overlaid.

The detector attempts to find contributions to the signal of the form

    A*exp(2j*pi*(f*x + 1/2*a*x**2))

where _x_ is sample number going from zero upward, _A_ is complex
amplitude, and _f_ and _a_ are some real parameters. This prescribes
signal whose frequency changes linearly with time, _f_ being
the starting frequency and _a_ the frequency slope. (The frequency
and its slope are, respectively, in units of cycle per sample and
cycle per sample squared.)

The detector separates samples on the script's input into frames of
some fixed length N. These frames are multiplied with a window
function and a phase factor, then they are transformed with DFT. 

The window function is an ordinary Hann window. The phase factor
varies from sample to sample and is of the form

    exp(-1j*pi*b*x**2)

where _x_ is sample number going from 0 to N-1 and _b_ is a fixed
parameter.

Effect of the phase factor on a linearly modulated signal
---------------------------------------------------------

Suppose the frame resembles a linearly modulated signal. Multiplying
samples of the frame with the phase factor has the effect of changing
the frequency slope. If the parameter _b_ coincides with frequency slope
_a_ of the linearly-modulated signal, the frequency slope is zeroed out
and the transformed signal is a constant-frequency one, which will then
have strong response in one of the DFT bins.

For each frame, the detector varies _b_ and repeats the DFT. This then
produces a 2D array. Parameter _b_ varies along one axis of the array,
while DFT bins correspond to the other axis of the array.

The detector searches the array for local maxima in absolute value.
Such a maximum is then considered a detection of linearly-modulated
constituent signal with parameters derived from location of the maximum
within the array. 

Usage
-----

    $ ./lfms_detector.py SAMPLE_RATE OUTPUT_PLOTS_PREFIX < SAMPLES

Input is expected to be raw 32-bit floating-point quadrature samples
with I and Q channels interleaved.

'''


import matplotlib as mpl
mpl.use('Agg')

import numpy as np
from subprocess import check_output
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from skimage.feature import peak_local_max
import sys
import math
from tqdm import tqdm
tqdm_notebook = tqdm


def waterfall_image(signal, bins):
    window = 0.5 * (1.0 - np.cos((2 * math.pi * np.arange(bins)) / bins))
    segment = int(bins / 2)
    nsegments = int(len(signal) / segment)
    m = np.repeat(np.reshape(signal[0:segment * nsegments], (nsegments, segment)), 2, axis=0)
    t = np.reshape(m[1:len(m) - 1], (nsegments - 1, bins))
    dfts = np.fft.fft(np.multiply(t, window))
    dfts_ = np.concatenate((dfts[:, int(bins / 2):bins], dfts[:, 0:int(bins / 2)]), axis=1)
    return np.log(np.abs(dfts_))


def waterfall(samples, sample_rate, time_offset=0, freq_offset=0, freq_lim=None, bins=8192, ax=None):
    '''
    waterfall sets up a matplotlib figure with waterfall plot of the signal
    passed in _samples_.
    '''

    img = waterfall_image(samples, bins).T
    img[np.isneginf(img)] = np.nan

    dpi = 80
    margin = 0.05
    xpixels, ypixels = img.shape
    figsize = (1+margin)*ypixels/dpi*3, (1+margin)*xpixels/dpi*3

    if ax is None:
        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = fig.add_axes([margin, margin, 1-2*margin, 1-2*margin])

    vmin = np.percentile(img, 50)
    vmax = vmin + 6.6

    ax.imshow(img, extent=[time_offset, time_offset + len(samples)/sample_rate,
                           freq_offset + sample_rate/2, freq_offset - sample_rate/2],
              aspect='auto', interpolation='none', cmap='magma', norm=Normalize(vmin=vmin, vmax=vmax))
    ax.set_xlabel('Time [s]'); ax.set_ylabel('Frequency [Hz]');

    if freq_lim is not None:
        ax.set_ylim(freq_lim[0] + freq_offset, freq_lim[1] + freq_offset)

    return (fig, ax)


def lfms_search(x):
    '''
    lfms_search implements the detection itself. Given a frame _x_, it repeats
    the DFT with different values for the parameter _b_ described earlier.
    (In code, the parameter is called _a_.)
    '''

    bins = len(x)
    i = np.arange(bins)

    window = 0.5 * (1.0 - np.cos((2 * math.pi * i) / bins))
    a_space = np.arange(-0.40, 0.40, 0.002)/bins/2/np.pi
    
    field_ = np.array([np.fft.fft(x*window*np.exp(-1j*np.pi*a*i**2))
                       for a in a_space])
    field = np.abs(field_)

    ret = []
    for indices in peak_local_max(np.log(field), min_distance=100, exclude_border=True):
        indices = tuple(indices)
        a = a_space[indices[0]]
        bin_ = indices[1]
        db_level = np.log10(field[indices]/bins*2)*20

        ret.append((db_level, (bin_/bins+0.5)%1-0.5, a))

    return ret


def lfms_search_plot(sig, sig_sr, time_offset=0, nbins=128, vizu_nbins=128):
    sr = sig_sr

    # pass frames to lfms_search
    findings = ((x, lfms_search(sig[nbins*x:nbins*(x+1)]))
                for x in tqdm_notebook(range(int(len(sig)/nbins))))

    # combine detections from different frames into one array
    coords = [(level, x*nbins, freq*sr, nbins, a*nbins*sr)
              for x, frame_findings in findings
              for level, freq, a in frame_findings]

    fig, ax = waterfall(sig, sig_sr, bins=vizu_nbins, time_offset=time_offset)

    # draw detections into the waterfall plot
    levels = [level for level, _a, _b, _c, _d in coords]
    lmin = np.percentile(levels, 20)
    lmax = np.percentile(levels, 95)
    for level, x, y, dx, dy in coords:
        color_alpha = min(1.0, max((level-lmin)/(lmax-lmin), 0.0))
        ax.arrow(time_offset + x/sig_sr, y, dx/sig_sr, dy,
                 color=(0.0, 1.0, 0.0, color_alpha))
    return coords, fig


def main():
    sample_rate, output_prefix = float(sys.argv[1]), sys.argv[2]
    snapshot_period = 60*4

    time = 0
    while True:
        inp = sys.stdin.buffer.read(8 * int(sample_rate * snapshot_period))
        if not inp:
            break
        sig = np.fromstring(inp, dtype=np.complex64)

        _, fig = lfms_search_plot(
            sig, sample_rate, time_offset=time,
            nbins=16384, vizu_nbins=2048
        )
        fn = ('%s_%06d.png' % (output_prefix, time))
        print("writing %s" % fn)
        fig.savefig(fn)

        time += snapshot_period


if __name__ == "__main__":
    main()
