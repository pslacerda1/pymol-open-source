from pymol import cmd
from typing import List, Union, Any, Tuple
from pathlib import Path
from enum import StrEnum


def test_docstring():
    @cmd.new_command
    def func1():
        """docstring"""
    assert func1.__doc__ == "docstring"


def test_bool(capsys):
    @cmd.new_command
    def func2(a: bool, b: bool):
        assert a
        assert not b

    cmd.do("func2 yes, 0")
    out, err = capsys.readouterr()
    assert out == '' and err == ''


def test_generic(capsys):
    @cmd.new_command
    def func3(
        nullable_point: Tuple[float, float, float],
        my_var: Union[int, float] = 10,
        my_foo: Union[int, float] = 10.0,
        extended_calculation: bool = True,
        old_style: Any = "Old behavior"
    ):
        assert nullable_point == (1., 2., 3.)
        assert extended_calculation
        assert isinstance(my_var, int)
        assert isinstance(my_foo, float)
        assert old_style == "Old behavior"

    cmd.do("func3 nullable_point=1 2 3, my_foo=11.0")
    out, err = capsys.readouterr()
    assert out + err == ''

def test_path(capsys):
    @cmd.new_command
    def func4(dirname: Path = Path('.')):
        assert dirname.exists()
    cmd.do('func4 ..')
    cmd.do('func4')
    out, err = capsys.readouterr()
    assert out + err == ''

def test_any(capsys):
    @cmd.new_command
    def func5(old_style: Any):
        assert old_style != "RuntimeError"
    func5(RuntimeError)
    cmd.do("func5 RuntimeError")
    out, err = capsys.readouterr()
    assert 'AssertionError' in out+err

def test_list(capsys):
    @cmd.new_command
    def func6(a: List):
        assert a[1] == "2"
    cmd.do("func6 1 2 3")
    out, err = capsys.readouterr()
    assert out + err == ''

    @cmd.new_command
    def func7(a: List[int]):
        assert a[1] == 2
    cmd.do("func7 1 2 3")
    out, err = capsys.readouterr()
    assert out + err == ''

def test_tuple(capsys):
    @cmd.new_command
    def func8(a: Tuple[str, int]):
        assert a == ("fooo", 42)
    cmd.do("func8 fooo 42")
    out, err = capsys.readouterr()
    assert out + err == ''

def test_parse_docs():
    @cmd.new_command
    def func9(
        # multiline
        # documentation works
        foo: int, # inline
        a: str,
        # bar are strings
        bar: Tuple[str, int], # continued...
        b: Any = 10, # The new old age
        # aaaa
        c: Any = 'a' # b
    ):
        "main description"
        pass

    assert func9.__arg_docs['foo'] == "multiline documentation works inline"
    assert func9.__arg_docs['a'] == ""
    assert func9.__arg_docs['bar'] == "bar are strings continued..."
    assert func9.__arg_docs['b'] == 'The new old age'
    assert func9.__arg_docs['c'] == 'aaaa b'
    assert func9.__annotations__['foo'] == int
    assert func9.__annotations__['bar'] == Tuple[str, int]

def test_default(capsys):
    @cmd.new_command
    def func10(a: str="sele"):
        assert a == "sele"
    cmd.do('func10')
    out, err = capsys.readouterr()
    assert out + err == ''

def test_str_enum(capsys):
    class E(StrEnum):
        A = "a"
    @cmd.new_command
    def func11(e: E):
        assert e == E.A
        assert isinstance(e, E)
    cmd.do('func11 a')
    out, err = capsys.readouterr()
    assert out + err == ''