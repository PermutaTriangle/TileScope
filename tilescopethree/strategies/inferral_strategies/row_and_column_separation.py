"""An inferral function that tries to separate cells in rows and columns."""

from tilings.algorithms import RowColSeparation


def row_and_column_separation(tiling, **kwargs):
    rcs = RowColSeparation(tiling)
    return rcs.rule()
