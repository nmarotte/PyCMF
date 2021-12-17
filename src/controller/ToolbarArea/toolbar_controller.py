from controller.ToolbarArea.subcontrollers.SelectComponent.controller import SelectComponentController
from controller.ToolbarArea.subcontrollers.simulation_time_controller import SimulationTimeController


class ToolbarController:
    def __init__(self):
        self.select_component_controller = SelectComponentController()
        self.simulation_time_controller = SimulationTimeController()
