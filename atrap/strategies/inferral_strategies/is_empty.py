from atrap.tools import basis_partitioning
from grids import PositiveClass, Tiling
from .inferral_class import InferralStrategy

def is_empty(tiling, basis):
    verification_length = tiling.total_points + len(basis[-1])
    verification_length += sum(1 for _, block in tiling.non_points if isinstance(block, PositiveClass))
    empty = True
    for length in range(verification_length + 1):
        _, avoiding_perms = basis_partitioning(tiling, length, basis)
        if avoiding_perms:
            empty = False
            break
    if empty:
        yield InferralStrategy("This tiling contains no avoiding perms", Tiling({}))
