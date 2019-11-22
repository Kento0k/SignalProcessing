from signals.signals import Signal, Sine, DoubleSideband, Discrete, Detect
from plotter.plotter import Plotter
from matplotlib import pyplot
import numpy as np


def task1(original_signal: Signal, original_freq, carrier_freq, k=64, noise_freq=None):
    Plotter.plot(original_signal)
    Plotter.fourier_transform(original_signal)

    modulated_signal = DoubleSideband(original_signal, carrier_freq)
    if noise_freq is not None:
        modulated_signal = modulated_signal + Sine(noise_freq, amplitude=amplitude, t_start=0, t_end=1,
                                                discretization=10000)
    Plotter.plot(modulated_signal, t_end=0.1)
    Plotter.fourier_transform(modulated_signal)

    discrete_signal = Discrete(modulated_signal, k, signal_min=min(modulated_signal.get_y()),
                               signal_max=max(modulated_signal.get_y()))
    Plotter.plot(discrete_signal, t_end=0.1)

    detected_signal = Detect(discrete_signal, carrier_freq, filter_freq=30)
    Plotter.plot(detected_signal, t_end=0.1)
    Plotter.fourier_transform(detected_signal)

    detected_signal2 = Detect(detected_signal, original_freq, filter_freq=7)
    Plotter.plot(detected_signal2)
    Plotter.fourier_transform(detected_signal2)

    lbound = max(detected_signal2.get_y()) / pow(10, 3/20)
    print("lbound: %d" % lbound)
    sig_out = np.ones(len(detected_signal2.get_x()))
    for i in range(0, len(detected_signal2.get_x())):
        if detected_signal2.get_y()[i] <= lbound:
            sig_out[i] = 0
        else:
            break

    k = 1
    while sig_out[k] == 0:
        k = k + 1
        if k == sig_out.__len__() - 1:
            break
    print('delay: %f' % detected_signal2.get_x()[k])
    pyplot.plot(detected_signal.get_x(), sig_out, '.')
    # pyplot.xlim(0, 1000)
    pyplot.show()


if __name__ == '__main__':
    ################ lab params #########################
    original_freq = 19
    carrier_freq = 650
    k = 1024

    ################ othe params ####################
    amplitude = 1
    t_start, t_end = 0, 1

    noise_freq_1 = carrier_freq - 2.5 * original_freq
    noise_freq_2 = carrier_freq - 4 * original_freq

    ################ main part ####################
    original_signal = Sine(original_freq, amplitude=amplitude, t_start=t_start, t_end=t_end, discretization=10000)
    task1(original_signal, original_freq, carrier_freq, k=k)

    task1(original_signal, original_freq, carrier_freq, k=k, noise_freq=noise_freq_1)
    task1(original_signal, original_freq, carrier_freq, k=k, noise_freq=noise_freq_2)
    # noised_signal_1 = original_signal + Sine(noise_freq_1, amplitude=amplitude, t_start=t_start, t_end=t_end,
    #                                          discretization=10000)
    # task1(noised_signal_1, original_freq, carrier_freq, k=k)
    #
    # modulated_signal = DoubleSideband(original_signal, carrier_freq)
    # noised_signal_1_1 = modulated_signal + Sine(noise_freq_1, amplitude=amplitude, t_start=t_start, t_end=t_end,
    #                                             discretization=10000)
    # pyplot.plot(noised_signal_1_1.get_x(), noised_signal_1_1.get_y())
    # pyplot.xlim(0, 0.1)
    # pyplot.title("ZASHUMLENNYI")
    # pyplot.show()
    #
    # noised_signal2 = original_signal + Sine(noise_freq_2, amplitude=amplitude, t_start=t_start, t_end=t_end,
    #                                         discretization=10000)
    # task1(noised_signal2, original_freq, carrier_freq, k=k)
