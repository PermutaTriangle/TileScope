from comb_spec_searcher import *
from grids_three import *
from permuta import *
from tilescopethree import *
from tilescopethree.strategy_packs import point_placements_db
import sys
from queue import Queue
import json
from tilescopethree.strategies import one_by_one_verification

pack = point_placements_db
pack.ver_strats = [one_by_one_verification]

if len(sys.argv) > 1:
    inp = sys.argv[1]
else:
    inp = input("Enter filename: ")

try:
    with open(inp, 'r') as f:
        tree_json = f.readline().strip()
    tree = ProofTree.from_json(Tiling, tree_json)
except FileNotFoundError:
    t = TileScopeTHREE(inp, pack)
    tree = t.auto_search(verbose=True,status_update=30)

queue = Queue()

funcs = dict()


def prog_header():
    return ("from collections import defaultdict\n"
            # "from pymongo import MongoClient\n\n"
            # "mongo = MongoClient('mongodb://localhost:27017/permsdb_three')\n"
            "mem = defaultdict(dict)\n\n"
            "import sys\n"
            "sys.setrecursionlimit(10**6)\n"
            "from sympy import Poly, abc, sympify, var\n"
            "from grids_three.db_conf import taylor_expand\n"
            "from grids_three import Tiling, Obstruction, Requirement\n"
            "from permuta import Perm\n"
            "genfs = dict()\n\n")


def get_func(pnode):
    return str(pnode.get_function())[:-3]


def func_header(func):
    return "def {}(n):".format(func)


def mem_lookup(func):
    return ("if n in mem['{}']:\n"
            "\treturn mem['{}'][n]\n").format(func, func)


def db_lookup(pnode):
    '''    return ("info = mongo.permsdb_three.factordb.find_one({{'key': "
            "{}}})\n"
            "error = None\n"
            "if info is None:\n"
            "\terror = 'Tiling not in database. '\n"
            "elif 'coeffs' not in info:\n"
            "\terror = 'Coefficients not in database. '\n"
            "elif len(info['coeffs']) <= n:\n"
            "\terror = 'Coefficients only go up to {{}}.'"
            ".format(len(info['coeffs'])-1)\n"
            "else:\n"
            "\tans = info['coeffs'][n+1]\n"
            "if error:\n"
            "\traise ValueError(error)\n").format(
                                pnode.eqv_path_objects[0].compress())
    '''
    return ("if '{}' in genfs:\n"
            "\tans = taylor_expand(genfs['{}'],n=n)[-1]\n"
            "else:\n"
            "\tgenf = None\n"
            "\tgenf = {}.get_genf()\n"
            "\tans = taylor_expand(genf, n=n)[-1]\n"
            "\tgenfs['{}'] = genf\n"
            ).format(get_func(pnode), get_func(pnode),
                     repr(pnode.eqv_path_objects[-1]),
                     get_func(pnode))


def base_case(pnode):
    return ("if n < 0:\n"
            "\treturn 0\n")


def mem_save(func):
    return "mem['{}'][n] = ans\n".format(func)


def get_rec(pnode):
    func = get_func(pnode)

    body = mem_lookup(func)
    body += base_case(pnode)

    if pnode.disjoint_union:
        body += ("ans = " +
                 " + ".join([get_func(child)+"(n)"
                            for child in pnode.children])+"\n")
        for child in pnode.children:
            queue.put(child)
    elif pnode.decomposition:
        '''if get_func(pnode) == 'F_54030':
            print(pnode.eqv_path_objects[-1])
            for child in pnode.children:
                print(child.eqv_path_objects[0])'''
        points = 0
        pos_children = 0
        children = []
        for child in pnode.children:
            if child.eqv_path_objects[-1].is_point_tiling():
                points += 1
            else:
                if child.eqv_path_objects[-1].requirements:
                    pos_children += 1
                children.append(child)
        ind = "i"  # index variable
        rem = "n+1"
        body += "ans = 0\n"
        for i, child in enumerate(children[:-1]):
            if child.eqv_path_objects[-1].requirements:
                start = 1
                pos_children -= 1
            else:
                start = 0
            tabs = '\t'*i
            body += "{}for {} in range({},{}-{}):\n".format(tabs, ind, start, rem,
                                                                points+pos_children)
            rem += "-{}".format(ind)
            ind = chr(ord(ind)+1)

        ind = "i"
        if points == 0:
            rem = "n"
        else:
            rem = "n-{}".format(points)
        tabs = '\t'*(len(children)-1)
        if tabs:
            body += "{}ans += ".format(tabs)
        for child in children[:-1]:
            body += "{}({}) * ".format(get_func(child), ind)
            rem += "-{}".format(ind)
            ind = chr(ord(ind)+1)

        if len(children) == 1:
            body += "ans = {}({})\n".format(get_func(children[-1]), rem)
        elif len(children) > 1:
            body += "{}({})\n".format(get_func(children[-1]), rem)

        for child in pnode.children:
            queue.put(child)
    elif pnode.recursion:
        return
    elif pnode.strategy_verified:  # call database
        tiling = pnode.eqv_path_objects[-1]
        if  (len(tiling.obstructions) == 1 and
                 len(tiling.obstructions[0]) == 1):
            body += ("if n == 0:\n"
                     "\tans=1\n"
                     "else:\n"
                     "\tans=0\n")
        elif pnode.eqv_path_objects[0].is_point_tiling():
            body += ("if n == 1:\n"
                     "\tans=1\n"
                     "else:\n"
                     "\tans=0\n")
        else:
            body += db_lookup(pnode)

    body += mem_save(func)
    body += "return ans\n\n"

    funcs[func] = body

if tree:
    queue.put(tree.root)
    while not queue.empty():
        get_rec(queue.get())
    with open("temp.py", 'w') as f:
        print(prog_header(), file=f)
        for func, body in funcs.items():
            print(func_header(func), file=f)
            for line in body.split('\n'):
                print("\t"+line, file=f)
    from temp import F_0
    for i in range(1000):
        print(i, F_0(i))

#print(json.dumps(tree.to_jsonable()))
