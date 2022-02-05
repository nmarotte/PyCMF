from typing import final, TYPE_CHECKING, Callable, Any

if TYPE_CHECKING:
    from modelsv2.universe import Universe


def on_tick_wrapper(cls: type["BaseModel"]):
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


class BaseModelMeta(type):
    def __new__(mcs, name, bases, dct: dict[str, Any]):
        x = super().__new__(mcs, name, bases, dct)
        # Ignore the warning, it is due to the fact that super().__new__ returns a basic type
        # and not a type of the class (type["BaseModel"] in this case)
        x.on_tick = on_tick_wrapper(x)
        return x


class BaseModel(metaclass=BaseModelMeta):
    on_tick_methods: list[Callable] = []
    on_tick: Callable[[callable], callable]
    universe: "Universe" = None

    @final
    def update(self):
        """
        The update function that is called when the model wants to move forward in time
        :return:
        """
        for method in self.on_tick_methods:
            method(self)
