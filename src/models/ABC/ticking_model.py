from typing import final, Callable, Any


def on_tick_builder(cls: type["TickingModel"]):
    """
    Returns a function that takes a function in parameters (this is usually called a decorator)
    :param cls: the class that contains a list attribute called `on_tick_methods` to which
    the method called will be appended to when a new method is added to the class.
    This can be either at the class definition with the `def` keyword followed by a class method.
    Or dynamically when adding a setting an attribute of the class to a function (with at least 1 parameters to catch the `self`)
    :return: the decorator
    """

    def decorator_factory(enabled: bool = True):
        """
        Allows for the decorator to take parameters
        :param enabled: if the on_tick method should be used on update
        :return:
        """

        def on_tick_decorator(func: callable) -> callable:
            """
            Appends the method to a specific list that is a CLASS attribute (static) of the class given to the outside function
            :param func: the callable, a.k.a. the stuff that appears after the `def` in the class. Either function or class method
            :return: the callable given in parameter so the function can be properly called
            """
            func.enabled = enabled
            cls.on_tick_methods.append(func)
            return func

        return on_tick_decorator

    return decorator_factory


class TickableModelMeta(type):
    def __new__(mcs, name, bases, dct: dict[str, Any]):
        x = super().__new__(mcs, name, bases, dct)
        # Ignore the warning, it is due to the fact that super().__new__ returns a basic type
        # and not a type of the class (type["BaseModel"] in this case)
        x.on_tick = on_tick_builder(x)
        return x


class TickingModel(metaclass=TickableModelMeta):
    on_tick_methods: list[Callable] = []
    on_tick: Callable[[callable], callable]

    def __init__(self):
        self._t = 0
        self.__running = False

    def update(self):
        """
        The update function that is called when the model wants to move forward in time
        Else, it will only tick the on_tick method of the model updating
        :return:
        """
        for method in self.on_tick_methods:
            if method.enabled and method.__module__ == self.__module__:
                method(self)
        self._t += 1

    @final
    def get_time(self):
        return self._t

    @final
    def is_running(self):
        return self.__running
