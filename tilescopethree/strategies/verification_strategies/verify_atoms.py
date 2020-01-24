"""A strategy for checking if a tiling is a point."""
from tilings.algorithms.enumeration import BasicEnumeration


def verify_atoms(tiling, **kwargs):
    """
    Verify the most basics tilings.
    """
    return BasicEnumeration(tiling).verification_rule()
