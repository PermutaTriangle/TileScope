"""The fusion strategy."""
from collections import defaultdict
from comb_spec_searcher import Strategy
from grids_three import Tiling


def fusion(tiling, **kwargs):
    """Yield rules found by fusing rows and columns of a tiling."""
    for row_index in range(tiling.dimensions[1] - 1):
        if fusable(tiling, row_index, True):
            yield Strategy(("Fuse rows {} and {}|{}|."
                            "").format(row_index, row_index + 1, row_index),
                           [fuse_tiling(tiling, row_index, True)],
                           inferable=[True], workable=[True], 
                           possibly_empty=[False], constructor='other')
    for col_index in range(tiling.dimensions[0] - 1):
        if fusable(tiling, col_index, False):
            yield Strategy(("Fuse columns {} and {}|{}|."
                            "").format(col_index, col_index + 1, col_index),
                           [fuse_tiling(tiling, col_index, False)],
                           inferable=[True], workable=[True], 
                           possibly_empty=[False], constructor='other')

def fusable(tiling, row_index, row):
    """Return True if rows 'row_index' and 'row_index + 1' can be fused."""
    return (can_fuse_set_of_gridded_perms(tiling.obstructions, row_index, row)
            and all(can_fuse_set_of_gridded_perms(req_list, row_index, row)
                    for req_list in tiling.requirements))


def can_fuse_set_of_gridded_perms(gridded_perms, row_index, row):
    """Return True if rows 'row_index' and 'row_index + 1' can be fused,
    maintaining the containment of the set of gridded permutations."""
    fuse_counter = defaultdict(int)
    for gp in gridded_perms:
        fuse_counter[fuse_gridded_perm(gp, row_index, row)] += 1
    for gp, count in fuse_counter.items():
        if row:
            row_count = sum(1 for c in gp.pos if c[1] == row_index)
        else:
            row_count = sum(1 for c in gp.pos if c[0] == row_index)
        if row_count + 1 != count:
            return False
    return True


def fuse_tiling(tiling, row_index, row=True, **kwargs):
    """
    Return the tiling where rows 'row_index' and 'row_index + 1' are fused.

    If row=False, then it does the same for columns.
    """
    fused_obstructions = [fuse_gridded_perm(ob, row_index, row)
                          for ob in tiling.obstructions]
    fused_requirements = [[fuse_gridded_perm(req, row_index, row)
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


def fuse_gridded_perm(gp, row_index, row=True):
    """Fuses rows 'row_index' and 'row_index + 1'."""
    fused_pos = []
    for cell in gp.pos:
        x, y = cell
        if row and y > row_index:
            y -= 1
        elif not row and x > row_index:
            x -= 1
        fused_pos.append((x, y))
    return  gp.__class__(gp.patt, fused_pos)
