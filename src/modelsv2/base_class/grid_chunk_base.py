from typing import Optional

from collections.abc import Collection, Iterator

from modelsv2.physical_class.chunk_component import ChunkComponent


class GridChunkBase(list[ChunkComponent]):
    """
    The implementation aspect of the GridChunk
    """
    COMPONENTS = "WATER", "AIR", "LAND"
    water_component: ChunkComponent = None
    air_component: ChunkComponent = None
    land_component: ChunkComponent = None

    def reindex(self):
        """
        Search the parent class for this object in it and set the index variable accordingly
        :return:
        """
        self.index = self.parent.index(self)

    def __init__(self, components: Collection[ChunkComponent], *, index: int = None, parent=None):
        super().__init__()
        self.parent = parent
        self.index = index
        if self.index is None and self.parent is not None and self in self.parent:
            # No index provided but parent provided ? Find the object in the parent
            self.reindex()
        self.neighbours = self.parent.neighbours(self.index) if self.parent else None

        # Add only the components that are not empty
        for i, component in enumerate(components):
            if not component.is_empty():
                # Link the component's reference to the chunk to self
                component.chunk = self
                # Link the water/air/land _component object variable to the component of the corresponding type
                self[component.type.upper()] = component

    def __len__(self) -> int:
        """
        :return: the size of the grid chunk, that is equal to the amount of different components it contain
        """
        return sum(self[x] is not None for x in GridChunkBase.COMPONENTS)

    def __iter__(self) -> Iterator[ChunkComponent]:
        return (self[x] for x in GridChunkBase.COMPONENTS if self[x] is not None)

    def __contains__(self, __x: object) -> bool:
        if isinstance(__x, ChunkComponent):
            return any(__x == self[x] for x in GridChunkBase.COMPONENTS if self[x] is not None)
        return super().__contains__(__x)

    def __setitem__(self, key: str, value: Optional[ChunkComponent]):
        if key.upper() not in GridChunkBase.COMPONENTS:
            raise NotImplementedError(f"Component {key} is not a valid component type")
        self.__setattr__(f"{key.lower()}_component", value)

    def __getitem__(self, item: str):
        if item.upper() not in GridChunkBase.COMPONENTS:
            raise NotImplementedError(f"Component {item} is not a valid component type")
        return self.__getattribute__(f"{item.lower()}_component")

    def __eq__(self, other: object):
        return isinstance(other, GridChunkBase) and all(self[x] == other[x] for x in GridChunkBase.COMPONENTS)

    def __ne__(self, other: "GridChunkBase"):
        return not self.__eq__(other)
