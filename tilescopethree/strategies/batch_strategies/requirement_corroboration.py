"""
    Module containing the requirement corroboration strategy.
"""
from comb_spec_searcher import Strategy
from grids_three import Obstruction, Tiling


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
            yield Strategy(
                formal_step="",
                objects=[
                    Tiling(obstructions=tiling.obstructions,
                           requirements=tiling.requirements + ((req,),)),
                    Tiling(obstructions=tiling.obstructions + (
                        Obstruction(req.patt, req.pos),),
                           requirements=tiling.requirements)],
                workable=[True, True])
