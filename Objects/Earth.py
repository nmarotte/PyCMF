import imageio
import numpy as np
from pylab import *
from tqdm import tqdm

from ABC.Ticked import Ticked
from Agregations.WaterComponent import WaterComponent


class Earth(Ticked):
    def __init__(self, shape_water_component=(25, 25, 25), max_t=100):
        super().__init__(t_stop=max_t)
        self.shape = shape_water_component
        self.water_component = WaterComponent(self.shape)

    def tick(self):
        self.water_component.tick()
        self.one_tick_passed()

    def save_current_plot(self):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        temperatures = np.array([wb.temperature for wb in self.water_component.flat])
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

        colmap = cm.ScalarMappable(cmap=cm.hsv)
        colmap.set_array(np.linspace(273, 373, 100))

        ax.scatter(xs, ys, zs, c=cm.hsv(temperatures / 373), marker='o')
        cb = fig.colorbar(colmap)
        cb.ax.set_title("Temperature (°K)")

        plt.title(f"Temps t={self.t}")

        plt.savefig(f"plots/{self.t}.png")
        plt.close()

    def build_gif(self):
        with imageio.get_writer('plots/result.gif', mode='I', loop=1) as writer:
            for filename in range(self.t):
                image = imageio.imread(f"plots/{filename}.png")
                writer.append_data(image)

    def animate(self):
        with tqdm(total=self.max_t) as progress_bar:
            self.save_current_plot()
            while self.t < self.max_t:
                self.tick()
                self.save_current_plot()
                progress_bar.update(1)
            self.build_gif()

    def get_random_wb(self):
        return np.random.choice(self.water_component)


if __name__ == '__main__':
    terre = Earth(shape_water_component=(25, 25, 25), max_t=300)

    terre.animate()
