"""The fusion strategy."""
from itertools import chain

from comb_spec_searcher import Rule
from tilings.algorithms import Fusion


def general_fusion_iterator(tiling, fusion_class):
    """
    Generator over rules found by fusing rows or columns of `tiling` using
    the fusion defined by `fusion_class`.
    """
    assert issubclass(fusion_class, Fusion)
    ncol = tiling.dimensions[0]
    nrow = tiling.dimensions[1]
    possible_fusion = chain(
        (fusion_class(tiling, row_idx=r) for r in range(nrow-1)),
        (fusion_class(tiling, col_idx=c) for c in range(ncol-1))
    )
    return (fusion.rule() for fusion in possible_fusion if fusion.fusable())


def fusion(tiling, **kwargs):
    """Generator over rules found by fusing rows or columns of `tiling`."""
    return general_fusion_iterator(tiling, fusion_class=Fusion)
