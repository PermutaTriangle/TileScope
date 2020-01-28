from tilings.algorithms.enumeration import DatabaseEnumeration


def database_verified(tiling, **kwargs):
    return DatabaseEnumeration(tiling).verification_rule()
