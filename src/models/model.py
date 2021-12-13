from abc import abstractmethod


class Model:
    running: bool = False
    t: int = 0

    @abstractmethod
    def update(self):
        return

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
