
from permuta import Perm, PermSet
from grids import Tiling, Block, PositiveClass
from .inferral_class import InferralStrategy
from collections import defaultdict
from .jays_subclass_inferral import jays_subclass_inferral

def subclass_inferral(tiling, basis, **kwargs):
    '''Return a new tiling where all non-points have been inferred.
    This is a more primitive approach avoiding using the basis
    partitioning function'''
    tiling = Tiling()

    total_points = tiling.total_points
    total_points += sum(1 for _, block in tiling.non_points if isinstance(block, PositiveClass))

    '''This will be the inferred tiling that is returned'''
    inferred_tiling_dict = { cell: block for cell, block in tiling.point_cells }
    '''We will add a perm to this tiling, to determine if it is forbidden in a cell'''
    point_tiling_dict = { cell: block for cell, block in tiling if isinstance(block, PositiveClass) or block is Block.point }

    for cell, block in tiling.non_points:
        '''For all non point cells, we want to try and add to the original basis'''
        original_basis = list(block.basis)
        for length in range(len(original_basis[-1])):
            '''The maximum length of pattern that can be added is the size of the last'''
            inferral_length = total_points + length
            for patt in PermSet.avoiding(original_basis).of_length(length):
                '''For each potential pattern, to add it to the basis, we need that it
                always creates a bad permutation with all the points'''
                point_tiling_dict[cell] = PermSet([patt])
                if any( perm.avoids(*basis) for perm in Tiling(point_tiling_dict)):
                    continue
                original_basis.append(patt)
        point_tiling_dict.pop(cell)
        '''We updated the inferred_tiling'''
        inferred_tiling_dict[cell] = PermSet.avoiding(original_basis)


    inferred_tiling = Tiling(inferred_tiling_dict)

    # assert inferred_tiling == old_subclass_inferral(tiling, basis)
    if not tiling == inferred_tiling:

        yield InferralStrategy("After tiling subset inferral", inferred_tiling)


#
#
#
#
# def old_subclass_inferral(tiling, basis):
#     """Return a new tiling where all non-points have been inferred."""
#
#     # The containing/avoiding perms_of_cells dictionary
#     perms_of_cells_dicts = (defaultdict(set), defaultdict(set))
#
#     # We only need to check permutations up to this length because any longer
#     # perm can be reduced to a perm of this length and still contain the patt
#     # if it already did
#     verification_length = tiling.total_points + len(basis[-1])
#     verification_length += sum(1 for _, block in tiling.non_points if isinstance(block, PositiveClass))
#
#     for length in range(verification_length + 1):
#         # Get the partitioning into containing/avoiding perms
#         partitions = basis_partitioning(tiling, length, basis)
#
#         # For containing and avoiding
#         for partition, perms_of_cells in zip(partitions, perms_of_cells_dicts):
#             # For each perm and its associated info
#             for cell_infos in partition.values():
#                 # Store for each cell its contribution to the perm
#                 #print(partition)
#                 #print(perms_of_cells)
#                 #print(cell_infos)
#                 for cell_info in cell_infos:
#                     for cell, info in cell_info.items():
#                         cell_perm, _, _ = info
#                         perms_of_cells[cell].add(cell_perm)
#
#     # Now we have for all cells, the ways they contributed perms to perm
#     containing_perms_of_cells, avoiding_perms_of_cells = perms_of_cells_dicts
#
#     # Keep all the points, no need to infer on them
#     tiling_dict = {cell: Block.point for cell in tiling.point_cells}
#
#     # However, for all non-points
#     for cell, block in tiling.non_points:
#         # If an element exclusively contributes to containing perms,
#         # we add this element to the basis
#         # print(cell, containing_perms_of_cells[cell], avoiding_perms_of_cells[cell])
#         new_basis_elements = containing_perms_of_cells[cell] \
#                            - avoiding_perms_of_cells[cell]
#
#         #print(cell, block)
#         #print()
#         #print(containing_perms_of_cells[cell])
#         #print()
#         #print(avoiding_perms_of_cells[cell])
#         #print()
#         #print(new_basis_elements)
#         #print()
#         # If basis contains the point, the block will consist
#         # solely of the empty perm, so no need to add to the new tiling
#         if Perm((0,)) in new_basis_elements:
#             continue
#
#         # Add the new basis elements to the old basis elements
#         new_basis = new_basis_elements.union(block.basis)
#         #print(new_basis)
#         #print()
#         #print()
#         #print()
#         #print()
#
#         # Create the new block for the new tiling
#         new_block = PermSet.avoiding(new_basis)
#         if isinstance(block, PositiveClass):
#             # Positive classes remain positive
#             new_block = PositiveClass(new_block)
#
#         # Put the block into the cell of the new tiling
#         tiling_dict[cell] = new_block
#     new_tiling = Tiling(tiling_dict)
#     return new_tiling
#     # if not tiling == new_tiling:
#     #     return InferralStrategy("After tiling subset inferral", new_tiling)
