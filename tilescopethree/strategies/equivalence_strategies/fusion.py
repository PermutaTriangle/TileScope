"""The fusion strategy."""
from itertools import chain

from comb_spec_searcher import Rule
from tilings.algorithms import Fusion


class FusionRuleFactory(Fusion):
    def formal_step(self):
        """
        Return the formal step of the fusion.
        """
        fusing = 'rows' if self._fuse_row else 'columns'
        idx = self._row_idx if self._fuse_row else self._col_idx
        return "Fuse {} {} and {}.".format(fusing, idx, idx+1)

    def rule(self):
        """
        Return a tilescope rule for the fusion.
        """
        return Rule(formal_step=self.formal_step(),
                    comb_classes=[self.fused_tiling()],
                    inferable=[True],
                    workable=[True],
                    possibly_empty=[False],
                    constructor='other')


def general_fusion_iterator(tiling, fusion_class):
    """
    Generator over rules found by fusing rows or columns of `tiling` using
    the fusion defined by `fusion_class`.
    """
    assert issubclass(fusion_class, FusionRuleFactory)
    ncol = tiling.dimensions[0]
    nrow = tiling.dimensions[1]
    possible_fusion = chain(
        (fusion_class(tiling, row_idx=r) for r in range(nrow-1)),
        (fusion_class(tiling, col_idx=c) for c in range(ncol-1))
    )
    return (fusion.rule() for fusion in possible_fusion if fusion.fusable())


def fusion(tiling, **kwargs):
    """Generator over rules found by fusing rows or columns of `tiling`."""
    return general_fusion_iterator(tiling, fusion_class=FusionRuleFactory)
