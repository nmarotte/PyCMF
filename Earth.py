import imageio
from pylab import *
from tqdm import tqdm
import numpy as np

from WaterBody import WaterBody


class Earth:
    def __init__(self, shape_water_component=(10, 10, 10), max_t=10):
        self.shape = shape_water_component
        self.water_bodies = WaterBody.generate_as_shape(self.shape)
        self.t = 0
        self.max_t = max_t

    def tick(self):
        for wb in self.water_bodies.flat:
            wb.tick()

        self.t += 1

    def animate(self):
        with tqdm(total=self.max_t) as progress_bar:
            self.save_current_plot()
            while self.t < self.max_t:
                self.tick()
                self.save_current_plot()
                progress_bar.update(1)
            self.build_gif()

    def save_current_plot(self):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        temperatures = np.array([wb.temperature for wb in self.water_bodies.flat])
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

        yg = ax.scatter(xs, ys, zs, c=cm.hsv(temperatures / 373), marker='o')
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

    def get_random_wb(self):
        return np.random.choice(self.water_bodies.flat)


if __name__ == '__main__':
    terre = Earth(max_t=300)
    for i in range(50):
        terre.get_random_wb().temperature = 373

    terre.animate()
