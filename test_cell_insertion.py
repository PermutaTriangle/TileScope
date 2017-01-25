from atrap import *
from permuta import *


#input_set = Tile.INCREASING
input_set = Tile.DECREASING
#input_set = PermSet.avoiding([Perm((0, 1)), Perm((1, 0))])
#input_set = PermSet.avoiding([Perm((0, 2, 1))])
T = Tiling({(0, 0): input_set})

print("Our tiling:")
print()
print(T)
print()

print("Doing cell insertion first step")

cell_empty, cell_non_empty = cell_insertion_helper(T, (0, 0))

print("Left tiling:")
print()
print(cell_empty)
print()
print("Right preliminary tiling:")
print()
print(cell_non_empty)
print()

print("Doing tiling inferral")

inferred_tile = tiling_inferral(cell_non_empty, input_set)

print("Inferred tile:")

print()
print(inferred_tile)
print()

print("Result of cell_insertion:")
for (_, left), (letter, right) in cell_insertion(T, (0, 0), input_set):
    print()
    print(left)
    print()
    print(letter)
    print()
    print(right)
    print()
    print("Verifying left one")
    if verify_tiling(left, input_set):
        print("Tile is verified")
    else:
        print("Tile is NOT verified")
    print()
    print("Verifying right one")
    if verify_tiling(right, input_set):
        print("Tile is verified")
    else:
        print("Tile is NOT verified")
