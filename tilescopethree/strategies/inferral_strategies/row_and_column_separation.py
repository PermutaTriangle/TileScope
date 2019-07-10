"""An inferral function that tries to separate cells in rows and columns."""
from collections import defaultdict
from comb_spec_searcher import InferralStrategy
from tilings import Tiling


def row_and_column_inequalities_of_tiling(tiling):
    """Computes the inequalities based on length 2 obstructions.

    A cell (x_0, y_0) is 'less' than (x_1, y_1) in the column order if x_0 =
    x_1 and there exists an obstruction (Perm((0, 1)), [(x_1, y_1), (x_0,
    y_0)]). The function returns a tuple of dictionaries, one for the rows and
    one for the columns. Each key in the dictionaries is a row(column) with
    dictionaries as values, where the keys are the cells and values are the set
    of cells which the cell is 'less' than in the respective ordering.
    """
    smaller_than_row = defaultdict(dict)
    smaller_than_col = defaultdict(dict)
    for ob in tiling.obstructions:
        if len(ob) == 2:
            if ob.is_single_cell():
                continue
            c1, c2 = ob.pos
            # If the two points are in the same column
            if c1[0] == c2[0]:
                col = c1[0]
                if col not in smaller_than_col:
                    smaller_than_col[col] = {
                        cell: set() for cell in tiling.cells_in_col(col)}
                # whether the obstruction is 01 or 10, c2 < c1
                smaller_than_col[col][c2].add(c1)
            # If the two points are in the same row
            elif c1[1] == c2[1]:
                row = c1[1]
                if row not in smaller_than_row:
                    smaller_than_row[row] = {
                        cell: set() for cell in tiling.cells_in_row(row)}
                if ob.patt[0] == 0:
                    # the obstruction is 01, so c2 < c1 (further up)
                    smaller_than_row[row][c2].add(c1)
                else:
                    # the obstruction is 10, so c1 < c2 (further down)
                    smaller_than_row[row][c1].add(c2)
        elif len(ob) > 2:
            # obstructions are ordered by length
            break
    return smaller_than_row, smaller_than_col


def separations(inequalities, unprocessed_cells=None,
                current_cell=None, current_state=None):
    """
    A recursive function for generating the splittings of a row/column from the
    given inequalities.

    It will split the cells from the row/column into parts. Any two cells in
    the same part must be on the the same row/column as one another. A part to
    the left of another must be below/further to the left than the other. For
    example in the tiling given by (0,0):Av(132), (1,1): Point, (2,0) Av(132)
    the separations of the first row will look like [ [(2,0)] [(0,0)]] ] and
    [ [(0,0), (2,0)] ]. The second is the trivial solution and is always
    returned.
    """
    if current_state is None:
        current_state = []
    if unprocessed_cells is None:
        unprocessed_cells = list(inequalities.keys())
    if current_cell is None:
        current_cell = unprocessed_cells[0]
        unprocessed_cells = unprocessed_cells[1:]

    if current_state == []:
        # The next state must be the one with exactly one part
        current_state.append([current_cell])
        if unprocessed_cells:
            # we then take the next cell to pass to the recursive call
            next_cell = unprocessed_cells[0]
            return [separation
                    for separation in separations(inequalities,
                                                  unprocessed_cells[1:],
                                                  next_cell,
                                                  current_state)]
        return [current_state]

    must_mix_with = [cell for cell in inequalities.keys()
                     if (cell not in inequalities[current_cell] and
                         current_cell not in inequalities[cell] and
                         cell is not current_cell)]

    mixing_with_one = False
    for index, part in enumerate(current_state):
        if any(cell in part for cell in must_mix_with):
            if mixing_with_one:
                # The cell has to mix with two necessarily separate parts,
                # hence no solution
                return []
            mixing_with_one = True
            # The cell must mix with this part
            mixing_with_index = index

    if mixing_with_one:
        for index, part in enumerate(current_state):
            if index < mixing_with_index:
                if any(current_cell not in inequalities[cell]
                       for cell in part):
                    # There is some element in the part to the left which can't
                    # appear below the current cell
                    return []
            elif index > mixing_with_index:
                if any(cell not in inequalities[current_cell]
                       for cell in part):
                    # There is some element in the part to the right which
                    # can't appear above the current cell
                    return []
        current_state[mixing_with_index].append(current_cell)
        if unprocessed_cells:
            next_cell = unprocessed_cells[0]
            return [separation
                    for separation in separations(inequalities,
                                                  unprocessed_cells[1:],
                                                  next_cell, current_state)]

        return [current_state]

    # The cell didn't mix with a part
    furthest_left_index = 0
    furthest_right_index = len(current_state)
    # We search for the interval where the current cell can be placed
    for index, part in enumerate(current_state):
        if any(cell not in inequalities[current_cell] for cell in part):
            # The current cell may not appear to the left of this part
            furthest_left_index = index + 1

    for index, part in reversed(list(enumerate(current_state))):
        if any(current_cell not in inequalities[cell] for cell in part):
            # The current cell may not appear to the right of this part
            furthest_right_index = index

    if furthest_left_index > furthest_right_index:
        # in which case the interval is empty
        if furthest_left_index == furthest_right_index + 1:
            # Must mix with part with furthest_right_index
            current_state[furthest_right_index].append(current_cell)
            if unprocessed_cells:
                next_cell = unprocessed_cells[0]
                return [
                    separation
                    for separation in separations(inequalities,
                                                  unprocessed_cells[1:],
                                                  next_cell, current_state)]
            return [current_state]
        return []

    # We now need to create the potential states, for example, consider the
    # "fake" current state [ [] [] [] [] [] [] [] ] then given the interval
    # [1,3] then where you see an "x" the current cell can be placed
    # [ [x] x [x] x [x] x [x] [] [] [] ]

    potential_states = []

    if furthest_left_index > 0:
        potential_state = (current_state[:furthest_left_index-1] +
                           [current_state[furthest_left_index - 1] +
                           [current_cell]] +
                           current_state[furthest_left_index:])
        potential_states.append(potential_state)

    for index in range(furthest_left_index, furthest_right_index + 1):
        if index == len(current_state):
            potential_state = current_state + [[current_cell]]
            potential_states.append(potential_state)

        else:
            potential_state = (current_state[:index] + [current_state[index] +
                               [current_cell]] + current_state[index+1:])
            potential_states.append(potential_state)

            potential_state = (current_state[:index] + [[current_cell]] +
                               current_state[index:])
            potential_states.append(potential_state)

    if unprocessed_cells:
        next_cell = unprocessed_cells[0]
        final_states = []
        for potential_state in potential_states:
            # for each potential state, we call recursively
            final_states.extend(
                separation for separation in separations(inequalities,
                                                         unprocessed_cells[1:],
                                                         next_cell,
                                                         potential_state))
        return final_states

    return potential_states


