"""The more general fusion strategy. Fuse two rows if actually one row where
you can draw a line somewhere."""
from comb_spec_searcher import Rule
from tilings.algorithms import ComponentFusion

from .fusion import general_fusion_iterator


def fusion_with_interleaving(tiling, **kwargs):
    """
    Yield rules found by fusing rows and columns of a tiling, where the
    unfused tiling obtained by drawing a line through certain heights/indices
    of the row/column.
    """
    if tiling.requirements:
        return
    yield from general_fusion_iterator(tiling, ComponentFusion)
