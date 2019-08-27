from tilescopethree import TileScopeTHREE
from tilescopethree.strategies.batch_strategies.cell_insertion import \
    all_cell_insertions
from tilescopethree.strategies.equivalence_strategies.fusion_with_interleaving import (
    fusable, fuse_tiling)
from tilescopethree.strategies.equivalence_strategies.point_placements import \
    place_point_of_requirement
from tilescopethree.strategy_packs import point_placements

from permuta import Perm
from permuta.descriptors import Basis
from tilings import Requirement, Tiling

basis = input("Insert basis (in the form 123_132): ")

start_tiling = Tiling.from_string(basis)

basis = Basis([Perm.to_standard(p) for p in basis.split('_')])

tilescope = TileScopeTHREE(start_tiling, point_placements)

options = ("1: insert a point\n"
           "2: place a point\n"
           "3: factors\n"
           "4: fuse\n"
           "5: insert requirement\n"
           "-1: undo last move\n"
           "q: quit")

curr_task = [start_tiling]
old_tasks = []

def infer(tiling):
    """Repeatedly apply inferral strategies until no change."""
    inferred = tiling
    change = False
    for strategy in point_placements.inferral_strats:
        s = strategy(inferred)
        if s is not None:
            new_inferred = s.comb_classes[0]
            if new_inferred != inferred:
                change = True
                inferred = new_inferred
    if not change:
        return inferred
    return infer(inferred)

def insert_point(tiling):
    """Inserts a point into the cell given by the user."""
    if len(tiling.active_cells) == len(tiling.positive_cells):
        print("All cells already positive. Try some other strategy.")
        return None
    if len(tiling.active_cells) == 1:
        cell = (0,0)
    else:
        print("Which cell do you want to insert into?")
        cell = get_coordinate(tiling)
    print("Inserting point into cell {}.".format(cell))
    empty = tiling.insert_cell(cell)
    non_empty = tiling.empty_cell(cell)
    return [empty, non_empty]

def insert_req(tiling):
    """Inserts a req into the cell given by the user."""
    if len(tiling.active_cells) == len(tiling.positive_cells):
        print("All cells already positive. Try some other strategy.")
        return None
    if len(tiling.active_cells) == 1:
        cell = (0,0)
    else:
        print("Which cell do you want to insert into?")
        cell = get_coordinate(tiling)
    print("Inserting req into cell {}.".format(cell))
    r = input("Type the req you want to insert: ")
    patt = Perm.to_standard(r)
    empty = tiling.add_single_cell_obstruction(patt, cell)
    non_empty = tiling.add_single_cell_requirement(patt, cell)
    return [empty, non_empty]

# def place_point(tiling):
#     """Place a point, by asking the user to select a requirement, 
#     a point and a direction."""
#     placeable = [(i, r[0]) for i, r in enumerate(tiling.requirements) 
#                  if len(r) == 1]
#     if not placeable:
#         print("Can only place into length 1 requirements.")
#         return None
#     print("Which point would you like to place?")
#     for i, (_, r) in enumerate(placeable):
#         print("{}: {}".format(i, repr(r)))
    
#     i = -1
#     while i not in range(len(placeable)):
#         try:
#             i = int(input("Insert number: "))
#         except:
#             print("Invalid output, try again")
#             continue
#         if i not in range(len(placeable)):
#             print("Pick a number between 0 and {}.".format(len(placeable) - 1))
#     idx = placeable[i][0]
#     r = placeable[i][1]
#     if len(r) == 1:
#         point_idx = 0
#     else:
#         raise NotImplementedError("Only place points atm.")

#     print("Which direction do you want to place the point?")
#     print("0: rightmost \n1: topmost \n2: leftmost \n3: bottommost")
#     d = int(input("Insert number: "))
#     return [place_point_of_requirement(tiling, idx, point_idx, d)]

def place_point(tiling):
    """Place a point, by asking the user to select a requirement, 
    a point and a direction."""
    placeable = [(i, r[0]) for i, r in enumerate(tiling.requirements) 
                 if len(r) == 1]
    if not placeable:
        print("Can only place into length 1 requirements.")
        return None
    if len(placeable) == 1:
        idx = placeable[0][0]
        r = placeable[0][1]
    else:
        print("Which point would you like to place?")
        for i, (_, r) in enumerate(placeable):
            print("{}: {}".format(i, repr(r)))
        
        i = -1
        while i not in range(len(placeable)):
            try:
                i = int(input("Insert number: "))
            except:
                print("Invalid output, try again")
                continue
            if i not in range(len(placeable)):
                print("Pick a number between 0 and {}.".format(len(placeable) - 1))
        idx = placeable[i][0]
        r = placeable[i][1]
    if len(r) == 1:
        point_idx = 0
    else:
        print("Input the index of the point you want to place")
        point_idx = int(input("Insert number: "))

    print("Which direction do you want to place the point?")
    print("0: rightmost \n1: topmost \n2: leftmost \n3: bottommost")
    d = int(input("Insert number: "))
    return [place_point_of_requirement(tiling, idx, point_idx, d)]

