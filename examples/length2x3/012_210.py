import atrap
from permuta import *

input_set = PermSet.avoiding([Perm((0,1,2)), Perm((2,1,0))])

#recipes = [atrap.recipes.all_row_and_column_insertions]
recipes = [atrap.recipes.all_cell_insertions]
bakery = atrap.bakery_naive.Bakery(input_set, recipes)

#bakery = atrap.bakery_naive.Bakery(input_set)

print("Finding proof for:\n")
print(input_set)
print()
print(bakery)

while True:
    good = bakery.bake()
    if good:
        bakery.give_me_proof()
        break
