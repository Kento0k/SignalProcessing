from signals.signals import Signal, Sine, DoubleSideband, Discrete, Detect
from plotter.plotter import Plotter
from matplotlib import pyplot
import numpy as np


def task1(original_signal: Signal, original_freq, carrier_freq):
    Plotter.plot(original_signal)
    Plotter.fourier_transform(original_signal)

    modulated_signal = DoubleSideband(original_signal, carrier_freq)
    Plotter.plot(modulated_signal, t_end=0.1)
    Plotter.fourier_transform(modulated_signal)

    discrete_signal = Discrete(modulated_signal, 64, signal_min=min(modulated_signal.get_y()), signal_max=max(modulated_signal.get_y()))
    Plotter.plot(discrete_signal, t_end=0.1)

    detect1 = Sine(carrier_freq, 1, 0, 1, discretization=10000)
    detected_signal = Detect(discrete_signal, carrier_freq, filter_freq=100)
    Plotter.plot(detected_signal, t_end=0.1)
    Plotter.fourier_transform(detected_signal)

    detect2 = Sine(original_freq, 1, 0, 1, discretization=10000)
    detected_signal2 = Detect(detected_signal, original_freq, filter_freq=1)
    Plotter.plot(detected_signal2)
    Plotter.fourier_transform(detected_signal2)

    lbound = 3
    sig_out = np.ones(len(detected_signal2.get_x()))
    for i in range(0, len(detected_signal2.get_x())):
        if detected_signal2.get_y()[i] <= lbound:
            sig_out[i] = 0
        else:
            break

    k = 1
    while sig_out[k] == 0:
        k = k + 1
    print(detected_signal2.get_x()[k])

    pyplot.plot(sig_out, '.')
    # pyplot.xlim(0, 1000)
    pyplot.show()

original_freq = 38
carrier_freq = 892
noise1 = carrier_freq - 2.5 * original_freq
noise2 = carrier_freq - 4 * original_freq

original_signal = Sine(38, 1, 0, 1, discretization=10000)
task1(original_signal, original_freq, carrier_freq)

noised_signal1 = original_signal + Sine(noise1, 1, 0, 1, discretization=10000)
task1(noised_signal1, original_freq, carrier_freq)

noised_signal2 = original_signal + Sine(noise2, 1, 0, 1, discretization=10000)
task1(noised_signal2, original_freq, carrier_freq)


