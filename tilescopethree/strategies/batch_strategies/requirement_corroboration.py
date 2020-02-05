"""
    Module containing the requirement corroboration strategy.
"""
from typing import Iterable

from comb_spec_searcher import Rule
from tilings import Tiling
from tilings.algorithms import RequirementCorroboration


def requirement_corroboration(tiling: Tiling, ignore_parent: bool = True,
                              **kwargs) -> Iterable[Rule]:
    """
    The requirement corroboration strategy.

    The requirement corroboration strategy is a batch strategy that considers
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
    yield from RequirementCorroboration(tiling).rules(ignore_parent)
