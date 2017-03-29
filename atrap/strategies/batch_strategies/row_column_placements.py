from grids import Tiling, Block, PositiveClass

from .batch_class import BatchStrategy


def all_row_placements(tiling, **kwargs):
    for row in range(tiling.dimensions.j):
        if len(tiling.get_row(row)) < 2:
            continue

        if any( not (block is Block.point or isinstance(block, PositiveClass)) for _, block in tiling.get_row(row) ):
            # Row inelegible as some block is not a point.
            continue

        if any( sum(1 for _, col_block in tiling.get_col(cell.i)
               if isinstance(col_block, PositiveClass)
               or col_block is Block.point) != 1 for cell, _ in tiling.get_row(row) ):
            # Row ineligible because there is a cell that is not
            # the sole non-class cell in its respective col
            continue

        bottommost_tiling_dicts = [ {} for _ in tiling.get_row(row) ]
        topmost_tiling_dicts = [ {} for _ in tiling.get_row(row) ]
        for cell, block in tiling:

            for index, value in enumerate(tiling.get_row(row)):
                cell_being_placed, _ = value

                if cell.i == cell_being_placed.i:
                    if cell.j == cell_being_placed.j:
                        # same cell

                        bottommost_tiling_dicts[index][cell] = Block.point
                        topmost_tiling_dicts[index][cell] = Block.point

                        if isinstance(block, PositiveClass):
                            perm_class = block.perm_class
                            bottommost_tiling_dicts[index][(cell.i - 0.5, cell.j + 0.5)] = perm_class
                            bottommost_tiling_dicts[index][(cell.i + 0.5, cell.j + 0.5)] = perm_class
                            topmost_tiling_dicts[index][(cell.i + 0.5, cell.j - 0.5)] = perm_class
                            topmost_tiling_dicts[index][(cell.i - 0.5, cell.j - 0.5)] = perm_class
                    else:
                        # same column, different row
                        bottommost_tiling_dicts[index][(cell.i + 0.5, cell.j)] = block
                        bottommost_tiling_dicts[index][(cell.i - 0.5, cell.j)] = block
                        topmost_tiling_dicts[index][(cell.i + 0.5, cell.j)] = block
                        topmost_tiling_dicts[index][(cell.i - 0.5, cell.j)] = block
                elif cell.j == cell_being_placed.j:
                    #same row, different column
                    bottommost_tiling_dicts[index][(cell.i, cell.j + 0.5)] = block
                    topmost_tiling_dicts[index][(cell.i, cell.j - 0.5)] = block
                else:
                    # different row and different column
                    bottommost_tiling_dicts[index][cell] = block
                    topmost_tiling_dicts[index][cell] = block

        bottommost_tilings = [ Tiling(tiling_dict) for tiling_dict in bottommost_tiling_dicts]
        bottommost_formal_step = "Placing the minimum point into row {}".format(row)
        yield BatchStrategy( bottommost_formal_step, bottommost_tilings )

        topmost_tilings = [ Tiling(tiling_dict) for tiling_dict in topmost_tiling_dicts ]
        topmost_formal_step = "Placing the maximum point into row {}".format(row)
        yield BatchStrategy( topmost_formal_step, topmost_tilings )

def all_minimum_row_placements(tiling, basis):
        for row in range(tiling.dimensions.j):
            if len(tiling.get_row(row)) < 2:
                continue

            if any( not (block is Block.point or isinstance(block, PositiveClass)) for _, block in tiling.get_row(row) ):
                # Row inelegible as some block is not a point.
                continue

            if any( sum(1 for _, col_block in tiling.get_col(cell.i)
                   if isinstance(col_block, PositiveClass)
                   or col_block is Block.point) != 1 for cell, _ in tiling.get_row(row) ):
                # Row ineligible because there is a cell that is not
                # the sole non-class cell in its respective col
                continue

            bottommost_tiling_dicts = [ {} for _ in tiling.get_row(row) ]
            for cell, block in tiling:

                for index, value in enumerate(tiling.get_row(row)):
                    cell_being_placed, _ = value

                    if cell.i == cell_being_placed.i:
                        if cell.j == cell_being_placed.j:
                            # same cell

                            bottommost_tiling_dicts[index][cell] = Block.point

                            if isinstance(block, PositiveClass):
                                perm_class = block.perm_class
                                bottommost_tiling_dicts[index][(cell.i - 0.5, cell.j + 0.5)] = perm_class
                                bottommost_tiling_dicts[index][(cell.i + 0.5, cell.j + 0.5)] = perm_class
                        else:
                            # same column, different row
                            bottommost_tiling_dicts[index][(cell.i + 0.5, cell.j)] = block
                            bottommost_tiling_dicts[index][(cell.i - 0.5, cell.j)] = block
                    elif cell.j == cell_being_placed.j:
                        #same row, different column
                        bottommost_tiling_dicts[index][(cell.i, cell.j + 0.5)] = block
                    else:
                        # different row and different column
                        bottommost_tiling_dicts[index][cell] = block

            bottommost_tilings = [ Tiling(tiling_dict) for tiling_dict in bottommost_tiling_dicts]
            bottommost_formal_step = "Placing the minimum point into row {}".format(row)
            yield BatchStrategy( bottommost_formal_step, bottommost_tilings )
