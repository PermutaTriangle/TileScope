from base64 import b64decode, b64encode

from grids_three import Tiling, Obstruction, Requirement
from grids_three.db_conf import update_database, check_database

from permuta import Perm
from permuta.permutils import (antidiagonal_set, complement_set, inverse_set,
                               rotate_90_clockwise_set,
                               rotate_180_clockwise_set,
                               rotate_270_clockwise_set)
import tqdm


def twist_one_by_ones(tiling):
    """
    Returns all tilings which can reached by twisting a single cell.
    """
    if tiling.requirements:
        raise NotImplementedError("Can't handle requirements")
    one_by_ones = set(tiling.active_cells)
    for ob in tiling.obstructions:
        if not one_by_ones:
            break
        if not ob.is_single_cell():
            for c in ob.pos:
                one_by_ones.discard(c)

    sym_sets = [antidiagonal_set, complement_set, inverse_set,
                rotate_90_clockwise_set, rotate_180_clockwise_set,
                rotate_270_clockwise_set]
    cell_basis = tiling.cell_basis()
    twists = set()
    for cell in one_by_ones:
        av, _ = cell_basis[cell]
        for sym_set in sym_sets:
            sym_av = sym_set(av)
            twisted_obs = ([ob for ob in tiling.obstructions
                            if cell not in ob.pos] +
                           [Obstruction.single_cell(p, cell) for p in sym_av])
            twists.add(Tiling(twisted_obs))
    return set(twists)


seen = set()


def get_twists(db, update=True):
    twists = set()
    for tiling in tqdm.tqdm(list(db)):
        if tiling.requirements:
            raise NotImplementedError("Can't handle requirements")
        if tiling in seen:
            continue
        new_twists = twist_one_by_ones(tiling)

        if update:
            info = check_database(tiling)
            for twist in new_twists:
                try:
                    update_database(twist, info.get('min_poly'),
                                    info.get('genf'), None)
                except ValueError as e:
                    print("initial:")
                    print(tiling)
                    print("twisted:")
                    print(twist)
                    raise e
        twists |= new_twists
        seen.add(tiling)
    return twists

til_syms = [Tiling.reverse, Tiling.complement, Tiling.inverse,
            Tiling.antidiagonal, Tiling.rotate270, Tiling.rotate180,
            Tiling.rotate90]


def get_symmetry(db):
    sym_database = set()
    for tiling in tqdm.tqdm(db):
        sym_database.add(tiling)
        for sym in til_syms:
            sym_database.add(sym(tiling))
    return sym_database

if __name__ == "__main__":
    import sys
    old_db = sys.argv[1]

    print("Reading database")

    database = set()
    f = open(old_db, 'r')
    for line in f:
        compression = b64decode(line.encode())
        tiling = Tiling.decompress(compression)
        database.add(tiling)
    f.close()

    print("Computing symmetries")

    database = get_symmetry(database)

    print("Writing symmetry databse")

    with_sym = old_db.split('.')[0] + "_symmetry.txt"
    f = open(with_sym, 'w')
    for tiling in tqdm.tqdm(database):
        compression = b64encode(tiling.compress()).decode()
        f.write(compression + "\n")
    f.close()

    print("Computing twists")

    # sym_database = frozenset(database)

    curr_db = None
    i = 0
    while curr_db != database:
        i += 1
        print("iteration {}".format(i))
        curr_db = set(database)
        database |= get_twists(database, update=True)
        # database = get_symmetry(database)
    print(len(database))

    # print("Deleting twists")
    # from pymongo import MongoClient
    # mongo = MongoClient('mongodb://localhost:27017/permsdb_three')
    # print("Removing twists")
    # for twist in tqdm.tqdm(database):
    #     if twist in sym_database:
    #         continue
    #     mongo.permsdb_three.min_poly.delete_one({'key': twist.compress()})

    print("Writing twisted database")

    with_twists = old_db.split('.')[0] + "_twisted.txt"
    f = open(with_twists, 'w')
    for tiling in tqdm.tqdm(database):
        compression = b64encode(tiling.compress()).decode()
        f.write(compression + "\n")
    f.close()

    print("Done")
