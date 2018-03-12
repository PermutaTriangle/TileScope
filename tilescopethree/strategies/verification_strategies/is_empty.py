
def is_empty_strategy(tiling, **kwargs):
    """The is empty verification strategy.

    A tiling is empty if during initialition of the object contradictory
    obstructions and requirements are detected.
    """
    if tiling.is_empty():
        return True
    for reqlist in tiling.requirements:
        assert not all(any(ob in req for ob in tiling.obstructions)
                       for req in reqlist)
    return False
