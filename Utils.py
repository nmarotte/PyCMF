import numpy as np


def neighbors(index_single: int, shape: tuple):
    if len(shape) not in [3]:
        raise NotImplemented
    index_multi = np.unravel_index(index_single, shape)
    for dim in range(len(shape)):
        if index_multi[dim] > 0:
            yield np.ravel_multi_index([im - 1 if i == dim else im for i, im in enumerate(index_multi)], shape)
