from abc import ABC, abstractmethod

import imageio
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

from ABC.Ticked import Ticked


class Plotable(Ticked, ABC):
    def __init__(self, shape: tuple, t_stop: int):
        super().__init__(t_stop)
        self.shape = shape
        self.colmap = None

    @abstractmethod
    def data_to_plot(self):
        """
        abstraction of what property to plot, to redefine in subclass depending on the property you want to watch
        :return:
        """

    def save_current_plot(self):
        if self.colmap is None:
            self.colmap = cm.ScalarMappable(cmap=cm.hsv)
            self.colmap.set_array(np.linspace(min(self.data_to_plot()), max(self.data_to_plot()), 100))
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        xs = []
        ys = []
        zs = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                for k in range(self.shape[2]):
                    xs.append(i)
                    ys.append(j)
                    zs.append(k)

        xs = np.array(xs)
        ys = np.array(ys)
        zs = np.array(zs)

        ax.scatter(xs, ys, zs, c=cm.hsv(self.data_to_plot() / 373), marker='o')
        cb = fig.colorbar(self.colmap)
        cb.ax.set_title("Temperature (°K)")

        plt.title(f"Temps t={self.t}")

        plt.savefig(f"InputOutput/Outputs/plots/{self.t}.png")
        plt.close()

    def build_gif(self):
        with imageio.get_writer('InputOutput/Outputs/plots/result.gif', mode='I', loop=1) as writer:
            for filename in range(self.t):
                image = imageio.imread(f"InputOutput/Outputs/plots/{filename}.png")
                writer.append_data(image)
