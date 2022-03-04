from typing import Optional

from models.physical_class.earth import Earth
from models.physical_class.sun import Sun


class UniverseBase:
    earth: Optional[Earth] = None
    sun: Optional[Sun] = None

    def __iter__(self):
        return (x for x in (self.earth, self.sun))