def factors(tiling):
    """Return the factors of a tiling."""
    factor_list = tiling.find_factors()
    if len(factor_list) == 1:
        print("Tiling already fully factored.")
        return None
    return factor_list

def fuse(tiling, basis=basis):
    """Determines rows and columns that can be fuse and ask the user to choose 
    which to fuse"""
    if tiling.requirements:
        print("Can't fuse tilings with requirements.")
        return None
    fusable_rows = []
    fusable_cols = []
    bases = tiling.cell_basis()
    for row_index in range(tiling.dimensions[1] - 1):
        if fusable(tiling, row_index, bases, True, basis=basis):
            fusable_rows.append(row_index)
    for col_index in range(tiling.dimensions[0] - 1):
        if fusable(tiling, col_index, bases, False, basis=basis):
            fusable_cols.append(col_index)
    if fusable_rows and fusable_cols:
        choice = int(input(("You can fuse rows {} and columns {}. Do you want "
                            "to fuse a row or column? Enter 0 for row, or 1 "
                            "for column: ".format(
                                    ", ".join(str(i) for i in fusable_rows), 
                                    ", ".join(str(j) for j in fusable_cols)))))
        if choice:
            fusable_rows = False
        else:
            fusable_cols = False
    if fusable_rows:
        idx = int(input(("You can fuse the rows {}. Insert the row to fuse: "
                         "".format(", ".join(str(i) for i in fusable_rows)))))
    elif fusable_cols:
        idx = int(input(("You can fuse the columns {}. Insert the column to fuse:"
                         " ".format(", ".join(str(i) for i in fusable_cols)))))
    else:
        print("No rows or columns can be fused.")
        return None
    return [fuse_tiling(tiling, idx, bool(fusable_rows))]

def get_coordinate(tiling):
    """Makes the user select a cell in the tiling."""
    x, y = int(input("x-coordinate: ")), int(input("y-coordinate: "))
    if (x, y) not in tiling.active_cells:
        print("Cell ({}, {}) not in tiling, try again.".format(x, y))
        return get_coordinate(tiling)
    return (x, y)

def tiling_print(tiling):
    """Print the grid of a tiling detailing local obstructions plus all the 
    crossing obstructions and requirements."""
    print(tiling)

def print_tilings(tilings):
    for i, t in enumerate(tilings):
        print("{}:".format(i))
        tiling_print(t)
        verified = verify(t)
        if verified is not None:
            print(verified)


def pick_tiling(tilings):
    """Return a tiling chosen from the list chosen by the user."""
    if len(tilings) == 1:
        return tilings[0]
    else:
        try:
            i = int(input("Insert number of tiling to work from next: "))
        except:
            print("invalid input, try again")
            return pick_tiling(tilings)
        if i not in range(len(tilings)):
            print(("{} is not a valid option, pick a number from 0 to {}"
                   "".format(i, len(tilings) - 1)))
            return pick_tiling(tilings)
        return tilings[i]

def verify(tiling):
    """Return a formal step string if tiling is verified, otherwise None."""
    for strat in point_placements.ver_strats:
        s = strat(tiling, basis=basis)
        if s is not None:
            return s.formal_step

    
print("Starting process with tiling: ")
tiling_print(start_tiling)

while True:
    tiling = pick_tiling(curr_task)
    next_step = input(("What would you like to do?\n" + options 
                       + "\nInsert number: "))
    if next_step == "1":
        # insert a point
        tilings = insert_point(tiling)
    elif next_step == "2":
        # place a point
        tilings = place_point(tiling)
    elif next_step == "3":
        tilings = factors(tiling)
    elif next_step == "4":
        tilings = fuse(tiling)
    elif next_step == "5":
        tilings = insert_req(tiling)
    elif next_step == "-1":
        # go to previous step
        if old_tasks:
            tilings = old_tasks.pop()
        print_tilings(tilings)
        continue
    elif next_step == "q":
        # quit
        break
    else:
        print("Invalid input. Enter 'q' to quit.")
        continue

    if tilings is None:
        continue

    # Remove empty tilings
    tilings = [infer(t) for t in tilings if not t.is_empty()]

    print_tilings(tilings)

    old_tasks.append(curr_task)
    curr_task = tilings
