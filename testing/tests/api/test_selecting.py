from pymol import cmd
from pymol import test_utils


def test_float_operators():
    cmd.reinitialize()
    cmd.pseudoatom(pos=[1, 2, 3], b=5)

    assert cmd.count_atoms("b >= 4 & b == 5 & b=5") == 1
    assert cmd.count_atoms("pc. < 1.2 & fc. == 0") == 1
    assert cmd.count_atoms("x=1 & y >= 2.0 & z <=3") == 1
