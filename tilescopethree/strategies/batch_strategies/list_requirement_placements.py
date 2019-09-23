from itertools import product

from comb_spec_searcher import BatchRule
from permuta.misc import DIR_EAST, DIR_NORTH, DIR_SOUTH, DIR_WEST
from tilings.algorithms import RequirementPlacement


def requirement_list_placement(tiling, **kwargs):
    """Places all requirements on the tiling in every direction."""
    req_placement = RequirementPlacement(tiling)
    directions = (DIR_EAST, DIR_NORTH, DIR_SOUTH, DIR_WEST)
    for req, direction in product(tiling.requirements, directions):
        yield BatchRule(req_placement.place_point_of_req_list(req, direction),
                        "Inserting {} point of requirement list ({})".format(
                            req_placement._direction_string(direction),
                            ", ".join(str(r) for r in req)))

def row_placements(tiling, **kwargs):
    yield from RequirementPlacement(tiling).all_row_placement_rules()

def col_placements(tiling, **kwargs):
    yield from RequirementPlacement(tiling).all_col_placement_rules()

def row_and_col_placements(tiling, **kwargs):
    req_placements = RequirementPlacement(tiling)
    yield from req_placements.all_row_placement_rules()
    yield from req_placements.all_col_placement_rules()

def partial_row_placements(tiling, **kwargs):
    req_placements = (RequirementPlacement(tiling, own_row=False),
                      RequirementPlacement(tiling, own_col=False))
    for req_placement in req_placements:
        yield from req_placement.all_row_placement_rules()

def partial_col_placements(tiling, **kwargs):
    req_placements = (RequirementPlacement(tiling, own_row=False),
                      RequirementPlacement(tiling, own_col=False))
    for req_placement in req_placements:
        yield from req_placement.all_col_placement_rules()

def partial_row_and_col_placements(tiling, **kwargs):
    req_placements = (RequirementPlacement(tiling, own_row=False),
                      RequirementPlacement(tiling, own_col=False))
    for req_placement in req_placements:
        yield from req_placement.all_row_placement_rules()
        yield from req_placement.all_col_placement_rules()

