from sympy import diff, sympify, symbols
from sympy.abc import x
from grids import Tiling, Factor, Block, PositiveClass, lex_min
from permuta import Av
from functools import reduce
from operator import add, mul
from math import factorial

from pymongo import MongoClient
mongo = MongoClient('mongodb://webapp:c73f12a3@tagl.is:27017/permsdb')

__all__ = ["get_tiling_genf", "genf_from_db", "factor_from_db", "permeval", "taylor_expand"]

def get_tiling_genf(tiling, identifier, inp_set, root_func):
    factorEqs = []
    for factor in tiling.find_factors():
        eq = factor_from_db(factor)
        if eq:
            factorEqs.append(eq)
            continue
        func = 0
        pos = False
        sets = 0
        for k, v in factor.factor.items():
            w = v if v == Block.point else (Av(v.basis) if isinstance(v, PositiveClass) else v)
            if len(factor) == 1:
                if w == inp_set:
                    factorEqs.append(root_func - (1 if isinstance(v, PositiveClass) else 0))
                    break
                ext_genf = genf_from_db(v)
                if ext_genf == None:
                    raise RuntimeError("Cannot find generating function for " + str(identifier) + " because generating function for " + repr(v) + " is unknown")
                factorEqs.append(ext_genf - (1 if isinstance(v, PositiveClass) else 0))
                break
            if v is not Block.point:
                pos = isinstance(v,PositiveClass)
                ext_genf = genf_from_db(v)
                if ext_genf == None:
                    raise RuntimeError("Cannot find generating function for " + str(identifier) + " because generating function for " + repr(v) + " is unknown")
                func = ext_genf
                sets += 1
        else:
            if sets > 1:
                raise RuntimeError("Unknown factor found \n" + str(factor))
            if func:
                points = len(factor.factor)-1
                eq = x*diff(x*(func - (1 if pos else 0)),x)
                for _ in range(points-1):
                    eq = x*diff(x*eq,x)
                factorEqs.append(eq.doit())
            else:
                points = len(factor.factor)
                factorEqs.append(factorial(points)*x**points)
    return reduce(mul, factorEqs, 1)


def genf_from_db(inputset):
    permset = Av(lex_min(list(inputset.basis)))
    avoid = '_'.join([''.join([str(i+1) for i in perm]) for perm in permset.basis])
    result = mongo.permsdb.perm.find_one({'avoid':avoid})
    if not result or 'sympy_genf' not in result:
        return None
    res = result['sympy_genf']
    for c in "BCDEFGH":
        if c in res:
            return None
    return sympify(result['sympy_genf'])

def factor_from_db(factor):
    key = factor.minimum()
    result = mongo.permsdb.factor.find_one({'factor':str(key)})
    if not result:
        return None
    return sympify(result['genf'])

def taylor_expand(gen_func, terms=10):
    coeffs = []
    fac = 1
    gen_func = gen_func.series(n=terms+1)
    for i in range(terms+1):
        coeffs.append(gen_func.subs(x, 0)//fac)
        gen_func = diff(gen_func)
        fac *= (i+1)

    return coeffs

def permeval(text):
    if text.startswith("Av+"):
        return PositiveClass(eval("Av([" + text[4:-1]+"])"))
    elif text.startswith("Av"):
        return eval("Av([" + text[3:-1]+"])")
    else:
        return Block.point
