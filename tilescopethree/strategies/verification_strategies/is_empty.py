from comb_spec_searcher import VerificationStrategy


def is_empty_strategy(tiling, **kwargs):
    """The is empty verification strategy."""
    if tiling.is_empty():
        return VerificationStrategy("Tiling is empty!")
