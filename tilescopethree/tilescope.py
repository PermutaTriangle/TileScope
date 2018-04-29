"""
,--,--'.                          ,--,--'.
`- | . |  ,-. ,-. ,-. ,-. ,-. ,-. `- |   |-. ,-. ,-. ,-.
 , | | |  |-' `-. |   | | | | |-'  , |   | | |   |-' |-'
 `-' ' `' `-' `-' `-' `-' |-' `-'  `-'   ' ' '   `-' `-'
                          |
                          '
"""
from comb_spec_searcher import CombinatorialSpecificationSearcher
from comb_spec_searcher.objectqueue import ObjectQueue
from grids_three import Obstruction, Tiling
from permuta import Perm
from permuta.descriptors import Basis
from tilescopethree.strategies import is_empty_strategy


class TileScopeTHREE(CombinatorialSpecificationSearcher):
    """
    An instance of TileScope is used to build up knowledge about tilings with
    respect to the given basis.
    """
    def __init__(self,
                 basis=None,
                 strategy_pack=None,
                 symmetry=False,
                 forward_equivalence=False,
                 compress=True,
                 objectqueue=ObjectQueue,
                 start_tiling=None,
                 logger_kwargs={'processname': 'runner'}):
        """Initialise TileScope."""
        if basis is None and start_tiling is None:
            raise ValueError(("Tilescope requires either a start tiling or a "
                              "basis."))
        if basis is not None and start_tiling is not None:
            raise ValueError(("Tilescope takes either a basis or a "
                              "start_tiling, not both."))

        if basis is not None:
            if isinstance(basis, str):
                self.basis = Basis([Perm.to_standard([int(c) for c in p])
                                    for p in basis.split('_')])
            else:
                self.basis = Basis(basis)
            start_tiling = Tiling(
                obstructions=[Obstruction.single_cell(patt, (0, 0))
                              for patt in self.basis])
        else:
            self.basis = []

        if symmetry or strategy_pack.symmetry:
            symmetries = [Tiling.inverse, Tiling.reverse, Tiling.complement,
                          Tiling.antidiagonal, Tiling.rotate90,
                          Tiling.rotate180, Tiling.rotate270]
            symmetries = [sym for sym in symmetries
                          if sym(start_tiling) == start_tiling]
        else:
            symmetries = []

        function_kwargs = {"basis": self.basis}

        CombinatorialSpecificationSearcher.__init__(
            self,
            start_object=start_tiling,
            strategy_pack=strategy_pack,
            symmetry=symmetries,
            compress=compress,
            forward_equivalence=forward_equivalence,
            objectqueue=objectqueue,
            is_empty_strategy=is_empty_strategy,
            function_kwargs=function_kwargs,
            logger_kwargs=logger_kwargs)
