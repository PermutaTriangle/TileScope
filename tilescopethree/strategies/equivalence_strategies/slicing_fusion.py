"""The slicing fusion strategy."""
from itertools import chain, product

from comb_spec_searcher import Rule
from tilings import Tiling
from permuta import Av, Perm

def slicing_fusion(tiling, power_level=1, **kwargs):
    """Yield rules found by slicing fusing rows and columns of a tiling."""
    sf_class = {1: SlicingFusion,
                2: SlicingFusionLevel2,
                3: SlicingFusionLevel3}[power_level]
    if tiling.requirements:
        return []
    ncol = tiling.dimensions[1]
    nrow = tiling.dimensions[0]
    possible_fusion = chain(
        (sf_class(tiling, True, r, c) for r, c in
         product(range(nrow - 1), range(ncol))),
        (sf_class(tiling, False, r, c) for r, c in
         product(range(nrow), range(ncol - 1))),
    )
    return (fusion.rule() for fusion in possible_fusion if fusion.fusable())


def is_monotone_cell(tiling, cell):
    """ Check if a cell is non-empty and increasing or decreasing """
    local_obstruction = tiling.cell_basis()[cell][0]
    return (any(ob in [Perm((0, 1)), Perm((1, 0))] for ob in local_obstruction)
            and not is_empty_cell(tiling, cell))


def is_empty_cell(tiling, cell):
    """ Check if the cell is empty in the tiling """
    return cell in tiling.empty_cells


class Fusion(object):
    """
    Fusion algorithm container class.

    Check if a fusion is valid and compute the fusion.

    If `row_idx` is provided it attempts to fuse row `row_idx` with row
    `row_idx+1`.

    If incited `col_ids` is provided it attempts to fuse column `col_idx` with column
    `col_idx+1`.
    """

    def __init__(self, tiling, row_idx=None, col_idx=None):
        self._tiling = tiling
        if row_idx is None and col_idx is not None:
            self._col_idx = col_idx
            self._fuse_row = False
        elif col_idx is None and row_idx is not None:
            self._row_idx = row_idx
            self._fuse_row = True
        else:
            raise RuntimeError('Cannot specify a row and a columns')

    def _fuse_gridded_perm(self, gp):
        """
        Fuse the gridded permutation `gp`.
        """
        fused_pos = []
        for x, y in gp.pos:
            if self._fuse_row and y > self._row_idx:
                y -= 1
            elif not self._fuse_row and x > self._col_idx:
                x -= 1
            fused_pos.append((x, y))
        return  gp.__class__(gp.patt, fused_pos)

    def _unfuse_gridded_perm(self, gp):
        """ Generator of all the possible ways to unfuse a gridded permutations. """
        stretch_above = (lambda p: p if p[1] < self._row_idx else (p[0], p[1]+1))
        stretch_left = (lambda p: p if p[0] < self._col_idx else (p[0]+1, p[1]))
        if self._fuse_row:
            stretch = stretch_above
            editable_pos_idx = [i for i, p in enumerate(gp.pos) if p[1] == self._row_idx]
            editable_pos_idx.sort(key=lambda i: gp.patt[i])
        else:
            stretch = stretch_left
            editable_pos_idx = [i for i, p in enumerate(gp.pos) if p[0] == self._col_idx]
            editable_pos_idx.sort()
        pos = list(map(stretch, gp.pos))
        yield gp.__class__(gp.patt, pos)
        row_shift = int(self._fuse_row)
        col_shift = 1 - int(self._fuse_row)
        for i in editable_pos_idx:
            pos[i] = (pos[i][0] - col_shift, pos[i][1] - row_shift)
            yield gp.__class__(gp.patt, pos)



    def _fuse_counter(self, gridded_perms):
        """
        Count the multiplicities of a set of gridded permutations after the fusion.

        Return a dictionary of gridded permutations with their multiplicities.
        """
        fuse_counter = dict()
        for gp in gridded_perms:
            fused_perm = self._fuse_gridded_perm(gp)
            fuse_counter[fused_perm] = fuse_counter.get(fused_perm, 0) + 1
        return fuse_counter

    @property
    def obstruction_fuse_counter(self):
        """
        Dictionary of multiplicities of fused obstructions.
        """
        if hasattr(self, '_obstruction_fuse_counter'):
            return self._obstruction_fuse_counter
        fuse_counter = self._fuse_counter(self._tiling.obstructions)
        self._obstruction_fuse_counter = fuse_counter
        return self._obstruction_fuse_counter

    @property
    def requirements_fuse_counters(self):
        """
        List of fuse counters for each of the requirements list of the tiling.
        """
        if hasattr(self, '_requirements_fuse_counters'):
            return self._requirements_fuse_counters
        counters = [self._fuse_counter(req_list) for req_list in
                    self._tiling.requirements]
        self._requirements_fuse_counters = counters
        return self._requirements_fuse_counters

    def _can_fuse_set_of_gridded_perms(self, fuse_counter):
        """
        Check if a set of gridded permutations can be fused.
        """
        return all(self._is_valid_count(count, gp) for gp, count in
            fuse_counter.items())

    def _is_valid_count(self, count, gp):
        """
        Check if the fuse count `count` for a given gridded permutation `gp` is
        valid.
        """
        return (self._point_in_fuse_region(gp) + 1 == count)

    def _point_in_fuse_region(self, fused_gp):
        """
        Return the number of point of the gridded permutation `fused_gp` in the
        fused row or column.
        """
        if self._fuse_row:
            return sum(1 for cell in fused_gp.pos if cell[1] == self._row_idx)
        else:
            return sum(1 for cell in fused_gp.pos if cell[0] == self._col_idx)

    def fusable(self):
        """
        Check if the fusion is possible.
        """
        return (self._can_fuse_set_of_gridded_perms(self.obstruction_fuse_counter) and
                all(self._can_fuse_set_of_gridded_perms(self.requirements_fuse_counters)))

    def fusion(self):
        """
        Return the fused tiling.
        """
        return Tiling(
            obstructions = self.obstruction_fuse_counter.keys(),
            requirements = map(dict.keys, self.requirements_fuse_counters),
        )

    def description(self):
        """
        Return a description of the fusion.
        """
        if self._fuse_row:
            return f"Fuse rows {self._row_idx} and {self._row_idx+1}|{self._row_idx}|."
        else:
            return f"Fuse columns {self._col_idx} and {self._col_idx+1}|{self._col_idx}|."

    def rule(self):
        """
        Return a rule for the slicing fusion.
        """
        return Rule(formal_step=self.description(),
                    comb_classes=[self.fusion()],
                    inferable=[True],
                    workable=[True],
                    possibly_empty=[False],
                    constructor='other')


