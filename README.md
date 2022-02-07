# UndCliMo
UNDerstandable CLI MOdel (UCM for short)

This module requires tqdm for showing the advancement of the computation, as well as matplotlib for plotting the simulation and imageio for creating a gif

TODO structure of the models 3 types:

- base_class (earth_base, grid_chunk_base, etc ...) and inheriting from BaseModel : Contains the basic structural/pythonic stuff for the class (correct inheritance, redefinition of dunder methods, etc ...)
- physical_class (earth, grid_chunk, etc ...) and inheriting from its base_class : Contains the physical properties and method for that class (temperature, mass, etc ...)
- ticking_class (ticking_earth, ticking_universe, etc ...) and inheriting from its physical_class as well as TickableModel : Interface to store all the class methods that have to be executed at each time step of the simulation via the `@TickableModel.on_tick` decorator



Required Libraries : 
unittest for testing
PyQt5 for the graphical interface
numpy for the models
