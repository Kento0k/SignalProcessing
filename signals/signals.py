from numpy import sin, cos, arange, pi, floor, sqrt
from scipy.signal import butter, lfilter


class Signal:
    def __init__(self):
        self._t = self._get_time()
        self._cache = self._eval()
        if not hasattr(self, "title"):
            self.title = "Signal"

    def _get_time(self):
        return None

    def _eval(self):
        return None

    def get_x(self):
        return self._t

    def get_y(self):
        return self._cache

    def __mul__(self, other):
        sig = Signal()
        sig._t = self.get_x()
        sig._cache = self.get_y() * other.get_y()
        return sig

    def __add__(self, other):
        sig = Signal()
        sig._t = self.get_x()
        sig._cache = self.get_y() + other.get_y()
        return sig


class Sinusoidal(Signal):
    def __init__(self, freq, amplitude, t_start, t_end, phase=0, discretization=500, title=None):
        self.freq = freq
        self.amplitude = amplitude
        self.discretization = discretization
        self.phase = phase
        self.sample_rate = 1 / self.discretization
        self.t_start = t_start
        self.t_end = t_end
        if title is None:
            self.title = "Sinusoidal"
        else:
            self.title = title

        super().__init__()

    def _get_time(self):
        return arange(self.t_start, self.t_end, self.sample_rate)


class Sine(Sinusoidal):
    def _eval(self):
        return self.amplitude * sin(2 * pi * self.freq * self._t + self.phase)


class Cosine(Sinusoidal):
    def _eval(self):
        return self.amplitude * cos(2 * pi * self.freq * self._t + self.phase)


class DoubleSideband(Signal):
    def __init__(self, signal: Sinusoidal, carrier_freq, m=1, carrier_phase=0, title=None):
        self.signal = signal
        self.carrier_freq = carrier_freq
        self.carrier_phase = carrier_phase
        self.m = m
        if title is None:
            self.title = "DoubleSideband"
        else:
            self.title = title

        super().__init__()

    def _get_time(self):
        return self.signal._t

    def _eval(self):
        if isinstance(self.signal, Cosine):
            _func = cos
        if isinstance(self.signal, Sine):
            _func = sin
        else:
            _func = sin

        return (1 + self.m * self.signal._cache) * _func((2 * pi * self.carrier_freq * self._t + self.carrier_phase))


class Discrete(Signal):
    def __init__(self, signal: Signal, level, signal_min=-1, signal_max=1, title=None):
        self.level = level
        self.signal_min = signal_min
        self.signal_max = signal_max
        self.signal = signal
        if title is None:
            self.title = "Discrete"
        else:
            self.title = title

        super().__init__()

    def _get_time(self):
        return self.signal._t

    def _eval(self):
        y_shift = self.signal_min
        delta = (self.signal_max - self.signal_min) / self.level
        return floor((self.signal.get_y() - y_shift) / delta + 0.5)


class Detect(Signal):
    def __init__(self, source: Signal, detect_freq, filter_freq, title=None):
        self.source = source
        self.detect_freq = detect_freq
        self.filter_freq = filter_freq
        self._t = source.get_x()
        if title is None:
            self.title = "Detect"
        else:
            self.title = title

        super().__init__()

    def _get_time(self):
        return self._t

    def _eval(self):
        sin_out = self.source.get_y() * sin(2 * pi * self.detect_freq * self.source.get_x())
        cos_out = self.source.get_y() * cos(2 * pi * self.detect_freq * self.source.get_x())
        b, a = butter(2, self.filter_freq,
                      fs=(len(self.source.get_x()) / abs(self.source.get_x()[0] - self.source.get_x()[-1])))
        sin_out_butt = lfilter(b, a, sin_out)
        cos_out_butt = lfilter(b, a, cos_out)
        return sqrt(pow(sin_out_butt, 2) + pow(cos_out_butt, 2))
