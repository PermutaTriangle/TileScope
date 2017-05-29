from collections import Iterable
from grids import Tiling


class RecursiveStrategy(object):

    def __init__(self, formal_step, tilings, back_maps):
        if not isinstance(formal_step, str):
            raise TypeError("Formal step not a string")
        if not isinstance(tilings, Iterable):
            raise TypeError("Tilings not iterable")
        if not tilings:
            raise TypeError("There are no tilings, a recursive strategy contains a list with more than one tilings")
        elif len(tilings) == 1:
            raise TypeError("There is one tiling, recursive strategies breaks tilings into multiple tilings.")
        if any(not isinstance(tiling, Tiling) for tiling in tilings):
            raise TypeError("A recursive strategy takes a list of tilings")
        if any(not isinstance(hopefully_dict, dict) for hopefully_dict in back_maps):
            raise TypeError("One of the maps is not a dictionary")

        self.formal_step = formal_step
        self.tilings = [tiling for tiling in tilings]
        self.back_maps = [part_map for part_map in back_maps]
