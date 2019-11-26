from matplotlib.pyplot import figure
from scipy.fftpack import fft, fftshift, fftfreq

from signals import signals


class Plotter:
    @staticmethod
    def plot(signal: signals.Signal, t_start=0, t_end=None, _title_pref=None, _title=None, x_label="time", y_label="V"):
        fig = figure(dpi=200)
        splt = fig.add_subplot(111)

        if _title is None:
            _title = signal.title

        if _title_pref is not None:
            _title = "%s %s" % (_title_pref, _title)

        splt.set_title(_title)
        splt.set_xlabel(x_label)
        splt.set_ylabel(y_label)
        splt.set_xlim(t_start, t_end)
        splt.plot(signal.get_x(), signal.get_y())
        fig.show()

    @staticmethod
    def fourier_transform(signal: signals.Signal, _title_pref=None):
        signal_fft = abs(fftshift(fft(signal.get_y())))
        signal_fft = 2 * signal_fft / len(signal_fft)
        f_fft = fftshift(fftfreq(len(signal.get_x()), abs(signal.get_x()[1] - signal.get_x()[0])))
        cutoff = max(signal_fft) * pow(10, -3)

        last_nonzero_index = None
        for idx, item in enumerate(signal_fft):
            if item > cutoff:
                last_nonzero_index = idx
        spacing = f_fft[last_nonzero_index] * 0.1
        fig = figure(dpi=200)
        splt = fig.add_subplot(111)
        print(f_fft[last_nonzero_index])
        splt.set_xlim(-f_fft[last_nonzero_index] - spacing, f_fft[last_nonzero_index] + spacing)
        splt.plot(f_fft, signal_fft)
        title = "%s Fourier spectrum" % signal.title
        if _title_pref is not None:
            title = "%s %s" % (_title_pref, title)
        splt.set_title(title)
        fig.show()
