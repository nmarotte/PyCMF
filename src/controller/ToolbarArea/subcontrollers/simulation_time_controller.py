from typing import TYPE_CHECKING

from views.Widgets.simulation_time_widget import SimulationTimeWidget

if TYPE_CHECKING:
    from controller.main_controller import MainController
    from controller.ToolbarArea.toolbar_area_controller import ToolbarController


class SimulationTimeController:
    def __init__(self, parent_controller: "ToolbarController", main_controller: "MainController"):
        self.parent_controller = parent_controller
        self.main_controller = main_controller
        self.view = SimulationTimeWidget(controller=self)

    def build_pressed(self):
        self.view.build_button.setText("Rebuild Simulation")
        self.view.start_button.setEnabled(True)
        return self.main_controller.build_pressed()

    def start_pressed(self):
        self.view.start_button.hide()
        self.view.layout().replaceWidget(self.view.start_button, self.view.stop_button)
        self.view.stop_button.show()
        self.view.pause_simulation.setEnabled(True)
        return self.main_controller.start_pressed()

    def pause_pressed(self):
        self.view.layout().replaceWidget(self.view.pause_simulation, self.view.resume_simulation)
        self.view.resume_simulation.show()
        self.view.pause_simulation.hide()
        return self.main_controller.pause_pressed()

    def resume_pressed(self):
        self.view.layout().replaceWidget(self.view.resume_simulation, self.view.pause_simulation)
        self.view.resume_simulation.hide()
        self.view.pause_simulation.show()
        return self.main_controller.resume_pressed()

    def stop_pressed(self):
        self.view.stop_button.hide()
        self.view.layout().replaceWidget(self.view.stop_button, self.view.start_button)
        self.view.start_button.show()
        self.view.pause_simulation.setEnabled(False)
        # If resume is still in layout, replace it with pause
        if self.view.pause_simulation.isHidden():
            self.view.layout().replaceWidget(self.view.resume_simulation, self.view.pause_simulation)
            self.view.resume_simulation.hide()
            self.view.pause_simulation.show()

        # Change build button back to "Build" and disable Start
        self.view.build_button.setText("Build Simulation")
        self.view.start_button.setEnabled(False)

        return self.main_controller.stop_pressed()
