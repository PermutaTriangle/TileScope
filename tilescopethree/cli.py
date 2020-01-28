import argparse

from comb_spec_searcher import StrategyPack
from tilescopethree import StrategyPacks, TileScopeTHREE
from tilings import Tiling


def list_stratpacks(args):
    """
    Prints out every strategy pack available.
    """
    for pack in dir(StrategyPacks):
        if isinstance(getattr(StrategyPacks, pack), StrategyPack):
            print(pack)
    return 0


def search_tree(args):
    """
    Search for a tree.
    """
    print('searching for a tree')
    try:
        pack_to_run = getattr(StrategyPacks, args.strategy_pack)
    except AttributeError as e:
        print("Strategy pack '{}' was not found".format(args.strategy_pack))
        return 1
    start_class = Tiling.from_string(args.basis)
    css = TileScopeTHREE(start_class, pack_to_run)
    css.auto_search(status_update=30)
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='A command line tool for the Periscope algorithm.'
    )
    subparsers = parser.add_subparsers(title='subcommands')
    # List command
    parser_list = subparsers.add_parser('list', help='List all the strategy '
                                        'packs available.')
    parser_list.set_defaults(func=list_stratpacks)
    # Tree command
    parser_tree = subparsers.add_parser('tree', help='Search for a tree with '
                                        'for a given permutation class with a '
                                        'given strategy pack.')
    parser_tree.add_argument('basis', type=str, help='The basis of the '
                             'permutation class. The permutation can be 1 or '
                             '0-based and are separated by an underscore')
    parser_tree.add_argument('strategy_pack', type=str, help='The strategy '
                             'pack to run. The strategy defines the set of '
                             'strategy that will be used to  expand the '
                             'universe of combinatorial classes.')
    parser_tree.set_defaults(func=search_tree)
    # Running the parsers
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    main()
