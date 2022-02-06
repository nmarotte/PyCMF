from typing import final, TYPE_CHECKING, Callable, Any


def on_tick_wrapper(cls: type["TickingModel"]):
    """
    Returns a function that takes a function in parameters (this is usually called a decorator)
    :param cls: the class that contains a list attribute called `on_tick_methods` to which
    the method called will be appended to when a new method is added to the class.
    This can be either at the class definition with the `def` keyword followed by a class method.
    Or dynamically when adding a setting an attribute of the class to a function (with at least 1 parameters to catch the `self`)
    :return: the decorator
    """
    def _(clb: callable) -> callable:
        """
        Appends the method to a specific list that is a CLASS attribute (static) of the class given to the outside function
        :param clb: the callable, a.k.a. the stuff that appears after the `def` in the class. Either function or classmethod
        :return: the callable given in parameter so the function can be properly called
        """
        cls.on_tick_methods.append(clb)
        return clb

    return _


class TickableModelMeta(type):
    def __new__(mcs, name, bases, dct: dict[str, Any]):
        x = super().__new__(mcs, name, bases, dct)
        # Ignore the warning, it is due to the fact that super().__new__ returns a basic type
        # and not a type of the class (type["BaseModel"] in this case)
        x.on_tick = on_tick_wrapper(x)
        return x


class TickingModel(metaclass=TickableModelMeta):
    __t: int = 0
    on_tick_methods: list[Callable] = []
    on_tick: Callable[[callable], callable]

    def __init__(self):
        self.__running = False
        self.pause_updating = self.stop_updating
        self.resume_updating = self.start_simulation

    @final
    def update(self, *, update_globally=False):
        """
        The update function that is called when the model wants to move forward in time
        :param update_globally: if True, will use the update method on all the models at once, globally ticking the simulation
        Else, it will only tick the on_tick method of the model updating
        :return:
        """
        for method in self.on_tick_methods:
            if update_globally or method.__module__ == self.__module__:
                method(self)
        TickingModel.__t += 1

    @final
    def __update_loop(self):
        while True:
            if not self.__running:
                break
            print(f"Simulating t={self.__t}")
            self.update()
        print("done")

    @staticmethod
    @final
    def get_time():
        return TickingModel.__t

    @final
    def is_running(self):
        return self.__running

    @final
    def start_simulation(self):
        self.__running = True
        self.__update_loop()

    @final
    def stop_updating(self):
        self.__running = False



