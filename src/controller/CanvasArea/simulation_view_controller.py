class SimulationViewController:
    def __init__(self):
        self.title_controller = title_controller
        self.canvas_controller = canvas_controller
        self.text_edit_controller = text_edit_controller

    def clear_canvas(self):
        self.canvas_controller.clear_canvas()