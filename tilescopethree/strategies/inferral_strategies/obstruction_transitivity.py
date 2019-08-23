from collections import defaultdict

from comb_spec_searcher import InferralRule
from permuta import Perm
from tilings import Obstruction, Tiling


def compute_new_ineqs(pos, ineqs):
    """Computes the transitive relation over positive cells.

    Given a list of inequalities and positive cells, a new set of inequalities
    is computed. For every positive cell c, when g < c < l the relation g < l
    is added if not already there. The new list of inequalities is returned.
    """
    gtlist = defaultdict(list)
    ltlist = defaultdict(list)
    for left, right in ineqs:
        ltlist[left].append(right)
        gtlist[right].append(left)
    stack = list(pos)
    ineqs = set(ineqs)
    newineqs = set()
    while len(stack) > 0:
        cur = stack.pop(0)
        for gt in gtlist[cur]:
            for lt in ltlist[cur]:
                if (gt, lt) not in ineqs:
                    gtlist[lt].append(gt)
                    ltlist[gt].append(lt)
                    ineqs.add((gt, lt))
                    if gt != lt:
                        newineqs.add((gt, lt))
                    if lt not in stack and lt in pos:
                        stack.append(lt)
                    if gt not in stack and gt in pos:
                        stack.append(gt)
    return newineqs


def compute_ineq_ob(left, right):
    """Given an inequality of cells left < right, compute an obstruction."""
    if left[0] == right[0]:
        # same column
        if left[1] < right[1]:
            return Obstruction(Perm((1, 0)), [right, left])
        else:
            return Obstruction(Perm((0, 1)), [right, left])
    elif left[1] == right[1]:
        # same row
        if left[0] < right[0]:
            return Obstruction(Perm((1, 0)), [left, right])
        else:
            return Obstruction(Perm((0, 1)), [right, left])
    else:
        raise ValueError(
            ("Can not construct an obstruction from inequality {} < {}"
             ).format(left, right))


def obstruction_transitivity(tiling, **kwargs):
    """The obstruction transitivity strategy.

    The obstruction transitivity considers all length 2 obstructions with both
    points in the same row or some column. By considering these length 2
    obstructions in similar manner as the row and column separation, as
    inequality relations. When the the obstructions use a positive cell,
    transitivity applies, i.e. if a < b < c and b is positive, then a < c.
    """
    positive_cells_col = defaultdict(list)
    positive_cells_row = defaultdict(list)
    for cell in tiling.positive_cells:
        positive_cells_col[cell[0]].append(cell[1])
        positive_cells_row[cell[1]].append(cell[0])
    colineq = defaultdict(set)
    rowineq = defaultdict(set)
    for ob in tiling.obstructions:
        if len(ob) != 2 or ob.is_localized():
            continue
        leftcol, rightcol = ob.pos[0][0], ob.pos[1][0]
        leftrow, rightrow = ob.pos[0][1], ob.pos[1][1]
        # In same column
        if leftcol == rightcol:
            if ob.patt == Perm((0, 1)):
                colineq[leftcol].add((rightrow, leftrow))
            else:
                colineq[leftcol].add((rightrow, leftrow))
        # In same row
        elif ob.pos[0][1] == ob.pos[1][1]:
            if ob.patt == Perm((0, 1)):
                rowineq[leftrow].add((rightcol, leftcol))
            else:
                rowineq[leftrow].add((leftcol, rightcol))

    newineqs = []
    for col, ineqs in colineq.items():
        for left, right in compute_new_ineqs(positive_cells_col[col], ineqs):
            newineqs.append(((col, left), (col, right)))
    for row, ineqs in rowineq.items():
        for left, right in compute_new_ineqs(positive_cells_row[row], ineqs):
            newineqs.append(((left, row), (right, row)))

    if newineqs:
        return InferralRule(
            "Computing transitivity of inequalities.",
            Tiling(obstructions=(tiling.obstructions + tuple(
                   compute_ineq_ob(left, right) for left, right in newineqs)),
                   requirements=tiling.requirements))