def row_and_column_separation(tiling, **kwargs):
    # First we calculate the set of inequalities for all the rows and columns
    row_ineqs, col_ineqs = row_and_column_inequalities_of_tiling(tiling)

    separated_rows, separated_cols = [], []
    # When creating the new tiling, we need to keep track of the shifted cell
    # we add, in case a cell appears on a separated row and column
    inferred = False
    row_map = {}
    shift = 0
    for row in range(tiling.dimensions[1]):
        inequalities = row_ineqs[row]
        if inequalities:
            # Calculate the separation, described in the function
            row_separations = sorted(separations(inequalities),
                                     key=lambda x: (len(x), x))
            separation = row_separations[-1]
            inferred = True if len(row_separations) != 1 else inferred
        else:
            separation = [[c for c in tiling.cells_in_row(row)]]

        for index, cells in enumerate(separation):
            for cell in cells:
                row_map[cell] = cell[1] + shift + index
        shift += len(separation) - 1
        if len(separation) > 1:
            separated_rows.append(row)

    col_map = {}
    shift = 0
    for col in range(tiling.dimensions[0]):
        # Calculate the separation, described in the function
        inequalities = col_ineqs[col]
        if inequalities:
            # sort them by length, i.e. number of parts in the separation
            column_separations = sorted(separations(inequalities),
                                        key=lambda x: (len(x), x))
            separation = column_separations[-1]
            inferred = True if len(column_separations) != 1 else inferred
        else:
            separation = [[c for c in tiling.cells_in_col(col)]]

        for index, cells in enumerate(separation):
            for cell in cells:
                col_map[cell] = cell[0] + shift + index
        shift += len(separation) - 1
        if len(separation) > 1:
            separated_cols.append(col)

    if inferred:
        def cell_map(c):
            return (col_map[c], row_map[c])

        obstructions = [ob.minimize(cell_map) for ob in tiling.obstructions
                        if not ob.is_point_perm() and
                        not ob.minimize(cell_map).contradictory()]
        requirements = [[req.minimize(cell_map) for req in reqs]
                        for reqs in tiling.requirements]

        separated_tiling = Tiling(obstructions=obstructions,
                                  requirements=requirements)
        # we only return it if it is different
        formal_step = "Separated rows [{}] and columns [{}]".format(
            ", ".join(map(str, separated_rows)),
            ", ".join(map(str, separated_cols)))
        if kwargs.get('regions', False):
            fwd_map = separated_tiling.forward_map
            return ([separated_tiling],
                    [{c: set([fwd_map[cell_map(c)]])
                      for c in tiling.active_cells
                      if (cell_map(c) in fwd_map and
                          fwd_map[cell_map(c)] in
                          separated_tiling.active_cells)}])
        return InferralStrategy(formal_step, separated_tiling)
