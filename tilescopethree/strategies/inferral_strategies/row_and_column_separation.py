"""An inferral function that tries to separate cells in rows and columns."""

from comb_spec_searcher import InferralRule
from tilings.algorithms import RowColSeparation


def row_and_column_separation(tiling, **kwargs):
    rcs = RowColSeparation(tiling)
    if rcs.separable():
        formal_step = 'Row and column separation'
        separated_tiling = rcs.separated_tiling()
        return InferralRule(formal_step, separated_tiling)