class SlicingFusion(Fusion):
    """
    Slicing fusion algorithm container class.

    Check if a slicing fusion is valid and compute the fused tiling.

    If `fuse_row` is `True` it attempts to fuse row `row_idx` with row
    `row_idx+1` with a special cell in column `col_idx`

    If `fuse_row` is `False` it attempts to fuse column `col_idx` with column
    `col_idx+1` with a special cell in row `row_idx`

    NOTE:

    - `self._special_cell is set in `self._pre_check()`
    """

    def __init__(self, tiling, fuse_row, row_idx, col_idx):
        self._tiling = tiling
        self._row_idx = row_idx
        self._col_idx = col_idx
        self._fuse_row = fuse_row

    def _satisfy_special_cell_condition(self, cell):
        """
        Check that the cell satisfy the condition to be a special cell
        """
        return is_empty_cell(self._tiling, cell)

    def _satisfy_special_cell_partener_condition(self, cell):
        """
        Check that the cell satisfy the condition to me the cell fused with
        the special cell.
        """
        return is_monotone_cell(self._tiling, cell)

    def _is_special_pair(self, special_cell, fused_cell):
        """
        Check if `special_cell` can be the special cell of the fusion and be
        fused with the fused cell
        """
        return (self._satisfy_special_cell_condition(special_cell) and
                self._satisfy_special_cell_partener_condition(fused_cell))

    def _pre_check(self):
        """
        Make a preliminary check before testing if the actual fusion is
        possible.

        Check if a special cell can be selected with the specified row and
        column. If possible, it sets the attribute `special_cell` of `self`.
        """
        if self._fuse_row:
            cells = [(self._col_idx, self._row_idx),
                     (self._col_idx, self._row_idx + 1)]
        else:
            cells = [(self._col_idx, self._row_idx),
                     (self._col_idx + 1, self._row_idx)]
        if self._is_special_pair(cells[0], cells[1]):
            self._special_cell = cells[0]
            return True
        elif self._is_special_pair(cells[1], cells[0]):
            self._special_cell = cells[1]
            return True
        else:
            return False

    @property
    def special_cell(self):
        if hasattr(self, '_special_cell'):
            pass
        elif not self._pre_check():
            raise RuntimeError('Pre-check failed. No slicing fusion possible and no '
                        'special cell')
        return self._special_cell

    def _is_localized_in_special_cell(self, gp):
        """
        Check if a permutation is localized in the special cell.
        """
        return all(self.special_cell == cell for cell in gp.pos)

    @property
    def obstruction_fuse_counter(self):
        """
        Dictionary of multiplicities of fused obstructions.

        Only the good obstructions (i.e. the ones that are not localized in the
        special cell) are fused.
        """
        if hasattr(self, '_obstruction_fuse_counter'):
            return self._obstruction_fuse_counter
        good_obs = (ob for ob in self._tiling.obstructions
                    if not self._is_localized_in_special_cell(ob))
        fuse_counter = self._fuse_counter(good_obs)
        self._obstruction_fuse_counter = fuse_counter
        return self._obstruction_fuse_counter

    def _is_valid_count(self, count, gp):
        """
        Check if the fuse count `count` for a given gridded permutation `gp` is
        valid.
        """
        return (self._point_in_fuse_region(gp) + 1 ==
                count + self._num_addable_gp(gp))

    def _num_addable_gp(self, gp):
        """
        Return the number of gridded permutations that fuse to `gp` and
        that have at least a point in the special cell
        """
        fused_special_cell = (self._col_idx, self._row_idx)
        if self._fuse_row:
            special_cell_in_top_fusion_row = (self.special_cell[1] ==
                                              self._row_idx + 1)
            values_in_cell = [val for val, cell in zip(gp.patt, gp.pos)
                              if cell == fused_special_cell]
            values_in_row = [val for val, cell in zip(gp.patt, gp.pos)
                             if cell[1] == self._row_idx]
            if special_cell_in_top_fusion_row:
                return sum(1 for v in values_in_row if v <=
                                max(values_in_cell, default=-1))
            else:
                return sum(1 for v in values_in_row if v >=
                                min(values_in_cell, default=len(gp)))
        else:
            special_cell_in_right_fusion_row = (self.special_cell[0] ==
                                                self._col_idx + 1)
            indices_in_cell = [idx for idx, cell in zip(range(len(gp)), gp.pos)
                              if cell == fused_special_cell]
            indices_in_col = [idx for idx, cell in zip(range(len(gp)), gp.pos)
                             if cell[0] == self._col_idx]
            if special_cell_in_right_fusion_row:
                return sum(1 for i in indices_in_col if i <=
                                max(indices_in_cell, default=-1))
            else:
                return sum(1 for i in indices_in_col if i >=
                                min(indices_in_cell, default=len(gp)))

    def fusable(self):
        """
        Check if the fusion is possible.
        """
        if self._tiling.requirements:
            raise NotImplementedError('Does not handle requirements at the '
                                      'moment')
        if not self._pre_check():
            return False
        if self._can_fuse_set_of_gridded_perms(self.obstruction_fuse_counter):
            return True

    def description(self):
        """
        Return a description of the fusion.
        """
        description = ""
        if self._fuse_row:
            description += f"Slice fuse rows {self._row_idx} and {self._row_idx+1}."
        else:
            description += f"Slice fuse columns {self._col_idx} and {self._col_idx+1}."
        description += f" The special cell is {self.special_cell}."
        return description


class SlicingFusionLevel2(SlicingFusion):

    def _satisfy_special_cell_partener_condition(self, cell):
        """
        Check that the cell satisfy the condition to me the cell fused with
        the special cell.
        """
        return True

    def description(self):
        return super().description() + 'Power level 2'


class SlicingFusionLevel3(SlicingFusion):

    def description(self):
        return super().description() + 'Power level 3'

    def _is_special_pair(self, special_cell, fused_cell):
        special_basis = self._tiling.cell_basis()[special_cell][0]
        other_basis = self._tiling.cell_basis()[fused_cell][0]
        return all(p not in Av(special_basis) for p in other_basis)
