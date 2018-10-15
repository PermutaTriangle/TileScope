"""A strategy for checking if a tiling is contained in a subclass."""

from comb_spec_searcher import VerificationStrategy
from itertools import chain
from permuta.descriptors import Basis
from permuta import Av, Perm, PermSet
from permuta.permutils import basis_of_SB
from grids_three import Tiling, Requirement, Obstruction


def subclass_verified(tiling, basis, **kwargs):
    """The subclass verified strategy.

    A tiling is subclass verified if it only generates permutations in a
    proper subclass of Av(basis).
    """
    if tiling.dimensions == (1, 1):
        return None
    else:
        maxlen = kwargs.get('maxpattlen', 4)
        patterns = set(perm for perm in chain(*[Av(basis).of_length(i)
                                                for i in range(maxlen + 1)]))
        maxlen += tiling.maximum_length_of_minimum_gridded_perm()
        for i in range(maxlen + 1):
            for g in tiling.objects_of_length(i):
                perm = g.patt
                patterns = set(pattern for pattern in patterns
                               if perm.avoids(pattern))
                if not patterns:
                    return None
        return VerificationStrategy(formal_step=("The tiling belongs to the "
                                                 "subclass obtained by adding"
                                                 " the patterns {}."
                                                 "".format(Basis(patterns))))


def rie_verified(tiling, basis, **kwargs):
    """X
    """
    if tiling.dimensions == (1, 1) and len(tiling.requirements) == 1 and len(tiling.requirements[0]) == 1:

        only_req = tiling.requirements[0][0].patt

        k = 3
        rie_basis = basis_of_SB(k)
        print('Looking at {}'.format(only_req))

        max_len = len(only_req)+max(len(b) for b in rie_basis)

        # TODO take into account in these two is_ins_enc
        # that all perms on C(T) contain only_req

        # def is_ins_enc(B):
        #     for i in range(2*k+1, max_len+1):
        #         for g in tiling.objects_of_length(i):
        #             perm = g.patt
        #             if perm not in Av(rie_basis):
        #                 return False
        #     return True

        def is_ins_enc(B):
            for basis_patt in rie_basis:
                gp = Requirement(pattern=basis_patt, positions=((0, 0) for _ in range(len(basis_patt))))
                temp = Tiling(tiling.obstructions, ((tiling.requirements[0][0],), (gp,))).merge()
                if temp.obstructions != (Obstruction(Perm(()), ()),):
                    return False
            return True

        if is_ins_enc(rie_basis) or is_ins_enc([p.inverse for p in rie_basis]):
            print(tiling)
            print()
            print('I verified the positive root!')
            print('using the requirement {}'.format(only_req))
            # assert False
            return VerificationStrategy(formal_step=("RIE! {}."
                                                    "".format(max_len)))
    else:
        return None
