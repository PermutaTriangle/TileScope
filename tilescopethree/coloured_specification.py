"""A specification for keeping track of regions of tilings.

We create a set Rules from the input of a proof tree. The Rule class has
    Rule: start_tiling, end_tiling, forward_map, constructor
and from any rule it should be possible to get an equation. The Colour class
has
    Colour: tilings -> cells which have this colour
and each Colour will return a unique catalytic variable. A Specification is
then a set of rules and colours
    Spec: Rules, Colours.
Each tiling in the specification will appear once as a start_tiling in a rule,
and have a unique function/variable assigneb to it.
"""

from grids_three import Tiling
from regions import parse_formal_step

class Rule:
    """A class for a combinatorial rule of tilings. It keeps track of how the
    regions of the tiling change when the strategy is applied."""
    def __init__(self, start_tiling, formal_step, constructor):
        self.start_tiling = start_tiling
        self.formal_step = formal_step
        self.constructor = constructor
        strategy = parse_formal_step(formal_step)
        self.end_tilings, self.forwards_maps = strategy(start_tiling)


def Colour:
    """A colour represents a region of points within the specification that is
    traced by applying strategies."""
    def __init__(self, initial_tiling, initial_region, spec):
        self.initial_tiling = initial_tiling
        self.initial_region = initial_region
        self.specification = spec



if __name__ == "__main__":
    import json
    from comb_spec_searcher import ProofTree
    with open("tree.txt", 'r') as f:
        string = list(f)[0]
        d = json.loads(string)
        tree = ProofTree.from_dict(Tiling, d)

    for node in tree.nodes():
        print(node.formal_step)
        try:
            if not node.recursion and not node.strategy_verified:
                constructor = ("disjoint" if node.disjoint_union
                               else "cartesian")
                Rule(node.eqv_path_objects[0], node.formal_step, constructor)
            print()
        except Exception as e:
            print(e)
            print()
            continue

