# UndCliMo

## Introduction
UNDerstandable CLI MOdel (UCM for short) is a framework developped as part of my Master's thesis in Computer Science at the ULB. The framework provides 3 layers of implementation :

- base_class (earth_base, grid_chunk_base, etc ...) and inheriting from BaseModel : Contains the basic structural/pythonic stuff for the class (correct inheritance, redefinition of dunder methods, etc ...)
- physical_class (earth, grid_chunk, etc ...) and inheriting from its base_class : Contains the physical properties and method for that class (temperature, mass, etc ...)
- ticking_class (ticking_earth, ticking_universe, etc ...) and inheriting from its physical_class as well as TickableModel, that is an interface to store all the class methods that have to be executed at each time step of the simulation via the `@TickableModel.on_tick` decorator

The framework is currently **not** able to provide accurate simulations of real-world physical process, but provides a few examples with placeholder simulations such as the averaging of the temperature at each time step

## Running the code
To run the framework, you can edit the script in `main.py` and then execute it with `python3.9 main.py`.

For running the program with the graphical interface, you can use the GUI command line argument and execute `python3.9 main.py GUI`. In that way you will be able to dynamically change the simulation
## Requirements

Required Libraries : 
- unittest for testing
- PyQt5 for the graphical interface
- numpy for the models
