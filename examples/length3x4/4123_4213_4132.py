import time
import atrap
from permuta import *

# Some tree we once drew on the board by hand and found recursion involving
# components. Atrap can do it with a single component

task = '4123_4213_4132'
patts = [ Perm([ int(c)-1 for c in p ]) for p in task.split('_') ]
input_set = PermSet.avoiding(patts)

# recipes = [atrap.recipes.all_row_and_column_insertions]
recipes = [atrap.recipes.all_cell_insertions]
# recipes = [atrap.recipes.all_cell_insertions, atrap.recipes.all_row_and_column_insertions]
bakery = atrap.patisserie.Bakery(input_set, recipes)

#def print(*args, **kwargs):
#    pass


print("Finding proof for:\n")
print(input_set)
print()

start_time = time.time()

while True:
    #print("Size of frontier:", len(bakery.frontier))
    good = bakery.bake(verbose=True)
    if good:
        break

tree = bakery.get_proof_tree()

print()
print("Finding the proof tree took", int(time.time() - start_time), "seconds")
print()
print("Human readable:")
print()

tree.pretty_print()

print()
print("Computer readable (JSON):")
print()
print(tree.to_json(indent="    ", sort_keys=True))
