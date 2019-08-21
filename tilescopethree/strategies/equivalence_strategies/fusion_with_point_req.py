from functools import partial, update_wrapper

from permuta import Perm
from tilings import Tiling, Requirement

from tilescopethree.strategies.equivalence_strategies.fusion import Fusion
from tilescopethree.strategies.equivalence_strategies.fusion import general_fusion_iterator


class FusionWithPointReq(Fusion):
    """
    Like normal fusion but will still fuse if cells contains point requirements.
    """

    def _is_valid_count(self, count, gp):
        if isinstance(gp, Requirement) and gp.patt == Perm((0,)):
            return True
        return super()._is_valid_count(count, gp)

    @staticmethod
    def _two_point_req(cell):
        """
        Return a requirement list that's equivalent to having two points in the
        cell.
        """
        return [Requirement(Perm((0, 1)), (cell, cell)),
                Requirement(Perm((1, 0)), (cell, cell))]

    def fused_tiling(self):
        """
        Return the fused tiling.
        """
        t = super().fused_tiling()
        bases = self._tiling.cell_basis()
        if self._fuse_row:
            ncol = t.dimensions[0]
            cell_pairs = (((col, self._row_idx), (col, self._row_idx+1))
                     for col in range(ncol))
        else:
            nrow = t.dimensions[1]
            cell_pairs = (((self._col_idx, row), (self._col_idx+1, row))
                     for row in range(nrow))
        for cell1, cell2 in cell_pairs:
            if Perm((0,)) in bases[cell1][1] and Perm((0,)) in bases[cell2][1]:
                new_req = FusionWithPointReq._two_point_req(cell1)
                t = t.add_list_requirement(new_req)
        return t

    def formal_step(self):
        """
        Return the formal step of the fusion.
        """
        return super().formal_step() + ' Ignoring point requirement.'


def fusion_with_point_req(tiling, **kwargs):
    """
    Generator over rules found by fusing rows or columns of `tiling`.
    Point requirements are ignored
    """
    yield from general_fusion_iterator(tiling, fusion_class=FusionWithPointReq)
