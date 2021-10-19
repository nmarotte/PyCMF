from __future__ import annotations
from abc import ABC


class Neighbored(ABC):
    def __init__(self, index: int):
        self.index: int = index
        self.neighbors = []

    def add_neighbor(self, neighbor: Neighbored):
        self.neighbors.append(neighbor)

    def is_neighbor_of(self, index):
        return index in self.neighbors
