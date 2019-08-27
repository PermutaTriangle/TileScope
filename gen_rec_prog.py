import json
import sys
from queue import Queue

from tilescopethree import *
from tilescopethree.strategies import one_by_one_verification
from tilescopethree.strategy_packs import point_placements_db

from comb_spec_searcher import *
from permuta import *
from tilings import *

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
    tree = t.auto_search(verbose=True, status_update=30)

queue = Queue()

funcs = dict()  # Dictionary from function names to function bodies


def prog_header():
    '''
        Creates a header for the recurrence relation program
        with necessary imports and dictionaries required
        by the program.
    '''
    return ("from collections import defaultdict\n"
            "mem = defaultdict(dict)\n\n"
            "import sys\n"
            "sys.setrecursionlimit(10**6)\n"
            "from sympy import Poly, abc, sympify, var\n"
            "from tilings.db_conf import taylor_expand\n"
            "from tilings import Tiling, Obstruction, Requirement\n"
            "from permuta import Perm\n"
            "genfs = dict()\n\n")


def get_func(pnode):
    '''
        Returns the name of pnode
    '''
    return str(pnode.get_function())[:-3]


def func_header(func):
    '''
        Returns the function signature given the name of the function.
    '''
    return "def {}(n):".format(func)


def mem_lookup(func):
    '''
        Given a func returns code that will check if the value
        for the given parameters has been computed already and if so,
        returns that value.
    '''
    return ("if n in mem['{}']:\n"
            "\treturn mem['{}'][n]\n").format(func, func)


def mem_save(func):
    '''
        Remember the value computed for given parameters.
    '''
    return "mem['{}'][n] = ans\n".format(func)


def db_lookup(pnode):
    '''
        Computes or looks up the generating function for a verified
        node and then stores it for future use.
    '''
    return ("if '{}' in genfs:\n"
            "\tcoeffs = taylor_expand(genfs['{0}'],n=n+expand_each_time-1)\n"
            "\tfor i, coeff in enumerate(coeffs[n:]):\n"
            "\t\tmem['{0}'][(n+i)] = coeff\n"
            "\tans = coeffs[n]\n"
            "else:\n"
            "\tgenf = None\n"
            "\tgenf = {}.get_genf()\n"
            "\tans = taylor_expand(genf, n=n)[-1]\n"
            "\tgenfs['{}'] = genf\n"
            ).format(get_func(pnode), get_func(pnode),
                     repr(pnode.eqv_path_objects[-1]),
                     get_func(pnode))


def base_case(pnode):
    '''
        Finds all the required base cases for a given node.
        Base cases are:
            - There are no objects of negative length
    '''
    return ("if n < 0:\n"
            "\treturn 0\n")


def get_rec(pnode):
    func = get_func(pnode)

    body = base_case(pnode)
    body += mem_lookup(func)

    if pnode.disjoint_union:
        body += ("ans = " +
                 " + ".join([get_func(child) + "(n)"
                             for child in pnode.children]) + "\n")
        for child in pnode.children:
            queue.put(child)
    elif pnode.decomposition:
        atoms = 0  # Number of children that are just the atom
        # Number of children that are positive (do not contain epsilon)
        pos_children = 0
        children = []  # A list of children that are not atoms
        for child in pnode.children:
            '''
                Disjoint union will just return the sum of all
                the children with the correct function signatures.
            '''
            if child.eqv_path_objects[-1].is_atom():
                atoms += 1
            else:
                if child.eqv_path_objects[-1].is_positive():
                    pos_children += 1
                children.append(child)
        ind = 0  # index variable
        # the remainder (how many points we have left to distribute)
        rem = "n+1"
        body += "ans = 0\n"
        for i, child in enumerate(children[:-1]):
            if child.eqv_path_objects[-1].is_positive():
                start = 1  # If the child is positive then it contains no length 0 objects
                # so we start with length 1 objects
                pos_children -= 1
            else:
                start = 0
            tabs = '\t' * i
            body += "{}for {} in range({},{}-{}):\n".format(tabs,
                                                            "i" + str(ind), start, rem, atoms + pos_children)
            # We chose i{ind} points for this child so we subtract
            rem += "-{}".format("i" + str(ind))
            # that many points
            ind += 1

        ind = 0
        if atoms == 0:
            rem = "n"
        else:
            rem = "n-{}".format(atoms)

        tabs = '\t' * (len(children) - 1)
        body += "{}ans += ".format(tabs)

        for child in children[:-1]:
            body += "{}({}) * ".format(get_func(child), "i" + str(ind))
            rem += "-{}".format("i" + str(ind))
            ind += 1

        body += "{}({})\n".format(get_func(children[-1]), rem)

        for child in pnode.children:
            queue.put(child)

    elif pnode.recursion:
        return
    elif pnode.strategy_verified:  # call database
        if pnode.eqv_path_objects[-1].is_epsilon():
            body += ("if n == 0:\n"
                     "\tans = 1\n"
                     "else:\n"
                     "\tans = 0\n")
        elif pnode.eqv_path_objects[-1].is_atom():
            body += ("if n == 1:\n"
                     "\tans = 1\n"
                     "else:\n"
                     "\tans = 0\n")
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
                print("\t" + line, file=f)

    from temp import F_0
    for i in range(100):
        print(i, F_0(i))
