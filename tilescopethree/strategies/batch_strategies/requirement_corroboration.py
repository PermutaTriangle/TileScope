"""
    Module containing the requirement corroboration strategy.
"""
from comb_spec_searcher import Rule
from tilings import Obstruction, Requirement, Tiling


def requirement_corroboration(tiling, basis, **kwargs):
    """
    The requirement corroboration strategy.

    The requirement corrobation strategy is a batch strategy that considers
    each requirement of each requirement list. For each of these requirements,
    the strategy returns two tilings; one where the requirement has been turned
    into an obstruction and another where the requirement has been singled out
    and a new requirement list added with only the requirement. This new
    requirement list contains only the singled out requirement.

    This implements the notion of partitioning the set of gridded permutations
    into those that satisfy this requirement and those that avoid it. Those
    that avoid the requirement, must therefore satisfy another requirement from
    the same list and hence the requirement list must be of length at least 2.
    """
    for reqs in tiling.requirements:
        if len(reqs) == 1:
            continue
        for req in reqs:
            yield Rule(
                formal_step="Inserting requirement {}.".format(str(req)),
                comb_classes=gp_insertion(tiling, req),
                ignore_parent=True,
                possibly_empty=[True, True],
                workable=[True for _ in range(2)],
                inferable=[True for _ in range(2)],
                constructor='disjoint')

def gp_insertion(tiling, gp, regions=False):
    """Return a list of size 2, where the first tiling avoids the gridded perm
    gp and the second contains gp."""
    tilings = [tiling.add_obstruction(gp.patt, gp.pos),
               tiling.add_requirement(gp.patt, gp.pos)]
    
    if regions:
        forward_maps = [{c: frozenset([c]) for c in tiling.active_cells},
                        {c: frozenset([c]) for c in tiling.active_cells}]
        return tilings, forward_maps
    else:
        return tilings