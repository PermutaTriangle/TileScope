from comb_spec_searcher import InferralRule
from permuta import Perm
from tilings import Obstruction, Tiling
from tilings.algorithms import EmptyCellInferral, SubobstructionInferral


def empty_cell_inferral(tiling, **kwargs):
    """The empty cell inferral strategy.

    The strategy considers each active but non-positive cell and inserts a
    point requirement. If the resulting tiling is empty, then a point
    obstruction can be added into the cell, i.e. the cell is empty."""
    eci = EmptyCellInferral(tiling)
    return eci.rule()


def subobstruction_inferral(tiling, **kwargs):
    """Return tiling created by adding all subobstructions which can be
    added."""
    soi = SubobstructionInferral(tiling)
    return soi.rule()
