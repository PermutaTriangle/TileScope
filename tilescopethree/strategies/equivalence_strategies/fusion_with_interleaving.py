"""The more general fusion strategy. Fuse two rows if actually one row where
you can draw a line somewhere."""
from collections import defaultdict
from comb_spec_searcher import Strategy
from functools import partial, update_wrapper
from itertools import chain
from tilings import Tiling, Obstruction
from permuta import Perm

from tilescopethree.strategies.equivalence_strategies.fusion import Fusion
from tilescopethree.strategies.equivalence_strategies.fusion import general_fusion_iterator


class FusionWithInterleaving(Fusion):

    def __init__(self, tiling, row_idx=None, col_idx=None):
        super().__init__(tiling, row_idx=row_idx, col_idx=col_idx)
        self._bases = tiling.cell_basis()

    def _pre_check(self):
        return not self._tiling.requirements

    def fusable(self, **kwargs):
        """Return true if adjacent rows can be viewed as one row where you draw a
        horizontal line through the permutation."""
        if not self._pre_check():
            return False
        bases = self._bases
        tiling = self._tiling
        row_index = self._row_idx if self._fuse_row else self._col_idx
        row = self._fuse_row
        first_row = (tiling.cells_in_row(row_index)
                     if row else tiling.cells_in_col(row_index))
        # only consider rows of size one
        if len(first_row) > 1:
            return False
        second_row = (tiling.cells_in_row(row_index + 1)
                      if row else tiling.cells_in_col(row_index + 1))
        # adjacent cells in rows must not be empty
        if len(first_row) != len(second_row):
            return False
        first_cell = list(first_row)[0]
        second_cell = list(second_row)[0]
        # ensure the other cell is adjacent
        if ((row and first_cell[0] != second_cell[0]) or
                (not row and first_cell[1] != second_cell[1])):
            return False
        # ensure other cells basis is the same, and not the same as the root basis
        if (bases[first_cell][0] != bases[second_cell][0]):
            return False
        obstructions_to_add = []
        for ob in tiling.obstructions:
            # for each obstruction that occupies the first cell, draw a line
            # through it in every way so that it crosses to the secoond cell
            #TODO: Should we be worried about obstruction going only to the
            #      second cell?
            if ob.occupies(first_cell):
                # ignore the obstructions that imply skew or sum components
                if len(ob) == 2 and ob.occupies(second_cell):
                    continue
                # the point in the first cell
                in_cell = [(idx, val) for idx, val in enumerate(ob.patt)
                           if ob.pos[idx] == first_cell]
                if row:
                    in_cell = sorted(in_cell, key=lambda x: (x[1], x[0]))
                special_cell = second_cell
                # place i points in bottom cell, rest in top.
                for i in range(len(in_cell)):
                    maxdex = [point[0] for point in in_cell[i:]]
                    pos = [special_cell if i in maxdex else c
                        for i, c in enumerate(ob.pos)]
                    obstructions_to_add.append(Obstruction(ob.patt, pos))
            if ob.occupies(second_cell):
                in_cell = [(idx, val) for idx, val in enumerate(ob.patt)
                           if ob.pos[idx] == second_cell]
                if row:
                    in_cell = sorted(in_cell, key=lambda x: -x[1])
                else:
                    in_cell = sorted(in_cell, key=lambda x: -x[0])
                special_cell = first_cell
                # place i points in bottom cell, rest in top.
                for i in range(len(in_cell)):
                    maxdex = [point[0] for point in in_cell[i:]]
                    pos = [special_cell if i in maxdex else c
                        for i, c in enumerate(ob.pos)]
                    obstructions_to_add.append(Obstruction(ob.patt, pos))

        # if the tiling is unchanged, then the previous obstruction imply all those
        #  obstructions that needed to be added, and therefore we can think of this
        #  as one row with a line drawn through it
        if tiling == Tiling(list(tiling.obstructions) + obstructions_to_add,
                                tiling.requirements):
            # return True
            if (Obstruction(Perm((0, 1)),
                            (first_cell, second_cell)) in tiling.obstructions or
                Obstruction(Perm((0, 1)),
                            (second_cell, first_cell)) in tiling.obstructions or
                Obstruction(Perm((1, 0)),
                            (first_cell, second_cell)) in tiling.obstructions or
                Obstruction(Perm((1, 0)),
                            (second_cell, first_cell)) in tiling.obstructions):
                return True

    def fused_tiling(self, **kwargs):
        """
        Return the tiling where rows 'row_index' and 'row_index + 1' are fused.

        If row=False, then it does the same for columns.

        (Note unlike fusion file, we ignore obstruction using the other cell)
        """
        tiling = self._tiling
        row_index = self._row_idx if self._fuse_row else self._col_idx
        row = self._fuse_row
        fused_obstructions = [self._fuse_gridded_perm(ob)
                              for ob in tiling.obstructions
                              if ((row and
                                   all(c[1] != row_index + 1 for c in ob.pos)) or
                                  (not row and
                                   all(c[0] != row_index + 1 for c in ob.pos)))]
        fused_requirements = [[self._fuse_gridded_perm(req)
                               for req in req_list]
                              for req_list in tiling.requirements]
        fused_tiling = Tiling(fused_obstructions, fused_requirements)
        if kwargs.get('regions', False):
            cell_to_region = {}
            for cell in tiling.active_cells:
                x, y = cell
                if row and y > row_index:
                    y -= 1
                elif not row and x > row_index:
                    x -= 1
                cell_to_region[cell] = set([(x, y)])
            return ([fused_tiling], [cell_to_region])
        return fused_tiling

    def formal_step(self):
        """
        Return the formal step of the fusion.
        """
        if self._fuse_row:
            return f"Fuse fancily rows {self._row_idx} and {self._row_idx+1}."
        else:
            return f"Fuse fancily columns {self._col_idx} and {self._col_idx+1}."

def fusion_with_interleaving(tiling, **kwargs):
    """
    Yield rules found by fusing rows and columns of a tiling, where the
    unfused tiling obtained by drawing a line through certain heights/indices
    """
    yield from general_fusion_iterator(tiling,
                                       fusion_class=FusionWithInterleaving)
