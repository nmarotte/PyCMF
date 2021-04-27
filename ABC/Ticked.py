from abc import abstractmethod
from abc import ABC



class Ticked(ABC):
    def __init__(self, t_stop: int, t_start: int = 0):
        self.t = t_start
        self.max_t = t_stop

    def one_tick_passed(self):
        self. t += 1

    @abstractmethod
    def tick(self):
        """
        What happens at every tick
        :return:
        """