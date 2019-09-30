from signals import signals
from matplotlib.pyplot import figure, title, show, xlabel, ylabel
# import matplotlib.pyplot as plt


class Plotter:
    @staticmethod
    def plot(signal: signals.Signal, _title ="Signal", x_label ="time", y_label ="V"):
        fig = figure()
        splt = fig.add_subplot(111)
        splt.plot(signal.get_x(), signal.get_y())
        fig.show()