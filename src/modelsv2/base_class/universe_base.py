from modelsv2.base_model import BaseModel
from modelsv2.tickable_model import TickableModel


class UniverseBase(BaseModel):
    def __new__(cls, *args, **kwargs):
        if BaseModel.universe is None:
            BaseModel.universe = super(UniverseBase, cls).__new__(cls, *args, **kwargs)
        return BaseModel.universe
