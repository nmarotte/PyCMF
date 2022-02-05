from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from universe import Universe


class BaseModel:
    universe: "Universe" = None
    running: bool = False
    t: int = 0

    # @abstractmethod
    # def update(self):
    #     return

    def tick(self):
        self.t += 1

    def start_simulation(self):
        self.running = True
        self.__update_loop()

    def pause_updating(self):
        self.running = False

    def resume_updating(self):
        self.running = True
        self.__update_loop()

    def stop_updating(self):
        self.running = False

    def __update_loop(self):
        while True:
            if not self.running:
                break
            print(f"Simulating t={self.t}")
            self.update()
        print("done")
