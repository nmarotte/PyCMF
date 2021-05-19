
import numpy as np

from tqdm import tqdm
import cv2

from ABC.Plotable import Plotable
from ABC.Ticked import Ticked
from Agregations.AirComponent import AirComponent
from Agregations.SoilComponent import SoilComponent
from Agregations.WaterComponent import WaterComponent
from Objects.CubeOfSoil import CubeOfSoil
from Objects.CubeOfWater import CubeOfWater

from Utils import neighbors_single, neighbors_multi


class Earth(Plotable):
    circumference = 40075000  # [m]

    def __init__(self, shape, t_stop, wc=None, sc=None, ac=None):
        super().__init__(shape, t_stop=t_stop)
        self.water_component = WaterComponent.full_component(shape, t_stop) if wc is None else wc
        self.soil_component = SoilComponent.full_component(shape, t_stop) if sc is None else sc
        self.air_component = AirComponent(shape, t_stop) if ac is None else ac

    def data_to_plot(self):
        return np.array([wb.temperature for wb in self.water_component])

    @classmethod
    def from_world_map(cls, filename: str, t_stop):
        """

        Earth circumference = 40 075 000 m
        If we have 40 pixels, each pixel is a square of 40 075 000 / 40
        :param t_stop: stop time for the simulation
        :param filename: name of the image from which to take pixels
        :return:
        """
        im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        thresh = 127
        im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
        shape = im_bw.shape
        
        cube_side_length = Earth.circumference / len(im_bw)
        wc = WaterComponent.empty_component(shape, t_stop)
        sc = SoilComponent.empty_component(shape, t_stop)
        for index, pixel in np.ndenumerate(im_bw):
            index_single = np.ravel_multi_index(index, shape)
            if pixel == 255:  # White -> Water
                wc.add(CubeOfWater(index_single, mass=CubeOfWater.material_density * cube_side_length ** 3,
                                   temperature=300, volume=cube_side_length ** 3), index_single)
                sc.add(None, index_single)
            elif pixel == 0:  # Black -> Earth
                sc.add(CubeOfSoil(index_single, mass=CubeOfSoil.material_density * cube_side_length ** 3,
                                  temperature=300, volume=cube_side_length ** 3), index_single)
                wc.add(None, index_single)

        for index, pixel in np.ndenumerate(im_bw):
            index_single = np.ravel_multi_index(index, shape)
            cube = wc[index_single] if wc[index_single] is not None else sc[index_single]
            for n in neighbors_multi(index, shape):
                neighbor_single = np.ravel_multi_index(n, shape)
                neighbor = wc[neighbor_single] if wc[neighbor_single] is not None else sc[neighbor_single]
                cube.add_neighbor(neighbor)
                neighbor.add_neighbor(cube)
        return cls(shape, t_stop, wc=wc, sc=sc)

    def tick(self):
        self.water_component.tick()
        # self.soil_component.tick()
        # self.air_component.tick()
        self.one_tick_passed()

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

    def save_as_image(self, filename, dimension):
        if dimension == "basic":  # Saves black for Earth and White for Water for 2d view
            pixels = []
            for i in range(self.shape[0]):
                row = []
                for j in range(self.shape[1]):
                    flat_index = np.ravel_multi_index((i, j), self.shape)
                    row.append(255 if self.water_component[flat_index] is not None else 0)
                pixels.append(row)
            cv2.imwrite(filename, np.array(pixels))




if __name__ == '__main__':
    np.seterr('raise')
    terre = Earth(shape=(25, 25, 25), t_stop=300)

    terre.animate()

    terre = Earth.from_world_map("InputOutput/Inputs/Map48by40.png", 100)
    terre.save_as_image(filename="InputOutput/Outputs/Map48by40.png", dimension="basic")
