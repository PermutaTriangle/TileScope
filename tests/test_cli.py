import os

import pytest


def test_entrypoints():
    exit_status = os.system('permscope --help')
    assert exit_status == 0
    exit_status = os.system('permscope list --help')
    assert exit_status == 0
    exit_status = os.system('permscope tree --help')
    assert exit_status == 0


def test_list():
    exit_status = os.system('permscope list')
    assert exit_status == 0


@pytest.mark.timeout(20)
def test_tree():
    exit_status = os.system('permscope tree 132 point_placements')
    assert exit_status == 0
    exit_status = os.system('permscope tree 132')
    assert exit_status != 0
    exit_status = os.system('permscope tree point_placements')
    assert exit_status != 0
