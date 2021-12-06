from abc import abstractmethod


class StartButtonController:
    @abstractmethod
    def start_pressed(self):
        pass


class PauseButtonController:
    @abstractmethod
    def pause_pressed(self):
        pass


class ResumeButtonController:
    @abstractmethod
    def resume_pressed(self):
        pass


class StopButtonController:
    @abstractmethod
    def stop_pressed(self):
        pass


class ClearButtonController:
    @abstractmethod
    def clear_pressed(self):
        pass
