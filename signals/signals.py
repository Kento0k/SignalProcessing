from numpy import sin, cos, arange, pi, floor, sqrt
from scipy.signal import butter, lfilter


class Signal:
    def __init__(self):
        self._t = self._get_time()
        self._cache = self._eval()

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


class Sinusoidal(Signal):
    def __init__(self, freq, amplitude, t_start, t_end, phase=0, discretization=500):
        self.freq = freq
        self.amplitude = amplitude
        self.discretization = discretization
        self.phase = phase
        self.sample_rate = 1 / (self.freq * self.discretization)
        self.t_start = t_start
        self.t_end = t_end
        super().__init__()

    def _get_time(self):
        return arange(self.t_start, self.t_end, self.sample_rate)


class Sine(Sinusoidal):
    def _eval(self):
        return self.amplitude * sin(2 * pi * self.freq * self._t + self.phase)


class Cosine(Sinusoidal):
    def _eval(self):
        return self.amplitude * cos(2 * pi * self.freq * self._t + self.phase)


class DoubleSideband(Sinusoidal):
    def __init__(self, signal: Sinusoidal, carrier_freq, carrier_phase, m):
        self.signal = signal
        self.carrier_freq = carrier_freq
        self.carrier_phase = carrier_phase
        self.m = m
        super().__init__(signal.freq, signal.amplitude, signal.t_start, signal.t_end, signal.phase, signal.discretization)

    def _get_time(self):
        return self.signal._t

    def _eval(self):
        if isinstance(self.signal, Cosine):
            _func = sin
        if isinstance(self.signal, Sine):
            _func = cos
        return 0.5 * (1 + self.m * self.signal._cache) * _func((2 * pi * self.carrier_freq * self._t + self.carrier_phase))


class Discrete(Signal):
    def __init__(self, signal: Signal, level):
        self.level = level
        self.signal = signal
        super().__init__()

    def _get_time(self):
        return self.signal._t

    def _eval(self):
        if isinstance(self.signal, DoubleSideband):
            return floor((self.signal.get_y() + self.signal.m) * self.level / (2 * self.signal.m))
        else:
            return (1 / self.level) * floor(self.signal.get_y() * self.level + 0.5)


class Detect(Signal):
    def __init__(self, signal: Discrete):
        self.signal = signal
        super().__init__()

    def _get_time(self):
        return self.signal.get_x()

    def _eval(self):
        if isinstance(self.signal.signal, DoubleSideband):
            sin_out = self.signal * Sine(self.signal.signal.carrier_freq, 1, 0, 1, 0,
                                         1 / (self.signal.signal.carrier_freq * self.signal.signal.sample_rate))
            cos_out = self.signal * Cosine(self.signal.signal.carrier_freq, 1, 0, 1, 0,
                                           1 / (self.signal.signal.carrier_freq * self.signal.signal.sample_rate))
            b, a = butter(2, self.signal.signal.freq / (2 * self.signal.signal.carrier_freq))
            sin_out_butt = lfilter(b, a, sin_out.get_y())
            cos_out_butt = lfilter(b, a, cos_out.get_y())
            return sqrt(pow(sin_out_butt, 2) + pow(cos_out_butt, 2))
